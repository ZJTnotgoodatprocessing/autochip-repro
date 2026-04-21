# 后中期主线策略：强模型 + 更难 Benchmark 验证 AutoChip 有效性

> 创建日期：2026-04-21
> 目的：为后中期阶段确定主 benchmark、模型路线和实验矩阵设计

---

## 一、Benchmark 选型比较

### 候选 Benchmark 概览

| 维度 | RTLLM 2.0 | CVDP (NVlabs) | VerilogEval-Human (扩展) |
|------|-----------|---------------|-------------------------|
| **来源** | 港科大 (HKUST-ZhiYao) | NVIDIA NVlabs | NVlabs (已在用) |
| **发布时间** | 2024 (ASP-DAC / ICCAD) | 2025-2026 (arXiv) | 2023 (ICCAD) |
| **题目数量** | 50 个设计 | 783 题 (13 类) | 156 题 (已用 20) |
| **题目类型** | spec-to-RTL (纯自然语言→Verilog) | 多种：代码生成/调试/理解/修改 | spec-to-RTL + code-completion |
| **难度范围** | 中高（含流水线乘法器、FSM、RISC-V 子组件、异步 FIFO、浮点运算等） | 最高（含商业级验证场景） | 低到中高 |
| **是否全新 benchmark** | ✅ 本项目从未使用 | ✅ 全新 | ❌ 已在使用 |
| **自然语言规格** | ✅ `design_description.txt` | ✅ JSONL 中的 prompt | ✅ `_prompt.txt` |
| **Testbench** | ✅ `testbench.v`（标准 Verilog） | ✅ 含 test harness（需 Docker） | ✅ `_test.sv` + `_ref.sv` |
| **参考设计** | ✅ `verified_verilog.v` | 部分（初始版本隐藏 reference） | ✅ `_ref.sv` |
| **验证方式** | 编译 + 功能仿真 | Docker 容器化仿真 | 编译 + 功能仿真 |
| **iverilog 兼容性** | ⚠️ 原始用 VCS，但 testbench 为标准 Verilog，**可适配 iverilog** | ❌ 需要 Docker + 商业 EDA（Xcelium） | ✅ 已验证 |
| **接入工作量** | **小**：结构简单，适配 loader 即可 | **大**：需 Docker、特殊 harness、JSONL 解析 | 无（已接入） |
| **对论文说服力** | ★★★★ 全新 benchmark + 更难 + 有学术引用 | ★★★★★ 最新最权威，但接入成本极高 | ★★ 已用过，扩展价值有限 |
| **适合 AutoChip 闭环验证** | ★★★★★ 完美匹配 spec-to-RTL + feedback loop | ★★★ 部分任务适合（code generation），但框架差异大 | ★★★ 已证明，价值有限 |

### 选型结论

#### 🏆 主推荐：RTLLM 2.0

**理由：**

1. **全新 benchmark**：本项目从未使用过 RTLLM，直接回应导师"接入全新更难 benchmark"的要求
2. **难度显著更高**：50 个设计覆盖流水线乘法器、异步 FIFO、LFSR、浮点乘法器、RISC-V 子组件（ALU/ROM/指令寄存器）、序列检测器等，远超 VerilogEval 的 Easy/Medium 主体
3. **完美匹配 AutoChip 研究问题**：纯 spec-to-RTL 任务，每题有自然语言描述 + testbench + 参考设计，与当前 feedback loop 流程完全兼容
4. **接入成本低**：每个设计一个目录，含 `design_description.txt` + `testbench.v` + `verified_verilog.v`，结构比 VerilogEval 更简单
5. **iverilog 可适配**：testbench 为标准 Verilog，原始仅用 VCS 运行，但可通过 iverilog `-g2012` 编译（可能需要少量 testbench 修复）
6. **学术价值**：ASP-DAC 2024 + ICCAD 2024 两篇发表，被广泛引用，在论文中引入可提升学术说服力
7. **分类清晰**：4 大类（算术/存储/控制/杂项）50 个设计，便于做错误分类分析

#### 已验证的 iverilog 兼容性

实际测试结果（2026-04-21，使用 cloned RTLLM 仓库）：

| 设计 | 类别 | iverilog 编译 | 仿真结果 |
|------|------|--------------|---------|
| adder_8bit | Arithmetic/Adder | ✅ 通过 | ✅ Your Design Passed |
| fsm | Control/FSM | ✅ 通过 | ✅ Your Design Passed |
| asyn_fifo | Memory/FIFO | ❌ 失败 | testbench 使用了 `break` 语句，iverilog 不支持 |

结论：大部分 RTLLM 设计与 iverilog 兼容。少数 testbench 使用了 VCS 特有语句（如 `break`），需要逐个修复为 iverilog 兼容写法（将 `break` 替换为 `disable`）。预计需要修复的 testbench 不超过 5 个。

#### 🥈 备选：VerilogEval-Human Hard 子集扩展

如果 RTLLM 接入过程中遇到大量 iverilog 不兼容问题，可回退到从 VerilogEval 156 题中选取更难子集作为补充。但这不应作为主方向。

#### ❌ 不推荐：CVDP

CVDP 虽然是最权威的新 benchmark（783 题、NVlabs 出品），但：
- 需要 Docker 容器化运行环境
- 部分任务需要商业 EDA（Cadence Xcelium）
- 任务类型混杂（调试、理解、修改），不全是 spec-to-RTL
- 接入成本极高，对本科毕设工期不现实
- reference solution 初始版本被隐藏（防数据污染），不利于案例分析

---

## 二、强模型实验路线

### 分层模型矩阵

| 梯队 | 模型 | Provider | 角色 | 特点 |
|------|------|----------|------|------|
| **T1 主验证** | GPT-4o | OpenAI | 主实验强模型 | 当前最强通用模型之一，代码生成能力极强 |
| **T1 主验证** | Claude Sonnet 3.5/4 | Anthropic | 主实验强模型 | 强推理能力，体系内可直接使用 |
| **T2 对照** | Claude Haiku 3.5 | Anthropic | 已有基线 | 已有 VerilogEval 20题实验数据作对照 |
| **T2 对照** | GPT-4o-mini | OpenAI | 轻量级对照 | 成本低，可做大量对比实验 |
| **T3 可选** | DeepSeek-V3/Coder | DeepSeek | 开源对照 | 中国开源模型代表，代码能力强 |

### 核心实验问题

1. **强模型 zero-shot 已很强时，feedback 还有价值吗？**
   - 如果 GPT-4o 在 RTLLM 上 zero-shot 就能通过 40/50，feedback 只提升到 42/50，那贡献有限
   - 如果 zero-shot 只通过 30/50 而 feedback 提升到 40/50，则 feedback 价值清晰

2. **更难 benchmark 是否让 feedback 重新体现价值？**
   - VerilogEval 上 Haiku zero-shot 已 80%，提升空间有限
   - RTLLM 难度更高，预期 zero-shot pass rate 更低，feedback 的提升空间更大

3. **最有说服力的对比**：
   - Haiku + VerilogEval（已有基线）
   - Haiku + RTLLM（弱模型 × 难 benchmark）
   - GPT-4o/Sonnet + VerilogEval（强模型 × 易 benchmark）
   - **GPT-4o/Sonnet + RTLLM（强模型 × 难 benchmark）** ← 最核心

### 推荐实验矩阵

| 实验 | 模型 | Benchmark | 模式 | 优先级 |
|------|------|-----------|------|--------|
| E1 | Claude Haiku 3.5 | RTLLM-2.0 (50题) | zero-shot + feedback | ★★★★ |
| E2 | GPT-4o | RTLLM-2.0 (50题) | zero-shot + feedback | ★★★★★ |
| E3 | Claude Sonnet | RTLLM-2.0 (50题) | zero-shot + feedback | ★★★★ |
| E4 | GPT-4o | VerilogEval-20 | zero-shot + feedback | ★★★ |
| E5 | Haiku 重复实验 | VerilogEval-20 | zero-shot + feedback (×3) | ★★★ |

E2 和 E1 优先执行，可形成 **"强模型 vs 弱模型 × 难 benchmark"** 的完整对比。

---

## 三、工程实现计划

### 3.1 RTLLM 接入方案

#### 每个 RTLLM 设计目录结构：
```
RTLLM/
├── Arithmetic/
│   ├── adder_8bit/
│   │   ├── design_description.txt   ← 自然语言描述（映射到 Task.description）
│   │   ├── testbench.v              ← testbench（映射到 Task.testbench_path）
│   │   ├── verified_verilog.v       ← 参考答案
│   │   └── LLM_generated_verilog.v  ← LLM 生成结果（不需要）
│   ├── adder_16bit/
│   │   └── ...
│   └── ...
├── Memory/
├── Control/
└── Miscellaneous/
```

#### 适配要点：
1. **Task 映射**：`design_description.txt` → `Task.description`，但需从中提取 module interface（RTLLM 描述中包含 I/O 定义）
2. **Module 名**：RTLLM 不像 VerilogEval 使用 `TopModule`，每个设计有独立 module 名
3. **Testbench 兼容性**：原始用 VCS，需验证 iverilog 兼容性（可能需要 `-g2012` 或少量修改）
4. **Pass/Fail 判断**：RTLLM testbench 输出 `===========Your Design Passed===========` 或 `===========Error===========`

#### 新增文件：
- `src/runner/rtllm_loader.py` — RTLLM benchmark 加载器
- `scripts/run_rtllm_subset.py` — RTLLM 实验运行脚本

### 3.2 多 Provider 支持

#### 架构设计：
```
src/llm/
├── __init__.py
├── base.py          ← LLMProvider 抽象基类 [NEW]
├── anthropic.py     ← Anthropic 实现（从 client.py 重构） [NEW]
├── openai_provider.py  ← OpenAI 实现 [NEW]
├── client.py        ← 保持向后兼容，作为 facade [MODIFY]
└── config.py        ← Provider 配置管理 [NEW]
```

#### 关键设计：
- `LLMProvider` 基类定义 `generate()` 和 `generate_with_history()` 接口
- `client.py` 的 `generate()` 等函数保持原签名不变，内部代理到对应 provider
- 通过 `.env` 中 `LLM_PROVIDER=anthropic|openai|deepseek` 切换
- 保持对现有脚本的 100% 向后兼容

---

## 四、执行顺序建议

### 第 1 步（本轮）：工程基础
- [x] 创建策略文档
- [ ] 实现 LLM provider 抽象层（保持向后兼容）
- [ ] Clone RTLLM 到 third_party/，验证 iverilog 兼容性
- [ ] 实现 rtllm_loader.py skeleton

### 第 2 步（下一轮）：RTLLM 接入打通
- 完成 rtllm_loader.py，适配 testbench 输出解析
- 在 2-3 个简单 RTLLM 设计上验证全流程（Haiku zero-shot + feedback）
- 修复 iverilog 兼容性问题

### 第 3 步：RTLLM 全量实验
- E1: Haiku × RTLLM-50
- E2: GPT-4o × RTLLM-50（需 OpenAI provider 就绪）

### 第 4 步：交叉对比与结果整理
- E3-E5 实验
- 结果可视化、论文素材整理

---

## 五、为什么 RTLLM 优先于 Haiku 重复实验

| 维度 | RTLLM 主线 | Haiku 重复实验 |
|------|-----------|---------------|
| **研究价值** | 高——验证 AutoChip 在全新、更难 benchmark 上的有效性 | 低——仅证明已有结论的统计稳定性 |
| **导师建议匹配** | 完美匹配"更强模型 + 更难 benchmark" | 不匹配 |
| **论文贡献** | 可作为论文核心实验 | 仅作为补充实验/附录 |
| **答辩说服力** | "我们在全新 benchmark 上验证了框架" | "我们重复跑了已有实验" |

**结论**：Haiku 重复实验仍值得做（放在 E5），但应在 RTLLM 主线启动后并行完成，不应阻塞主线。
