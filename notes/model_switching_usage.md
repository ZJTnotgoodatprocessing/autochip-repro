# 如何切换模型：项目标准用法

> 创建日期：2026-04-21
> 适用范围：所有实验脚本（run_rtllm_subset.py, run_verilogeval_subset.py 等）

---

## 推荐方式：使用 `--model` 参数

```bash
# 使用默认模型（Haiku）
python scripts/run_rtllm_subset.py --subset core5

# 切换到其他模型 —— 只需改 --model，不需要改 key 或 base_url
python scripts/run_rtllm_subset.py --subset core5 --model claude-sonnet-4-5-20250929
python scripts/run_rtllm_subset.py --subset core5 --model gpt-5.2
```

**原理**：`--model` 参数在脚本内部会设置 `os.environ["ANTHROPIC_MODEL"]`，从而覆盖 `.env` 中的默认值。所有下游模块（`src/llm/client.py`）读取 `ANTHROPIC_MODEL` env var 来决定 model 名。

---

## 为什么不推荐手动改 `.env`

1. `.env` 中的 `ANTHROPIC_MODEL` 是**全局默认值**，改了会影响所有脚本
2. 每次实验切换模型都改 `.env` 容易遗忘恢复，导致后续实验用错模型
3. `--model` 只影响当次运行，不会留下副作用
4. 实验结果 JSON 中会记录实际使用的 model name，便于溯源

---

## 当前环境说明

### 统一 API Relay

本项目通过第三方 API 网关（relay）统一访问各模型。配置方式：

```env
# .env 中固定配置（不需要改）
ANTHROPIC_API_KEY=sk-ant-...    # relay 统一 key
ANTHROPIC_BASE_URL=https://...  # relay 统一入口
ANTHROPIC_MODEL=claude-haiku-4-5-20251001  # 默认模型
```

理论上，只需通过 `--model` 传入不同模型名称即可切换模型，**无需更换 key 或 base_url**。

### 当前已验证可用的模型

| 模型名 | 状态 | 验证结果 | 验证时间 |
|--------|------|---------|--------|
| `claude-haiku-4-5-20251001` | ✅ 可用 | RTLLM CORE_5: ZS 60%, FB 80% | 2026-04-21 |
| `claude-sonnet-4-5-20250929` | ✅ 可用 | RTLLM smoke: 1/2 PASS (multi_booth_8bit) | 2026-04-21 |
| `gpt-5.2` | ✅ 可用 | RTLLM smoke: 2/2 PASS (adder_8bit + multi_booth_8bit) | 2026-04-21 |

> **注意**：relay 的模型命名可能与官方模型名不同。当前确认的名称：
> - Sonnet → `claude-sonnet-4-5-20250929`（不是 `claude-sonnet-4-20250514`）
> - GPT → `gpt-5.2`（不是 `gpt-4o`）

---

## 已支持 `--model` 的脚本

| 脚本 | `--model` 支持 |
|------|---------------|
| `scripts/run_rtllm_subset.py` | ✅ |
| `scripts/run_verilogeval_subset.py` | ✅ |
| `scripts/run_single_task.py` | 待确认 |
| `scripts/run_small_batch.py` | 待确认 |

---

## 后续强模型实验的准备步骤

1. **确认 relay 可用模型列表**：联系第三方 relay 提供商，查询当前 group 下可用的模型
2. **开通所需模型**：如果有 group 限制，申请为 GPT-4o / Sonnet 等开通 channel
3. **验证连通性**：用以下命令快速验证：
   ```bash
   python scripts/run_rtllm_subset.py --problems adder_8bit --mode zero-shot --model <model_name>
   ```
4. **执行正式实验**：确认可用后，跑完整 CORE_5 或更大子集
