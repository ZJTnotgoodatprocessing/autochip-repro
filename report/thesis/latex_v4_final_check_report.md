# LaTeX PDF v4 定稿前专项核查与小修报告

> 日期：2026-05-08
> PDF 版本：v4（定稿前专项小修）
> 文件路径：`report/thesis/latex/thesis_draft_latex_v4.pdf`

---

## 1. 本轮修订目标

对 v3 进行定稿前专项核查与小修，不大规模重写。重点修正封面题目换行、附录实验命令准确性、多轮对话实验公平比较表述，以及全文最终检查。

---

## 2. 封面题目换行修复

**问题**：v3 封面题目"生成"被自动断为"生/成"两行。

**修复**：在 `com_info.tex` 的 `\thesistitle` 中插入 `\\` 手动控制换行位置：

```diff
-{基于EDA工具反馈的LLM Verilog生成与自动优化}
+{基于EDA工具反馈的LLM Verilog\\ 生成与自动优化}
```

**验证**：编译通过（0 errors），`\\` 在 cls 的 `\centering` minipage 中产生居中换行。封面、中文摘要标题页、任务书标题均使用同一变量，换行位置一致且自然。

---

## 3. 附录实验命令核对与修正

**问题**：v3 附录使用了不存在的脚本 `run_rtllm_experiment.py` 和不存在的参数 `--problems STUDY_12`。

**核实**：通过 `ls scripts` 和 `grep` 确认真实脚本为 `run_rtllm_subset.py`，真实 CLI 参数包括：

| 参数 | 说明 |
|------|------|
| `--model` | 模型名称 |
| `--subset study12` | 预定义子集（hardcoded 12题） |
| `--mode` | `zero-shot`/`feedback`/`ablation`/`granularity`/`multiturn`/`prompt_strategy` |
| `--feedback-mode` | `succinct`/`compile_only`/`rich` |
| `--prompt-strategy` | `base`/`cot`/`few_shot`/`few_shot_cot` |
| `--feedback-k` | 候选数量（默认3） |
| `--feedback-iterations` | 最大迭代轮数（默认5） |

**修正**：将附录中所有命令改为使用 `run_rtllm_subset.py`，覆盖全部7种实验模式的典型命令模板。

---

## 4. 多轮对话实验表述修正

**问题**：v3 中 Sonnet 的 MT k=1 与 ST k=3 的 +33pp 比较存在不公平（候选数量不同）。

**修正**：将主结论改为控制候选数量的公平对比（ST k=1 vs MT k=1），两模型均为 +17pp。明确指出 MT k=1 vs ST k=3 的比较因候选数量不同仅可作为参考。表格数据未修改。

---

## 5. 任务书修正

- 第1条"AutoChip论文及开源代码"改为"AutoChip原论文"

---

## 6. 全文最终检查结果

### 异常字符/TODO

| 检查项 | 结果 |
|--------|------|
| TODO | 0（data/ 目录下） |
| `_ `（下划线+空格） | 0 |
| 敏感信息（sk-/api_key/base_url） | 0 |

### 正式题目一致性

- 中文题目：基于EDA工具反馈的LLM Verilog生成与自动优化 ✅
- 英文题目：LLM Verilog Generation and Automatic Optimization Based on EDA Tool Feedback ✅

### 封面和任务书信息

| 项目 | 值 | 状态 |
|------|-----|------|
| 学号 | 22373311 | ✅ |
| 学院 | 计算机学院 | ✅ |
| 专业 | 计算机科学与技术（无"专业"后缀） | ✅ |
| 姓名 | 张金涛 | ✅ |
| 指导教师 | 王锐 | ✅ |
| 班级 | 220611 | ✅ |
| 毕设时间 | 2025.12.29 ~ 2026.5.22 | ✅ |
| 答辩时间 | 2026年6月3日 | ✅ |
| 任务书参考资料 | 8条，均未溢出 | ✅ |
| 原始资料第1条 | "AutoChip原论文" | ✅ |

### 图表检查

| 检查项 | 结果 |
|--------|------|
| 图 3.1–3.2 存在且清晰 | ✅ |
| 图 5.1–5.14 存在且清晰 | ✅ |
| v1 废弃图未插入 | ✅ |
| 图题在图下、表题在表上 | ✅ |
| 表 4.1（RQ对应）和表 5.9（结论汇总）准确 | ✅ |

### 引用和参考文献

| 检查项 | 结果 |
|--------|------|
| 参考文献条数 | 17 |
| BibTeX 编译警告 | 0 |
| Undefined citation | 0 |
| `??` 未解析引用 | 0 |
| 废弃文献混入 | 无 |

**关于 `[S.l.: s.n.]`**：这是 BibTeX 在 `gbt7714` 国标样式下的标准输出，表示 "Sine loco: sine nomine"（拉丁语，意为"无出版地：无出版者"）。当 `.bib` 条目缺少 `address` 和 `publisher` 字段时，国标格式自动补充此标注。这是符合 GB/T 7714 参考文献著录规则的正常行为，不影响格式审查。

### 敏感信息

| 检查项 | 结果 |
|--------|------|
| sk- | 0 |
| api_key/API_KEY | 0 |
| base_url/BASE_URL | 0 |
| token/TOKEN/PAT | 0 |

---

## 7. 编译结果

| 项目 | 值 |
|------|-----|
| 编译命令 | xelatex → bibtex → xelatex → xelatex |
| PDF 页数 | **54 页** |
| PDF 大小 | ~1962 KB |
| Overfull hbox | 0.29pt × 1（英文摘要，不可见） |
| Undefined reference | 0 |
| Undefined citation | 0 |
| BibTeX warnings | 0 |
| TODO | 0 |
| 实验数据修改 | 无 |

---

## 8. 仍需用户人工确认的问题

| # | 问题 |
|---|------|
| 1 | 封面题目换行效果是否满意（建议打开 v4 PDF 检查封面） |
| 2 | 附录命令模板是否需要进一步调整 |
| 3 | 多轮对话公平比较表述是否准确 |
| 4 | 参考文献中的 [S.l.: s.n.] 是否需要补充出版信息消除 |
| 5 | 是否需要进一步微调后开始最终提交 |
