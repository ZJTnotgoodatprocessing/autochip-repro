# 权威实验结果索引 (Authoritative Experiment Index)

> **本文档是论文写作、答辩引用实验结果时的唯一入口。**
> 最后更新：2026-04-24
> 最后审计：2026-04-24 `audit_project.py` PASSED (24/24), `audit_data.py` PASSED (全部一致)

---

## 一、实验阶段总览

| # | 阶段 | Commit | 状态 | Notes 文档 | 数据目录 |
|---|------|--------|------|------------|----------|
| 1 | VerilogEval-Human 20题 Haiku 主实验 | pre-midterm | ✅ Authoritative | `haiku_main_experiment_summary.md` | `outputs/verilogeval_both_20260412_173450.json` |
| 2 | RTLLM CORE_5 打通验证 | `9e6ee6d` | ⚠️ Exploratory | `rtllm_core5_definition.md` | `outputs/runs/rtllm/rtllm_both_20260421_202309/` |
| 3 | RTLLM STUDY_12 正式实验 | `3338b96` | ✅ Authoritative | `rtllm_formal_experiment_summary.md` | 见§二 |
| 4 | 结果资产化与案例分析 | `3c61486` | ✅ Authoritative | `rtllm_case_studies.md`, `rtllm_experiment_reliability_note.md` | `outputs/reports/fig_*.png` |
| 5 | Feedback Ablation (ZS/RO/FB) | `7655475` | ✅ Authoritative | `rtllm_feedback_ablation_summary.md` | 见§二 |
| 6 | Stability Repeated Runs (×4) | `8989133` | ✅ Authoritative | `rtllm_stability_summary.md` | 见§二 |
| 7 | Feedback Granularity (L0–L4) | `5ccd419` | ✅ Authoritative | `rtllm_feedback_granularity_summary.md` | 见§二 |
| 8 | Multi-turn v1 | `9760eb4` | ❌ **Superseded** | — | 见§三（不可引用） |
| 9 | Multi-turn v2 (bug-fixed) | `e792955` | ✅ Authoritative | `rtllm_multiturn_feedback_summary.md` | 见§二 |
| 10 | Project Audit | `6b113aa` | ✅ Authoritative | 本文档 | `scripts/audit_*.py` |
| 11 | Prompt Strategy (P0/P1/P2/P3) | *pending* | ✅ Authoritative | `rtllm_prompt_strategy_summary.md` | `rtllm_prompt_strategy_20260425_032429/` |

---

## 二、权威数据目录交叉索引

### 2.1 正式实验 (STUDY_12)

| 模型 | 运行目录 | ZS | FB | API Err |
|------|----------|----|----|---------|
| Haiku 4.5 | `rtllm_both_20260422_004806/` | 42% | 50% | 0 |
| Sonnet 4.6 | `rtllm_both_20260422_011115/` | 42% | 58% | 0 |
| GPT-5.4 | `rtllm_both_20260422_013439/` | 50% | 83% | 0 |

图表：`fig_passrate_comparison.png`, `fig_per_problem_matrix.png`, `fig_feedback_gain.png`

### 2.2 消融实验

| 模型 | 运行目录 | ZS | RO | FB |
|------|----------|----|----|-----|
| GPT-5.4 | `rtllm_ablation_20260422_222409/` | 50% | 67% | 83% |
| Sonnet 4.6 | `rtllm_ablation_20260422_214745/` | 75% | 75% | 58% |

图表：`fig_ablation_comparison.png`, `fig_ablation_decomposition.png`

### 2.3 稳定性实验 (4 轮重复)

| 模型 | Run 1 | Run 2 | Run 3 | Run 4 | 均值 ± SD |
|------|-------|-------|-------|-------|-----------|
| GPT-5.4 FB | 83% | 75% | 83% | 75% | 79.2% ± 4.2% |
| Sonnet FB | 58% | 50% | 58% | 67% | 58.3% ± 5.9% |

GPT runs: `rtllm_ablation_20260422_222409/`, `…_20260423_031507/`, `…_035517/`, `…_043355/`
Sonnet runs: `rtllm_ablation_20260422_214745/`, `…_20260423_051839/`, `…_130908/`, `…_134523/`
图表：`fig_stability_ablation.png`, `fig_stability_formal.png`

### 2.4 反馈粒度实验

| 模型 | L0 ZS | L1 RO | L2 CO | L3 SU | L4 RI |
|------|-------|-------|-------|-------|-------|
| GPT-5.4 | 58% | 75% | **92%** | **92%** | 83% |
| Sonnet 4.6 | 50% | 67% | **75%** | 67% | 67% |

Runs: `rtllm_granularity_20260423_212239/` (GPT), `…_233052/` (Sonnet)
图表：`fig_granularity_curve.png`, `fig_granularity_matrix.png`

### 2.5 Multi-turn v2 (权威版)

| 模型 | A:STk3 | D:STk1 | B:MTk1 | C:COk3 |
|------|--------|--------|--------|--------|
| GPT-5.4 | 83% | 83% | 100%* | 83% |
| Sonnet 4.6 | 17% | 33% | **50%** | 33% |

*GPT MT: 5/5 有效题通过 (1 题 API err 排除)
Runs: `rtllm_multiturn_20260424_160853/` (GPT), `…_181012/` (Sonnet)
图表：`fig_multiturn_comparison_v2.png`, `fig_multiturn_matrix_v2.png`

---

## 三、已废弃结果 (Superseded) — 不可作为论文结论引用

### 3.1 Multi-turn v1 (`9760eb4`)

| 运行目录 | 状态 | 原因 |
|----------|------|------|
| `rtllm_multiturn_20260424_031541/` (GPT) | ❌ Superseded | 反馈数据源 bug + 混淆变量 |
| `rtllm_multiturn_20260424_040236/` (Sonnet) | ❌ Superseded | 同上 |

**v1 的错误结论**：「multi-turn 对 GPT 有害 (−50pp)，对 Sonnet 中性」
**v2 修正后结论**：「multi-turn 对两模型均 +17pp」

> **论文引用规则**：如需提及 v1，仅可作为"工程审计案例"——说明本项目通过复盘发现并修正了实验 bug，体现研究严谨性。**不可**将 v1 的数字作为方法结论引用。

### 3.2 探索性早期运行

| 运行目录 | 状态 | 说明 |
|----------|------|------|
| `rtllm_both_20260421_202309/` (Haiku CORE_5) | ⚠️ Exploratory | CORE_5 打通验证，非正式结果 |
| `rtllm_zero-shot_20260421_233828/` (Sonnet 4.5) | ⚠️ Exploratory | 早期测试 |
| `rtllm_zero-shot_20260421_233909/` (GPT-5.2) | ⚠️ Exploratory | 早期测试 |

### 3.3 已废弃图表

| 图表 | 状态 | 替代版本 |
|------|------|----------|
| `fig_multiturn_comparison.png` | ❌ Superseded | `fig_multiturn_comparison_v2.png` |
| `fig_multiturn_matrix.png` | ❌ Superseded | `fig_multiturn_matrix_v2.png` |

---

## 四、当前可写入论文的权威结论

### 4.1 高置信结论（可直接写入）

| # | 结论 | 数据支撑 | 支撑 Commit | 支撑 Notes | 谨慎程度 |
|---|------|----------|-------------|------------|----------|
| C1 | VerilogEval-Human 上，Haiku feedback 从 80% 提升至 90% | §2 VerilogEval | pre-midterm | `haiku_main_experiment_summary.md` | 低 |
| C2 | RTLLM STUDY_12 上，feedback 对三模型均有正向增益，GPT-5.4 增益最大 (+33pp) | §2.1 正式实验 | `3338b96` | `rtllm_formal_experiment_summary.md` | 低 |
| C3 | GPT-5.4 的 feedback 优势在 4 轮稳定性实验中 100% 成立 (79.2% ± 4.2%) | §2.3 稳定性 | `8989133` | `rtllm_stability_summary.md` | 低 |
| C4 | Feedback 约 57% 的收益来自错误反馈信息本身，43% 来自多采样 (GPT) | §2.2 消融 | `7655475` | `rtllm_feedback_ablation_summary.md` | 低 |
| C5 | 存在"仅 feedback 能解决"的设计：sequence_detector, traffic_light (GPT) | §2.2 + §2.3 | `7655475` | `rtllm_feedback_ablation_summary.md` | 低 |
| C6 | Feedback 粒度呈倒 U 型，compile-only / succinct 是最优区间 | §2.4 粒度 | `5ccd419` | `rtllm_feedback_granularity_summary.md` | 中 |
| C7 | Rich feedback 可能导致信息过载，反而降低通过率 | §2.4 粒度 | `5ccd419` | `rtllm_feedback_granularity_summary.md` | 中 |

### 4.2 需要谨慎表述的结论

| # | 结论 | 风险点 | 支撑 Commit | 支撑 Notes | 建议表述 |
|---|------|--------|-------------|------------|----------|
| C8 | Feedback 效果具有模型依赖性：Sonnet 上 FB < RO | 稳定但反直觉 | `8989133` | `rtllm_stability_summary.md` | "在本实验设置下，feedback 对 Sonnet 4.6 未产生正向效果，甚至低于 retry-only" |
| C9 | Multi-turn v2 对话式反馈对两模型均 +17pp | 6 题小子集、单次运行 | `e792955` | `rtllm_multiturn_feedback_summary.md` | "在控制候选数后，multi-turn 对话在 6 题子集上展现正向趋势（+17pp），但需更大规模验证" |
| C10 | k=3 多候选选择对 Sonnet 可能有害 (17% < 33%) | 小样本 | `e792955` | `rtllm_multiturn_feedback_summary.md` | "在本实验中观察到 k=3 对 Sonnet 产生候选选择偏差，需谨慎解释" |
| C11 | 粒度倒 U 型结论来自 STUDY_12 + 两模型 | 样本有限 | `5ccd419` | `rtllm_feedback_granularity_summary.md` | "在 RTLLM STUDY_12 和两个模型上观察到" |

### 4.3 不可写入论文的结论

| 结论 | 原因 |
|------|------|
| "Multi-turn 对 GPT 有害 (−50pp)" | ❌ v1 bug 导致的错误结论，已被 v2 取代 |
| "Multi-turn 对 Sonnet 中性" | ❌ v1 结论，v2 显示 +17pp |
| "Single-turn 清洁重置优势" | ❌ v1 叙事，由 bug 驱动 |

---

## 五、审计记录

| 审计项 | 时间 | 结果 |
|--------|------|------|
| `audit_project.py` (代码正确性) | 2026-04-24 23:22 | **PASSED** (24/24 checks) |
| `audit_data.py` (数据一致性) | 2026-04-24 23:22 | **PASSED** (20 runs, 0 inconsistencies) |
| 文档-数据交叉验证 | 2026-04-24 23:22 | **PASSED** (11 项全部匹配) |
| Multi-turn v1 bug 发现与修正 | 2026-04-24 | ✅ 已修正 (commit `e792955`) |

---

## 五bis、结论 → 原始数据完整交叉索引

| 结论 | 原始结果目录 | summary.json | 分析文档 | 图表 | 状态 |
|------|-------------|--------------|----------|------|------|
| C1: Haiku FB +10pp | `outputs/verilogeval_both_20260412_173450.json` | 同左 | `haiku_main_experiment_summary.md` | `haiku_pass_rate_bar.png` | ✅ |
| C2: 三模型 FB 增益 | `rtllm_both_20260422_004806/`, `…011115/`, `…013439/` | 各目录 `summary.json` | `rtllm_formal_experiment_summary.md` | `fig_passrate_comparison.png`, `fig_per_problem_matrix.png` | ✅ |
| C3: GPT FB 稳定 | 4 runs: `rtllm_ablation_20260422_222409/` 等 | 各目录 `summary.json` | `rtllm_stability_summary.md` | `fig_stability_ablation.png` | ✅ |
| C4: FB ≠ 重试 | `rtllm_ablation_20260422_222409/` | `summary.json` | `rtllm_feedback_ablation_summary.md` | `fig_ablation_decomposition.png` | ✅ |
| C5: FB-only 题 | `rtllm_ablation_20260422_222409/` + 4 stability runs | `summary.json` + `details.json` | `rtllm_feedback_ablation_summary.md` | `fig_ablation_comparison.png` | ✅ |
| C6–C7: 粒度倒U | `rtllm_granularity_20260423_212239/`, `…233052/` | `summary.json` | `rtllm_feedback_granularity_summary.md` | `fig_granularity_curve.png` | ✅ |
| C8: Sonnet FB<RO | 4 runs: `rtllm_ablation_20260422_214745/` 等 | `summary.json` | `rtllm_stability_summary.md` | `fig_stability_ablation.png` | ✅ |
| C9: MT +17pp | `rtllm_multiturn_20260424_160853/`, `…181012/` | `summary.json` | `rtllm_multiturn_feedback_summary.md` | `fig_multiturn_comparison_v2.png` | ✅ |
| C10: k=3 害 Sonnet | `rtllm_multiturn_20260424_181012/` | `summary.json` | `rtllm_multiturn_feedback_summary.md` | `fig_multiturn_matrix_v2.png` | ✅ |
| C11: 粒度局限 | 同 C6–C7 | 同上 | 同上 | 同上 | ✅ |

---

## 六、论文推荐引用格式

引用实验结果时，请注明以下信息：

```
数据来源: outputs/runs/rtllm/<run_dir>/summary.json
分析文档: notes/<summary_doc>.md
验证脚本: scripts/audit_data.py
```

### 论文实验章节推荐结构

1. **实验设置** — 引用 STUDY_12 定义 (`rtllm_study12_definition.md`)
2. **主实验结果** — 引用 §2.1 正式实验
3. **消融分析** — 引用 §2.2 消融实验
4. **稳定性验证** — 引用 §2.3 稳定性实验
5. **反馈粒度分析** — 引用 §2.4 粒度实验
6. **多轮对话探索** — 引用 §2.5 Multi-turn v2（注明小子集）
7. **局限性讨论** — 引用 §4.2 谨慎结论 + 天花板题分析
