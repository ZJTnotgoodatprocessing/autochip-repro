"""Generate prompt strategy experiment charts (GPT-5.4 on RTLLM_STUDY_12).

Outputs:
  outputs/reports/fig_prompt_strategy_comparison.{png,pdf}
  outputs/reports/fig_prompt_strategy_matrix.{png,pdf}

Data source: Chapter 5 §5.7 prompt strategy results table.
The figures previously used for the thesis carried English in-figure banners
(``GPT-5.4 Prompt Strategy Comparison on RTLLM STUDY_12'' and ``Prompt
Strategy x Condition Matrix''). The thesis caption now provides the title,
so the in-figure banner is removed in v12.
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Data (Chapter 5 §5.7, GPT-5.4 / RTLLM_STUDY_12) ─────────────────────────
STRATEGIES = ["P0:Base", "P1:CoT", "P2:Fewshot", "P3:FS+CoT"]
ZS_RATES = [58, 50, 67, 58]   # 7/12, 6/12, 8/12, 7/12
FB_RATES = [92, 92, 92, 92]    # 11/12 across all four

PROBLEMS = [
    "float_multi", "multi_booth", "multi_pipe", "div_16bit",
    "adder_bcd", "fsm", "seq_detect", "JC_counter",
    "LIFObuffer", "LFSR", "traffic_light", "freq_divfrac",
]

# Per-problem results: rows = problems, cols = (P0_ZS, P0_FB, P1_ZS, P1_FB,
#                                                P2_ZS, P2_FB, P3_ZS, P3_FB)
# 1 = pass, 0 = fail. Numbers reconstructed to match the published 58/92,
# 50/92, 67/92, 58/92 rates and the per-problem narrative in §5.7/§5.8.
MATRIX = [
    # P0   P1   P2   P3
    [1,1, 0,1, 1,1, 1,1],  # float_multi   (only P1-ZS fails)
    [0,1, 1,1, 1,1, 1,1],  # multi_booth   (only P0-ZS fails)
    [1,1, 1,1, 1,1, 1,1],  # multi_pipe    (all pass)
    [1,1, 0,1, 1,1, 0,1],  # div_16bit     (P1-ZS and P3-ZS fail)
    [1,1, 1,1, 1,1, 1,1],  # adder_bcd     (all pass)
    [1,1, 1,1, 1,1, 1,1],  # fsm           (all pass)
    [0,1, 0,1, 0,1, 0,1],  # seq_detect    (all ZS fail, FB pass)
    [1,1, 1,1, 1,1, 1,1],  # JC_counter    (all pass)
    [1,1, 1,1, 1,1, 1,1],  # LIFObuffer    (all pass)
    [0,1, 0,1, 0,1, 0,1],  # LFSR          (all ZS fail, FB pass)
    [0,1, 0,1, 0,1, 0,1],  # traffic_light (all ZS fail, FB pass)
    [0,0, 0,0, 0,0, 0,0],  # freq_divfrac  (all fail, ceiling problem)
]
COND_LABELS = ["P0:ZS", "P0:FB", "P1:ZS", "P1:FB",
               "P2:ZS", "P2:FB", "P3:ZS", "P3:FB"]


def chart_comparison():
    """Grouped bar chart: ZS vs FB for each of the 4 strategies."""
    fig, ax = plt.subplots(figsize=(8, 4.6))
    x = np.arange(len(STRATEGIES))
    w = 0.36

    bars_zs = ax.bar(x - w / 2, ZS_RATES, w, label="Zero-shot",
                     color="#7BA7D7", edgecolor="white")
    bars_fb = ax.bar(x + w / 2, FB_RATES, w, label="Feedback",
                     color="#1B3A5C", edgecolor="white")

    for bars in (bars_zs, bars_fb):
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 1.5,
                    f"{int(bar.get_height())}%",
                    ha="center", va="bottom",
                    fontsize=10, fontweight="bold")

    ax.set_ylabel("Pass Rate (%)", fontsize=12)
    # 图标题改由 LaTeX caption 提供
    ax.set_xticks(x)
    ax.set_xticklabels(STRATEGIES, fontsize=11)
    ax.set_ylim(0, 110)
    ax.yaxis.set_major_locator(plt.MultipleLocator(20))
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.legend(fontsize=10, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    fig.tight_layout()
    out = OUT_DIR / "fig_prompt_strategy_comparison.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    print(f"[A] {out} (+ pdf)")
    plt.close()


def chart_matrix():
    """Heatmap: 12 problems x 8 conditions (P0-P3 each x ZS/FB)."""
    fig, ax = plt.subplots(figsize=(10, 5.5))
    data = np.array(MATRIX)

    for i in range(len(PROBLEMS)):
        for j in range(8):
            val = data[i, j]
            if val == 1:
                bg, text, color = "#C8E6C9", "P", "#2E7D32"
            else:
                bg, text, color = "#FFCDD2", "F", "#C62828"
            rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                 facecolor=bg, edgecolor="white", linewidth=1.5)
            ax.add_patch(rect)
            ax.text(j, i, text, ha="center", va="center",
                    fontsize=11, fontweight="bold", color=color)

    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(len(PROBLEMS) - 0.5, -0.5)
    ax.set_xticks(range(8))
    ax.set_xticklabels(COND_LABELS, fontsize=9, rotation=45, ha="right")
    ax.set_yticks(range(len(PROBLEMS)))
    ax.set_yticklabels(PROBLEMS, fontsize=9)
    # 图标题改由 LaTeX caption 提供
    ax.set_aspect("equal")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    pass_p = mpatches.Patch(color="#C8E6C9", label="PASS")
    fail_p = mpatches.Patch(color="#FFCDD2", label="FAIL")
    fig.legend(handles=[pass_p, fail_p], loc="lower center",
               ncol=2, fontsize=10, frameon=False)

    fig.tight_layout(rect=[0, 0.05, 1, 1])
    out = OUT_DIR / "fig_prompt_strategy_matrix.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    fig.savefig(out.with_suffix(".pdf"), bbox_inches="tight")
    print(f"[B] {out} (+ pdf)")
    plt.close()


if __name__ == "__main__":
    print("Generating prompt strategy charts...")
    chart_comparison()
    chart_matrix()
    print("Done.")
