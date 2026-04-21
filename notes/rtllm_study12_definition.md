# RTLLM_STUDY_12 正式研究子集定义

> 定义日期：2026-04-22
> 用途：后中期正式实验矩阵——论文与答辩的核心数据来源
> 前置要求：所有 12 题均来自兼容性审计中"可稳定仿真"的 41 题清单

---

## 题目清单

| # | 设计名 | 类别 | 难度 | 选择理由 |
|---|--------|------|------|---------|
| 1 | float_multi | Arithmetic/Other | ★★★★★ | IEEE 754 浮点乘法器，需理解指数/尾数拆分与规格化，是整个 RTLLM 最难的纯组合/算术题之一 |
| 2 | multi_booth_8bit | Arithmetic/Multiplier | ★★★★ | Booth 编码乘法器，涉及补码乘法算法，算法复杂度远超简单移位加 |
| 3 | multi_pipe_8bit | Arithmetic/Multiplier | ★★★★ | 流水线乘法器，需正确处理多级 pipeline 寄存器与时序 |
| 4 | div_16bit | Arithmetic/Divider | ★★★★ | 16 位迭代除法器，需实现移位-比较-减法循环算法 |
| 5 | adder_bcd | Arithmetic/Adder | ★★★ | BCD 加法器，需处理十进制进位修正（>9 加 6），编码逻辑非标准 |
| 6 | fsm | Control/FSM | ★★★ | Mealy 型序列检测器（10011），含循环检测与状态转移 |
| 7 | sequence_detector | Control/FSM | ★★★ | 另一种序列检测器，验证 FSM 类任务的泛化能力 |
| 8 | JC_counter | Control/Counter | ★★★ | Johnson 计数器，需理解反馈移位结构 |
| 9 | LIFObuffer | Memory/LIFO | ★★★ | 栈式存储结构，含读写指针、满/空判断逻辑 |
| 10 | LFSR | Memory/Shifter | ★★★ | 线性反馈移位寄存器，需正确选择反馈多项式 |
| 11 | traffic_light | Miscellaneous/Others | ★★★★ | 交通灯控制器，含多状态 FSM + 定时计数器 + 输出编码 |
| 12 | freq_divbyfrac | Miscellaneous/Freq divider | ★★★★ | 分频器（小数分频），需 dual-modulus 或 Σ-Δ 技术，是频率分频类最难的设计 |

---

## 覆盖分析

### 类别分布
| 类别 | 数量 | 代表题目 |
|------|------|---------|
| Arithmetic | 5 | float_multi, multi_booth_8bit, multi_pipe_8bit, div_16bit, adder_bcd |
| Control | 3 | fsm, sequence_detector, JC_counter |
| Memory | 2 | LIFObuffer, LFSR |
| Miscellaneous | 2 | traffic_light, freq_divbyfrac |

### 难度分布
| 难度 | 数量 | 占比 |
|------|------|------|
| ★★★★★ (Very Hard) | 1 | 8% |
| ★★★★ (Hard) | 5 | 42% |
| ★★★ (Medium) | 6 | 50% |

### 与 CORE_5 的对比

| 维度 | CORE_5 | STUDY_12 |
|------|--------|----------|
| 题目数 | 5 | 12 |
| Hard 题占比 | 2/5 (40%) | 6/12 (50%) |
| 类别覆盖 | 4 类 | 4 类（更均衡） |
| 最难题 | traffic_light (★★★★) | float_multi (★★★★★) |
| 用途 | Smoke / 流程验证 | **论文核心实验** |
| CORE_5 题纳入 | — | 保留 4/5（去掉 adder_8bit，太简单） |

---

## 预期 Feedback 价值分析

### 最可能体现 feedback 价值的题
1. **float_multi** — 极难，zero-shot 大概率失败，feedback 有充分修复空间
2. **traffic_light** — 复杂状态机，容易出微妙状态转移错误，feedback 可定向修复
3. **div_16bit** — 算法型任务，编译错误或仿真不匹配后，feedback 的错误定位非常精准
4. **multi_pipe_8bit** — 时序类错误（pipeline 延迟不对）是 feedback 擅长修复的场景

### 可能体现"强模型 zero-shot 已很强"的题
1. **fsm / sequence_detector** — FSM 是 LLM 的强项，强模型可能 zero-shot 即通过
2. **JC_counter / LFSR** — 经典结构，强模型训练数据中可能有大量类似代码
3. **adder_bcd** — BCD 加法逻辑相对固定

---

## 在脚本中使用

```bash
# 默认 Haiku
python scripts/run_rtllm_subset.py --subset study12

# 切换模型
python scripts/run_rtllm_subset.py --subset study12 --model claude-sonnet-4-6
python scripts/run_rtllm_subset.py --subset study12 --model gpt-5.4
```
