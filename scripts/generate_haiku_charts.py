"""Generate charts for VerilogEval experiment results."""

import argparse
import json
import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

from src.utils.artifacts import find_latest_file

# ── Try to use a CJK font for Chinese titles ──
_CJK_FONTS = ["SimHei", "Microsoft YaHei", "STHeiti", "WenQuanYi Micro Hei", "Noto Sans CJK SC"]
_font_found = False
for _name in _CJK_FONTS:
    if any(_name.lower() in f.name.lower() for f in fm.fontManager.ttflist):
        plt.rcParams["font.sans-serif"] = [_name] + plt.rcParams.get("font.sans-serif", [])
        plt.rcParams["axes.unicode_minus"] = False
        _font_found = True
        break
if not _font_found:
    print("Warning: No CJK font found, Chinese text may not render correctly")


def _load_results(path: Path) -> list[dict]:
    data = json.loads(path.read_text("utf-8"))
    return data.get("summary", data).get("results", [])


def main():
    parser = argparse.ArgumentParser(description="Generate charts from a VerilogEval result JSON")
    parser.add_argument("--input", type=str, default=None, help="Path to summary JSON (default: latest run)")
    parser.add_argument("--output-dir", type=str, default=None, help="Directory for chart outputs")
    args = parser.parse_args()

    input_path = Path(args.input).resolve() if args.input else find_latest_file(
        [
            "outputs/runs/verilogeval/*/summary.json",
            "outputs/verilogeval_both_*.json",
        ],
        PROJECT,
    )
    if input_path is None:
        raise FileNotFoundError("No VerilogEval summary JSON found")

    results = _load_results(input_path)
    if not results:
        raise ValueError(f"No results found in {input_path}")

    out_dir = Path(args.output_dir).resolve() if args.output_dir else PROJECT / "outputs" / "reports" / "charts"
    out_dir.mkdir(parents=True, exist_ok=True)

    zs_pass = sum(1 for r in results if r["zs_passed"])
    fb_pass = sum(1 for r in results if r["fb_passed"])
    total = len(results)

    # ── Bar chart: zero-shot vs feedback pass rate ──
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(
        ["零样本 (Zero-shot)", "反馈循环 (Feedback)"],
        [zs_pass / total * 100, fb_pass / total * 100],
        color=["#5B9BD5", "#ED7D31"],
        width=0.5,
    )
    for bar, val in zip(bars, [zs_pass, fb_pass]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                f"{val}/{total} ({val/total*100:.0f}%)", ha="center", fontsize=11)

    ax.set_ylabel("通过率 (%)", fontsize=12)
    ax.set_title("Haiku 模型在 VerilogEval-Human 子集上的表现", fontsize=13)
    ax.set_ylim(0, 105)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.tight_layout()
    fig.savefig(out_dir / "haiku_pass_rate_bar.png", dpi=150)
    print(f"Saved: {out_dir / 'haiku_pass_rate_bar.png'}")

    # ── Per-problem detail chart ──
    fig2, ax2 = plt.subplots(figsize=(14, 5))
    names = [r["task_name"].replace("Prob", "P") for r in results]
    zs_ranks = [r["zs_rank"] for r in results]
    fb_ranks = [r["fb_rank"] for r in results]

    x = range(len(names))
    w = 0.35
    ax2.bar([i - w/2 for i in x], zs_ranks, w, label="零样本", color="#5B9BD5")
    ax2.bar([i + w/2 for i in x], fb_ranks, w, label="反馈循环", color="#ED7D31")

    ax2.set_xticks(list(x))
    ax2.set_xticklabels(names, rotation=45, ha="right", fontsize=8)
    ax2.set_ylabel("Rank 得分", fontsize=11)
    ax2.set_title("各题目零样本 vs 反馈循环 Rank 对比 (Haiku)", fontsize=12)
    ax2.legend(fontsize=10)
    ax2.set_ylim(0, 1.1)
    ax2.axhline(y=1.0, color="green", linestyle="--", alpha=0.3, linewidth=0.8)
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    fig2.tight_layout()
    fig2.savefig(out_dir / "haiku_per_problem_rank.png", dpi=150)
    print(f"Saved: {out_dir / 'haiku_per_problem_rank.png'}")

    plt.close("all")
    print(f"Loaded input: {input_path}")
    print("Done.")


if __name__ == "__main__":
    main()
