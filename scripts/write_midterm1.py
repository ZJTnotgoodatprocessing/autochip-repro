
import re
from pathlib import Path

CONTENT = Path("scripts/midterm1_content.txt").read_text(encoding="utf-8")
Path("notes/midterm1.md").write_text(CONTENT, encoding="utf-8")
chinese = len(re.findall(r"[一-鿿　-〿＀-￯]", CONTENT))
print(f"Total chars: {len(CONTENT)}")
print(f"Chinese chars: {chinese}")
