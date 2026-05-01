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
| 第 1 章 绪论 | 待开始 | 4-5 页 | — | — |
| 第 6 章 总结展望 | 待开始 | 2-3 页 | — | — |
| 中文摘要 | 待开始 | 1 页 | — | — |
| 英文摘要 | 待开始 | 1 页 | — | — |
| 致谢 | 待开始 | 1 页 | — | — |
| 参考文献 | 待开始 | 2-3 页 | — | — |
| 附录 | 待开始 | 3-5 页 | — | — |
| **总计** | — | **~45-58 页** | — | — |

---

## 七、关键写作约束

1. **所有实验数据必须可追溯**：每个数字都应能在 `authoritative_experiment_index.md` 中找到对应的 run 目录和 summary.json
2. **不可引用 Multi-turn v1**：任何引用 `9760eb4` 数据的段落都是错误的。仅可作为"工程审计案例"提及
3. **谨慎结论需标注局限**：C6–C11 结论需在正文中注明实验规模限制
4. **图表一致性**：同一论文中的图表风格应统一（配色、字体、坐标轴格式）
5. **术语一致性**：全文应统一使用"反馈循环"（feedback loop）、"零样本"（zero-shot）、"重试"（retry-only）等术语
6. **不虚构数据**：如果某个实验方向未实施，只能在"展望"中提及，不能写成已完成
