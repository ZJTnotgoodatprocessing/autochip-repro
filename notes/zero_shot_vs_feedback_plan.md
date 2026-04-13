# Zero-shot vs Feedback 对比实验计划

## 实验目标

量化 AutoChip feedback loop 对 Verilog 生成 pass rate 的提升效果。

## 实验设定

| 参数 | Zero-shot | Feedback |
|------|-----------|----------|
| 候选数 k | 1 | 3 |
| 最大迭代 | 1 | 5 |
| Temperature | 0.7 | 0.7 |
| 模型 | 统一读 `ANTHROPIC_MODEL` | 同左 |

两组实验使用同一个脚本 `scripts/compare_zero_shot_vs_feedback.py`，内部复用 `run_feedback_loop()`：
- Zero-shot = `run_feedback_loop(task, k=1, max_iterations=1)`
- Feedback = `run_feedback_loop(task, k=3, max_iterations=5)`

## 任务集

### 简单任务（预期 zero-shot 即通过）
| 任务 | 类型 | 测试点 |
|------|------|--------|
| sample_task | wire 连接 | 4 |
| and_gate | 2 输入与门 | 4 |
| mux2to1 | 2:1 MUX | 8 |
| adder_8bit | 8 位加法器 | 8 |
| population_count | 3 位 popcount | 8 |

### 难任务（预期 zero-shot 可能失败）
| 任务 | 类型 | 测试点 | 预期难度来源 |
|------|------|--------|-------------|
| edge_detect | 时序：上升沿检测 | 18 | 需要 flip-flop 存储 prev 值，reset 行为 |
| priority_encoder_8 | 组合：优先编码器 | 256 | 优先级方向、全零处理 |
| signed_add_overflow | 组合：带溢出检测的有符号加法 | 26 | 溢出条件判断、有符号/无符号混淆 |
| lfsr_5bit | 时序：线性反馈移位寄存器 | 46 | 特定多项式、移位方向、反馈 tap 位置 |

## 运行命令

```bash
# 跑全部 9 个任务
python scripts/compare_zero_shot_vs_feedback.py

# 只跑难任务
python scripts/compare_zero_shot_vs_feedback.py --tasks edge_detect priority_encoder_8 signed_add_overflow lfsr_5bit

# 调参
python scripts/compare_zero_shot_vs_feedback.py --feedback-k 5 --feedback-iterations 8 --temperature 0.5
```

## 输出

- 控制台对比表格
- `outputs/comparison_{timestamp}.json` — 完整数据
- `outputs/comparison_{timestamp}.csv` — 表格数据

## 关键指标

1. **Zero-shot pass rate** vs **Feedback pass rate**
2. **Improved count**: 多少任务从 zero-shot FAIL 变为 feedback PASS
3. **迭代次数**: feedback 通过的任务平均需要几轮迭代

## 预期假设

- 简单任务：两组都 PASS，feedback 无额外收益
- 难任务：zero-shot 部分 FAIL，feedback 可以修复其中部分/全部
- 如果 feedback 在所有难任务上都无法改善，说明需要更好的 feedback 策略或更多迭代次数
