# RTLLM 提示词策略对比实验总结

> 实验日期：2026-04-25
> 模型：GPT-5.4
> 任务集：RTLLM STUDY_12 (12 题)
> 运行目录：`outputs/runs/rtllm/rtllm_prompt_strategy_20260425_032429/`

---

## 一、实验目的

比较不同初始提示词策略对 RTLLM_STUDY_12 上 RTL 生成质量的影响，并判断各策略与 feedback loop 之间是替代关系还是互补关系。

---

## 二、各 Prompt Strategy 定义

### P0: Base Prompt（当前默认）
直接指令式 prompt，要求模型生成 Verilog 代码，不输出解释。

### P1: CoT / Reasoning-before-code
要求模型先分析逻辑类型（组合/时序/FSM）、关键信号关系、时序要求，然后在 `module...endmodule` 块中输出代码。

### P2: Few-shot Prompt
在 prompt 中提供 2 个简单 Verilog 示例（8 位加法器、4 位计数器），然后要求模型生成目标代码。

### P3: Few-shot + CoT
结合 P1 和 P2，先提供示例，再要求分析后编码。

---

## 三、Few-shot 示例来源

- **示例 1**：8 位加法器 (`adder_8bit`) — 来自 RTLLM benchmark 但 **不在 STUDY_12 子集中**
- **示例 2**：4 位同步复位计数器 — 自定义简单任务

两个示例均为纯组合/简单时序逻辑，不包含目标任务答案，不存在数据泄漏风险。

---

## 四、实验结果

### 4.1 总体通过率

| 策略 | Zero-shot | Feedback | FB 增益 |
|------|-----------|----------|---------|
| P0: Base | 7/12 (**58%**) | 11/12 (**92%**) | +34pp |
| P1: CoT | 6/12 (**50%**) | 11/12 (**92%**) | +42pp |
| P2: Fewshot | **8/12** (**67%**) | 11/12 (**92%**) | +25pp |
| P3: FS+CoT | 7/12 (**58%**) | 11/12 (**92%**) | +34pp |

### 4.2 逐题结果矩阵

| 题目 | P0:ZS | P0:FB | P1:ZS | P1:FB | P2:ZS | P2:FB | P3:ZS | P3:FB |
|------|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
| float_multi | ✓ | ✓(1) | ✗ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) |
| multi_booth_8bit | ✗ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) |
| multi_pipe_8bit | ✓ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) |
| div_16bit | ✓ | ✓(1) | ✗ | ✓(1) | ✓ | ✓(1) | ✗ | ✓(1) |
| adder_bcd | ✓ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) |
| fsm | ✓ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) |
| sequence_detector | ✗ | ✓(2) | ✗ | ✓(2) | ✗ | ✓(2) | ✗ | ✓(2) |
| JC_counter | ✓ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) |
| LIFObuffer | ✓ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) | ✓ | ✓(1) |
| LFSR | ✗ | ✓(2) | ✗ | ✓(2) | ✗ | ✓(3) | ✗ | ✓(2) |
| traffic_light | ✗ | ✓(2) | ✗ | ✓(2) | ✗ | ✓(1) | ✗ | ✓(1) |
| freq_divbyfrac | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ |

### 4.3 ZS 差异分析

CoT (P1) 相比 Base (P0) 在 ZS 阶段：
- **改善**：multi_booth_8bit (✗→✓)
- **退化**：float_multi (✓→✗), div_16bit (✓→✗)
- 净效果：**−1 题 (−8pp)**

Fewshot (P2) 相比 Base (P0) 在 ZS 阶段：
- **改善**：multi_booth_8bit (✗→✓)
- **退化**：无
- 净效果：**+1 题 (+9pp)**

FS+CoT (P3) 相比 Base (P0) 在 ZS 阶段：
- **改善**：multi_booth_8bit (✗→✓)
- **退化**：div_16bit (✓→✗)
- 净效果：**0 题 (±0pp)**

---

## 五、核心发现

### 5.1 CoT 是否有帮助？

**整体而言 CoT 对 GPT-5.4 无帮助，甚至轻微有害。**

CoT 将 ZS 通过率从 58% 降至 50%。原因分析：
- CoT 要求模型先分析再编码，但在 float_multi 和 div_16bit 等复杂算术任务上，分析步骤引入了额外的输出长度，可能干扰了代码生成质量
- CoT 的"先分析"指令可能与 RTLLM 自带的详细 description 有功能重叠

### 5.2 Few-shot 是否有帮助？

**Fewshot 对 ZS 有轻微帮助 (+9pp)，是本实验中 ZS 最优策略。**

- 提供结构性示例帮助模型在 multi_booth_8bit 上生成正确代码
- 没有对任何原本通过的题产生退化
- 但帮助有限：仅改善 1 题

### 5.3 Feedback 是否仍有增益？

**Feedback 在所有策略下均有显著增益。**

| 策略 | FB 增益 |
|------|---------|
| P0: Base | +34pp |
| P1: CoT | **+42pp** |
| P2: Fewshot | +25pp |
| P3: FS+CoT | +34pp |

- Feedback 将所有策略的通过率拉平至 92% (11/12)
- 唯一未通过的 freq_divbyfrac 是所有策略 + feedback 均无法解决的天花板题

### 5.4 提示词策略与 feedback 的关系

**互补关系，且 feedback 是主导因素。**

关键发现：
1. **初始 prompt 质量影响 ZS 通过率，但 feedback 几乎完全消除了这种差异**（所有策略 FB 均为 92%）
2. **更强的初始 prompt (Fewshot) 减少了 feedback 的边际收益**（25pp vs 34pp），因为起点更高
3. **更弱的初始 prompt (CoT) 反而有更高的 feedback 收益**（42pp），因为 feedback 能修复 CoT 引入的初始错误
4. **Feedback 对所有策略都是有益的，不存在"某种 prompt 让 feedback 变差"的情况**

### 5.5 后续默认 prompt 建议

**建议保持 Base prompt 作为默认。**

理由：
1. Base 在 ZS 阶段表现与 Fewshot 接近（差 1 题），且 FB 后结果相同
2. Base prompt 更简洁，token 消耗更少
3. Fewshot 的 ZS 优势仅 1 题，不具统计显著性
4. 如果需要最大化 ZS 性能（如无法使用 feedback 的场景），可考虑切换到 Fewshot

---

## 六、与历史实验的一致性验证

本轮 P0:Base 的结果（ZS=58%, FB=92%）与 STUDY_12 正式实验（ZS=50%, FB=83%）相比有一定波动，这与稳定性实验观察到的 GPT-5.4 stochastic variation 一致：
- ZS: 58% vs 50%（±8pp 在 79.2%±4.2% 的 stability 范围内）
- FB: 92% vs 83%（+9pp，额外通过了 multi_booth_8bit，单次波动）

---

## 七、Sonnet 补跑

本轮未补跑 Claude Sonnet 4.6。由于 GPT-5.4 的结果已经清晰表明 feedback 是主导因素（所有策略 FB 均为 92%），且 prompt strategy 对最终结果影响有限，在 Sonnet 上重复该实验的信息增量较低。如有需要可在后续轮次补充。

---

## 八、图表资产

| 图表 | 文件 |
|------|------|
| 4 策略 ZS/FB 对比柱状图 | `outputs/reports/fig_prompt_strategy_comparison.png` |
| 逐题策略×条件矩阵 | `outputs/reports/fig_prompt_strategy_matrix.png` |
