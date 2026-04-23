"""Generate feedback granularity experiment charts.

Outputs:
  outputs/reports/fig_granularity_curve.png   — line chart: pass rate vs feedback level
  outputs/reports/fig_granularity_matrix.png  — heatmap: per-problem × per-level results
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Experiment data ──────────────────────────────────────────────────────────

LEVELS = ["L0\nZero-shot", "L1\nRetry-only", "L2\nCompile-only", "L3\nSuccinct", "L4\nRich"]
LEVELS_SHORT = ["L0:ZS", "L1:RO", "L2:CO", "L3:SU", "L4:RI"]

GPT_RATES = [58, 75, 92, 92, 83]   # 7/12, 9/12, 11/12, 11/12, 10/12
SON_RATES = [50, 67, 75, 67, 67]   # 6/12, 8/12, 9/12, 8/12, 8/12

PROBLEMS = [
    "float_multi", "multi_booth_8bit", "multi_pipe_8bit", "div_16bit",
    "adder_bcd", "fsm", "sequence_detector", "JC_counter",
    "LIFObuffer", "LFSR", "traffic_light", "freq_divbyfrac"
]

# Per-problem pass/fail (1=pass, 0=fail)
GPT_MATRIX = [
    #  ZS  RO  CO  SU  RI
    [1, 1, 1, 1, 1],  # float_multi
    [1, 1, 1, 1, 1],  # multi_booth_8bit
    [1, 1, 1, 1, 1],  # multi_pipe_8bit
    [0, 1, 1, 1, 1],  # div_16bit
    [1, 1, 1, 1, 1],  # adder_bcd
    [1, 1, 1, 1, 1],  # fsm
    [0, 0, 1, 1, 0],  # sequence_detector  ← rich HURTS
    [1, 1, 1, 1, 1],  # JC_counter
    [1, 1, 1, 1, 1],  # LIFObuffer
    [0, 0, 1, 1, 1],  # LFSR
    [0, 1, 1, 1, 1],  # traffic_light
    [0, 0, 0, 0, 0],  # freq_divbyfrac
]

SON_MATRIX = [
    [1, 1, 1, 1, 1],  # float_multi
    [1, 1, 1, 1, 1],  # multi_booth_8bit
    [1, 1, 1, 1, 1],  # multi_pipe_8bit
    [0, 1, 1, 0, 0],  # div_16bit  ← succinct & rich HURT
    [1, 1, 1, 1, 1],  # adder_bcd
    [1, 1, 1, 1, 1],  # fsm
    [0, 0, 1, 1, 1],  # sequence_detector
    [1, 1, 1, 1, 1],  # JC_counter
    [0, 0, 0, 0, 0],  # LIFObuffer
    [0, 0, 1, 0, 0],  # LFSR  ← only compile-only works
    [0, 1, 0, 1, 1],  # traffic_light
    [0, 0, 0, 0, 0],  # freq_divbyfrac
]


def chart_granularity_curve():
    """Line chart: pass rate vs feedback granularity level."""
    fig, ax = plt.subplots(figsize=(9, 5.5))

    x = np.arange(len(LEVELS))

    ax.plot(x, GPT_RATES, 'o-', color="#1B3A5C", linewidth=2.5, markersize=10,
            label="GPT-5.4", zorder=5)
    ax.plot(x, SON_RATES, 's--', color="#6495ED", linewidth=2.5, markersize=10,
            label="Sonnet 4.6", zorder=5)

    # Annotate values
    for i, (g, s) in enumerate(zip(GPT_RATES, SON_RATES)):
        ax.annotate(f"{g}%", (i, g), textcoords="offset points", xytext=(0, 12),
                    ha="center", fontsize=10, fontweight="bold", color="#1B3A5C")
        offset_y = -18 if s != g else -18
        ax.annotate(f"{s}%", (i, s), textcoords="offset points", xytext=(0, offset_y),
                    ha="center", fontsize=10, fontweight="bold", color="#6495ED")

    # Highlight the peak
    gpt_peak = max(GPT_RATES)
    gpt_peak_idx = GPT_RATES.index(gpt_peak)
    ax.axhline(y=gpt_peak, color="#1B3A5C", alpha=0.15, linestyle=":", linewidth=1)

    ax.set_xticks(x)
    ax.set_xticklabels(LEVELS, fontsize=9)
    ax.set_ylabel("Pass Rate (%)", fontsize=12)
    ax.set_ylim(35, 100)
    ax.yaxis.set_major_locator(plt.MultipleLocator(10))
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.legend(fontsize=11, loc="lower right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_title("Feedback Granularity Curve\nRTLLM STUDY_12 (12 problems, k=3, iter=5)",
                 fontsize=13, fontweight="bold", pad=10)

    # Add arrow annotation for "information overload"
    ax.annotate("Information\noverload?",
                xy=(4, GPT_RATES[4]), xytext=(4.3, GPT_RATES[4] + 8),
                arrowprops=dict(arrowstyle="->", color="#C44E52", lw=1.5),
                fontsize=9, color="#C44E52", fontstyle="italic", ha="left")

    fig.text(0.5, 0.01,
             "L0=single shot, L1=retry w/o feedback, L2=compile errors only, "
             "L3=compile+sim summary (default), L4=compile+sim+hints",
             ha="center", fontsize=7.5, color="gray", style="italic")

    fig.tight_layout(rect=[0, 0.03, 1, 1])
    out = OUT_DIR / "fig_granularity_curve.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[A] {out}")
    plt.close()


def chart_granularity_matrix():
    """Heatmap: per-problem × per-level results for both models."""
    fig, axes = plt.subplots(1, 2, figsize=(12, 6.5), sharey=True)

    for ax, matrix, name, rates in [
        (axes[0], GPT_MATRIX, "GPT-5.4", GPT_RATES),
        (axes[1], SON_MATRIX, "Sonnet 4.6", SON_RATES),
    ]:
        data = np.array(matrix)
        cmap = plt.cm.colors.ListedColormap(["#FFCDD2", "#C8E6C9"])  # red-ish, green-ish

        ax.imshow(data, cmap=cmap, aspect="auto", interpolation="nearest")

        # Add text labels
        for i in range(len(PROBLEMS)):
            for j in range(5):
                text = "✓" if data[i, j] else "✗"
                color = "#2E7D32" if data[i, j] else "#C62828"
                ax.text(j, i, text, ha="center", va="center",
                        fontsize=13, fontweight="bold", color=color)

        ax.set_xticks(range(5))
        ax.set_xticklabels(LEVELS_SHORT, fontsize=9)
        ax.set_yticks(range(len(PROBLEMS)))
        ax.set_yticklabels(PROBLEMS, fontsize=8)

        # Add pass rate at bottom
        for j, r in enumerate(rates):
            ax.text(j, len(PROBLEMS) - 0.15, f"{r}%",
                    ha="center", va="top", fontsize=8, fontweight="bold",
                    color="#1B3A5C",
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="white", alpha=0.8))

        ax.set_title(name, fontsize=13, fontweight="bold")

        # Grid
        ax.set_xticks([x - 0.5 for x in range(1, 5)], minor=True)
        ax.set_yticks([y - 0.5 for y in range(1, len(PROBLEMS))], minor=True)
        ax.grid(which="minor", color="white", linewidth=1.5)
        ax.tick_params(which="minor", size=0)

    # Legend
    pass_patch = mpatches.Patch(color="#C8E6C9", label="PASS")
    fail_patch = mpatches.Patch(color="#FFCDD2", label="FAIL")
    fig.legend(handles=[pass_patch, fail_patch], loc="lower center",
               ncol=2, fontsize=10, frameon=False)

    fig.suptitle("Feedback Granularity Matrix\nRTLLM STUDY_12 — Per-Problem Results",
                 fontsize=14, fontweight="bold", y=1.02)

    fig.tight_layout(rect=[0, 0.04, 1, 1])
    out = OUT_DIR / "fig_granularity_matrix.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[B] {out}")
    plt.close()


if __name__ == "__main__":
    print("Generating granularity charts...")
    chart_granularity_curve()
    chart_granularity_matrix()
    print("Done.")
