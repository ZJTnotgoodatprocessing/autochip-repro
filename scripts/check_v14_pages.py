"""One-off helper: dump per-page char counts of v14 PDF to detect figure-only pages.
Pages with very small char counts beyond the header (~30 chars) are likely
floats that pushed all body text out, i.e. figure-dominated pages.
"""
import fitz  # PyMuPDF

doc = fitz.open("report/thesis/latex/main.pdf")
print("TOTAL PAGES:", doc.page_count)
print("=" * 60)
print("Pages with low char count (likely figure-dominated):")
print("-" * 60)
for i in range(doc.page_count):
    p = doc.load_page(i)
    t = (p.get_text() or "").strip()
    chars = len(t)
    # header for body pages is "北京航空航天大学毕业设计(论文) 第 X 页 " (~25-30 chars)
    body_chars = max(0, chars - 30)
    if body_chars < 200:
        # show snippet to help identify which figure
        snip = t.replace("\n", " ")[:80]
        print(f"p.{i+1:02d}  chars={chars:4d}  body~={body_chars:4d}  {snip}")
print("-" * 60)
print(f"Total pages with body~ < 200 chars: ", end="")
print(sum(1 for i in range(doc.page_count)
          if max(0, len((doc.load_page(i).get_text() or "").strip()) - 30) < 200))
doc.close()
