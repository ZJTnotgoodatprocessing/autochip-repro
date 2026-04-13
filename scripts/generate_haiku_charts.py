"""Generate bar chart for Haiku main experiment results."""

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

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

PROJECT = Path(__file__).resolve().parent.parent
DATA = json.loads((PROJECT / "outputs/verilogeval_both_20260412_173450.json").read_text("utf-8"))
OUT = PROJECT / "outputs" / "reports"
OUT.mkdir(exist_ok=True)

results = DATA["results"]
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
fig.savefig(OUT / "haiku_pass_rate_bar.png", dpi=150)
print(f"Saved: {OUT / 'haiku_pass_rate_bar.png'}")

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
fig2.savefig(OUT / "haiku_per_problem_rank.png", dpi=150)
print(f"Saved: {OUT / 'haiku_per_problem_rank.png'}")

plt.close("all")
print("Done.")
