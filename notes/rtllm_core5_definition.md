# RTLLM_CORE_5 子集定义

> 定义日期：2026-04-21
> 用途：后中期主线实验的首批小规模验证子集

---

## 题目清单

| # | 设计名 | 类别 | 难度评估 | 选择理由 |
|---|--------|------|----------|---------|
| 1 | adder_8bit | Arithmetic/Adder | Easy | 基线 smoke 题，结构简单，已验证 iverilog 全流程通过 |
| 2 | multi_booth_8bit | Arithmetic/Multiplier | Medium-Hard | Booth 编码乘法器，算法复杂，代表算术类中等难度 |
| 3 | fsm | Control/FSM | Medium | 序列检测 FSM（Mealy 型），代表控制逻辑类核心场景 |
| 4 | LIFObuffer | Memory/LIFO | Medium | 栈式存储结构，代表存储类，含读写指针管理 |
| 5 | traffic_light | Miscellaneous/Others | Medium-Hard | 交通灯控制器（含状态机+定时），代表综合应用类 |

---

## 覆盖分析

### 类别覆盖
- Arithmetic: 2 题（adder_8bit, multi_booth_8bit）
- Control/FSM: 1 题（fsm）
- Memory: 1 题（LIFObuffer）
- Miscellaneous: 1 题（traffic_light）

### 难度分布
- Easy: 1 题
- Medium: 2 题
- Medium-Hard: 2 题

### iverilog 兼容性
- 5/5 全部已通过编译+仿真验证

---

## 使用方式

### 首轮 smoke（快速验证流水线）
优先按以下顺序跑：
1. `adder_8bit` — 最简单，验证 RTLLM 接入流程
2. `fsm` — 验证 FSM 类任务

### 首轮正式小实验（zero-shot vs feedback 对比）
全部 5 题跑完 zero-shot + feedback，产出：
- 逐题 pass/fail + rank 对比
- 与 VerilogEval 基线的横向讨论

---

## 在脚本中使用

```bash
# 跑 RTLLM_CORE_5 全部 5 题
python scripts/run_rtllm_subset.py --subset core5

# 指定模型
python scripts/run_rtllm_subset.py --subset core5 --model gpt-5.4
```
