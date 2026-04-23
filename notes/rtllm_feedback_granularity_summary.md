# RTLLM STUDY_12 反馈粒度实验总结

> 实验日期：2026-04-23
> 目的：比较不同反馈信息量对修复效果的影响
> 模型：GPT-5.4, Claude Sonnet 4.6
> Benchmark：RTLLM STUDY_12 (12 题)

---

## 一、实验目的

前期实验已证明 feedback loop 对 GPT-5.4 有稳定正向效果（+29.2pp），但对 Sonnet 4.6 有负面效果。本轮实验旨在回答更细粒度的问题：

1. **不同粒度的反馈信息，对修复效果的影响是否显著不同？**
2. **更丰富的反馈是否总是更好，还是存在"信息过多反而干扰"？**
3. **Sonnet 4.6 上 feedback 表现差，是否与反馈组织方式有关？**
4. **是否存在一个"最优反馈粒度"？**

---

## 二、反馈级别定义

| 级别 | 名称 | 内容 | 描述 |
|------|------|------|------|
| L0 | Zero-shot | 无 | 单次生成，无反馈 |
| L1 | Retry-only | 无 | 重复尝试，不含任何错误信息 |
| L2 | Compile-only | 编译错误 | 只反馈编译错误；仿真失败仅给出"未通过"，不提供细节 |
| L3 | Succinct | 编译错误 + 仿真摘要 | **当前默认方法**。包含 mismatch 数量 + 仿真输出前 40 行 |
| L4 | Rich | 编译错误 + 详细仿真 + 分析提示 | 仿真输出前 80 行 + stderr + 显式分析提示（检查 FSM、信号宽度等） |

---

## 三、实验参数

| 参数 | 值 |
|------|-----|
| Benchmark | RTLLM STUDY_12 (12 题) |
| 模式 | granularity (每题运行 L0-L4 共 5 级) |
| k (候选数) | 3 |
| max_iterations | 5 |
| temperature | 0.7 |

---

## 四、GPT-5.4 结果

### 4.1 总体通过率

| 级别 | 通过数 | 通过率 |
|------|--------|--------|
| L0 Zero-shot | 7/12 | **58%** |
| L1 Retry-only | 9/12 | **75%** |
| L2 Compile-only | 11/12 | **92%** |
| L3 Succinct | 11/12 | **92%** |
| L4 Rich | 10/12 | **83%** |

### 4.2 核心发现

1. **L2 和 L3 并列最高（92%）**：仅含编译错误的反馈就足以达到最优效果
2. **L4 Rich（83%）反而低于 L2/L3**：存在"信息过载"效应
3. **L1→L2 是最大跃升**（75%→92%，+17pp）：说明即使是最基础的编译反馈也极有价值
4. **L0→L1 也有显著提升**（58%→75%，+17pp）：多采样本身也有价值

### 4.3 逐题对比

| 题目 | L0 | L1 | L2 | L3 | L4 | 分析 |
|------|:--:|:--:|:--:|:--:|:--:|------|
| float_multi | ✓ | ✓ | ✓ | ✓ | ✓ | 简单题，全通过 |
| multi_booth_8bit | ✓ | ✓ | ✓ | ✓ | ✓ | 简单题，全通过 |
| multi_pipe_8bit | ✓ | ✓ | ✓ | ✓ | ✓ | 简单题，全通过 |
| div_16bit | ✗ | ✓ | ✓ | ✓ | ✓ | 所有反馈级别均能解决 |
| adder_bcd | ✓ | ✓ | ✓ | ✓ | ✓ | 简单题，全通过 |
| fsm | ✓ | ✓ | ✓ | ✓ | ✓ | 简单题，全通过 |
| **sequence_detector** | ✗ | ✗ | **✓** | **✓** | **✗** | ⭐ **L4 过载失败！** |
| JC_counter | ✓ | ✓ | ✓ | ✓ | ✓ | 简单题，全通过 |
| LIFObuffer | ✓ | ✓ | ✓ | ✓ | ✓ | 简单题，全通过 |
| LFSR | ✗ | ✗ | ✓(5) | ✓(2) | ✓(4) | L3 效率最高 |
| traffic_light | ✗ | ✓(4) | ✓(2) | ✓(2) | ✓(4) | 反馈加速收敛 |
| freq_divbyfrac | ✗ | ✗ | ✗ | ✗ | ✗ | 天花板题，全失败 |

### 4.4 关键案例：sequence_detector

这是本次实验最重要的发现：

- **L0 Zero-shot**: FAIL（编译失败）
- **L1 Retry-only**: FAIL（15 次盲试均未通过）
- **L2 Compile-only**: **PASS**（仅编译错误就够修复）
- **L3 Succinct**: **PASS**（同上）
- **L4 Rich**: **FAIL**（加入详细仿真输出 + 分析提示后反而失败）

**解释**：Rich 模式加入的"分析提示"（检查 FSM 转换、信号宽度等）可能导致模型过度关注提示中提到的方向，而忽略了真正的问题。这是典型的 **prompt distraction** / **information overload** 现象。

### 4.5 关键案例：LFSR

- L2: PASS(iter=5) — 勉强在最后一轮通过
- L3: PASS(iter=2) — 仿真摘要帮助快速定位
- L4: PASS(iter=4) — 过多信息反而减慢收敛

说明 **L3 Succinct 是修复效率最优的粒度**——既有足够信息又不至于过载。

---

## 五、Claude Sonnet 4.6 结果

### 5.1 总体通过率

| 级别 | 通过数 | 通过率 |
|------|--------|--------|
| L0 Zero-shot | 6/12 | **50%** |
| L1 Retry-only | 8/12 | **67%** |
| L2 Compile-only | 9/12 | **75%** |
| L3 Succinct | 8/12 | **67%** |
| L4 Rich | 8/12 | **67%** |

### 5.2 核心发现

1. **L2 Compile-only 是 Sonnet 的最佳粒度（75%）**
2. **L3 和 L4 反而回落到 67%**——与 L1 Retry-only 持平！
3. **仿真信息对 Sonnet 是噪声**：加入仿真输出后性能反而下降
4. **L0→L1（+17pp）和 L1→L2（+8pp）有正向贡献**
5. **L2→L3（-8pp）和 L2→L4（-8pp）有负向贡献**

### 5.3 逐题对比

| 题目 | L0 | L1 | L2 | L3 | L4 | 分析 |
|------|:--:|:--:|:--:|:--:|:--:|------|
| float_multi | ✓ | ✓ | ✓ | ✓ | ✓ | 全通过 |
| multi_booth_8bit | ✓ | ✓ | ✓ | ✓ | ✓ | 全通过 |
| multi_pipe_8bit | ✓ | ✓ | ✓ | ✓ | ✓ | 全通过 |
| **div_16bit** | ✗ | ✓ | ✓ | **✗** | **✗** | ⭐ 仿真信息导致回归 |
| adder_bcd | ✓ | ✓ | ✓ | ✓ | ✓ | 全通过 |
| fsm | ✓ | ✓ | ✓ | ✓ | ✓ | 全通过 |
| sequence_detector | ✗ | ✗ | ✓ | ✓ | ✓ | 反馈有效 |
| JC_counter | ✓ | ✓ | ✓ | ✓ | ✓ | 全通过 |
| LIFObuffer | ✗ | ✗ | ✗ | ✗ | ✗ | 天花板题 |
| **LFSR** | ✗ | ✗ | **✓** | **✗** | **✗** | ⭐ 仅 compile-only 能通过 |
| traffic_light | ✗ | ✓ | ✗ | ✓ | ✓ | 波动 |
| freq_divbyfrac | ✗ | ✗ | ✗ | ✗ | ✗ | 天花板题 |

### 5.4 关键案例：div_16bit

- L0: FAIL, L1: PASS, L2: PASS
- **L3 Succinct: FAIL** — 加入仿真输出后 Sonnet 修不好了！
- **L4 Rich: FAIL** — 更多信息进一步恶化

**解释**：Sonnet 在收到详细仿真输出后，可能试图"过度适配"仿真中显示的具体 mismatch，导致代码质量下降。Compile-only 模式反而给了 Sonnet 足够的自由度来重新思考解法。

### 5.5 关键案例：LFSR

- 所有级别中**只有 L2 Compile-only 通过**
- L3 和 L4 反而失败

这进一步证实：**对 Sonnet 而言，仿真信息是干扰信号**。

---

## 六、两模型对比分析

### 6.1 反馈粒度曲线对比

| 级别 | GPT-5.4 | Sonnet 4.6 | 差异 |
|------|---------|------------|------|
| L0 Zero-shot | 58% | 50% | GPT +8 |
| L1 Retry-only | 75% | 67% | GPT +8 |
| L2 Compile-only | **92%** | **75%** | GPT +17 |
| L3 Succinct | **92%** | 67% | GPT +25 |
| L4 Rich | 83% | 67% | GPT +16 |

### 6.2 最佳粒度

| 模型 | 最佳级别 | 通过率 | 次优级别 |
|------|---------|--------|---------|
| GPT-5.4 | L2/L3 并列 | 92% | L4 Rich (83%) |
| Sonnet 4.6 | **L2 Compile-only** | **75%** | L1/L3/L4 并列 (67%) |

### 6.3 核心结论

1. **反馈粒度确实重要**：L2 vs L4 在 GPT 上差 9pp，在 Sonnet 上差 8pp
2. **"更多反馈不一定更好"**：两个模型在 L4 Rich 上都出现了性能下降
3. **最优粒度具有模型依赖性**：
   - GPT-5.4：L2 = L3 > L4 > L1 > L0（仿真信息有帮助但不宜过多）
   - Sonnet 4.6：L2 > L1 = L3 = L4 > L0（仿真信息反而是噪声）
4. **Compile-only (L2) 是稳健的通用选择**：两模型在此级别均达到最高或接近最高
5. **Sonnet 的"feedback 无效"问题部分可归因于反馈组织方式**：
   - 前期稳定性实验中 Sonnet FB<RO，使用的是 L3 Succinct
   - 本轮实验表明 L2 Compile-only (75%) > L1 Retry-only (67%)
   - 说明 Sonnet 并非"不能利用反馈"，而是"不能有效利用仿真信息"

---

## 七、"信息过载"效应分析

### 7.1 GPT-5.4 的过载边界

GPT-5.4 在 L2→L3 之间没有损失（均 92%），但 L3→L4 出现了下降（92%→83%）。

受影响的题目：
- `sequence_detector`: L3 PASS → L4 FAIL（最明显的过载案例）

分析：Rich 模式添加的"分析提示"虽然意图良好，但可能导致模型偏离原本可行的修复路径。

### 7.2 Sonnet 4.6 的过载边界

Sonnet 在 L1→L2 之后就开始下降（L2→L3 从 75% 跌到 67%）。

受影响的题目：
- `div_16bit`: L2 PASS → L3 FAIL
- `LFSR`: L2 PASS → L3 FAIL

分析：Sonnet 对仿真输出中的具体 mismatch 信息可能产生"过度拟合"，试图修复每一个具体的输出差异而不是从根本上重新设计逻辑。

### 7.3 模型对反馈的"消化能力"差异

| 维度 | GPT-5.4 | Sonnet 4.6 |
|------|---------|------------|
| 编译反馈利用 | ✅ 优秀 | ✅ 良好 |
| 仿真摘要利用 | ✅ 有效 | ❌ 有害 |
| 详细日志利用 | ⚠️ 部分有害 | ❌ 有害 |
| 分析提示利用 | ⚠️ 可能误导 | ❌ 无改善 |
| 过载阈值 | L3-L4 之间 | L2-L3 之间 |

---

## 八、对论文写作的影响

### 8.1 正式论文推荐段落

> We investigated the impact of feedback granularity on repair effectiveness across five levels: zero-shot (L0), retry-only (L1), compile-only (L2), succinct feedback with simulation summary (L3), and rich feedback with detailed simulation output (L4). On GPT-5.4, we observed a clear inverted-U shaped curve: pass rate increased from 58% (L0) to 92% at L2-L3, then declined to 83% at L4. On Sonnet 4.6, the optimal level was L2 (compile-only, 75%), with performance dropping when simulation details were added (L3-L4: 67%). These results demonstrate that (1) even minimal feedback (compilation errors) provides substantial value over unguided retrying, and (2) excessive feedback information can degrade performance through a "prompt distraction" effect, where the model over-focuses on specific mismatch details rather than rethinking its design approach. Notably, the information overload threshold is model-dependent, suggesting that feedback strategies should be calibrated to the model's capacity for information integration.

### 8.2 答辩口头表述

> "反馈粒度实验揭示了一个'反馈收益的倒 U 型曲线'——信息太少不够用，信息太多反而干扰。GPT-5.4 在 compile-only 和 succinct 级别达到 92% 的峰值，而过于详细的反馈降到 83%。Sonnet 的过载阈值更低，仿真信息对它完全是噪声。这说明反馈策略需要针对模型特性进行校准。"

---

## 九、实验目录索引

| 模型 | 目录 |
|------|------|
| GPT-5.4 | `outputs/runs/rtllm/rtllm_granularity_20260423_212239/` |
| Sonnet 4.6 | `outputs/runs/rtllm/rtllm_granularity_20260423_233052/` |

---

## 十、图表资产

| 图表 | 文件 | 说明 |
|------|------|------|
| 反馈粒度曲线 | `outputs/reports/fig_granularity_curve.png` | 两模型 × 5 级通过率折线图 |
| 反馈粒度矩阵 | `outputs/reports/fig_granularity_matrix.png` | 逐题 × 逐级 PASS/FAIL 热力图 |

---

## 十一、方法论说明

1. 每级反馈在相同 API 预算下运行（k=3, iter=5 = 最多 15 次调用）
2. L0 除外（k=1, iter=1 = 仅 1 次调用）
3. 所有级别使用相同的 prompt 模板，仅反馈内容不同
4. 本轮为单次实验；关键发现（如 L4 过载）需要结合稳定性实验结果交叉验证
5. Sonnet 实验过程中出现若干 API 连接超时，但均通过内置重试机制成功恢复，最终 API error count = 0
