"""Generate thesis Chapter 3 figures: system architecture and feedback loop flow.

Produces:
  - figure/fig_system_architecture_v2.png
  - figure/fig_feedback_loop_v2.png

Requires: matplotlib (pip install matplotlib)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "report" / "thesis" / "latex" / "figure"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def _rounded_box(ax, xy, w, h, label, color="#4A90D9", fontsize=9, text_color="white"):
    """Draw a rounded rectangle with centered label."""
    box = mpatches.FancyBboxPatch(
        xy, w, h,
        boxstyle="round,pad=0.12",
        facecolor=color, edgecolor="#2C3E50", linewidth=1.2,
    )
    ax.add_patch(box)
    cx, cy = xy[0] + w / 2, xy[1] + h / 2
    ax.text(cx, cy, label, ha="center", va="center",
            fontsize=fontsize, color=text_color, fontweight="bold",
            fontfamily="sans-serif")


def _arrow(ax, start, end, color="#2C3E50"):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5))


def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.5, 7.5)
    ax.axis("off")
    ax.set_aspect("equal")

    # Title
    ax.text(5.25, 7.1, "System Module Architecture & Data Flow",
            ha="center", fontsize=13, fontweight="bold", fontfamily="sans-serif")

    # --- Modules ---
    bw, bh = 2.0, 0.7  # box width, height

    # Row 1: Benchmarks
    _rounded_box(ax, (0.3, 5.8), bw, bh, "VerilogEval\nLoader", "#27AE60")
    _rounded_box(ax, (3.0, 5.8), bw, bh, "RTLLM\nLoader", "#27AE60")

    # Row 2: Unified Task
    _rounded_box(ax, (1.6, 4.5), bw, bh, "Task Interface", "#E67E22")

    # Row 3: Prompt Builder + LLM Client
    _rounded_box(ax, (0.0, 3.2), bw, bh, "Prompt\nBuilder", "#4A90D9")
    _rounded_box(ax, (3.0, 3.2), bw, bh, "LLM Client\n(API Gateway)", "#4A90D9")

    # Row 4: Verilog Extractor + EDA
    _rounded_box(ax, (5.5, 4.5), bw, bh, "Verilog\nExtractor", "#8E44AD")
    _rounded_box(ax, (5.5, 3.2), bw, bh, "iverilog\nCompiler", "#C0392B")
    _rounded_box(ax, (8.2, 3.2), bw, bh, "VVP\nSimulator", "#C0392B")

    # Row 5: Ranker + Feedback Loop
    _rounded_box(ax, (5.5, 1.9), bw, bh, "Ranker\n(Scorer)", "#8E44AD")
    _rounded_box(ax, (2.5, 1.0), 3.0, bh, "Feedback Loop Controller", "#2C3E50")

    # Row 6: Artifact Manager
    _rounded_box(ax, (8.2, 1.9), bw, bh, "Artifact\nManager", "#16A085")
    _rounded_box(ax, (8.2, 0.7), bw, bh, "Outputs\n(JSON/CSV)", "#16A085")

    # --- Arrows ---
    # Loaders -> Task
    _arrow(ax, (1.3, 5.8), (2.2, 5.2))
    _arrow(ax, (4.0, 5.8), (3.2, 5.2))

    # Task -> Prompt Builder
    _arrow(ax, (2.1, 4.5), (1.0, 3.9))

    # Prompt Builder -> LLM
    _arrow(ax, (2.0, 3.55), (3.0, 3.55))

    # LLM -> Extractor
    _arrow(ax, (5.0, 3.55), (5.5, 4.5))

    # Extractor -> Compiler
    _arrow(ax, (6.5, 4.5), (6.5, 3.9))

    # Compiler -> Simulator
    _arrow(ax, (7.5, 3.55), (8.2, 3.55))

    # Simulator -> Ranker
    _arrow(ax, (9.2, 3.2), (7.2, 2.6))

    # Ranker -> Loop Controller
    _arrow(ax, (5.5, 2.1), (5.5, 1.7))

    # Loop Controller -> Prompt Builder (feedback arrow, curved)
    ax.annotate("", xy=(0.5, 3.2), xytext=(2.5, 1.3),
                arrowprops=dict(arrowstyle="-|>", color="#E74C3C", lw=2.0,
                                connectionstyle="arc3,rad=0.4"))
    ax.text(0.3, 2.1, "feedback", fontsize=8, color="#E74C3C",
            fontstyle="italic", fontfamily="sans-serif")

    # Ranker -> Artifact Manager
    _arrow(ax, (7.5, 2.15), (8.2, 2.15))
    # Artifact -> Outputs
    _arrow(ax, (9.2, 1.9), (9.2, 1.4))

    plt.tight_layout()
    out = OUT_DIR / "fig_system_architecture_v2.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"Saved: {out}")
    plt.close()


def generate_feedback_loop_flow():
    fig, ax = plt.subplots(figsize=(8, 11))
    ax.set_xlim(-1, 9)
    ax.set_ylim(-0.5, 12)
    ax.axis("off")
    ax.set_aspect("equal")

    ax.text(4, 11.5, "Feedback Loop Control Flow",
            ha="center", fontsize=13, fontweight="bold", fontfamily="sans-serif")

    bw, bh = 3.0, 0.6
    dw, dh = 2.4, 0.8  # diamond

    # Start
    ax.add_patch(plt.Circle((4, 10.8), 0.3, color="#2C3E50"))
    ax.text(4, 10.8, "Start", ha="center", va="center", color="white", fontsize=8, fontweight="bold")

    # Box: Build Initial Prompt
    _rounded_box(ax, (2.5, 9.6), bw, bh, "Build Initial Prompt", "#4A90D9", 9)
    _arrow(ax, (4, 10.5), (4, 10.2))

    # Box: Generate k Candidates
    _rounded_box(ax, (2.5, 8.5), bw, bh, "Generate k Candidates (LLM)", "#4A90D9", 9)
    _arrow(ax, (4, 9.6), (4, 9.1))

    # Box: Extract Verilog
    _rounded_box(ax, (2.5, 7.4), bw, bh, "Extract Verilog Code", "#8E44AD", 9)
    _arrow(ax, (4, 8.5), (4, 8.0))

    # Box: Compile (iverilog)
    _rounded_box(ax, (2.5, 6.3), bw, bh, "Compile (iverilog -g2012)", "#C0392B", 9)
    _arrow(ax, (4, 7.4), (4, 6.9))

    # Diamond: Compile OK?
    diamond1 = mpatches.FancyBboxPatch((2.8, 5.1), dw, dh,
                                        boxstyle="round,pad=0.05",
                                        facecolor="#F39C12", edgecolor="#2C3E50", lw=1.2)
    ax.add_patch(diamond1)
    ax.text(4, 5.5, "Compile\nSuccess?", ha="center", va="center", fontsize=8, fontweight="bold")
    _arrow(ax, (4, 6.3), (4, 5.9))

    # Compile fail -> Build compile feedback
    _rounded_box(ax, (6.0, 5.1), 2.2, bh, "Build Compile\nFeedback", "#E74C3C", 8)
    ax.annotate("No", xy=(6.0, 5.4), xytext=(5.2, 5.5),
                fontsize=8, color="#E74C3C", fontweight="bold")

    # Box: Simulate (vvp)
    _rounded_box(ax, (2.5, 3.9), bw, bh, "Simulate (vvp)", "#C0392B", 9)
    ax.annotate("Yes", xy=(4, 4.5), xytext=(3.2, 4.8),
                fontsize=8, color="#27AE60", fontweight="bold")
    _arrow(ax, (4, 5.1), (4, 4.5))

    # Diamond: Pass?
    diamond2 = mpatches.FancyBboxPatch((2.8, 2.7), dw, dh,
                                        boxstyle="round,pad=0.05",
                                        facecolor="#F39C12", edgecolor="#2C3E50", lw=1.2)
    ax.add_patch(diamond2)
    ax.text(4, 3.1, "rank = 1.0\n(Pass)?", ha="center", va="center", fontsize=8, fontweight="bold")
    _arrow(ax, (4, 3.9), (4, 3.5))

    # Pass -> Output best
    _rounded_box(ax, (2.5, 1.5), bw, bh, "Output Best Verilog", "#27AE60", 9)
    ax.annotate("Yes", xy=(4, 2.1), xytext=(3.2, 2.4),
                fontsize=8, color="#27AE60", fontweight="bold")
    _arrow(ax, (4, 2.7), (4, 2.1))

    # End
    ax.add_patch(plt.Circle((4, 0.7), 0.3, color="#2C3E50"))
    ax.text(4, 0.7, "End", ha="center", va="center", color="white", fontsize=8, fontweight="bold")
    _arrow(ax, (4, 1.5), (4, 1.0))

    # Fail -> check iterations
    _rounded_box(ax, (6.0, 2.7), 2.2, bh, "Update\nGlobal Best", "#E67E22", 8)
    ax.annotate("No", xy=(5.2, 3.0), xytext=(5.0, 3.3),
                fontsize=8, color="#E74C3C", fontweight="bold")
    _arrow(ax, (5.2, 3.1), (6.0, 3.0))

    # Sim fail -> Build sim feedback
    _rounded_box(ax, (6.0, 3.9), 2.2, bh, "Build Sim\nFeedback", "#E74C3C", 8)

    # Feedback arrows back to Generate (curved)
    ax.annotate("", xy=(5.3, 8.8), xytext=(7.1, 5.7),
                arrowprops=dict(arrowstyle="-|>", color="#E74C3C", lw=1.8,
                                connectionstyle="arc3,rad=-0.3"))
    ax.annotate("", xy=(5.3, 8.7), xytext=(7.1, 4.5),
                arrowprops=dict(arrowstyle="-|>", color="#E74C3C", lw=1.8,
                                connectionstyle="arc3,rad=-0.35"))
    ax.annotate("", xy=(5.3, 8.6), xytext=(7.1, 3.3),
                arrowprops=dict(arrowstyle="-|>", color="#E74C3C", lw=1.8,
                                connectionstyle="arc3,rad=-0.4"))

    ax.text(7.8, 7.0, "Next\nIteration", fontsize=8, color="#E74C3C",
            fontstyle="italic", ha="center", fontfamily="sans-serif")

    plt.tight_layout()
    out = OUT_DIR / "fig_feedback_loop_v2.png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"Saved: {out}")
    plt.close()


if __name__ == "__main__":
    generate_system_architecture()
    generate_feedback_loop_flow()
    print("Done.")
