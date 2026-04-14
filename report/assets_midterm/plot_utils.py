from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FONTS = ["SimHei", "Microsoft YaHei", "DejaVu Sans"]


def configure_matplotlib_fonts() -> None:
    plt.rcParams["font.sans-serif"] = DEFAULT_FONTS
    plt.rcParams["axes.unicode_minus"] = False


def save_figure(fig, relative_base_path: str, dpi: int = 200) -> None:
    base = PROJECT_ROOT / relative_base_path
    base.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(base.with_suffix(".png"), dpi=dpi, bbox_inches="tight", facecolor="white", edgecolor="none")
    fig.savefig(base.with_suffix(".svg"), bbox_inches="tight", facecolor="white", edgecolor="none")
    print(f"Saved: {base.with_suffix('.png')} / {base.with_suffix('.svg')}")
