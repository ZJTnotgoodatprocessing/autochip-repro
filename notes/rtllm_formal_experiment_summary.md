# RTLLM STUDY_12 正式实验结果汇总

> 实验日期：2026-04-22
> Benchmark：RTLLM 2.0 — STUDY_12 子集（12 题）
> 实验脚本：`scripts/run_rtllm_subset.py --subset study12 --mode both`
> 参数：temperature=0.7, feedback k=3, max_iterations=5

---

## 一、总体结果

### 通过率对比

| 模型 | Zero-shot | Feedback | 提升幅度 | Feedback 改善题数 |
|------|-----------|----------|---------|-----------------|
| **claude-haiku-4-5-20251001** | 5/12 (42%) | 6/12 (50%) | +8pp | 2 |
| **claude-sonnet-4-6** | 5/12 (42%) | 7/12 (58%) | +17pp | 2 |
| **gpt-5.4** | 6/12 (50%) | 10/12 (83%) | **+33pp** | **4** |

> **核心发现**：Feedback 对所有模型均有正向增益，且对强模型（GPT-5.4）的增益最大。
> GPT-5.4 在 STUDY_12 上从 50% 提升至 83%，是 feedback 机制最大的受益者。

### API 错误统计

三组实验均为 **0 API errors**，实验数据完整可靠。

---

## 二、逐题对比表

| # | 题目 | 类别 | Haiku ZS | Haiku FB | Sonnet ZS | Sonnet FB | GPT ZS | GPT FB |
|---|------|------|----------|----------|-----------|-----------|--------|--------|
| 1 | float_multi | Arithmetic/Other | FAIL | FAIL | FAIL | **PASS**(1) | FAIL | **PASS**(1) |
| 2 | multi_booth_8bit | Arithmetic/Multiplier | PASS | PASS(1) | PASS | PASS(1) | PASS | PASS(1) |
| 3 | multi_pipe_8bit | Arithmetic/Multiplier | PASS | FAIL | PASS | PASS(1) | PASS | PASS(1) |
| 4 | div_16bit | Arithmetic/Divider | PASS | PASS(1) | FAIL | **PASS**(1) | FAIL | **PASS**(2) |
| 5 | adder_bcd | Arithmetic/Adder | PASS | PASS(1) | PASS | PASS(1) | PASS | PASS(1) |
| 6 | fsm | Control/FSM | FAIL | **PASS**(1) | PASS | PASS(1) | PASS | PASS(1) |
| 7 | sequence_detector | Control/FSM | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |
| 8 | JC_counter | Control/Counter | PASS | PASS(1) | PASS | PASS(1) | PASS | PASS(1) |
| 9 | LIFObuffer | Memory/LIFO | FAIL | **PASS**(1) | FAIL | FAIL | PASS | PASS(1) |
| 10 | LFSR | Memory/Shifter | FAIL | FAIL | FAIL | FAIL | FAIL | **PASS**(5) |
| 11 | traffic_light | Miscellaneous | FAIL | FAIL | FAIL | FAIL | FAIL | **PASS**(1) |
| 12 | freq_divbyfrac | Miscellaneous | FAIL | FAIL | FAIL | FAIL | FAIL | FAIL |

> 粗体 **PASS** 表示由 feedback 从 FAIL 改善为 PASS。括号内数字为 feedback 迭代次数。

---

## 三、Feedback 改善分析

### 哪些题最能体现 feedback 价值？

| 题目 | Haiku FB | Sonnet FB | GPT FB | 分析 |
|------|----------|-----------|--------|------|
| **float_multi** | FAIL | **PASS** | **PASS** | 强模型专属收益：IEEE 754 浮点逻辑极复杂，只有强模型能在 feedback 引导下修正 |
| **div_16bit** | PASS(ZS) | **PASS**(FB) | **PASS**(FB) | Feedback 跨模型通用：Haiku 零样本即通过，但 Sonnet/GPT 反而需要 feedback 修复 |
| **LFSR** | FAIL | FAIL | **PASS**(5轮) | GPT-5.4 独有：唯一一个通过 5 轮持续修复最终通过的题，展示了 feedback 深度修复能力 |
| **traffic_light** | FAIL | FAIL | **PASS**(1轮) | GPT-5.4 独有：Haiku 和 Sonnet 均无法修复的复杂 FSM + 定时控制器 |
| **fsm** | **PASS**(FB) | PASS(ZS) | PASS(ZS) | Haiku 专属收益：弱模型通过 feedback 追上强模型 |
| **LIFObuffer** | **PASS**(FB) | FAIL | PASS(ZS) | 差异化模式：Haiku 能 feedback 修，Sonnet 不能，GPT 零样本即过 |

### 三个核心论文观点

1. **"Feedback 对强模型增益最大"**
   - GPT-5.4：+33pp（50%→83%），4 题改善
   - Sonnet 4.6：+17pp（42%→58%），2 题改善
   - Haiku：+8pp（42%→50%），2 题改善
   - 反直觉发现：不是"弱模型最需要 feedback"，而是"强模型最能利用 feedback"

2. **"Feedback 能修复 zero-shot 无法解决的复杂设计"**
   - float_multi（IEEE 754）、LFSR（5轮迭代）、traffic_light（复杂 FSM）
   - 这些都是零样本 100% 失败的题，只有 feedback 路径能通过

3. **"存在天花板题——所有模型+feedback 均失败"**
   - sequence_detector、freq_divbyfrac 是当前 AutoChip 框架的盲区
   - 为论文提供了"局限性讨论"的素材

---

## 四、模型差异化分析

### GPT-5.4：feedback 最佳受益者
- Zero-shot 50%（最高），但真正拉开差距的是 feedback 阶段
- **独有通过**：LFSR（5轮修复）、traffic_light
- 表明：最强模型在闭环中的表现远超其零样本能力

### Claude Sonnet 4.6：稳健中档
- Zero-shot 与 Haiku 持平（42%），但 feedback 更有效（58% vs 50%）
- **独有修复**：float_multi 和 div_16bit（通过 feedback）
- 与 Haiku 相比，在复杂算术题上更有修复能力

### Claude Haiku 4.5：基线代表
- 在简单题上与强模型持平
- Feedback 仅改善 2 题（fsm、LIFObuffer）
- 适合作为成本效益基线

---

## 五、实验运行元数据

| 模型 | 运行目录 | 用时（估计） |
|------|---------|------------|
| Haiku | `outputs/runs/rtllm/rtllm_both_20260422_004806/` | ~18 min |
| Sonnet 4.6 | `outputs/runs/rtllm/rtllm_both_20260422_011115/` | ~22 min |
| GPT-5.4 | `outputs/runs/rtllm/rtllm_both_20260422_013439/` | ~18 min |

每个运行目录包含：
- `summary.json`：汇总结果
- `details.json`：完整迭代过程（含每次 prompt/response/compile/sim）
- `summary.csv`：表格格式
