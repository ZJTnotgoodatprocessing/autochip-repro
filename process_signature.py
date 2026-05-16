"""
将 签字.jpg 处理为可在 LaTeX 中嵌入的透明背景签名 PNG。

处理步骤：
1. 加载 JPG，转灰度阈值化（把灰白纸张背景变透明）
2. 描笔像素强化为纯黑
3. 裁剪到签名内容紧凑边界（去除大片透明边缘）
4. 保存为 RGBA PNG
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter

SRC = Path(r"c:\Users\17819\autochip-repro\签字.jpg")
DST = Path(r"c:\Users\17819\autochip-repro\report\thesis\latex\figure\signature.png")

# 阈值: 灰度值小于此则视为笔迹（保留），大于此视为背景（透明）
# 纸张背景看起来是 ~180-200，墨水是 ~30-80，取 130 作为分界
THRESHOLD = 130
MARGIN_LEFT_PX = 0   # 左侧无留白，便于在 LaTeX 中与上下行左缘对齐
MARGIN_RIGHT_PX = 6
MARGIN_TOP_PX = 6
MARGIN_BOTTOM_PX = 6

def main():
    img = Image.open(SRC).convert("RGB")
    print(f"原图尺寸: {img.size}")

    # 轻度高斯模糊去除纸张纹理噪点（避免阈值化后留下散点）
    img_smooth = img.filter(ImageFilter.GaussianBlur(radius=0.6))
    arr = np.array(img_smooth)

    # 灰度
    gray = arr.mean(axis=2)

    # 笔迹掩码（True = 笔迹）
    ink_mask = gray < THRESHOLD

    # 计算 alpha：笔迹处不透明（255），背景处透明（0）
    # 在阈值附近做一段平滑过渡，保留笔迹边缘抗锯齿
    SOFT_BAND = 30  # 在 [THRESHOLD-SOFT_BAND, THRESHOLD] 范围内做线性过渡
    alpha = np.zeros_like(gray, dtype=np.uint8)
    full = gray < (THRESHOLD - SOFT_BAND)
    band = (gray >= (THRESHOLD - SOFT_BAND)) & (gray < THRESHOLD)
    alpha[full] = 255
    alpha[band] = (255 * (THRESHOLD - gray[band]) / SOFT_BAND).astype(np.uint8)

    # 颜色：笔迹处统一为纯黑（提高视觉对比）；背景处任意（被 alpha 隐藏）
    rgba = np.zeros((arr.shape[0], arr.shape[1], 4), dtype=np.uint8)
    rgba[..., 0] = 0  # R
    rgba[..., 1] = 0  # G
    rgba[..., 2] = 0  # B
    rgba[..., 3] = alpha

    # 裁剪到笔迹边界
    rows = np.any(ink_mask, axis=1)
    cols = np.any(ink_mask, axis=0)
    if not rows.any() or not cols.any():
        raise RuntimeError("未检测到笔迹，阈值可能不合适")

    top, bottom = np.where(rows)[0][[0, -1]]
    left, right = np.where(cols)[0][[0, -1]]
    top = max(0, top - MARGIN_TOP_PX)
    left = max(0, left - MARGIN_LEFT_PX)
    bottom = min(arr.shape[0] - 1, bottom + MARGIN_BOTTOM_PX)
    right = min(arr.shape[1] - 1, right + MARGIN_RIGHT_PX)

    cropped = rgba[top : bottom + 1, left : right + 1]
    print(f"裁剪后尺寸: {cropped.shape[1]} x {cropped.shape[0]}  (原 {arr.shape[1]} x {arr.shape[0]})")

    out = Image.fromarray(cropped, "RGBA")
    DST.parent.mkdir(parents=True, exist_ok=True)
    out.save(DST, "PNG", optimize=True)
    print(f"已保存: {DST}")

    # 顺手输出签名占图的可视面积比（用于参考）
    ink_count = int(ink_mask.sum())
    total = arr.shape[0] * arr.shape[1]
    print(f"笔迹像素占比: {ink_count / total * 100:.2f}%")


if __name__ == "__main__":
    main()
