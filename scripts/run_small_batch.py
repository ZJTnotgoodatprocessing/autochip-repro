"""Run a small batch of AutoChip tasks (single-round, no feedback loop).

Usage:
    python scripts/run_small_batch.py                          # run all tasks in data/
    python scripts/run_small_batch.py --tasks sample_task and_gate mux2to1
    python scripts/run_small_batch.py --data-dir data/ --temperature 0.5
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

from src.llm.client import generate, get_model_name
from src.utils.extract_verilog import extract_modules
from src.runner.task import load_task
from src.runner.verilog_executor import compile, simulate
from src.ranking.ranker import rank


def run_one_task(task_dir: Path, temperature: float, model_name: str, out_dir: Path) -> dict:
    """Run a single task and return a result dict. Never raises."""
    result = {
        "task_name": task_dir.name,
        "model_name": model_name,
        "temperature": temperature,
        "compile_ok": False,
        "sim_passed": False,
        "rank": -2.0,
        "mismatches": None,
        "total_samples": None,
        "error": None,
    }

    try:
        task = load_task(task_dir)
    except Exception as e:
        result["error"] = f"load failed: {e}"
        return result

    prompt = (
        "Generate a Verilog module that satisfies the following description.\n"
        "Return ONLY the Verilog code, no explanations.\n\n"
        f"Description:\n{task.description}\n\n"
        f"Module interface:\n{task.module_header}\n\n"
        "Your implementation:"
    )

    # LLM call
    try:
        response = generate(prompt, temperature=temperature)
    except Exception as e:
        result["error"] = f"LLM call failed: {e}"
        return result

    # Extract Verilog
    modules = extract_modules(response)
    if not modules:
        result["rank"] = -2.0
        result["error"] = "no valid module extracted"
        _save_output(result, prompt, response, "", None, None, out_dir)
        return result

    verilog_code = modules[0]

    # Compile
    comp = compile(verilog_code, task.testbench_path)
    if not comp.success:
        result["rank"] = rank(comp, None)
        result["error"] = f"compile failed"
        _save_output(result, prompt, response, verilog_code, comp, None, out_dir)
        return result

    result["compile_ok"] = True

    # Simulate
    sim = simulate(comp._out_path)  # type: ignore[attr-defined]
    score = rank(comp, sim)

    result["sim_passed"] = sim.passed
    result["rank"] = score
    result["mismatches"] = sim.mismatches
    result["total_samples"] = sim.total_samples

    _save_output(result, prompt, response, verilog_code, comp, sim, out_dir)
    return result


def _save_output(result, prompt, response, verilog_code, comp, sim, out_dir):
    """Save detailed JSON for one task run."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = out_dir / f"{result['task_name']}_{timestamp}.json"
    out_file.write_text(json.dumps({
        "task_name": result["task_name"],
        "model_name": result["model_name"],
        "timestamp": timestamp,
        "temperature": result["temperature"],
        "prompt": prompt,
        "raw_response": response,
        "extracted_verilog": verilog_code,
        "compile_stdout": comp.stdout if comp else "",
        "compile_stderr": comp.stderr if comp else "",
        "sim_stdout": sim.stdout if sim else "",
        "sim_stderr": sim.stderr if sim else "",
        "mismatches": sim.mismatches if sim else None,
        "total_samples": sim.total_samples if sim else None,
        "rank": result["rank"],
        "passed": result["sim_passed"],
        "error": result["error"],
    }, indent=2, ensure_ascii=False), encoding="utf-8")


def discover_tasks(data_dir: Path) -> list[Path]:
    """Return sorted list of task directories (each must have description.txt)."""
    tasks = []
    for d in sorted(data_dir.iterdir()):
        if d.is_dir() and (d / "description.txt").exists():
            tasks.append(d)
    return tasks


def main():
    parser = argparse.ArgumentParser(description="Run small batch of AutoChip tasks")
    parser.add_argument("--data-dir", default="data", help="Root directory containing task subdirs")
    parser.add_argument("--tasks", nargs="*", help="Specific task names to run (default: all)")
    parser.add_argument("--model", type=str, default=None, help="Override model name (default: ANTHROPIC_MODEL env var)")
    parser.add_argument("--temperature", type=float, default=0.7)
    args = parser.parse_args()

    if args.model:
        os.environ["ANTHROPIC_MODEL"] = args.model

    project_root = Path(__file__).resolve().parent.parent
    data_dir = (project_root / args.data_dir).resolve()
    out_dir = project_root / "outputs"

    model_name = get_model_name()

    # Discover tasks
    all_tasks = discover_tasks(data_dir)
    if args.tasks:
        all_tasks = [t for t in all_tasks if t.name in args.tasks]

    if not all_tasks:
        print("No tasks found.")
        sys.exit(1)

    print(f"=== AutoChip Batch Run ===")
    print(f"Model: {model_name}")
    print(f"Tasks: {len(all_tasks)}")
    print(f"Temperature: {args.temperature}")
    print()

    # Run each task
    results = []
    for i, task_dir in enumerate(all_tasks, 1):
        print(f"[{i}/{len(all_tasks)}] Running {task_dir.name}...", end=" ", flush=True)
        r = run_one_task(task_dir, args.temperature, model_name, out_dir)
        status = "PASS" if r["sim_passed"] else ("COMPILE_FAIL" if not r["compile_ok"] else "SIM_FAIL")
        if r["error"] and not r["compile_ok"]:
            status = f"ERROR: {r['error']}"
        print(status)
        results.append(r)

    # Summary table
    print()
    print(f"{'Task':<22} {'Compile':>8} {'Sim':>8} {'Rank':>8} {'Passed':>8}")
    print("-" * 58)
    for r in results:
        compile_str = "OK" if r["compile_ok"] else "FAIL"
        sim_str = "PASS" if r["sim_passed"] else ("FAIL" if r["compile_ok"] else "-")
        rank_str = f"{r['rank']:.2f}"
        passed_str = "Y" if r["sim_passed"] else "N"
        print(f"{r['task_name']:<22} {compile_str:>8} {sim_str:>8} {rank_str:>8} {passed_str:>8}")

    # Aggregate stats
    total = len(results)
    compile_ok = sum(1 for r in results if r["compile_ok"])
    sim_pass = sum(1 for r in results if r["sim_passed"])
    print("-" * 58)
    print(f"Compile success rate:  {compile_ok}/{total} ({compile_ok/total*100:.0f}%)")
    print(f"Simulation pass rate:  {sim_pass}/{total} ({sim_pass/total*100:.0f}%)")
    print(f"Total passed:          {sim_pass}/{total}")

    # Save batch summary
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    summary_file = out_dir / f"batch_summary_{timestamp}.json"
    summary_file.write_text(json.dumps({
        "timestamp": timestamp,
        "model_name": model_name,
        "temperature": args.temperature,
        "total_tasks": total,
        "compile_success": compile_ok,
        "sim_pass": sim_pass,
        "results": results,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nSummary saved: {summary_file}")


if __name__ == "__main__":
    main()
