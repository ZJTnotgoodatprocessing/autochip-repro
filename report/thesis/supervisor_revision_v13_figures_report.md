# 导师修订 v13 — 第 3 章流程图重绘报告

**日期**：2026-05-16
**对应 commit**：本轮 v13 修订（待生成 hash）
**输出 PDF**：`report/thesis/latex/thesis_supervisor_revision_v13_figures.pdf`（64 页）
**前一版本**：v12（`b36b081`，`thesis_supervisor_revision_v12.pdf`，63 页）

---

## 1. 本轮修订目标

v12 中按导师意见 #1 的"图一眼看出 AI 生成且不美观"问题已经做了：
- 删除全部 15 张图的图内英文 banner；
- 全部数据图统一输出 PDF 矢量；
- `\includegraphics` 切换到 `.pdf`。

但 v12 自检中明确承认：第 3 章 5 张系统设计类流程图（图 3.1–3.5）的主体仍然是 matplotlib `FancyBboxPatch` 自动布局的"色块 + 圆角矩形 + 渐变箭头 + 多色卡片"风格，这正是评审眼中"AI 生成感"最强的部分。

**v13 的唯一目标**：把这 5 张图整体重绘为正式论文风格的黑白 / 灰阶矢量图，彻底消除该问题；同时顺手收敛第 3.7 节"4 项核心检查"的正文表述，避免再出现"24"字样让导师误以为未改。

不重写正文、不新增实验、不改实验数据。

---

## 2. 第 3 章 5 张图风格变化对照

| 图号 | 旧文件（v12） | 新文件（v13） |
|---|---|---|
| 图 3.1 | `figure/fig_system_architecture_v2.pdf` | `figure/fig_system_architecture_v13.pdf` |
| 图 3.2 | `figure/fig_task_normalization_v1.pdf` | `figure/fig_task_normalization_v13.pdf` |
| 图 3.3 | `figure/fig_llm_code_extraction_v1.pdf` | `figure/fig_llm_code_extraction_v13.pdf` |
| 图 3.4 | `figure/fig_feedback_loop_v2.pdf` | `figure/fig_feedback_loop_v13.pdf` |
| 图 3.5 | `figure/fig_feedback_decision_v1.pdf` | `figure/fig_feedback_decision_v13.pdf` |

旧 v1 / v2 PDF 文件**未删除**，仍保留在 `figure/` 目录下，便于回溯任何旧版本编译产物。

风格变化：

| 维度 | v12 旧图 | v13 新图 |
|---|---|---|
| 矩形形状 | 圆角 (`FancyBboxPatch boxstyle=round,pad=0.10`) | **直角** (`Rectangle`) |
| 框内填充 | 多色（绿/橙/蓝/紫/红/灰），低饱和但仍是色块堆叠 | **白底**，全部框统一无色填充 |
| 边框颜色 | `#2C3E50` 深灰蓝 | `#1A1A1A` 近黑 |
| 箭头颜色 | 主流程深灰 + 反馈红色 | 主流程黑 + **单一深蓝** `#1F3A5F` 用于决策菱形和反馈虚线 |
| 反馈回路 | 红色弧线 + 红色斜体"feedback / Next Iteration" | 深蓝色虚线 + 深蓝色斜体"反馈回路 / 下一轮迭代" |
| 装饰元素 | 圆形起止点（"Start / End"）、多色文字标注 | 全部移除，仅保留文本框与决策菱形 |
| 字体 | 多种 fontweight 与彩色文本混用 | 统一中文 sans-serif，仅"PASS"等关键词加粗，无彩色文字 |
| 图内英文 banner | v12 已删 | 仍无 |
| 图号"图 3.x" | v12 已确认无 | 仍无 |
| 输出格式 | PDF + PNG | PDF + PNG（PDF 用于论文，PNG 仅 GitHub 预览） |

---

## 3. 实现方式

**全部使用 matplotlib + Rectangle / Polygon 实现**，未使用 TikZ。理由：

1. 项目内全部 13 张数据图 + 2 张原流程图都是 matplotlib 体系，统一技术栈便于后续维护；
2. xelatex + ctex 中文环境下，TikZ 中文 + 多文本框流程图需引入 `\usetikzlibrary{positioning,shapes,arrows.meta}` 且对每张图额外维护 200+ 行 LaTeX 源码，工作量远大于 matplotlib 重绘；
3. matplotlib 用纯 `Rectangle`（非 `FancyBboxPatch`）+ 统一线宽 + 单色填充已经能达到与 TikZ 视觉等效的"线框稿"风格，输出 PDF 同为矢量。

**生成脚本**：`scripts/generate_thesis_ch3_figures_v13.py`
- 可重复运行（`python scripts/generate_thesis_ch3_figures_v13.py`）；
- 不覆盖 v1 / v2 旧图；
- 同时输出 PDF + 200 dpi PNG；
- 字体优先 `Microsoft YaHei`，回退 `SimHei` / `Noto Sans CJK SC`。

---

## 4. 风格合规自检（按用户提示词 16 条）

| # | 风格要求 | v13 是否满足 |
|---|---|---|
| 1 | 白底 | ✅ `facecolor="white"` |
| 2 | 黑/深灰线框为主 | ✅ `#1A1A1A` |
| 3 | 最多一种低饱和强调色 | ✅ 仅 `#1F3A5F` 深蓝（用于决策菱形和反馈虚线） |
| 4 | 不要圆角矩形 | ✅ `Rectangle`，非 `FancyBboxPatch` |
| 5 | 不要阴影 | ✅ 未使用任何阴影 patch |
| 6 | 不要渐变 | ✅ 单色填充 |
| 7 | 不要大面积彩色填充 | ✅ 全部白色填充 |
| 8 | 不要装饰性图标 | ✅ 已移除 v12 的 Start / End 圆点 |
| 9 | 不要"图 3.x"硬编码 | ✅ 全部图内未出现图号 |
| 10 | 不要顶部英文标题 | ✅ 5 张图均无 banner |
| 11 | 图题完全交给 LaTeX `\caption{}` | ✅ |
| 12 | 箭头线宽统一 | ✅ 统一 `LW = 1.1`，箭头风格 `-|>`、`mutation_scale=12` |
| 13 | 框内文字短 | ✅ 单格最长一条不超过 14 个汉字或等价英文 |
| 14 | 字号保证打印可读 | ✅ 主框 10–11 pt，副字 8.5–9.5 pt |
| 15 | 优先输出 PDF 矢量 | ✅ |
| 16 | LaTeX `\includegraphics{...pdf}` | ✅ chapter3.tex 5 处全部切到 v13 PDF |

---

## 5. 第 3.7 节"4 项核心检查"表述修正

**v12 自检版（被本轮重写）**：

> 代码审计脚本（`audit_project.py`）围绕评分器、Verilog 模块提取器、仿真输出解析器和反馈循环逻辑这 4 个核心模块执行自动化断言检查（共 24 个独立断言），确保核心接口在迭代过程中不发生回归。

技术上真实，但保留了"24 个独立断言"，导师快速扫读时可能误以为 v12 仍未把"24 项"改掉。

**v13 修订版**（`@c:/Users/17819/autochip-repro/report/thesis/latex/data/chapter3.tex:198`）：

> 代码审计脚本（`audit_project.py`）围绕评分器、Verilog 模块提取器、仿真输出解析器和反馈循环逻辑执行 4 项核心检查，确保核心接口在迭代过程中不发生回归。

LaTeX 正文 0 处出现"24 项 / 24 个独立断言 / 24 项自动化"。"24 个 `check()` 断言"这一事实仅保留在本轮报告与 `supervisor_revision_v12_report.md` 中，论文正文不再出现该数字。

`grep -R "24 项\|24项\|24 个独立断言\|24个独立断言" report/thesis/latex/data` → 0 命中。

---

## 6. 同步修改的 caption（图 3.1）

旧 caption 描述了"绿/橙/蓝/紫/红/深灰六种颜色"和"红色弧线"等彩色信息：

> 系统模块架构与数据流。模块颜色按功能分组：绿色为 benchmark 加载器与产物输出，橙色为统一 Task 接口，蓝色为提示词构建与 LLM 调用，紫色为代码提取与评分，红色为 EDA 编译仿真，深灰为反馈循环控制器；红色弧线标示反馈信号从控制器回流至下一轮提示词构建的路径。

v13 图已全部黑白，caption 同步重写为不依赖彩色的描述：

> 系统模块架构与数据流。系统按 Benchmark 加载、统一 Task 接口、生成、验证、反馈控制和产物输出六层组织：实线箭头表示前向数据流，深蓝色虚线表示反馈回路，由反馈构造器将验证结果回送至提示词构建器以进入下一轮迭代。

其余 4 张图的 caption 在 v12 已是中性描述，未做改动。

---

## 7. 编译检查

```bash
cd report/thesis/latex
xelatex -interaction=nonstopmode main.tex
bibtex main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

| 项目 | 结果 |
|---|---|
| 输出页数 | **64 页**（v12 为 63 页，新图行高与 v12 略不同，正文增加 1 页） |
| 输出 PDF 大小 | 999 619 字节（约 976 KB） |
| Undefined references | **0** |
| Undefined citations | **0** |
| BibTeX warnings | **0**（`main.blg` `warning$ -- 0`） |
| Overfull \hbox | 2 处，分别为 0.11 pt 和 1.95 pt，均小于 2 pt，符合既定 < 5 pt 容忍度 |
| Underfull \hbox | 多处，全部小于 5 pt |
| Font Warnings | 仅 `U/rsfs/m/n` 数学字体回退、`fancyhdr \headheight` 提示，均为历史非阻塞警告，不影响显示 |

---

## 8. v13 检查清单（按用户提示词第八节 19 条）

| # | 检查项 | 结果 |
|---|---|---|
| 1 | 第 3 章 5 张图均已切换为 v13 新图 | ✅ chapter3.tex 5 处 `\includegraphics` 全部指向 `_v13.pdf` |
| 2 | 图内无"图 3.x"硬编码 | ✅ 重绘脚本未写入图号 |
| 3 | 图内无英文顶部标题 | ✅ 全部去除 |
| 4 | 图形风格为黑白/灰阶正式论文风格 | ✅ |
| 5 | 无圆角卡片、阴影、渐变、大面积彩色填充 | ✅ |
| 6 | 第 3.7 正文不再出现"24 项"或"24 个独立断言" | ✅ grep 0 命中 |
| 7 | 表 4.3 仍无星级 | ✅ grep `\\star\|★` chapter4.tex → 0 命中 |
| 8 | 图 5.6 顶部英文标题仍已清除 | ✅ 沿用 v12 已重出的 `fig_granularity_curve.pdf` |
| 9 | 第 5.8/5.9 格式仍正常 | ✅ chapter5.tex 共 8 处 `\subsubsection*` 保留 |
| 10 | 目录与正文页码对应 | ✅ 二次 xelatex 后已稳定 |
| 11 | 图号、表号连续 | ✅ |
| 12 | 0 undefined citation/reference | ✅ |
| 13 | 0 BibTeX warning | ✅ |
| 14 | 无严重 Overfull | ✅ 仅 2 处 < 2 pt |
| 15 | 未修改实验数据 | ✅ `outputs/runs/` 完全未触碰 |
| 16 | 未提交 `check/*.pdf` | ✅ untracked，不在本轮 commit 内 |
| 17 | 未提交字体文件 | ✅ |
| 18 | 未提交 LaTeX 中间产物 | ✅ `.aux .bbl .blg .log .out .toc .lof .lot` 均在 `.gitignore` |
| 19 | v9/v10/v11/v12 历史 PDF 未删除、未覆盖 | ✅ 7 个历史 PDF 全部保留：v7 / v8 / v9 / v10_ch3_ch4ch5 / v11 / v12 / v13_figures |

---

## 9. 是否建议将 v13 发给导师

**建议直接发**。本轮处理的两件事——

1. 第 3 章 5 张系统设计图重绘为正式黑白线框风格；
2. §3.7 文本中去掉"24"字样；

——都是导师意见 #1 和 #2 在 v12 之后唯一仍可见的两处尾巴。修复后：

- 论文中所有自绘图都已脱离 matplotlib 默认风格的"AI 生成感"；
- 数据图（13 张）保持 v12 已统一的低饱和色板 + 无 banner 风格；
- 系统设计图（5 张）改为黑白线框正式风格；
- 数字与代码描述完全一致，没有"24/4"歧义。

唯一已知的视觉小问题：图 3.1 的反馈虚线水平段在生成层下边缘附近通过，与"Verilog Extractor"框右下角距离很近；图 3.4 的反馈虚线在"PASS"框的左外侧通过。这两处不影响图意，且都是有意为之以避开主要数据流箭头。导师如认为需要调整可在下一轮指示。

---

## 10. 文件清单

新增：

- `scripts/generate_thesis_ch3_figures_v13.py`（图生成脚本）
- `report/thesis/latex/figure/fig_system_architecture_v13.{pdf,png}`
- `report/thesis/latex/figure/fig_task_normalization_v13.{pdf,png}`
- `report/thesis/latex/figure/fig_llm_code_extraction_v13.{pdf,png}`
- `report/thesis/latex/figure/fig_feedback_loop_v13.{pdf,png}`
- `report/thesis/latex/figure/fig_feedback_decision_v13.{pdf,png}`
- `report/thesis/latex/thesis_supervisor_revision_v13_figures.pdf`（v13 论文快照）
- `report/thesis/supervisor_revision_v13_figures_report.md`（本文件）

修改：

- `report/thesis/latex/data/chapter3.tex`：5 处 `\includegraphics` 切到 v13；图 3.1 caption 重写；§3.7 去掉"24 个独立断言"
- `report/thesis/latex/main.pdf`：重新编译产物
- `notes/thesis_writing_plan.md`：追加 v13 状态记录
- `report/thesis/latex_migration_notes.md`：追加 v13 状态记录

未触碰：

- `outputs/runs/**`（实验数据）
- `report/thesis/latex/figure/fig_*_v1.pdf` / `fig_*_v2.pdf`（v12 旧图保留）
- 任何历史 PDF 快照
