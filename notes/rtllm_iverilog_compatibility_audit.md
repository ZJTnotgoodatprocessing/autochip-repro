# RTLLM iverilog 兼容性审计报告

> 扫描日期：2026-04-21
> 扫描工具：`scripts/scan_rtllm_iverilog.py`
> iverilog 版本：本机安装版（`-g2012`）
> 方法：对每个设计，读取 verified_*.v 参考文件，修正 module 名后与 testbench.v 一起编译和仿真

---

## 总体结果

| 指标 | 数量 | 百分比 |
|------|------|--------|
| 总设计数 | 50 | 100% |
| 编译通过 | 46 | 92% |
| 仿真通过 | 41 | 82% |
| 编译失败 | 4 | 8% |
| 编译通过但仿真异常 | 5 | 10% |

---

## 编译失败：4 个设计

| 设计 | 类别 | 失败原因 | 修复难度 |
|------|------|---------|---------|
| adder_pipe_64bit | Arithmetic/Adder | testbench 引用了未定义的子模块 | 中（需修改 testbench） |
| multi_pipe_4bit | Arithmetic/Multiplier | testbench 引用了未定义的子模块 | 中 |
| ring_counter | Control/Counter | testbench 使用了 iverilog 不支持的赋值语法 | 低（改赋值方式） |
| asyn_fifo | Memory/FIFO | testbench 使用了 `break` 语句 | 低（改为 `disable`） |

### 失败模式分类

1. **Unknown module reference (2 题)**：testbench 实例化了设计内部的子模块，参考文件未正确导出。可能是参考文件的 module 层次结构与 testbench 期望不一致。
2. **Unsupported feature — `break` (1 题)**：iverilog 不支持 SystemVerilog 的 `break`，可用 `disable` 替代。
3. **Unsupported feature — 赋值语法 (1 题)**：iverilog 对某些 SystemVerilog 赋值形式不支持。

---

## 编译通过但仿真异常：5 个设计

| 设计 | 类别 | 问题 | 说明 |
|------|------|------|------|
| radix2_div | Arithmetic/Divider | ERROR（仿真结果不匹配） | 参考设计本身可能有 bug 或 iverilog 行为差异 |
| calendar | Miscellaneous/Others | `$readmemh` 找不到文件 | testbench 依赖外部 `.dat` 数据文件 |
| alu | Miscellaneous/RISC-V | `$readmemh` 找不到文件 | 同上 |
| clkgenerator | Miscellaneous/RISC-V | 20/20 failures | 参考设计与 testbench 预期不一致 |
| signal_generator | Miscellaneous/Signal generation | `$readmemh` 找不到文件 | 同上 |

---

## 完全可用设计清单（41 题）

以下 41 个设计在当前 iverilog + vvp 环境下**编译+仿真全部通过**：

### Arithmetic (16/19)
- accu, adder_8bit, adder_16bit, adder_32bit, adder_bcd
- comparator_3bit, comparator_4bit
- div_16bit
- multi_8bit, multi_16bit, multi_booth_8bit, multi_pipe_8bit
- fixed_point_adder, fixed_point_substractor, float_multi
- sub_64bit

### Control (5/6)
- counter_12, JC_counter, up_down_counter
- fsm, sequence_detector

### Memory (4/5)
- LIFObuffer
- barrel_shifter, LFSR, right_shifter

### Miscellaneous (16/20)
- freq_div, freq_divbyeven, freq_divbyfrac, freq_divbyodd
- edge_detect, parallel2serial, pulse_detect, serial2parallel, synchronizer, traffic_light, width_8to16
- instr_reg, pe, RAM, ROM
- square_wave

---

## 结论

1. **82% 的 RTLLM 设计可以直接在当前流水线中使用**，无需任何修改
2. 编译失败的 4 题中，2 题是 testbench 子模块引用问题，2 题是 iverilog 语法限制
3. 仿真异常的 5 题中，3 题是外部数据文件缺失，2 题是参考设计问题
4. **对于 RTLLM_CORE_5 子集，应全部从 41 题可用清单中选取**
