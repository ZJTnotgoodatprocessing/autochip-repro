# 论文附录规划

> 说明：本文件规划论文附录的结构和内容，后续在 Word 合并时填充具体内容。
> 附录用于说明实验可复现性，不替代正文。

---

## 附录 A：主要实验命令与参数

列出本文全部正式实验的运行命令和关键参数，供读者复现参考。

### A.1 VerilogEval-Human 基线实验

```bash
# Zero-shot + Feedback 对比
python scripts/run_verilogeval_subset.py --mode both
# 参数：temperature=0.7, k=3, max_iterations=5
```

### A.2 RTLLM_STUDY_12 正式实验

```bash
# Haiku（默认模型）
python scripts/run_rtllm_subset.py --subset study12 --mode both

# Sonnet 4.6
python scripts/run_rtllm_subset.py --subset study12 --mode both --model claude-sonnet-4-6

# GPT-5.4
python scripts/run_rtllm_subset.py --subset study12 --mode both --model gpt-5.4
```

### A.3 消融实验（ZS / RO / FB）

```bash
python scripts/run_rtllm_subset.py --subset study12 --mode ablation --model gpt-5.4
python scripts/run_rtllm_subset.py --subset study12 --mode ablation --model claude-sonnet-4-6
```

### A.4 稳定性重复实验

```bash
# 重复运行消融实验 4 次（每次独立 API 调用）
python scripts/run_rtllm_subset.py --subset study12 --mode ablation --model gpt-5.4
# 执行 4 次，每次生成独立 run_id
```

### A.5 反馈粒度实验

```bash
python scripts/run_rtllm_subset.py --subset study12 --mode granularity --model gpt-5.4
python scripts/run_rtllm_subset.py --subset study12 --mode granularity --model claude-sonnet-4-6
```

### A.6 多轮对话反馈实验

```bash
python scripts/run_rtllm_subset.py --subset study12 --mode multiturn --model gpt-5.4 \
    --problems div_16bit sequence_detector LFSR traffic_light freq_divbyfrac fsm
python scripts/run_rtllm_subset.py --subset study12 --mode multiturn --model claude-sonnet-4-6 \
    --problems div_16bit sequence_detector LFSR traffic_light freq_divbyfrac fsm
```

### A.7 提示词策略实验

```bash
python scripts/run_rtllm_subset.py --subset study12 --mode both --model gpt-5.4 \
    --prompt-strategy base
python scripts/run_rtllm_subset.py --subset study12 --mode both --model gpt-5.4 \
    --prompt-strategy cot
python scripts/run_rtllm_subset.py --subset study12 --mode both --model gpt-5.4 \
    --prompt-strategy fewshot
python scripts/run_rtllm_subset.py --subset study12 --mode both --model gpt-5.4 \
    --prompt-strategy fewshot_cot
```

> 注：所有命令中的 API 密钥和服务端点通过 `.env` 文件配置，不在命令行中暴露。

---

## 附录 B：关键实验结果文件索引

以 `notes/authoritative_experiment_index.md` 为准。

| 实验 | 状态 | 数据目录 | 分析文档 |
|------|------|---------|---------|
| VerilogEval 基线 | Authoritative | `outputs/verilogeval_both_*.json` | `notes/haiku_main_experiment_summary.md` |
| RTLLM 正式实验 (Haiku) | Authoritative | `outputs/runs/rtllm/rtllm_both_20260422_004806/` | `notes/rtllm_formal_experiment_summary.md` |
| RTLLM 正式实验 (Sonnet) | Authoritative | `outputs/runs/rtllm/rtllm_both_20260422_011115/` | 同上 |
| RTLLM 正式实验 (GPT) | Authoritative | `outputs/runs/rtllm/rtllm_both_20260422_013439/` | 同上 |
| 消融实验 (GPT) | Authoritative | `outputs/runs/rtllm/rtllm_ablation_20260422_222409/` | `notes/rtllm_feedback_ablation_summary.md` |
| 消融实验 (Sonnet) | Authoritative | `outputs/runs/rtllm/rtllm_ablation_20260422_214745/` | 同上 |
| 稳定性 (GPT ×4) | Authoritative | `outputs/runs/rtllm/rtllm_ablation_2026042[2-3]_*/` | `notes/rtllm_stability_summary.md` |
| 稳定性 (Sonnet ×4) | Authoritative | `outputs/runs/rtllm/rtllm_ablation_2026042[2-3]_*/` | 同上 |
| 粒度实验 | Authoritative | `outputs/runs/rtllm/rtllm_granularity_*/` | `notes/rtllm_feedback_granularity_summary.md` |
| 多轮对话 v2 | Authoritative | `outputs/runs/rtllm/rtllm_multiturn_20260424_*/` | `notes/rtllm_multiturn_feedback_summary.md` |
| 多轮对话 v1 | **Superseded** | — | ❌ 不可引用 |
| 提示词策略 | Authoritative | `outputs/runs/rtllm/rtllm_prompt_strategy_20260425_*/` | `notes/rtllm_prompt_strategy_summary.md` |

---

## 附录 C：核心代码模块索引

| 模块路径 | 功能说明 |
|---------|---------|
| `src/feedback/loop_runner.py` | 反馈循环控制器：单轮/多轮/retry-only 模式、全局最优追踪 |
| `src/feedback/prompt_builder.py` | 提示词构建：初始提示、反馈提示、粒度控制（L2-L4）、策略分发（P0-P3） |
| `src/runner/verilog_executor.py` | Verilog 编译仿真：iverilog 编译、vvp 仿真、双格式输出解析 |
| `src/runner/rtllm_loader.py` | RTLLM benchmark 加载器：目录遍历、module 名提取、testbench 定位 |
| `src/runner/verilogeval_loader.py` | VerilogEval 加载器：ref+test 合并、接口提取 |
| `src/runner/task.py` | 统一 Task 数据结构定义 |
| `src/llm/client.py` | LLM 客户端：统一网关、三级优先级、重试机制、错误分类 |
| `src/ranking/ranker.py` | AutoChip 评分器：编译/仿真结果 → 标量分数 |
| `src/utils/extract_verilog.py` | Verilog 代码提取：正则匹配 module...endmodule |
| `src/utils/artifacts.py` | 实验产物管理：目录创建、元数据记录、Git 信息采集 |
| `scripts/run_rtllm_subset.py` | RTLLM 实验主脚本：支持 --subset/--mode/--model/--prompt-strategy |
| `scripts/run_verilogeval_subset.py` | VerilogEval 实验主脚本 |
| `scripts/audit_project.py` | 代码审计：24 项自动化检查 |
| `scripts/audit_data.py` | 数据审计：从 summary.json 重算通过率并交叉验证 |

---

## 附录 D：图表与结果资产索引

### D.1 可用于论文的图表（`outputs/reports/`）

| # | 文件名 | 主题 | 适合章节 |
|---|--------|------|---------|
| 1 | `haiku_pass_rate_bar.png` | Haiku VerilogEval ZS/FB 通过率 | §5.1 |
| 2 | `fig_passrate_comparison.png` | 三模型 ZS/FB 通过率对比 | §5.2 |
| 3 | `fig_per_problem_matrix.png` | 逐题 PASS/FAIL 矩阵 | §5.2 |
| 4 | `fig_feedback_gain.png` | Feedback 增益柱状图 | §5.2 |
| 5 | `fig_ablation_comparison.png` | ZS/RO/FB 三条件对比 | §5.3 |
| 6 | `fig_ablation_decomposition.png` | 收益分解图 | §5.3 |
| 7 | `fig_stability_ablation.png` | 稳定性三条件误差棒 | §5.4 |
| 8 | `fig_stability_formal.png` | 正式实验重复对比 | §5.4 |
| 9 | `fig_granularity_curve.png` | L0–L4 粒度折线图 | §5.5 |
| 10 | `fig_granularity_matrix.png` | 粒度逐题热力图 | §5.5 |
| 11 | `fig_multiturn_comparison_v2.png` | MT v2 条件对比 | §5.6 |
| 12 | `fig_multiturn_matrix_v2.png` | MT v2 逐题矩阵 | §5.6 |
| 13 | `fig_prompt_strategy_comparison.png` | 4 策略 ZS/FB 对比 | §5.7 |
| 14 | `fig_prompt_strategy_matrix.png` | 策略逐题矩阵 | §5.7 |

### D.2 系统架构图（`report/figures/`）

| # | 文件名 | 主题 | 适合章节 |
|---|--------|------|---------|
| 1 | `fig_system_architecture.png` | 系统总体架构 | §3.1 |
| 2 | `fig_feedback_loop_flow.png` | 反馈循环流程图 | §3.5 |
| 3 | `fig_case_study_repair.png` | 典型修复过程 | §5.8 |

### D.3 不可使用的废弃图表

| 文件名 | 原因 |
|--------|------|
| `fig_multiturn_comparison.png` | Multi-turn v1 废弃版，已被 v2 替代 |
| `fig_multiturn_matrix.png` | Multi-turn v1 废弃版，已被 v2 替代 |
