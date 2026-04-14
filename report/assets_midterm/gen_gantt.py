"""生成图表 F：项目阶段进展甘特图

基于 notes/current_status.md 中已记录的真实时间线。
"""

import sys
from pathlib import Path
from datetime import datetime

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT))

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from report.assets_midterm.plot_utils import configure_matplotlib_fonts, save_figure

configure_matplotlib_fonts()

# 真实项目阶段（基于 git log 和 notes 记录）
stages = [
    ("文献调研与选题确认",        "2026-02-20", "2026-03-15", "completed"),
    ("环境搭建与流水线验证",      "2026-03-15", "2026-04-01", "completed"),
    ("自定义任务集构建",          "2026-04-01", "2026-04-05", "completed"),
    ("反馈循环核心实现",          "2026-04-05", "2026-04-10", "completed"),
    ("VerilogEval 基准接入",      "2026-04-10", "2026-04-11", "completed"),
    ("Haiku 主实验执行",          "2026-04-11", "2026-04-12", "completed"),
    ("实验分析与图表整理",        "2026-04-12", "2026-04-14", "completed"),
    ("中期报告撰写",             "2026-04-11", "2026-04-14", "completed"),
    ("扩大实验规模",             "2026-04-15", "2026-05-10", "planned"),
    ("反馈策略优化",             "2026-04-20", "2026-05-15", "planned"),
    ("毕业论文撰写",             "2026-05-01", "2026-06-01", "planned"),
    ("答辩准备",                 "2026-05-25", "2026-06-10", "planned"),
]

fig, ax = plt.subplots(figsize=(10, 5.5))

colors = {"completed": "#4CAF50", "planned": "#BDBDBD"}
edge_colors = {"completed": "#2E7D32", "planned": "#757575"}

y_positions = list(range(len(stages) - 1, -1, -1))

for i, (name, start_s, end_s, status) in enumerate(stages):
    start = datetime.strptime(start_s, "%Y-%m-%d")
    end = datetime.strptime(end_s, "%Y-%m-%d")
    y = y_positions[i]
    ax.barh(y, (end - start).days, left=start, height=0.6,
            color=colors[status], edgecolor=edge_colors[status], linewidth=0.8)
    ax.text(start, y, f" {name}", va="center", ha="left", fontsize=8, fontweight="bold",
            color="#222" if status == "completed" else "#555")

# 中期检查线
midterm_date = datetime(2026, 4, 14)
ax.axvline(midterm_date, color="#C62828", linewidth=1.5, linestyle="--", zorder=5)
ax.text(midterm_date, len(stages) - 0.3, " 中期检查", fontsize=8, color="#C62828",
        fontweight="bold", va="bottom")

ax.set_yticks(y_positions)
ax.set_yticklabels([""] * len(stages))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
plt.xticks(fontsize=8, rotation=30)

ax.set_xlabel("日期 (2026年)", fontsize=9)
ax.set_title("项目阶段进展图", fontsize=13, fontweight="bold")

# Legend
from matplotlib.patches import Patch
legend_elements = [
    Patch(facecolor="#4CAF50", edgecolor="#2E7D32", label="已完成"),
    Patch(facecolor="#BDBDBD", edgecolor="#757575", label="计划中"),
]
ax.legend(handles=legend_elements, loc="lower right", fontsize=8)

ax.set_xlim(datetime(2026, 2, 15), datetime(2026, 6, 15))
ax.grid(axis="x", alpha=0.3)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

plt.tight_layout()
save_figure(fig, "report/figures/fig_project_gantt")
