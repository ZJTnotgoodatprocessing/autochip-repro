"""Verilog executor — iverilog compile + vvp simulate wrappers."""

import re
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path


@dataclass
class CompileResult:
    success: bool
    has_warnings: bool = False
    stdout: str = ""
    stderr: str = ""


@dataclass
class SimResult:
    passed: bool = False
    total_samples: int = 0
    mismatches: int = 0
    stdout: str = ""
    stderr: str = ""


def compile(verilog_code: str, testbench_path: Path, work_dir: Path | None = None) -> CompileResult:
    """Compile *verilog_code* together with *testbench_path* using iverilog.

    If *work_dir* is None a temporary directory is created (and returned inside
    the result so the caller can run simulate() afterwards).
    """
    if work_dir is None:
        work_dir = Path(tempfile.mkdtemp(prefix="autochip_"))

    design_path = work_dir / "design.v"
    design_path.write_text(verilog_code, encoding="utf-8")
    out_path = work_dir / "sim.out"

    proc = subprocess.run(
        ["iverilog", "-g2012", "-o", str(out_path), str(design_path), str(testbench_path)],
        capture_output=True,
        text=True,
        timeout=30,
    )

    log = (proc.stdout + proc.stderr).strip()
    success = proc.returncode == 0
    has_warnings = success and ("warning" in log.lower())

    result = CompileResult(
        success=success,
        has_warnings=has_warnings,
        stdout=proc.stdout.strip(),
        stderr=proc.stderr.strip(),
    )
    # Attach work_dir and out_path so caller can find compiled binary
    result._work_dir = work_dir  # type: ignore[attr-defined]
    result._out_path = out_path  # type: ignore[attr-defined]
    return result


def simulate(compiled_path: Path) -> SimResult:
    """Run vvp on a compiled iverilog binary and parse mismatch info."""
    if not compiled_path.exists():
        return SimResult(stderr="Compiled binary not found")

    proc = subprocess.run(
        ["vvp", str(compiled_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )

    stdout = proc.stdout.strip()
    stderr = proc.stderr.strip()

    # Parse VerilogEval-style output:
    #   "Hint: Total mismatched samples is 0 out of 256 samples"
    m = re.search(r"mismatched samples is (\d+) out of (\d+)", stdout)
    if m:
        mismatches = int(m.group(1))
        total = int(m.group(2))
        return SimResult(
            passed=(mismatches == 0),
            total_samples=total,
            mismatches=mismatches,
            stdout=stdout,
            stderr=stderr,
        )

    # If we can't parse mismatch info, check return code at least
    return SimResult(passed=(proc.returncode == 0), stdout=stdout, stderr=stderr)
