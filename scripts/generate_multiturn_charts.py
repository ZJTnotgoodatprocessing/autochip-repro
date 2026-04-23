"""Generate multi-turn vs single-turn comparison charts."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Data ─────────────────────────────────────────────────────────────────────

PROBLEMS = ["div_16bit", "sequence_detector", "LFSR",
            "traffic_light", "freq_divbyfrac", "fsm"]

CONDITIONS = ["A: Single-turn\n(Succinct)", "B: Multi-turn\n(Succinct)", "C: Single-turn\n(Compile-only)"]
CONDITIONS_SHORT = ["ST(L3)", "MT(L3)", "CO(L2)"]

# Pass rates
GPT_RATES = [83, 33, 50]   # 5/6, 2/6, 3/6
SON_RATES = [67, 67, 67]   # 4/6, 4/6, 4/6

# Per-problem: 1=pass, 0=fail
#                          ST  MT  CO
GPT_MATRIX = [
    [1, 1, 1],  # div_16bit
    [1, 0, 0],  # sequence_detector
    [1, 0, 0],  # LFSR
    [1, 0, 1],  # traffic_light
    [0, 0, 0],  # freq_divbyfrac
    [1, 1, 1],  # fsm
]

SON_MATRIX = [
    [0, 0, 0],  # div_16bit
    [1, 1, 1],  # sequence_detector
    [1, 1, 1],  # LFSR
    [1, 1, 1],  # traffic_light
    [0, 0, 0],  # freq_divbyfrac
    [1, 1, 1],  # fsm
]


def chart_multiturn_comparison():
    """Bar chart: pass rate by condition for each model."""
    fig, ax = plt.subplots(figsize=(8, 5.5))

    x = np.arange(len(CONDITIONS))
    width = 0.32

    bars_gpt = ax.bar(x - width/2, GPT_RATES, width, color="#1B3A5C",
                       label="GPT-5.4", zorder=3, edgecolor="white", linewidth=0.5)
    bars_son = ax.bar(x + width/2, SON_RATES, width, color="#6495ED",
                       label="Sonnet 4.6", zorder=3, edgecolor="white", linewidth=0.5)

    # Annotate
    for bar in bars_gpt:
        h = bar.get_height()
        ax.annotate(f"{h}%", xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 5), textcoords="offset points",
                    ha="center", fontsize=11, fontweight="bold", color="#1B3A5C")
    for bar in bars_son:
        h = bar.get_height()
        ax.annotate(f"{h}%", xy=(bar.get_x() + bar.get_width()/2, h),
                    xytext=(0, 5), textcoords="offset points",
                    ha="center", fontsize=11, fontweight="bold", color="#6495ED")

    ax.set_xticks(x)
    ax.set_xticklabels(CONDITIONS, fontsize=9)
    ax.set_ylabel("Pass Rate (%)", fontsize=12)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_locator(plt.MultipleLocator(10))
    ax.grid(axis="y", alpha=0.3, linestyle="--", zorder=0)
    ax.legend(fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_title("Single-turn vs Multi-turn Feedback\nMultiturn-6 Subset (6 problems, k=3/1, iter=5)",
                 fontsize=13, fontweight="bold", pad=10)

    # Add annotation for GPT multi-turn drop
    ax.annotate("−50pp!\nMT hurts GPT",
                xy=(1 - width/2, 33), xytext=(1 - width/2 - 0.3, 60),
                arrowprops=dict(arrowstyle="->", color="#C44E52", lw=1.5),
                fontsize=9, color="#C44E52", fontstyle="italic", ha="center")

    fig.tight_layout()
    out = OUT_DIR / "fig_multiturn_comparison.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[A] {out}")
    plt.close()


def chart_multiturn_matrix():
    """Per-problem heatmap for both models."""
    import matplotlib.patches as mpatches

    fig, axes = plt.subplots(1, 2, figsize=(9, 5), sharey=True)

    for ax, matrix, name, rates in [
        (axes[0], GPT_MATRIX, "GPT-5.4", GPT_RATES),
        (axes[1], SON_MATRIX, "Sonnet 4.6", SON_RATES),
    ]:
        data = np.array(matrix)
        cmap = plt.cm.colors.ListedColormap(["#FFCDD2", "#C8E6C9"])

        ax.imshow(data, cmap=cmap, aspect="auto", interpolation="nearest")

        for i in range(len(PROBLEMS)):
            for j in range(3):
                text = "✓" if data[i, j] else "✗"
                color = "#2E7D32" if data[i, j] else "#C62828"
                ax.text(j, i, text, ha="center", va="center",
                        fontsize=14, fontweight="bold", color=color)

        ax.set_xticks(range(3))
        ax.set_xticklabels(CONDITIONS_SHORT, fontsize=9)
        ax.set_yticks(range(len(PROBLEMS)))
        ax.set_yticklabels(PROBLEMS, fontsize=9)

        for j, r in enumerate(rates):
            ax.text(j, len(PROBLEMS) - 0.15, f"{r}%",
                    ha="center", va="top", fontsize=8, fontweight="bold",
                    color="#1B3A5C",
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="white", alpha=0.8))

        ax.set_title(name, fontsize=13, fontweight="bold")

        ax.set_xticks([x - 0.5 for x in range(1, 3)], minor=True)
        ax.set_yticks([y - 0.5 for y in range(1, len(PROBLEMS))], minor=True)
        ax.grid(which="minor", color="white", linewidth=1.5)
        ax.tick_params(which="minor", size=0)

    pass_patch = mpatches.Patch(color="#C8E6C9", label="PASS")
    fail_patch = mpatches.Patch(color="#FFCDD2", label="FAIL")
    fig.legend(handles=[pass_patch, fail_patch], loc="lower center",
               ncol=2, fontsize=10, frameon=False)

    fig.suptitle("Multi-turn Experiment Matrix\nPer-Problem Results",
                 fontsize=14, fontweight="bold", y=1.02)

    fig.tight_layout(rect=[0, 0.04, 1, 1])
    out = OUT_DIR / "fig_multiturn_matrix.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[B] {out}")
    plt.close()


if __name__ == "__main__":
    print("Generating multi-turn charts...")
    chart_multiturn_comparison()
    chart_multiturn_matrix()
    print("Done.")
