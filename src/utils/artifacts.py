from __future__ import annotations

import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def timestamp_now() -> str:
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def make_run_id(prefix: str, timestamp: str | None = None) -> str:
    return f"{prefix}_{timestamp or timestamp_now()}"


def create_run_dir(category: str, run_id: str) -> Path:
    return ensure_dir(PROJECT_ROOT / "outputs" / "runs" / category / run_id)


def _run_git(args: list[str]) -> str | None:
    try:
        completed = subprocess.run(
            ["git", *args],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        return completed.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_git_metadata() -> dict[str, Any]:
    commit = _run_git(["rev-parse", "HEAD"])
    branch = _run_git(["rev-parse", "--abbrev-ref", "HEAD"])
    status = _run_git(["status", "--short"])
    return {
        "commit": commit,
        "branch": branch,
        "dirty": bool(status),
    }


def _json_safe(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, dict):
        return {k: _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    return value


def build_run_metadata(
    *,
    run_id: str,
    script_path: str,
    model_name: str,
    timestamp: str,
    run_kind: str,
    parameters: dict[str, Any],
    source_inputs: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "run_id": run_id,
        "timestamp": timestamp,
        "script": script_path,
        "run_kind": run_kind,
        "argv": sys.argv,
        "model_name": model_name,
        "parameters": _json_safe(parameters),
        "source_inputs": _json_safe(source_inputs or {}),
        "git": get_git_metadata(),
        "runtime": {
            "python_version": sys.version,
            "platform": platform.platform(),
        },
    }


def find_latest_file(patterns: list[str], base_dir: Path | None = None) -> Path | None:
    root = base_dir or PROJECT_ROOT
    candidates: list[Path] = []
    for pattern in patterns:
        candidates.extend(path for path in root.glob(pattern) if path.is_file())
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)
