# Word 初稿 v1 整合说明

> 生成日期：2026-05-02
> 生成脚本：`scripts/gen_thesis_docx.py`

---

## 1. 文件信息

| 项目 | 值 |
|------|---|
| Word 初稿路径 | `report/thesis/thesis_draft_v1.docx` |
| 文件大小 | 1,446,401 bytes (~1.4 MB) |
| 使用模板 | 未直接使用模板文件（从空白文档生成，模板文件 `北航本科生论文模板.docx` 保持不变） |
| 总段落数 | 755 |

---

## 2. 已整合的章节和组件

| # | 组件 | 来源文件 | 状态 |
|---|------|---------|------|
| 1 | 封面页 | 脚本生成 | ✅ 含学校/学院/专业/学号/姓名/导师/题目 |
| 2 | 本人声明 | 脚本生成 | ✅ |
| 3 | 中文摘要 | `abstract_zh.md` | ✅ 含关键词 |
| 4 | 英文摘要 | `abstract_en.md` | ✅ 含 Key Words |
| 5 | 目录占位 | 脚本生成 | ⬜ 需在 Word 中手动生成 |
| 6 | 第 1 章 绪论 | `chapter1_introduction.md` | ✅ |
| 7 | 第 2 章 相关技术 | `chapter2_related_work.md` | ✅ |
| 8 | 第 3 章 系统设计 | `chapter3_system_design.md` | ✅ |
| 9 | 第 4 章 实验设计 | `chapter4_experiment_design.md` | ✅ |
| 10 | 第 5 章 实验结果 | `chapter5_results_analysis.md` | ✅ |
| 11 | 第 6 章 总结展望 | `chapter6_conclusion.md` | ✅ |
| 12 | 致谢 | `acknowledgements.md` | ✅ |
| 13 | 参考文献 | `references.md` | ✅ 含 TODO:verify 标记 |
| 14 | 附录 | `appendix_plan.md` | ✅ |

---

## 3. 图表插入情况

### 3.1 已成功插入的图（16 张）

| # | 图号 | 文件来源 |
|---|------|---------|
| 1 | 图 3.1 | `report/figures/fig_system_architecture.png` |
| 2 | 图 3.2 | `report/figures/fig_feedback_loop_flow.png` |
| 3 | 图 5.1 | `outputs/reports/haiku_pass_rate_bar.png` |
| 4 | 图 5.3 | `outputs/reports/fig_passrate_comparison.png` |
| 5 | 图 5.4 | `outputs/reports/fig_per_problem_matrix.png` |
| 6 | 图 5.5 | `outputs/reports/fig_feedback_gain.png` |
| 7 | 图 5.6 | `outputs/reports/fig_ablation_comparison.png` |
| 8 | 图 5.7 | `outputs/reports/fig_ablation_decomposition.png` |
| 9 | 图 5.8 | `outputs/reports/fig_stability_ablation.png` |
| 10 | 图 5.9 | `outputs/reports/fig_stability_formal.png` |
| 11 | 图 5.10 | `outputs/reports/fig_granularity_curve.png` |
| 12 | 图 5.11 | `outputs/reports/fig_granularity_matrix.png` |
| 13 | 图 5.12 | `outputs/reports/fig_multiturn_comparison_v2.png` |
| 14 | 图 5.13 | `outputs/reports/fig_multiturn_matrix_v2.png` |
| 15 | 图 5.14 | `outputs/reports/fig_prompt_strategy_comparison.png` |
| 16 | 图 5.15 | `outputs/reports/fig_prompt_strategy_matrix.png` |

### 3.2 仍为占位的图

**无** — 所有 16 张图均已成功插入。

### 3.3 废弃图确认

以下废弃图**未被插入**（符合预期）：
- `fig_multiturn_comparison.png` (v1 废弃)
- `fig_multiturn_matrix.png` (v1 废弃)

---

## 4. 参考文献 TODO 项

以下条目仍需人工核验：

| 编号 | 条目 | TODO |
|------|------|------|
| [4] | RTLLM 2.0 | 确认是 ICCAD 2024 还是 arXiv |
| [5] | RTLFixer | 确认作者、出处 |
| [6] | HDLDebugger | 确认作者、出处 |
| [7] | AIvril | 确认作者、出处 |
| [11] | HDLBits | 确认是否放入正式参考文献 |
| — | VeriAssist | 确认正文是否引用 |
| — | VerilogCoder | 确认正文是否引用 |
| — | IEEE 754 | 确认是否需要引用 |

---

## 5. 后续需要人工检查的格式问题

1. **封面格式**：当前为纯文本生成，需对照模板调整字体、间距、居中排列
2. **目录**：需在 Word 中手动插入自动目录
3. **页码**：需设置分节页码（前置部分罗马数字，正文阿拉伯数字）
4. **页眉**：需按模板要求设置
5. **字体**：正文字体需统一为模板要求（宋体/Times New Roman）
6. **标题样式**：Heading 1-4 已使用，但样式参数需按模板微调
7. **图表编号**：已有文本图号，需确认与实际图片对应
8. **图表题注格式**：需按模板要求调整居中、字号
9. **表格**：Markdown 表格以纯文本形式插入，需手动转为 Word 表格
10. **参考文献格式**：需统一为 GB/T 7714 或学校要求格式
11. **参考文献编号**：正文中的引用标注需补充
12. **附录代码块**：代码命令以纯文本插入，格式需调整

---

## 6. 重要提醒

- 原始模板文件 `北航本科生论文模板.docx` **未被修改**
- Multi-turn v1 废弃图**未被插入**
- 所有 `TODO: verify` 标记**已保留**在参考文献中
- 无敏感信息泄露（无 API key / base_url / token）
