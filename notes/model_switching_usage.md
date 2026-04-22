# 如何切换模型：项目标准用法

> 创建日期：2026-04-21
> 最后更新：2026-04-22
> 适用范围：所有实验脚本（run_rtllm_subset.py, run_verilogeval_subset.py 等）

---

## 推荐方式：使用 `--model` 参数

```bash
# 使用默认模型（Haiku）
python scripts/run_rtllm_subset.py --subset study12

# 切换到其他模型 —— 只需改 --model，不需要改 key 或 base_url
python scripts/run_rtllm_subset.py --subset study12 --model claude-sonnet-4-6
python scripts/run_rtllm_subset.py --subset study12 --model gpt-5.4
python scripts/run_rtllm_subset.py --subset study12 --model gemini-2.5-pro
```

**原理**：`--model` 参数在脚本内部设置 `os.environ["LLM_MODEL"]`，优先级高于 `.env` 中的 `ANTHROPIC_MODEL`。完整优先级链：`LLM_MODEL` > `ANTHROPIC_MODEL` > 代码默认值。

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

只需通过 `--model` 传入不同模型名称即可切换模型，**无需更换 key 或 base_url**。

---

## Relay 可用模型目录（权威列表）

> **重要**：以下模型名称由用户在 relay 平台上确认提供，是唯一正确的名称。
> 不要自行编造或猜测模型名称——relay 的命名可能与官方命名不同。

### Anthropic 系列

| Relay 模型名 | 对应模型 | 实验验证 |
|-------------|---------|---------|
| `claude-haiku-4-5-20251001` | Claude Haiku 4.5 | ✅ RTLLM STUDY_12: ZS 42%, FB 50% |
| `claude-sonnet-4-5-20250929` | Claude Sonnet 4.5 | ✅ RTLLM smoke: 1/2 PASS |
| `claude-sonnet-4-6` | Claude Sonnet 4.6 | ✅ RTLLM STUDY_12: ZS 42%, FB 58% |
| `claude-opus-4-6` | Claude Opus 4.6 | 未验证 |

### OpenAI 系列

| Relay 模型名 | 对应模型 | 实验验证 |
|-------------|---------|---------|
| `gpt-5.4` | GPT-5.4 | ✅ RTLLM STUDY_12: ZS 50%, FB 83% |

### Google 系列

| Relay 模型名 | 对应模型 | 实验验证 |
|-------------|---------|---------|
| `gemini-2.5-pro` | Gemini 2.5 Pro | 未验证 |
| `gemini-3-flash-preview` | Gemini 3 Flash (Preview) | 未验证 |
| `gemini-3-pro-preview` | Gemini 3 Pro (Preview) | 未验证 |
| `gemini-3.1-pro-preview` | Gemini 3.1 Pro (Preview) | 未验证 |

### 其他模型

| Relay 模型名 | 对应模型 | 实验验证 |
|-------------|---------|---------|
| `deepseek-v3.2` | DeepSeek V3.2 | 未验证 |
| `kimi-k2.5` | Kimi K2.5 (Moonshot) | 未验证 |
| `glm5` | GLM-5 (智谱) | 未验证 |

### 已知过期/不可用的模型名

以下名称在 relay 上返回 `model_not_found`，**不要使用**：

- ~~`gpt-4o`~~ → 应使用 `gpt-5.4`
- ~~`gpt-5.2`~~ → 已被 `gpt-5.4` 取代
- ~~`claude-sonnet-4-20250514`~~ → 应使用 `claude-sonnet-4-6`
- ~~`claude-3-5-sonnet-20241022`~~ → 过旧命名

---

## 已支持 `--model` 的脚本

| 脚本 | `--model` 支持 |
|------|---------------|
| `scripts/run_rtllm_subset.py` | ✅ |
| `scripts/run_verilogeval_subset.py` | ✅ |

---

## 后续实验推荐模型选择

### 已完成正式实验矩阵

| 模型 | RTLLM STUDY_12 ZS | RTLLM STUDY_12 FB | 改善题数 |
|------|-------------------|-------------------|---------|
| `claude-haiku-4-5-20251001` | 42% | 50% | 2 |
| `claude-sonnet-4-6` | 42% | 58% | 2 |
| `gpt-5.4` | 50% | 83% | 4 |

### 扩展实验推荐

| 实验角色 | 推荐模型 | 理由 |
|---------|---------|------|
| **默认基线** | `claude-haiku-4-5-20251001` | 已有 VerilogEval + RTLLM 完整基线 |
| **跨厂商扩展** | `gemini-2.5-pro` / `deepseek-v3.2` | 验证框架跨厂商泛化能力 |
| **最强模型** | `claude-opus-4-6` | Anthropic 旗舰，预期更强 |

### 快速验证连通性

```bash
python scripts/run_rtllm_subset.py --problems adder_8bit --mode zero-shot --model <model_name>
```
