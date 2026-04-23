"""Prompt builder — constructs initial and feedback prompts for the AutoChip loop.

Supports multiple feedback granularity levels for ablation experiments:
  - compile_only:  Only compilation errors, no simulation info.
  - succinct:      Compilation + succinct simulation summary (DEFAULT / current).
  - rich:          Everything in succinct + detailed simulation output / diffs.
"""

from enum import Enum
from pathlib import Path
from src.runner.verilog_executor import CompileResult, SimResult


class FeedbackMode(str, Enum):
    """Feedback granularity levels.

    Level 0 (zero-shot) and Level 1 (retry-only) are handled in loop_runner,
    not here — those don't use any feedback prompt at all.
    """
    COMPILE_ONLY = "compile_only"  # Level 2: compile errors only
    SUCCINCT = "succinct"          # Level 3: current default
    RICH = "rich"                  # Level 4: detailed sim output


_PROMPTS_DIR = Path(__file__).resolve().parent.parent.parent / "prompts"


def build_initial_prompt(description: str, module_header: str) -> str:
    """Build the zero-shot prompt for the first generation round."""
    return (
        "Generate a Verilog module that satisfies the following description.\n"
        "Return ONLY the Verilog code, no explanations.\n\n"
        f"Description:\n{description}\n\n"
        f"Module interface:\n{module_header}\n\n"
        "Your implementation:"
    )


# ── Feedback summarizers per granularity level ───────────────────────────────


def _summarize_compile_only(
    compile_result: CompileResult | None,
    sim_result: SimResult | None,
) -> str:
    """Level 2: Only compilation feedback. Simulation failures are reported
    as a generic 'simulation did not pass' without details."""
    parts: list[str] = []

    if compile_result and not compile_result.success:
        parts.append("COMPILATION FAILED.")
        stderr = compile_result.stderr.strip()
        if stderr:
            lines = stderr.splitlines()
            if len(lines) > 30:
                lines = lines[:30] + [f"... ({len(lines) - 30} more lines truncated)"]
            parts.append("Compiler errors:\n" + "\n".join(lines))
        return "\n".join(parts)

    # Compilation succeeded — give only a pass/fail for simulation
    if sim_result is None:
        parts.append("Compilation succeeded. Simulation did not produce results.")
    elif sim_result.passed:
        parts.append("All simulation tests passed.")
    else:
        parts.append(
            "Compilation succeeded, but SIMULATION FAILED. "
            "Your design does not produce the expected outputs. "
            "Please review your logic and try again."
        )

    return "\n".join(parts)


def _summarize_succinct(
    compile_result: CompileResult | None,
    sim_result: SimResult | None,
) -> str:
    """Level 3: Compilation errors + succinct simulation summary.
    This is the ORIGINAL / DEFAULT method used throughout all prior experiments."""
    parts: list[str] = []

    if compile_result and not compile_result.success:
        parts.append("COMPILATION FAILED.")
        stderr = compile_result.stderr.strip()
        if stderr:
            lines = stderr.splitlines()
            if len(lines) > 30:
                lines = lines[:30] + [f"... ({len(lines) - 30} more lines truncated)"]
            parts.append("Compiler errors:\n" + "\n".join(lines))
        return "\n".join(parts)

    # Compilation succeeded — check simulation
    if compile_result and compile_result.has_warnings:
        stderr = compile_result.stderr.strip()
        if stderr:
            parts.append(f"Compilation warnings:\n{stderr}")

    if sim_result is None:
        parts.append("Simulation did not produce results.")
        return "\n".join(parts)

    if sim_result.passed:
        parts.append("All simulation tests passed.")
        return "\n".join(parts)

    # Simulation failed — extract useful info
    parts.append(
        f"SIMULATION FAILED: {sim_result.mismatches} mismatched samples "
        f"out of {sim_result.total_samples}."
    )

    # Include simulation output (truncated) for debugging clues
    stdout = sim_result.stdout.strip()
    if stdout:
        lines = stdout.splitlines()
        if len(lines) > 40:
            lines = lines[:40] + [f"... ({len(lines) - 40} more lines truncated)"]
        parts.append("Simulation output:\n" + "\n".join(lines))

    return "\n".join(parts)


def _summarize_rich(
    compile_result: CompileResult | None,
    sim_result: SimResult | None,
) -> str:
    """Level 4: Everything in succinct + detailed simulation log.
    Provides more simulation output lines and explicit guidance."""
    parts: list[str] = []

    if compile_result and not compile_result.success:
        parts.append("COMPILATION FAILED.")
        stderr = compile_result.stderr.strip()
        if stderr:
            lines = stderr.splitlines()
            if len(lines) > 50:
                lines = lines[:50] + [f"... ({len(lines) - 50} more lines truncated)"]
            parts.append("Compiler errors:\n" + "\n".join(lines))
        return "\n".join(parts)

    # Compilation succeeded — include warnings
    if compile_result and compile_result.has_warnings:
        stderr = compile_result.stderr.strip()
        if stderr:
            parts.append(f"Compilation warnings:\n{stderr}")

    if sim_result is None:
        parts.append("Simulation did not produce results.")
        return "\n".join(parts)

    if sim_result.passed:
        parts.append("All simulation tests passed.")
        return "\n".join(parts)

    # Simulation failed — provide rich detail
    parts.append(
        f"SIMULATION FAILED: {sim_result.mismatches} mismatched samples "
        f"out of {sim_result.total_samples}."
    )

    # Extended simulation output (up to 80 lines vs 40 in succinct)
    stdout = sim_result.stdout.strip()
    if stdout:
        lines = stdout.splitlines()
        if len(lines) > 80:
            lines = lines[:80] + [f"... ({len(lines) - 80} more lines truncated)"]
        parts.append("Full simulation output:\n" + "\n".join(lines))

    # Simulation stderr (may contain $display debug messages)
    stderr = sim_result.stderr.strip() if sim_result.stderr else ""
    if stderr:
        se_lines = stderr.splitlines()
        if len(se_lines) > 20:
            se_lines = se_lines[:20] + ["... (truncated)"]
        parts.append("Simulation stderr:\n" + "\n".join(se_lines))

    # Add explicit analysis guidance
    parts.append(
        "\nAnalysis hints:\n"
        "- Check if your state machine transitions are correct.\n"
        "- Verify signal widths and signedness match the expected interface.\n"
        "- Ensure reset logic initializes all registers properly.\n"
        "- Compare your output timing with the expected waveform above."
    )

    return "\n".join(parts)


# ── Dispatch table ───────────────────────────────────────────────────────────

_SUMMARIZERS = {
    FeedbackMode.COMPILE_ONLY: _summarize_compile_only,
    FeedbackMode.SUCCINCT: _summarize_succinct,
    FeedbackMode.RICH: _summarize_rich,
}


def _summarize_feedback(
    compile_result: CompileResult | None,
    sim_result: SimResult | None,
    *,
    mode: FeedbackMode = FeedbackMode.SUCCINCT,
) -> str:
    """Produce a feedback string at the requested granularity level."""
    return _SUMMARIZERS[mode](compile_result, sim_result)


# ── Public prompt builder ────────────────────────────────────────────────────


def build_feedback_prompt(
    description: str,
    module_header: str,
    previous_code: str,
    compile_result: CompileResult | None,
    sim_result: SimResult | None,
    *,
    feedback_mode: FeedbackMode = FeedbackMode.SUCCINCT,
) -> str:
    """Build a feedback prompt using the template at the specified granularity."""
    template_path = _PROMPTS_DIR / "feedback_succinct.txt"
    template = template_path.read_text(encoding="utf-8")

    feedback_text = _summarize_feedback(
        compile_result, sim_result, mode=feedback_mode
    )

    return template.format(
        description=description,
        module_header=module_header,
        previous_code=previous_code,
        feedback=feedback_text,
    )
