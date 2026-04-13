# 小批量运行 — 下一步

## 运行命令

```bash
# 跑全部 5 个任务
python scripts/run_small_batch.py

# 只跑指定任务
python scripts/run_small_batch.py --tasks sample_task and_gate mux2to1

# 调低 temperature 观察稳定性
python scripts/run_small_batch.py --temperature 0.3
```

## 预期输出

```
=== AutoChip Batch Run ===
Model: claude-opus-4-6
Tasks: 5

[1/5] Running adder_8bit... PASS
[2/5] Running and_gate... PASS
...

Task                    Compile      Sim     Rank   Passed
----------------------------------------------------------
adder_8bit                   OK     PASS     1.00        Y
and_gate                     OK     PASS     1.00        Y
mux2to1                      OK     PASS     1.00        Y
population_count             OK     PASS     1.00        Y
sample_task                  OK     PASS     1.00        Y
----------------------------------------------------------
Compile success rate:  5/5 (100%)
Simulation pass rate:  5/5 (100%)
```

## 跑通后关注点

1. **5/5 全通过**：说明单轮 pipeline 稳定，可以进入 feedback loop 阶段
2. **有个别 COMPILE_FAIL**：检查 LLM 生成的代码，可能是 module 名不匹配或语法问题
3. **有 SIM_FAIL (rank < 1.0)**：正常——这恰好是 feedback loop 要解决的场景

## 批量跑通后的下一阶段

实现 **feedback loop**（AutoChip 核心）：
1. `src/llm/client.py` — 加 `generate_with_history(messages)` 支持多轮对话
2. 新增 `src/feedback/builder.py` — 将编译/仿真错误格式化为反馈 prompt
3. 新增 `scripts/run_single_task_iterative.py` — 迭代主循环：
   - generate → compile → sim → rank
   - 如果 rank < 1.0：构建反馈 → 追加到 conversation history → 再次 generate
   - 终止：rank == 1.0 或达到 MAX_ITERATIONS
