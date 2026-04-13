# 单任务验证记录

## 验证时间
2026-04-10

## 验证结果
```
Task:     sample_task (simple wire: in → out)
Compile:  OK (无错误/无警告)
Sim:      mismatches=0, total=4, passed=True
Rank:     1.0
Result:   PASS
Output:   outputs/sample_task_20260410_011941.json
```

## LLM 生成的代码
```verilog
module top_module(input in, output out);
    assign out = in;
endmodule
```

## 已验证的 pipeline 步骤
1. task.py:load_task() — 正确加载 description + module_header + testbench 路径
2. client.py:generate() — Anthropic SDK 通过中转站成功调用
3. extract_verilog.py:extract_modules() — 正确从 LLM 回复中提取 module...endmodule
4. verilog_executor.py:compile() — iverilog 编译成功，临时文件写入正常
5. verilog_executor.py:simulate() — vvp 仿真成功，正确解析 "mismatched samples is 0 out of 4"
6. ranker.py:rank() — 正确计算 (4-0)/4 = 1.0
7. JSON 输出 — 结构完整，字段齐全

## 当前覆盖 vs 论文流程

| 论文步骤 | 状态 | 代码位置 |
|----------|------|----------|
| 输入 prompt + testbench | 已实现 | runner/task.py |
| LLM 生成候选 | 已实现(k=1) | llm/client.py |
| Response 解析 | 已实现 | utils/extract_verilog.py |
| iverilog 编译 | 已实现 | runner/verilog_executor.py:compile() |
| vvp 仿真 | 已实现 | runner/verilog_executor.py:simulate() |
| 排名打分 | 已实现 | ranking/ranker.py |
| **Feedback loop** | **未实现** | 编译/仿真失败时直接 exit，未反馈 |
| **Feedback builder** | **未实现** | 缺少错误信息格式化模块 |
| **多轮对话历史** | **未实现** | client.py 仅支持单条 message |
| 多候选 (k>1) | 未实现 | 当前仅生成 1 个 |

## 下一阶段：加 Feedback Loop

理由：feedback loop 是 AutoChip 的核心创新，缺了它就不算复现。批量运行只是外层 for 循环，优先级低。

### 需要改动的文件

1. **src/llm/client.py**
   - 新增 `generate_with_history(messages: list[dict]) -> str`
   - 支持多轮对话（传入完整 conversation history）

2. **新增 src/feedback/builder.py**
   - `build_feedback(code, compile_result, sim_result) -> str`
   - succinct 模式：只给关键错误信息

3. **新增 scripts/run_single_task_iterative.py** （或改造现有 run_single_task.py）
   - 主循环：generate → compile → simulate → rank → 未通过？→ build feedback → 追加到 history → 再 generate
   - 终止条件：rank == 1.0 或 迭代次数达到 MAX_ITERATIONS

### 验证方式
找一道 LLM 大概率一次做不对的题目（如带状态机的 sequential circuit），观察是否能通过迭代修复。
