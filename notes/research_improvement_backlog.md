# AutoChip 研究改进路线 (Research Improvement Backlog)

> 最后更新：2026-04-23
> 当前阶段：RTLLM STUDY_12 正式实验 + 消融 + 稳定性实验已完成

---

## 一、现有实验资产

| 阶段 | 状态 | 关键成果 |
|------|------|----------|
| RTLLM STUDY_12 正式实验 | ✅ 完成 | 三模型结果，GPT-5.4 最优 |
| 消融实验 (ZS/RO/FB) | ✅ 完成 | feedback 贡献 +16.7pp (GPT-5.4) |
| 稳定性实验 (4轮重复) | ✅ 完成 | GPT FB 79.2% ± 4.2%，结论稳定 |
| 反馈粒度实验 | 🔄 进行中 | 5 级反馈对比 |
| 论文/答辩资产化 | ✅ 完成 | 图表、案例分析、可靠性说明 |

---

## 二、研究改进方向排序

### 1. 反馈粒度实验 ⭐ [高优先级 → 进行中]

- **研究价值**: ★★★★★ — 直接回答"什么级别的反馈信息最有效"，是论文核心论证的关键补充
- **实现成本**: 低 — 仅需修改 prompt_builder，复用已有实验框架
- **与当前阶段匹配度**: 完美匹配 — 自然承接消融实验
- **建议**: 已在本轮实施。结果将直接回答 Sonnet 上 feedback 表现差是否与信息粒度有关

---

### 2. 提示词策略对比 (Few-shot / CoT) ⭐ [高优先级]

- **研究价值**: ★★★★☆ — Few-shot 和 Chain-of-Thought 是当前 LLM 研究中最主流的提示优化手段，对比它们与 feedback loop 的效果有很强的论文价值
- **实现成本**: 中 — 需要设计 few-shot 示例集（可从已通过题目中采样），CoT 需要修改提示词
- **与当前阶段匹配度**: 高 — 可复用 RTLLM STUDY_12 框架
- **建议优先级**: 高 — 建议作为下一轮实验
- **具体方向**:
  - Few-shot: 从已通过的简单题目中提取 1-2 个 (description, code) 作为 in-context example
  - CoT: 在提示词中要求模型先分析需求，再编写代码
  - 对比组: Zero-shot vs Few-shot-zero vs CoT-zero vs Feedback (current)

---

### 3. 更大规模 Benchmark 扩展 [中优先级]

- **研究价值**: ★★★★☆ — 扩大题目规模能增强结论的泛化性
- **实现成本**: 低 — 基础设施已完备，只需扩大子集
- **与当前阶段匹配度**: 中 — 但在方法论完善之前扩大规模意义有限
- **建议优先级**: 中 — 建议在提示词策略对比后进行
- **具体方向**:
  - 从 STUDY_12 扩展到 STUDY_24 或全量 RTLLM
  - 关注不同难度层级的表现差异
  - 与 VerilogEval 交叉验证

---

### 4. 更多模型对照 [中优先级]

- **研究价值**: ★★★☆☆ — 增加模型覆盖面可增强泛化性，但边际价值递减
- **实现成本**: 低 — 统一中转站已支持多模型切换
- **与当前阶段匹配度**: 中
- **建议优先级**: 中 — 可在扩大 benchmark 时顺便补充
- **备选模型**: DeepSeek V3.2, Gemini 2.5 Pro, Claude Opus 4.6
- **注意**: 当前三模型（Haiku/Sonnet/GPT-5.4）已覆盖弱/中/强能力梯度

---

### 5. 多轮对话反馈 [中低优先级]

- **研究价值**: ★★★☆☆ — 将 feedback loop 从"单轮提示"升级为"多轮对话"，可能提升上下文理解
- **实现成本**: 高 — 需要大幅修改 LLM client 和 loop_runner，支持对话历史管理、token 预算控制
- **与当前阶段匹配度**: 低 — 工程改动大，可能需要 2-3 天
- **建议优先级**: 中低 — 建议作为论文"改进方向"讨论，不一定需要实现
- **风险**: token 预算可能快速耗尽；API 成本显著增加

---

### 6. RAG (检索增强生成) [低优先级]

- **研究价值**: ★★★☆☆ — 从开源 Verilog 代码库中检索相关设计作为参考，理论上能提升生成质量
- **实现成本**: 高 — 需要构建 Verilog 代码向量库、实现语义检索、设计合理的 prompt 集成方式
- **与当前阶段匹配度**: 低 — 工程量大，超出当前论文聚焦范围
- **建议优先级**: 低 — 建议仅在"未来工作"中讨论
- **技术挑战**: Verilog 代码的语义相似性定义不成熟；检索质量高度依赖语料库

---

### 7. 形式化验证集成 [低优先级]

- **研究价值**: ★★★★☆ — 将仿真验证替换或补充为形式化验证（model checking / SAT-based equivalence），可提供更强的正确性保证
- **实现成本**: 极高 — 需要集成 Yosys / SymbiYosys 等工具链，编写 PSL/SVA 属性，处理工具链兼容性
- **与当前阶段匹配度**: 很低 — 完全不同的技术栈
- **建议优先级**: 低 — 建议仅在"未来工作"中讨论
- **论文价值**: 可以在"Limitations"中提及"当前依赖仿真验证，未来可引入形式化方法以增强正确性保证"

---

## 三、推荐执行路线图

```
已完成                         当前                         后续（建议顺序）
──────────────────────────────────────────────────────────────────────
正式实验     →  消融实验     →  反馈粒度实验   →  提示词策略对比
稳定性实验   →  结果资产化   →                 →  扩大 benchmark
                                               →  补充模型（可选）
                                               →  论文终稿写作
```

---

## 四、论文"未来工作"部分建议

以下方向建议在论文中作为"Future Work"讨论：

1. **多轮对话反馈**: "Extending the single-prompt feedback loop to a multi-turn conversational protocol could improve context retention..."
2. **RAG 增强**: "Retrieving relevant Verilog designs from open-source repositories as in-context references..."
3. **形式化验证集成**: "Replacing simulation-based verification with formal equivalence checking..."
4. **自适应反馈粒度**: "Automatically selecting the optimal feedback granularity based on the problem type or model..."
