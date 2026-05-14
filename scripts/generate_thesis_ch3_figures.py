"""Generate thesis Chapter 3 figures.

Produces (PNG + PDF):
  - figure/fig_system_architecture_v2.png            (Fig 3.1, English)
  - figure/fig_feedback_loop_v2.png                  (Fig 3.2, English)
  - figure/fig_task_normalization_v1.{pdf,png}       (Fig 3.3, Chinese)
  - figure/fig_llm_code_extraction_v1.{pdf,png}      (Fig 3.4, Chinese)
  - figure/fig_feedback_decision_v1.{pdf,png}        (Fig 3.5, Chinese)

Requires: matplotlib (pip install matplotlib)
Chinese fonts: Microsoft YaHei / SimHei (Windows defaults). The script falls
back to DejaVu Sans if neither is found, in which case Chinese glyphs may
render as squares. Re-run with a Chinese font installed to fix.
"""

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import font_manager
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent.parent / "report" / "thesis" / "latex" / "figure"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Chinese font configuration ---
_CN_FONT_CANDIDATES = ["Microsoft YaHei", "SimHei", "SimSun", "Noto Sans CJK SC"]
_AVAILABLE_FONTS = {f.name for f in font_manager.fontManager.ttflist}
_CN_FONT = next((f for f in _CN_FONT_CANDIDATES if f in _AVAILABLE_FONTS), None)
if _CN_FONT:
    plt.rcParams["font.sans-serif"] = [_CN_FONT, "DejaVu Sans"]
    plt.rcParams["font.family"] = "sans-serif"
    print(f"[font] using Chinese font: {_CN_FONT}")
else:
    print("[font] no Chinese font found; Chinese glyphs may render as boxes")
plt.rcParams["axes.unicode_minus"] = False


def _save(fig, basename: str, also_pdf: bool = False) -> None:
    png_out = OUT_DIR / f"{basename}.png"
    fig.savefig(png_out, dpi=300, bbox_inches="tight", facecolor="white")
    print(f"Saved: {png_out}")
    if also_pdf:
        pdf_out = OUT_DIR / f"{basename}.pdf"
        fig.savefig(pdf_out, bbox_inches="tight", facecolor="white")
        print(f"Saved: {pdf_out}")
    plt.close(fig)


def _rounded_box(ax, xy, w, h, label, color="#4A90D9", fontsize=9, text_color="white"):
    """Draw a rounded rectangle with centered label."""
    box = mpatches.FancyBboxPatch(
        xy, w, h,
        boxstyle="round,pad=0.12",
        facecolor=color, edgecolor="#2C3E50", linewidth=1.2,
    )
    ax.add_patch(box)
    cx, cy = xy[0] + w / 2, xy[1] + h / 2
    ax.text(cx, cy, label, ha="center", va="center",
            fontsize=fontsize, color=text_color, fontweight="bold",
            fontfamily="sans-serif")


def _arrow(ax, start, end, color="#2C3E50"):
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.5))


def generate_system_architecture():
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.5, 7.5)
    ax.axis("off")
    ax.set_aspect("equal")

    # Title
    ax.text(5.25, 7.1, "System Module Architecture & Data Flow",
            ha="center", fontsize=13, fontweight="bold", fontfamily="sans-serif")

    # --- Modules ---
    bw, bh = 2.0, 0.7  # box width, height

    # Row 1: Benchmarks
    _rounded_box(ax, (0.3, 5.8), bw, bh, "VerilogEval\nLoader", "#27AE60")
    _rounded_box(ax, (3.0, 5.8), bw, bh, "RTLLM\nLoader", "#27AE60")

    # Row 2: Unified Task
    _rounded_box(ax, (1.6, 4.5), bw, bh, "Task Interface", "#E67E22")

    # Row 3: Prompt Builder + LLM Client
    _rounded_box(ax, (0.0, 3.2), bw, bh, "Prompt\nBuilder", "#4A90D9")
    _rounded_box(ax, (3.0, 3.2), bw, bh, "LLM Client\n(API Gateway)", "#4A90D9")

    # Row 4: Verilog Extractor + EDA
    _rounded_box(ax, (5.5, 4.5), bw, bh, "Verilog\nExtractor", "#8E44AD")
    _rounded_box(ax, (5.5, 3.2), bw, bh, "iverilog\nCompiler", "#C0392B")
    _rounded_box(ax, (8.2, 3.2), bw, bh, "VVP\nSimulator", "#C0392B")

    # Row 5: Ranker + Feedback Loop
    _rounded_box(ax, (5.5, 1.9), bw, bh, "Ranker\n(Scorer)", "#8E44AD")
    _rounded_box(ax, (2.5, 1.0), 3.0, bh, "Feedback Loop Controller", "#2C3E50")

    # Row 6: Artifact Manager
    _rounded_box(ax, (8.2, 1.9), bw, bh, "Artifact\nManager", "#16A085")
    _rounded_box(ax, (8.2, 0.7), bw, bh, "Outputs\n(JSON/CSV)", "#16A085")

    # --- Arrows ---
    # Loaders -> Task
    _arrow(ax, (1.3, 5.8), (2.2, 5.2))
    _arrow(ax, (4.0, 5.8), (3.2, 5.2))

    # Task -> Prompt Builder
    _arrow(ax, (2.1, 4.5), (1.0, 3.9))

    # Prompt Builder -> LLM
    _arrow(ax, (2.0, 3.55), (3.0, 3.55))

    # LLM -> Extractor
    _arrow(ax, (5.0, 3.55), (5.5, 4.5))

    # Extractor -> Compiler
    _arrow(ax, (6.5, 4.5), (6.5, 3.9))

    # Compiler -> Simulator
    _arrow(ax, (7.5, 3.55), (8.2, 3.55))

    # Simulator -> Ranker
    _arrow(ax, (9.2, 3.2), (7.2, 2.6))

    # Ranker -> Loop Controller
    _arrow(ax, (5.5, 2.1), (5.5, 1.7))

    # Loop Controller -> Prompt Builder (feedback arrow, curved)
    ax.annotate("", xy=(0.5, 3.2), xytext=(2.5, 1.3),
                arrowprops=dict(arrowstyle="-|>", color="#E74C3C", lw=2.0,
                                connectionstyle="arc3,rad=0.4"))
    ax.text(0.3, 2.1, "feedback", fontsize=8, color="#E74C3C",
            fontstyle="italic", fontfamily="sans-serif")

    # Ranker -> Artifact Manager
    _arrow(ax, (7.5, 2.15), (8.2, 2.15))
    # Artifact -> Outputs
    _arrow(ax, (9.2, 1.9), (9.2, 1.4))

    plt.tight_layout()
    _save(fig, "fig_system_architecture_v2")


def generate_feedback_loop_flow():
    fig, ax = plt.subplots(figsize=(8, 11))
    ax.set_xlim(-1, 9)
    ax.set_ylim(-0.5, 12)
    ax.axis("off")
    ax.set_aspect("equal")

    ax.text(4, 11.5, "Feedback Loop Control Flow",
            ha="center", fontsize=13, fontweight="bold", fontfamily="sans-serif")

    bw, bh = 3.0, 0.6
    dw, dh = 2.4, 0.8  # diamond

    # Start
    ax.add_patch(plt.Circle((4, 10.8), 0.3, color="#2C3E50"))
    ax.text(4, 10.8, "Start", ha="center", va="center", color="white", fontsize=8, fontweight="bold")

    # Box: Build Initial Prompt
    _rounded_box(ax, (2.5, 9.6), bw, bh, "Build Initial Prompt", "#4A90D9", 9)
    _arrow(ax, (4, 10.5), (4, 10.2))

    # Box: Generate k Candidates
    _rounded_box(ax, (2.5, 8.5), bw, bh, "Generate k Candidates (LLM)", "#4A90D9", 9)
    _arrow(ax, (4, 9.6), (4, 9.1))

    # Box: Extract Verilog
    _rounded_box(ax, (2.5, 7.4), bw, bh, "Extract Verilog Code", "#8E44AD", 9)
    _arrow(ax, (4, 8.5), (4, 8.0))

    # Box: Compile (iverilog)
    _rounded_box(ax, (2.5, 6.3), bw, bh, "Compile (iverilog -g2012)", "#C0392B", 9)
    _arrow(ax, (4, 7.4), (4, 6.9))

    # Diamond: Compile OK?
    diamond1 = mpatches.FancyBboxPatch((2.8, 5.1), dw, dh,
                                        boxstyle="round,pad=0.05",
                                        facecolor="#F39C12", edgecolor="#2C3E50", lw=1.2)
    ax.add_patch(diamond1)
    ax.text(4, 5.5, "Compile\nSuccess?", ha="center", va="center", fontsize=8, fontweight="bold")
    _arrow(ax, (4, 6.3), (4, 5.9))

    # Compile fail -> Build compile feedback
    _rounded_box(ax, (6.0, 5.1), 2.2, bh, "Build Compile\nFeedback", "#E74C3C", 8)
    ax.annotate("No", xy=(6.0, 5.4), xytext=(5.2, 5.5),
                fontsize=8, color="#E74C3C", fontweight="bold")

    # Box: Simulate (vvp)
    _rounded_box(ax, (2.5, 3.9), bw, bh, "Simulate (vvp)", "#C0392B", 9)
    ax.annotate("Yes", xy=(4, 4.5), xytext=(3.2, 4.8),
                fontsize=8, color="#27AE60", fontweight="bold")
    _arrow(ax, (4, 5.1), (4, 4.5))

    # Diamond: Pass?
    diamond2 = mpatches.FancyBboxPatch((2.8, 2.7), dw, dh,
                                        boxstyle="round,pad=0.05",
                                        facecolor="#F39C12", edgecolor="#2C3E50", lw=1.2)
    ax.add_patch(diamond2)
    ax.text(4, 3.1, "rank = 1.0\n(Pass)?", ha="center", va="center", fontsize=8, fontweight="bold")
    _arrow(ax, (4, 3.9), (4, 3.5))

    # Pass -> Output best
    _rounded_box(ax, (2.5, 1.5), bw, bh, "Output Best Verilog", "#27AE60", 9)
    ax.annotate("Yes", xy=(4, 2.1), xytext=(3.2, 2.4),
                fontsize=8, color="#27AE60", fontweight="bold")
    _arrow(ax, (4, 2.7), (4, 2.1))

    # End
    ax.add_patch(plt.Circle((4, 0.7), 0.3, color="#2C3E50"))
    ax.text(4, 0.7, "End", ha="center", va="center", color="white", fontsize=8, fontweight="bold")
    _arrow(ax, (4, 1.5), (4, 1.0))

    # Fail -> check iterations
    _rounded_box(ax, (6.0, 2.7), 2.2, bh, "Update\nGlobal Best", "#E67E22", 8)
    ax.annotate("No", xy=(5.2, 3.0), xytext=(5.0, 3.3),
                fontsize=8, color="#E74C3C", fontweight="bold")
    _arrow(ax, (5.2, 3.1), (6.0, 3.0))

    # Sim fail -> Build sim feedback
    _rounded_box(ax, (6.0, 3.9), 2.2, bh, "Build Sim\nFeedback", "#E74C3C", 8)

    # Feedback arrows back to Generate (curved)
    ax.annotate("", xy=(5.3, 8.8), xytext=(7.1, 5.7),
                arrowprops=dict(arrowstyle="-|>", color="#E74C3C", lw=1.8,
                                connectionstyle="arc3,rad=-0.3"))
    ax.annotate("", xy=(5.3, 8.7), xytext=(7.1, 4.5),
                arrowprops=dict(arrowstyle="-|>", color="#E74C3C", lw=1.8,
                                connectionstyle="arc3,rad=-0.35"))
    ax.annotate("", xy=(5.3, 8.6), xytext=(7.1, 3.3),
                arrowprops=dict(arrowstyle="-|>", color="#E74C3C", lw=1.8,
                                connectionstyle="arc3,rad=-0.4"))

    ax.text(7.8, 7.0, "Next\nIteration", fontsize=8, color="#E74C3C",
            fontstyle="italic", ha="center", fontfamily="sans-serif")

    plt.tight_layout()
    _save(fig, "fig_feedback_loop_v2")


# ----------------------------------------------------------------------
# New v10 figures (Chinese labels, PDF + PNG)
# ----------------------------------------------------------------------

def _plain_box(ax, xy, w, h, label, color="#FFFFFF", edge="#2C3E50",
               text_color="#1A1A1A", fontsize=10, lw=1.3, bold=False):
    """White-fill rectangle with black text. Friendlier for B/W printing."""
    box = mpatches.FancyBboxPatch(
        xy, w, h,
        boxstyle="round,pad=0.10",
        facecolor=color, edgecolor=edge, linewidth=lw,
    )
    ax.add_patch(box)
    cx, cy = xy[0] + w / 2, xy[1] + h / 2
    ax.text(cx, cy, label, ha="center", va="center",
            fontsize=fontsize, color=text_color,
            fontweight="bold" if bold else "normal")


def _label(ax, xy, text, fontsize=9, color="#555555", style="italic", ha="left"):
    ax.text(xy[0], xy[1], text, fontsize=fontsize, color=color,
            fontstyle=style, ha=ha, va="center")


def generate_task_normalization():
    """Fig 3.3  multi-source benchmark -> unified Task interface."""
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis("off")
    ax.set_aspect("auto")

    # Top sources
    ve_x, rt_x = 0.4, 5.8
    src_w, src_h = 3.8, 1.8
    _plain_box(ax, (ve_x, 6.0), src_w, src_h,
               "VerilogEval-Human\n\n描述文本\n模块接口声明\n参考实现 / Testbench",
               color="#EAF3FB", fontsize=9)
    _plain_box(ax, (rt_x, 6.0), src_w, src_h,
               "RTLLM 2.0\n\ndesign_description.txt\ntestbench.v\nverified_*.v",
               color="#EAF3FB", fontsize=9)

    # Loaders row
    ld_y, ld_w, ld_h = 4.4, 3.8, 0.9
    _plain_box(ax, (ve_x, ld_y), ld_w, ld_h,
               "VerilogEval Loader\n读取描述 + 合并参考与 Testbench",
               color="#FDF6E3", fontsize=9)
    _plain_box(ax, (rt_x, ld_y), ld_w, ld_h,
               "RTLLM Loader\n递归扫描目录 + 正则提取模块名",
               color="#FDF6E3", fontsize=9)

    # Arrows: source -> loader
    _arrow(ax, (ve_x + src_w / 2, 6.0), (ve_x + ld_w / 2, ld_y + ld_h))
    _arrow(ax, (rt_x + src_w / 2, 6.0), (rt_x + ld_w / 2, ld_y + ld_h))

    # Unified Task box
    task_x, task_y, task_w, task_h = 1.0, 2.5, 8.0, 1.3
    _plain_box(ax, (task_x, task_y), task_w, task_h,
               "统一 Task 接口\nname  ·  description  ·  module_header  ·  testbench_path",
               color="#E8F5E9", fontsize=11, bold=True)
    _label(ax, (task_x + task_w + 0.05, task_y + task_h / 2),
           "  下游模块仅依赖该接口", color="#2E7D32", style="italic", ha="left")

    # Arrows: loaders -> task
    _arrow(ax, (ve_x + ld_w / 2, ld_y), (task_x + 2.0, task_y + task_h))
    _arrow(ax, (rt_x + ld_w / 2, ld_y), (task_x + task_w - 2.0, task_y + task_h))

    # Bottom consumers
    cons_w, cons_h = 2.4, 0.9
    cons_y = 0.5
    cons_xs = [0.7, 3.8, 6.9]
    cons_labels = ["Prompt Builder\n初始/反馈提示词",
                   "Verilog Executor\niverilog + vvp",
                   "Ranker\n标量评分 [-2,1]"]
    for x, lab in zip(cons_xs, cons_labels):
        _plain_box(ax, (x, cons_y), cons_w, cons_h, lab,
                   color="#F0F0F5", fontsize=9)
        _arrow(ax, (x + cons_w / 2, task_y), (x + cons_w / 2, cons_y + cons_h))

    ax.set_title("图 3.3  多源 benchmark 到统一 Task 接口的转换流程",
                 fontsize=12, pad=10)
    plt.tight_layout()
    _save(fig, "fig_task_normalization_v1", also_pdf=True)


def generate_llm_code_extraction():
    """Fig 3.4  LLM raw response -> compilable Verilog."""
    fig, ax = plt.subplots(figsize=(9.5, 8))
    ax.set_xlim(0, 9.5)
    ax.set_ylim(0, 11)
    ax.axis("off")
    ax.set_aspect("auto")

    # Top: raw LLM response with annotations
    raw_x, raw_y, raw_w, raw_h = 0.6, 7.5, 8.3, 2.6
    _plain_box(ax, (raw_x, raw_y), raw_w, raw_h,
               "", color="#FAFAFA", lw=1.0)
    ax.text(raw_x + 0.3, raw_y + raw_h - 0.35,
            "LLM 原始回复", fontsize=11, fontweight="bold")

    # Mock content lines
    lines = [
        ("Sure, here is the design...",         "#888888", "  解释文本"),
        ("<reasoning> First we... </reasoning>", "#888888", "  CoT 推理段"),
        ("```verilog",                            "#C0392B", "  Markdown 围栏"),
        ("module adder(...);  ...  endmodule",   "#1565C0", "  目标 Verilog 代码块"),
        ("```",                                   "#C0392B", "  Markdown 围栏"),
        ("Hope this helps.",                      "#888888", "  解释尾段"),
    ]
    line_y = raw_y + raw_h - 0.7
    for txt, color, note in lines:
        ax.text(raw_x + 0.4, line_y, txt, fontsize=9,
                color=color, fontfamily="monospace")
        ax.text(raw_x + raw_w - 0.3, line_y, note, fontsize=8.5,
                color=color, ha="right", fontstyle="italic")
        line_y -= 0.32

    # Stage 1
    s1_y = 6.0
    _plain_box(ax, (raw_x, s1_y), raw_w, 0.85,
               "阶段 1：移除 Markdown 围栏\n正则匹配 ```verilog ... ``` 并剥离",
               color="#FFF3E0", fontsize=10)
    _arrow(ax, (raw_x + raw_w / 2, raw_y), (raw_x + raw_w / 2, s1_y + 0.85))

    # Stage 2
    s2_y = 4.5
    _plain_box(ax, (raw_x, s2_y), raw_w, 0.85,
               r"阶段 2：定位 module ... endmodule" + "\n忽略所有解释文本与 CoT 推理",
               color="#FFF3E0", fontsize=10)
    _arrow(ax, (raw_x + raw_w / 2, s1_y), (raw_x + raw_w / 2, s2_y + 0.85))

    # Stage 3
    s3_y = 3.0
    _plain_box(ax, (raw_x, s3_y), raw_w, 0.85,
               "阶段 3：写入 candidate.v\n仅保留可编译的 Verilog 代码",
               color="#FFF3E0", fontsize=10)
    _arrow(ax, (raw_x + raw_w / 2, s2_y), (raw_x + raw_w / 2, s3_y + 0.85))

    # Bottom: iverilog
    iv_x, iv_y, iv_w, iv_h = 2.5, 1.2, 4.5, 1.0
    _plain_box(ax, (iv_x, iv_y), iv_w, iv_h,
               "iverilog -g2012 编译\n+ vvp 仿真",
               color="#E3F2FD", fontsize=10, bold=True)
    _arrow(ax, (raw_x + raw_w / 2, s3_y), (iv_x + iv_w / 2, iv_y + iv_h))

    # Compatibility annotation
    ax.text(0.6, 0.4,
            "该提取流程兼容 Base / CoT / Few-shot / Few-shot+CoT 四种提示策略，"
            "无需为不同策略维护专用解析器。",
            fontsize=9, color="#444444", fontstyle="italic")

    ax.set_title("图 3.4  LLM 回复到可编译 Verilog 的提取流程",
                 fontsize=12, pad=10)
    plt.tight_layout()
    _save(fig, "fig_llm_code_extraction_v1", also_pdf=True)


def generate_feedback_decision():
    """Fig 3.5  EDA verification result -> feedback prompt."""
    fig, ax = plt.subplots(figsize=(11, 7.5))
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 9)
    ax.axis("off")
    ax.set_aspect("auto")

    # Top inputs
    cmp_x, cmp_w = 0.5, 4.5
    sim_x = 6.0
    inp_y, inp_h = 7.2, 1.5
    _plain_box(ax, (cmp_x, inp_y), cmp_w, inp_h,
               "编译结果 (iverilog)\n\n● 错误：rank = -1.0\n● 警告：rank = -0.5\n● 通过",
               color="#FDECEA", fontsize=9.5)
    _plain_box(ax, (sim_x, inp_y), cmp_w, inp_h,
               "仿真结果 (vvp)\n\n● 通过：rank = 1.0\n● 不匹配 N/M：rank ∈ (0, 1)\n● 超时 / 无输出：rank = 0.0",
               color="#FDECEA", fontsize=9.5)

    # Ranker
    rk_x, rk_y, rk_w, rk_h = 2.5, 5.4, 6.0, 1.0
    _plain_box(ax, (rk_x, rk_y), rk_w, rk_h,
               "评分器 Ranker\n标量评分  rank ∈ [-2.0, 1.0]",
               color="#E8F5E9", fontsize=11, bold=True)
    _arrow(ax, (cmp_x + cmp_w / 2, inp_y), (rk_x + rk_w / 2 - 1.2, rk_y + rk_h))
    _arrow(ax, (sim_x + cmp_w / 2, inp_y), (rk_x + rk_w / 2 + 1.2, rk_y + rk_h))

    # Decision
    dec_x, dec_y, dec_w, dec_h = 3.5, 3.7, 4.0, 0.9
    _plain_box(ax, (dec_x, dec_y), dec_w, dec_h,
               "控制器判定\nrank = 1.0 ?",
               color="#FFF8E1", fontsize=10, bold=True)
    _arrow(ax, (rk_x + rk_w / 2, rk_y), (dec_x + dec_w / 2, dec_y + dec_h))

    # Yes branch -> output
    out_x, out_y, out_w, out_h = 8.0, 3.7, 2.6, 0.9
    _plain_box(ax, (out_x, out_y), out_w, out_h,
               "返回 global_best\n实验记录 PASS",
               color="#E0F2F1", fontsize=9.5)
    ax.annotate("", xy=(out_x, out_y + out_h / 2),
                xytext=(dec_x + dec_w, dec_y + dec_h / 2),
                arrowprops=dict(arrowstyle="-|>", color="#2E7D32", lw=1.5))
    ax.text((dec_x + dec_w + out_x) / 2, dec_y + dec_h / 2 + 0.25,
            "是", fontsize=10, color="#2E7D32", fontweight="bold", ha="center")

    # No branch -> feedback builder
    fb_x, fb_y, fb_w, fb_h = 3.0, 2.0, 5.0, 0.9
    _plain_box(ax, (fb_x, fb_y), fb_w, fb_h,
               "反馈构造器  FeedbackBuilder",
               color="#EDE7F6", fontsize=10, bold=True)
    ax.annotate("", xy=(fb_x + fb_w / 2, fb_y + fb_h),
                xytext=(dec_x + dec_w / 2, dec_y),
                arrowprops=dict(arrowstyle="-|>", color="#C0392B", lw=1.5))
    ax.text(dec_x + dec_w / 2 + 0.45, (dec_y + fb_y + fb_h) / 2 + 0.05,
            "否", fontsize=10, color="#C0392B", fontweight="bold")

    # Three feedback levels
    lvl_y, lvl_h = 0.6, 0.9
    lvl_w = 3.0
    lvl_xs = [0.4, 4.0, 7.6]
    lvl_labels = [
        "L2 Compile-only\n仅编译错误信息",
        "L3 Succinct\n编译错误 + 不匹配数 + 输出前 40 行",
        "L4 Rich\n编译错误 + 输出前 80 行 + 分析提示",
    ]
    for x, lab in zip(lvl_xs, lvl_labels):
        _plain_box(ax, (x, lvl_y), lvl_w, lvl_h, lab,
                   color="#F3E5F5", fontsize=9)
        _arrow(ax, (fb_x + fb_w / 2, fb_y), (x + lvl_w / 2, lvl_y + lvl_h))

    # Bottom note (centered, below all level boxes)
    ax.text(5.5, 0.15,
            "三种粒度对应的反馈文本将拼入下一轮 prompt，参见表 3.3",
            fontsize=9, color="#444444", fontstyle="italic",
            ha="center", va="center")

    ax.set_title("图 3.5  EDA 验证结果到反馈提示词的转换逻辑",
                 fontsize=12, pad=10)
    plt.tight_layout()
    _save(fig, "fig_feedback_decision_v1", also_pdf=True)


if __name__ == "__main__":
    # Existing v2 figures (English labels) -- kept untouched
    generate_system_architecture()
    generate_feedback_loop_flow()
    # New v10 figures (Chinese labels, PDF + PNG)
    generate_task_normalization()
    generate_llm_code_extraction()
    generate_feedback_decision()
    print("Done.")
