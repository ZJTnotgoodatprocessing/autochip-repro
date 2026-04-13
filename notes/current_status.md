# 当前项目状态

## 课题名称
基于大语言模型与 EDA 工具反馈的 RTL 代码自动生成与自修复研究

## 研究主线
以 AutoChip 为主要参考对象，复现并分析其“生成—编译/仿真—反馈—修复”的 RTL 自动生成闭环机制，构建可运行原型系统，并在公开 benchmark 上验证 feedback loop 的作用。

## 当前阶段定位
当前项目已经完成核心系统搭建，已从“原型实现阶段”进入“实验分析与论文材料整理阶段”。

## 已完成工作
1. 完成 AutoChip 相关文献调研，并确定以 AutoChip 为主复现对象。
2. 完成 AutoChip 风格原型系统搭建。
3. 完成单任务与小批量任务运行验证。
4. 完成 succinct feedback loop 实现。
5. 完成 VerilogEval-Human 子集接入。
6. 完成 Haiku 主实验。
7. 完成实验总结、图表与关键案例分析。
8. 已开始整理中期报告与中期答辩材料。

## 当前主实验基线
- model: claude-haiku-4-5-20251001
- benchmark: VerilogEval-Human subset (20 problems)
- zero-shot: 16/20 (80%)
- feedback: 18/20 (90%)
- improved by feedback: 2 tasks
- API errors: 0

## 当前关键案例
- Prob109_fsm1：zero-shot 失败，feedback 第 2 轮修复成功
- Prob127_lemmings1：zero-shot 失败，feedback 第 2 轮修复成功
- Prob140_fsm_hdlc：feedback 有提升但未完全通过
- Prob082_lfsr32：feedback 无效，反映领域知识缺失问题

## 当前阶段结论
1. feedback loop 对部分 FSM / 控制逻辑类任务有效。
2. 对“接近正确但存在局部逻辑错误”的代码，feedback 修复效果较好。
3. 对需要精确领域知识或复杂协议边界条件的问题，feedback 能力有限。
4. 当前结果已可作为中期报告和后续论文实验部分的阶段性支撑。

## 当前最优先任务
1. 完成中期报告定稿
2. 完成中期答辩 PPT 和口头汇报稿
3. 整理主实验结果表、图和案例分析
4. 明确中期之后的后续实验计划

## 中期之后准备继续做的事
1. 扩大实验样本规模，或补充重复实验验证稳定性
2. 深化错误类型分析
3. 优化 feedback prompt
4. 视时间做少量补充对比或消融实验
5. 逐步完成论文正文撰写

## 注意事项
- 不要重新初始化项目
- 不要覆盖已有 outputs/ 和 notes/
- 优先复用现有 scripts、src 和已有实验结果
- 区分“已完成”“正在进行”“后续计划”
- 后续工作重点是实验分析与论文整理，而不是重新搭系统