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
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from src.runner.task import load_task
from src.llm.client import get_model_name
from src.feedback.loop_runner import run_feedback_loop
from src.utils.artifacts import build_run_metadata, create_run_dir, make_run_id, timestamp_now


def discover_tasks(data_dir: Path, names: list[str] | None = None) -> list[Path]:
    tasks = []
    for d in sorted(data_dir.iterdir()):
        if d.is_dir() and (d / "description.txt").exists():
            if names is None or d.name in names:
                tasks.append(d)
    return tasks


def _serialize_feedback_result(result) -> dict:
    """Serialize full feedback-loop result for detailed comparison artifacts."""
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


def run_experiment(task, k: int, max_iterations: int, temperature: float):
    """Run feedback loop and return summary + detailed results."""
    result = run_feedback_loop(task, k=k, max_iterations=max_iterations, temperature=temperature)
    summary = {
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
    detailed = _serialize_feedback_result(result)
    return summary, detailed


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

    timestamp = timestamp_now()
    run_id = make_run_id("comparison", timestamp)
    run_dir = create_run_dir("comparison", run_id)

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
    detailed_results = []
    for i, td in enumerate(task_dirs, 1):
        task = load_task(td)
        print(f"[{i}/{len(task_dirs)}] {task.name}")

        # Zero-shot: k=1, max_iterations=1
        print(f"  Zero-shot...", end=" ", flush=True)
        zs, zs_detail = run_experiment(task, k=1, max_iterations=1, temperature=args.temperature)
        if zs["api_error"]:
            zs_status = f"API_ERR({zs['api_error_type']})"
        elif zs["passed"]:
            zs_status = "PASS"
        else:
            zs_status = f"FAIL({zs['best_rank']:.2f})"
        print(zs_status)

        # Feedback loop
        print(f"  Feedback(k={args.feedback_k},iter={args.feedback_iterations})...", end=" ", flush=True)
        fb, fb_detail = run_experiment(task, k=args.feedback_k, max_iterations=args.feedback_iterations, temperature=args.temperature)
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
        detailed_results.append({
            "task_name": task.name,
            "zero_shot": zs_detail,
            "feedback": fb_detail,
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
    summary = {
        "metadata": build_run_metadata(
            run_id=run_id,
            script_path="scripts/compare_zero_shot_vs_feedback.py",
            model_name=model_name,
            timestamp=timestamp,
            run_kind="comparison",
            parameters={
                "data_dir": args.data_dir,
                "tasks": args.tasks,
                "temperature": args.temperature,
                "feedback_k": args.feedback_k,
                "feedback_iterations": args.feedback_iterations,
            },
            source_inputs={
                "task_dirs": [str(p.resolve()) for p in task_dirs],
            },
        ),
        "summary": {
            "total_tasks": total,
            "zero_shot_valid_runs": zs_valid,
            "zero_shot_api_errors": zs_api,
            "zero_shot_pass": zs_pass,
            "feedback_valid_runs": fb_valid,
            "feedback_api_errors": fb_api,
            "feedback_pass": fb_pass,
            "improved_count": improved_count,
            "results": rows,
        },
    }
    summary_json_file = run_dir / "summary.json"
    summary_json_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[JSON] {summary_json_file}")

    detailed = {
        "metadata": summary["metadata"],
        "results": detailed_results,
    }
    detailed_json_file = run_dir / "details.json"
    detailed_json_file.write_text(json.dumps(detailed, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[DETAIL] {detailed_json_file}")

    # ── Save CSV ─────────────────────────────────────────────────────────
    summary_csv_file = run_dir / "summary.csv"
    all_keys = list(dict.fromkeys(k for r in rows for k in r.keys()))
    with open(summary_csv_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_keys)
        writer.writeheader()
        writer.writerows(rows)
    print(f"[CSV]  {summary_csv_file}")


if __name__ == "__main__":
    main()
