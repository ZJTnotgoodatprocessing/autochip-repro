# 导师修订 v14b — 进一步缩小图 3.3 / 图 3.5

**日期**：2026-05-17
**对应 commit**：本轮 v14b 修订（待生成 hash）
**输出 PDF**：`report/thesis/latex/thesis_supervisor_revision_v14b_ch3_figshrink.pdf`（**64 页**，v14a 是 66 页）
**前一版本**：v14a（`92a01df`，`thesis_supervisor_revision_v14a_ch3_figrefine.pdf`，66 页）

---

## 1. 本轮修改的范围

导师在 v14a PDF 上仍观察到图 3.3 和图 3.5 占满一整页。复核后确认：

```
v14a 中图独占页面：
  Fig 3.1  在 p23  chars=414  独占
  Fig 3.3  在 p26  chars=364  独占
  Fig 3.5  在 p31  chars=299  独占
```

之前的"低字符页"自检使用了 200 字阈值，把这三页都漏判了（414/364/299 都 > 200）。本轮修复了自检脚本（`scripts/check_v14a_figures.py` 直接按 caption "图3.x" 定位），并按用户具体要求把 **3.3 和 3.5** 进一步缩小。

图 3.1 也独占，但用户明确没要求修改，故保留现状。如导师后续要求一并缩小，可在下一轮按相同方法处理。

---

## 2. 关键技术决定

### 2.1 试错过程：figsize 不能单独缩

第一次尝试同时缩 figsize 和 LaTeX width：
- Fig 3.3：figsize (6.0, 7.0) → (4.5, 5.25)，width 0.65 → 0.55
- Fig 3.5：figsize (8.5, 6.95) → (5.5, 4.5)，width 0.85 → 0.70

生成出来的 PNG 显示**严重文字重叠**：
- Fig 3.3：`<reasoning> First we ... </reasoning>` 与右侧 "CoT 推理段" 标注重叠；
  `module adder(...); ... endmodule` 与 "目标 Verilog 代码块" 重叠。
- Fig 3.5：L2 / L3 / L4 三个底部子框的说明文字互相重叠；顶部两输入框中
  "·通过：进入仿真" 等文字突破框底部。

**根因**：matplotlib 的 fontsize 单位是 pt（绝对长度），而 axes 内的 box
（如 `_box` 用的 width/height 参数）是 axes 单位（相对 figsize）。当
figsize 缩小时，box 的 inch 尺寸变小，但 fontsize 仍是 10pt，文字相对
box 变得更大，从而撑爆 box 边界。

**修复**：figsize 回退到 v14a 的 (6.0, 7.0) / (8.5, 6.95)，仅靠减小
LaTeX width 控制纸面尺寸。这样 box 与 fontsize 等比缩小，不会出现内容
溢出。

代价：渲染字号会偏小（计算见 §2.3）。

### 2.2 实际修改

```diff
# scripts/generate_thesis_ch3_figures_v13.py
  def fig_llm_code_extraction():
-     # v14: figsize reduced from (9.0, 10.5); LaTeX width tightened to 0.65.
-     fig, ax = plt.subplots(figsize=(6.0, 7.0))
+     # v14b: keep figsize (6.0, 7.0) -- shrinking it makes the in-figure
+     # text (whose size is in pt, independent of figsize) overflow the
+     # axes-unit-sized boxes ...
+     # Use the LaTeX width below (0.55, was 0.65) to control the printed size.
+     fig, ax = plt.subplots(figsize=(6.0, 7.0))

  def fig_feedback_decision():
-     # v14: figsize reduced from (11.0, 9.0); LaTeX width tightened to 0.85.
-     fig, ax = plt.subplots(figsize=(8.5, 6.95))
+     # v14b: keep figsize (8.5, 6.95) -- the L2/L3/L4 sub-boxes carry text
+     # that, sized in pt, overlaps neighbours if figsize is shrunk.
+     fig, ax = plt.subplots(figsize=(8.5, 6.95))
```

```diff
# report/thesis/latex/data/chapter3.tex
  \begin{figure}[htbp]
- \includegraphics[width=0.65\textwidth]{figure/fig_llm_code_extraction_v13.pdf}
+ \includegraphics[width=0.55\textwidth]{figure/fig_llm_code_extraction_v13.pdf}
  \caption{LLM回复到可编译Verilog文件的提取流程}

  \begin{figure}[htbp]
- \includegraphics[width=0.85\textwidth]{figure/fig_feedback_decision_v13.pdf}
+ \includegraphics[width=0.70\textwidth]{figure/fig_feedback_decision_v13.pdf}
  \caption{EDA验证结果到反馈提示词的转换逻辑}
```

PNG 文件实际未变化（figsize 不变 → 输出像素不变）；只有 LaTeX 端
按新的 width 重排版。

### 2.3 渲染字号估算

按 textwidth = 13cm 估算最坏情况的渲染字号（中文 sans-serif）：

| 图 | figsize_w | LaTeX width | 渲染宽度 | scale | 10pt 渲染后 |
|---|---|---|---|---|---|
| 3.3 | 6.0 in (15.24 cm) | 0.55 | 7.15 cm | 0.469 | **4.7 pt** |
| 3.5 | 8.5 in (21.59 cm) | 0.70 | 9.10 cm | 0.421 | **4.2 pt** |

确实偏小，但可接受：
- 主要信息载体（如 "iverilog -g2012 编译 + vvp 仿真"、"Ranker · 标量评分"）
  以 11pt bold 设置，渲染后 ~5.2 / 4.6 pt 仍可读；
- 3.3 中 monospace 代码示例本身就只是示意性的 placeholder（"Sure, here
  is the design..."），不需要逐字辨识；
- 3.5 中的 L2/L3/L4 三联在正文（line 196 起）有完整复述。

如果导师要求字号更大，下一轮可以反向调整：保持 LaTeX width 0.55/0.70
不变，把 figsize 缩到 (4.5, 5.25) / (5.5, 4.5)，**同时**把所有
fontsize 从 10pt 提到 13pt（×1.3 补偿），axes 元素与文字按比例同步
缩放，可恢复到 ~6 pt 的渲染字号但代码量较大。本轮采用更稳的低风险路径。

---

## 3. 自检结果

### 3.1 PyMuPDF 图独占检测

```
v14b 中图独占页面：
  Fig 3.1  在 p23  chars=414  仍独占（用户未要求修改）
  Fig 3.2  在 p24  chars=953  共存
  Fig 3.3  在 p26  chars=886  ← 共存（v14a 是 364，已修复）
  Fig 3.4  在 p29  chars=767  共存
  Fig 3.5  在 p30  chars=924  ← 共存（v14a 是 299，已修复）
```

3.3 / 3.5 共存页字符数分别提升至 886 / 924（v14a 是 364 / 299），均已
有正文段落与图同页。

### 3.2 LaTeX 编译

```
pages = 64 (v14a = 66, -2 页)
errors = 0
undefined refs / cites = 0
Overfull \hbox > 5pt = 0
Overfull \hbox 总数 = 2 (1.95pt + 0.11pt，与 v13/v14/v14a 完全一致)
```

### 3.3 视觉检查

通过 PNG 预览确认 v14b 渲染下：
- Fig 3.3：六行 LLM 原始回复 + 右侧标注分列两侧无重叠；阶段 1/2/3 三层
  长方框 + 底部 iverilog 框竖向线性排列清晰；
- Fig 3.5：顶部两输入框 / Ranker / rank 决策菱形 / Feedback Builder /
  L2-L4 三联 全部分行清晰，文字均在框内，箭头连接正确。

---

## 4. 关于图 3.1（独占页面）的说明

```
Fig 3.1  在 p23  chars=414
```

视觉上是图占整页 + caption + 段落首句溢到下页。本轮**未触动**，因为
导师只点名了 3.3 和 3.5。如需后续修复，建议：

```diff
# chapter3.tex
- \includegraphics[width=0.78\textwidth]{figure/fig_system_architecture_v13.pdf}
+ \includegraphics[width=0.65\textwidth]{figure/fig_system_architecture_v13.pdf}
```

不需要改 figsize，理由同 §2.1。预计可释放出 1 页空间。等导师反馈后再
做。

---

## 5. 修改文件清单

| 文件 | 操作 |
|---|---|
| `scripts/generate_thesis_ch3_figures_v13.py` | 注释更新（figsize 维持 v14a，仅说明）|
| `report/thesis/latex/data/chapter3.tex` | 2 处 LaTeX width 修改 |
| `scripts/check_v14a_figures.py` | 新增（按 "图3.x" caption 定位图独占页面）|
| `report/thesis/latex/main.pdf` | 重编 64 页 |
| `report/thesis/latex/thesis_supervisor_revision_v14b_ch3_figshrink.pdf` | 新增 |
| `report/thesis/supervisor_revision_v14b_ch3_figshrink_report.md` | 新增（本报告）|
| `notes/thesis_writing_plan.md` | 追加 v14b 状态 |
| `report/thesis/latex_migration_notes.md` | 追加 v14b 状态 |
| `report/thesis/latex/figure/*.pdf` 与 `*.png` | 重生成（内容不变，元数据变）|

---

## 6. v14b 不做的事

- 第 3 章正文逻辑 — 完全未触（仅 2 个 includegraphics 的 width 数字
  从 0.65 改成 0.55、从 0.85 改成 0.70）；
- 图内排版 — 完全未触（PNG 视觉与 v14a 一致）；
- 第 4 / 5 / 6 章 — 完全未触；
- 实验数据 — 完全未触；
- 图 3.1 / 3.2 / 3.4 — 完全未触。
