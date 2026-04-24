"""Generate multi-turn v2 comparison charts (4-condition, bug-fixed)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PROBLEMS = ["div_16bit", "sequence_detector", "LFSR",
            "traffic_light", "freq_divbyfrac", "fsm"]

# ── GPT-5.4 v2 results ──────────────────────────────────────────────────────
# A:STk3  D:STk1  B:MTk1  C:COk3
GPT_PASS = [5, 5, 5, 5]  # out of 6,6,5(1 API err),6
GPT_TOTAL = [6, 6, 5, 6]
GPT_RATES = [round(p/t*100) for p, t in zip(GPT_PASS, GPT_TOTAL)]  # 83,83,100,83

GPT_MATRIX = [
    # A  D  B  C
    [1, 1, 1, 1],  # div_16bit
    [1, 1, 1, 1],  # sequence_detector
    [1, 1, 1, 1],  # LFSR
    [1, 1, 1, 1],  # traffic_light
    [0, 0, -1, 0], # freq_divbyfrac (-1 = API_ERR for B)
    [1, 1, 1, 1],  # fsm
]

# ── Sonnet 4.6 v2 results ───────────────────────────────────────────────────
SON_PASS = [1, 2, 3, 2]
SON_TOTAL = [6, 6, 6, 6]
SON_RATES = [round(p/t*100) for p, t in zip(SON_PASS, SON_TOTAL)]  # 17,33,50,33

SON_MATRIX = [
    # A  D  B  C
    [0, 0, 0, 0],  # div_16bit
    [0, 0, 1, 0],  # sequence_detector — MT only PASS!
    [0, 1, 1, 1],  # LFSR
    [0, 0, 0, 0],  # traffic_light
    [0, 0, 0, 0],  # freq_divbyfrac
    [1, 1, 1, 1],  # fsm
]

CONDITIONS = ["A: ST\nk=3", "D: ST\nk=1", "B: MT\nk=1", "C: CO\nk=3"]
CONDITIONS_SHORT = ["A:STk3", "D:STk1", "B:MTk1", "C:COk3"]


def chart_comparison():
    """Bar chart: 4-condition pass rate for each model."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    x = np.arange(len(CONDITIONS))
    width = 0.32

    bars_gpt = ax.bar(x - width/2, GPT_RATES, width, color="#1B3A5C",
                       label="GPT-5.4", zorder=3, edgecolor="white", linewidth=0.5)
    bars_son = ax.bar(x + width/2, SON_RATES, width, color="#6495ED",
                       label="Sonnet 4.6", zorder=3, edgecolor="white", linewidth=0.5)

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
    ax.set_ylim(0, 115)
    ax.yaxis.set_major_locator(plt.MultipleLocator(10))
    ax.grid(axis="y", alpha=0.3, linestyle="--", zorder=0)
    ax.legend(fontsize=11)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    ax.set_title("Single-turn vs Multi-turn Feedback (v2, bug-fixed)\n"
                 "Multiturn-6 Subset · 4 conditions · iter=5",
                 fontsize=13, fontweight="bold", pad=10)

    # Annotate Sonnet MT advantage
    ax.annotate("MT helps\nSonnet +33pp",
                xy=(2 + width/2, 50), xytext=(2.6, 75),
                arrowprops=dict(arrowstyle="->", color="#2E7D32", lw=1.5),
                fontsize=9, color="#2E7D32", fontstyle="italic", ha="center")

    # Note about GPT MT API error
    ax.annotate("*GPT MT: 5/5\n(1 API err excluded)",
                xy=(2 - width/2, 100), xytext=(1.0, 105),
                fontsize=7, color="#666", ha="center",
                arrowprops=dict(arrowstyle="->", color="#999", lw=0.8))

    fig.tight_layout()
    out = OUT_DIR / "fig_multiturn_comparison_v2.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[A] {out}")
    plt.close()


def chart_matrix():
    """Per-problem heatmap for both models, 4 conditions."""
    import matplotlib.patches as mpatches
    fig, axes = plt.subplots(1, 2, figsize=(10, 5.5), sharey=True)

    for ax, matrix, name, rates in [
        (axes[0], GPT_MATRIX, "GPT-5.4", GPT_RATES),
        (axes[1], SON_MATRIX, "Sonnet 4.6", SON_RATES),
    ]:
        data = np.array(matrix)
        # Custom colormap: -1=grey(ERR), 0=red(FAIL), 1=green(PASS)
        for i in range(len(PROBLEMS)):
            for j in range(4):
                val = data[i, j]
                if val == 1:
                    bg = "#C8E6C9"
                    text, color = "✓", "#2E7D32"
                elif val == 0:
                    bg = "#FFCDD2"
                    text, color = "✗", "#C62828"
                else:
                    bg = "#E0E0E0"
                    text, color = "ERR", "#616161"

                rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                     facecolor=bg, edgecolor="white", linewidth=1.5)
                ax.add_patch(rect)
                ax.text(j, i, text, ha="center", va="center",
                        fontsize=12 if val != -1 else 8,
                        fontweight="bold", color=color)

        ax.set_xlim(-0.5, 3.5)
        ax.set_ylim(len(PROBLEMS) - 0.5, -0.5)
        ax.set_xticks(range(4))
        ax.set_xticklabels(CONDITIONS_SHORT, fontsize=8)
        ax.set_yticks(range(len(PROBLEMS)))
        ax.set_yticklabels(PROBLEMS, fontsize=9)
        ax.set_title(name, fontsize=13, fontweight="bold")
        ax.set_aspect("equal")

    pass_p = mpatches.Patch(color="#C8E6C9", label="PASS")
    fail_p = mpatches.Patch(color="#FFCDD2", label="FAIL")
    err_p = mpatches.Patch(color="#E0E0E0", label="API ERR")
    fig.legend(handles=[pass_p, fail_p, err_p], loc="lower center",
               ncol=3, fontsize=10, frameon=False)

    fig.suptitle("Multi-turn Experiment Matrix (v2, bug-fixed)\nPer-Problem Results",
                 fontsize=14, fontweight="bold", y=1.02)
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    out = OUT_DIR / "fig_multiturn_matrix_v2.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[B] {out}")
    plt.close()


if __name__ == "__main__":
    print("Generating multi-turn v2 charts...")
    chart_comparison()
    chart_matrix()
    print("Done.")
