"""Run RTLLM benchmark subset: zero-shot vs feedback comparison.

Usage:
    # Run CORE_5 with default model (Haiku)
    python scripts/run_rtllm_subset.py --subset core5

    # Run with a specific model (via unified relay — just change model name)
    python scripts/run_rtllm_subset.py --subset core5 --model gpt-4o
    python scripts/run_rtllm_subset.py --subset core5 --model claude-sonnet-4-20250514

    # Run only zero-shot
    python scripts/run_rtllm_subset.py --subset core5 --mode zero-shot

    # Run specific problems
    python scripts/run_rtllm_subset.py --problems adder_8bit fsm traffic_light

    # Limit number of problems (useful for quick smoke)
    python scripts/run_rtllm_subset.py --subset core5 --limit 2

Common model names (via unified relay, no key/base_url change needed):
    claude-haiku-4-5-20251001      (Haiku 4.5 — current default)
    claude-sonnet-4-5-20250929     (Sonnet 4.5)
    claude-sonnet-4-6              (Sonnet 4.6)
    claude-opus-4-6                (Opus 4.6)
    gpt-5.4                        (GPT-5.4)
    gemini-2.5-pro                 (Gemini 2.5 Pro)
    deepseek-v3.2                  (DeepSeek V3.2)
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from src.llm.client import get_model_name
from src.runner.rtllm_loader import discover_all, load_by_name, RTLLMProblem
from src.runner.task import Task
from src.feedback.loop_runner import run_feedback_loop
from src.utils.artifacts import build_run_metadata, create_run_dir, make_run_id, timestamp_now

# ── Predefined subsets ───────────────────────────────────────────────────────

SUBSETS = {
    "core5": [
        "adder_8bit",         # Arithmetic/Adder — Easy, smoke test
        "multi_booth_8bit",   # Arithmetic/Multiplier — Medium-Hard
        "fsm",                # Control/FSM — Medium, Mealy sequence detector
        "LIFObuffer",         # Memory/LIFO — Medium, stack structure
        "traffic_light",      # Miscellaneous — Medium-Hard, FSM + timing
    ],
}


def _rtllm_to_task(problem: RTLLMProblem) -> Task:
    """Convert an RTLLMProblem to a Task for the feedback loop.

    RTLLM design_description.txt contains the full spec including module name
    and I/O ports. We extract a module header from the description and pass
    the full description text as the task description.
    """
    desc = problem.description

    # Build module_header from the description's Module name / Input / Output sections
    module_header = _extract_module_header(desc, problem.module_name)

    return Task(
        name=problem.name,
        description=desc,
        module_header=module_header,
        testbench_path=problem.testbench_path,
    )


def _extract_module_header(description: str, module_name: str) -> str:
    """Extract or synthesize a Verilog module header from RTLLM description.

    RTLLM descriptions have a structured format with "Module name:", "Input ports:",
    "Output ports:" sections. We parse these to build a valid module interface.
    """
    lines = description.splitlines()

    # Collect port lines from Input/Output sections
    input_ports = []
    output_ports = []
    current_section = None

    for line in lines:
        stripped = line.strip()
        lower = stripped.lower()

        if lower.startswith("input port"):
            current_section = "input"
            continue
        elif lower.startswith("output port"):
            current_section = "output"
            continue
        elif lower.startswith(("implementation", "parameter", "module name", "give me")):
            if current_section:
                current_section = None
            continue

        if current_section and stripped and not stripped.startswith("Module"):
            # Clean up the port description — extract port name/type
            # e.g., "a[7:0]: 8-bit input operand A." -> "input [7:0] a"
            port_line = _parse_port_line(stripped, current_section)
            if port_line:
                if current_section == "input":
                    input_ports.append(port_line)
                else:
                    output_ports.append(port_line)

    if not input_ports and not output_ports:
        # Fallback: just return a minimal header
        return f"module {module_name}(\n    // See description for port definitions\n);"

    all_ports = input_ports + output_ports
    ports_str = ",\n    ".join(all_ports)
    return f"module {module_name}(\n    {ports_str}\n);"


def _parse_port_line(line: str, direction: str) -> str | None:
    """Parse a single RTLLM port description line into a Verilog port declaration.

    Examples:
        "a[7:0]: 8-bit input operand A." -> "input [7:0] a"
        "sum[7:0]: 8-bit output..." -> "output [7:0] sum"
        "cin: Carry-in input." -> "input cin"
        "CLK: Clock signal..." -> "input CLK"
    """
    # Remove leading bullet/number markers
    line = re.sub(r'^[\-\*\d\.]+\s*', '', line)

    # Match patterns like "name[range]: description" or "name: description"
    m = re.match(r'(\w+)(\[[\w\-:]+\])?\s*[:.](.*)$', line)
    if not m:
        return None

    port_name = m.group(1)
    port_range = m.group(2) or ""

    # Skip lines that don't look like port declarations
    if port_name.lower() in ('the', 'a', 'an', 'this', 'each', 'when', 'if', 'for'):
        return None

    dir_kw = "input" if direction == "input" else "output"

    # Check if description mentions "reg" for output
    desc = m.group(3).lower() if m.group(3) else ""
    reg_kw = ""
    if direction == "output" and "reg" in desc:
        reg_kw = " reg"

    if port_range:
        return f"{dir_kw}{reg_kw} {port_range} {port_name}"
    else:
        return f"{dir_kw}{reg_kw} {port_name}"


def _serialize_feedback_result(result) -> dict:
    """Serialize full feedback-loop result for detailed artifacts."""
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


def _run_one(task, k, max_iterations, temperature):
    """Run feedback loop and return both summary and detailed dicts."""
    result = run_feedback_loop(
        task, k=k, max_iterations=max_iterations, temperature=temperature,
    )
    summary = {
        "task_name": result.task_name,
        "k": k,
        "max_iterations": max_iterations,
        "total_iterations": result.total_iterations,
        "best_rank": result.best_rank,
        "passed": result.passed,
        "api_error": result.api_error,
        "api_error_type": result.api_error_type,
        "api_error_message": result.api_error_message,
    }
    detailed = _serialize_feedback_result(result)
    return summary, detailed


def _status_str(d: dict, prefix: str) -> str:
    """Format a result dict entry for display."""
    if d.get(f"{prefix}_api_error"):
        return f"API_ERR({d.get(f'{prefix}_api_error_type', '?')})"
    if d.get(f"{prefix}_passed"):
        iters = d.get(f"{prefix}_iterations", "")
        return f"PASS(iter={iters})" if iters and prefix == "fb" else "PASS"
    rank = d.get(f"{prefix}_rank", -2)
    return f"FAIL({rank:.2f})"


def main():
    parser = argparse.ArgumentParser(
        description="RTLLM benchmark experiment runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Common model names (unified relay — just change the name, no key change needed):
  claude-haiku-4-5-20251001      Haiku 4.5 (default)
  claude-sonnet-4-5-20250929     Sonnet 4.5
  claude-sonnet-4-6              Sonnet 4.6
  claude-opus-4-6                Opus 4.6
  gpt-5.4                        GPT-5.4
  gemini-2.5-pro                 Gemini 2.5 Pro
  deepseek-v3.2                  DeepSeek V3.2
        """,
    )
    parser.add_argument("--model", type=str, default=None,
                        help="Model name to use (overrides ANTHROPIC_MODEL env var). "
                             "Via unified relay, just change this name to switch models.")
    parser.add_argument("--subset", type=str, default="core5",
                        choices=list(SUBSETS.keys()),
                        help="Predefined subset to run (default: core5)")
    parser.add_argument("--problems", nargs="*",
                        help="Override with specific RTLLM problem names")
    parser.add_argument("--mode", choices=["zero-shot", "feedback", "both"], default="both",
                        help="Experiment mode (default: both)")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--feedback-k", type=int, default=3,
                        help="Number of candidates per feedback iteration (default: 3)")
    parser.add_argument("--feedback-iterations", type=int, default=5,
                        help="Max feedback iterations (default: 5)")
    parser.add_argument("--limit", type=int, default=None,
                        help="Limit number of problems to run (for quick smoke tests)")
    args = parser.parse_args()

    # ── Model switching: --model overrides env var ────────────────────────
    if args.model:
        os.environ["ANTHROPIC_MODEL"] = args.model

    model_name = get_model_name()

    # ── Determine problem list ───────────────────────────────────────────
    if args.problems:
        problem_names = args.problems
    else:
        problem_names = list(SUBSETS[args.subset])

    if args.limit:
        problem_names = problem_names[:args.limit]

    # Validate availability
    all_rtllm = {p.name: p for p in discover_all()}
    missing = [n for n in problem_names if n not in all_rtllm]
    if missing:
        print(f"ERROR: RTLLM problems not found: {missing}")
        print(f"Available: {sorted(all_rtllm.keys())}")
        sys.exit(1)

    problems = [all_rtllm[n] for n in problem_names]

    timestamp = timestamp_now()
    run_id = make_run_id(f"rtllm_{args.mode}", timestamp)
    run_dir = create_run_dir("rtllm", run_id)

    print("=" * 70)
    print("RTLLM Benchmark Experiment")
    print("=" * 70)
    print(f"Model:              {model_name}")
    print(f"Subset:             {args.subset if not args.problems else 'custom'}")
    print(f"Problems:           {len(problems)}")
    print(f"Mode:               {args.mode}")
    print(f"Temperature:        {args.temperature}")
    if args.mode in ("feedback", "both"):
        print(f"Feedback k:         {args.feedback_k}")
        print(f"Feedback max iter:  {args.feedback_iterations}")
    print(f"Output dir:         {run_dir}")
    print()

    rows = []
    detailed_results = []

    for i, prob in enumerate(problems, 1):
        task = _rtllm_to_task(prob)
        print(f"[{i}/{len(problems)}] {prob.name} ({prob.category})")

        zs = None
        fb = None

        # ── Zero-shot ────────────────────────────────────────────────────
        if args.mode in ("zero-shot", "both"):
            print("  Zero-shot...", end=" ", flush=True)
            zs, zs_detail = _run_one(task, k=1, max_iterations=1, temperature=args.temperature)
            if zs["api_error"]:
                print(f"API_ERR({zs['api_error_type']})")
            elif zs["passed"]:
                print("PASS")
            else:
                print(f"FAIL({zs['best_rank']:.2f})")

        # ── Feedback ─────────────────────────────────────────────────────
        if args.mode in ("feedback", "both"):
            print(f"  Feedback(k={args.feedback_k},iter={args.feedback_iterations})...", end=" ", flush=True)
            fb, fb_detail = _run_one(task, k=args.feedback_k, max_iterations=args.feedback_iterations,
                                     temperature=args.temperature)
            if fb["api_error"]:
                print(f"API_ERR({fb['api_error_type']})")
            elif fb["passed"]:
                print(f"PASS(iter={fb['total_iterations']})")
            else:
                print(f"FAIL({fb['best_rank']:.2f})")

        # ── Build row ────────────────────────────────────────────────────
        row = {"task_name": prob.name, "category": prob.category}
        detail_row = {"task_name": prob.name, "category": prob.category}
        if zs:
            row["zs_passed"] = zs["passed"]
            row["zs_rank"] = zs["best_rank"]
            row["zs_api_error"] = zs["api_error"]
            row["zs_api_error_type"] = zs.get("api_error_type")
            detail_row["zero_shot"] = zs_detail
        if fb:
            row["fb_passed"] = fb["passed"]
            row["fb_rank"] = fb["best_rank"]
            row["fb_iterations"] = fb["total_iterations"]
            row["fb_api_error"] = fb["api_error"]
            row["fb_api_error_type"] = fb.get("api_error_type")
            detail_row["feedback"] = fb_detail
        if zs and fb:
            row["improved"] = (not zs["passed"] and not zs["api_error"]) and fb["passed"]
            detail_row["improved"] = row["improved"]

        rows.append(row)
        detailed_results.append(detail_row)
        print()

    # ── Summary table ────────────────────────────────────────────────────
    print()
    if args.mode == "both":
        print(f"{'Problem':<28} {'Category':<25} {'Zero-shot':>10} {'Feedback':>18} {'Improved?':>10}")
        print("-" * 95)
        for r in rows:
            zs_str = _status_str(r, "zs")
            fb_str = _status_str(r, "fb")
            if r.get("zs_api_error") or r.get("fb_api_error"):
                imp = "api_err"
            elif r.get("improved"):
                imp = "YES"
            elif r.get("zs_passed"):
                imp = "-"
            else:
                imp = "no"
            print(f"{r['task_name']:<28} {r['category']:<25} {zs_str:>10} {fb_str:>18} {imp:>10}")

        total = len(rows)
        zs_api = sum(1 for r in rows if r.get("zs_api_error"))
        fb_api = sum(1 for r in rows if r.get("fb_api_error"))
        zs_valid = total - zs_api
        fb_valid = total - fb_api
        zs_pass = sum(1 for r in rows if r.get("zs_passed") and not r.get("zs_api_error"))
        fb_pass = sum(1 for r in rows if r.get("fb_passed") and not r.get("fb_api_error"))
        improved = sum(1 for r in rows if r.get("improved"))

        print("-" * 95)
        print(f"Zero-shot:  {zs_pass}/{zs_valid} pass ({zs_pass/zs_valid*100:.0f}%)" if zs_valid else "Zero-shot:  no valid runs")
        print(f"Feedback:   {fb_pass}/{fb_valid} pass ({fb_pass/fb_valid*100:.0f}%)" if fb_valid else "Feedback:   no valid runs")
        print(f"API errors: {zs_api} zero-shot, {fb_api} feedback")
        print(f"Improved by feedback: {improved} task(s)")

    elif args.mode == "zero-shot":
        print(f"{'Problem':<28} {'Category':<25} {'Result':>10} {'Rank':>8}")
        print("-" * 75)
        for r in rows:
            if r.get("zs_api_error"):
                status = "API_ERR"
            elif r.get("zs_passed"):
                status = "PASS"
            else:
                status = "FAIL"
            print(f"{r['task_name']:<28} {r['category']:<25} {status:>10} {r.get('zs_rank', -2):>8.2f}")
        total = len(rows)
        api_err = sum(1 for r in rows if r.get("zs_api_error"))
        valid = total - api_err
        passed = sum(1 for r in rows if r.get("zs_passed") and not r.get("zs_api_error"))
        print("-" * 75)
        if valid:
            print(f"Pass rate: {passed}/{valid} ({passed/valid*100:.0f}%), API errors: {api_err}")

    else:  # feedback only
        print(f"{'Problem':<28} {'Category':<25} {'Result':>10} {'Rank':>8} {'Iters':>6}")
        print("-" * 81)
        for r in rows:
            if r.get("fb_api_error"):
                status = "API_ERR"
            elif r.get("fb_passed"):
                status = "PASS"
            else:
                status = "FAIL"
            print(f"{r['task_name']:<28} {r['category']:<25} {status:>10} {r.get('fb_rank', -2):>8.2f} {r.get('fb_iterations', 0):>6}")
        total = len(rows)
        api_err = sum(1 for r in rows if r.get("fb_api_error"))
        valid = total - api_err
        passed = sum(1 for r in rows if r.get("fb_passed") and not r.get("fb_api_error"))
        print("-" * 81)
        if valid:
            print(f"Pass rate: {passed}/{valid} ({passed/valid*100:.0f}%), API errors: {api_err}")

    # ── Save results ─────────────────────────────────────────────────────
    total = len(rows)
    zs_api = sum(1 for r in rows if r.get("zs_api_error"))
    fb_api = sum(1 for r in rows if r.get("fb_api_error"))

    summary_data = {
        "metadata": build_run_metadata(
            run_id=run_id,
            script_path="scripts/run_rtllm_subset.py",
            model_name=model_name,
            timestamp=timestamp,
            run_kind="rtllm_subset",
            parameters={
                "mode": args.mode,
                "subset": args.subset if not args.problems else "custom",
                "temperature": args.temperature,
                "feedback_k": args.feedback_k if args.mode != "zero-shot" else None,
                "feedback_iterations": args.feedback_iterations if args.mode != "zero-shot" else None,
            },
            source_inputs={
                "problem_names": problem_names,
                "benchmark": "RTLLM-2.0",
            },
        ),
        "summary": {
            "total_problems": total,
            "results": rows,
        },
    }

    if args.mode in ("both", "zero-shot"):
        zs_valid = total - zs_api
        zs_pass = sum(1 for r in rows if r.get("zs_passed") and not r.get("zs_api_error"))
        summary_data["summary"]["zero_shot_valid_runs"] = zs_valid
        summary_data["summary"]["zero_shot_api_errors"] = zs_api
        summary_data["summary"]["zero_shot_pass"] = zs_pass
    if args.mode in ("both", "feedback"):
        fb_valid = total - fb_api
        fb_pass = sum(1 for r in rows if r.get("fb_passed") and not r.get("fb_api_error"))
        summary_data["summary"]["feedback_valid_runs"] = fb_valid
        summary_data["summary"]["feedback_api_errors"] = fb_api
        summary_data["summary"]["feedback_pass"] = fb_pass
    if args.mode == "both":
        summary_data["summary"]["improved_count"] = sum(1 for r in rows if r.get("improved"))

    detailed = {
        "metadata": summary_data["metadata"],
        "results": detailed_results,
    }

    summary_json = run_dir / "summary.json"
    summary_json.write_text(json.dumps(summary_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[JSON] {summary_json}")

    details_json = run_dir / "details.json"
    details_json.write_text(json.dumps(detailed, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[DETAIL] {details_json}")

    csv_file = run_dir / "summary.csv"
    if rows:
        all_keys = list(dict.fromkeys(k for r in rows for k in r.keys()))
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=all_keys)
            writer.writeheader()
            writer.writerows(rows)
        print(f"[CSV]  {csv_file}")


if __name__ == "__main__":
    main()
