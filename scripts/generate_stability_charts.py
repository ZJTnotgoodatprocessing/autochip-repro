"""Generate stability experiment charts with mean + error bars.

Outputs:
  outputs/reports/fig_stability_ablation.png   — 3-condition with error bars
  outputs/reports/fig_stability_formal.png     — ZS vs FB with error bars
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "outputs" / "reports"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Data from 4 runs each ────────────────────────────────────────────────────

# GPT-5.4 (4 ablation runs)
GPT_ZS = [50, 50, 33, 67]
GPT_RO = [67, 58, 67, 58]
GPT_FB = [83, 75, 83, 75]

# Sonnet 4.6 (4 ablation runs)
SON_ZS = [75, 58, 58, 58]
SON_RO = [75, 67, 75, 75]
SON_FB = [58, 50, 58, 67]


def chart_ablation_errorbars():
    """Three-condition grouped bar chart with error bars for both models."""
    fig, ax = plt.subplots(figsize=(9, 5.5))
    
    models = ["GPT-5.4", "Sonnet 4.6"]
    x = np.arange(len(models))
    w = 0.22
    
    zs_means = [np.mean(GPT_ZS), np.mean(SON_ZS)]
    ro_means = [np.mean(GPT_RO), np.mean(SON_RO)]
    fb_means = [np.mean(GPT_FB), np.mean(SON_FB)]
    zs_stds = [np.std(GPT_ZS), np.std(SON_ZS)]
    ro_stds = [np.std(GPT_RO), np.std(SON_RO)]
    fb_stds = [np.std(GPT_FB), np.std(SON_FB)]
    
    bars_zs = ax.bar(x - w, zs_means, w, yerr=zs_stds,
                     label="Zero-shot", color="#B0C4DE", edgecolor="white",
                     capsize=4, error_kw={"linewidth": 1.5})
    bars_ro = ax.bar(x, ro_means, w, yerr=ro_stds,
                     label="Retry-only (k=3, iter=5)", color="#6495ED", edgecolor="white",
                     capsize=4, error_kw={"linewidth": 1.5})
    bars_fb = ax.bar(x + w, fb_means, w, yerr=fb_stds,
                     label="Feedback (k=3, iter=5)", color="#1B3A5C", edgecolor="white",
                     capsize=4, error_kw={"linewidth": 1.5})
    
    for bars, means, stds in [(bars_zs, zs_means, zs_stds),
                               (bars_ro, ro_means, ro_stds),
                               (bars_fb, fb_means, fb_stds)]:
        for bar, m, s in zip(bars, means, stds):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + s + 2,
                    f"{m:.0f}%", ha="center", va="bottom",
                    fontsize=10, fontweight="bold")
    
    ax.set_ylabel("Pass Rate (%)", fontsize=12)
    ax.set_title("Repeated Ablation Experiment (n=4 runs per model)\nMean ± Std on RTLLM STUDY_12",
                 fontsize=13, fontweight="bold", pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels(models, fontsize=12)
    ax.set_ylim(0, 100)
    ax.yaxis.set_major_locator(plt.MultipleLocator(20))
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    ax.legend(fontsize=9, loc="upper left")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    fig.text(0.5, 0.01,
             "Error bars = 1 SD across 4 independent runs (temperature=0.7)",
             ha="center", fontsize=8, color="gray", style="italic")
    
    fig.tight_layout(rect=[0, 0.03, 1, 1])
    out = OUT_DIR / "fig_stability_ablation.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[A] {out}")
    plt.close()


def chart_formal_errorbars():
    """ZS vs FB with error bars — formal experiment view."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 5), sharey=True)
    
    data = [
        ("GPT-5.4", GPT_ZS, GPT_FB),
        ("Sonnet 4.6", SON_ZS, SON_FB),
    ]
    
    colors_zs = "#B0C4DE"
    colors_fb = "#1B3A5C"
    
    for ax, (name, zs, fb) in zip(axes, data):
        conditions = ["Zero-shot", "Feedback"]
        means = [np.mean(zs), np.mean(fb)]
        stds = [np.std(zs), np.std(fb)]
        x = np.arange(2)
        
        bars = ax.bar(x, means, 0.5, yerr=stds,
                      color=[colors_zs, colors_fb], edgecolor="white",
                      capsize=6, error_kw={"linewidth": 2})
        
        for bar, m, s in zip(bars, means, stds):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + s + 2,
                    f"{m:.1f}%\n±{s:.1f}", ha="center", va="bottom",
                    fontsize=10, fontweight="bold")
        
        # Individual data points
        for i, vals in enumerate([zs, fb]):
            jitter = np.random.RandomState(42).uniform(-0.08, 0.08, len(vals))
            ax.scatter(np.full(len(vals), i) + jitter, vals,
                      color="black", alpha=0.4, s=30, zorder=5)
        
        gain = np.mean(fb) - np.mean(zs)
        arrow_color = "#27ae60" if gain > 0 else "#C44E52"
        sign = "+" if gain > 0 else ""
        ax.annotate(f"{sign}{gain:.1f}pp",
                   xy=(1, np.mean(fb)), xytext=(0, np.mean(zs)),
                   arrowprops=dict(arrowstyle="->", color=arrow_color, lw=2),
                   fontsize=11, fontweight="bold", color=arrow_color,
                   ha="center", va="center")
        
        ax.set_title(name, fontsize=13, fontweight="bold")
        ax.set_xticks(x)
        ax.set_xticklabels(conditions, fontsize=10)
        ax.set_ylim(0, 100)
        ax.yaxis.set_major_locator(plt.MultipleLocator(20))
        ax.grid(axis="y", alpha=0.3, linestyle="--")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
    
    axes[0].set_ylabel("Pass Rate (%)", fontsize=12)
    
    fig.suptitle("Repeated Experiment: Zero-shot vs Feedback (n=4)\nRTLLM STUDY_12",
                fontsize=14, fontweight="bold", y=1.02)
    fig.text(0.5, -0.02,
             "Black dots = individual runs. Error bars = 1 SD.",
             ha="center", fontsize=8, color="gray", style="italic")
    
    fig.tight_layout()
    out = OUT_DIR / "fig_stability_formal.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"[B] {out}")
    plt.close()


if __name__ == "__main__":
    print("Generating stability charts...")
    chart_ablation_errorbars()
    chart_formal_errorbars()
    print("Done.")
