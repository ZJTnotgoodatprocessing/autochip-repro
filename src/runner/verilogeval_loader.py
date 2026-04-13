"""VerilogEval-Human benchmark loader.

Reads problems from the cloned NVlabs/verilog-eval repository and returns
Task objects compatible with the existing pipeline.

Expected repo layout (third_party/verilog-eval/):
  dataset_code-complete-iccad2023/
    ProbNNN_name_ifc.txt      # module interface (TopModule header)
    ProbNNN_name_ref.sv       # RefModule (golden solution)
    ProbNNN_name_test.sv      # testbench (expects TopModule + RefModule)
  dataset_spec-to-rtl/
    ProbNNN_name_prompt.txt   # natural-language specification
"""

from pathlib import Path
from src.runner.task import Task


_DEFAULT_REPO = Path(__file__).resolve().parent.parent.parent / "third_party" / "verilog-eval"
_CC_DIR = "dataset_code-complete-iccad2023"
_STR_DIR = "dataset_spec-to-rtl"
_COMBINED_DIR_NAME = "_combined_testbenches"


def _ensure_combined_dir(repo_dir: Path) -> Path:
    """Create (if needed) the directory for combined ref+test files."""
    d = repo_dir / _COMBINED_DIR_NAME
    d.mkdir(exist_ok=True)
    return d


def load_verilogeval_task(problem_id: str, repo_dir: Path | None = None) -> Task:
    """Load a single VerilogEval problem as a Task.

    Args:
        problem_id: e.g. "Prob007_wire" or "Prob109_fsm1"
        repo_dir: path to cloned verilog-eval repo (default: third_party/verilog-eval)
    """
    repo = (repo_dir or _DEFAULT_REPO).resolve()
    cc = repo / _CC_DIR
    s2r = repo / _STR_DIR

    # ── description: prefer spec-to-rtl (pure NL), fallback to code-complete ──
    desc_path_s2r = s2r / f"{problem_id}_prompt.txt"
    desc_path_cc = cc / f"{problem_id}_prompt.txt"

    if desc_path_s2r.exists():
        description = desc_path_s2r.read_text(encoding="utf-8").strip()
    elif desc_path_cc.exists():
        description = desc_path_cc.read_text(encoding="utf-8").strip()
    else:
        raise FileNotFoundError(f"No prompt file for {problem_id}")

    # ── module header ──
    ifc_path = cc / f"{problem_id}_ifc.txt"
    if not ifc_path.exists():
        raise FileNotFoundError(f"Missing interface file: {ifc_path}")
    module_header = ifc_path.read_text(encoding="utf-8").strip()

    # ── combined testbench: ref.sv + test.sv ──
    ref_path = cc / f"{problem_id}_ref.sv"
    test_path = cc / f"{problem_id}_test.sv"
    for p in (ref_path, test_path):
        if not p.exists():
            raise FileNotFoundError(f"Missing file: {p}")

    combined_dir = _ensure_combined_dir(repo)
    combined_path = combined_dir / f"{problem_id}_combined_test.sv"

    # Re-create combined file each time (cheap, guarantees freshness)
    ref_content = ref_path.read_text(encoding="utf-8")
    test_content = test_path.read_text(encoding="utf-8")
    combined_path.write_text(ref_content + "\n" + test_content, encoding="utf-8")

    return Task(
        name=problem_id,
        description=description,
        module_header=module_header,
        testbench_path=combined_path.resolve(),
    )


def list_problems(repo_dir: Path | None = None) -> list[str]:
    """Return sorted list of all available problem IDs."""
    repo = (repo_dir or _DEFAULT_REPO).resolve()
    cc = repo / _CC_DIR
    ids = set()
    for f in cc.glob("*_ifc.txt"):
        # Prob007_wire_ifc.txt -> Prob007_wire
        ids.add(f.name.removesuffix("_ifc.txt"))
    return sorted(ids)
