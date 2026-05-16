# LaTeX 迁移工作记录

> 创建日期：2026-05-06
> 更新日期：2026-05-07
> 状态：PDF v2 已编译（题目修正+格式检查）

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

**当前状态：✅ MiKTeX 25.12 已安装，PDF v3 已编译。**

### 版本历史

| 版本 | 日期 | 页数 | 说明 |
|------|------|------|------|
| v1 | 2026-05-06 | 59 | 初始迁移版 |
| v2 | 2026-05-07 | 59 | 题目修正+格式检查 |
| v3 | 2026-05-07 | 54 | 结构优化+全文润色+封面修正 |
| v4 | 2026-05-08 | 54 | 定稿前专项小修 |
| final | 2026-05-08 | 54 | 最终候选版（基于v4+参考文献补充） |
| v5 | 2026-05-08 | 57 | 知网+导师意见修订：Ch2引用增强+Ch3扩充+降AIGC |
| v6-lite | 2026-05-09 | 57 | 工作量表述轻量修订：核心系统+实验脚本+图表产物 |
| v7 | 2026-05-11 | 58 | 导师意见修订：调整立论+Ch5文字增强+致谢重写 |
| v8 | 2026-05-13 | 59 | 导师意见修订：重组Ch3+重写Ch4+27条文献+降AIGC |
| v9 | 2026-05-13 | 58 | 精修：Sonnet分析+成本效率+降AIGC+图表小修 |
| v9（autochip-fix） | 2026-05-14 | 58 | AutoChip 定位表述修订：§2.4.4 首句重写 + §2.6 本文定位重写 + §2 引言措辞调整；AutoChip 改为最接近相关工作和对比对象。覆盖 `thesis_supervisor_revision_v9.pdf`，详见 `report/thesis/autochip_positioning_fix_report.md` |
| v10 | 2026-05-14 | 63 | 第 3 章扩充 + 第 4/5 章对齐：§3.3/§3.4/§3.6 各新增一段技术解释 + 一张中文图（图 3.3 任务归一化、图 3.4 LLM 代码提取、图 3.5 反馈决策）；§4.4 末尾新增"实验设计与结果章节对应关系"表；第 5 章开头改为承接第 4 章三层设计，§5.1/§5.3/§5.5/§5.8 各新增过渡句，§5.5/§5.7 加 LaTeX label，§5.10 重写小结按三层结构回扣；图脚本 `scripts/generate_thesis_ch3_figures.py` 已扩充，PDF + PNG 双输出；独立 PDF：`thesis_supervisor_revision_v10_ch3_ch4ch5.pdf`，**`thesis_supervisor_revision_v9.pdf` 保留为 AutoChip 定位修订后的 58 页快照，未被本轮覆盖**；详见 `report/thesis/supervisor_revision_v10_ch3_ch4ch5_report.md` |

### 编译命令

```bash
cd report/thesis/latex
xelatex main.tex
bibtex main
xelatex main.tex
xelatex main.tex
```

### v4 主要修改

1. 封面题目换行修复：插入 `\\` 防止"生成"被拆分
2. 附录命令修正：`run_rtllm_experiment.py` → `run_rtllm_subset.py`，参数改为真实 CLI
3. 多轮对话实验公平比较表述修正（ST k=1 vs MT k=1 为公平对比）
4. 任务书原始资料第1条改为"AutoChip原论文"
5. 所有实验数据保持不变
6. v1/v2/v3 均保留为历史版本

---

## 7. 后续 TODO

- [x] 用户安装 TeX Live / MiKTeX 后本地编译验证
- [x] 修复编译错误（bibs.bib 行内注释）
- [x] 附录内容完善（代码路径修正）
- [x] 任务书字段确认（答辩日期、起止时间、班级号）
- [ ] 表格格式微调（部分表格需要优化列宽）
- [ ] 图片大小和位置微调
- [ ] 参考文献 DOI/页码补全（RTLCoder 等）
- [ ] 行溢出警告修复（ch2、ch5 共 2 处）

---

## 8. v12 状态记录（2026-05-16）

- v12 PDF：`thesis_supervisor_revision_v12.pdf` 63 页 / 0.94 MB
- 基于 v11 (`086fcd2`) 落实导师 6 条意见
- 全部 13 张数据图（chapter 5 + 附录 B）+ 2 张流程图（图 3.1/3.2）已删除
  图内英文 banner，由 LaTeX `\caption{}` 提供图题
- 全部数据图增加 PDF 矢量输出；`\includegraphics` 切换 `.pdf` 引用
  （PDF 体积从 2.21 MB 降到 0.94 MB）
- 表 4.3 删除"难度"星级列，改为"设计特征与选入理由"
- 第 5.8 / 5.9 段首 `\noindent\textbf{...}` 与 `\paragraph{...}` 统一
  改为 `\subsubsection*{...}`（不入目录）
- "24 项自动化检查" → "4 项自动化检查"（chapter 3 §3.7、chapter 4 §4.6）
- 详细修订报告：`report/thesis/supervisor_revision_v12_report.md`
- 编译：xelatex 两次稳定通过；0 undefined ref/cite、0 BibTeX warning、0
  overfull/underfull
- 历史 v9 / v10 / v11 / v12 PDF 全部保留，未覆盖

---

## 9. v13 状态记录（2026-05-16，第 3 章流程图重绘）

- v13 PDF：`thesis_supervisor_revision_v13_figures.pdf` 64 页 / 0.95 MB
- 基线：v12 (`b36b081`)
- 第 3 章 5 张系统设计图（图 3.1–3.5）从 matplotlib `FancyBboxPatch`
  圆角多色卡片整体重绘为黑白直角线框风格，仅保留单一深蓝
  `#1F3A5F` 用于决策菱形和反馈虚线
- 新图文件：
  `figure/fig_system_architecture_v13.pdf`
  `figure/fig_task_normalization_v13.pdf`
  `figure/fig_llm_code_extraction_v13.pdf`
  `figure/fig_feedback_loop_v13.pdf`
  `figure/fig_feedback_decision_v13.pdf`
  （旧 v1 / v2 PDF 保留未删除，便于回溯历史）
- `chapter3.tex` 5 处 `\includegraphics` 全部切到 `_v13.pdf`，图 3.1
  caption 重写为不依赖颜色的描述
- `chapter3.tex` §3.7 删除"共 24 个独立断言"细节，仅保留"4 项核心
  检查"；LaTeX 正文 0 处 "24 项 / 24 个独立断言"
- 生成脚本：`scripts/generate_thesis_ch3_figures_v13.py`（可重复运行）
- 详细修订报告：`report/thesis/supervisor_revision_v13_figures_report.md`
- 编译：xelatex 两次稳定通过；0 undefined ref/cite；BibTeX 0 warning；
  Overfull 仅 2 处 < 2 pt
- 历史 v7 / v8 / v9 / v10 / v11 / v12 / v13 PDF 全部保留
