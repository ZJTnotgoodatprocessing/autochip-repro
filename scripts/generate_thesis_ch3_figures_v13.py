"""Generate Chapter 3 system-design figures in a formal line-art style (v13).

This script intentionally avoids the visual cues that betray AI-generated /
auto-laid-out diagrams: rounded corners, drop shadows, gradients, large
saturated fills, decorative icons, and in-figure English banners are all
removed. Output style:

  * white background;
  * black / dark-grey rectangles with uniform line width;
  * one accent colour (dark navy) used only for decision diamonds and the
    feedback return path;
  * arrows of identical thickness, no curved spaghetti routing;
  * no in-figure 图3.x labels or English titles -- the LaTeX caption owns
    the title;
  * vector PDF as primary output, PNG only for repository preview.

The script is idempotent: re-running overwrites the v13 figures and leaves
older versions (v1/v2) untouched, so v9-v12 PDFs continue to compile from
the previous figure set if checked out.

Usage (from project root):

    python scripts/generate_thesis_ch3_figures_v13.py
"""
from __future__ import annotations

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon
from matplotlib import font_manager
from pathlib import Path


# ---------------------------------------------------------------------------
# Output location
# ---------------------------------------------------------------------------

OUT_DIR = (
    Path(__file__).resolve().parent.parent
    / "report" / "thesis" / "latex" / "figure"
)
OUT_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------------
# Visual constants
# ---------------------------------------------------------------------------

EDGE = "#1A1A1A"          # main rectangle / arrow colour (near-black)
TEXT = "#111111"
ACCENT = "#1F3A5F"        # single low-saturation dark navy
MUTED = "#555555"          # group labels, side notes
GROUP_EDGE = "#999999"     # dashed group outline
LW = 1.1                   # uniform line width


# ---------------------------------------------------------------------------
# Font setup -- prefer a Chinese sans-serif so 中文 labels render correctly.
# ---------------------------------------------------------------------------

_CN_CANDIDATES = ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "SimSun"]
_AVAILABLE = {f.name for f in font_manager.fontManager.ttflist}
_CN_FONT = next((f for f in _CN_CANDIDATES if f in _AVAILABLE), None)
if _CN_FONT:
    plt.rcParams["font.sans-serif"] = [_CN_FONT, "DejaVu Sans"]
    plt.rcParams["font.family"] = "sans-serif"
    print(f"[font] using Chinese font: {_CN_FONT}")
else:
    print("[font] no Chinese sans-serif found; CJK glyphs may show as boxes")
plt.rcParams["axes.unicode_minus"] = False


# ---------------------------------------------------------------------------
# Drawing helpers
# ---------------------------------------------------------------------------

def _save(fig, basename: str) -> None:
    pdf = OUT_DIR / f"{basename}.pdf"
    png = OUT_DIR / f"{basename}.png"
    fig.savefig(pdf, bbox_inches="tight", facecolor="white")
    fig.savefig(png, dpi=200, bbox_inches="tight", facecolor="white")
    print(f"  saved: {pdf.name} / {png.name}")
    plt.close(fig)


def _box(ax, xy, w, h, label, *, fontsize=10, weight="normal",
          edge=EDGE, lw=LW, fill="white"):
    ax.add_patch(Rectangle(xy, w, h, facecolor=fill, edgecolor=edge,
                            linewidth=lw))
    cx, cy = xy[0] + w / 2, xy[1] + h / 2
    ax.text(cx, cy, label, ha="center", va="center",
            fontsize=fontsize, color=TEXT, fontweight=weight)


def _group(ax, xy, w, h, title):
    """Dashed outer group box with a left-aligned label inside the top edge."""
    ax.add_patch(Rectangle(xy, w, h, facecolor="white", edgecolor=GROUP_EDGE,
                            linewidth=0.9, linestyle=(0, (4, 3))))
    ax.text(xy[0] + 0.15, xy[1] + h - 0.05, title,
            ha="left", va="top", fontsize=9, color=MUTED, fontstyle="italic")


def _diamond(ax, cx, cy, w, h, label, *, fontsize=9, edge=ACCENT, lw=LW):
    pts = [(cx, cy + h / 2), (cx + w / 2, cy),
           (cx, cy - h / 2), (cx - w / 2, cy)]
    ax.add_patch(Polygon(pts, closed=True, facecolor="white",
                          edgecolor=edge, linewidth=lw))
    ax.text(cx, cy, label, ha="center", va="center",
            fontsize=fontsize, color=TEXT)


def _arrow(ax, start, end, *, color=EDGE, lw=LW, ls="-"):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                 linestyle=ls, mutation_scale=12,
                                 shrinkA=0, shrinkB=0))


def _label(ax, xy, text, *, fontsize=8.5, color=MUTED, ha="center",
            va="center", style="normal"):
    ax.text(*xy, text, fontsize=fontsize, color=color,
            ha=ha, va=va, fontstyle=style)


# ===========================================================================
# Fig 3.1 -- system architecture (layered)
# ===========================================================================

def fig_system_architecture():
    # v14: figsize reduced from (11.5, 11.0) so that LaTeX width 0.78 keeps
    # the visual font size around 6pt and the figure no longer fills a page.
    fig, ax = plt.subplots(figsize=(8.0, 7.65))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 13)
    ax.axis("off")
    ax.set_aspect("auto")

    # Layer geometry (top -> bottom).
    layers = [
        ("Benchmark 层",     11.6),
        ("统一 Task 接口",   9.7),
        ("生成层",           7.8),
        ("验证层",           5.9),
        ("反馈控制层",       4.0),
        ("产物层",           2.1),
    ]
    layer_w = 11.0
    layer_h = 1.55
    layer_x = 0.6

    # Draw dashed group containers.
    for title, cy in layers:
        _group(ax, (layer_x, cy - layer_h / 2), layer_w, layer_h, title)

    # --- Benchmark layer ---
    cy = layers[0][1]
    _box(ax, (1.4, cy - 0.45), 3.6, 0.9, "VerilogEval Loader")
    _box(ax, (7.0, cy - 0.45), 3.6, 0.9, "RTLLM Loader")

    # --- Task Interface ---
    cy = layers[1][1]
    _box(ax, (1.4, cy - 0.45), 9.2, 0.9,
          "Task(name, description, module_header, testbench_path)",
          weight="bold")

    # --- Generation layer ---
    cy = layers[2][1]
    gw = 3.0
    gxs = [1.0, 4.5, 8.0]
    for x, lab in zip(gxs, ["Prompt Builder", "LLM Client", "Verilog Extractor"]):
        _box(ax, (x, cy - 0.45), gw, 0.9, lab)
    # Internal arrows inside generation layer
    _arrow(ax, (gxs[0] + gw, cy), (gxs[1], cy))
    _arrow(ax, (gxs[1] + gw, cy), (gxs[2], cy))

    # --- Verification layer ---
    cy = layers[3][1]
    _box(ax, (1.4, cy - 0.45), 4.8, 0.9, "Icarus Verilog  /  VVP")
    _box(ax, (7.0, cy - 0.45), 3.6, 0.9, "Ranker (rank ∈ [-2, 1])")
    _arrow(ax, (1.4 + 4.8, cy), (7.0, cy))

    # --- Feedback control ---
    cy = layers[4][1]
    _box(ax, (1.4, cy - 0.45), 4.8, 0.9, "Feedback Loop Controller")
    _box(ax, (7.0, cy - 0.45), 3.6, 0.9, "Feedback Builder")
    _arrow(ax, (1.4 + 4.8, cy), (7.0, cy))

    # --- Artifact layer ---
    cy = layers[5][1]
    aw = 3.0
    axs = [1.0, 4.5, 8.0]
    for x, lab in zip(axs, ["Metadata", "summary.json", "details.json"]):
        _box(ax, (x, cy - 0.45), aw, 0.9, lab)

    # --- Inter-layer arrows (forward path, on the central axis) ---
    cx = 6.0
    for upper, lower in zip(layers[:-1], layers[1:]):
        _arrow(ax, (cx, upper[1] - layer_h / 2),
                (cx, lower[1] + layer_h / 2))

    # --- Feedback return path (dashed, accent colour) ---
    # From Feedback Builder back up to Prompt Builder.
    fb_x = 10.6
    fb_top = layers[2][1] - 0.4   # slightly below Generation layer top
    fb_bot = layers[4][1]
    # Up the right gutter, then left into Prompt Builder.
    ax.annotate("", xy=(fb_x, fb_top), xytext=(fb_x, fb_bot),
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=LW,
                                 linestyle=(0, (4, 3))))
    ax.annotate("", xy=(2.5, fb_top), xytext=(fb_x, fb_top),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=LW,
                                 linestyle=(0, (4, 3)),
                                 mutation_scale=12, shrinkA=0, shrinkB=0))
    _label(ax, (fb_x + 0.05, (fb_top + fb_bot) / 2),
           "反馈回路", color=ACCENT, ha="left", style="italic")

    _save(fig, "fig_system_architecture_v13")


# ===========================================================================
# Fig 3.2 -- multi-source benchmark normalisation
# ===========================================================================

def fig_task_normalization():
    fig, ax = plt.subplots(figsize=(11, 8.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 9)
    ax.axis("off")

    # Top sources
    src_w, src_h = 3.6, 1.7
    ve_x, rt_x = 0.7, 6.7
    src_y = 6.8
    _box(ax, (ve_x, src_y), src_w, src_h,
          "VerilogEval-Human\n\n· 描述文本\n· 模块接口声明\n· 参考实现 / Testbench",
          fontsize=9.5)
    _box(ax, (rt_x, src_y), src_w, src_h,
          "RTLLM 2.0\n\n· design_description.txt\n· testbench.v\n· verified_*.v",
          fontsize=9.5)

    # Loaders
    ld_y, ld_h = 5.2, 0.95
    _box(ax, (ve_x, ld_y), src_w, ld_h,
          "VerilogEval Loader\n读取描述并合并参考与 Testbench", fontsize=9.5)
    _box(ax, (rt_x, ld_y), src_w, ld_h,
          "RTLLM Loader\n递归扫描目录并正则提取模块名", fontsize=9.5)

    _arrow(ax, (ve_x + src_w / 2, src_y), (ve_x + src_w / 2, ld_y + ld_h))
    _arrow(ax, (rt_x + src_w / 2, src_y), (rt_x + src_w / 2, ld_y + ld_h))

    # Unified task box (centre)
    task_w, task_h = 9.0, 1.25
    task_x, task_y = 1.0, 3.1
    _box(ax, (task_x, task_y), task_w, task_h,
          "统一 Task 接口\nname  ·  description  ·  module_header  ·  testbench_path",
          fontsize=11, weight="bold")

    _arrow(ax, (ve_x + src_w / 2, ld_y),
            (task_x + task_w * 0.25, task_y + task_h))
    _arrow(ax, (rt_x + src_w / 2, ld_y),
            (task_x + task_w * 0.75, task_y + task_h))

    # v14a: side annotation removed; content is already covered in §3.3
    # prose ("下游模块仅依赖 name/description/module_header/testbench_path
    # 四个字段"). Removing it eliminates a coloured in-figure annotation
    # that the supervisor flagged as distracting.

    # Downstream consumers
    cons_w, cons_h = 2.6, 0.95
    cons_y = 1.1
    cons_xs = [0.9, 4.2, 7.5]
    cons_labels = ["Prompt Builder\n初始 / 反馈提示词",
                   "Verilog Executor\niverilog + vvp",
                   "Ranker\n标量评分 [-2, 1]"]
    for x, lab in zip(cons_xs, cons_labels):
        _box(ax, (x, cons_y), cons_w, cons_h, lab, fontsize=9.5)
        _arrow(ax, (x + cons_w / 2, task_y),
                (x + cons_w / 2, cons_y + cons_h))

    _save(fig, "fig_task_normalization_v13")


# ===========================================================================
# Fig 3.3 -- LLM raw response -> compilable Verilog
# ===========================================================================

def fig_llm_code_extraction():
    # v14b: keep figsize (6.0, 7.0) -- shrinking it makes the in-figure
    # text (whose size is in pt, independent of figsize) overflow the
    # axes-unit-sized boxes (the LLM raw response box would have its
    # monospace lines overlapping the right-side annotations).  Use the
    # LaTeX width below (0.55, was 0.65) to control the printed size.
    fig, ax = plt.subplots(figsize=(6.0, 7.0))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 12)
    ax.axis("off")

    # Top: raw LLM response box with annotated lines
    raw_x, raw_w = 0.5, 8.0
    raw_y, raw_h = 8.0, 3.4
    ax.add_patch(Rectangle((raw_x, raw_y), raw_w, raw_h,
                            facecolor="white", edgecolor=EDGE, linewidth=LW))
    ax.text(raw_x + 0.25, raw_y + raw_h - 0.32,
            "LLM 原始回复", fontsize=11, fontweight="bold", color=TEXT)

    # Mock content lines + side annotations.  All monochrome: we only
    # use bold weight to mark the target Verilog block.
    line_y = raw_y + raw_h - 0.85
    rows = [
        ("Sure, here is the design...",                   "解释文本",        "normal"),
        ("<reasoning>  First we ...  </reasoning>",        "CoT 推理段",      "normal"),
        ("```verilog",                                       "Markdown 围栏",   "normal"),
        ("module adder(...);  ...  endmodule",               "目标 Verilog 代码块", "bold"),
        ("```",                                              "Markdown 围栏",   "normal"),
        ("Hope this helps.",                                  "解释尾段",        "normal"),
    ]
    for text, note, weight in rows:
        ax.text(raw_x + 0.4, line_y, text, fontsize=9,
                color=TEXT, fontfamily="monospace", fontweight=weight)
        ax.text(raw_x + raw_w - 0.25, line_y, note, fontsize=8.5,
                color=MUTED, ha="right", fontstyle="italic")
        line_y -= 0.42

    # Stage 1
    _arrow(ax, (raw_x + raw_w / 2, raw_y),
            (raw_x + raw_w / 2, 7.2))
    _box(ax, (raw_x, 6.3), raw_w, 0.9,
          "阶段 1：移除 Markdown 围栏  (正则匹配 ```verilog ... ``` 并剥离)",
          fontsize=10)

    # Stage 2
    _arrow(ax, (raw_x + raw_w / 2, 6.3),
            (raw_x + raw_w / 2, 5.5))
    _box(ax, (raw_x, 4.6), raw_w, 0.9,
          r"阶段 2：定位 module ... endmodule  (忽略解释文本与 CoT 推理)",
          fontsize=10)

    # Stage 3
    _arrow(ax, (raw_x + raw_w / 2, 4.6),
            (raw_x + raw_w / 2, 3.8))
    _box(ax, (raw_x, 2.9), raw_w, 0.9,
          "阶段 3：写入 candidate.v  (仅保留可编译的 Verilog 代码)",
          fontsize=10)

    # Compiler -- v14a: widened (iv_w 4.0 -> 6.0) so the bold Chinese text
    # "iverilog -g2012 编译 + vvp 仿真" no longer crowds the box edges.
    # Centre stays at x=4.5 to line up with the upstream stages.
    iv_x, iv_w = 1.5, 6.0
    iv_y, iv_h = 1.1, 1.0
    _arrow(ax, (raw_x + raw_w / 2, 2.9),
            (iv_x + iv_w / 2, iv_y + iv_h))
    _box(ax, (iv_x, iv_y), iv_w, iv_h,
          "iverilog -g2012 编译  +  vvp 仿真",
          fontsize=10, weight="bold")

    # v14a: footer note removed; content ("兼容 Base / CoT / Few-shot /
    # Few-shot+CoT 四种提示策略") is already covered in §3.4 prose, so the
    # in-figure annotation only added visual noise after the figsize cut.

    _save(fig, "fig_llm_code_extraction_v13")


# ===========================================================================
# Fig 3.4 -- feedback loop control flow
# ===========================================================================

def fig_feedback_loop():
    # v14: figsize reduced from (9.0, 11.5) -> (4.5, 5.75); paired with LaTeX
    # width=0.50 so the figure occupies only ~45% of textheight and stops
    # claiming a dedicated page next to algorithm 1.
    fig, ax = plt.subplots(figsize=(4.5, 5.75))
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 13)
    ax.axis("off")

    cx = 4.0      # main column centre
    bw, bh = 4.4, 0.85
    bx = cx - bw / 2

    # Linear chain top -> bottom.
    chain = [
        (12.0, "初始 Prompt"),
        (10.7, "LLM 生成 k 个候选"),
        (9.4,  "提取 Verilog 代码"),
        (8.1,  "iverilog 编译  +  vvp 仿真"),
        (6.8,  "Ranker 评分"),
    ]
    for cy, lab in chain:
        _box(ax, (bx, cy - bh / 2), bw, bh, lab,
              weight="bold" if cy == chain[0][0] else "normal")

    for (cy_a, _), (cy_b, _) in zip(chain[:-1], chain[1:]):
        _arrow(ax, (cx, cy_a - bh / 2), (cx, cy_b + bh / 2))

    # Decision diamond
    diam_cy = 5.0
    _diamond(ax, cx, diam_cy, 4.4, 1.7,
              "best_rank == 1.0 ?", fontsize=10)
    _arrow(ax, (cx, chain[-1][0] - bh / 2), (cx, diam_cy + 0.85))

    # PASS branch (right)
    pass_x, pass_y = 7.2, diam_cy - 0.45
    _box(ax, (pass_x, pass_y), 1.6, 0.9, "PASS",
          fontsize=11, weight="bold", edge=ACCENT)
    ax.annotate("", xy=(pass_x, diam_cy),
                xytext=(cx + 2.2, diam_cy),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=LW,
                                 mutation_scale=12, shrinkA=0, shrinkB=0))
    _label(ax, ((cx + 2.2 + pass_x) / 2, diam_cy + 0.22),
           "是", color=ACCENT, ha="center", style="normal", fontsize=10)

    # NO branch -> feedback prompt builder (below).  v14a: the original
    # single-line bold label "构造反馈 Prompt  (附编译/仿真信息)" was
    # crowding the right edge of its box after the figsize shrink; split
    # into two lines and raise the box height accordingly so the text has
    # vertical breathing room.
    fb_y = 2.7
    fb_h = 1.3
    _box(ax, (bx, fb_y - fb_h / 2), bw, fb_h,
          "构造反馈 Prompt\n（附编译 / 仿真信息）", weight="bold")
    _arrow(ax, (cx, diam_cy - 0.85), (cx, fb_y + fb_h / 2))
    _label(ax, (cx + 0.25, (diam_cy - 0.85 + fb_y + fb_h / 2) / 2 + 0.1),
           "否", color=ACCENT, ha="left", fontsize=10)

    # Iteration counter / End on the side
    end_y = 1.0
    _box(ax, (bx, end_y - bh / 2), bw, bh,
          "iter += 1   (iter ≤ max_iter)", fontsize=9.5)
    _arrow(ax, (cx, fb_y - fb_h / 2), (cx, end_y + bh / 2))

    # Feedback return path: bend right, go up, re-enter at "LLM 生成"
    return_x = bx + bw + 0.6
    return_top = chain[1][0]    # LLM Generate row
    return_bot = end_y
    # vertical up
    ax.annotate("", xy=(return_x, return_top), xytext=(return_x, return_bot),
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=LW,
                                 linestyle=(0, (4, 3))))
    # horizontal in: end -> return_x
    ax.annotate("", xy=(return_x, return_bot), xytext=(bx + bw, return_bot),
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=LW,
                                 linestyle=(0, (4, 3))))
    # horizontal back into main column at LLM Generate
    ax.annotate("", xy=(bx + bw, return_top), xytext=(return_x, return_top),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=LW,
                                 linestyle=(0, (4, 3)),
                                 mutation_scale=12, shrinkA=0, shrinkB=0))
    _label(ax, (return_x + 0.05, (return_top + return_bot) / 2),
           "下一轮迭代", color=ACCENT, ha="left", style="italic")

    _save(fig, "fig_feedback_loop_v13")


# ===========================================================================
# Fig 3.5 -- EDA result -> feedback prompt decision chain
# ===========================================================================

def fig_feedback_decision():
    # v14b: keep figsize (8.5, 6.95) -- the L2/L3/L4 sub-boxes carry text
    # that, sized in pt, overlaps neighbours if figsize is shrunk.  Page-
    # area control is delegated to the LaTeX width below (0.70, was 0.85).
    fig, ax = plt.subplots(figsize=(8.5, 6.95))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 9.5)
    ax.axis("off")

    # Top: two parallel inputs
    inp_w, inp_h = 4.4, 1.55
    cmp_x, sim_x = 0.7, 5.9
    inp_y = 7.2
    _box(ax, (cmp_x, inp_y), inp_w, inp_h,
          "编译结果  (iverilog)\n\n· 错误：rank = -1.0\n"
          "· 警告：rank = -0.5\n· 通过：进入仿真",
          fontsize=9.5)
    _box(ax, (sim_x, inp_y), inp_w, inp_h,
          "仿真结果  (vvp)\n\n· 通过：rank = 1.0\n"
          "· 不匹配 N / M：rank ∈ (0, 1)\n· 超时 / 无输出：rank = 0.0",
          fontsize=9.5)

    # Ranker
    rk_x, rk_w = 2.0, 7.0
    rk_y, rk_h = 5.6, 0.95
    _box(ax, (rk_x, rk_y), rk_w, rk_h,
          "Ranker  ·  标量评分  rank ∈ [-2.0, 1.0]",
          fontsize=11, weight="bold")
    _arrow(ax, (cmp_x + inp_w / 2, inp_y), (rk_x + rk_w / 2 - 1.4, rk_y + rk_h))
    _arrow(ax, (sim_x + inp_w / 2, inp_y), (rk_x + rk_w / 2 + 1.4, rk_y + rk_h))

    # Decision diamond
    dec_cx, dec_cy = 5.5, 4.2
    _diamond(ax, dec_cx, dec_cy, 3.4, 1.45,
              "rank == 1.0 ?", fontsize=10)
    _arrow(ax, (dec_cx, rk_y), (dec_cx, dec_cy + 0.73))

    # Yes branch -> PASS box on the right
    pass_x, pass_w = 8.6, 2.0
    pass_y, pass_h = dec_cy - 0.45, 0.9
    _box(ax, (pass_x, pass_y), pass_w, pass_h,
          "返回 global_best\n实验记录 PASS",
          fontsize=10, edge=ACCENT)
    ax.annotate("", xy=(pass_x, dec_cy), xytext=(dec_cx + 1.7, dec_cy),
                arrowprops=dict(arrowstyle="-|>", color=ACCENT, lw=LW,
                                 mutation_scale=12, shrinkA=0, shrinkB=0))
    _label(ax, ((dec_cx + 1.7 + pass_x) / 2, dec_cy + 0.22),
           "是", color=ACCENT, ha="center", fontsize=10)

    # No branch -> Feedback Builder (below)
    fb_w, fb_h = 5.4, 0.9
    fb_x, fb_y = (11 - fb_w) / 2, 2.4
    _box(ax, (fb_x, fb_y), fb_w, fb_h,
          "Feedback Builder  ·  按粒度组装反馈文本",
          fontsize=10.5, weight="bold")
    _arrow(ax, (dec_cx, dec_cy - 0.73), (dec_cx, fb_y + fb_h))
    _label(ax, (dec_cx + 0.3, (dec_cy - 0.73 + fb_y + fb_h) / 2 + 0.05),
           "否", color=ACCENT, ha="left", fontsize=10)

    # Three granularity options at the bottom.  Arrows fan out from the
    # bottom edge of the Feedback Builder box at 1/6, 3/6, 5/6 of its width
    # so that L2 and L4 arrows clearly originate inside the FB box rather
    # than from empty space outside it; L3 stays vertical, L2/L4 are mild
    # diagonals (~24 deg).
    lvl_w, lvl_h = 3.2, 0.95
    lvl_y = 0.7
    lvl_xs = [0.4, 3.9, 7.4]
    # v14: tightened L3/L4 wording (dropped spaces around "+") so the labels
    # fit inside the boxes after the figsize shrink; the full descriptions
    # remain in the L0-L4 table 3.4 (feedback_levels).
    lvl_labels = [
        "L2  Compile-only\n仅编译错误信息",
        "L3  Succinct\n编译错误+不匹配数+前40行输出",
        "L4  Rich\n编译错误+前80行输出+分析提示",
    ]
    fb_anchor_xs = [fb_x + fb_w * 1 / 6,
                    fb_x + fb_w * 3 / 6,
                    fb_x + fb_w * 5 / 6]
    for anchor_x, x, lab in zip(fb_anchor_xs, lvl_xs, lvl_labels):
        _box(ax, (x, lvl_y), lvl_w, lvl_h, lab, fontsize=8.5)
        _arrow(ax, (anchor_x, fb_y), (x + lvl_w / 2, lvl_y + lvl_h))

    _save(fig, "fig_feedback_decision_v13")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    fig_system_architecture()
    fig_task_normalization()
    fig_llm_code_extraction()
    fig_feedback_loop()
    fig_feedback_decision()
    print("Done.")
