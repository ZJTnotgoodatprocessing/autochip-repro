# AutoChip 定位表述修订报告

> 日期：2026-05-14
> 关联 PDF：`report/thesis/latex/thesis_supervisor_revision_v9.pdf`（58 页，覆盖更新）
> 上一版基线：HEAD `f92389d`

---

## 一、本轮导师意见

> 2.4.4 小节中第一句仍然是直接说"复现了 AutoChip"，让人感觉这个毕设就是把 AutoChip 复现了一下。应该是把 AutoChip 当成一个普通的相关工作，然后对比一下，AutoChip 应该是一个 most close related work 的身份。除了这一处表达，其它地方也要注意类似问题。

---

## 二、修改前的问题

修改前在 `report/thesis/latex/data/chapter2.tex` 中存在两处明显将 AutoChip 写成"本文系统的实现框架"或"本文复现对象"的表述：

1. **§2.4.4 首句**（line 74，旧）

   > 本文复现了 AutoChip 的核心闭环思想，并在以下维度进行了扩展和深化……

   将"复现 AutoChip"作为本文工作的主语和立论起点，容易让审阅者将本毕设理解为"对 AutoChip 的复现 + 小幅扩展"。

2. **§2.6 本文定位**（line 102，旧）

   > 本文的定位是：在 AutoChip 反馈闭环框架的基础上，构建一个可复现的实验平台……

   把 AutoChip 写成本文系统的"框架来源"，与论文实际定位（基于 EDA 工具反馈的 Verilog 生成与自动优化系统，AutoChip 仅为最接近的相关工作）不一致。

此外，章节引言（line 4，旧）将"AutoChip 方法论"与"Verilog 设计要素""LLM 代码生成机制"等技术基础并列为本章覆盖的主题，AutoChip 在章节大纲中权重过高。

---

## 三、§2.4.4 如何修改

### 3.1 标题改写

```diff
- \subsection{本文与AutoChip的关系}
+ \subsection{本文工作与最接近相关工作的关系}
```

### 3.2 首句重写

新版首句（line 74）：

> 在已有研究中，AutoChip 与本文最为接近：二者都关注如何利用 EDA 工具的编译与仿真反馈引导大语言模型修复 Verilog 代码。与 AutoChip 侧重于展示反馈闭环的可行性不同，本文面向 Verilog 代码生成与自动优化任务，构建了一个可复现的实验系统，并在此基础上从更难基准、多模型对比、反馈收益归因和反馈策略边界等维度展开进一步实验：在评估范围上，同时接入 VerilogEval 和 RTLLM 两个公开 benchmark；在模型覆盖上，使用 Haiku、Sonnet 4.6 和 GPT-5.4 三个不同能力层级的模型进行交叉验证；在实验方法上，设计了 retry-only 消融条件以定量分离多采样收益与反馈信息收益。

### 3.3 段尾追加定位说明

在 §2.4.4 末尾（line 76 段尾）追加一句明确 AutoChip 在本文中的角色：

> AutoChip 在本章及第 5 章中作为最接近的相关工作和对比对象出现，而非本文系统的实现框架。

---

## 四、§2.6 是否修改

是。重写 §2.6 "本文定位"段落（line 102），删除"在 AutoChip 反馈闭环框架的基础上"主语化表述。

新版定位句：

> 本文的定位是：面向 Verilog 代码生成与自动优化任务，构建一个由 EDA 编译与仿真反馈驱动的实验系统，并将 AutoChip 等反馈式代码修复工作作为最接近的相关工作进行对比。在更强模型和更高难度的 benchmark 上，本文系统地分析反馈循环的有效性及其影响因素。与上述相关工作相比，本文的特色在于：通过严格的消融实验设计分离反馈信息与多采样各自的贡献，通过多轮独立重复实验验证结论的统计稳定性，并在反馈粒度、多轮对话和提示词策略等维度对反馈机制的适用条件和边界进行系统验证。

同时调整了第 2 章引言（line 4）中关于"AutoChip 方法论"的措辞，改为"反馈闭环式 RTL 代码修复的相关工作（其中 AutoChip 是与本文最为接近的代表性工作）"，使章节大纲不再把 AutoChip 列为与"Verilog 设计要素"同级的独立技术基础。

---

## 五、全文搜索结果

执行命令：

```bash
grep -nP "复现.{0,3}AutoChip|AutoChip.{0,3}复现|AutoChip风格|AutoChip 风格|在AutoChip.{0,5}基础上|在 AutoChip.{0,5}基础上|AutoChip反馈闭环框架|AutoChip 反馈闭环框架|AutoChip框架|AutoChip 框架" -r report/thesis/latex
```

结果：**No results found**（修改后）。

修改前命中两处，均位于 `chapter2.tex`，已按上述方案改写。

第 5 章的 `本文并非停留在对已有闭环思路的复现` 一句保留——该句已经使用"已有闭环思路"的中性表述，并非将 AutoChip 写成本文复现对象。

---

## 六、AutoChip 当前保留位置与理由

| 位置 | 上下文 | 角色 | 是否合理 |
|------|--------|------|---------|
| `chapter1.tex` §1.2.2 | "AutoChip 等工作提出了利用 EDA 工具反馈驱动代码修复的方法" | 相关工作综述 | ✅ |
| `chapter2.tex` §2.3.3 | "这一闭环思想构成了 AutoChip 方法的基础" | 一般性闭环思想的具体实例 | ✅ |
| `chapter2.tex` §2.4.1 | "AutoChip 提出了一种基于 EDA 工具反馈的 Verilog 代码迭代修复方法" | 相关工作技术描述 | ✅ |
| `chapter2.tex` §2.4.2 | "AutoChip 采用的简洁反馈策略……" | 相关工作技术细节 | ✅ |
| `chapter2.tex` §2.4.4 | "AutoChip 与本文最为接近：二者都关注……" | **最接近相关工作** | ✅（本轮重写） |
| `chapter2.tex` §2.5.1 | "AutoChip 提出了反馈闭环范式" | 相关研究方向梳理 | ✅ |
| `chapter2.tex` §2.6 | "将 AutoChip 等反馈式代码修复工作作为最接近的相关工作进行对比" | 本文定位 | ✅（本轮重写） |
| `chapter3.tex` §3.5 | "评分规则借鉴了已有反馈循环研究 \cite{autochip} 的设计思路" | 单点设计借鉴 | ✅ |
| `chapter5.tex` §5.9 | "本文的反馈循环机制受到 AutoChip 等已有工作的启发……与 AutoChip 侧重于验证反馈循环的可行性不同……" | 第 5 章对比讨论 | ✅ |
| `bibs.bib` | `@inproceedings{autochip,...}` | 参考文献 | ✅ |
| `assign.tex` | "1. AutoChip 原论文" / 参考文献 \[1\] | 任务书原始资料 | ✅ |

参考文献 `\cite{autochip}` 和任务书原始资料中的 AutoChip 条目均保留，未删除任何引用。

---

## 七、PDF 编译结果

```
xelatex -interaction=nonstopmode main.tex
bibtex main
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

| 检查项 | 结果 |
|--------|------|
| 总页数 | **58 页**（与上一版 v9 一致） |
| Undefined citation | **0** |
| Undefined reference | **0** |
| Overfull \\hbox / \\vbox | **0** |
| BibTeX warning | **0** |
| 字体形状告警 | 仅有 `TU/TimesNewRoman(0)/b/n` 与 `TU/txtt/m/n` 两条字体形状替换信息（与 v9 同；MiKTeX 字体表行为，不影响排版） |

PDF 已覆盖至 `report/thesis/latex/thesis_supervisor_revision_v9.pdf`。

---

## 八、页数

58 页（与上一版 v9 完全一致；本次修改主要为 §2.4.4 和 §2.6 内容重写，篇幅基本相当）。

---

## 九、PDF 使用建议

建议继续使用 `report/thesis/latex/thesis_supervisor_revision_v9.pdf` 作为当前最新版本。本次修订仅针对 AutoChip 定位表述，未改动实验数据、参考文献、章节结构、图表和致谢，符合 v9 的总体定位。

如需在文件名上区分本次修订，可额外保留一份 `thesis_supervisor_revision_v9_autochip_fix.pdf`；若不区分，则直接以覆盖版作为最新版送审即可。

---

## 十、未做的事

- 未新增 / 重跑实验
- 未修改实验数据
- 未删除任何 AutoChip 参考文献
- 未把 AutoChip 从相关工作章节移除
- 未大改第 3、4、5、6 章
- 未改致谢
- 未提交 `check/` 目录或字体文件
