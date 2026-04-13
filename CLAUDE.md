# AutoChip Repro Project Guide

## Project Goal
本项目用于复现并分析 AutoChip 风格的 RTL 自动生成与反馈修复框架，核心目标是验证 EDA 工具反馈对 Verilog 自动生成质量的提升作用，并在此基础上探索轻量改进方向。

## Project Scope
当前项目重点不是训练新模型，而是：
1. 构建 AutoChip 风格原型系统
2. 接入 benchmark
3. 跑 zero-shot vs feedback 实验
4. 做案例分析
5. 支撑中期报告、毕业论文和答辩材料

## Current Main Benchmark
VerilogEval-Human subset (20 problems)

## Main Experiment Baseline
- model: claude-haiku-4-5-20251001
- zero-shot: 16/20
- feedback: 18/20
- improved by feedback: 2 tasks
- API errors: 0

## Key Findings So Far
1. feedback loop 将通过率从 80% 提升到 90%
2. feedback 对部分 FSM 任务有效
3. 对 LFSR 抽头类问题和复杂协议边界条件问题作用有限
4. 当前系统已具备中期报告所需的阶段性成果

## Current Priorities
1. 完成中期报告与中期答辩材料
2. 整理实验图表与关键案例
3. 继续做错误类型分析
4. 视时间补充小规模实验或轻量改进

## Working Rules
- 不要从头开始重建项目
- 不要覆盖已有实验输出
- 不要删除 notes/ 和 outputs/ 中已有结果
- 先读取项目现状再继续开发
- 优先复用现有脚本和模块
- 修改代码时保持 run_single_task.py、run_feedback_loop.py、run_verilogeval_subset.py 等主流程稳定

## Important Files
- notes/current_status.md
- notes/haiku_main_experiment_summary.md
- outputs/reports/haiku_pass_rate_bar.png
- outputs/reports/haiku_per_problem_rank.png
- scripts/run_verilogeval_subset.py
- scripts/run_feedback_loop.py
- src/feedback/
- src/runner/
- src/llm/

## What To Avoid
- 不要把未完成的内容写成已完成
- 不要夸大实验结论
- 不要把中期报告写成开题报告
- 不要在没有必要时大幅扩展研究范围
- 不要优先做高风险、大工程量的新方向

## Preferred Next-Step Style
继续工作时，优先先做：
1. 读取当前项目状态
2. 总结已完成进度
3. 明确下一步最重要的 2~3 项任务
4. 再开始修改代码或整理文档