# AutoChip 复现 Checklist

## 论文阅读
- [ ] 通读 AutoChip 论文，标注核心 claim
- [ ] 理解 Figure 1 的系统架构：Prompt → LLM → Verilog → Compile → Simulate → Feedback loop
- [ ] 明确论文的评估指标：functional correctness (pass@k)、迭代轮次、token 消耗
- [ ] 整理论文中使用的 HDLBits 题目列表（Table I）

## 环境搭建
- [ ] 克隆 AutoChip 仓库到 `third_party/AutoChip`
- [ ] 阅读原仓库 README，理解代码结构
- [ ] 安装 Python 依赖
- [ ] 安装 Icarus Verilog（iverilog >= 11.0）
- [ ] 配置 `.env` 中的 API key
- [ ] 跑通 AutoChip 自带 demo，截图/日志存入 `logs/`

## 核心复现
- [ ] 确认 HDLBits testbench 文件齐全
- [ ] 使用 GPT-4 跑 baseline（与论文设定一致）
- [ ] 逐题记录结果：pass/fail、迭代次数、生成的 Verilog 代码
- [ ] 汇总 pass rate，与论文 Table 对比
- [ ] 若结果偏差 > 5%，排查原因（API 版本、prompt 差异、随机性）

## 扩展实验
- [ ] 替换为 Claude 后端，复跑相同题目
- [ ] 替换为开源模型（如 CodeLlama / DeepSeek Coder），复跑相同题目
- [ ] 设计 prompt 变体实验（至少 3 种 prompt 策略）
- [ ] 设计反馈粒度实验（编译错误 only / +仿真结果 / +波形 diff）
- [ ] 所有实验结果写入 `outputs/` 并用模板记录到 `report/`

## 报告撰写
- [ ] 整理实验数据，制作对比表格和图表
- [ ] 撰写毕设论文/报告初稿
- [ ] 导师审阅 → 修改 → 定稿
