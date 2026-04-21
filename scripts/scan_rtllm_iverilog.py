"""Scan all RTLLM designs for iverilog compatibility.

For each design:
1. Read the verified reference .v file
2. Rename the module to match testbench expectations
3. Try iverilog compile with the testbench
4. If compile succeeds, try vvp simulate
5. Report results
"""

import re
import subprocess
import tempfile
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent

import sys
sys.path.insert(0, str(PROJECT))

from src.runner.rtllm_loader import discover_all


def scan_one(problem) -> dict:
    """Test one RTLLM problem with its reference design."""
    result = {
        "name": problem.name,
        "category": problem.category,
        "compile": None,
        "simulate": None,
        "error_detail": "",
    }

    if not problem.reference_path or not problem.reference_path.exists():
        result["compile"] = "NO_REF"
        result["error_detail"] = "No reference design found"
        return result

    # Read reference code and fix module name (verified_X -> X)
    ref_code = problem.reference_path.read_text(encoding="utf-8", errors="replace")
    # Replace verified_<name> with <name> for module declaration
    fixed_code = re.sub(
        r'\bmodule\s+verified_' + re.escape(problem.module_name),
        f'module {problem.module_name}',
        ref_code
    )

    d = Path(tempfile.mkdtemp(prefix="rtllm_scan_"))
    design_path = d / "design.v"
    design_path.write_text(fixed_code, encoding="utf-8")
    out_path = d / "sim.out"

    # Compile
    try:
        r1 = subprocess.run(
            ["iverilog", "-g2012", "-o", str(out_path), str(design_path), str(problem.testbench_path)],
            capture_output=True, text=True, timeout=30,
        )
    except Exception as e:
        result["compile"] = "EXCEPTION"
        result["error_detail"] = str(e)[:200]
        return result

    if r1.returncode != 0:
        result["compile"] = "FAIL"
        # Extract key error
        err = (r1.stdout + r1.stderr).strip()
        # Find first error line
        for line in err.splitlines():
            if "error" in line.lower() or "sorry" in line.lower():
                result["error_detail"] = line.strip()[:200]
                break
        if not result["error_detail"]:
            result["error_detail"] = err[:200]
        return result

    result["compile"] = "OK"

    # Simulate
    try:
        r2 = subprocess.run(
            ["vvp", str(out_path)],
            capture_output=True, text=True, timeout=30,
        )
    except subprocess.TimeoutExpired:
        result["simulate"] = "TIMEOUT"
        result["error_detail"] = "vvp timed out (30s)"
        return result
    except Exception as e:
        result["simulate"] = "EXCEPTION"
        result["error_detail"] = str(e)[:200]
        return result

    stdout = r2.stdout.strip()
    if "Your Design Passed" in stdout:
        result["simulate"] = "PASS"
    elif "failures" in stdout:
        result["simulate"] = "FAIL_SIM"
        result["error_detail"] = [l for l in stdout.splitlines() if "failure" in l.lower()][:1]
        result["error_detail"] = result["error_detail"][0] if result["error_detail"] else stdout[:200]
    elif "Error" in stdout:
        result["simulate"] = "ERROR"
        result["error_detail"] = stdout[:200]
    else:
        result["simulate"] = "UNKNOWN"
        result["error_detail"] = stdout[:200]

    return result


def main():
    problems = discover_all()
    print(f"Scanning {len(problems)} RTLLM designs for iverilog compatibility...\n")

    results = []
    for i, p in enumerate(problems):
        r = scan_one(p)
        results.append(r)
        status = f"{r['compile']}"
        if r["compile"] == "OK":
            status += f" / {r['simulate']}"
        tag = "OK" if r.get("simulate") == "PASS" else ("??" if r["compile"] == "OK" else "XX")
        print(f"  [{i+1:2d}/50] {tag:2s} {p.name:30s} [{p.category:40s}] {status}")
        if r["error_detail"] and r.get("simulate") != "PASS":
            print(f"          → {r['error_detail'][:120]}")

    # Summary
    compile_ok = sum(1 for r in results if r["compile"] == "OK")
    sim_pass = sum(1 for r in results if r.get("simulate") == "PASS")
    compile_fail = sum(1 for r in results if r["compile"] == "FAIL")
    no_ref = sum(1 for r in results if r["compile"] == "NO_REF")

    print(f"\n{'='*60}")
    print(f"  Total designs:    {len(results)}")
    print(f"  Compile OK:       {compile_ok}")
    print(f"  Sim PASS:         {sim_pass}")
    print(f"  Compile FAIL:     {compile_fail}")
    print(f"  No reference:     {no_ref}")
    print(f"  Other issues:     {len(results) - compile_ok - compile_fail - no_ref}")
    print(f"{'='*60}")

    # Group compile failures by error pattern
    if compile_fail > 0:
        print(f"\nCompile failure patterns:")
        patterns = {}
        for r in results:
            if r["compile"] == "FAIL":
                # Extract key pattern
                detail = r["error_detail"]
                if "break" in detail.lower():
                    pat = "break statement not supported"
                elif "sorry" in detail.lower():
                    pat = "unsupported feature (sorry)"
                elif "Unknown module" in detail:
                    pat = "unknown module reference"
                else:
                    pat = detail[:80]
                patterns.setdefault(pat, []).append(r["name"])
        for pat, names in patterns.items():
            print(f"  [{len(names)}] {pat}")
            for n in names:
                print(f"       - {n}")


if __name__ == "__main__":
    main()
