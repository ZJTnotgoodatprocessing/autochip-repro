"""Task loader — reads a benchmark problem directory."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Task:
    name: str
    description: str
    module_header: str
    testbench_path: Path


def load_task(task_dir: str | Path) -> Task:
    """Load a task from a directory containing description.txt,
    module_header.v, and testbench.v."""
    d = Path(task_dir)
    if not d.is_dir():
        raise FileNotFoundError(f"Task directory not found: {d}")

    desc_file = d / "description.txt"
    header_file = d / "module_header.v"
    tb_file = d / "testbench.v"

    for f in (desc_file, header_file, tb_file):
        if not f.exists():
            raise FileNotFoundError(f"Missing required file: {f}")

    return Task(
        name=d.name,
        description=desc_file.read_text(encoding="utf-8").strip(),
        module_header=header_file.read_text(encoding="utf-8").strip(),
        testbench_path=tb_file.resolve(),
    )
