"""One-off helper: locate which page each Chapter 3 figure caption lands on
and report the body-text character count on that page so we can decide
whether the figure visually occupies the whole page even if the caption
adds a few hundred chars."""
from pathlib import Path
import fitz
import re

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "report" / "thesis" / "latex" / "main.pdf"

CAPTIONS = {
    "3.1": "图3.1",
    "3.2": "图3.2",
    "3.3": "图3.3",
    "3.4": "图3.4",
    "3.5": "图3.5",
}

doc = fitz.open(PDF)
print(f"PDF: {PDF.name}, total pages = {len(doc)}")
print("=" * 70)

for fig, needle in CAPTIONS.items():
    found = []
    for i, page in enumerate(doc, start=1):
        text = page.get_text()
        if needle in text:
            # Approximate body text excluding caption keyword and header
            body = re.sub(r"北京航空航天大学毕业设计\(论文\) 第\s*[A-Z0-9]+\s*页", "", text)
            chars = len(body.strip())
            found.append((i, chars, text.strip()[:100]))
    if not found:
        print(f"Fig {fig}  NOT FOUND (caption text mismatch?)")
        continue
    for pg, chars, preview in found:
        print(f"Fig {fig}  page {pg:3d}  chars={chars:4d}  preview: {preview!r}")
    print("-" * 70)

doc.close()
