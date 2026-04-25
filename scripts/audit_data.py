"""Verify all experiment results — cross-check raw data with documented summaries."""
import json
from pathlib import Path

run_dir = Path("outputs/runs/rtllm")

def load_results(run_name):
    sp = run_dir / run_name / "summary.json"
    return json.loads(sp.read_text(encoding="utf-8"))

def count_by_prefix(results, prefix):
    passed = sum(1 for r in results if r.get(f"{prefix}_passed"))
    api_err = sum(1 for r in results if r.get(f"{prefix}_api_error"))
    total = len(results)
    valid = total - api_err
    return passed, valid, api_err

print("=" * 60)
print("=== 1. Formal Experiment (STUDY_12) ===")
print("=" * 60)

for model, run in [
    ("GPT-5.4",    "rtllm_both_20260422_013439"),
    ("Sonnet 4.6", "rtllm_both_20260422_011115"),
    ("Haiku",      "rtllm_both_20260422_004806"),
]:
    data = load_results(run)
    results = data["summary"]["results"]
    zs_p, zs_v, zs_e = count_by_prefix(results, "zs")
    fb_p, fb_v, fb_e = count_by_prefix(results, "fb")
    print(f"\n{model}:")
    print(f"  Zero-shot: {zs_p}/{zs_v} = {zs_p/zs_v*100:.1f}% (api_err={zs_e})")
    print(f"  Feedback:  {fb_p}/{fb_v} = {fb_p/fb_v*100:.1f}% (api_err={fb_e})")

print("\n" + "=" * 60)
print("=== 2. Ablation Experiment ===")
print("=" * 60)

for model, run in [
    ("GPT-5.4",    "rtllm_ablation_20260422_222409"),
    ("Sonnet 4.6", "rtllm_ablation_20260422_214745"),
]:
    data = load_results(run)
    results = data["summary"]["results"]
    # Ablation has zs, ro, fb prefixes
    for pfx, label in [("zs", "ZeroShot"), ("ro", "RetryOnly"), ("fb", "Feedback")]:
        p, v, e = count_by_prefix(results, pfx)
        if v > 0:
            print(f"  {model} {label}: {p}/{v} = {p/v*100:.1f}% (api_err={e})")

print("\n" + "=" * 60)
print("=== 3. Stability Experiment (4 ablation rounds) ===")
print("=" * 60)

# GPT stability: runs 222409, 031507, 035517, 043355
gpt_stab_runs = [
    "rtllm_ablation_20260422_222409",
    "rtllm_ablation_20260423_031507",
    "rtllm_ablation_20260423_035517",
    "rtllm_ablation_20260423_043355",
]
for i, run in enumerate(gpt_stab_runs, 1):
    data = load_results(run)
    results = data["summary"]["results"]
    fb_p, fb_v, fb_e = count_by_prefix(results, "fb")
    if fb_v > 0:
        print(f"  GPT R{i}: FB={fb_p}/{fb_v} ({fb_p/fb_v*100:.1f}%)")

# Sonnet stability: runs 214745, 051839, 130908, 134523
son_stab_runs = [
    "rtllm_ablation_20260422_214745",
    "rtllm_ablation_20260423_051839",
    "rtllm_ablation_20260423_130908",
    "rtllm_ablation_20260423_134523",
]
for i, run in enumerate(son_stab_runs, 1):
    data = load_results(run)
    results = data["summary"]["results"]
    fb_p, fb_v, fb_e = count_by_prefix(results, "fb")
    if fb_v > 0:
        print(f"  Sonnet R{i}: FB={fb_p}/{fb_v} ({fb_p/fb_v*100:.1f}%)")

print("\n" + "=" * 60)
print("=== 4. Granularity Experiment ===")
print("=" * 60)

for model, run in [
    ("GPT-5.4",    "rtllm_granularity_20260423_212239"),
    ("Sonnet 4.6", "rtllm_granularity_20260423_233052"),
]:
    data = load_results(run)
    results = data["summary"]["results"]
    for pfx, label in [("co", "CompOnly"), ("su", "Succinct"), ("ri", "Rich")]:
        p, v, e = count_by_prefix(results, pfx)
        if v > 0:
            print(f"  {model} {label}: {p}/{v} = {p/v*100:.1f}% (api_err={e})")

print("\n" + "=" * 60)
print("=== 5. Multi-turn v2 (fixed) ===")
print("=" * 60)

for model, run in [
    ("GPT-5.4",    "rtllm_multiturn_20260424_160853"),
    ("Sonnet 4.6", "rtllm_multiturn_20260424_181012"),
]:
    data = load_results(run)
    results = data["summary"]["results"]
    for pfx, label in [("a", "STk3"), ("d", "STk1"), ("b", "MTk1"), ("c", "COk3")]:
        p, v, e = count_by_prefix(results, pfx)
        if v > 0:
            print(f"  {model} {label}: {p}/{v} = {p/v*100:.1f}% (api_err={e})")

print("\n" + "=" * 60)
print("=== 6. Multi-turn v1 (DEPRECATED) ===")
print("=" * 60)

for model, run in [
    ("GPT-5.4",    "rtllm_multiturn_20260424_031541"),
    ("Sonnet 4.6", "rtllm_multiturn_20260424_040236"),
]:
    data = load_results(run)
    results = data["summary"]["results"]
    for pfx, label in [("st", "ST"), ("mt", "MT"), ("co", "CO")]:
        p, v, e = count_by_prefix(results, pfx)
        if v > 0:
            print(f"  {model} {label}: {p}/{v} = {p/v*100:.1f}% (DEPRECATED)")

print("\n" + "=" * 60)
print("=== 7. Prompt Strategy Experiment ===")
print("=" * 60)

ps_run = "rtllm_prompt_strategy_20260425_032429"
ps_path = run_dir / ps_run / "summary.json"
if ps_path.exists():
    data = load_results(ps_run)
    results = data["summary"]["results"]
    for pfx, label in [
        ("p0zs", "Base ZS"), ("p0fb", "Base FB"),
        ("p1zs", "CoT ZS"), ("p1fb", "CoT FB"),
        ("p2zs", "Fewshot ZS"), ("p2fb", "Fewshot FB"),
        ("p3zs", "FS+CoT ZS"), ("p3fb", "FS+CoT FB"),
    ]:
        p, v, e = count_by_prefix(results, pfx)
        if v > 0:
            print(f"  {label}: {p}/{v} = {p/v*100:.1f}% (api_err={e})")
else:
    print(f"  WARNING: {ps_run} not found — skipping")

print("\n" + "=" * 60)
print("Data audit complete. Check results above against documentation.")

