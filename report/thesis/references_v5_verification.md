# v5 新增参考文献核验记录

> 日期：2026-05-08
> 新增数量：6条（从17条增至23条）
> 核验方式：通过 arXiv / IEEE 官方页面 / 项目文档 URL 逐条确认

---

## 新增文献核验

| # | BibTeX key | 标题 | 核验来源 | 状态 |
|---|-----------|------|---------|------|
| 1 | `transformer` | Attention Is All You Need (Vaswani et al., NeurIPS 2017) | [arXiv:1706.03762](https://arxiv.org/abs/1706.03762) | ✅ 已确认 |
| 2 | `codex` | Evaluating Large Language Models Trained on Code (Chen et al., 2021) | [arXiv:2107.03374](https://arxiv.org/abs/2107.03374) | ✅ 已确认 |
| 3 | `instructgpt` | Training Language Models to Follow Instructions with Human Feedback (Ouyang et al., NeurIPS 2022) | [arXiv:2203.02155](https://arxiv.org/abs/2203.02155) | ✅ 已确认 |
| 4 | `codellama` | Code Llama: Open Foundation Models for Code (Rozière et al., 2023) | [arXiv:2308.12950](https://arxiv.org/abs/2308.12950) | ✅ 已确认 |
| 5 | `ieee1364` | IEEE Standard for Verilog Hardware Description Language (IEEE Std 1364-2005) | [IEEE SA](https://standards.ieee.org/ieee/1364/) | ✅ 已确认 |
| 6 | `yosys` | Yosys — A Free Verilog Synthesis Suite (Wolf & Glaser, Austrochip 2013) | [YosysHQ Docs](https://yosyshq.readthedocs.io/projects/yosys/) | ✅ 已确认 |

---

## 各文献在正文中的引用位置

| BibTeX key | 引用章节 | 引用上下文 |
|-----------|---------|----------|
| `transformer` | §2.2.1, §2.8 | Transformer架构基础 |
| `codex` | §2.2.1, §2.4.3, §2.8 | Codex/HumanEval/pass@k评估方法 |
| `instructgpt` | §2.2.2, §2.8 | RLHF/指令跟随对齐 |
| `codellama` | §2.2.1 | 开源代码模型 |
| `ieee1364` | §2.1.1, §2.3.1, §2.8 | Verilog语言标准 |
| `yosys` | §2.3.1, §2.8 | 开源EDA综合工具 |

---

## 核验说明

1. 全部6条文献均通过访问其官方页面（arXiv abstract / IEEE SA / YosysHQ docs）确认标题、作者、年份和出处信息。
2. 无捏造信息。
3. 所有新增文献在正文中均有实际引用，非凑数。
4. BibTeX 编译无 warning。
