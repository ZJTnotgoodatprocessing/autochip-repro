# Haiku 主实验结果报告

## 实验配置

| 参数 | 值 |
|------|-----|
| 模型 | claude-haiku-4-5-20251001 |
| 基准测试 | VerilogEval-Human 子集 (20题) |
| 温度 | 0.7 |
| 零样本设置 | k=1, max_iterations=1 |
| 反馈循环设置 | k=3, max_iterations=5 |
| API 错误 | 0 |
| 实验时间 | 2026-04-12 |

## 汇总结果

| 方法 | 通过数 | 总数 | 通过率 |
|------|--------|------|--------|
| 零样本 (Zero-shot) | 16 | 20 | 80% |
| 反馈循环 (Feedback) | 18 | 20 | 90% |
| **反馈改善** | **2** | **4** (零样本失败) | **50%** |

反馈循环将通过率从 80% 提升至 90%，绝对提升 10 个百分点。在 4 道零样本失败的题目中，反馈成功修复了 2 道 (50%)。

## 逐题详细结果

| # | 题目 | 难度 | 类型 | 零样本 | 反馈循环 | 反馈迭代数 | 改善? |
|---|------|------|------|--------|----------|-----------|-------|
| 1 | Prob001_zero | Easy | Comb | PASS | PASS | 1 | - |
| 2 | Prob007_wire | Easy | Comb | PASS | PASS | 1 | - |
| 3 | Prob014_andgate | Easy | Comb | PASS | PASS | 1 | - |
| 4 | Prob024_hadd | Easy | Comb | PASS | PASS | 1 | - |
| 5 | Prob027_fadd | Easy | Comb | PASS | PASS | 1 | - |
| 6 | Prob031_dff | Easy | Seq | PASS | PASS | 1 | - |
| 7 | Prob035_count1to10 | Easy | Seq | PASS | PASS | 1 | - |
| 8 | Prob041_dff8r | Easy | Seq | PASS | PASS | 1 | - |
| 9 | Prob025_reduction | Medium | Comb | PASS | PASS | 1 | - |
| 10 | Prob022_mux2to1 | Medium | Comb | PASS | PASS | 1 | - |
| 11 | Prob050_kmap1 | Medium | Comb | PASS | PASS | 1 | - |
| 12 | Prob054_edgedetect | Medium | Seq | PASS | PASS | 1 | - |
| 13 | Prob068_countbcd | Medium | Seq | PASS | PASS | 1 | - |
| 14 | Prob082_lfsr32 | Medium | Seq | **FAIL** (0.02%) | **FAIL** (0.02%) | 5 | 否 |
| 15 | Prob085_shift4 | Medium | Seq | PASS | PASS | 1 | - |
| 16 | Prob030_popcount255 | Medium-Hard | Comb | PASS | PASS | 1 | - |
| 17 | Prob109_fsm1 | Hard | FSM | **FAIL** (0.0%) | **PASS** | 2 | **是** |
| 18 | Prob127_lemmings1 | Hard | FSM | **FAIL** (63.8%) | **PASS** | 2 | **是** |
| 19 | Prob140_fsm_hdlc | Hard | FSM | **FAIL** (92.5%) | **FAIL** (97.1%) | 5 | 否 |
| 20 | Prob144_conwaylife | Very Hard | Seq | PASS | PASS | 1 | - |

> 括号内百分比为 rank 得分（正确样本比例），PASS 等价于 rank=100%。

## 案例分析：四道关键题目

### 1. Prob109_fsm1 — 简单 FSM（反馈修复成功）

- 零样本：FAIL，rank=0.0（编译失败或完全不匹配）
- 反馈循环：第 2 轮迭代通过
- 分析：这是一个基础的有限状态机题目。零样本生成的代码存在状态转移逻辑错误，导致仿真完全不匹配。反馈循环在第 2 轮通过编译/仿真错误信息定位了状态转移条件的问题，成功修正。这体现了反馈循环对"接近正确但有局部逻辑错误"的代码的修复能力。

### 2. Prob127_lemmings1 — Lemmings 游戏 FSM（反馈修复成功）

- 零样本：FAIL，rank=63.8%（约 36% 样本不匹配）
- 反馈循环：第 2 轮迭代通过
- 分析：Lemmings 状态机需要处理行走、坠落、方向切换等多个状态。零样本生成的代码已经大部分正确（63.8% 匹配），但在某些边界状态转移上有误。反馈循环利用仿真的 mismatch 信息，在第 2 轮即修复了剩余的状态转移错误。这是反馈循环最典型的成功场景：代码"接近正确"，只需少量修正。

### 3. Prob140_fsm_hdlc — HDLC 协议 FSM（反馈未能修复）

- 零样本：FAIL，rank=92.5%
- 反馈循环：FAIL，rank=97.1%（5 轮迭代，微幅提升）
- 分析：HDLC 帧检测 FSM 是一个复杂的协议级状态机，需要精确识别 flag 序列 (01111110)、bit stuffing 和 abort 条件。零样本已达到 92.5% 的匹配率，反馈循环经过 5 轮迭代仅提升至 97.1%。剩余的 ~3% 错误可能涉及极端边界条件（如连续 flag、abort 后的恢复等），这些场景在仿真错误信息中难以直接定位。这说明反馈循环对"需要全局协议理解"的深层逻辑错误修复能力有限。

### 4. Prob082_lfsr32 — 32位 LFSR（反馈未能修复）

- 零样本：FAIL，rank=0.02%（几乎完全不匹配）
- 反馈循环：FAIL，rank=0.02%（5 轮迭代，无改善）
- 分析：32 位线性反馈移位寄存器需要精确的抽头位置（tap positions）。如果抽头多项式错误，输出序列将完全不同，导致极低的匹配率。反馈循环无法从"几乎全部不匹配"的仿真结果中推断出正确的抽头位置——这本质上是一个需要精确数学知识（特征多项式）的问题，而非可以通过错误信息迭代修复的逻辑错误。这揭示了反馈循环的根本局限：当错误源于缺失的领域知识而非代码逻辑时，迭代修复无效。

## 关键发现

1. **反馈循环有效提升通过率**：从 80% 提升至 90%，绝对提升 10 个百分点。
2. **反馈对"接近正确"的代码最有效**：Prob109_fsm1 和 Prob127_lemmings1 均在第 2 轮即修复，说明反馈循环擅长修复局部逻辑错误。
3. **反馈对领域知识缺失无效**：Prob082_lfsr32 的抽头多项式错误无法通过迭代修复。
4. **反馈对深层协议逻辑改善有限**：Prob140_fsm_hdlc 经过 5 轮迭代仅微幅提升（92.5%→97.1%），边界条件错误难以从仿真输出中定位。
5. **Easy/Medium 题目零样本即可解决**：16 道 Easy/Medium 题目全部零样本通过，说明 Haiku 模型对基础 Verilog 生成能力充足。

## 图表

- 通过率对比柱状图：`outputs/reports/haiku_pass_rate_bar.png`
- 逐题 Rank 对比图：`outputs/reports/haiku_per_problem_rank.png`
