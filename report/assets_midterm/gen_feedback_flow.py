"""生成图表 B：AutoChip Feedback Loop 逻辑流程图

展示方法论层面的闭环逻辑，而非代码模块名。
"""

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT))

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

from report.assets_midterm.plot_utils import configure_matplotlib_fonts, save_figure

configure_matplotlib_fonts()

fig, ax = plt.subplots(figsize=(8, 11))
ax.set_xlim(0, 8)
ax.set_ylim(0, 11.5)
ax.axis("off")

def draw_process(ax, cx, cy, w, h, text, color="#E3F2FD"):
    box = FancyBboxPatch((cx - w/2, cy - h/2), w, h, boxstyle="round,pad=0.08",
                         facecolor=color, edgecolor="#333", linewidth=1.2)
    ax.add_patch(box)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=9, fontweight="bold")

def draw_diamond(ax, cx, cy, w, h, text, color="#FFF9C4"):
    diamond = plt.Polygon([(cx, cy+h/2), (cx+w/2, cy), (cx, cy-h/2), (cx-w/2, cy)],
                          facecolor=color, edgecolor="#333", linewidth=1.2)
    ax.add_patch(diamond)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=8, fontweight="bold")

def draw_io(ax, cx, cy, w, h, text, color="#E8F5E9"):
    # Parallelogram
    dx = 0.2
    para = plt.Polygon([(cx-w/2+dx, cy+h/2), (cx+w/2+dx, cy+h/2),
                         (cx+w/2-dx, cy-h/2), (cx-w/2-dx, cy-h/2)],
                        facecolor=color, edgecolor="#333", linewidth=1.2)
    ax.add_patch(para)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=8)

def arrow(ax, x1, y1, x2, y2, label="", color="#333"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.3))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        offset = 0.15 if x1 == x2 else 0.2
        ax.text(mx + 0.15, my, label, fontsize=7, color="#555", va="center")

# === Flow ===
CX = 4.0

# Start
draw_io(ax, CX, 10.8, 2.8, 0.5, "输入：任务描述 + 模块接口")

# Step 1: Zero-shot generation
arrow(ax, CX, 10.55, CX, 10.2)
draw_process(ax, CX, 9.8, 3.2, 0.6, "第 1 轮：LLM 零样本生成 (k 个候选)")

# Step 2: Extract
arrow(ax, CX, 9.5, CX, 9.1)
draw_process(ax, CX, 8.7, 3.0, 0.6, "提取 Verilog 模块代码")

# Step 3: Compile
arrow(ax, CX, 8.4, CX, 8.0)
draw_diamond(ax, CX, 7.5, 2.8, 0.8, "编译通过？")

# Compile fail
ax.annotate("", xy=(1.2, 7.5), xytext=(CX - 1.4, 7.5),
            arrowprops=dict(arrowstyle="-|>", color="#C62828", lw=1.2))
ax.text(1.8, 7.7, "否", fontsize=8, color="#C62828", fontweight="bold")
draw_process(ax, 1.2, 6.8, 1.8, 0.6, "提取编译\n错误信息", "#FFCDD2")

# Compile pass
arrow(ax, CX, 7.1, CX, 6.6, "是")
draw_process(ax, CX, 6.2, 3.0, 0.6, "运行功能仿真 (vvp)")

# Step 4: Sim check
arrow(ax, CX, 5.9, CX, 5.5)
draw_diamond(ax, CX, 5.0, 2.8, 0.8, "仿真全部通过？")

# Sim pass -> output
ax.annotate("", xy=(7.0, 5.0), xytext=(CX + 1.4, 5.0),
            arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=1.2))
ax.text(6.0, 5.2, "是", fontsize=8, color="#2E7D32", fontweight="bold")
draw_io(ax, 7.0, 4.3, 1.6, 0.5, "输出：通过", "#C8E6C9")

# Sim fail
arrow(ax, CX, 4.6, CX, 4.2, "否")
draw_process(ax, CX, 3.8, 3.0, 0.6, "统计不匹配样本数\n提取仿真错误信息", "#FFCDD2")

# Step 5: Rank & select best
arrow(ax, CX, 3.5, CX, 3.1)
draw_process(ax, CX, 2.7, 3.0, 0.6, "评分 (rank) 并选择最优候选")

# Step 6: Check iteration
arrow(ax, CX, 2.4, CX, 2.0)
draw_diamond(ax, CX, 1.5, 3.0, 0.8, "达到最大迭代次数？")

# Max reached -> output fail
ax.annotate("", xy=(7.0, 1.5), xytext=(CX + 1.5, 1.5),
            arrowprops=dict(arrowstyle="-|>", color="#C62828", lw=1.2))
ax.text(6.1, 1.7, "是", fontsize=8, color="#C62828", fontweight="bold")
draw_io(ax, 7.0, 0.8, 1.8, 0.5, "输出：未通过\n(最优 rank)", "#FFCDD2")

# No -> construct feedback
ax.text(2.3, 1.2, "否", fontsize=8, color="#2E7D32", fontweight="bold")
ax.annotate("", xy=(1.2, 1.5), xytext=(CX - 1.5, 1.5),
            arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=1.2))

draw_process(ax, 1.2, 2.0, 2.0, 0.6, "构造精简反馈\n(succinct feedback)", "#E8F5E9")

# Feedback -> compile-error join
ax.annotate("", xy=(1.2, 3.8), xytext=(1.2, 2.3),
            arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=1.5, linestyle="--"))

# compile error box -> feedback builder (join)
ax.annotate("", xy=(1.2, 2.6), xytext=(1.2, 6.5),
            arrowprops=dict(arrowstyle="-|>", color="#C62828", lw=1.2, linestyle="--"))

# feedback prompt -> back to LLM generation
ax.annotate("", xy=(CX - 1.6, 9.8), xytext=(1.2, 4.4),
            arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=2.0,
                          connectionstyle="arc3,rad=-0.4", linestyle="--"))
ax.text(0.3, 7.0, "反馈提示词\n→ 下一轮生成", fontsize=7, color="#2E7D32",
        fontweight="bold", ha="center", rotation=90)

# Title
ax.set_title("AutoChip 反馈循环逻辑流程图", fontsize=13, fontweight="bold", pad=12)

# Annotation
ax.text(CX, 0.2, "注：每轮生成 k 个候选（本实验 k=3），选 rank 最高者作为下一轮的基础",
        ha="center", va="center", fontsize=7, color="#666", style="italic")

plt.tight_layout()
save_figure(fig, "report/figures/fig_feedback_loop_flow")
