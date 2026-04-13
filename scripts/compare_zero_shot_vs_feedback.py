"""Compare zero-shot vs feedback loop on the same set of tasks.

Usage:
    python scripts/compare_zero_shot_vs_feedback.py
    python scripts/compare_zero_shot_vs_feedback.py --tasks edge_detect lfsr_5bit
    python scripts/compare_zero_shot_vs_feedback.py --feedback-k 5 --feedback-iterations 8
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

from src.runner.task import load_task
from src.llm.client import get_model_name
from src.feedback.loop_runner import run_feedback_loop


def discover_tasks(data_dir: Path, names: list[str] | None = None) -> list[Path]:
    tasks = []
    for d in sorted(data_dir.iterdir()):
        if d.is_dir() and (d / "description.txt").exists():
            if names is None or d.name in names:
                tasks.append(d)
    return tasks


def run_experiment(task, k: int, max_iterations: int, temperature: float):
    """Run feedback loop and return summary dict."""
    result = run_feedback_loop(task, k=k, max_iterations=max_iterations, temperature=temperature)
    return {
        "task_name": result.task_name,
        "k": k,
        "max_iterations": max_iterations,
        "total_iterations": result.total_iterations,
        "best_rank": result.best_rank,
        "passed": result.passed,
        "best_verilog": result.best_verilog,
        "api_error": result.api_error,
        "api_error_type": result.api_error_type,
    }


def main():
    parser = argparse.ArgumentParser(description="Compare zero-shot vs feedback loop")
    parser.add_argument("--data-dir", default="data", help="Task data directory")
    parser.add_argument("--tasks", nargs="*", help="Specific task names (default: all)")
    parser.add_argument("--model", type=str, default=None, help="Override model name (default: ANTHROPIC_MODEL env var)")
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--feedback-k", type=int, default=3, help="Candidates per iteration for feedback (default: 3)")
    parser.add_argument("--feedback-iterations", type=int, default=5, help="Max iterations for feedback (default: 5)")
    args = parser.parse_args()

    if args.model:
        os.environ["ANTHROPIC_MODEL"] = args.model

    project_root = Path(__file__).resolve().parent.parent
    data_dir = (project_root / args.data_dir).resolve()
    out_dir = project_root / "outputs"
    out_dir.mkdir(exist_ok=True)

    model_name = get_model_name()
    task_dirs = discover_tasks(data_dir, args.tasks)

    if not task_dirs:
        print("No tasks found.")
        sys.exit(1)

    print(f"=== Zero-shot vs Feedback Comparison ===")
    print(f"Model:              {model_name}")
    print(f"Tasks:              {len(task_dirs)}")
    print(f"Temperature:        {args.temperature}")
    print(f"Feedback k:         {args.feedback_k}")
    print(f"Feedback max iter:  {args.feedback_iterations}")
    print()

    rows = []
    for i, td in enumerate(task_dirs, 1):
        task = load_task(td)
        print(f"[{i}/{len(task_dirs)}] {task.name}")

        # Zero-shot: k=1, max_iterations=1
        print(f"  Zero-shot...", end=" ", flush=True)
        zs = run_experiment(task, k=1, max_iterations=1, temperature=args.temperature)
        if zs["api_error"]:
            zs_status = f"API_ERR({zs['api_error_type']})"
        elif zs["passed"]:
            zs_status = "PASS"
        else:
            zs_status = f"FAIL({zs['best_rank']:.2f})"
        print(zs_status)

        # Feedback loop
        print(f"  Feedback(k={args.feedback_k},iter={args.feedback_iterations})...", end=" ", flush=True)
        fb = run_experiment(task, k=args.feedback_k, max_iterations=args.feedback_iterations, temperature=args.temperature)
        if fb["api_error"]:
            fb_status = f"API_ERR({fb['api_error_type']})"
        elif fb["passed"]:
            fb_status = f"PASS(iter={fb['total_iterations']})"
        else:
            fb_status = f"FAIL({fb['best_rank']:.2f})"
        print(fb_status)

        improved = (not zs["passed"] and not zs["api_error"]) and fb["passed"]
        rows.append({
            "task_name": task.name,
            "zs_passed": zs["passed"],
            "zs_rank": zs["best_rank"],
            "zs_api_error": zs["api_error"],
            "fb_passed": fb["passed"],
            "fb_rank": fb["best_rank"],
            "fb_iterations": fb["total_iterations"],
            "fb_api_error": fb["api_error"],
            "improved": improved,
        })
        print()

    # ── Summary table ────────────────────────────────────────────────────
    print()
    print(f"{'Task':<24} {'Zero-shot':>14} {'Feedback':>20} {'Improved?':>10}")
    print("-" * 72)
    for r in rows:
        if r.get("zs_api_error"):
            zs_str = "API_ERR"
        elif r["zs_passed"]:
            zs_str = "PASS"
        else:
            zs_str = f"FAIL({r['zs_rank']:.2f})"

        if r.get("fb_api_error"):
            fb_str = "API_ERR"
        elif r["fb_passed"]:
            fb_str = f"PASS(iter={r['fb_iterations']})"
        else:
            fb_str = f"FAIL({r['fb_rank']:.2f})"

        if r.get("zs_api_error") or r.get("fb_api_error"):
            imp_str = "api_err"
        elif r["improved"]:
            imp_str = "YES"
        elif r["zs_passed"]:
            imp_str = "-"
        else:
            imp_str = "no"
        print(f"{r['task_name']:<24} {zs_str:>14} {fb_str:>20} {imp_str:>10}")

    # Aggregate
    total = len(rows)
    zs_api = sum(1 for r in rows if r.get("zs_api_error"))
    fb_api = sum(1 for r in rows if r.get("fb_api_error"))
    zs_valid = total - zs_api
    fb_valid = total - fb_api
    zs_pass = sum(1 for r in rows if r["zs_passed"] and not r.get("zs_api_error"))
    fb_pass = sum(1 for r in rows if r["fb_passed"] and not r.get("fb_api_error"))
    improved_count = sum(1 for r in rows if r["improved"])
    print("-" * 72)
    if zs_valid:
        print(f"Zero-shot pass rate:  {zs_pass}/{zs_valid} valid ({zs_pass/zs_valid*100:.0f}%)")
    print(f"Feedback pass rate:   {fb_pass}/{fb_valid} valid ({fb_pass/fb_valid*100:.0f}%)" if fb_valid else "")
    print(f"API errors:           {zs_api} zero-shot, {fb_api} feedback")
    print(f"Improved by feedback: {improved_count} task(s)")

    # ── Save JSON ────────────────────────────────────────────────────────
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary = {
        "timestamp": timestamp,
        "model_name": model_name,
        "temperature": args.temperature,
        "feedback_k": args.feedback_k,
        "feedback_max_iterations": args.feedback_iterations,
        "total_tasks": total,
        "zero_shot_valid_runs": zs_valid,
        "zero_shot_api_errors": zs_api,
        "zero_shot_pass": zs_pass,
        "feedback_valid_runs": fb_valid,
        "feedback_api_errors": fb_api,
        "feedback_pass": fb_pass,
        "improved_count": improved_count,
        "results": rows,
    }
    json_file = out_dir / f"comparison_{timestamp}.json"
    json_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[JSON] {json_file}")

    # ── Save CSV ─────────────────────────────────────────────────────────
    csv_file = out_dir / f"comparison_{timestamp}.csv"
    all_keys = list(dict.fromkeys(k for r in rows for k in r.keys()))
    with open(csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[CSV]  {csv_file}")


if __name__ == "__main__":
    main()
