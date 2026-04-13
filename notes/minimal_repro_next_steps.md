# 最小复现 — 下一步操作

## 前置条件

### 1. 安装 Python 依赖
```bash
cd autochip-repro
pip install -r requirements.txt
```

### 2. 安装 Icarus Verilog
- Windows: 从 https://bleyer.org/icarus/ 下载安装包
- 安装后确认 `iverilog` 和 `vvp` 在 PATH 中：
```bash
iverilog -v
vvp -v
```

### 3. 配置 API
```bash
cp .env.example .env
```
编辑 `.env`，填入：
- `ANTHROPIC_API_KEY` — 你的中转站 API key
- `ANTHROPIC_BASE_URL` — 中转站地址（如 `https://xxx.example.com`）
- `ANTHROPIC_MODEL` — 使用的模型（默认 `claude-opus-4-6`）

## 验证步骤

### Step 1: 验证 API 连通性
```bash
python scripts/test_model_connection.py
```
预期输出：`Connection OK`

### Step 2: 跑通单任务
```bash
python scripts/run_single_task.py --task data/sample_task
```
预期输出：
```
[Task] sample_task
[LLM] Generating Verilog...
[Compile] OK
[Sim] mismatches=0, total=4, passed=True
[Rank] 1.0
[RESULT] PASS
```

## 跑通后下一步

1. **加入 feedback loop** — 编译/仿真失败时，把错误信息反馈给 LLM，再生成
2. **接入 VerilogEval benchmark** — 将真正的 benchmark 题目放入 `data/`
3. **支持多 candidate (k>1)** — 一次生成 k 个候选，选 rank 最高的
