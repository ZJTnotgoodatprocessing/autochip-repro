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

## Current Main Benchmarks
- VerilogEval-Human subset (20 problems) — Haiku baseline
- RTLLM STUDY_12 (12 problems) — 3 models × 2 conditions

## Main Experiment Results
- VerilogEval Haiku: ZS 80% → FB 90%
- RTLLM GPT-5.4: ZS 50% → FB 83% (+33pp)
- RTLLM Sonnet 4.6: ZS 42% → FB 58% (+17pp)
- RTLLM Haiku: ZS 42% → FB 50% (+8pp)
- Stability: GPT FB 79.2% ± 4.2% (4 runs)
- **Authoritative results**: see `notes/authoritative_experiment_index.md`

## Key Findings
1. Feedback consistently improves pass rates across models and benchmarks
2. ~57% of improvement comes from error feedback itself, ~43% from resampling (GPT ablation)
3. Feedback granularity shows inverted-U: compile-only/succinct optimal, rich may overload
4. Multi-turn dialogue provides +17pp over single-turn at equal k (v2, bug-fixed)
5. Feedback effectiveness is model-dependent: Sonnet FB < RO in stability runs
6. Ceiling problems exist (freq_divbyfrac, LFSR) beyond current framework capability

## Current Stage
Thesis writing preparation (all experiments completed, audit passed 2026-04-24)

## Current Priorities
1. Write thesis body text using `notes/authoritative_experiment_index.md` as citation source
2. Prepare final defense PPT
3. Optional: larger-scale multi-turn validation

## Working Rules
- Do not rebuild the project from scratch
- Do not overwrite existing experiment outputs
- Do not delete existing notes/ and outputs/ results
- Read project state before continuing development
- Reuse existing scripts and modules
- Keep run_single_task.py, run_feedback_loop.py, run_verilogeval_subset.py stable
- Save new experiment results to outputs/runs/{category}/{run_id}/

## Important Files
- **notes/authoritative_experiment_index.md** — single source of truth for all results
- notes/current_status.md
- scripts/audit_project.py — code correctness tests
- scripts/audit_data.py — data consistency verification
- scripts/run_rtllm_subset.py — main experiment runner
- src/feedback/ — feedback loop core
- src/runner/ — verilog executor
- src/llm/ — LLM client

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