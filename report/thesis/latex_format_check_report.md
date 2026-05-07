# LaTeX PDF v2 格式审查报告

> 审查日期：2026-05-07
> PDF 版本：v2（题目修正+格式检查）
> 文件路径：`report/thesis/latex/thesis_draft_latex_v2.pdf`

---

## 1. 本轮修改摘要

| 修改项 | 文件 | 内容 |
|--------|------|------|
| 正式题目（中文） | com_info.tex | → 基于EDA工具反馈的LLM Verilog生成与自动优化 |
| 正式题目（英文） | com_info.tex | → LLM Verilog Generation and Automatic Optimization Based on EDA Tool Feedback |
| 答辩日期 TODO | com_info.tex | → 2026年6月3日 |
| 毕设起止时间 | com_info.tex | → 2025.12.29 ~ 2026.5.22 |
| 班级号 | bachelor_info.tex | 223733 → 220611 |
| 关键词 | com_info.tex | 更新为匹配新题目 |
| Ch6 题目引用 | chapter6.tex | 更新为新题目 |
| 附录标题重复 | appendix.tex | "附录A：实验配置与运行命令" → "实验配置与运行命令" |
| 附录代码路径 | appendix.tex | 修正为真实路径（src/feedback/、src/runner/ 等） |
| 附录 TODO | appendix.tex | 已删除 |

---

## 2. 题目修改覆盖范围

### 已修改的位置

| 位置 | 旧题目 | 新题目 | 状态 |
|------|-------|-------|------|
| 封面（com_info.tex） | 基于大语言模型与EDA工具反馈的RTL代码自动生成与自修复研究 | 基于EDA工具反馈的LLM Verilog生成与自动优化 | ✅ |
| 英文题目（com_info.tex） | Automatic RTL Code Generation and Self-Repair... | LLM Verilog Generation and Automatic Optimization... | ✅ |
| Ch6 §6.1（chapter6.tex） | 围绕"基于大语言模型..." | 围绕"基于EDA工具反馈..." | ✅ |

### 验证：旧题目不再出现

```
grep "基于大语言模型与EDA" report/thesis/latex/data/ → 0 results ✅
grep "Self-Repair Based on Large Language" report/thesis/latex/ → 0 results ✅
```

### 保留的正文表述（不修改）

正文中以研究内容描述形式出现的"RTL自动生成""反馈修复""自修复"等术语按要求保留不变。

---

## 3. 编译信息

| 项目 | 值 |
|------|-----|
| 编译命令 | xelatex → bibtex → xelatex → xelatex |
| 编译工具 | MiKTeX 25.12 XeLaTeX |
| PDF 页数 | **59 页** |
| PDF 大小 | ~1965 KB |
| 编译错误 | 无 |
| 未定义引用 | 无 |
| 未定义 citation | 无 |

---

## 4. 封面与任务书检查

| 检查项 | 结果 |
|--------|------|
| 封面题目 | ✅ 基于EDA工具反馈的LLM Verilog生成与自动优化 |
| 学号 | ✅ 22373311 |
| 学院 | ✅ 计算机 |
| 专业 | ✅ 计算机科学与技术 |
| 学生姓名 | ✅ 张金涛 |
| 指导教师 | ✅ 王锐 |
| 班级 | ✅ 220611（已修正） |
| 毕设时间 | ✅ 2025.12.29 ~ 2026.5.22 |
| 答辩时间 | ✅ 2026年6月3日（已修正） |
| 任务书 TODO | ✅ 已清除 |
| 任务书参考文献 | ✅ 8 条，均可在一行内显示 |

---

## 5. 摘要与关键词检查

| 检查项 | 结果 |
|--------|------|
| 中文摘要 | ✅ 分段合理（5段） |
| 英文摘要 | ✅ 分段合理（4段） |
| 中文关键词 | ✅ 大语言模型；Verilog代码生成；EDA工具反馈；自动优化；RTLLM |
| 英文关键词 | ✅ Large Language Models; Verilog Generation; EDA Tool Feedback; Automatic Optimization; RTLLM |
| 乱码/异常符号 | ✅ 未发现 |

---

## 6. 目录检查

| 检查项 | 结果 |
|--------|------|
| 页码 | ✅ 正常 |
| 章节层级 | ✅ 合理 |
| 重复标题 | ✅ 已修正（附录"附录A：附录A..."已修正为"附录A 实验配置与运行命令"） |

---

## 7. 正文章节检查

| 章节 | 标题 | 状态 |
|------|------|------|
| 第1章 | 绪论 | ✅ |
| 第2章 | 相关技术与研究基础 | ✅ |
| 第3章 | 系统设计与实现 | ✅ |
| 第4章 | 实验设计 | ✅ |
| 第5章 | 实验结果与分析 | ✅ |
| 第6章 | 总结与展望 | ✅ |
| 结论 | 独立结论页 | ✅ |

- 章节编号连续 ✅
- 无模板示例残留 ✅
- 无 Markdown 残留符号 ✅
- 无未处理 TODO（LaTeX 源中仅 buaathesis.cls 内有模板自身 TODO） ✅

---

## 8. 图表检查

### 已插入的 16 张图

| 图 | 文件 | 状态 |
|----|------|------|
| 图3.1 系统架构 | fig_system_architecture.png | ✅ |
| 图3.2 反馈循环流程 | fig_feedback_loop_flow.png | ✅ |
| 图5.1 VerilogEval通过率 | haiku_pass_rate_bar.png | ✅ |
| 图5.2 RTLLM通过率对比 | fig_passrate_comparison.png | ✅ |
| 图5.3 逐题结果矩阵 | fig_per_problem_matrix.png | ✅ |
| 图5.4 Feedback增益 | fig_feedback_gain.png | ✅ |
| 图5.5 消融对比 | fig_ablation_comparison.png | ✅ |
| 图5.6 收益分解 | fig_ablation_decomposition.png | ✅ |
| 图5.7 稳定性消融 | fig_stability_ablation.png | ✅ |
| 图5.8 稳定性正式 | fig_stability_formal.png | ✅ |
| 图5.9 粒度曲线 | fig_granularity_curve.png | ✅ |
| 图5.10 粒度矩阵 | fig_granularity_matrix.png | ✅ |
| 图5.11 多轮对话v2 | fig_multiturn_comparison_v2.png | ✅ |
| 图5.12 多轮矩阵v2 | fig_multiturn_matrix_v2.png | ✅ |
| 图5.13 提示词策略 | fig_prompt_strategy_comparison.png | ✅ |
| 图5.14 策略矩阵 | fig_prompt_strategy_matrix.png | ✅ |

### 废弃图确认

- ❌ fig_multiturn_comparison.png（v1 废弃）— **未插入** ✅
- ❌ fig_multiturn_matrix.png（v1 废弃）— **未插入** ✅

---

## 9. 表格检查

| 检查项 | 结果 |
|--------|------|
| 三线表风格 | ✅ 使用 booktabs（\toprule/\midrule/\bottomrule） |
| 表题在表上方 | ✅ |
| 图题在图下方 | ✅ |
| 表4.2 难度星号 | ✅ 使用 $\star$ 符号显示正常 |
| 表5.6 脚注 | ✅ 使用 $^*$ 和表下注释 |

---

## 10. 参考文献检查

| 检查项 | 结果 |
|--------|------|
| 总数 | ✅ 17 条 |
| 未定义引用 `??` | ✅ 无 |
| BibTeX 错误 | ✅ 无（v1 的行内 TODO 注释已修复） |
| GB/T 7714 格式 | ✅ 使用 gbt7714-numerical.bst |
| 待核验候选文献 | ✅ 未混入 |

---

## 11. 附录检查

| 检查项 | 结果 |
|--------|------|
| 标题重复 | ✅ 已修正（"附录A：实验配置..." → "实验配置..."） |
| 代码路径正确性 | ✅ 已修正为真实路径 |
| 敏感信息 | ✅ 无 API key/token/base_url |
| TODO | ✅ 已清除 |

---

## 12. 敏感信息检查

```
grep "sk-" report/thesis/latex/ → 0 results ✅
grep "api_key" report/thesis/latex/ → 0 results ✅
grep "base_url" report/thesis/latex/ → 0 results ✅
```

**确认：无敏感信息。**

---

## 13. 编译警告汇总（非错误）

| 警告 | 说明 | 严重性 |
|------|------|--------|
| Font shape TU/TimesNewRoman(0)/b/n undefined | MiKTeX 字体替代 | 低（视觉影响小） |
| Overfull \hbox (3.6pt) ch2 L79-80 | 局部行溢出 | 低（可后续调整） |
| Overfull \hbox (5.0pt) ch5 L150 | 局部行溢出 | 低 |
| MiKTeX update warning | 安装后未检查更新 | 无影响 |

---

## 14. 仍需用户人工确认的问题

| # | 问题 | 建议 |
|---|------|------|
| 1 | 封面日期格式是否符合学校最新要求 | 请对照学校模板确认 |
| 2 | 任务书参考文献格式是否需要更详细 | 当前为简写，学校可能要求完整格式 |
| 3 | 行溢出警告（2处） | 可通过调整措辞或换行解决 |
| 4 | TimesNewRoman 粗体字体替代 | 如有严格字体要求需安装完整字体包 |
| 5 | 中图分类号 TP311 是否准确 | 请确认 |
| 6 | 单位代码 10006 是否正确 | 北航标准代码，请确认 |
