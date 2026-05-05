# 正文参考文献引用位置计划

> 说明：本文件标注正文中应插入参考文献编号的位置。
> 编号对应 `references_verified.md` 中的 [1]–[17]。
> 用户在 Word 中手工统一插入上角标引用。

---

## 第 1 章 绪论

| 位置 | 句子主题 | 建议引用 |
|------|---------|---------|
| §1.2.1 首段 | LLM 辅助 RTL 代码生成研究 | [8] ChipGPT, [15] Thakur DATE 2023 |
| §1.2.1 | VerilogEval benchmark | [2] VerilogEval |
| §1.2.1 | RTLLM benchmark | [3] RTLLM |
| §1.2.2 首句 | AutoChip 方法 | [1] AutoChip |
| §1.2.2 | RTLFixer 编译修复 | [5] RTLFixer |
| §1.2.2 | HDLDebugger 检索增强调试 | [6] HDLDebugger |
| §1.2.3 | 现有工作不足 | 可引用 [1][2][3] 作为对比背景 |

---

## 第 2 章 相关技术与研究基础

| 位置 | 句子主题 | 建议引用 |
|------|---------|---------|
| §2.2.1 | LLM 代码生成基本机制 | [12] Brown (Few-shot) |
| §2.3.1 | Icarus Verilog 工具 | [13] Icarus Verilog |
| §2.4.1 | AutoChip 核心思想 | [1] AutoChip |
| §2.4.4 | 本文与 AutoChip 关系 | [1] AutoChip |
| §2.5.1 | VerilogEval 介绍 | [2] VerilogEval, [14] HDLBits |
| §2.5.1 | VerilogEval V2 | [16] Revisiting VerilogEval |
| §2.5.2 | RTLLM 介绍 | [3] RTLLM |
| §2.6.1 "LLM 直接生成 RTL" | 相关工作概述 | [8] ChipGPT, [4] RTLCoder, [15] Thakur |
| §2.6.1 "评估方法" | benchmark 标准化 | [2] VerilogEval, [3] RTLLM |
| §2.6.1 "EDA 反馈" | 反馈修复方向 | [1] AutoChip, [5] RTLFixer, [6] HDLDebugger |
| §2.6.1 "提示词工程" | CoT / Few-shot | [11] CoT, [12] GPT-3 |
| §2.6.1 "多轮交互" | 代理方法 | [9] VerilogCoder, [17] Chip-Chat |

---

## 第 3 章 系统设计与实现

| 位置 | 句子主题 | 建议引用 |
|------|---------|---------|
| §3.1 | AutoChip 风格闭环设计 | [1] AutoChip |
| §3.4 | Icarus Verilog 编译仿真 | [13] Icarus Verilog |
| §3.2.1 | VerilogEval 加载器 | [2] VerilogEval |
| §3.2.2 | RTLLM 加载器 | [3] RTLLM |
| §3.7 | CoT / Few-shot 策略 | [11] CoT, [12] GPT-3 |

---

## 第 4 章 实验设计

| 位置 | 句子主题 | 建议引用 |
|------|---------|---------|
| §4.2.1 | VerilogEval-Human 20 题 | [2] VerilogEval |
| §4.2.2 | RTLLM_STUDY_12 | [3] RTLLM |
| §4.4 | Zero-shot / Feedback 条件 | [1] AutoChip |
| §4.4.5 | CoT / Few-shot 策略定义 | [11] CoT, [12] GPT-3 |

---

## 第 5 章 实验结果与分析

| 位置 | 句子主题 | 建议引用 |
|------|---------|---------|
| §5.1 | VerilogEval 基线 | [2] VerilogEval |
| §5.2 | RTLLM 正式实验 | [3] RTLLM |
| §5.3 | 消融实验设计动机 | [1] AutoChip（对比原论文方法） |
| §5.7 | CoT / Few-shot 讨论 | [11] CoT |
| §5.9.1 | 综合讨论-有效性 | [1] AutoChip |
| §5.9.6 | 局限性讨论 | [3] RTLLM, [13] Icarus Verilog |

---

## 第 6 章 总结与展望

| 位置 | 句子主题 | 建议引用 |
|------|---------|---------|
| §6.4.4 | 检索增强方向 | [6] HDLDebugger (RAG) |
| §6.4.5 | 形式化验证 | 可选：添加 SymbiYosys 相关引用 |

---

## 中文摘要 / 英文摘要

摘要通常不插入引用编号。如学校要求，可在首次提到 AutoChip 或 VerilogEval 时加注。
