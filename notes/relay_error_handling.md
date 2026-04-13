# 中转站 API 错误处理机制

## 问题背景

使用第三方中转站（relay/distributor）调用 LLM API 时，会遇到中转站层面的错误：
- `503 model_not_found: No available channel for model ... under group auto (distributor)`
- 连接超时、网关错误 (502/503)
- 速率限制 (429)

这些是**瞬态错误**，不代表模型能力失败，不应计入实验 FAIL 统计。

## 重试机制

**位置**: `src/llm/client.py`

| 参数 | 值 |
|------|-----|
| 最大重试次数 | 3 |
| 退避间隔 | 2s → 5s → 10s |
| 可重试错误类型 | 429, 502, 503, 529, `model_not_found`, `no available channel`, 连接错误 |

所有 LLM 调用（`generate()`, `generate_with_history()`）自动重试，对上层代码透明。

## 错误区分

重试耗尽后抛出 `APIError`，携带：
- `error_type`: `model_not_found`, `http_503`, `connection_error`, `timeout`, `unknown`
- `original`: 原始异常对象

### 数据结构中的字段

**CandidateResult** (每个候选):
```
api_error: bool
api_error_type: str | None
api_error_message: str | None
```

**FeedbackLoopResult** (整个 loop):
```
api_error: bool          # 当所有候选都因 API 错误失败时为 True
api_error_type: str | None
api_error_message: str | None
```

### 汇总脚本中的字段

**run_verilogeval_subset.py** 输出 JSON:
```json
{
  "zero_shot_valid_runs": 18,
  "zero_shot_api_errors": 2,
  "zero_shot_pass": 15,
  "feedback_valid_runs": 18,
  "feedback_api_errors": 2,
  "feedback_pass": 17
}
```

每行结果:
```json
{
  "task_name": "Prob031_dff",
  "zs_passed": false,
  "zs_rank": -2.0,
  "zs_api_error": true,
  "zs_api_error_type": "model_not_found"
}
```

## 重跑 API 错误题目

```bash
# 从上次结果中提取 API 错误的题目并重跑
python scripts/run_verilogeval_subset.py --retry-from outputs/verilogeval_both_20260410_xxxx.json

# 或手动指定题目
python scripts/run_verilogeval_subset.py --problems Prob024_hadd Prob031_dff Prob035_count1to10
```

`--retry-from` 会自动：
1. 从 JSON 中识别 `zs_api_error=true` 或 `fb_api_error=true` 的题目
2. 只重跑这些题目
3. 将结果合并回完整结果集
4. 输出新的 JSON/CSV

## 统计规则

- **valid_runs** = 总题数 - API 错误数
- **pass rate** 仅基于 valid_runs 计算
- API 错误题目在表格中显示为 `API_ERR(类型)` 而非 `FAIL(-2.00)`
- `improved` 只在 zero-shot 是真实 FAIL（非 API 错误）且 feedback 是 PASS 时才为 True
