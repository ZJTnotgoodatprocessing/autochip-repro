# run_feedback_loop — 下一步操作

## 基本用法

```bash
# 最简单 — 跑一个任务
python scripts/run_feedback_loop.py --task data/sample_task

# 调参
python scripts/run_feedback_loop.py --task data/adder_8bit --k 3 --max-iterations 5 --temperature 0.5

# 跑一个预期需要多轮修复的任务
python scripts/run_feedback_loop.py --task data/population_count --k 5 --max-iterations 8
```

## 预期输出

```
=== AutoChip Feedback Loop ===
Task:           adder_8bit
Model:          claude-opus-4-6
Candidates/iter: 3
Max iterations: 5
Temperature:    0.7

  Iter 1: candidates=[1.00, 1.00, 1.00]  best=1.00  PASS

--- Result ---
Total iterations: 1
Best rank:        1.00
Passed:           True
```

## 跑通后关注点

1. **一轮即 PASS**: 对简单任务（and_gate, sample_task）来说是正常的，说明 pipeline 工作正确
2. **多轮后 PASS**: feedback loop 生效的正面证据
3. **max_iterations 用完仍 FAIL**: 需要分析具体是编译失败还是仿真失败
4. **k 的效果**: 对比 k=1 和 k=3 的通过率差异

## 后续对比实验

要得到 zero-shot vs feedback 的可对比结果：

### 实验 A: Zero-shot baseline
```bash
# k=1, max_iterations=1 相当于 zero-shot
python scripts/run_feedback_loop.py --task data/adder_8bit --k 1 --max-iterations 1
```

### 实验 B: Feedback loop
```bash
# k=3, max_iterations=5 — 标准 feedback loop
python scripts/run_feedback_loop.py --task data/adder_8bit --k 3 --max-iterations 5
```

### 批量对比脚本（后续实现）
对 data/ 下所有任务跑两组实验，汇总为对比表格：
```
Task              Zero-shot  Feedback(k=3,iter=5)
-------------------------------------------------
sample_task         PASS        PASS (iter=1)
and_gate            PASS        PASS (iter=1)
adder_8bit          PASS        PASS (iter=1)
mux2to1             FAIL        PASS (iter=3)
population_count    FAIL        PASS (iter=2)
```

## 接入更难的 benchmark 题目

当前 5 个任务对于 Claude 来说可能太简单（全部一轮通过）。
为了真正展示 feedback loop 的价值，下一步需要从 HDLBits 引入更难的题目。

推荐加入的难度升级任务：
- 带状态机的 sequential circuit（如 FSM、counter）
- 需要边界处理的 combinational circuit（如 priority encoder）
- 多模块组合的复杂设计
