"""生成图表 C/D/E：三张表格导出为图片

C: 项目模块—代码文件映射表
D: VerilogEval-Human 20 题子集构成表
E: 实验设置汇总表
"""

import sys
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT))

import matplotlib.pyplot as plt
import numpy as np

from report.assets_midterm.plot_utils import configure_matplotlib_fonts, save_figure

configure_matplotlib_fonts()


def render_table(data, col_widths, title, filename, col_colors=None, figsize=None):
    """Render a table as a publication-quality figure."""
    n_rows = len(data)
    n_cols = len(data[0])
    if figsize is None:
        figsize = (sum(col_widths) * 1.2, 0.45 * n_rows + 0.8)

    fig, ax = plt.subplots(figsize=figsize)
    ax.axis("off")
    ax.set_title(title, fontsize=12, fontweight="bold", pad=12)

    table = ax.table(
        cellText=data[1:],
        colLabels=data[0],
        cellLoc="center",
        loc="center",
        colWidths=col_widths,
    )

    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1, 1.6)

    # Style header
    for j in range(n_cols):
        cell = table[0, j]
        cell.set_facecolor("#455A64")
        cell.set_text_props(color="white", fontweight="bold", fontsize=9)

    # Style body rows
    for i in range(1, n_rows):
        for j in range(n_cols):
            cell = table[i, j]
            cell.set_facecolor("#F5F5F5" if i % 2 == 0 else "white")
            cell.set_edgecolor("#CCCCCC")
            if col_colors and j in col_colors:
                text = data[i][j]
                if text in col_colors[j]:
                    cell.set_text_props(color=col_colors[j][text])

    plt.tight_layout()
    save_figure(fig, f"report/figures/{filename}")
    plt.close()


# ============================================================
# 图表 C：项目模块—代码文件映射表
# ============================================================
table_c = [
    ["功能模块", "目录/关键文件", "作用说明"],
    ["任务加载器", "src/runner/task.py", "读取任务描述、模块接口和测试平台文件"],
    ["VerilogEval 适配器", "src/runner/verilogeval_loader.py", "从 VerilogEval 仓库加载题目，合并 ref+test 文件"],
    ["提示词构建器", "src/feedback/prompt_builder.py", "构造零样本提示词与 succinct feedback 提示词"],
    ["LLM 客户端", "src/llm/client.py", "封装 Anthropic API 调用，含指数退避重试机制"],
    ["Verilog 提取器", "src/utils/extract_verilog.py", "从 LLM 响应中提取 module...endmodule 代码块"],
    ["编译/仿真执行器", "src/runner/verilog_executor.py", "调用 iverilog 编译、vvp 仿真，解析不匹配统计"],
    ["评分器", "src/ranking/ranker.py", "基于仿真匹配率计算 0~1.0 连续评分"],
    ["反馈循环控制器", "src/feedback/loop_runner.py", "控制多轮迭代修复，管理 k 候选与全局最优追踪"],
    ["反馈模板", "prompts/feedback_succinct.txt", "succinct feedback 提示词模板"],
    ["主实验脚本", "scripts/run_verilogeval_subset.py", "在 VerilogEval 子集上运行零样本 vs 反馈对照实验"],
    ["图表生成脚本", "scripts/generate_haiku_charts.py", "生成实验结果可视化图表"],
]
render_table(table_c, [0.2, 0.35, 0.45], "项目模块与代码文件映射表", "tab_module_mapping",
             figsize=(11, 6))


# ============================================================
# 图表 D：VerilogEval-Human 20 题子集构成表
# ============================================================
table_d = [
    ["难度级别", "电路类型", "题数", "代表题目"],
    ["Easy", "组合逻辑 (Comb)", "5", "Prob001_zero, Prob007_wire, Prob014_andgate,\nProb024_hadd, Prob027_fadd"],
    ["Easy", "时序逻辑 (Seq)", "3", "Prob031_dff, Prob035_count1to10, Prob041_dff8r"],
    ["Medium", "组合逻辑 (Comb)", "3", "Prob022_mux2to1, Prob025_reduction, Prob050_kmap1"],
    ["Medium", "时序逻辑 (Seq)", "4", "Prob054_edgedetect, Prob068_countbcd,\nProb082_lfsr32, Prob085_shift4"],
    ["Medium-Hard", "组合逻辑 (Comb)", "1", "Prob030_popcount255"],
    ["Hard", "有限状态机 (FSM)", "3", "Prob109_fsm1, Prob127_lemmings1, Prob140_fsm_hdlc"],
    ["Very Hard", "时序逻辑 (Seq)", "1", "Prob144_conwaylife"],
]
render_table(table_d, [0.15, 0.2, 0.08, 0.57], "VerilogEval-Human 20 题子集构成",
             "tab_benchmark_subset", figsize=(11, 4.5))


# ============================================================
# 图表 E：实验设置汇总表
# ============================================================
table_e = [
    ["配置项", "零样本 (Zero-shot)", "反馈循环 (Feedback)"],
    ["LLM 模型", "Claude Haiku\n(claude-haiku-4-5-20251001)", "Claude Haiku\n(claude-haiku-4-5-20251001)"],
    ["基准测试", "VerilogEval-Human 子集\n(20 题)", "VerilogEval-Human 子集\n(20 题)"],
    ["每轮候选数 (k)", "1", "3"],
    ["最大迭代轮数", "1 (不迭代)", "5"],
    ["温度 (temperature)", "0.7", "0.7"],
    ["反馈策略", "—", "succinct feedback\n(编译错误前 30 行 /\n仿真输出前 40 行)"],
    ["重试机制", "指数退避，最多 3 次", "指数退避，最多 3 次"],
    ["评价指标", "通过率 (pass rate)\nRank 得分 (匹配率)", "通过率 (pass rate)\nRank 得分 (匹配率)"],
    ["API 错误", "0", "0"],
]
render_table(table_e, [0.25, 0.375, 0.375], "实验设置汇总",
             "tab_experiment_config", figsize=(10, 5.5))


print("\nAll table figures generated.")
