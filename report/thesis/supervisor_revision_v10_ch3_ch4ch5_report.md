# 导师意见修订 v10 报告：第 3 章扩充 + 第 4/5 章对齐

> 日期：2026-05-14
> 关联 PDF：
> - `report/thesis/latex/thesis_supervisor_revision_v9.pdf`（保留为 AutoChip 定位修订后的 58 页快照，本轮未覆盖）
> - `report/thesis/latex/thesis_supervisor_revision_v10_ch3_ch4ch5.pdf`（本轮生成的 v10 独立 PDF，63 页）
>
> 上一版基线：HEAD `a077172`（v9 + AutoChip 定位修订）

---

## 一、本轮导师意见

1. 第 3 章感觉还是偏短，建议把第 3 章再丰富一点儿，增加一些技术内容，增加两到三个图。图的形式要恰当，尽量美观。
2. 第 4 章和第 5 章一定要"对齐"，即第 4 章写的实验、层层递进的设计，第 5 章的结果一定要跟它一一对应。

## 二、GitHub 同步状态

| 项 | 值 |
|---|---|
| 本地 HEAD（修改前） | `a077172b45cd1931b67384976943a28214b5b1a8` |
| 远程 main（修改前） | `a077172b45cd1931b67384976943a28214b5b1a8` |
| 同步状态 | ✅ 完全一致，AutoChip 定位修订已包含在远程 |
| 上轮 push 一致性 | 已确认（`git ls-remote origin main` 返回 `a077172`，与本地 HEAD 完全相同；外部检查若仍显示 `f92389d` 是 GitHub UI 缓存延迟） |

预期的远程提交链路（按时间倒序）：

```text
a077172  thesis v9: reposition AutoChip as most-close related work, not reproduction target
f92389d  appendix: split figures into Appendix B to match ch5 cross-references
9804897  assign: remove 'AutoChip reproduction' framing from task book work item 1
3bcdbee  thesis v9: Sonnet failure analysis, cost-benefit, AIGC reduction, figure fixes (58p)
```

✅ 全部出现在 `git log --oneline -n 8` 的输出中。

## 三、第 3 章新增了哪些技术内容

修改文件：`report/thesis/latex/data/chapter3.tex`

### §3.3 多源 benchmark 的统一接入

新增一段（约 200 字）说明 VerilogEval 与 RTLLM 在表层数据格式上的差异：

- VerilogEval-Human 的描述文本与 TopModule 接口分开存储、参考实现需与测试平台合并
- RTLLM 2.0 将描述放在 `design_description.txt`，测试平台直接以 `testbench.v` 提供

并解释了如果不做归一化，提示词构建器、执行器、评分器都需要分别处理两套数据来源；统一 Task 接口将所有差异收敛到加载器一层，下游模块仅依赖四个字段，正是后续支持多 benchmark 交叉实验的工程基础。

末尾追加一句关于第 4 章七组实验、两个 benchmark 交叉对比时仅需切换命令行参数的工程效果。

### §3.4 代码生成与提取

新增一段（约 270 字）说明 LLM 原始回复中常见的非代码内容：

- 开场客套语、CoT 推理段（包裹在 `<reasoning>` 标签或自由形式段落中）
- Markdown 围栏与语言标签
- 结尾解释文本

解释了直接送入 `iverilog` 会因非 Verilog 语法而失败；阐述了两阶段提取的设计动机是分离"回复结构"与"代码内容"，两阶段彼此独立、便于扩展；并明确该统一提取流程兼容 Base / CoT / Few-shot / Few-shot+CoT 四种提示策略，这一点直接支持了第 5 章 §5.7 提示词策略实验的实验合理性。

### §3.6 反馈构造与迭代修复控制

新增一段（约 290 字）解释反馈信息的具体构造逻辑由评分结果驱动。说明了从 EDA 验证结果到下一轮反馈提示词的完整决策路径：

1. 编译器和仿真器的输出被评分器映射为 $[-2.0, 1.0]$ 区间内的标量分数
2. 控制器根据 rank 是否等于 1.0 判断当前是否已通过
3. 若已通过则直接返回 `global_best`；否则将 rank 和原始 EDA 输出共同交给反馈构造器
4. 反馈构造器按照配置的粒度模式生成简短或详细的反馈文本，再拼入下一轮 prompt

并解释了评分器对 rank 的统一量化使得不同来源的错误能够进入同一比较空间；反馈构造器与评分器的解耦则允许在不改动评分逻辑的前提下灵活切换 L2/L3/L4 三种反馈粒度，这一设计直接支撑了第 5 章 §5.5 的反馈粒度实验。

## 四、新增了哪些图

新增 3 张技术图，均使用 Microsoft YaHei 中文字体渲染，PDF + PNG 双格式输出。

| 图号 | LaTeX label | PDF 路径 | 内容 |
|------|------------|----------|------|
| 图 3.3 | `fig:task_normalization` | `figure/fig_task_normalization_v1.pdf` | 多源 benchmark 到统一 Task 接口的转换流程 |
| 图 3.4 | `fig:llm_code_extraction` | `figure/fig_llm_code_extraction_v1.pdf` | LLM 回复到可编译 Verilog 文件的提取流程 |
| 图 3.5 | `fig:feedback_decision` | `figure/fig_feedback_decision_v1.pdf` | EDA 验证结果到反馈提示词的转换逻辑 |

每张新图配套至少 1 段解释正文（200--290 字），不存在"如图 3.x 所示"一句话结束的情况。

### 每张新图的设计要点

**图 3.3 多源 benchmark 转换流程**

- 上层：VerilogEval-Human 和 RTLLM 2.0 两个数据源（淡蓝色），各列出 3--4 个原始字段
- 中层：两个加载器（淡黄色）说明各自的归一化操作（合并参考与 testbench / 递归扫描 + 正则提取）
- 中央：统一 Task 接口（淡绿色，加粗），明确列出 `name` / `description` / `module_header` / `testbench_path` 四个字段
- 下层：Prompt Builder / Verilog Executor / Ranker 三个下游消费者（淡灰色）
- 右侧标注"下游模块仅依赖该接口"

**图 3.4 LLM 代码提取流程**

- 顶部：模拟一段真实 LLM 原始回复，包含 6 类典型片段（解释文本、CoT 推理、Markdown 围栏、目标 Verilog 代码块、围栏、解释尾段），每行右侧标注其类型，颜色区分（灰色解释、红色围栏、蓝色代码块）
- 中部：3 个橙黄色阶段框（移除 Markdown 围栏 / 定位 module ... endmodule / 写入 candidate.v），每框附说明语
- 底部：iverilog 编译 + vvp 仿真盒（淡蓝色，加粗）
- 最下方斜体说明：兼容四种提示策略

**图 3.5 反馈决策逻辑**

- 顶部：编译结果与仿真结果两个红色输入框，各列出 3 个分支及对应 rank 值
- 中层：评分器（绿色，加粗）给出 rank ∈ [-2.0, 1.0]
- 决策：rank = 1.0 ? 黄色判定框，"是" 分支引到右侧 PASS 输出（绿色），"否" 分支向下到反馈构造器（紫色）
- 底层：L2 / L3 / L4 三个粒度框（淡紫色），每框列出反馈内容
- 底部斜体：对应表 3.3 的指引

### 图风格特点

- 节点全部使用中文（技术标识符如 `iverilog`、`module` 等保留英文以避免歧义）
- 配色克制（每图最多 4--5 种淡色调），适合黑白打印
- 所有箭头方向清晰，无重叠（之前的 v10 第一版 fig 3.5 右下角"↓ 注入下一轮 prompt"标注与 L4 框重叠，已移到底部居中）
- 字号 9--12pt 范围，论文中可读
- 不依赖商业软件，由 `scripts/generate_thesis_ch3_figures.py` 用 matplotlib 一次性生成
- 图生成脚本可重复运行，PDF 导出保留矢量质量

## 五、第 4 章和第 5 章如何完成一一对应

修改文件：`report/thesis/latex/data/chapter4.tex` 与 `report/thesis/latex/data/chapter5.tex`

### 1. 第 4 章新增"实验设计与第 5 章结果章节的对应关系"表

在 §4.4 末尾新增 §4.4.4 子节 + 表 `tab:design_results_map`，包含 9 行：

```text
有效性验证   VerilogEval-Human 基线        验证反馈循环基础有效性          5.1
有效性验证   RTLLM_STUDY_12 正式            更难任务和多模型验证            5.2
收益归因     Feedback vs Retry-only 消融   分离反馈信息与多采样贡献         5.3
稳定性验证   4 轮重复实验                   检查结论统计稳健性              5.4
机制探索     反馈粒度实验                   分析反馈信息量影响              5.5
机制探索     多轮对话反馈实验               分析反馈组织方式影响            5.6
机制探索     提示词策略实验                 分析初始提示词影响              5.7
补充分析     典型案例分析                   解释成功、失败与边界            5.8
补充分析     综合讨论与小结                 跨实验整合与对照                5.9--5.10
```

✅ 三线表，表题在表上，列宽通过 `p{...}` 控制不溢出，与第 5 章实际章节标题完全一致。

### 2. 第 5 章开头明确承接第 4 章三层设计

原句："本章依次呈现七组实验的结果并进行分析。所有数据以实验结果索引为准。"

改为："本章按照第 4 章提出的三层实验设计展开结果分析：5.1--5.2 对应有效性验证，5.3--5.4 对应收益归因与稳定性验证，5.5--5.7 对应机制探索，5.8--5.10 对典型案例和综合结论进行补充讨论。与表 \ref{tab:design_results_map} 的对应关系逐一对齐，所有数据以实验结果索引为准。"

### 3. 第 5 章四处过渡句

| 位置 | 新增过渡句（自然口吻，避免机械堆叠"第一层/第二层"） |
|------|--------------------------------------------|
| §5.1 开头 | "首先报告第一层有效性验证实验。本节记录在 VerilogEval-Human 20 题子集上使用 Haiku 模型进行的基线实验，用以确认反馈循环在较低难度任务上的基本有效性。" |
| §5.3 开头 | "在确认反馈循环整体有效后，接下来进入第二层收益归因分析，需要回答的疑问是：这个提升究竟来自反馈信息本身，还是仅仅因为多采样机会增加？" |
| §5.5 开头 | "在完成有效性和收益归因分析后，本节开始进入第三层机制探索，首先考察反馈信息量的影响。" |
| §5.8 开头 | "前述结果给出了三层实验的整体统计结论，本节选取典型题目进一步解释反馈循环在具体任务上的作用方式，覆盖反馈修复成功、反馈弥补模型差距、反馈稳定收益与天花板题四类场景。" |

### 4. §5.5 / §5.7 增补了 LaTeX label

| section | 新增 label |
|---------|-----------|
| §5.5 反馈粒度实验 | `\label{sec:granularity}` |
| §5.7 提示词策略实验 | `\label{sec:prompt_strategy}` |

这两个 label 同时被第 3 章新增段落引用（§3.4 引 `sec:prompt_strategy`、§3.6 引 `sec:granularity`），形成第 3 章设计与第 5 章结果之间的双向链接。

### 5. §5.10 本章小结回扣第 4 章三层设计

改写后的小结按照"有效性验证（对应 5.1--5.2）→ 收益归因与稳定性（对应 5.3--5.4）→ 机制探索（对应 5.5--5.7）→ 典型案例与综合讨论（对应 5.8--5.9）"的顺序整合关键结论，明确说明每一层验证回应了第 4 章哪一项实验设计，并保留原版关于本文系统性扩展的总结。

## 六、是否新增"实验设计与结果章节对应关系"表

✅ 已新增。表名 `tab:design_results_map`，位于第 4 章 §4.4.4，9 行 4 列三线表。

## 七、是否保持实验数据不变

✅ 全部实验数值与 v9 一致：

- VerilogEval-Human 基线：80% → 90%（+10pp，2/4 修复）
- RTLLM 三模型对比：Haiku 5/12→6/12，Sonnet 5/12→7/12，GPT 6/12→10/12
- GPT-5.4 稳定性：均值 50.0% / 62.5% / 79.2%，标准差 ±11.8% / ±4.2% / ±4.2%
- Sonnet 4.6 稳定性：均值 62.5% / 72.9% / 58.3%，FB > RO 0/4 轮
- 粒度实验、多轮对话、提示词策略各表数据完全保持原值

未新增任何实验，未重跑任何实验，未修改任何 JSON 或 CSV 实验产物文件。

## 八、PDF 页数

| 版本 | 页数 | 文件 |
|------|------|------|
| v9（AutoChip 定位修订，本轮保留不动） | 58 | `thesis_supervisor_revision_v9.pdf` |
| **v10（本轮独立生成）** | **63** | `thesis_supervisor_revision_v10_ch3_ch4ch5.pdf` |

页数增加 5 页，主要来自：

- 第 3 章新增 3 张图（每张约占 1/2--3/4 页）+ 3 段解释正文
- 第 4 章新增 1 张设计-结果对应表（约 1/3 页）
- 第 5 章新增 4 处过渡句 + 重写小结（净增约 1/3 页）

## 九、编译警告

| 检查项 | 结果 |
|--------|------|
| Undefined citation | 0 |
| Undefined reference | 0 |
| Overfull \\hbox | 0 |
| Overfull \\vbox | 0 |
| BibTeX warning | 0 |
| 字体形状告警 | 仅 `TU/TimesNewRoman(0)/b/n` 与 `TU/txtt/m/n`（与 v9 同，MiKTeX 字体表行为，不影响排版） |

## 十、敏感信息检查

| 命中模式 | 结果 |
|---------|------|
| `sk-[A-Za-z0-9]{10,}` 在 latex 目录 | 无 |
| `api_key` / `API_KEY` / `base_url` / `BASE_URL` 在 latex 目录 | 无 |
| 在 `scripts/`、`src/` 中 | 仅命中环境变量名引用（`ANTHROPIC_API_KEY`、`OPENAI_API_KEY`、`os.environ.get(...)`），无硬编码密钥；属普通文本，不算泄漏 |
| `ghp_` 在仓库内 | 无 |

## 十一、AutoChip 定位是否回退

✅ **未回退**。本轮所有改动均集中在第 3、4、5 章，未触及 §2.4.4、§2.6 的 AutoChip 定位段落。重新检索：

- `\grep "复现.{0,3}AutoChip|AutoChip.{0,3}复现|在AutoChip.{0,5}基础上|AutoChip反馈闭环框架|AutoChip 反馈闭环框架"` → 0 命中
- §2.4.4 仍为"本文工作与最接近相关工作的关系"
- §2.4.4 首句仍为"在已有研究中，AutoChip 与本文最为接近：二者都关注……"
- §2.6 本文定位仍为"将 AutoChip 等反馈式代码修复工作作为最接近的相关工作进行对比"

## 十二、未提交项

- ✅ 未提交 `check/*.pdf`（被 `.gitignore` 排除）
- ✅ 未提交字体文件（`report/thesis/latex/font/` 被 `.gitignore` 排除）
- ✅ 未提交 `__pycache__/`、`*.aux`、`*.log`、`*.bbl` 等中间产物
- ✅ `HANDOFF_PROMPT_FOR_CASCADE.md` 仍为 untracked，未入库

## 十三、是否建议发给导师

✅ **建议**。本轮已严格按照导师两条意见处理：

1. 第 3 章新增 3 张技术图（图 3.3 / 3.4 / 3.5）+ 约 760 字技术正文，从"目标—挑战—方案—实现"框架中得到自然扩充，未变成模块清单或代码细节堆砌。
2. 第 4 章新增对应关系表，第 5 章开头、四处过渡、§5.10 小结全部按三层设计对齐，第 3 章新增段落与第 5 章实验小节通过 `sec:granularity` 和 `sec:prompt_strategy` 两个 label 形成双向引用。

实验数据、AutoChip 定位、致谢、参考文献、摘要均未改动；编译告警与上一版完全一致；PDF 体积合理（2.1 MB / 63 页）。

**送审 PDF**：`report/thesis/latex/thesis_supervisor_revision_v10_ch3_ch4ch5.pdf`（本轮独立生成，63 页）。

**说明**：`thesis_supervisor_revision_v9.pdf` 保留为 v9 + AutoChip 定位修订的历史快照（58 页），本轮不覆盖该文件。

---

## 附：本轮未做的事

- 未新增 / 重跑实验
- 未修改实验数据
- 未删除任何 AutoChip 引用
- 未改动 §2.4.4 / §2.6 的 AutoChip 定位
- 未改摘要、致谢、结论、参考文献
- 未删除任何历史 PDF（v1--v9 全部保留）
- 未提交 `check/`、字体、`__pycache__/`
