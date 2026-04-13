# Feedback Loop 实现计划

## 概述

实现 AutoChip 的核心机制——succinct feedback loop，使 LLM 能根据编译/仿真错误反馈迭代修复 Verilog 代码。

## 架构

```
                     ┌─────────────┐
                     │  Initial    │
                     │  Prompt     │
                     └─────┬───────┘
                           │
                    ┌──────▼──────┐
              ┌────►│  LLM (k个)  │◄────┐
              │     └──────┬──────┘     │
              │            │            │
              │     ┌──────▼──────┐     │
              │     │  Extract    │     │
              │     │  Verilog    │     │
              │     └──────┬──────┘     │
              │            │            │
              │     ┌──────▼──────┐     │
              │     │  Compile    │     │
              │     │  (iverilog) │     │
              │     └──────┬──────┘     │
              │            │            │
              │     ┌──────▼──────┐     │
              │     │  Simulate   │     │
              │     │  (vvp)      │     │
              │     └──────┬──────┘     │
              │            │            │
              │     ┌──────▼──────┐     │
              │     │  Rank &     │     │
              │     │  Select Best│     │
              │     └──────┬──────┘     │
              │            │            │
              │     pass?  │            │
              │     ┌──────▼──────┐     │
              │  Y  │             │  N  │
              │◄────┤  rank==1.0? ├────►│
              │     │             │     │
              │     └─────────────┘     │
              │                         │
         ┌────▼────┐          ┌─────────▼─────────┐
         │  DONE   │          │  Build Feedback    │
         │  (PASS) │          │  Prompt (succinct) │
         └─────────┘          └───────────────────┘
```

## 新增/修改的文件

| 文件 | 类型 | 说明 |
|------|------|------|
| `prompts/feedback_succinct.txt` | 新增 | 反馈 prompt 模板，占位符填充 |
| `src/feedback/prompt_builder.py` | 新增 | `build_initial_prompt()` + `build_feedback_prompt()` |
| `src/feedback/loop_runner.py` | 新增 | `run_feedback_loop()` 主循环 |
| `src/llm/client.py` | 修改 | 新增 `generate_with_history()` |
| `scripts/run_feedback_loop.py` | 新增 | CLI 入口脚本 |

## 关键设计决策

1. **Succinct feedback**: 只传递关键错误信息（编译错误行或仿真失败的 mismatch 数），不传全量 log，控制 token 消耗
2. **k 候选**: 第 1 轮和后续轮都生成 k 个候选，取 rank 最高的作为该轮结果
3. **全局最优追踪**: feedback prompt 基于历史最优候选构建，而非仅上一轮的最优
4. **不破坏现有脚本**: `run_single_task.py` 和 `run_small_batch.py` 完全不动

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| k | 3 | 每轮候选数 |
| max_iterations | 5 | 最大迭代轮数 |
| temperature | 0.7 | LLM 采样温度 |

## 输出格式

每次运行保存到 `outputs/feedback_{task_name}_{timestamp}.json`，包含：
- 每轮每个候选的完整记录（prompt, raw_response, verilog, compile/sim results, rank）
- 最终最优候选代码和 rank
- 是否通过 + 总迭代轮数
