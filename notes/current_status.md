# 当前项目状态

## 课题名称
基于大语言模型与 EDA 工具反馈的 RTL 代码自动生成与自修复研究

## 研究主线
以 AutoChip 为主要参考对象，复现并分析其"生成—编译/仿真—反馈—修复"的 RTL 自动生成闭环机制，构建可运行原型系统，并在公开 benchmark 上验证 feedback loop 的作用。

## 当前阶段定位
**后中期阶段**（2026-04-22 更新）。RTLLM STUDY_12 正式实验矩阵已完成，进入结果资产化与论文撰写阶段。

## 已完成工作
1. 完成 AutoChip 相关文献调研，并确定以 AutoChip 为主复现对象。
2. 完成 AutoChip 风格原型系统搭建（src/ 全部核心模块）。
3. 完成单任务与小批量任务运行验证。
4. 完成 succinct feedback loop 实现。
5. 完成 VerilogEval-Human 子集接入（20 题）。
6. 完成 Haiku 主实验（20 题，zero-shot vs feedback，0 API 错误）。
7. 完成实验总结、图表与关键案例分析。
8. 完成中期报告定稿与中期答辩。
9. **完成 RTLLM 2.0 接入**：50 题兼容性审计（41/50 可用），rtllm_loader 实现。
10. **完成 RTLLM STUDY_12 正式实验矩阵**：3 模型 × 2 条件，0 API 错误。
11. **完成正式结果分析**：图表资产化、典型案例分析、可靠性说明。
12. **完成 LLM_MODEL 变量清理**：支持 provider-agnostic 模型切换。

## 当前主实验基线

### VerilogEval-Human（Haiku 基线）
- model: claude-haiku-4-5-20251001
- benchmark: VerilogEval-Human subset (20 problems)
- zero-shot: 16/20 (80%), feedback: 18/20 (90%), improved: 2
- 权威结果来源: `outputs/verilogeval_both_20260412_173450.json`

### RTLLM STUDY_12 正式实验矩阵（论文核心数据）
| 模型 | Zero-shot | Feedback | 改善题数 |
|------|-----------|----------|----------|
| claude-haiku-4-5-20251001 | 5/12 (42%) | 6/12 (50%) | 2 |
| claude-sonnet-4-6 | 5/12 (42%) | 7/12 (58%) | 2 |
| gpt-5.4 | 6/12 (50%) | 10/12 (83%) | 4 |
- 权威结果来源: `outputs/runs/rtllm/rtllm_both_20260422_*/`

## 当前关键案例
- Prob109_fsm1：zero-shot 失败，feedback 第 2 轮修复成功
- Prob127_lemmings1：zero-shot 失败，feedback 第 2 轮修复成功
- Prob140_fsm_hdlc：feedback 有提升但未完全通过（92.5% → 97.1%）
- Prob082_lfsr32：feedback 无效，反映领域知识缺失问题

## 当前阶段结论
1. feedback loop 对部分 FSM / 控制逻辑类任务有效。
2. 对"接近正确但存在局部逻辑错误"的代码，feedback 修复效果较好。
3. 对需要精确领域知识或复杂协议边界条件的问题，feedback 能力有限。
4. 当前结果已可作为中期报告和后续论文实验部分的阶段性支撑。

## 当前最优先任务（后中期阶段）
1. ✅ ~~设计并执行"更强模型 + 更难 benchmark"验证 AutoChip 有效性的扩展实验~~ → 已完成（STUDY_12）
2. 论文正文撰写：将 RTLLM STUDY_12 结果整理为实验章节
3. 可选扩展：更多模型（gemini-2.5-pro / deepseek-v3.2）对照实验
4. 可选扩展：Haiku 重复实验验证结果稳定性
5. 最终答辩 PPT 准备

## 后续研究重点
### A 层：低风险、快速沉淀
- Haiku 重复实验（证明结果稳定性）
- 错误类型细化分析
- k 值消融实验

### B 层：更有研究价值的方向（导师建议）
- 更强模型实验：zero-shot 已很强时，feedback loop 是否仍有价值
- 更难 benchmark 子集：在 Hard 题上 feedback 的修复效率
- 强模型 + 难 benchmark 交叉实验：AutoChip 的价值边界
- 反馈策略消融：区分反馈价值 vs 多次重试价值

## 注意事项
- 不要重新初始化项目
- 不要覆盖已有 outputs/ 和 notes/
- 优先复用现有 scripts、src 和已有实验结果
- 区分"已完成""正在进行""后续计划"
- 后续工作重点是扩展实验与论文整理，不再围绕中期报告
- 新实验结果使用 `outputs/runs/{category}/{run_id}/` 格式保存