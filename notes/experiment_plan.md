# 实验计划

## 实验一：Baseline 复现

**目的**：验证在相同设定下能否复现论文结果

| 参数 | 设定 |
|------|------|
| LLM | GPT-4（与论文一致） |
| Benchmark | HDLBits 子集（论文 Table I 中的题目） |
| 最大迭代轮次 | 10 |
| Temperature | 0.7 |
| 反馈内容 | 编译错误 + 仿真 pass/fail |

**预期产出**：pass rate 表格，与论文数据的偏差分析

---

## 实验二：LLM 后端对比

**目的**：对比不同 LLM 在 HDL 生成任务上的表现

| 模型 | 来源 | 备注 |
|------|------|------|
| GPT-4 | OpenAI API | baseline |
| GPT-4o | OpenAI API | 速度更快，观察质量差异 |
| Claude Sonnet | Anthropic API | 对比不同厂商 |
| DeepSeek Coder | 本地/API | 开源模型代表 |

**控制变量**：prompt 模板、迭代轮次、temperature 均保持一致

**预期产出**：多模型 pass rate 对比表 + 柱状图

---

## 实验三：Prompt 策略对比

**目的**：探索 prompt engineering 对 Verilog 生成质量的影响

| 策略 | 描述 |
|------|------|
| Zero-shot | 仅给出模块接口和功能描述 |
| Few-shot | 附带 1-2 个已解决的示例 |
| CoT (Chain-of-Thought) | 要求模型先分析电路逻辑再写代码 |

**固定 LLM**：GPT-4（baseline 模型）

**预期产出**：不同 prompt 策略的 pass rate 对比 + 失败案例分析

---

## 实验四：反馈粒度实验

**目的**：验证不同反馈信息量对迭代修复效果的影响

| 反馈级别 | 内容 |
|----------|------|
| Level 0 | 无反馈（单次生成） |
| Level 1 | 仅编译错误信息 |
| Level 2 | 编译错误 + 仿真 pass/fail（AutoChip 默认） |
| Level 3 | 编译错误 + 仿真 log + 期望 vs 实际输出 diff |

**预期产出**：反馈粒度 vs pass rate 曲线，说明反馈信息量的边际收益

---

## 统计与可视化规划

- 每个实验至少跑 3 次取平均（控制随机性）
- 使用 `scripts/` 中的脚本自动汇总 `outputs/` 下的结果
- 图表使用 matplotlib/seaborn，保存为 PDF 供报告引用
