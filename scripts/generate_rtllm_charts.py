"""Generate formal experiment charts for RTLLM STUDY_12 results.

Outputs:
  outputs/reports/fig_passrate_comparison.png   — Chart A: 3-model pass rate comparison
  outputs/reports/fig_per_problem_matrix.png    — Chart B: per-problem improvement matrix
  outputs/reports/fig_feedback_gain.png         — Chart C: feedback gain ranking
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Data ─────────────────────────────────────────────────────────────────────

MODELS = ["Haiku 4.5", "Sonnet 4.6", "GPT-5.4"]
ZS_RATES = [42, 42, 50]
FB_RATES = [50, 58, 83]
FB_IMPROVED = [2, 2, 4]

PROBLEMS = [
    "float_multi", "multi_booth_8bit", "multi_pipe_8bit", "div_16bit",
    "adder_bcd", "fsm", "sequence_detector", "JC_counter",
    "LIFObuffer", "LFSR", "traffic_light", "freq_divbyfrac",
]

# Per-problem results: 0=FAIL, 1=PASS, -1=compile fail
DATA = {
    "Haiku 4.5": {
        "zs": [0, 1, 1, 1, 1, 0, -1, 1, 0, -1, 0, 0],
        "fb": [0, 1, 0, 1, 1, 1, -1, 1, 1, -1, 0, 0],
    },
    "Sonnet 4.6": {
        "zs": [0, 1, 1, 0, 1, 1, -1, 1, 0, -1, 0, 0],
        "fb": [1, 1, 1, 1, 1, 1, -1, 1, 0, -1, 0, 0],
    },
    "GPT-5.4": {
        "zs": [0, 1, 1, 0, 1, 1, -1, 1, 1, -1, 0, 0],
        "fb": [1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 0],
    },
}


def chart_a_passrate():
    """Chart A: 3-model pass rate bar comparison."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    x = np.arange(len(MODELS))
    w = 0.32
    
    bars_zs = ax.bar(x - w/2, ZS_RATES, w, label="Zero-shot", color="#7BAFD4", edgecolor="white", linewidth=0.5)
    bars_fb = ax.bar(x + w/2, FB_RATES, w, label="Feedback", color="#2B5C8A", edgecolor="white", linewidth=0.5)
    
    # Value labels
    for bar in bars_zs:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f"{int(bar.get_height())}%", ha="center", va="bottom", fontsize=11, fontweight="bold")
    for bar in bars_fb:
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                f"{int(bar.get_height())}%", ha="center", va="bottom", fontsize=11, fontweight="bold")
    
    # Improvement annotations
    for i, (zs, fb) in enumerate(zip(ZS_RATES, FB_RATES)):
        gain = fb - zs
        ax.annotate(f"+{gain}pp", xy=(x[i] + w/2, fb + 6), fontsize=9,
                    ha="center", color="#C44E52", fontweight="bold")
    
    ax.set_ylabel("Pass Rate (%)", fontsize=12)
    ax.set_title("RTLLM STUDY_12: Zero-shot vs Feedback Pass Rate", fontsize=13, fontweight="bold", pad=15)
    ax.set_xticks(x)
    ax.set_xticklabels(MODELS, fontsize=11)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_locator(plt.MultipleLocator(20))
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.legend(fontsize=10, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    fig.text(0.5, 0.01, "n=12 problems | feedback: k=3, max_iter=5 | temperature=0.7",
             ha="center", fontsize=8, color="gray")
    
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    out = OUT_DIR / "fig_passrate_comparison.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[A] {out}")
    plt.close()


def chart_b_per_problem():
    """Chart B: per-problem improvement heatmap matrix."""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    n_prob = len(PROBLEMS)
    n_model = len(MODELS)
    
    # Build matrix: each cell = (zs_status, fb_status)
    # Color coding: green=pass, red=fail, orange=improved, dark_red=compile_fail
    cell_w = 1.0
    cell_h = 1.0
    
    colors = {
        "pass_both": "#4CAF50",      # green - ZS pass, FB pass
        "improved":  "#FF9800",       # orange - ZS fail, FB pass
        "fail_both": "#E57373",       # light red - both fail (sim)
        "compile_fail": "#B71C1C",    # dark red - compile fail
        "regressed": "#9E9E9E",       # gray - ZS pass, FB fail
    }
    
    for mi, model in enumerate(MODELS):
        zs = DATA[model]["zs"]
        fb = DATA[model]["fb"]
        for pi in range(n_prob):
            # Determine cell category
            if zs[pi] == -1 or fb[pi] == -1:
                cat = "compile_fail"
                label = "X"
            elif zs[pi] == 1 and fb[pi] == 1:
                cat = "pass_both"
                label = "P"
            elif zs[pi] == 0 and fb[pi] == 1:
                cat = "improved"
                label = "+"
            elif zs[pi] == 1 and fb[pi] == 0:
                cat = "regressed"
                label = "R"
            else:
                cat = "fail_both"
                label = "F"
            
            x = pi * cell_w
            y = (n_model - 1 - mi) * cell_h
            rect = plt.Rectangle((x, y), cell_w * 0.92, cell_h * 0.85,
                                  facecolor=colors[cat], edgecolor="white", linewidth=1.5)
            ax.add_patch(rect)
            ax.text(x + cell_w * 0.46, y + cell_h * 0.42, label,
                    ha="center", va="center", fontsize=11, fontweight="bold",
                    color="white" if cat in ("compile_fail", "pass_both") else "black")
    
    ax.set_xlim(-0.1, n_prob * cell_w)
    ax.set_ylim(-0.1, n_model * cell_h)
    ax.set_xticks([i * cell_w + cell_w * 0.46 for i in range(n_prob)])
    ax.set_xticklabels(PROBLEMS, rotation=45, ha="right", fontsize=9)
    ax.set_yticks([i * cell_h + cell_h * 0.42 for i in range(n_model)])
    ax.set_yticklabels(list(reversed(MODELS)), fontsize=11)
    ax.set_title("Per-Problem Result Matrix (RTLLM STUDY_12)", fontsize=13, fontweight="bold", pad=15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(left=False, bottom=False)
    
    # Legend
    legend_items = [
        mpatches.Patch(facecolor=colors["pass_both"], label="P = ZS Pass, FB Pass"),
        mpatches.Patch(facecolor=colors["improved"], label="+ = Improved by Feedback"),
        mpatches.Patch(facecolor=colors["fail_both"], label="F = Both Failed (sim)"),
        mpatches.Patch(facecolor=colors["compile_fail"], label="X = Compile Failure"),
        mpatches.Patch(facecolor=colors["regressed"], label="R = Regressed"),
    ]
    ax.legend(handles=legend_items, loc="upper right", bbox_to_anchor=(1.01, -0.15),
              ncol=3, fontsize=8, frameon=False)
    
    fig.tight_layout()
    out = OUT_DIR / "fig_per_problem_matrix.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[B] {out}")
    plt.close()


def chart_c_feedback_gain():
    """Chart C: feedback gain ranking (horizontal bar)."""
    fig, ax = plt.subplots(figsize=(7, 3.5))
    
    gains = [fb - zs for zs, fb in zip(ZS_RATES, FB_RATES)]
    colors_bar = ["#7BAFD4", "#5B8DB8", "#2B5C8A"]
    
    y = np.arange(len(MODELS))
    bars = ax.barh(y, gains, height=0.55, color=colors_bar, edgecolor="white", linewidth=0.5)
    
    for bar, gain, imp in zip(bars, gains, FB_IMPROVED):
        ax.text(bar.get_width() + 0.8, bar.get_y() + bar.get_height()/2,
                f"+{gain}pp ({imp} problems)", va="center", fontsize=11, fontweight="bold")
    
    ax.set_yticks(y)
    ax.set_yticklabels(MODELS, fontsize=11)
    ax.set_xlabel("Feedback Gain (percentage points)", fontsize=11)
    ax.set_title("Feedback Improvement by Model", fontsize=13, fontweight="bold", pad=10)
    ax.set_xlim(0, max(gains) + 15)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.invert_yaxis()
    
    fig.tight_layout()
    out = OUT_DIR / "fig_feedback_gain.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[C] {out}")
    plt.close()


if __name__ == "__main__":
    print("Generating RTLLM STUDY_12 formal charts...")
    chart_a_passrate()
    chart_b_per_problem()
    chart_c_feedback_gain()
    print("Done.")
