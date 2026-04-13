"""Run a single AutoChip task (single-round, no feedback loop).

Usage:
    python scripts/run_single_task.py --task data/sample_task
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


def build_prompt(task) -> str:
    return (
        "Generate a Verilog module that satisfies the following description.\n"
        "Return ONLY the Verilog code, no explanations.\n\n"
        f"Description:\n{task.description}\n\n"
        f"Module interface:\n{task.module_header}\n\n"
        "Your implementation:"
    )


def main():
    parser = argparse.ArgumentParser(description="Run single AutoChip task")
    parser.add_argument("--task", required=True, help="Path to task directory")
    parser.add_argument("--model", type=str, default=None, help="Override model name (default: ANTHROPIC_MODEL env var)")
    parser.add_argument("--temperature", type=float, default=0.7)
    args = parser.parse_args()

    if args.model:
        os.environ["ANTHROPIC_MODEL"] = args.model

    # 1. Load task
    task = load_task(args.task)
    print(f"[Task] {task.name}")
    print(f"[Desc] {task.description[:80]}...")

    # 2. Build prompt & call LLM
    prompt = build_prompt(task)
    model_name = get_model_name()
    print(f"[LLM] Generating Verilog with {model_name}...")
    response = generate(prompt, temperature=args.temperature)
    print(f"[LLM] Got {len(response)} chars")

    # 3. Extract Verilog
    modules = extract_modules(response)
    if not modules:
        print("[FAIL] No valid Verilog module extracted from LLM response")
        print(f"[Rank] -2.0")
        print("\n--- Raw LLM response ---")
        print(response)
        sys.exit(1)

    print(f"[Parse] Extracted {len(modules)} module(s)")
    verilog_code = modules[0]

    # 4. Compile
    print("[Compile] Running iverilog...")
    comp = compile(verilog_code, task.testbench_path)
    if not comp.success:
        print(f"[Compile] FAILED")
        print(f"[Compile stderr]\n{comp.stderr}")
        print(f"[Rank] {rank(comp, None)}")
        sys.exit(1)

    if comp.has_warnings:
        print(f"[Compile] OK with warnings")
        print(f"[Compile stderr]\n{comp.stderr}")
    else:
        print(f"[Compile] OK")

    # 5. Simulate
    print("[Sim] Running vvp...")
    sim = simulate(comp._out_path)  # type: ignore[attr-defined]
    print(f"[Sim] mismatches={sim.mismatches}, total={sim.total_samples}, passed={sim.passed}")

    if sim.stdout:
        print(f"[Sim stdout]\n{sim.stdout}")

    # 6. Rank
    score = rank(comp, sim)
    print(f"\n[Rank] {score}")
    if sim.passed:
        print("[RESULT] PASS")
    else:
        print("[RESULT] FAIL")

    # 7. Save output
    out_dir = Path(__file__).resolve().parent.parent / "outputs"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_file = out_dir / f"{task.name}_{timestamp}.json"
    out_file.write_text(json.dumps({
        "task_name": task.name,
        "model_name": model_name,
        "timestamp": timestamp,
        "temperature": args.temperature,
        "prompt": prompt,
        "raw_response": response,
        "extracted_verilog": verilog_code,
        "compile_stdout": comp.stdout,
        "compile_stderr": comp.stderr,
        "sim_stdout": sim.stdout,
        "sim_stderr": sim.stderr,
        "mismatches": sim.mismatches,
        "total_samples": sim.total_samples,
        "rank": score,
        "passed": sim.passed,
    }, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[Saved] {out_file}")


if __name__ == "__main__":
    main()
