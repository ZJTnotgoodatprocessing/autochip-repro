# LaTeX 迁移工作记录

> 创建日期：2026-05-06
> 状态：LaTeX 源文件已完成，PDF 编译待用户环境

---

## 1. 模板解析

### 1.1 模板来源

- 目录：`北航毕业设计论文latex模板/`（工作区根目录，未纳入 Git）
- 模板类型：buaathesis.cls（北航学位论文 LaTeX 模板）

### 1.2 模板核心文件

| 文件 | 用途 |
|------|------|
| `sample-bachelor.tex` | 主入口文件（本科论文） |
| `buaathesis.cls` | 文档类定义 |
| `gbt7714.sty` + `.bst` | GB/T 7714 参考文献样式 |
| `data/com_info.tex` | 通用信息（学院/专业/标题/作者/导师） |
| `data/bachelor/bachelor_info.tex` | 本科专用信息（班级/学号） |
| `data/bachelor/assign.tex` | 任务书信息 |
| `data/abstract.tex` | 中英文摘要 |
| `data/chapter*.tex` | 正文章节 |
| `data/conclusion.tex` | 结论页 |
| `data/bachelor/acknowledgement.tex` | 致谢 |
| `data/reference.tex` | 参考文献引入 |
| `data/bibs.bib` | BibTeX 文献库 |
| `figure/buaa*.pdf` | 学校 logo |
| `font/` | 字体文件（SimSun/SimHei/STKaiti/STXingkai/TimesNewRoman） |

### 1.3 关键结论

1. **主入口文件**：`sample-bachelor.tex`（本项目命名为 `main.tex`）
2. **本科论文信息**：`data/com_info.tex` + `data/bachelor/bachelor_info.tex`
3. **摘要**：`data/abstract.tex`，使用 `\begin{cabstract}` / `\begin{eabstract}`
4. **正文章节**：通过 `\include{data/chapter*}` 引入
5. **致谢**：`data/bachelor/acknowledgement.tex`
6. **参考文献**：BibTeX 管理，`data/bibs.bib` + `gbt7714` 宏包
7. **附录**：`\appendix` 后 `\include{data/appendix*}`
8. **使用 BibTeX**（非手写 reference）
9. **推荐编译命令**：`xelatex → bibtex → xelatex → xelatex`

---

## 2. LaTeX 工程结构

```
report/thesis/latex/
├── main.tex                       # 主入口
├── buaathesis.cls                 # 文档类
├── gbt7714-author-year.bst        # 参考文献样式
├── gbt7714-numerical.bst          # 参考文献样式
├── gbt7714.sty                    # 参考文献宏包
├── data/
│   ├── com_info.tex               # 学院/专业/标题/作者/导师
│   ├── abstract.tex               # 中英文摘要
│   ├── chapter1.tex               # 第1章 绪论
│   ├── chapter2.tex               # 第2章 相关技术
│   ├── chapter3.tex               # 第3章 系统设计
│   ├── chapter4.tex               # 第4章 实验设计
│   ├── chapter5.tex               # 第5章 实验结果
│   ├── chapter6.tex               # 第6章 总结展望
│   ├── conclusion.tex             # 结论页
│   ├── reference.tex              # 参考文献引入
│   ├── appendix.tex               # 附录
│   ├── bibs.bib                   # BibTeX 文献库（17条已核验）
│   └── bachelor/
│       ├── bachelor_info.tex      # 学号/班级/日期
│       ├── assign.tex             # 任务书
│       └── acknowledgement.tex    # 致谢
├── figure/                        # 图片（16张项目图 + 3张学校logo）
│   ├── buaamark.pdf
│   ├── buaaname.pdf
│   ├── buaaname_ch.pdf
│   ├── fig_system_architecture.png
│   ├── fig_feedback_loop_flow.png
│   ├── haiku_pass_rate_bar.png
│   ├── fig_passrate_comparison.png
│   ├── fig_per_problem_matrix.png
│   ├── fig_feedback_gain.png
│   ├── fig_ablation_comparison.png
│   ├── fig_ablation_decomposition.png
│   ├── fig_stability_ablation.png
│   ├── fig_stability_formal.png
│   ├── fig_granularity_curve.png
│   ├── fig_granularity_matrix.png
│   ├── fig_multiturn_comparison_v2.png
│   ├── fig_multiturn_matrix_v2.png
│   ├── fig_prompt_strategy_comparison.png
│   └── fig_prompt_strategy_matrix.png
└── font/                          # 字体（本地使用，不提交 Git）
```

---

## 3. 迁移清单

| 源 Markdown | 目标 LaTeX | 状态 |
|-------------|-----------|------|
| abstract_zh.md | data/abstract.tex (cabstract) | ✅ 已迁移 |
| abstract_en.md | data/abstract.tex (eabstract) | ✅ 已迁移 |
| chapter1_introduction.md | data/chapter1.tex | ✅ 已迁移 |
| chapter2_related_work.md | data/chapter2.tex | ✅ 已迁移 |
| chapter3_system_design.md | data/chapter3.tex | ✅ 已迁移 |
| chapter4_experiment_design.md | data/chapter4.tex | ✅ 已迁移 |
| chapter5_results_analysis.md | data/chapter5.tex | ✅ 已迁移 |
| chapter6_conclusion.md | data/chapter6.tex | ✅ 已迁移 |
| acknowledgements.md | data/bachelor/acknowledgement.tex | ✅ 已迁移 |
| appendix_plan.md | data/appendix.tex | ✅ 已迁移（简化版） |
| references_verified.md | data/bibs.bib | ✅ 17条已核验 |

---

## 4. 图表插入状态

### 4.1 已插入的图（16张）

| 图编号 | 文件 | 章节 |
|--------|------|------|
| 图3.1 | fig_system_architecture.png | Ch3 §3.1 |
| 图3.2 | fig_feedback_loop_flow.png | Ch3 §3.5 |
| 图5.1 | haiku_pass_rate_bar.png | Ch5 §5.1 |
| 图5.2 | fig_passrate_comparison.png | Ch5 §5.2 |
| 图5.3 | fig_per_problem_matrix.png | Ch5 §5.2 |
| 图5.4 | fig_feedback_gain.png | Ch5 §5.2 |
| 图5.5 | fig_ablation_comparison.png | Ch5 §5.3 |
| 图5.6 | fig_ablation_decomposition.png | Ch5 §5.3 |
| 图5.7 | fig_stability_ablation.png | Ch5 §5.4 |
| 图5.8 | fig_stability_formal.png | Ch5 §5.4 |
| 图5.9 | fig_granularity_curve.png | Ch5 §5.5 |
| 图5.10 | fig_granularity_matrix.png | Ch5 §5.5 |
| 图5.11 | fig_multiturn_comparison_v2.png | Ch5 §5.6 |
| 图5.12 | fig_multiturn_matrix_v2.png | Ch5 §5.6 |
| 图5.13 | fig_prompt_strategy_comparison.png | Ch5 §5.7 |
| 图5.14 | fig_prompt_strategy_matrix.png | Ch5 §5.7 |

### 4.2 废弃图（未插入）

- ❌ fig_multiturn_comparison.png（v1 废弃）
- ❌ fig_multiturn_matrix.png（v1 废弃）

### 4.3 已插入的表格

- 表3.1 评分机制定义
- 表4.1 RTLLM审计结果
- 表4.2 STUDY_12任务组成
- 表4.3 模型配置
- 表5.1–5.8 各实验结果表

---

## 5. 审阅报告高优先级处理情况

| # | 问题 | 状态 |
|---|------|------|
| 1 | Ch5 §5.3.2 "49%" vs "57%" 语境说明 | ✅ 已在 LaTeX 中注明单轮结果与稳定性均值的区别 |
| 2 | Ch1 §1.3/§1.4 模板化编号列表 | ✅ 已改写为自然段落 |
| 3 | Ch6 §6.2 "结论X"机械格式 | ✅ 已改写为自然段 |
| 4 | Ch5 §5.3.3 "最有力的证据" | ✅ 已改为"直接证据" |
| 5 | 中文摘要过长段落 | ✅ 已拆分为多段 |

---

## 6. 编译状态

**当前状态：⚠️ 用户系统未安装 XeLaTeX，无法在当前环境编译。**

### 推荐编译方式

用户在本地安装 TeX Live 或 MiKTeX 后，执行：

```bash
cd report/thesis/latex
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

或使用 latexmk：

```bash
latexmk -xelatex main.tex
```

### 编译注意事项

1. 需要 XeLaTeX（因为使用中文字体）
2. 需要 `font/` 目录下的字体文件（SimSun.ttc, SimHei.ttf 等）
3. 字体文件已从模板复制到 `report/thesis/latex/font/`，但不提交 Git
4. 如果编译报字体找不到，需确认字体路径或安装系统字体

---

## 7. 后续 TODO

- [ ] 用户安装 TeX Live 后本地编译验证
- [ ] 修复可能的编译错误
- [ ] 表格格式微调（部分表格需要优化列宽）
- [ ] 图片大小和位置微调
- [ ] 附录内容完善
- [ ] 任务书字段确认（答辩日期等）
- [ ] 参考文献 DOI/页码补全（RTLCoder 等）
