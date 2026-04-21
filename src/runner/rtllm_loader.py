"""RTLLM benchmark loader.

Loads design problems from the RTLLM 2.0 repository structure.
Each design has:
  - design_description.txt  (natural language spec → prompt)
  - testbench.v             (simulation testbench)
  - verified_*.v or *.v     (reference design, for analysis only)

Output format: RTLLM testbenches print
  ===========Your Design Passed===========
  ===========Test completed with N /M failures===========
  ===========Error===========
"""

import re
from dataclasses import dataclass, field
from pathlib import Path

# Default RTLLM root under third_party
_DEFAULT_RTLLM_ROOT = Path(__file__).resolve().parent.parent.parent / "third_party" / "RTLLM"

# The four RTLLM category directories
_CATEGORIES = ["Arithmetic", "Memory", "Control", "Miscellaneous"]


@dataclass
class RTLLMProblem:
    """A single RTLLM design problem."""
    name: str                   # e.g. "adder_8bit"
    category: str               # e.g. "Arithmetic/Adder"
    description: str            # contents of design_description.txt
    module_name: str            # extracted module name from description
    testbench_path: Path        # absolute path to testbench.v
    reference_path: Path | None # absolute path to verified_*.v (may not exist)
    design_dir: Path            # absolute path to the design directory


def _extract_module_name(description: str) -> str:
    """Extract module name from RTLLM design_description.txt.

    RTLLM descriptions typically contain:
        Module name:
            module_name_here
    """
    # Match "Module name:" followed by the actual name on the next line
    m = re.search(r"Module\s+name\s*:\s*\n?\s*(\w+)", description, re.IGNORECASE)
    if m:
        return m.group(1).strip()

    # Fallback: look for a line that is just a single identifier after "Module name:"
    for i, line in enumerate(description.splitlines()):
        if "module name" in line.lower():
            # Check the next line for the name
            lines = description.splitlines()
            if i + 1 < len(lines):
                candidate = lines[i + 1].strip()
                if re.match(r"^\w+$", candidate):
                    return candidate
    return "top_module"  # last resort fallback


def _find_reference(design_dir: Path) -> Path | None:
    """Find the reference (verified) Verilog file in a design directory."""
    # RTLLM naming: verified_<name>.v or verified_verilog.v
    for p in design_dir.glob("verified_*.v"):
        return p
    # Some designs might just have a single non-testbench .v file
    for p in design_dir.glob("*.v"):
        if p.name != "testbench.v":
            return p
    return None


def discover_all(rtllm_root: Path | None = None) -> list[RTLLMProblem]:
    """Discover all RTLLM design problems by walking category directories.

    Args:
        rtllm_root: Path to the RTLLM repo root. Defaults to third_party/RTLLM.

    Returns:
        List of RTLLMProblem instances, sorted by category then name.
    """
    root = Path(rtllm_root or _DEFAULT_RTLLM_ROOT).resolve()
    if not root.exists():
        raise FileNotFoundError(
            f"RTLLM root not found: {root}\n"
            f"Clone it: git clone https://github.com/hkust-zhiyao/RTLLM.git third_party/RTLLM"
        )

    problems: list[RTLLMProblem] = []

    for cat_dir in sorted(root.iterdir()):
        if not cat_dir.is_dir() or cat_dir.name.startswith("_"):
            continue
        if cat_dir.name not in _CATEGORIES:
            continue

        # Walk subcategories (e.g. Arithmetic/Adder/adder_8bit)
        for design_dir in sorted(cat_dir.rglob("*")):
            if not design_dir.is_dir():
                continue
            desc_file = design_dir / "design_description.txt"
            tb_file = design_dir / "testbench.v"
            if not desc_file.exists() or not tb_file.exists():
                continue

            description = desc_file.read_text(encoding="utf-8", errors="replace")
            module_name = _extract_module_name(description)
            category = str(design_dir.relative_to(root).parent).replace("\\", "/")
            ref_path = _find_reference(design_dir)

            problems.append(RTLLMProblem(
                name=design_dir.name,
                category=category,
                description=description,
                module_name=module_name,
                testbench_path=tb_file.resolve(),
                reference_path=ref_path.resolve() if ref_path else None,
                design_dir=design_dir.resolve(),
            ))

    return problems


def list_names(rtllm_root: Path | None = None) -> list[str]:
    """Return sorted list of all RTLLM design names."""
    return [p.name for p in discover_all(rtllm_root)]


def load_by_name(name: str, rtllm_root: Path | None = None) -> RTLLMProblem:
    """Load a specific RTLLM problem by design name."""
    for p in discover_all(rtllm_root):
        if p.name == name:
            return p
    available = list_names(rtllm_root)
    raise ValueError(f"RTLLM design '{name}' not found. Available: {available[:10]}...")


if __name__ == "__main__":
    # Quick self-test: list all discovered problems
    problems = discover_all()
    print(f"Discovered {len(problems)} RTLLM problems:")
    for p in problems:
        ref_tag = "ref" if p.reference_path else "no-ref"
        print(f"  [{p.category}] {p.name} (module={p.module_name}, {ref_tag})")
