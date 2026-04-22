"""Generate ablation experiment charts for RTLLM STUDY_12.

Outputs:
  outputs/reports/fig_ablation_comparison.png  — 3-condition pass rate comparison
  outputs/reports/fig_ablation_decomposition.png — Improvement decomposition (stacked)
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Data ─────────────────────────────────────────────────────────────────────

MODELS = ["Sonnet 4.6", "GPT-5.4"]
ZS = [75, 50]
RO = [75, 67]
FB = [58, 83]

# GPT-5.4 per-problem (for decomposition focus)
PROBLEMS = [
    "float_multi", "multi_booth_8bit", "multi_pipe_8bit", "div_16bit",
    "adder_bcd", "fsm", "sequence_detector", "JC_counter",
    "LIFObuffer", "LFSR", "traffic_light", "freq_divbyfrac",
]
GPT_ZS = [1,1,0,0,1,1,0,1,1,0,0,0]
GPT_RO = [1,1,1,1,1,1,0,1,1,0,0,0]
GPT_FB = [1,1,1,1,1,1,1,1,1,0,1,0]


def chart_ablation_comparison():
    """Three-condition grouped bar chart for both models."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    x = np.arange(len(MODELS))
    w = 0.25
    
    bars_zs = ax.bar(x - w, ZS, w, label="Zero-shot (1 attempt)", color="#B0C4DE", edgecolor="white")
    bars_ro = ax.bar(x, RO, w, label="Retry-only (k=3, iter=5)", color="#6495ED", edgecolor="white")
    bars_fb = ax.bar(x + w, FB, w, label="Feedback (k=3, iter=5)", color="#1B3A5C", edgecolor="white")
    
    for bars in [bars_zs, bars_ro, bars_fb]:
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
                    f"{int(bar.get_height())}%", ha="center", va="bottom",
                    fontsize=11, fontweight="bold")
    
    ax.set_ylabel("Pass Rate (%)", fontsize=12)
    ax.set_title("Ablation Study: Zero-shot vs Retry-only vs Feedback\n(RTLLM STUDY_12)",
                 fontsize=13, fontweight="bold", pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(MODELS, fontsize=12)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_locator(plt.MultipleLocator(20))
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.legend(fontsize=9, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    fig.text(0.5, 0.01, "Retry-only uses identical API budget as Feedback, but without error information",
             ha="center", fontsize=8, color="gray", style="italic")
    
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    out = OUT_DIR / "fig_ablation_comparison.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[A] {out}")
    plt.close()


def chart_improvement_decomposition():
    """Stacked bar showing improvement decomposition for GPT-5.4."""
    fig, ax = plt.subplots(figsize=(7, 4.5))
    
    # GPT-5.4 decomposition
    zs_rate = 50
    ro_gain = 67 - 50   # +17pp from multi-sampling
    fb_gain = 83 - 67   # +16pp from feedback signal
    
    labels = ["GPT-5.4"]
    x = np.arange(len(labels))
    w = 0.45
    
    ax.barh(x, zs_rate, height=w, label=f"Zero-shot baseline ({zs_rate}%)",
            color="#B0C4DE", edgecolor="white")
    ax.barh(x, ro_gain, height=w, left=zs_rate,
            label=f"Multi-sampling gain (+{ro_gain}pp)",
            color="#6495ED", edgecolor="white")
    ax.barh(x, fb_gain, height=w, left=zs_rate + ro_gain,
            label=f"Feedback signal gain (+{fb_gain}pp)",
            color="#1B3A5C", edgecolor="white")
    
    # Annotations
    ax.text(zs_rate/2, 0, f"{zs_rate}%", ha="center", va="center",
            fontsize=12, fontweight="bold", color="black")
    ax.text(zs_rate + ro_gain/2, 0, f"+{ro_gain}pp", ha="center", va="center",
            fontsize=12, fontweight="bold", color="white")
    ax.text(zs_rate + ro_gain + fb_gain/2, 0, f"+{fb_gain}pp", ha="center", va="center",
            fontsize=12, fontweight="bold", color="white")
    
    # Total label
    ax.text(zs_rate + ro_gain + fb_gain + 1.5, 0, f"= {zs_rate + ro_gain + fb_gain}%",
            ha="left", va="center", fontsize=13, fontweight="bold", color="#C44E52")
    
    ax.set_xlim(0, 100)
    ax.set_yticks(x)
    ax.set_yticklabels(labels, fontsize=12)
    ax.set_xlabel("Pass Rate (%)", fontsize=11)
    ax.set_title("Improvement Decomposition: Multi-sampling vs Feedback Signal\n(GPT-5.4 on RTLLM STUDY_12)",
                 fontsize=12, fontweight="bold", pad=10)
    ax.legend(fontsize=9, loc="lower right")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.3, linestyle="--")
    
    # Key case callout
    ax.text(50, -0.55,
            "sequence_detector & traffic_light: only solvable by feedback (15 retries all failed)",
            ha="center", fontsize=8, color="#C44E52", style="italic")
    
    fig.tight_layout()
    out = OUT_DIR / "fig_ablation_decomposition.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[B] {out}")
    plt.close()


if __name__ == "__main__":
    print("Generating ablation charts...")
    chart_ablation_comparison()
    chart_improvement_decomposition()
    print("Done.")
