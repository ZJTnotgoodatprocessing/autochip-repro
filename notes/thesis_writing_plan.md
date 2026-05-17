# 毕业论文写作计划

> 创建日期：2026-05-01
> 论文题目：基于大语言模型与 EDA 工具反馈的 RTL 代码自动生成与自修复研究
> 权威实验索引：`notes/authoritative_experiment_index.md`

---

## 一、论文模板解析

### 1.1 模板文件

- 文件：`北航本科生论文模板.docx`（356KB，位于项目根目录）
- 模板来自北航本科生毕业论文官方模板
- 模板内含一篇完整示例论文（电场/水滴迁移相关），需全部替换为本项目内容

### 1.2 模板包含的主要部分

| # | 部分 | 模板中的位置 | 说明 |
|---|------|-------------|------|
| 1 | 封面 | 页首 | 含学号、姓名、院系、课题名称、指导教师 |
| 2 | 本人声明 | 封面后 | 学术诚信声明，签字页 |
| 3 | 中文摘要 | 声明后 | 含关键词 |
| 4 | 英文摘要 (Abstract) | 中文摘要后 | 含 Key words |
| 5 | 目录 | 摘要后 | 自动生成，含章节及页码 |
| 6 | 正文各章 | 目录后 | 示例为 3 章正文 + 各级小节 |
| 7 | 结论 | 正文后 | 独立章节 |
| 8 | 致谢 | 结论后 | 感谢语 |
| 9 | 参考文献 | 致谢后 | 含期刊、会议、学位论文、报纸等格式示例 |
| 10 | 附录 | 参考文献后 | 示例含附录 A（图）、B（表）、C（代码） |

### 1.3 模板格式要点

- 标题使用 Word 内建 Heading 1 / Heading 2 等样式
- 图表编号格式：`图X.Y`、`表X.Y`
- 参考文献使用上角标 `[1]` 格式
- 正文字体/字号需按模板保持（模板已预设）
- 附录按 A/B/C 编排

---

## 二、论文总章节结构

### 第 1 章 绪论
- 1.1 研究背景与意义
- 1.2 LLM 在 RTL/Verilog 生成中的研究现状
- 1.3 EDA 工具反馈在代码生成中的研究价值
- 1.4 本文主要工作与贡献
- 1.5 论文组织结构

### 第 2 章 相关技术与研究基础
- 2.1 Verilog 与 RTL 设计基础
- 2.2 大语言模型代码生成机制
- 2.3 EDA 编译与仿真验证流程
  - 2.3.1 Icarus Verilog 编译器
  - 2.3.2 VVP 仿真引擎
- 2.4 AutoChip 方法介绍
- 2.5 RTL 生成评估基准
  - 2.5.1 VerilogEval benchmark
  - 2.5.2 RTLLM benchmark
- 2.6 本文与已有工作的关系

### 第 3 章 系统设计与实现
- 3.1 系统总体架构
- 3.2 任务加载与 benchmark 接入
  - 3.2.1 VerilogEval 加载器
  - 3.2.2 RTLLM 加载器
- 3.3 LLM 调用与模型管理
- 3.4 Verilog 提取、编译与仿真执行
  - 3.4.1 代码提取
  - 3.4.2 编译验证
  - 3.4.3 仿真执行与结果解析
- 3.5 评分机制
- 3.6 反馈循环控制
  - 3.6.1 单轮反馈（Single-turn Feedback Loop）
  - 3.6.2 Retry-only 模式
  - 3.6.3 反馈粒度控制
  - 3.6.4 多轮对话反馈（Multi-turn Feedback）
- 3.7 提示词策略模块
- 3.8 实验结果管理与审计机制

### 第 4 章 实验设计
- 4.1 实验总体目标
- 4.2 Benchmark 与任务子集
  - 4.2.1 VerilogEval-Human 20 题子集
  - 4.2.2 RTLLM STUDY_12 子集
- 4.3 模型设置
- 4.4 实验条件定义
  - 4.4.1 Zero-shot / Retry-only / Feedback 三条件
  - 4.4.2 稳定性重复实验设置
  - 4.4.3 反馈粒度五级设置（L0–L4）
  - 4.4.4 多轮对话反馈四条件
  - 4.4.5 Prompt Strategy 四策略
- 4.5 评价指标与统计方法

### 第 5 章 实验结果与分析
- 5.1 VerilogEval-Human 中期基线实验
- 5.2 RTLLM STUDY_12 正式实验矩阵
- 5.3 反馈价值消融实验
- 5.4 稳定性重复实验
- 5.5 反馈粒度实验
- 5.6 多轮对话反馈实验
- 5.7 提示词策略实验
- 5.8 典型案例分析
- 5.9 综合讨论
  - 5.9.1 反馈机制的有效性
  - 5.9.2 模型依赖性
  - 5.9.3 框架局限与天花板题

### 第 6 章 总结与展望
- 6.1 本文工作总结
- 6.2 主要实验结论
- 6.3 系统局限性讨论
- 6.4 后续工作展望

### 致谢

### 参考文献

### 附录
- 附录 A：RTLLM STUDY_12 完整逐题结果矩阵
- 附录 B：核心代码片段（feedback loop 核心逻辑）
- 附录 C：典型修复过程示例

---

## 三、论文材料映射表

> 所有实验数据引用以 `notes/authoritative_experiment_index.md` 为唯一入口。
> ⚠️ Multi-turn v1 (`9760eb4`) 不可引用。

### 3.1 正文章节 → 数据源映射

| 论文章节 | 主要内容 | 数据/图表来源 | 对应 notes | 对应 outputs | 注意事项 |
|---------|---------|-------------|-----------|-------------|---------|
| §1 绪论 | 研究背景与动机 | 文献综述 | — | — | 需查阅 AutoChip/RTLLM 原始论文 |
| §2 相关技术 | 技术基础介绍 | 文献 + 系统描述 | — | — | 引用 VerilogEval/RTLLM 论文 |
| §3.1 系统架构 | 架构图 | `fig_system_architecture.png` | — | `report/figures/` | 中期已有，可直接使用 |
| §3.6 反馈循环 | 流程图 | `fig_feedback_loop_flow.png` | — | `report/figures/` | 中期已有，可直接使用 |
| §4.2 Benchmark | 任务子集定义 | — | `rtllm_study12_definition.md` | — | — |
| §5.1 VerilogEval 基线 | Haiku ZS/FB | `haiku_pass_rate_bar.png` | `haiku_main_experiment_summary.md` | `verilogeval_both_20260412_173450.json` | 中期基线，低谨慎 |
| §5.2 RTLLM 正式实验 | 三模型 ZS/FB | `fig_passrate_comparison.png`, `fig_per_problem_matrix.png`, `fig_feedback_gain.png` | `rtllm_formal_experiment_summary.md` | `rtllm_both_*` (3 runs) | **论文核心数据**，低谨慎 |
| §5.3 消融实验 | ZS/RO/FB 分解 | `fig_ablation_comparison.png`, `fig_ablation_decomposition.png` | `rtllm_feedback_ablation_summary.md` | `rtllm_ablation_20260422_*` | 低谨慎 |
| §5.4 稳定性实验 | 4轮重复统计 | `fig_stability_ablation.png`, `fig_stability_formal.png` | `rtllm_stability_summary.md` | 8 runs ablation_* | 低谨慎 |
| §5.5 粒度实验 | L0–L4 曲线 | `fig_granularity_curve.png`, `fig_granularity_matrix.png` | `rtllm_feedback_granularity_summary.md` | `rtllm_granularity_*` (2 runs) | 中谨慎：样本有限 |
| §5.6 多轮对话 | 4 条件对比 | `fig_multiturn_comparison_v2.png`, `fig_multiturn_matrix_v2.png` | `rtllm_multiturn_feedback_summary.md` | `rtllm_multiturn_20260424_*` (2 runs) | ⚠️ 中谨慎：6 题小子集；**必须用 v2 图表** |
| §5.7 Prompt Strategy | 4 策略对比 | `fig_prompt_strategy_comparison.png`, `fig_prompt_strategy_matrix.png` | `rtllm_prompt_strategy_summary.md` | `rtllm_prompt_strategy_20260425_*` | 低谨慎 |
| §5.8 案例分析 | 修复过程 | `fig_case_study_repair.png` | `rtllm_case_studies.md` | details.json 中的迭代记录 | — |
| §6 总结展望 | 结论 + 未来工作 | — | `research_improvement_backlog.md` | — | 引用 C1–C11 结论 |

### 3.2 结论可引用性

| 结论编号 | 结论内容 | 谨慎级别 | 引用要求 |
|---------|---------|---------|---------|
| C1 | Haiku FB +10pp (VerilogEval) | 低 | 可直接写 |
| C2 | 三模型 FB 增益，GPT +33pp | 低 | 可直接写 |
| C3 | GPT FB 79.2%±4.2% 稳定 | 低 | 可直接写 |
| C4 | FB ~57% 来自反馈，43% 重采样 | 低 | 可直接写 |
| C5 | sequence_detector/traffic_light 仅 FB 可解 | 低 | 可直接写 |
| C6 | 粒度倒 U 型 | 中 | 需注明"在 STUDY_12 和两模型上观察到" |
| C7 | Rich 信息过载 | 中 | 需注明样本有限 |
| C8 | Sonnet FB < RO | 中 | 需谨慎表述"在本实验设置下" |
| C9 | MT +17pp | 中 | 需注明 6 题子集、单次运行 |
| C10 | k=3 对 Sonnet 有害 | 中 | 需注明小样本 |
| C11 | 粒度局限 | 中 | 同 C6 |
| — | Fewshot ZS +9pp, FB 拉平至 92% | 低 | 可直接写 |
| — | CoT 轻微有害 (−8pp ZS) | 低 | 可直接写，注明单次运行 |
| ❌ | MT v1 任何结论 | — | **不可引用** |

---

## 四、论文可用图表清单

### 4.1 `outputs/reports/` 目录（后中期实验图表）

| # | 文件名 | 主题 | 适合章节 | 状态 | 数据来源 | 备注 |
|---|--------|------|---------|------|---------|------|
| 1 | `fig_passrate_comparison.png` | 三模型 ZS/FB 通过率对比 | §5.2 | ✅ 可直接使用 | 正式实验 | **核心图** |
| 2 | `fig_per_problem_matrix.png` | 逐题×模型 PASS/FAIL 矩阵 | §5.2 | ✅ 可直接使用 | 正式实验 | |
| 3 | `fig_feedback_gain.png` | Feedback 增益柱状图 | §5.2 | ✅ 可直接使用 | 正式实验 | |
| 4 | `fig_ablation_comparison.png` | ZS/RO/FB 三条件对比 | §5.3 | ✅ 可直接使用 | 消融实验 | |
| 5 | `fig_ablation_decomposition.png` | 收益分解（重采样 vs 反馈） | §5.3 | ✅ 可直接使用 | 消融实验 | **论文亮点图** |
| 6 | `fig_stability_ablation.png` | 稳定性：两模型×三条件误差棒 | §5.4 | ✅ 可直接使用 | 稳定性实验 | |
| 7 | `fig_stability_formal.png` | 稳定性：ZS vs FB + 逐轮数据 | §5.4 | ✅ 可直接使用 | 稳定性实验 | |
| 8 | `fig_granularity_curve.png` | L0–L4 粒度折线图 | §5.5 | ✅ 可直接使用 | 粒度实验 | **倒 U 型核心图** |
| 9 | `fig_granularity_matrix.png` | 粒度逐题热力图 | §5.5 | ✅ 可直接使用 | 粒度实验 | |
| 10 | `fig_multiturn_comparison_v2.png` | MT 4 条件对比（v2 修正版） | §5.6 | ✅ 可直接使用 | MT v2 实验 | **必须用 v2** |
| 11 | `fig_multiturn_matrix_v2.png` | MT 逐题矩阵（v2） | §5.6 | ✅ 可直接使用 | MT v2 实验 | |
| 12 | `fig_prompt_strategy_comparison.png` | 4 策略 ZS/FB 对比 | §5.7 | ✅ 可直接使用 | PS 实验 | |
| 13 | `fig_prompt_strategy_matrix.png` | 策略逐题矩阵 | §5.7 | ✅ 可直接使用 | PS 实验 | |
| 14 | `haiku_pass_rate_bar.png` | Haiku VerilogEval 通过率 | §5.1 | ✅ 可直接使用 | 中期基线 | |
| 15 | `haiku_per_problem_rank.png` | Haiku 逐题 rank | §5.1 | ⚠️ 仅供参考 | 中期基线 | 信息与 §5.2 重叠 |
| 16 | `fig_multiturn_comparison.png` | MT 对比（v1 废弃版） | — | ❌ 不可使用 | MT v1 (superseded) | 已被 v2 替代 |
| 17 | `fig_multiturn_matrix.png` | MT 矩阵（v1 废弃版） | — | ❌ 不可使用 | MT v1 (superseded) | 已被 v2 替代 |

### 4.2 `report/figures/` 目录（中期报告资产）

| # | 文件名 | 主题 | 适合章节 | 状态 | 备注 |
|---|--------|------|---------|------|------|
| 1 | `fig_system_architecture.png` | 系统总体架构图 | §3.1 | ✅ 可直接使用 | 中期已有 |
| 2 | `fig_feedback_loop_flow.png` | 反馈循环流程图 | §3.6 | ✅ 可直接使用 | 中期已有 |
| 3 | `fig_case_study_repair.png` | 典型修复过程 | §5.8 | ✅ 可直接使用 | 中期已有 |
| 4 | `fig_project_gantt.png` | 项目甘特图 | 不建议放正文 | ⚠️ 仅供参考 | 中期汇报用 |
| 5 | `tab_benchmark_subset.png` | Benchmark 子集表 | §4.2 | ⚠️ 需更新 | 仅含 VerilogEval，缺 RTLLM |
| 6 | `tab_experiment_config.png` | 实验配置表 | §4.4 | ⚠️ 需更新 | 仅含早期设置 |
| 7 | `tab_module_mapping.png` | 模块映射表 | §3 | ⚠️ 需确认是否过时 | 中期版本 |

### 4.3 图表总结

- **可直接使用**：15 张（含 2 张 v2 multi-turn）
- **需要更新/重绘**：2-3 张（中期表格类图需更新以涵盖 RTLLM）
- **不可使用**：2 张（v1 multi-turn 废弃图）
- **仅供参考**：2 张（甘特图、haiku_per_problem_rank）

### 4.4 论文需新建的图表

| 需求 | 建议内容 | 来源 |
|------|---------|------|
| §3.1 系统架构补充 | 可能需要增加 RTLLM 接入路径 | 基于现有架构图扩展 |
| §4.2 STUDY_12 子集定义 | 12 题名称/类别/难度表 | `rtllm_study12_definition.md` |
| §5.9 综合对比 | 所有实验结论汇总表 | `authoritative_experiment_index.md` §四 |

---

## 五、推荐写作顺序

### 推荐顺序及理由

| 优先级 | 章节 | 理由 |
|--------|------|------|
| **1** | **第 3 章：系统设计与实现** | 系统已完全实现且稳定，代码即素材，无需等待其他输入。写完后可作为实验章节的方法基础。 |
| **2** | **第 4 章：实验设计** | 所有实验已完成，设计方案已固定。写实验设计时可以参考 3 章的系统描述，确保一致性。 |
| **3** | **第 5 章：实验结果与分析** | 数据已全部就绪，图表已生成。这是论文最重要的章节，需要最多时间打磨。先写 3/4 章后，5 章可引用前文的术语和方法定义。 |
| **4** | **第 2 章：相关技术** | 需要文献调研，但范围已基本确定。在写完 3-5 章后，可以更精准地确定需要覆盖哪些背景知识。 |
| **5** | **第 1 章：绪论** | 绪论需要全局视角——知道全文写了什么才能写好"本文主要工作与贡献"。放最后写。 |
| **6** | **第 6 章：总结与展望** | 依赖 5 章的完整分析。未来工作方向已在 `research_improvement_backlog.md` 中规划好。 |
| **7** | **摘要** | 全文完成后再提炼，确保摘要准确反映论文内容。 |
| **8** | **致谢** | 最后写，个人表达。 |

### 为什么不从第 1 章开始？

1. **绪论需要全局概览**：只有写完 3-5 章，才能准确描述"本文做了什么"和"主要贡献"
2. **实验章节是论文核心**：本科毕设论文最重要的是实验数据和分析，先把核心写扎实
3. **系统设计最容易下手**：代码已经写好，直接按模块描述即可，是最佳起步点
4. **避免反复修改**：如果先写绪论，后续实验分析可能推翻某些预设表述，造成返工

---

## 六、写作进度跟踪

| 章节 | 状态 | 预计页数 | 开始日期 | 完成日期 |
|------|------|---------|---------|---------|
| 第 3 章 系统设计 | ✅ 初稿已完成 | 8-10 页 | 2026-05-01 | 2026-05-01 | 草稿：`report/thesis/chapter3_system_design.md` |
| 第 4 章 实验设计 | ✅ 初稿已完成 | 5-7 页 | 2026-05-01 | 2026-05-01 | 草稿：`report/thesis/chapter4_experiment_design.md` |
| 第 5 章 实验结果 | ✅ 初稿已完成 | 12-15 页 | 2026-05-02 | 2026-05-02 | 草稿：`report/thesis/chapter5_results_analysis.md` |
| 第 2 章 相关技术 | ✅ 初稿已完成 | 6-8 页 | 2026-05-02 | 2026-05-02 | 草稿：`report/thesis/chapter2_related_work.md` |
| 第 1 章 绪论 | ✅ 初稿已完成 | 4-5 页 | 2026-05-02 | 2026-05-02 | 草稿：`report/thesis/chapter1_introduction.md` |
| 第 6 章 总结展望 | ✅ 初稿已完成 | 2-3 页 | 2026-05-02 | 2026-05-02 | 草稿：`report/thesis/chapter6_conclusion.md` |
| 中文摘要 | ✅ 初稿已完成 | 1 页 | 2026-05-02 | 2026-05-02 | 草稿：`report/thesis/abstract_zh.md` |
| 英文摘要 | ✅ 初稿已完成 | 1 页 | 2026-05-02 | 2026-05-02 | 草稿：`report/thesis/abstract_en.md` |
| 致谢 | ✅ 初稿已完成 | 1 页 | 2026-05-02 | 2026-05-02 | 草稿：`report/thesis/acknowledgements.md` |
| 参考文献 | ✅ 初稿已完成 | 2-3 页 | 2026-05-02 | 2026-05-02 | 草稿：`report/thesis/references.md` |
| 附录 | ✅ 规划已完成 | 3-5 页 | 2026-05-02 | 2026-05-02 | 草稿：`report/thesis/appendix_plan.md` |
| 完整 Word 初稿 | ✅ 内容整合版 v1 | — | 2026-05-02 | 2026-05-02 | `report/thesis/thesis_draft_v1.docx`（格式待人工处理） |
| 人工排版指导包 | ✅ 已完成 | — | 2026-05-05 | 2026-05-05 | `report/thesis/thesis_manual_formatting_guide.md` |
| 图表与制表建议 | ✅ 已完成 | — | 2026-05-05 | 2026-05-05 | `report/thesis/figure_table_placement_plan.md` |
| 参考文献核验版 | ✅ 初稿已完成 | — | 2026-05-05 | 2026-05-05 | `report/thesis/references_verified.md`（17 条已核验） |
| 正文引用位置计划 | ✅ 初稿已完成 | — | 2026-05-05 | 2026-05-05 | `report/thesis/citation_insertion_plan.md` |
| 全文内容审阅报告 | ✅ 已完成 | — | 2026-05-05 | 2026-05-05 | `report/thesis/thesis_content_review_report.md` |
| LaTeX 论文工程 | ✅ 已编译生成 PDF（59页） | — | 2026-05-06 | 2026-05-06 | `report/thesis/latex/thesis_draft_latex_v1.pdf` |
| LaTeX 迁移记录 | ✅ 已完成 | — | 2026-05-06 | 2026-05-06 | `report/thesis/latex_migration_notes.md` |
| LaTeX PDF v2（题目修正+格式检查） | ✅ 已生成（59页） | — | 2026-05-07 | 2026-05-07 | `report/thesis/latex/thesis_draft_latex_v2.pdf` |
| LaTeX 格式审查报告 | ✅ 已完成 | — | 2026-05-07 | 2026-05-07 | `report/thesis/latex_format_check_report.md` |
| LaTeX PDF v3（结构优化+全文润色） | ✅ 已生成（54页） | — | 2026-05-07 | 2026-05-07 | `report/thesis/latex/thesis_draft_latex_v3.pdf` |
| v3 润色报告 | ✅ 已完成 | — | 2026-05-07 | 2026-05-07 | `report/thesis/latex_polish_v3_report.md` |
| LaTeX PDF v4（定稿前专项小修） | ✅ 已生成（54页） | — | 2026-05-08 | 2026-05-08 | `report/thesis/latex/thesis_draft_latex_v4.pdf` |
| v4 核查报告 | ✅ 已完成 | — | 2026-05-08 | 2026-05-08 | `report/thesis/latex_v4_final_check_report.md` |
| LaTeX 最终候选版 | ✅ 已生成（54页） | — | 2026-05-08 | 2026-05-08 | `report/thesis/latex/thesis_final_candidate.pdf` |
| 最终候选检查报告 | ✅ 已完成 | — | 2026-05-08 | 2026-05-08 | `report/thesis/final_candidate_check_report.md` |
| 知网+导师意见修订 v5 | ✅ 已生成（57页） | — | 2026-05-08 | 2026-05-08 | `report/thesis/latex/thesis_revised_after_cnki_v5.pdf` |
| v5 修订报告 | ✅ 已完成 | — | 2026-05-08 | 2026-05-08 | `report/thesis/cnki_and_supervisor_revision_v5_report.md` |
| **总计** | — | **57 页** | — | — |
| 工作量表述轻量修订 v6-lite | ✅ 已生成（57页） | — | 2026-05-09 | 2026-05-09 | `report/thesis/latex/thesis_workload_revised_v6_lite.pdf` |
| 导师意见修订 v7 | ✅ 已生成（58页） | — | 2026-05-11 | 2026-05-11 | `report/thesis/latex/thesis_supervisor_revision_v7.pdf` |
| 导师意见修订 v8 | ✅ 已生成（59页） | — | 2026-05-13 | 2026-05-13 | `report/thesis/latex/thesis_supervisor_revision_v8.pdf` |
| 导师意见精修 v9 | ✅ 已生成（58页） | — | 2026-05-13 | 2026-05-13 | `report/thesis/latex/thesis_supervisor_revision_v9.pdf` |
| AutoChip定位表述修订 | ✅ 已完成 | — | 2026-05-14 | 2026-05-14 | 将AutoChip重新定位为最接近相关工作和对比对象，消除"单纯复现"观感；覆盖 `report/thesis/latex/thesis_supervisor_revision_v9.pdf`；详见 `report/thesis/autochip_positioning_fix_report.md` |
| 导师意见修订 v10 | ✅ 已生成（63页） | — | 2026-05-14 | 2026-05-14 | 增强第3章技术内容与图示，显式对齐第4章实验设计和第5章实验结果；新增 3 张中文技术图、1 张设计-结果对应表、4 处过渡句 + §5.10 小结回扣；独立 PDF：`report/thesis/latex/thesis_supervisor_revision_v10_ch3_ch4ch5.pdf`；v9 PDF 保留为 AutoChip 定位修订后的 58 页快照，**未被本轮覆盖**；详见 `report/thesis/supervisor_revision_v10_ch3_ch4ch5_report.md` |

> **正式论文题目**：基于EDA工具反馈的LLM Verilog生成与自动优化
>
> **下一步建议**：v10 可发给导师。送审 PDF 为 `thesis_supervisor_revision_v10_ch3_ch4ch5.pdf`（63 页）；`thesis_supervisor_revision_v9.pdf` 保留为 v9 + AutoChip 定位修订的历史快照（58 页）。本轮按导师意见扩充第 3 章技术内容（+3 张技术图 + 约 760 字正文）并显式对齐第 4 章实验设计与第 5 章结果章节（设计-结果对应表 + 三层过渡 + 小结回扣），实验数据、AutoChip 定位、致谢、参考文献全部保持不变。

---

## 七、关键写作约束

1. **所有实验数据必须可追溯**：每个数字都应能在 `authoritative_experiment_index.md` 中找到对应的 run 目录和 summary.json
2. **不可引用 Multi-turn v1**：任何引用 `9760eb4` 数据的段落都是错误的。仅可作为"工程审计案例"提及
3. **谨慎结论需标注局限**：C6–C11 结论需在正文中注明实验规模限制
4. **图表一致性**：同一论文中的图表风格应统一（配色、字体、坐标轴格式）
5. **术语一致性**：全文应统一使用"反馈循环"（feedback loop）、"零样本"（zero-shot）、"重试"（retry-only）等术语
6. **不虚构数据**：如果某个实验方向未实施，只能在"展望"中提及，不能写成已完成

---

## 八、v12 状态（2026-05-16，导师 v11 反馈后）

> **送审 PDF**：`report/thesis/latex/thesis_supervisor_revision_v12.pdf` 63 页 0.94 MB
> **基线**：v11 (`086fcd2`)
> **修订报告**：`report/thesis/supervisor_revision_v12_report.md`

导师对 v11 的 6 条意见全部落实：

1. 图表风格：全部数据图（13 张）+ 流程图（图 3.1/3.2）删除图内英文 banner，
   增加 PDF 矢量输出，`\includegraphics` 切换 `.pdf` 引用；PDF 体积 2.21 MB → 0.94 MB
2. "24 项自动化检查" → "4 项自动化检查"（chapter 3 §3.7 + chapter 4 §4.6）
3. 表 4.3 删除"难度"星级列，改为"设计特征与选入理由"
4. 图 5.6 顶部英文 `Feedback Granularity Curve / RTLLM STUDY_12 ...` 标题已清除
5. 第 5.8 / 5.9 段首加粗格式统一改为 `\subsubsection*{}`（不入目录）
6. 编译：xelatex 两次稳定通过，0 undefined ref/cite、0 BibTeX warning

**实验数据零修改**。v9 / v10 / v11 / v12 历史 PDF 全部保留。

---

## 九、v13 状态（2026-05-16，第 3 章流程图重绘）

> **送审 PDF**：`report/thesis/latex/thesis_supervisor_revision_v13_figures.pdf` 64 页 0.95 MB
> **基线**：v12 (`b36b081`)
> **修订报告**：`report/thesis/supervisor_revision_v13_figures_report.md`

承接 v12 自检中"流程图本体仍带 AI 生成感"的遗留：

1. 第 3 章 5 张系统设计图（图 3.1–3.5）整体重绘为正式论文黑白线框风格：
   - 直角矩形（`Rectangle`，非 `FancyBboxPatch`）；
   - 白底，统一近黑边框 `#1A1A1A`；
   - 单一深蓝 `#1F3A5F` 强调色，仅用于决策菱形和反馈虚线；
   - 移除多色卡片、Start/End 圆点、彩色斜体等装饰；
   - 输出 PDF 矢量，`chapter3.tex` 5 处 `\includegraphics` 切到 `_v13.pdf`；
   - 图 3.1 caption 同步去掉旧版彩色配色描述。
2. §3.7 文本删去"共 24 个独立断言"细节，仅保留"4 项核心检查"，
   `grep "24 项|24 个独立断言"` 在 LaTeX 正文 0 命中。

**生成脚本**：`scripts/generate_thesis_ch3_figures_v13.py`（可重复运行）
**实验数据零修改**。v7 / v8 / v9 / v10 / v11 / v12 / v13 历史 PDF 全部保留。

---

## 十、v14 状态（2026-05-17，第 3 章图尺寸 + 正文加强）

> **送审 PDF**：`report/thesis/latex/thesis_supervisor_revision_v14_ch3_refine.pdf` 65 页 1.02 MB
> **基线**：v13
> **修订报告**：`report/thesis/supervisor_revision_v14_ch3_refine_report.md`

针对导师对 v13 的两条意见：

1. **5 张图缩小**：图 3.1 / 3.3 / 3.4 / 3.5 的 matplotlib `figsize` 与 LaTeX
   `\includegraphics width` 联合缩放，使图加上 caption 后均不再独占整页
   （v13 中图 3.4 独占 p.29）。PyMuPDF 自检显示 v14 中 figure-only pages = 0。
   缩放原则：缩放比保持在 0.6–0.7（视觉字号 ≥ 6pt，A4 打印可读）。
   图 3.2 形状较扁本就不独占页面，未动。
   图 3.5 中 L3 / L4 标签紧凑化（去掉 `+` 旁空格）以避免溢出框。
2. **正文加强**：
   - §3.1 新增技术难点本质段（~280 字）+ 表 3.2（5 行难点—表现—思路对照）；
   - §3.2 新增"闭环 vs zero-shot"段（~180 字）引出框架复用性；
   - §3.3–§3.6 各新增一段设计取舍（~180–230 字）：加载器层封装、提取流程
     解耦、rank 标量 vs pass/fail、反馈粒度可切换 vs 固定；
   - §3.8 本章小结改写为两段：难点→方案回扣 + 本章在论文结构中的位置 +
     主动说明本科毕设范围内贡献的边界。

**实验数据零修改**。v7 / v8 / v9 / v10 / v11 / v12 / v13 / v14 历史 PDF
全部保留。第 4、5、6 章正文未触。

---

## 十一、v14a 状态（2026-05-17，第 3 章图微调 + v14 自查）

> **送审 PDF**：`report/thesis/latex/thesis_supervisor_revision_v14a_ch3_figrefine.pdf` 66 页 0.97 MB
> **基线**：v14 (`140c5c0`)
> **修订报告**：`report/thesis/supervisor_revision_v14a_ch3_figrefine_report.md`

针对导师对 v14 中三张图的细节反馈：

1. **图 3.2**：删除右侧蓝色斜体 _label（"加载器屏蔽数据来源差异 /
   下游模块仅依赖该接口"）。删除后整图布局对称，且该内容已在 §3.3
   正文中完整覆盖（第 76 行 + 第 80 行）。
2. **图 3.3**：iverilog 方框宽度从 4.0 axes unit 加宽到 6.0 axes unit
   （+50%），中心保持 x=4.5 与上方对齐；删除底部灰色斜体 _label
   （"该提取流程兼容 Base / CoT / Few-shot / Few-shot+CoT 四种提示
   策略"）。该内容已在 §3.4 正文 line 99 末尾覆盖。
3. **图 3.4**：把 `构造反馈 Prompt（附编译/仿真信息）` 方框拆为两行
   （"构造反馈 Prompt" + "（附编译 / 仿真信息）"），方框高度从
   bh=0.85 增到 fb_h=1.3，同步调整上下箭头端点匹配新箱体边界。

并对 v14 主任务完成质量做了逐条自查：图尺寸优化（4 张图均缩小，0 个
图独占页面）、§3.1 难点段 + 表 3.2、§3.2 闭环 vs zero-shot、§3.3–§3.6
设计取舍段（4 节均覆盖）、§3.8 难点→方案回扣（含贡献边界声明）。
五项要求均已完成且质量符合预期，详见 `supervisor_revision_v14a_ch3_figrefine_report.md`。

**实验数据零修改**。v7 / v8 / v9 / v10 / v11 / v12 / v13 / v14 / v14a
历史 PDF 全部保留。第 4、5、6 章正文未触。

---

## 十二、v14b 状态（2026-05-17，进一步缩小图 3.3 / 图 3.5）

> **送审 PDF**：`report/thesis/latex/thesis_supervisor_revision_v14b_ch3_figshrink.pdf` 64 页 0.97 MB
> **基线**：v14a (`92a01df`)
> **修订报告**：`report/thesis/supervisor_revision_v14b_ch3_figshrink_report.md`

导师在 v14a PDF 上仍然观察到图 3.3 和图 3.5 占满一整页。复核确认：
v14a 中三张图独占页面（Fig 3.1 在 p23 / Fig 3.3 在 p26 / Fig 3.5 在
p31），用户只点名 3.3 和 3.5。本轮把这两张的 LaTeX width 进一步收紧：

- Fig 3.3：`width=0.65\textwidth` → `width=0.55\textwidth`
- Fig 3.5：`width=0.85\textwidth` → `width=0.70\textwidth`

**关键技术决定**：figsize 维持不变（v14a 的 (6.0, 7.0) / (8.5, 6.95)），
仅靠 LaTeX width 控制纸面尺寸。最初尝试同时缩 figsize 和 width，但
matplotlib 的 fontsize 是 pt 绝对单位、box 宽高是 axes 单位（相对
figsize），缩 figsize 会让文字相对 box 变大、撑爆边界——Fig 3.3 的
monospace 代码与右侧标注重叠，Fig 3.5 的 L2/L3/L4 三联文字互压。维持
figsize 后，box 与 fontsize 同步缩放，纸面字号偏小但内容不溢出。

修复后：v14b 64 页（v14a 66 页，−2 页）；Fig 3.3 现在 p26 chars=886、
Fig 3.5 现在 p30 chars=924，均与正文段落同页，不再独占。Fig 3.1 仍在
p23 独占（chars=414），用户未要求修改，本轮保留。

并新增了一个图独占检测脚本 `scripts/check_v14a_figures.py`，按
caption "图3.x" 直接定位每张图的所在页和该页字符数（取代之前 200 字
阈值的近似检测，那个阈值漏判了 414/364/299 三种"中等密度但仍以图为主"
的页面）。

**实验数据零修改**。v7 / v8 / v9 / v10 / v11 / v12 / v13 / v14 / v14a
/ v14b 历史 PDF 全部保留。第 4、5、6 章正文未触。第 3 章只动了 2 个
includegraphics 的 width 数字（0.65→0.55、0.85→0.70），正文段落
完全未变。
