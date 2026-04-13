# VerilogEval-Human 接入计划

## 数据源

- 仓库：https://github.com/NVlabs/verilog-eval (NVlabs, MIT license)
- 本地路径：`third_party/verilog-eval/`（shallow clone）
- 总题量：156 题
- 本次子集：20 题（easy/medium/hard 混合）

## 数据格式

VerilogEval 每题有 4 个文件（在 `dataset_code-complete-iccad2023/` 目录下）：

| 文件 | 内容 |
|------|------|
| `ProbNNN_name_ifc.txt` | 模块接口声明（`module TopModule(...)；`） |
| `ProbNNN_name_prompt.txt` | 代码补全式 prompt |
| `ProbNNN_name_ref.sv` | 金标准 `RefModule` 实现 |
| `ProbNNN_name_test.sv` | SystemVerilog testbench（引用 `TopModule` + `RefModule`） |

另有 `dataset_spec-to-rtl/` 目录提供纯自然语言描述的 `_prompt.txt`。

## 适配方案

### 关键差异

| 项目 | 自定义任务 | VerilogEval |
|------|-----------|-------------|
| 模块名 | `top_module` | `TopModule` |
| Testbench 语言 | Verilog | SystemVerilog |
| 参考答案 | 内嵌在 testbench | 独立 `_ref.sv` 文件 |
| Mismatch 格式 | `mismatched samples is X out of Y` | 同左（兼容） |

### 适配代码

- `src/runner/verilogeval_loader.py`：
  - 读取 spec-to-rtl `_prompt.txt` → Task.description
  - 读取 `_ifc.txt` → Task.module_header
  - 合并 `_ref.sv` + `_test.sv` → 临时文件 → Task.testbench_path
- `src/runner/verilog_executor.py`：添加 `-g2012` 到 iverilog 命令

### 不需要修改的代码

- `src/feedback/loop_runner.py`：接受 Task 对象，不关心来源
- `src/feedback/prompt_builder.py`：使用 `task.description` + `task.module_header`，自动适配 TopModule
- `src/utils/extract_verilog.py`：regex 匹配任意 module 名
- `src/ranking/ranker.py`：纯数值逻辑

## 20 题子集

### Easy — 组合逻辑 (5 题)
| Problem ID | 描述 |
|-----------|------|
| Prob001_zero | 输出常数 0 |
| Prob007_wire | wire 直连 |
| Prob014_andgate | AND 门 |
| Prob024_hadd | 半加器 |
| Prob027_fadd | 全加器 |

### Easy — 时序逻辑 (3 题)
| Problem ID | 描述 |
|-----------|------|
| Prob031_dff | D 触发器 |
| Prob035_count1to10 | 1-10 计数器 |
| Prob041_dff8r | 8位 DFF + reset |

### Medium — 组合 (3 题)
| Problem ID | 描述 |
|-----------|------|
| Prob025_reduction | 归约运算 |
| Prob022_mux2to1 | 2:1 MUX |
| Prob050_kmap1 | 卡诺图实现 |

### Medium — 时序 (4 题)
| Problem ID | 描述 |
|-----------|------|
| Prob054_edgedetect | 8位边沿检测 |
| Prob068_countbcd | BCD 计数器 |
| Prob082_lfsr32 | 32位 LFSR |
| Prob085_shift4 | 4位移位寄存器 |

### Medium-Hard — 组合 (1 题)
| Problem ID | 描述 |
|-----------|------|
| Prob030_popcount255 | 255位 population count |

### Hard — FSM / 复杂设计 (4 题)
| Problem ID | 描述 |
|-----------|------|
| Prob109_fsm1 | 简单 FSM |
| Prob127_lemmings1 | Lemmings 游戏 FSM |
| Prob140_fsm_hdlc | HDLC 帧协议 FSM |
| Prob144_conwaylife | 16x16 Conway 生命游戏 |

## 运行命令

```bash
# 完整对比（zero-shot + feedback）
python scripts/run_verilogeval_subset.py

# 仅 zero-shot
python scripts/run_verilogeval_subset.py --mode zero-shot

# 仅 feedback
python scripts/run_verilogeval_subset.py --mode feedback

# 指定题目
python scripts/run_verilogeval_subset.py --problems Prob007_wire Prob109_fsm1

# 调参
python scripts/run_verilogeval_subset.py --feedback-k 5 --feedback-iterations 8
```

## 预期结果

- Easy 题：zero-shot 和 feedback 都应该 PASS
- Medium 题：zero-shot 可能部分 FAIL，feedback 应能修复一部分
- Hard 题：zero-shot 大概率 FAIL，feedback 可能修复 1-2 个
- **关键指标**：improved by feedback > 0，证明 feedback loop 有价值
