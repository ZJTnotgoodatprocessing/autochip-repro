# Multi-turn 实验子集定义

> 创建日期：2026-04-24
> 目标：验证 multi-turn 对话反馈 vs single-turn 反馈的效果差异

---

## 一、子集名单（6 题）

| # | 题目 | 类别 | 选择理由 | 希望验证的现象 |
|---|------|------|----------|----------------|
| 1 | `div_16bit` | Arithmetic/Divider | Sonnet 在 L3/L4 退化（L2:PASS → L3:FAIL） | multi-turn 是否能帮 Sonnet 正确利用仿真信息 |
| 2 | `sequence_detector` | Control/FSM | GPT 在 L4 退化（L3:PASS → L4:FAIL），Sonnet 在 L2/L3 才通过 | multi-turn 是否缓解信息过载 |
| 3 | `LFSR` | Memory/Shifter | Sonnet 仅 compile-only 通过（L2:PASS, L3/L4:FAIL） | multi-turn 是否改善 Sonnet 对仿真反馈的消化 |
| 4 | `traffic_light` | Misc/Others | GPT 所有反馈级别均通过（但需 2-4 轮），Sonnet 波动 | multi-turn 是否加速收敛 |
| 5 | `freq_divbyfrac` | Misc/Freq divider | 两模型在所有条件下均失败（天花板题） | multi-turn 是否能突破天花板 |
| 6 | `fsm` | Control/FSM | 两模型在所有条件下均通过（简单题） | 作为 sanity check 基线 |

---

## 二、选题逻辑

### 类型 1：Sonnet 反馈退化题（div_16bit, LFSR）

这两道题 Sonnet 在 compile-only (L2) 下能通过，但加入仿真信息后反而失败。
如果 multi-turn 能在这两题上让 Sonnet 通过，说明问题不是"仿真信息本身"，
而是 single-turn 的信息组织方式无法让 Sonnet 正确消化反馈。

### 类型 2：信息过载敏感题（sequence_detector）

GPT-5.4 在 Rich (L4) 下此题失败，但 Succinct (L3) 下通过。
multi-turn 可能通过分步引导（先给编译反馈，再给仿真反馈）来缓解过载。

### 类型 3：需要多轮修复的复杂题（traffic_light）

此题在 single-turn 下需要 2-4 个 iteration 才能通过。
multi-turn 的持续对话上下文可能让修复更高效。

### 类型 4：天花板题（freq_divbyfrac）

两模型在所有条件下均失败。如果 multi-turn 能突破，说明其价值极大；
如果仍然失败，说明这是模型能力上限而非反馈方式的问题。

### 类型 5：基线确认题（fsm）

简单题，所有条件均通过。确保 multi-turn 实现没有 bug。

---

## 三、对比实验矩阵

| 模型 | 条件 A: Single-turn (L3) | 条件 B: Multi-turn | 条件 C: Compile-only (L2) |
|------|--------------------------|--------------------|----|
| GPT-5.4 | ✅ | ✅ | ✅ |
| Sonnet 4.6 | ✅ | ✅ | ✅ |

每个条件统一参数：k=3, max_iterations=5, temperature=0.7

---

## 四、Multi-turn vs Single-turn 关键差异

### Single-turn（当前方法）

```
Round 1: [系统级指令 + 任务描述 + 模块接口] → LLM → 代码
Round 2: [系统级指令 + 任务描述 + 模块接口 + 上轮最优代码 + 反馈] → LLM → 代码
Round 3: 同上，重新组织成独立请求
```

- 每轮是一个独立的 API 调用
- 不保留对话历史
- LLM 无法记住之前尝试过什么

### Multi-turn（本轮实验）

```
Turn 1: user: [任务描述 + 模块接口]
        assistant: [代码 v1]
Turn 2: user: [反馈信息 + 修复请求]
        assistant: [代码 v2]
Turn 3: user: [反馈信息 + 修复请求]
        assistant: [代码 v3]
```

- 所有轮次在同一对话上下文中
- LLM 可以看到自己之前的所有尝试
- 可能的优势：更好的错误追踪、避免重复犯错
- 可能的风险：token 预算快速增长、上下文过长导致注意力分散
