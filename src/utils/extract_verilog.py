"""Extract Verilog module blocks from LLM response text."""

import re


def extract_modules(text: str | None) -> list[str]:
    """Return all `module ... endmodule` blocks found in *text*.

    Handles markdown ```verilog fences and stray backticks.
    Returns [] for empty / None input.
    """
    if not text:
        return []

    # Strip markdown code fences first
    text = re.sub(r"```(?:verilog|v|systemverilog)?\s*\n?", "", text)
    text = text.replace("```", "")

    modules = re.findall(r"(module\s+\w+[\s\S]*?endmodule)", text)
    return modules
