"""Run the AutoChip feedback loop on a single task.

Usage:
    python scripts/run_feedback_loop.py --task data/sample_task
    python scripts/run_feedback_loop.py --task data/adder_8bit --k 3 --max-iterations 5
    python scripts/run_feedback_loop.py --task data/population_count --temperature 0.5
"""

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from src.runner.task import load_task
from src.feedback.loop_runner import run_feedback_loop, IterationRecord
from src.llm.client import get_model_name
from src.utils.artifacts import build_run_metadata, create_run_dir, make_run_id, timestamp_now


def _log_iteration(record: IterationRecord) -> None:
    """Print progress for one iteration."""
    parts = []
    for c in record.candidates:
        if c.api_error:
            parts.append(f"API_ERR({c.api_error_type})")
        else:
            parts.append(f"{c.rank:.2f}")
    ranks_str = ", ".join(parts)
    status = "PASS" if record.passed else "FAIL"
    print(
        f"  Iter {record.iteration}: "
        f"candidates=[{ranks_str}]  "
        f"best={record.best_rank:.2f}  "
        f"{status}"
    )


def _serialize_result(result) -> dict:
    """Convert FeedbackLoopResult to a JSON-serializable dict."""
    iterations = []
    for ir in result.iterations:
        candidates = []
        for c in ir.candidates:
            candidates.append({
                "candidate_index": c.candidate_index,
                "prompt": c.prompt,
                "raw_response": c.raw_response,
                "extracted_verilog": c.extracted_verilog,
                "compile_stdout": c.compile_result.stdout if c.compile_result else "",
                "compile_stderr": c.compile_result.stderr if c.compile_result else "",
                "compile_ok": c.compile_result.success if c.compile_result else False,
                "sim_stdout": c.sim_result.stdout if c.sim_result else "",
                "sim_stderr": c.sim_result.stderr if c.sim_result else "",
                "sim_passed": c.sim_result.passed if c.sim_result else False,
                "sim_mismatches": c.sim_result.mismatches if c.sim_result else None,
                "sim_total_samples": c.sim_result.total_samples if c.sim_result else None,
                "rank": c.rank,
                "api_error": c.api_error,
                "api_error_type": c.api_error_type,
                "api_error_message": c.api_error_message,
            })
        iterations.append({
            "iteration": ir.iteration,
            "candidates": candidates,
            "best_candidate_index": ir.best_candidate_index,
            "best_rank": ir.best_rank,
            "passed": ir.passed,
        })

    return {
        "task_name": result.task_name,
        "model_name": result.model_name,
        "temperature": result.temperature,
        "k": result.k,
        "max_iterations": result.max_iterations,
        "total_iterations": result.total_iterations,
        "best_verilog": result.best_verilog,
        "best_rank": result.best_rank,
        "passed": result.passed,
        "api_error": result.api_error,
        "api_error_type": result.api_error_type,
        "api_error_message": result.api_error_message,
        "iterations": iterations,
    }


def main():
    parser = argparse.ArgumentParser(description="Run AutoChip feedback loop on a single task")
    parser.add_argument("--task", required=True, help="Path to task directory")
    parser.add_argument("--model", type=str, default=None, help="Override model name (default: ANTHROPIC_MODEL env var)")
    parser.add_argument("--k", type=int, default=3, help="Number of candidates per iteration (default: 3)")
    parser.add_argument("--max-iterations", type=int, default=5, help="Maximum feedback iterations (default: 5)")
    parser.add_argument("--temperature", type=float, default=0.7, help="LLM temperature (default: 0.7)")
    args = parser.parse_args()

    if args.model:
        os.environ["ANTHROPIC_MODEL"] = args.model

    # Load task
    task = load_task(args.task)

    print(f"=== AutoChip Feedback Loop ===")
    print(f"Task:           {task.name}")
    print(f"Model:          {get_model_name()}")
    print(f"Candidates/iter: {args.k}")
    print(f"Max iterations: {args.max_iterations}")
    print(f"Temperature:    {args.temperature}")
    print()

    # Run
    result = run_feedback_loop(
        task,
        k=args.k,
        max_iterations=args.max_iterations,
        temperature=args.temperature,
        on_iteration=_log_iteration,
    )

    # Summary
    print()
    print(f"--- Result ---")
    print(f"Total iterations: {result.total_iterations}")
    print(f"Best rank:        {result.best_rank:.2f}")
    print(f"Passed:           {result.passed}")
    if result.api_error:
        print(f"API Error:        {result.api_error_type}: {result.api_error_message}")

    if result.best_verilog:
        print(f"\n--- Best Verilog ---")
        print(result.best_verilog)

    # Save output
    timestamp = timestamp_now()
    run_id = make_run_id(f"feedback_{task.name}", timestamp)
    run_dir = create_run_dir("feedback", run_id)

    data = {
        "metadata": build_run_metadata(
            run_id=run_id,
            script_path="scripts/run_feedback_loop.py",
            model_name=result.model_name,
            timestamp=timestamp,
            run_kind="single_task_feedback",
            parameters={
                "task": args.task,
                "k": args.k,
                "max_iterations": args.max_iterations,
                "temperature": args.temperature,
            },
            source_inputs={
                "task_dir": str(Path(args.task).resolve()),
                "testbench_path": str(task.testbench_path),
            },
        ),
        "result": _serialize_result(result),
    }

    result_file = run_dir / "result.json"
    result_file.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\n[Saved] {result_file}")


if __name__ == "__main__":
    main()
