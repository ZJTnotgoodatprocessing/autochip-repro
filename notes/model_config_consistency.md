# 模型配置一致性说明

## 统一后的方案（2026-04-13 更新）

| 项目 | 值 |
|------|-----|
| 环境变量名 | `ANTHROPIC_MODEL` |
| 默认值常量 | `src.llm.client.DEFAULT_MODEL = "claude-haiku-4-5-20251001"` |
| 读取函数 | `src.llm.client.get_model_name()` |
| 配置文件 | `.env` 中的 `ANTHROPIC_MODEL=...` |

## 优先级链

```
命令行 --model > 环境变量 ANTHROPIC_MODEL > DEFAULT_MODEL 常量
```

## 使用方式

所有脚本和模块统一通过 `get_model_name()` 获取模型名：

```python
from src.llm.client import get_model_name
model = get_model_name()  # 读 ANTHROPIC_MODEL 环境变量，无则用 DEFAULT_MODEL
```

`generate()` 和 `generate_with_history()` 内部也使用 `get_model_name()`，
调用方无需手动传 model 参数（除非刻意覆盖）。

所有主要脚本支持 `--model` 参数，通过提前设置 `os.environ["ANTHROPIC_MODEL"]`
来覆盖环境变量，从而影响所有下游 `get_model_name()` 调用。

## 切换实验模型的方法

| 方法 | 命令示例 |
|------|----------|
| 改 `.env`（最常用） | 编辑 `.env` 中 `ANTHROPIC_MODEL=新模型名` |
| 命令行覆盖（单次） | `python scripts/run_verilogeval_subset.py --model 新模型名` |
| 临时环境变量 | `ANTHROPIC_MODEL=新模型名 python scripts/run_verilogeval_subset.py` |

## 改动记录

### 2026-04-13 更新
- `DEFAULT_MODEL` 从 `claude-opus-4-6` 改为 `claude-haiku-4-5-20251001`，与 `.env` 保持一致
- `.env.example` 同步更新为 `claude-haiku-4-5-20251001`
- 5 个主要脚本新增 `--model` CLI 参数支持：
  - `scripts/run_verilogeval_subset.py`
  - `scripts/run_feedback_loop.py`
  - `scripts/run_single_task.py`
  - `scripts/run_small_batch.py`
  - `scripts/compare_zero_shot_vs_feedback.py`

### 2026-04-10 初始统一
- 之前状态：`os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-6")` 在 7 处硬编码
- 之后状态：默认值集中定义在 `src/llm/client.py:DEFAULT_MODEL`，所有消费方通过 `get_model_name()` 读取

涉及文件：
- `src/llm/client.py` — 定义 `DEFAULT_MODEL` + `get_model_name()`
- `src/feedback/loop_runner.py` — 改用 `get_model_name()`
- `scripts/run_single_task.py` — 改用 `get_model_name()`
- `scripts/run_small_batch.py` — 改用 `get_model_name()`
- `scripts/run_feedback_loop.py` — 改用 `get_model_name()`
