# AutoChip Repro Project Guide

## Project Goal
本项目用于复现并分析 AutoChip 风格的 RTL 自动生成与反馈修复框架，核心目标是验证 EDA 工具反馈对 Verilog 自动生成质量的提升作用，并在此基础上探索轻量改进方向。

## Current Stage
**论文撰写准备阶段**（2026-04-25 更新）。全部实验已完成，代码/数据审计通过，权威索引已建立。

## Authoritative Results Entry Point
**`notes/authoritative_experiment_index.md`** — 所有实验结果的唯一引用入口。论文/答辩中的数据引用必须经此索引确认。

## Current Core Benchmarks
- **VerilogEval-Human 20题** — 中期基线（Haiku: ZS 80% → FB 90%）
- **RTLLM STUDY_12 (12题)** — 后中期核心实验（3 模型 × 多条件）

## Completed Experiments

| # | 实验 | 关键结果 |
|---|------|----------|
| 1 | VerilogEval Haiku 主实验 | ZS 80% → FB 90% |
| 2 | RTLLM STUDY_12 正式实验 | GPT: ZS 50% → FB 83%; Sonnet: 42% → 58%; Haiku: 42% → 50% |
| 3 | Feedback Ablation (ZS/RO/FB) | ~57% 来自反馈，~43% 来自重采样 |
| 4 | Stability (×4) | GPT FB 79.2% ± 4.2% |
| 5 | Feedback Granularity (L0–L4) | 倒 U 型：compile-only/succinct 最优 |
| 6 | Multi-turn v2 (bug-fixed) | MT 对两模型均 +17pp |
| 7 | Prompt Strategy (Base/CoT/Fewshot/FS+CoT) | Fewshot ZS +9pp; FB 将所有策略拉平至 92% |
| 8 | Project Audit | 代码 24/24 + 数据 20/20 |

## Key Findings
1. Feedback consistently improves pass rates across models and benchmarks
2. ~57% of improvement comes from error feedback itself, ~43% from resampling (GPT ablation)
3. Feedback granularity shows inverted-U: compile-only/succinct optimal, rich may overload
4. Multi-turn dialogue provides +17pp over single-turn at equal k (v2, bug-fixed)
5. Prompt strategy (CoT/Fewshot) has limited ZS impact; feedback dominates final results
6. Feedback effectiveness is model-dependent: Sonnet FB < RO in stability runs
7. Ceiling problems exist (freq_divbyfrac) beyond current framework capability

## Current Priorities
1. **论文实验章节撰写** — 以 `authoritative_experiment_index.md` 为引用入口
2. **论文系统设计章节整理** — 描述 AutoChip 风格原型系统架构
3. **最终答辩 PPT 资产整理** — 复用已有图表和案例分析

## Critical Warnings
- ⚠️ **Multi-turn v1 (`9760eb4`) 是 SUPERSEDED，不可引用**。其结论完全错误（MT 有害），已被 v2 (`e792955`) 替代
- ⚠️ **所有实验引用以 `authoritative_experiment_index.md` 为准**，不要从 notes/ 中的旧文档直接取数据

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
- notes/current_status.md — project status overview
- notes/research_improvement_backlog.md — experiment roadmap and future work
- scripts/audit_project.py — code correctness tests (24 checks)
- scripts/audit_data.py — data consistency verification (20+ runs)
- scripts/run_rtllm_subset.py — main experiment runner
- src/feedback/ — feedback loop core (loop_runner, prompt_builder)
- src/runner/ — verilog executor, task, loaders
- src/llm/ — LLM client (unified relay)

## What To Avoid
- Do not write incomplete work as completed
- Do not exaggerate experimental conclusions
- Do not expand research scope without necessity — all planned experiments are done
- Do not fabricate experimental data or intermediate traces
- Do not cite Multi-turn v1 results anywhere