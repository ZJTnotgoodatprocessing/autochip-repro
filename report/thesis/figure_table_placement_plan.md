# 论文图表与制表建议

> 说明：本文件给出具体到章节的图表/表格建议，供用户手工排版 Word 时参考。
> 所有图来源均为项目仓库中的真实文件。

---

## 第 1 章 绪论

本章以文字为主，一般不需要图表。

---

## 第 2 章 相关技术与研究基础

本章以文字为主，一般不需要图表。可选：

| # | 建议图/表 | 类型 | 来源 | 建议标题 | 放入正文? |
|---|----------|------|------|---------|----------|
| 1 | 相关工作对比表 | 三线表 | 手工整理 | 表 2.1 本文与相关工作的对比 | 可选 |

---

## 第 3 章 系统设计与实现

| # | 建议图/表 | 类型 | 来源 | 建议标题 | 放入正文? | 位置 |
|---|----------|------|------|---------|----------|------|
| 1 | 系统总体架构图 | 架构图 | `report/figures/fig_system_architecture.png` | 图 3.1 AutoChip 风格 RTL 生成与反馈修复系统架构 | ✅ 必须 | §3.1 |
| 2 | 反馈循环流程图 | 流程图 | `report/figures/fig_feedback_loop_flow.png` | 图 3.2 反馈循环控制流程 | ✅ 必须 | §3.6 |
| 3 | 核心模块映射表 | 三线表 | 手工整理自 `appendix_plan.md` 附录 C | 表 3.1 系统核心模块与代码文件映射 | ✅ 建议 | §3.1 或 §3.8 |
| 4 | 反馈粒度级别定义表 | 三线表 | 手工整理 | 表 3.2 反馈粒度五级定义（L0–L4） | ✅ 建议 | §3.6.3 |

**注意**：`report/figures/tab_module_mapping.png` 为中期截图式图片，建议改为 Word 三线表。

---

## 第 4 章 实验设计

| # | 建议图/表 | 类型 | 来源 | 建议标题 | 放入正文? | 位置 |
|---|----------|------|------|---------|----------|------|
| 1 | STUDY_12 任务组成表 | 三线表 | `notes/rtllm_study12_definition.md` | 表 4.1 RTLLM_STUDY_12 任务组成 | ✅ 必须 | §4.2.2 |
| 2 | 模型设置表 | 三线表 | `notes/model_switching_usage.md` | 表 4.2 实验模型配置 | ✅ 必须 | §4.3 |
| 3 | 实验条件汇总表 | 三线表 | 手工整理 | 表 4.3 七组实验条件汇总 | ✅ 必须 | §4.4 |
| 4 | 评价指标表 | 三线表 | 手工整理 | 表 4.4 评价指标定义 | ✅ 建议 | §4.5 |

**注意**：`report/figures/tab_benchmark_subset.png` 和 `tab_experiment_config.png` 为中期旧版截图，内容仅含 VerilogEval，建议不使用，改为包含 RTLLM 的新版三线表。

---

## 第 5 章 实验结果与分析

### 5.1 需插入的图（14 张）

| # | 建议图 | 来源文件 | 建议标题 | 位置 |
|---|--------|---------|---------|------|
| 1 | VerilogEval 通过率 | `outputs/reports/haiku_pass_rate_bar.png` | 图 5.1 VerilogEval-Human 零样本与反馈通过率对比 | §5.1 |
| 2 | 三模型通过率 | `outputs/reports/fig_passrate_comparison.png` | 图 5.2 RTLLM_STUDY_12 三模型通过率对比 | §5.2 |
| 3 | 逐题矩阵 | `outputs/reports/fig_per_problem_matrix.png` | 图 5.3 RTLLM_STUDY_12 逐题结果矩阵 | §5.2 |
| 4 | Feedback 增益 | `outputs/reports/fig_feedback_gain.png` | 图 5.4 各模型反馈增益对比 | §5.2 |
| 5 | 消融对比 | `outputs/reports/fig_ablation_comparison.png` | 图 5.5 零样本/重试/反馈三条件对比 | §5.3 |
| 6 | 收益分解 | `outputs/reports/fig_ablation_decomposition.png` | 图 5.6 GPT-5.4 反馈收益来源分解 | §5.3 |
| 7 | 稳定性误差棒 | `outputs/reports/fig_stability_ablation.png` | 图 5.7 稳定性实验三条件均值与标准差 | §5.4 |
| 8 | 稳定性正式 | `outputs/reports/fig_stability_formal.png` | 图 5.8 正式实验重复结果对比 | §5.4 |
| 9 | 粒度曲线 | `outputs/reports/fig_granularity_curve.png` | 图 5.9 反馈粒度通过率曲线（倒 U 型） | §5.5 |
| 10 | 粒度矩阵 | `outputs/reports/fig_granularity_matrix.png` | 图 5.10 反馈粒度逐题结果矩阵 | §5.5 |
| 11 | MT v2 对比 | `outputs/reports/fig_multiturn_comparison_v2.png` | 图 5.11 多轮对话反馈 v2 条件对比 | §5.6 |
| 12 | MT v2 矩阵 | `outputs/reports/fig_multiturn_matrix_v2.png` | 图 5.12 多轮对话反馈 v2 逐题矩阵 | §5.6 |
| 13 | PS 对比 | `outputs/reports/fig_prompt_strategy_comparison.png` | 图 5.13 提示词策略零样本与反馈对比 | §5.7 |
| 14 | PS 矩阵 | `outputs/reports/fig_prompt_strategy_matrix.png` | 图 5.14 提示词策略逐题结果矩阵 | §5.7 |

### 5.2 建议的三线表

| # | 建议表 | 内容来源 | 建议标题 | 位置 |
|---|--------|---------|---------|------|
| 1 | 三模型结果汇总 | Ch5 §5.2 正文数据 | 表 5.1 RTLLM_STUDY_12 三模型通过率汇总 | §5.2 |
| 2 | 消融结果表 | Ch5 §5.3 正文数据 | 表 5.2 消融实验收益分解 | §5.3 |
| 3 | 稳定性统计表 | Ch5 §5.4 正文数据 | 表 5.3 稳定性实验统计汇总 | §5.4 |
| 4 | 粒度结果表 | Ch5 §5.5 正文数据 | 表 5.4 反馈粒度实验通过率 | §5.5 |
| 5 | 策略结果表 | Ch5 §5.7 正文数据 | 表 5.5 提示词策略实验结果 | §5.7 |

### 5.3 废弃图（不可使用）

| 文件 | 原因 |
|------|------|
| `outputs/reports/fig_multiturn_comparison.png` | Multi-turn v1 废弃版 |
| `outputs/reports/fig_multiturn_matrix.png` | Multi-turn v1 废弃版 |

### 5.4 不建议放入正文的图

| 文件 | 原因 |
|------|------|
| `outputs/reports/haiku_per_problem_rank.png` | 信息与 §5.2 重叠，可放附录 |
| `report/figures/fig_project_gantt.png` | 项目管理图，不适合正文 |

---

## 第 6 章 总结与展望

本章以文字为主，一般不需要新图。可选：

| # | 建议图/表 | 类型 | 建议标题 | 放入正文? |
|---|----------|------|---------|----------|
| 1 | 主要结论汇总表 | 三线表 | 表 6.1 主要实验结论汇总 | 可选 |

---

## 三线表格式说明

北航本科论文中表格应采用三线表：
- 只有顶线、栏目线、底线三条横线
- 无竖线
- 表题在表格上方，居中，格式"表 X.Y 标题"
- 图题在图片下方，居中，格式"图 X.Y 标题"
