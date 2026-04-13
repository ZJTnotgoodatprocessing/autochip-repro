"""Run VerilogEval-Human 20-problem subset: zero-shot vs feedback comparison.

Usage:
    python scripts/run_verilogeval_subset.py
    python scripts/run_verilogeval_subset.py --mode zero-shot
    python scripts/run_verilogeval_subset.py --mode both --feedback-k 5 --feedback-iterations 8
    python scripts/run_verilogeval_subset.py --problems Prob007_wire Prob109_fsm1

    # Retry only API-error problems from a previous run:
    python scripts/run_verilogeval_subset.py --retry-from outputs/verilogeval_both_20260410_xxxx.json
"""

import argparse
import csv
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from src.llm.client import get_model_name
from src.runner.verilogeval_loader import load_verilogeval_task, list_problems
from src.feedback.loop_runner import run_feedback_loop

# ── 20-problem subset ────────────────────────────────────────────────────────

SUBSET_20 = [
    # Easy — Combinational
    "Prob001_zero",
    "Prob007_wire",
    "Prob014_andgate",
    "Prob024_hadd",
    "Prob027_fadd",
    # Easy — Sequential
    "Prob031_dff",
    "Prob035_count1to10",
    "Prob041_dff8r",
    # Medium — Combinational
    "Prob025_reduction",
    "Prob022_mux2to1",
    "Prob050_kmap1",
    # Medium — Sequential
    "Prob054_edgedetect",
    "Prob068_countbcd",
    "Prob082_lfsr32",
    "Prob085_shift4",
    # Medium-Hard — Combinational
    "Prob030_popcount255",
    # Hard — FSM / Complex
    "Prob109_fsm1",
    "Prob127_lemmings1",
    "Prob140_fsm_hdlc",
    "Prob144_conwaylife",
]


def _run_one(task, k, max_iterations, temperature):
    """Run feedback loop and return summary dict with API error info."""
    result = run_feedback_loop(
        task, k=k, max_iterations=max_iterations, temperature=temperature,
    )
    return {
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


def _load_previous_results(json_path: str) -> tuple[dict, list[str], dict]:
    """Load a previous run's JSON and return (row_dict_by_name, api_error_problem_ids, full_data)."""
    data = json.loads(Path(json_path).read_text(encoding="utf-8"))
    row_by_name = {}
    api_errors = []
    for r in data.get("results", []):
        name = r["task_name"]
        row_by_name[name] = r
        if r.get("zs_api_error") or r.get("fb_api_error"):
            api_errors.append(name)
    return row_by_name, api_errors, data


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
    parser = argparse.ArgumentParser(description="VerilogEval-Human subset experiment")
    parser.add_argument("--model", type=str, default=None, help="Override model name (default: ANTHROPIC_MODEL env var)")
    parser.add_argument("--mode", choices=["zero-shot", "feedback", "both"], default="both")
    parser.add_argument("--problems", nargs="*", help="Override problem list")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--feedback-k", type=int, default=3)
    parser.add_argument("--feedback-iterations", type=int, default=5)
    parser.add_argument("--retry-from", type=str, default=None,
                        help="Path to previous result JSON — only re-run API-error problems")
    args = parser.parse_args()

    if args.model:
        os.environ["ANTHROPIC_MODEL"] = args.model

    model_name = get_model_name()

    # ── Determine problem list ───────────────────────────────────────────
    prev_rows = {}
    prev_data = None
    if args.retry_from:
        prev_rows, api_error_ids, prev_data = _load_previous_results(args.retry_from)
        if not api_error_ids:
            print("No API-error problems found in previous run. Nothing to retry.")
            sys.exit(0)
        problem_ids = api_error_ids
        print(f"Retrying {len(problem_ids)} API-error problem(s) from: {args.retry_from}")
        if prev_data and "mode" in prev_data:
            args.mode = prev_data["mode"]
    else:
        problem_ids = args.problems or SUBSET_20

    # Validate
    available = set(list_problems())
    missing = [p for p in problem_ids if p not in available]
    if missing:
        print(f"ERROR: Problems not found in repo: {missing}")
        sys.exit(1)

    project_root = Path(__file__).resolve().parent.parent
    out_dir = project_root / "outputs"
    out_dir.mkdir(exist_ok=True)

    print("=" * 70)
    print("VerilogEval-Human Subset Experiment")
    print("=" * 70)
    print(f"Model:              {model_name}")
    print(f"Problems:           {len(problem_ids)}")
    print(f"Mode:               {args.mode}")
    print(f"Temperature:        {args.temperature}")
    if args.mode in ("feedback", "both"):
        print(f"Feedback k:         {args.feedback_k}")
        print(f"Feedback max iter:  {args.feedback_iterations}")
    print()

    rows = []

    for i, pid in enumerate(problem_ids, 1):
        task = load_verilogeval_task(pid)
        print(f"[{i}/{len(problem_ids)}] {pid}")

        zs = None
        fb = None

        # ── Zero-shot ────────────────────────────────────────────────────
        if args.mode in ("zero-shot", "both"):
            print("  Zero-shot...", end=" ", flush=True)
            zs = _run_one(task, k=1, max_iterations=1, temperature=args.temperature)
            if zs["api_error"]:
                print(f"API_ERR({zs['api_error_type']})")
            elif zs["passed"]:
                print("PASS")
            else:
                print(f"FAIL({zs['best_rank']:.2f})")

        # ── Feedback ─────────────────────────────────────────────────────
        if args.mode in ("feedback", "both"):
            print(f"  Feedback(k={args.feedback_k},iter={args.feedback_iterations})...", end=" ", flush=True)
            fb = _run_one(task, k=args.feedback_k, max_iterations=args.feedback_iterations,
                          temperature=args.temperature)
            if fb["api_error"]:
                print(f"API_ERR({fb['api_error_type']})")
            elif fb["passed"]:
                print(f"PASS(iter={fb['total_iterations']})")
            else:
                print(f"FAIL({fb['best_rank']:.2f})")

        # ── Build row ────────────────────────────────────────────────────
        row = {"task_name": pid}
        if zs:
            row["zs_passed"] = zs["passed"]
            row["zs_rank"] = zs["best_rank"]
            row["zs_api_error"] = zs["api_error"]
            row["zs_api_error_type"] = zs.get("api_error_type")
        if fb:
            row["fb_passed"] = fb["passed"]
            row["fb_rank"] = fb["best_rank"]
            row["fb_iterations"] = fb["total_iterations"]
            row["fb_api_error"] = fb["api_error"]
            row["fb_api_error_type"] = fb.get("api_error_type")
        if zs and fb:
            row["improved"] = (not zs["passed"] and not zs["api_error"]) and fb["passed"]

        rows.append(row)
        print()

    # ── Merge with previous results if retrying ──────────────────────────
    if args.retry_from:
        merged = []
        # Rebuild full list from previous run, replacing retried entries
        retried_names = {r["task_name"] for r in rows}
        retry_map = {r["task_name"]: r for r in rows}
        prev_data = json.loads(Path(args.retry_from).read_text(encoding="utf-8"))
        for prev_r in prev_data.get("results", []):
            name = prev_r["task_name"]
            if name in retried_names:
                merged.append(retry_map[name])
            else:
                merged.append(prev_r)
        rows = merged
        print(f"(Merged {len(retried_names)} retried result(s) into {len(rows)} total)\n")

    # ── Summary table ────────────────────────────────────────────────────
    print()
    if args.mode == "both":
        print(f"{'Problem':<28} {'Zero-shot':>14} {'Feedback':>22} {'Improved?':>10}")
        print("-" * 78)
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
            print(f"{r['task_name']:<28} {zs_str:>14} {fb_str:>22} {imp:>10}")

        total = len(rows)
        zs_api = sum(1 for r in rows if r.get("zs_api_error"))
        fb_api = sum(1 for r in rows if r.get("fb_api_error"))
        zs_valid = total - zs_api
        fb_valid = total - fb_api
        zs_pass = sum(1 for r in rows if r.get("zs_passed") and not r.get("zs_api_error"))
        fb_pass = sum(1 for r in rows if r.get("fb_passed") and not r.get("fb_api_error"))
        improved = sum(1 for r in rows if r.get("improved"))

        print("-" * 78)
        print(f"Zero-shot:  {zs_pass}/{zs_valid} valid pass ({zs_pass/zs_valid*100:.0f}%)" if zs_valid else "Zero-shot:  no valid runs")
        print(f"Feedback:   {fb_pass}/{fb_valid} valid pass ({fb_pass/fb_valid*100:.0f}%)" if fb_valid else "Feedback:   no valid runs")
        print(f"API errors: {zs_api} zero-shot, {fb_api} feedback")
        print(f"Improved by feedback: {improved} task(s)")

    elif args.mode == "zero-shot":
        print(f"{'Problem':<28} {'Result':>14} {'Rank':>8}")
        print("-" * 54)
        for r in rows:
            if r.get("zs_api_error"):
                status = f"API_ERR"
            elif r.get("zs_passed"):
                status = "PASS"
            else:
                status = "FAIL"
            print(f"{r['task_name']:<28} {status:>14} {r.get('zs_rank', -2):>8.2f}")
        total = len(rows)
        api_err = sum(1 for r in rows if r.get("zs_api_error"))
        valid = total - api_err
        passed = sum(1 for r in rows if r.get("zs_passed") and not r.get("zs_api_error"))
        print("-" * 54)
        if valid:
            print(f"Pass rate: {passed}/{valid} valid ({passed/valid*100:.0f}%), API errors: {api_err}")
        else:
            print(f"No valid runs. API errors: {api_err}")

    else:  # feedback only
        print(f"{'Problem':<28} {'Result':>14} {'Rank':>8} {'Iters':>6}")
        print("-" * 60)
        for r in rows:
            if r.get("fb_api_error"):
                status = "API_ERR"
            elif r.get("fb_passed"):
                status = "PASS"
            else:
                status = "FAIL"
            print(f"{r['task_name']:<28} {status:>14} {r.get('fb_rank', -2):>8.2f} {r.get('fb_iterations', 0):>6}")
        total = len(rows)
        api_err = sum(1 for r in rows if r.get("fb_api_error"))
        valid = total - api_err
        passed = sum(1 for r in rows if r.get("fb_passed") and not r.get("fb_api_error"))
        print("-" * 60)
        if valid:
            print(f"Pass rate: {passed}/{valid} valid ({passed/valid*100:.0f}%), API errors: {api_err}")
        else:
            print(f"No valid runs. API errors: {api_err}")

    # ── Save results ─────────────────────────────────────────────────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Compute stats
    total = len(rows)
    zs_api = sum(1 for r in rows if r.get("zs_api_error"))
    fb_api = sum(1 for r in rows if r.get("fb_api_error"))

    summary = {
        "timestamp": timestamp,
        "model_name": model_name,
        "temperature": args.temperature,
        "mode": args.mode,
        "feedback_k": args.feedback_k if args.mode != "zero-shot" else None,
        "feedback_max_iterations": args.feedback_iterations if args.mode != "zero-shot" else None,
        "total_problems": total,
        "results": rows,
    }

    if args.mode in ("both", "zero-shot"):
        zs_valid = total - zs_api
        zs_pass = sum(1 for r in rows if r.get("zs_passed") and not r.get("zs_api_error"))
        summary["zero_shot_valid_runs"] = zs_valid
        summary["zero_shot_api_errors"] = zs_api
        summary["zero_shot_pass"] = zs_pass
    if args.mode in ("both", "feedback"):
        fb_valid = total - fb_api
        fb_pass = sum(1 for r in rows if r.get("fb_passed") and not r.get("fb_api_error"))
        summary["feedback_valid_runs"] = fb_valid
        summary["feedback_api_errors"] = fb_api
        summary["feedback_pass"] = fb_pass
    if args.mode == "both":
        summary["improved_count"] = sum(1 for r in rows if r.get("improved"))

    json_file = out_dir / f"verilogeval_{args.mode}_{timestamp}.json"
    json_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[JSON] {json_file}")

    csv_file = out_dir / f"verilogeval_{args.mode}_{timestamp}.csv"
    if rows:
        all_keys = list(dict.fromkeys(k for r in rows for k in r.keys()))
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=all_keys)
            writer.writeheader()
            writer.writerows(rows)
        print(f"[CSV]  {csv_file}")


if __name__ == "__main__":
    main()
