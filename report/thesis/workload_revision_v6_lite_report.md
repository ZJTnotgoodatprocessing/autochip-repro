# 工作量表述轻量修订 v6-lite 报告

> 日期：2026-05-09
> 基于 commit：`7a9f106` → 本轮修订
> PDF 路径：`report/thesis/latex/thesis_workload_revised_v6_lite.pdf`

---

## 1. 修订原因

v5 中第 3 章开头写"总代码量约2100行（不含测试和脚本）"，容易让评委误以为整个毕设工作量只有2100行代码。实际上2100行仅指核心系统逻辑，项目还包含：

- RTLLM 兼容性扫描脚本（`scan_rtllm_iverilog.py`）
- 正式实验运行脚本（`run_rtllm_subset.py`），支持消融、稳定性、粒度、多轮、策略等多种模式
- 结果图表整理（17张报告图 + 14张论文图）
- 数据审计、代码审计等质量保障工具

## 2. 修订策略

- **不虚报**：不编造代码量数字，不把第三方 benchmark / LaTeX 模板 / 字体 / PDF 算作代码量
- **不堆砌**：不新增复杂统计脚本或工作量统计章节
- **自然补充**：在已有段落中自然提及实验脚本和图表产物
- **不展示**：不把审计脚本、图表生成脚本、LaTeX 工程作为正文重点

## 3. 修改文件清单

| 文件 | 修改内容 |
|------|---------|
| `chapter3.tex` 开头 | "总代码量约2100行" → 拆分说明核心系统+实验脚本 |
| `chapter3.tex` §3.8 审计小节后 | 新增一句图表资产说明 |
| `chapter3.tex` 本章小结 | 同步提及实验脚本和图表整理 |
| `chapter1.tex` §1.4 工程贡献 | 新增一句配套脚本说明 |
| `chapter6.tex` §6.1 系统总结 | 新增一句配套工作说明 |
| `appendix.tex` 模块索引表 | 新增 `run_rtllm_subset.py` 和 `scan_rtllm_iverilog.py` |

## 4. 未修改项

- chapter5.tex：实验数据不变
- bibs.bib：参考文献不变（23条）
- 图 3.1/3.2：不变
- 封面/任务书：不变
- chapter2.tex/chapter4.tex：不变
- conclusion.tex：不变

## 5. 编译结果

| 项目 | 结果 |
|------|------|
| PDF 页数 | **57 页**（与 v5 相同） |
| Overfull hbox | **0** |
| Undefined citation | 0 |
| Undefined reference | 0 |
| BibTeX warnings | 0 |
| 参考文献 | 23 条 |
| 敏感信息 | 0 |
| check/*.pdf 提交 | 否 |

## 6. 实验数据验证

chapter5.tex 中 13 项关键数据行全部保持不变。

## 7. 真实项目资产统计（仅供参考，不写入正文）

| 类别 | 数量 |
|------|------|
| scripts/*.py 实验/工具脚本 | 20 个 |
| outputs/reports 下图表资产 | 17 个 |
| report/figures 下论文图表 | 14 个 |

## 8. 建议

v6-lite 为轻量修订，可直接发给导师查阅。如导师无进一步意见，可作为最终提交版本。
