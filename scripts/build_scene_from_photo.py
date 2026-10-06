#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_scene_from_photo.py — 把一张竖向场景照片重构成 4:5 主视觉底图。

只做等比缩放、平移、裁切和窄条镜像补齐，不做涂抹、修补或去水印：
画面里不想要的内容（例如平台水印）靠"重新构图"排除到画外。

典型用法（把台座顶面对到"商品落在 80% 高度线"）：
    python build_scene_from_photo.py --src work/base/scene-photo-src.jpeg \
        --dst work/base/base-cn.png --podium-px 548 --podium-py 878 --px 0.674 --py 0.80

`--podium-px/--podium-py` 是源图里"商品要站的那个台面中心"的像素坐标（看图目测即可）；
不写则用 --x-hint/--y-hint 自动检测（浅色台面易与亮墙混淆，建议手动指定）。
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def detect_podium(img: Image.Image, x_hint: float, y_hint: float,
                  win=(0.34, 0.30, 0.14, 0.06)) -> tuple[float, float]:
    """在提示点附近找台面：高亮度、低饱和的大块区域，返回其几何中心。"""
    w, h = img.size
    arr = np.asarray(img.convert("RGB"), dtype="float32")
    lum = arr.mean(axis=2)
    sat = arr.max(axis=2) - arr.min(axis=2)
    mask = (lum > 175) & (sat < 34)
    x0, x1 = max(0, int((x_hint - win[0]) * w)), int((x_hint + win[1]) * w)
    y0, y1 = max(0, int((y_hint - win[2]) * h)), int((y_hint + win[3]) * h)
    sub = mask[y0:y1, x0:x1]
    if sub.sum() < 400:
        return x_hint * w, y_hint * h
    ys, xs = np.where(sub)
    return float(x0 + (xs.min() + xs.max()) / 2), float(y0 + ys.min() + (ys.max() - ys.min()) * 0.42)


def mirror_fill(canvas: Image.Image, side: str, amount: int) -> None:
    """用紧邻条带镜像补齐窄条（amount 通常 < 100px，接缝不可见）。"""
    w, h = canvas.size
    if amount <= 0:
        return
    if side == "left":
        strip = canvas.crop((amount, 0, amount * 2, h)).transpose(Image.FLIP_LEFT_RIGHT)
        canvas.paste(strip, (0, 0))
    elif side == "top":
        strip = canvas.crop((0, amount, w, amount * 2)).transpose(Image.FLIP_TOP_BOTTOM)
        canvas.paste(strip, (0, 0))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="把竖向场景照片重构成 4:5 主视觉底图")
    ap.add_argument("--src", required=True, help="原始场景照片")
    ap.add_argument("--dst", required=True, help="输出的底图（spec 里 background_image 指向它）")
    ap.add_argument("--width", type=int, default=1200)
    ap.add_argument("--height", type=int, default=1500)
    ap.add_argument("--px", type=float, default=0.674, help="台面中心的目标横向位置")
    ap.add_argument("--py", type=float, default=0.80, help="台面中心的目标纵向位置（0.8 = 商品落点）")
    ap.add_argument("--podium-px", type=float, default=None, help="源图里台面中心的像素 x（推荐手动指定）")
    ap.add_argument("--podium-py", type=float, default=None, help="源图里台面中心的像素 y")
    ap.add_argument("--x-hint", type=float, default=0.65, help="自动检测时的横向提示")
    ap.add_argument("--y-hint", type=float, default=0.54, help="自动检测时的纵向提示")
    args = ap.parse_args(argv)

    src = Image.open(args.src).convert("RGB")
    sw, sh = src.size
    if args.podium_px is not None and args.podium_py is not None:
        cx, cy, how = args.podium_px, args.podium_py, "手动指定"
    else:
        cx, cy = detect_podium(src, args.x_hint, args.y_hint)
        how = "自动检测"

    scale = args.width / sw                      # 按宽度铺满，左右不留空
    fitted = src.resize((args.width, round(sh * scale)), Image.LANCZOS)
    left = round(args.px * args.width - cx * scale)
    top = round(args.py * args.height - cy * scale)
    print(f"源图 {sw}×{sh}｜台面中心 ({cx:.0f},{cy:.0f})（{how}）｜缩放 {scale:.3f}｜偏移 left={left} top={top}")

    canvas = Image.new("RGB", (args.width, args.height))
    canvas.paste(fitted, (left, top))
    if left > 0:
        mirror_fill(canvas, "left", left)
    if top > 0:
        mirror_fill(canvas, "top", top)

    out = Path(args.dst)
    out.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(out, "PNG", optimize=True)
    print(f"已生成 {out} {canvas.size}（台面中心 → {args.px}/{args.py}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
