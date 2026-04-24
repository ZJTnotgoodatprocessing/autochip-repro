# 当前项目状态

## 课题名称
基于大语言模型与 EDA 工具反馈的 RTL 代码自动生成与自修复研究

## 研究主线
以 AutoChip 为主要参考对象，复现并分析其"生成—编译/仿真—反馈—修复"的 RTL 自动生成闭环机制，构建可运行原型系统，并在公开 benchmark 上验证 feedback loop 的作用。

## 当前阶段定位
**论文撰写准备阶段**（2026-04-24 更新）。全部实验已完成，权威结果索引已建立，代码与数据审计已通过。

## 已完成工作
1. 完成 AutoChip 相关文献调研，并确定以 AutoChip 为主复现对象。
2. 完成 AutoChip 风格原型系统搭建（src/ 全部核心模块）。
3. 完成单任务与小批量任务运行验证。
4. 完成 succinct feedback loop 实现。
5. 完成 VerilogEval-Human 子集接入（20 题）。
6. 完成 Haiku 主实验（20 题，zero-shot vs feedback，0 API 错误）。
7. 完成实验总结、图表与关键案例分析。
8. 完成中期报告定稿与中期答辩。
9. 完成 RTLLM 2.0 接入：50 题兼容性审计（41/50 可用），rtllm_loader 实现。
10. 完成 RTLLM STUDY_12 正式实验矩阵：3 模型 × 2 条件，0 API 错误。
11. 完成正式结果分析：图表资产化、典型案例分析、可靠性说明。
12. 完成 Feedback Ablation：zero-shot / retry-only / feedback 三条件消融。
13. 完成 Stability 实验：GPT-5.4 × 4 + Sonnet 4.6 × 4 轮重复。
14. 完成 Feedback Granularity 实验：L0–L4 五级粒度对比。
15. 完成 Multi-turn v2 实验：4 条件对照（修正 v1 bug 后结论反转）。
16. **完成项目审计**：代码正确性 24/24 + 数据一致性 20/20 + 文档交叉验证 11/11。
17. **完成权威实验索引**：`notes/authoritative_experiment_index.md`。

## 权威结果入口
**所有实验结果的引用请查阅 `notes/authoritative_experiment_index.md`。**

## 当前主实验基线

### VerilogEval-Human（Haiku 基线）
- model: claude-haiku-4-5-20251001
- zero-shot: 16/20 (80%), feedback: 18/20 (90%), improved: 2
- 权威结果来源: `outputs/verilogeval_both_20260412_173450.json`

### RTLLM STUDY_12 正式实验矩阵（论文核心数据）
| 模型 | Zero-shot | Feedback | 改善题数 |
|------|-----------|----------|----------|
| claude-haiku-4-5-20251001 | 5/12 (42%) | 6/12 (50%) | 2 |
| claude-sonnet-4-6 | 5/12 (42%) | 7/12 (58%) | 2 |
| gpt-5.4 | 6/12 (50%) | 10/12 (83%) | 4 |

## 审计状态
- `scripts/audit_project.py` — 2026-04-24 PASSED (24/24)
- `scripts/audit_data.py` — 2026-04-24 PASSED (20 runs, 0 inconsistencies)
- Multi-turn v1 bug 已修正 → v2 权威结果已替代

## 当前最优先任务
1. 论文正文撰写：以 `authoritative_experiment_index.md` 为引用入口
2. 最终答辩 PPT 准备
3. 可选扩展：更大规模 multi-turn 实验验证

## 注意事项
- 不要重新初始化项目
- 不要覆盖已有 outputs/ 和 notes/
- 引用实验结果前务必查阅权威索引，避免误引已废弃 v1 结论
- 新实验结果使用 `outputs/runs/{category}/{run_id}/` 格式保存