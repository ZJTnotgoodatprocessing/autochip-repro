"""Candidate ranker — scores Verilog candidates per AutoChip ranking rules.

Ranking rules:
  -2.0  no valid Verilog extracted
  -1.0  compilation failed
  -0.5  compiled with warnings (no sim result)
   0~1  (total_samples - mismatches) / total_samples
"""

from src.runner.verilog_executor import CompileResult, SimResult


def rank(compile_result: CompileResult | None, sim_result: SimResult | None) -> float:
    """Return a numeric rank for a single candidate."""
    if compile_result is None:
        return -2.0

    if not compile_result.success:
        return -1.0

    if sim_result is None or sim_result.total_samples == 0:
        # Compiled but no sim data available
        return -0.5 if compile_result.has_warnings else 0.0

    return (sim_result.total_samples - sim_result.mismatches) / sim_result.total_samples
