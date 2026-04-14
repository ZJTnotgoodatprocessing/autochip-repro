"""生成图表 A：系统总体架构图

基于真实项目模块结构绘制，体现完整闭环：
任务输入 → 提示词构建 → LLM 生成 → Verilog 提取 → 编译 → 仿真 → 评分 → 反馈 → 再生成
"""

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT))

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

from report.assets_midterm.plot_utils import configure_matplotlib_fonts, save_figure

configure_matplotlib_fonts()

fig, ax = plt.subplots(figsize=(12, 7.5))
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.axis("off")

def draw_box(ax, x, y, w, h, label_cn, label_en, color="#E8E8E8", fontsize=9):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                         facecolor=color, edgecolor="#333333", linewidth=1.2)
    ax.add_patch(box)
    ax.text(x + w/2, y + h/2 + 0.15, label_cn, ha="center", va="center",
            fontsize=fontsize, fontweight="bold", color="#222222")
    ax.text(x + w/2, y + h/2 - 0.2, label_en, ha="center", va="center",
            fontsize=7, color="#555555", style="italic")

def draw_arrow(ax, x1, y1, x2, y2, label="", color="#333333"):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5))
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx, my + 0.15, label, ha="center", va="bottom", fontsize=7, color="#666666")

# === 模块布局 ===
# Row 1: 输入
draw_box(ax, 0.3, 6.5, 2.2, 0.9, "任务加载器", "task.py / verilogeval_loader.py", "#D0E8FF")

# Row 2: 提示词 + LLM
draw_box(ax, 0.3, 4.8, 2.2, 0.9, "提示词构建器", "prompt_builder.py", "#D0E8FF")
draw_box(ax, 4.0, 4.8, 2.2, 0.9, "LLM 客户端", "client.py", "#FFE0B2")

# Row 3: 提取 + 编译仿真
draw_box(ax, 4.0, 3.0, 2.2, 0.9, "Verilog 提取器", "extract_verilog.py", "#D0E8FF")
draw_box(ax, 7.5, 4.0, 2.5, 0.9, "编译器 (iverilog)", "verilog_executor.py", "#E0E0E0")
draw_box(ax, 7.5, 2.8, 2.5, 0.9, "仿真器 (vvp)", "verilog_executor.py", "#E0E0E0")

# Row 4: 评分
draw_box(ax, 7.5, 1.2, 2.5, 0.9, "评分器", "ranker.py", "#D0E8FF")

# 反馈循环控制器 (大框)
feedback_box = FancyBboxPatch((3.5, 0.3), 3.2, 1.0, boxstyle="round,pad=0.1",
                               facecolor="#E8F5E9", edgecolor="#2E7D32", linewidth=1.8)
ax.add_patch(feedback_box)
ax.text(5.1, 0.95, "反馈循环控制器", ha="center", va="center",
        fontsize=10, fontweight="bold", color="#2E7D32")
ax.text(5.1, 0.6, "loop_runner.py", ha="center", va="center",
        fontsize=7, color="#388E3C", style="italic")

# === 数据 / 外部资源标注 ===
# VerilogEval benchmark
ax.text(0.3, 7.7, "VerilogEval-Human\n基准测试集 (20 题)", ha="left", va="center",
        fontsize=8, color="#333333",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF9C4", edgecolor="#F9A825"))

# Anthropic API
ax.text(5.1, 6.2, "Anthropic API\n(Claude Haiku)", ha="center", va="center",
        fontsize=8, color="#333333",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFE0B2", edgecolor="#E65100"))

# 输出
ax.text(10.8, 0.7, "实验结果\nJSON/CSV", ha="center", va="center",
        fontsize=8, color="#333333",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="#FFF9C4", edgecolor="#F9A825"))

# === 箭头 ===
# benchmark -> task loader
draw_arrow(ax, 1.4, 7.35, 1.4, 7.4)
ax.annotate("", xy=(1.4, 7.4), xytext=(1.4, 7.35),
            arrowprops=dict(arrowstyle="-|>", color="#333", lw=1.2))

# task loader -> prompt builder
draw_arrow(ax, 1.4, 6.5, 1.4, 5.7, "任务描述\n模块接口")

# prompt builder -> LLM
draw_arrow(ax, 2.5, 5.25, 4.0, 5.25, "提示词")

# API -> LLM
draw_arrow(ax, 5.1, 5.85, 5.1, 5.7)

# LLM -> extractor
draw_arrow(ax, 5.1, 4.8, 5.1, 3.9, "原始响应")

# extractor -> compiler
draw_arrow(ax, 6.2, 3.45, 7.5, 4.45, "Verilog 代码")

# compiler -> simulator
draw_arrow(ax, 8.75, 4.0, 8.75, 3.7)

# simulator -> ranker
draw_arrow(ax, 8.75, 2.8, 8.75, 2.1, "仿真结果")

# ranker -> output
draw_arrow(ax, 10.0, 1.65, 10.8, 1.2)

# ranker -> feedback controller
draw_arrow(ax, 7.5, 1.45, 6.7, 0.95, "评分 + 错误信息")

# feedback controller -> prompt builder (feedback loop)
ax.annotate("", xy=(1.4, 4.8), xytext=(3.5, 0.8),
            arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=2.0,
                          connectionstyle="arc3,rad=-0.3", linestyle="--"))
ax.text(1.0, 2.8, "反馈提示词\n(succinct feedback)", ha="center", va="center",
        fontsize=7, color="#2E7D32", fontweight="bold", rotation=60)

# 图例标注
legend_items = [
    mpatches.Patch(facecolor="#D0E8FF", edgecolor="#333", label="核心处理模块"),
    mpatches.Patch(facecolor="#FFE0B2", edgecolor="#333", label="外部 LLM 服务"),
    mpatches.Patch(facecolor="#E0E0E0", edgecolor="#333", label="EDA 工具 (iverilog/vvp)"),
    mpatches.Patch(facecolor="#E8F5E9", edgecolor="#2E7D32", label="反馈循环控制"),
]
ax.legend(handles=legend_items, loc="upper right", fontsize=7, framealpha=0.9)

ax.set_title("系统总体架构图", fontsize=14, fontweight="bold", pad=15)

plt.tight_layout()
save_figure(fig, "report/figures/fig_system_architecture")
