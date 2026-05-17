# 导师修订 v14 — 第 3 章图尺寸 + 正文加强报告

**日期**：2026-05-17
**对应 commit**：本轮 v14 修订（待生成 hash）
**输出 PDF**：`report/thesis/latex/thesis_supervisor_revision_v14_ch3_refine.pdf`（65 页）
**前一版本**：v13（`report/thesis/latex/thesis_supervisor_revision_v13_figures.pdf`，64 页）

---

## 1. 本轮修订的两条导师意见

导师对 v13 的反馈集中在第 3 章：

1. **图占页面比例过大**——v13 中第 3 章 5 张图的 PDF 物理尺寸偏大，部分图加上 caption 后接近独占整页，导致正文被频繁打断。
2. **第 3 章正文偏简单**——除了流程图和接口表，缺少明确的"难点—解决思路"对照、设计取舍说明，以及对本章在论文结构中位置的回扣。

v14 的目标即针对这两条意见，不动实验数据、不重排章节顺序，仅在：

- 5 张图的物理尺寸 / LaTeX `width` 上做联合缩放；
- 在 §3.1 增加难点表，在 §3.3–§3.6 各加一段设计取舍，在 §3.2 加一段"闭环 vs zero-shot"对比，在 §3.8 重写本章小结。

---

## 2. 5 张图的尺寸调整

第 3 章 5 张图的 figsize 与 LaTeX `width` 联合调整，使图加上 caption 后均不再独占整页。原则：

- 缩小 figsize 让字体相对图框变大；
- 同时缩小 LaTeX `width` 让最终物理宽度也变小；
- 二者比例保持在视觉字号 ≥ 6pt（缩放比 ≈ 0.6–0.7），保证 A4 打印仍可读。

| 图号 | 描述 | figsize (v13) | figsize (v14) | LaTeX width (v13) | LaTeX width (v14) |
|---|---|---|---|---|---|
| 3.1 | 系统架构 | 11.5×11.0 | **8.0×7.65** | 0.92 | **0.78** |
| 3.2 | Task 归一化 | 11.0×8.0 | 11.0×8.0（不变） | 0.92 | 0.92（不变） |
| 3.3 | 代码提取 | 9.0×10.5 | **6.0×7.0** | 0.85 | **0.65** |
| 3.4 | 反馈循环 | 9.0×11.5 | **4.5×5.75** | 0.85 | **0.50** |
| 3.5 | 反馈决策 | 11.0×9.0 | **8.5×6.95** | 0.95 | **0.85** |

图 3.2 形状本身较扁（aspect ≈ 0.73），v13 中加上 caption 没有独占页面，因此 v14 不动。

图 3.5 中 L3 / L4 标签文字因 figsize 缩小后曾溢出框右边界，文本紧凑化为 "编译错误+不匹配数+前40行输出" / "编译错误+前80行输出+分析提示"（去掉 `+` 旁空格），详细的反馈级别描述仍由表 3.4 (`tab:feedback_levels`) 给出。

### 2.1 验证：5 张图均不再独占页面

用 PyMuPDF 提取每页文字字符数，扣除页眉后正文字符 < 200 字符的页面被视为"图为主"页面。v14 的低字符页：

| 页面 | 字符 | 内容 | 是否预期 |
|---|---|---|---|
| p.01 | 95 | 封面 | ✅ 预期 |
| p.04 | 75 | 独立性声明 | ✅ 预期 |
| p.07 | 96 | Key words（摘要末尾） | ✅ 预期 |
| p.33 | 106 | §3.8 本章小结末尾 | ✅ 预期 |

**0 个图独占页面**（v13 中图 3.4 在 p.29 独占）。

---

## 3. 第 3 章正文增强

总计净增正文约 1700 字（不含表 3.2 内容）。所有增加都是"为什么这样设计"层面的解释，不引入新的实验数据，不改变现有 §3.2–§3.7 的事实陈述。

### 3.1 §3.1 增加难点段 + 表 3.2

紧接原 §3.1 末尾的"三类挑战"列举之后，加入：

- **1 段（约 280 字）**：阐明本章工程难点的本质不在于"调用一次 LLM"，而在于把不稳定的 NL 生成过程与严格的 EDA 流程串接起来，并保证流水线能在多模型/benchmark/反馈模式组合下稳定复用。
- **新表 3.2（5 行）**：列出 5 个技术难点 / 具体表现 / 解决思路三列对照，覆盖 benchmark 格式 / LLM 输出 / EDA 反馈信号 / 反馈信息量 / 实验复用五个层面。

表 3.2 的目的是给读者一个章节内导航——读者可以先看表，再选择性深入 §3.3–§3.7 中对应的实现细节。

### 3.2 §3.2 增加"闭环 vs zero-shot"段

在工程约束段之前，紧接图 3.1 之后增加 1 段（约 180 字），阐明反馈循环与 zero-shot 的关键差异：每一轮都要在自然语言↔可执行代码↔结构化反馈之间往返，本系统将流水线拆为 5 个相对独立环节正是为了支撑第 4 章七组实验在同一执行框架下的交叉比较。

### 3.3 §3.3 增加加载器层封装取舍段

加在 §3.3 末尾原"扩展到 RTLLM 时无需修改"段之后，约 180 字。强调把数据格式复杂度集中到加载器层 vs 分散到下游各模块的取舍：后者在新增第三个 benchmark 时会让改动面随支持来源数量近似线性扩散，前者新增 benchmark 的成本仅相当于新增一个加载器实现。

### 3.4 §3.4 增加提取流程解耦取舍段

加在 §3.4 中"在模型调用层面"之前，约 200 字。说明两阶段提取的另一目的是把代码提取从提示策略中解耦：若让每种提示策略各自维护解析逻辑，§5.7 的提示策略对比就会同时混入两层差异，难以判断通过率变化的来源。统一提取流程消除了这一混淆变量。

### 3.5 §3.5 增加 rank vs pass/fail 取舍段

加在 §3.5 末尾"两种中间状态含义"段之后，约 200 字。解释为何选 rank 标量而非 pass/fail 二值：反馈循环的全局最优追踪需要在尚未通过的候选之间做比较；只看 pass/fail 时所有未通过候选同等"失败"，控制器无法把"接近通过"和"完全错误"区分开。

### 3.6 §3.6 增加反馈粒度可切换取舍段

加在 §3.6 末尾提示策略段之后，约 230 字。说明反馈粒度做成可切换而非固定一种的原因：不同模型对"信息量 vs 噪声"的权衡点不一致，这是设计阶段无法仅凭推理确定的工程问题。提供 L2/L3/L4 三档让粒度实验能把"反馈是否有效"和"反馈粒度该多大"两个问题分开回答。

### 3.7 §3.8 本章小结重写

原 v13 §3.8 是 1 段总结模块映射；v14 改写为 2 段：

- **第 1 段**：从 5 类工程难点出发回扣本章设计——把整条流水线的差异封装到最合适的层，使下游模块以最小代价对接不同模型/benchmark/反馈模式。具体到加载器层 / 提取器层 / rank 标量 / L0–L4 五级粒度 / 单多轮对话切换的设计逐项说明。
- **第 2 段**：交代本章在论文结构中的位置——这些设计构成 §4 七组实验在三模型/两 benchmark 之间灵活组合的工程基础，也使 §5 对反馈/粒度/多轮/提示策略的对比能在统一基线下进行；并主动说明本章贡献不在新模型或新 EDA 算法，而在于把多个已有组件组装为可复现/可追溯/可扩展的实验框架，这是本科毕设范围内"动手实现"部分的主要工程重点。

第 2 段是为了回应导师"本章贡献到底是什么"的潜在质疑，给出了一个不夸大但也不弱化本科毕设范围内贡献的表述。

---

## 4. 编译自检

```
pages = 65 (v13 = 64, 增加表 3.2 + 6 段正文 + 小结改写共净增 1 页)
errors = 0
undefined refs / cites = 0
Overfull \hbox > 5pt = 0
Overfull \hbox 总数 = 2 (1.95pt + 0.11pt, 均与 v13 一致, 非本轮新增)
Underfull \hbox 总数 = 0
figure-only pages = 0
```

字体警告（`TU/TimesNewRoman(0)/b/n`, `TU/txtt/m/n`）为 buaathesis 模板已有，与 v13 一致，不影响内容。

---

## 5. 修改文件清单

| 文件 | 操作 | 内容 |
|---|---|---|
| `scripts/generate_thesis_ch3_figures_v13.py` | 修改 | 4 处 figsize 缩小；图 3.5 L3/L4 标签紧凑化 |
| `report/thesis/latex/data/chapter3.tex` | 修改 | 4 处 includegraphics width；6 处正文段落新增；§3.8 重写 |
| `report/thesis/latex/figure/fig_system_architecture_v13.pdf` | 重生成 | figsize (11.5×11.0) → (8.0×7.65) |
| `report/thesis/latex/figure/fig_llm_code_extraction_v13.pdf` | 重生成 | figsize (9.0×10.5) → (6.0×7.0) |
| `report/thesis/latex/figure/fig_feedback_loop_v13.pdf` | 重生成 | figsize (9.0×11.5) → (4.5×5.75) |
| `report/thesis/latex/figure/fig_feedback_decision_v13.pdf` | 重生成 | figsize (11.0×9.0) → (8.5×6.95) + 标签紧凑化 |
| `report/thesis/latex/main.pdf` | 重编 | 65 页 |
| `report/thesis/latex/thesis_supervisor_revision_v14_ch3_refine.pdf` | 新增 | 本轮交付 PDF |
| `report/thesis/supervisor_revision_v14_ch3_refine_report.md` | 新增 | 本报告 |
| `scripts/check_v14_pages.py` | 新增（一次性自检） | 用 PyMuPDF 提取每页文字字符数，检测图独占页 |

图 3.2 (`fig_task_normalization_v13.pdf`) 也会被脚本重新生成但内容字节不变（matplotlib 输出位级稳定），git diff 应为空。

旧 v1 / v2 / v13 图 PDF 文件**均未删除**，保留在 `figure/` 目录下，便于回溯任何旧版本编译产物。

---

## 6. v14 不做的事

为遵守"不改实验数据、不重排章节、不动结论"的原则，以下内容明确未改动：

- 第 4、5 章正文 — 完全未触；
- 全部 13 张数据图 — 完全未触；
- 第 3 章实验数据 / 接口说明 / 算法 1 — 完全未触；
- 第 6 章总结展望 — 完全未触；
- 参考文献 / 附录 — 完全未触。

下次如果还有进一步意见，可在 v15 中处理。

---

## 7. 待办：commit + push

```
git add scripts/generate_thesis_ch3_figures_v13.py
git add scripts/check_v14_pages.py
git add report/thesis/latex/data/chapter3.tex
git add report/thesis/latex/figure/fig_system_architecture_v13.pdf
git add report/thesis/latex/figure/fig_llm_code_extraction_v13.pdf
git add report/thesis/latex/figure/fig_feedback_loop_v13.pdf
git add report/thesis/latex/figure/fig_feedback_decision_v13.pdf
git add report/thesis/latex/figure/fig_system_architecture_v13.png
git add report/thesis/latex/figure/fig_llm_code_extraction_v13.png
git add report/thesis/latex/figure/fig_feedback_loop_v13.png
git add report/thesis/latex/figure/fig_feedback_decision_v13.png
git add report/thesis/latex/main.pdf
git add report/thesis/latex/thesis_supervisor_revision_v14_ch3_refine.pdf
git add report/thesis/supervisor_revision_v14_ch3_refine_report.md
git add notes/thesis_writing_plan.md
git add report/thesis/latex_migration_notes.md
git commit -m "thesis v14: shrink ch3 figures, add design-tradeoff paragraphs and challenge table"
git push
```
