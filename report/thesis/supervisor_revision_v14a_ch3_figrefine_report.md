# 导师修订 v14a — 第 3 章图微调 + v14 任务自查

**日期**：2026-05-17
**对应 commit**：本轮 v14a 修订（待生成 hash）
**输出 PDF**：`report/thesis/latex/thesis_supervisor_revision_v14a_ch3_figrefine.pdf`（66 页）
**前一版本**：v14（`140c5c0`，`thesis_supervisor_revision_v14_ch3_refine.pdf`，65 页）

---

## 1. 本轮的两项工作

导师对 v14 反馈了 4 条具体的图修订意见，并要求对 v14 的整体完成质量进行自查：

1. **图 3.1**：无需再修改。
2. **图 3.2**：右侧蓝字去掉（若内容重要则在正文提及）。
3. **图 3.3**：`iverilog -g2012 编译 + vvp 仿真` 方框不够大文字出界，加宽；底部灰色小字去掉（若重要则在正文提及）。
4. **图 3.4**：同样有字体出界，加大方框纵向长度把文字分两行放。
5. **图 3.5**：无需再修改。

外加：对 v14 主任务（图尺寸优化 + 第 3 章正文加强）做完整自查。

v14a 不动正文、不动实验数据、不重排章节，仅对 3 张图做局部微调。

---

## 2. 图修订实施

### 2.1 图 3.2 — 删除右侧蓝色 _label

原 v14：
```python
# Side annotation
_label(ax, (10.55, task_y + task_h / 2),
       "加载器屏蔽数据来源差异\n下游模块仅依赖该接口",
       color=ACCENT, ha="left", va="center", style="italic")
```

v14a：删除此 `_label` 调用，替换为注释说明删除原因。

该蓝字内容（"加载器屏蔽数据来源差异 / 下游模块仅依赖该接口"）**已在 §3.3 正文中完整覆盖**：
- 第 76 行：`所有下游模块——提示词构建器、执行器、评分器等——仅依赖Task接口，不感知数据来源是VerilogEval还是RTLLM。`
- 第 80 行：`下游模块仅依赖 name/description/module_header/testbench_path 四个字段`

因此图内蓝色标注是冗余的，删除不损失任何信息。

### 2.2 图 3.3 — 加宽 iverilog 方框 + 删除底部 _label

**加宽方框**：
```python
# 原 v14
iv_x, iv_w = 2.5, 4.0   # box spans x ∈ [2.5, 6.5]

# v14a
iv_x, iv_w = 1.5, 6.0   # box spans x ∈ [1.5, 7.5]，加宽 50%
```

方框中心保持在 x=4.5，与上方 `阶段 1/2/3` 三个长方框对齐。新宽度 6.0 让 bold 中文文本 "iverilog -g2012 编译 + vvp 仿真" 两侧有充足留白。

**删除底部 _label**：
```python
# 原 v14
_label(ax, (4.5, 0.45),
       "该提取流程兼容 Base / CoT / Few-shot / Few-shot+CoT 四种提示策略，"
       "无需为不同策略维护专用解析器。",
       ha="center", style="italic", fontsize=9)
```

该灰字内容已在 §3.4 正文中完整覆盖：
- 第 99 行末尾：`这一设计也使得提取器无需为Base、CoT、Few-shot、Few-shot+CoT四种提示策略维护各自的解析器，第 5.7 节的提示策略实验在统一提取流程下完成，避免了因解析逻辑差异引入的混淆变量。`

正文版本比图内灰字更详细（额外说明了"统一提取流程消除混淆变量"的设计意图），删除图内灰字不损失任何信息。

### 2.3 图 3.4 — 拆 `构造反馈 Prompt` 方框为两行 + 加高

原 v14：
```python
fb_y = 2.7
_box(ax, (bx, fb_y - bh / 2), bw, bh,       # bh = 0.85
      "构造反馈 Prompt  (附编译/仿真信息)", weight="bold")
```

`bh = 0.85` 是统一的链条方框高度。在 figsize 缩到 (4.5, 5.75) 后，bold + 长中文 `(附编译/仿真信息)` 在 fontsize=10 下接近右边界，部分渲染环境（PDF）会出现微溢出。

v14a：
```python
fb_y = 2.7
fb_h = 1.3                                  # 较 bh=0.85 加高约 53%
_box(ax, (bx, fb_y - fb_h / 2), bw, fb_h,
      "构造反馈 Prompt\n（附编译 / 仿真信息）", weight="bold")
```

- 文字按语义分两行：第一行 `构造反馈 Prompt`（功能名），第二行 `（附编译 / 仿真信息）`（功能说明）。
- 方框高度从 `bh=0.85` 增到 `fb_h=1.3`，给两行文本留出垂直呼吸空间。
- 同步调整下方箭头出发点：`(cx, fb_y - bh / 2)` → `(cx, fb_y - fb_h / 2)`，确保箭头不再从两行文本中间穿过。
- 上方箭头也同步调整到方框新上沿：`(cx, fb_y + fb_h / 2)`。

几何验证：
- 决策菱形底端 y=4.15；方框新上沿 y=3.35；箭头长 0.8，无重叠。
- 方框新下沿 y=2.05；iter 方框上沿 y=1.425；箭头长 0.625，无重叠。

---

## 3. 三张图修订效果（v14a PNG）

| 图号 | v14 问题 | v14a 现状 |
|---|---|---|
| 3.2 | 右侧蓝色斜体标注挂在 Task 接口框右边，导致整图不对称 | 蓝字删除后整体布局对称，下游 Prompt Builder / Verilog Executor / Ranker 三联看起来居中 |
| 3.3 | iverilog 方框文字接近边界；底部灰字与上方流程图不属同一逻辑层 | 方框文字两侧留白充足；底部留白干净，整图主体收敛在 `LLM 原始回复 → 阶段 1/2/3 → iverilog+vvp` 一条主线 |
| 3.4 | bold 长文本 `构造反馈 Prompt（附编译/仿真信息）` 在缩小 figsize 后右侧接近溢出 | 文字按语义分两行，方框增高 53%，视觉上有节奏感且不溢出 |

---

## 4. v14 主任务完成质量自查

针对 v14 原提示词的五项要求逐条对照实际交付。

### 4.1 图 3.1 / 3.3 / 3.4 / 3.5 缩小，保证打印清晰（要求 #1）

| 图号 | v13 LaTeX width | v14 LaTeX width | v14 figsize | 自检 |
|---|---|---|---|---|
| 3.1 | 0.92 | **0.78** | (11.5,11.0) → (8.0,7.65) | ✅ |
| 3.3 | 0.85 | **0.65** | (9.0,10.5) → (6.0,7.0) | ✅ |
| 3.4 | 0.85 | **0.50** | (9.0,11.5) → (4.5,5.75) | ✅ |
| 3.5 | 0.95 | **0.85** | (11.0,9.0) → (8.5,6.95) | ✅ |

- PyMuPDF 自检：**v14a 中 figure-only pages = 0**（v13 中图 3.4 在 p.29 独占）。
- 视觉字号：缩放比保持在 0.6–0.7，A4 打印仍可读。
- 图 3.2 形状本就扁，未独占页面，未动；图 3.5 L3/L4 标签紧凑化避免溢出（v14 已做）。

**结论：要求 #1 完成质量符合预期**。

### 4.2 §3.1 技术难点段 + 表 3.2（要求 #2 的"难点"层面）

实际交付：
- `chapter3.tex` 第 16 行：新增一段（约 280 字）阐明"上述三类挑战的本质并非'调用一次大语言模型'..."，强调流水线设计是真正难点。
- `chapter3.tex` 第 18–33 行：新增 `表 3.2 第 3 章系统设计对应的主要技术难点`，5 行三列对照（技术难点 / 具体表现 / 本文解决思路），覆盖 benchmark 格式 / LLM 输出 / EDA 反馈信号 / 反馈信息量 / 多组实验复用五个层面。
- 第 35 行末尾新增一句衔接："下文围绕这五类难点，依次介绍系统的总体方案和各部分的设计与实现。"

**结论：要求 #2 难点层面完成质量符合预期，且新增表 3.2 起到了章节内导航作用**。

### 4.3 §3.2 闭环 vs zero-shot + 框架复用性（要求 #2 的"创新点"层面）

实际交付：
- `chapter3.tex` 第 70 行：新增一段（约 180 字）。

关键文本节选：
> 与 zero-shot 一次性生成代码相比，反馈循环的关键在于每一轮都要把模型的自然语言输出转化为可执行的候选代码，再把 EDA 工具的离散结果转化为下一轮模型可理解的文本反馈。本系统将生成、验证、评分、反馈构造和结果记录拆为相对独立的环节，使得 zero-shot、retry-only、不同反馈粒度和多轮对话等实验条件都可以在同一执行框架下切换 …… 这一可复用性是第 4 章七组实验得以在统一基线下进行交叉比较的工程前提。

**结论：要求 #2 创新点层面完成质量符合预期，明确把闭环框架的可复用性与第 4 章七组实验的工程基础挂钩**。

### 4.4 §3.3–§3.6 设计取舍段（要求 #2 进一步深化）

| 节 | 设计取舍段位置 | 主题 |
|---|---|---|
| §3.3 多源benchmark | 第 91 行 | 加载器层封装 vs 下游分散处理 |
| §3.4 代码生成与提取 | 第 99 行末尾 / 第 108 行 | 提取流程从提示策略中解耦，消除混淆变量 |
| §3.5 编译仿真与评分 | 第 140 行 | rank 标量 vs pass/fail 二值评分的取舍 |
| §3.6 反馈构造 | 第 219 行 | 反馈粒度可切换 vs 固定一种的工程考虑 |

每段都遵循"如果不这么做会怎样 → 这么做的好处 → 与后续章节的关系"三段式表述。

**结论：要求 #2 设计取舍层面完成质量符合预期，4 节均覆盖且取舍论证清晰**。

### 4.5 §3.8 难点→方案回扣（要求 #3）

实际交付（第 231–233 行）：
- 第 1 段：从五类工程难点出发回扣本章设计逐项说明（加载器层 / 提取器层 / rank 标量 / L0–L4 五级粒度 / 单多轮对话切换）。
- 第 2 段：交代本章在论文结构中的位置（→ 第 4 章七组实验 → 第 5 章对比），并**主动说明本章贡献边界**：「本章描述的设计不包含新的模型架构或全新的 EDA 算法，主要贡献在于把多个已有组件组装为一个可复现、可追溯、可扩展的实验框架，这亦是本科毕设范围内"动手实现"部分的主要工程重点」。

**结论：要求 #3 完成质量符合预期，难点回扣 + 论文结构定位 + 贡献边界声明三重作用**。

### 4.6 自查总评

| 原 v14 提示词要求 | 实际交付 | 自评 |
|---|---|---|
| 1. 图 3.1/3.3/3.4/3.5 缩小、保持清晰 | 4 张图的 figsize 与 LaTeX width 联合缩放，0 个图独占页 | ✅ 完成 |
| 2.a §3.1 技术难点 | 新增段 + 表 3.2 5 行难点对照 | ✅ 完成 |
| 2.b §3.2 闭环 vs zero-shot | 新增段，强调框架可复用性与 §4 实验的依赖关系 | ✅ 完成 |
| 2.c §3.3–§3.6 设计取舍 | 4 节各 1 段，三段式表述 | ✅ 完成 |
| 3. §3.8 难点→方案回扣 | 2 段，含论文结构定位 + 贡献边界声明 | ✅ 完成 |

**v14 主任务整体完成质量符合提示词要求**。v14a 三处图微调进一步消除了导师在 v14 PDF 中观察到的细节缺陷。

---

## 5. 编译与版式自检

```
pages = 66 (v14 = 65, +1 页是 Fig 3.4 加高后正文小幅重排)
errors = 0
undefined refs / cites = 0
Overfull \hbox > 5pt = 0
Overfull \hbox 总数 = 2 (1.95pt + 0.11pt，与 v13 / v14 一致)
Underfull \hbox 总数 = 0
figure-only pages = 0
```

字体警告（`TU/TimesNewRoman(0)/b/n`, `TU/txtt/m/n`）为 buaathesis 模板已有，与所有历史版本一致。

---

## 6. 修改文件清单

| 文件 | 操作 | 内容 |
|---|---|---|
| `scripts/generate_thesis_ch3_figures_v13.py` | 修改 | Fig 3.2 删除右侧 _label；Fig 3.3 加宽 iverilog 方框 + 删除底部 _label；Fig 3.4 拆 `构造反馈 Prompt` 方框为两行 + 加高 |
| `report/thesis/latex/figure/fig_task_normalization_v13.pdf` | 重生成 | 删除右侧蓝色标注后整图右侧 bbox 收紧 |
| `report/thesis/latex/figure/fig_llm_code_extraction_v13.pdf` | 重生成 | iverilog 方框加宽；底部灰字删除 |
| `report/thesis/latex/figure/fig_feedback_loop_v13.pdf` | 重生成 | `构造反馈 Prompt` 拆两行 + 方框加高 |
| `report/thesis/latex/main.pdf` | 重编 | 66 页 |
| `report/thesis/latex/thesis_supervisor_revision_v14a_ch3_figrefine.pdf` | 新增 | 本轮交付 PDF |
| `report/thesis/supervisor_revision_v14a_ch3_figrefine_report.md` | 新增 | 本报告（含 v14 自查记录）|
| `notes/thesis_writing_plan.md` | 修改 | 追加 v14a 状态 |
| `report/thesis/latex_migration_notes.md` | 修改 | 追加 v14a 状态 |

图 3.1 / 3.5 的 PDF 会因脚本运行被重写，但内容字节稳定（matplotlib 输出确定性）。

旧 v1 / v2 / v13 / v14 图 PDF 文件**均未删除**，保留在 `figure/` 目录下。

---

## 7. v14a 不做的事

- 第 4 / 5 / 6 章正文 — 完全未触；
- 全部 13 张数据图 — 完全未触；
- 第 3 章正文 — 完全未触（仅图发生变化）；
- 参考文献 / 附录 — 完全未触；
- 实验数据、运行脚本（除图生成脚本外）— 完全未触。

---

## 8. 待办

```
git add scripts/generate_thesis_ch3_figures_v13.py
git add report/thesis/latex/figure/fig_task_normalization_v13.pdf
git add report/thesis/latex/figure/fig_task_normalization_v13.png
git add report/thesis/latex/figure/fig_llm_code_extraction_v13.pdf
git add report/thesis/latex/figure/fig_llm_code_extraction_v13.png
git add report/thesis/latex/figure/fig_feedback_loop_v13.pdf
git add report/thesis/latex/figure/fig_feedback_loop_v13.png
git add report/thesis/latex/main.pdf
git add report/thesis/latex/thesis_supervisor_revision_v14a_ch3_figrefine.pdf
git add report/thesis/supervisor_revision_v14a_ch3_figrefine_report.md
git add notes/thesis_writing_plan.md
git add report/thesis/latex_migration_notes.md
git commit -m "thesis v14a: fine-tune ch3 figures per supervisor feedback"
git push
```
