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

## Current Stage
Post-midterm (midterm defense completed 2026-04-14)

## Current Priorities
1. Design and execute expansion experiments with stronger models + harder benchmarks
2. Run repeat experiments on 20-problem subset for result stability
3. Deepen error type analysis and case study materials
4. Progressively write thesis body text
5. Accumulate final defense materials

## Working Rules
- Do not rebuild the project from scratch
- Do not overwrite existing experiment outputs
- Do not delete existing notes/ and outputs/ results
- Read project state before continuing development
- Reuse existing scripts and modules
- Keep run_single_task.py, run_feedback_loop.py, run_verilogeval_subset.py stable
- Save new experiment results to outputs/runs/{category}/{run_id}/

## Important Files
- notes/current_status.md
- notes/haiku_main_experiment_summary.md
- outputs/verilogeval_both_20260412_173450.json  (authoritative main experiment result)
- outputs/reports/haiku_pass_rate_bar.png
- outputs/reports/haiku_per_problem_rank.png
- scripts/run_verilogeval_subset.py
- scripts/run_feedback_loop.py
- src/feedback/
- src/runner/
- src/llm/

## What To Avoid
- Do not write incomplete work as completed
- Do not exaggerate experimental conclusions
- Do not continue modifying midterm report
- Do not expand research scope without necessity
- Do not prioritize high-risk, large-effort new directions
- Do not fabricate experimental data or intermediate traces

## Preferred Next-Step Style
When continuing work, prioritize:
1. Read current project state
2. Summarize completed progress
3. Identify the 2-3 most important next tasks
4. Then start modifying code or organizing documents