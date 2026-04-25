# AutoChip 研究改进路线 (Research Improvement Backlog)

> 最后更新：2026-04-25
> 当前阶段：**全部实验完成，进入论文撰写准备阶段**
> 权威引用入口：`notes/authoritative_experiment_index.md`

---

## 一、已完成实验资产

以下所有实验均已完成、通过审计，结果已纳入权威索引。**当前不再建议继续扩实验，除非论文写作中发现确切缺口。**

| # | 阶段 | 状态 | 关键成果 |
|---|------|------|----------|
| 1 | VerilogEval-Human 20题 Haiku 主实验 | ✅ 完成 | ZS 80% → FB 90%，中期基线 |
| 2 | RTLLM STUDY_12 正式实验 | ✅ 完成 | 三模型结果，GPT-5.4 最优 (ZS 50% → FB 83%) |
| 3 | Feedback Ablation (ZS/RO/FB) | ✅ 完成 | feedback 贡献 +16.7pp (GPT-5.4)，~57% 来自反馈本身 |
| 4 | Stability Repeated Runs (×4) | ✅ 完成 | GPT FB 79.2% ± 4.2%，结论稳定 |
| 5 | Feedback Granularity (L0–L4) | ✅ 完成 | 倒 U 型曲线：compile-only/succinct 最优，rich 可能过载 |
| 6 | Multi-turn v2 (bug-fixed) | ✅ 完成 | MT 对两模型均 +17pp（v1 有 bug 已修正并标记 superseded） |
| 7 | Prompt Strategy (P0–P3) | ✅ 完成 | Fewshot ZS +9pp，CoT 轻微有害，FB 将所有策略拉平至 92% |
| 8 | 结果资产化与案例分析 | ✅ 完成 | 图表、案例分析、可靠性说明 |
| 9 | 项目审计 | ✅ 完成 | 代码 24/24 + 数据 20/20 + 文档 11/11 |
| 10 | 权威实验索引 | ✅ 完成 | `authoritative_experiment_index.md` |

---

## 二、核心研究发现总览

1. **Feedback 一致性**: 反馈在所有模型和 benchmark 上均提升通过率
2. **反馈 vs 重采样**: ~57% 来自反馈信息本身，~43% 来自多次重采样机会 (GPT ablation)
3. **粒度倒 U**: compile-only/succinct 粒度最优，rich 粒度可能信息过载
4. **多轮对话**: 保持对话上下文可额外提升 +17pp，可解锁新修复策略
5. **提示词策略**: Fewshot 对 ZS 有轻微帮助 (+9pp)，但 feedback 将所有策略拉平至 92%，**feedback 是主导因素**
6. **CoT 无效**: CoT 对 GPT-5.4 的 ZS 轻微有害 (-8pp)，分析步骤可能干扰代码生成
7. **天花板题**: freq_divbyfrac 是所有策略 + feedback 均无法解决的天花板题
8. **模型依赖性**: Sonnet 的 feedback 效果弱于 GPT，且 k=3 多候选对 Sonnet 有害

---

## 三、当前优先任务

1. **论文实验章节撰写** — 以 `authoritative_experiment_index.md` 为唯一引用入口
2. **论文系统设计章节整理** — 描述 AutoChip 风格原型系统架构
3. **最终答辩 PPT 资产整理** — 复用已有图表和案例分析

---

## 四、论文"未来工作"部分建议

以下方向建议在论文中作为 Future Work 讨论，**当前阶段不建议实际执行**：

### 1. 扩大 Benchmark 规模
- 从 STUDY_12 扩展到 STUDY_24 或全量 RTLLM (50 题)
- 与 VerilogEval 交叉验证，增强泛化性
- 关注不同难度层级的表现差异

### 2. 更多模型对照
- 备选：DeepSeek V3.2、Gemini 2.5 Pro、Claude Opus 4.6、GLM5
- 当前三模型（Haiku/Sonnet/GPT-5.4）已覆盖弱/中/强能力梯度
- 边际价值递减，建议仅在论文中提及可扩展性

### 3. RAG (检索增强生成)
- 从开源 Verilog 代码库中检索相关设计作为参考
- 工程量大，超出当前论文聚焦范围
- 建议描述为"通过 RAG 提供领域知识可能进一步提升生成质量"

### 4. 形式化验证集成
- 用 Yosys / SymbiYosys 等工具替代或补充仿真验证
- 可在 Limitations 中提及"当前依赖仿真验证，未来可引入形式化方法"
- 工程量极高，完全不同技术栈

### 5. 自适应反馈策略
- 根据问题类型或模型自动选择最优反馈粒度
- 当前粒度实验已提供经验依据（compile-only/succinct 最优）
- 可作为"智能反馈调度"方向讨论

---

## 五、已废弃实验

| 实验 | Commit | 原因 |
|------|--------|------|
| Multi-turn v1 | `9760eb4` | 反馈数据源 bug，结论完全错误（MT 有害）→ 已被 v2 替代 |

⚠️ **Multi-turn v1 的结论不可引用。** 详见 `authoritative_experiment_index.md` §三。
