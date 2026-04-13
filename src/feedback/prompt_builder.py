"""Prompt builder — constructs initial and feedback prompts for the AutoChip loop."""

from pathlib import Path
from src.runner.verilog_executor import CompileResult, SimResult


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


def _summarize_feedback(
    compile_result: CompileResult | None,
    sim_result: SimResult | None,
) -> str:
    """Produce a succinct feedback string from compile/sim results."""
    parts: list[str] = []

    if compile_result and not compile_result.success:
        parts.append("COMPILATION FAILED.")
        stderr = compile_result.stderr.strip()
        if stderr:
            # Keep only the first 30 lines of compiler errors to stay succinct
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


def build_feedback_prompt(
    description: str,
    module_header: str,
    previous_code: str,
    compile_result: CompileResult | None,
    sim_result: SimResult | None,
) -> str:
    """Build a succinct feedback prompt using the template."""
    template_path = _PROMPTS_DIR / "feedback_succinct.txt"
    template = template_path.read_text(encoding="utf-8")

    feedback_text = _summarize_feedback(compile_result, sim_result)

    return template.format(
        description=description,
        module_header=module_header,
        previous_code=previous_code,
        feedback=feedback_text,
    )
