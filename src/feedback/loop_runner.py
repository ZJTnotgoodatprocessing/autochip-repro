"""Feedback loop runner — core AutoChip iterative generation logic.

Implements:
  Round 1: generate k candidates, compile/sim/rank each, pick the best.
  Rounds 2..N: if best didn't pass, build a succinct feedback prompt and
               generate k new candidates, repeat.
  Stops when: rank == 1.0 (pass) OR iteration count reaches max_iterations.

API errors (after retry exhaustion) are captured in FeedbackLoopResult
rather than crashing the entire batch run.
"""

from dataclasses import dataclass, field
from pathlib import Path

from src.llm.client import generate, generate_with_history, get_model_name, APIError
from src.utils.extract_verilog import extract_modules
from src.runner.task import Task
from src.runner.verilog_executor import (
    CompileResult,
    SimResult,
    compile as verilog_compile,
    simulate as verilog_simulate,
)
from src.ranking.ranker import rank as compute_rank
from src.feedback.prompt_builder import (
    build_initial_prompt, build_feedback_prompt, FeedbackMode, PromptStrategy,
    build_multiturn_initial_message, build_multiturn_feedback_message,
)


# ── data structures ──────────────────────────────────────────────────────────


@dataclass
class CandidateResult:
    """Result for a single LLM candidate within one iteration."""
    candidate_index: int
    prompt: str
    raw_response: str
    extracted_verilog: str | None
    compile_result: CompileResult | None
    sim_result: SimResult | None
    rank: float
    api_error: bool = False
    api_error_type: str | None = None
    api_error_message: str | None = None


@dataclass
class IterationRecord:
    """Full record for one iteration (all k candidates)."""
    iteration: int
    candidates: list[CandidateResult] = field(default_factory=list)
    best_candidate_index: int = -1
    best_rank: float = -2.0
    passed: bool = False


@dataclass
class FeedbackLoopResult:
    """Final output of the entire feedback loop run."""
    task_name: str
    model_name: str
    temperature: float
    k: int
    max_iterations: int
    iterations: list[IterationRecord] = field(default_factory=list)
    total_iterations: int = 0
    best_verilog: str | None = None
    best_rank: float = -2.0
    passed: bool = False
    api_error: bool = False
    api_error_type: str | None = None
    api_error_message: str | None = None


# ── helpers ──────────────────────────────────────────────────────────────────


def _evaluate_candidate(
    verilog_code: str | None,
    testbench_path: Path,
) -> tuple[CompileResult | None, SimResult | None, float]:
    """Compile, simulate, and rank a single candidate. Returns (comp, sim, rank)."""
    if verilog_code is None:
        return None, None, -2.0

    comp = verilog_compile(verilog_code, testbench_path)
    if not comp.success:
        return comp, None, compute_rank(comp, None)

    sim = verilog_simulate(comp._out_path)  # type: ignore[attr-defined]
    score = compute_rank(comp, sim)
    return comp, sim, score


def _generate_one_candidate(prompt: str, temperature: float):
    """Generate a single candidate. Returns (raw_response, extracted_verilog, api_error_info).

    api_error_info is None on success, or (error_type, error_message) on failure.
    """
    try:
        raw = generate(prompt, temperature=temperature)
        modules = extract_modules(raw)
        verilog = modules[0] if modules else None
        return raw, verilog, None
    except APIError as e:
        return "", None, (e.error_type, str(e))


# ── main loop ────────────────────────────────────────────────────────────────


def run_feedback_loop(
    task: Task,
    *,
    k: int = 3,
    max_iterations: int = 5,
    temperature: float = 0.7,
    no_feedback: bool = False,
    feedback_mode: FeedbackMode = FeedbackMode.SUCCINCT,
    prompt_strategy: PromptStrategy = PromptStrategy.BASE,
    on_iteration: callable = None,
) -> FeedbackLoopResult:
    """Run the AutoChip feedback loop on a single task.

    Args:
        no_feedback: If True, run in "retry-only" mode — all iterations use the
            initial prompt without any error feedback. This is the ablation
            condition for separating "multiple attempts" from "feedback value".

    API errors (after retry exhaustion) are captured in the result rather
    than raised. If ALL candidates in an iteration fail due to API errors,
    the loop stops early and marks the result with api_error=True.
    """
    model_name = get_model_name()
    result = FeedbackLoopResult(
        task_name=task.name,
        model_name=model_name,
        temperature=temperature,
        k=k,
        max_iterations=max_iterations,
    )

    global_best_verilog: str | None = None
    global_best_rank: float = -2.0
    global_best_comp: CompileResult | None = None
    global_best_sim: SimResult | None = None

    initial_prompt = build_initial_prompt(
        task.description, task.module_header, strategy=prompt_strategy,
    )

    for iteration_num in range(1, max_iterations + 1):
        iter_record = IterationRecord(iteration=iteration_num)

        # ── build prompt ─────────────────────────────────────────────────
        if iteration_num == 1 or no_feedback:
            # Round 1 always uses initial prompt.
            # In retry-only mode, ALL rounds use initial prompt (no error info).
            prompt = initial_prompt
        else:
            prompt = build_feedback_prompt(
                description=task.description,
                module_header=task.module_header,
                previous_code=global_best_verilog or "(no valid code generated)",
                compile_result=global_best_comp,
                sim_result=global_best_sim,
                feedback_mode=feedback_mode,
            )

        # ── generate k candidates ────────────────────────────────────────
        all_api_errors = True
        last_api_error_type = None
        last_api_error_msg = None

        for idx in range(k):
            raw, verilog, api_err = _generate_one_candidate(prompt, temperature)

            if api_err is not None:
                # API error — record it but don't evaluate
                cr = CandidateResult(
                    candidate_index=idx,
                    prompt=prompt,
                    raw_response="",
                    extracted_verilog=None,
                    compile_result=None,
                    sim_result=None,
                    rank=-2.0,
                    api_error=True,
                    api_error_type=api_err[0],
                    api_error_message=api_err[1],
                )
                last_api_error_type = api_err[0]
                last_api_error_msg = api_err[1]
            else:
                all_api_errors = False
                comp, sim, score = _evaluate_candidate(verilog, task.testbench_path)
                cr = CandidateResult(
                    candidate_index=idx,
                    prompt=prompt,
                    raw_response=raw,
                    extracted_verilog=verilog,
                    compile_result=comp,
                    sim_result=sim,
                    rank=score,
                )

            iter_record.candidates.append(cr)

            # Update iteration-level best (only non-api-error candidates)
            if not cr.api_error and cr.rank > iter_record.best_rank:
                iter_record.best_rank = cr.rank
                iter_record.best_candidate_index = idx

        # ── check if all candidates failed with API errors ───────────────
        if all_api_errors:
            result.api_error = True
            result.api_error_type = last_api_error_type
            result.api_error_message = last_api_error_msg
            result.iterations.append(iter_record)
            if on_iteration:
                on_iteration(iter_record)
            break

        # ── update global best ───────────────────────────────────────────
        if iter_record.best_candidate_index >= 0:
            best_in_iter = iter_record.candidates[iter_record.best_candidate_index]
            if best_in_iter.rank > global_best_rank:
                global_best_rank = best_in_iter.rank
                global_best_verilog = best_in_iter.extracted_verilog
                global_best_comp = best_in_iter.compile_result
                global_best_sim = best_in_iter.sim_result

        iter_record.passed = (global_best_rank == 1.0)
        result.iterations.append(iter_record)

        if on_iteration:
            on_iteration(iter_record)

        if global_best_rank == 1.0:
            break

    result.total_iterations = len(result.iterations)
    result.best_verilog = global_best_verilog
    result.best_rank = global_best_rank
    result.passed = (global_best_rank == 1.0)
    return result


# ── Multi-turn feedback loop ────────────────────────────────────────────────


def _generate_multiturn_candidate(messages: list[dict], temperature: float):
    """Generate a candidate using multi-turn conversation history.

    Returns (raw_response, extracted_verilog, api_error_info).
    """
    try:
        raw = generate_with_history(messages, temperature=temperature)
        modules = extract_modules(raw)
        verilog = modules[0] if modules else None
        return raw, verilog, None
    except APIError as e:
        return "", None, (e.error_type, str(e))


def run_multiturn_feedback_loop(
    task: Task,
    *,
    k: int = 1,
    max_iterations: int = 5,
    temperature: float = 0.7,
    feedback_mode: FeedbackMode = FeedbackMode.SUCCINCT,
    on_iteration: callable = None,
) -> FeedbackLoopResult:
    """Run a multi-turn conversational feedback loop on a single task.

    Unlike run_feedback_loop (single-turn), this function:
      - Maintains a growing list of (user, assistant) message pairs
      - Sends the full conversation history with each API call
      - The model can see all its previous attempts and feedback

    Note: Multi-turn uses k=1 per iteration by design. Each turn is a
    sequential refinement in a single conversation thread. Using k>1
    would require k independent conversation threads.
    """
    model_name = get_model_name()
    result = FeedbackLoopResult(
        task_name=task.name,
        model_name=model_name,
        temperature=temperature,
        k=k,
        max_iterations=max_iterations,
    )

    # Conversation history: alternating user/assistant messages
    conversation: list[dict] = []

    global_best_verilog: str | None = None
    global_best_rank: float = -2.0

    # last_iter_comp/sim tracks the LAST iteration's best candidate result.
    # This is what the model just generated (visible in conversation history),
    # so feedback must describe THIS code's errors, not the global best's.
    last_iter_comp: CompileResult | None = None
    last_iter_sim: SimResult | None = None

    for iteration_num in range(1, max_iterations + 1):
        iter_record = IterationRecord(iteration=iteration_num)

        # ── build user message ───────────────────────────────────────────
        if iteration_num == 1:
            user_msg = build_multiturn_initial_message(
                task.description, task.module_header
            )
        else:
            # Use last_iter (not global_best) so feedback matches the code
            # the model can see as its last response in the conversation.
            user_msg = build_multiturn_feedback_message(
                last_iter_comp, last_iter_sim,
                feedback_mode=feedback_mode,
            )

        conversation.append({"role": "user", "content": user_msg})

        # ── generate candidates (k threads, each with own conversation) ──
        all_api_errors = True
        last_api_error_type = None
        last_api_error_msg = None

        for idx in range(k):
            raw, verilog, api_err = _generate_multiturn_candidate(
                conversation, temperature
            )

            if api_err is not None:
                cr = CandidateResult(
                    candidate_index=idx,
                    prompt=user_msg,
                    raw_response="",
                    extracted_verilog=None,
                    compile_result=None,
                    sim_result=None,
                    rank=-2.0,
                    api_error=True,
                    api_error_type=api_err[0],
                    api_error_message=api_err[1],
                )
                last_api_error_type = api_err[0]
                last_api_error_msg = api_err[1]
            else:
                all_api_errors = False
                comp, sim, score = _evaluate_candidate(
                    verilog, task.testbench_path
                )
                cr = CandidateResult(
                    candidate_index=idx,
                    prompt=user_msg,
                    raw_response=raw,
                    extracted_verilog=verilog,
                    compile_result=comp,
                    sim_result=sim,
                    rank=score,
                )

            iter_record.candidates.append(cr)

            if not cr.api_error and cr.rank > iter_record.best_rank:
                iter_record.best_rank = cr.rank
                iter_record.best_candidate_index = idx

        # ── check if all failed ──────────────────────────────────────────
        if all_api_errors:
            result.api_error = True
            result.api_error_type = last_api_error_type
            result.api_error_message = last_api_error_msg
            result.iterations.append(iter_record)
            # Remove the unanswered user message from conversation
            conversation.pop()
            if on_iteration:
                on_iteration(iter_record)
            break

        # ── update global best & conversation history ────────────────────
        if iter_record.best_candidate_index >= 0:
            best_in_iter = iter_record.candidates[iter_record.best_candidate_index]
            # Add the best assistant response to conversation history
            conversation.append({
                "role": "assistant",
                "content": best_in_iter.raw_response,
            })

            # Always update last_iter to match what's now in conversation
            last_iter_comp = best_in_iter.compile_result
            last_iter_sim = best_in_iter.sim_result

            # Only update global best if this iteration improved
            if best_in_iter.rank > global_best_rank:
                global_best_rank = best_in_iter.rank
                global_best_verilog = best_in_iter.extracted_verilog

        iter_record.passed = (global_best_rank == 1.0)
        result.iterations.append(iter_record)

        if on_iteration:
            on_iteration(iter_record)

        if global_best_rank == 1.0:
            break

    result.total_iterations = len(result.iterations)
    result.best_verilog = global_best_verilog
    result.best_rank = global_best_rank
    result.passed = (global_best_rank == 1.0)
    return result

