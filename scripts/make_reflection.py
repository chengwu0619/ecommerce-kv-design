#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_reflection.py — 由商品抠图生成水面/台面倒影贴图。

商品站在水面或亮面石材上时，加一层倒影才不会"浮"起来。
输出仍是透明 PNG，在 spec 里当普通 image 图层用（配合 opacity）。

用法：
    python make_reflection.py --src work/base/product-cutout.png \
        --out work/base/product-reflection.png

然后在 spec 里放在商品下方（box 的 y 起点取商品底部所在高度）：
    { "type": "image", "path": "work/base/product-reflection.png",
      "box": [655, 1196, 400, 900], "fit": "contain", "opacity": 0.55 }
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="生成商品倒影贴图")
    ap.add_argument("--src", required=True, help="商品抠图（透明底 PNG）")
    ap.add_argument("--out", required=True)
    ap.add_argument("--fade-top", type=float, default=0.42, help="倒影最上沿的不透明度")
    ap.add_argument("--fade-bottom", type=float, default=0.03, help="倒影最下沿的不透明度")
    ap.add_argument("--blur", type=float, default=2.2, help="模糊半径（水面越大越糊）")
    ap.add_argument("--no-crop", action="store_true", help="不裁到 alpha 边界，保留原始画布")
    ap.add_argument("--threshold", type=int, default=128, help="判定商品边界的 alpha 阈值")
    args = ap.parse_args(argv)

    src = Image.open(args.src).convert("RGBA")
    if not args.no_crop:
        a = np.asarray(src.getchannel("A"))
        ys, xs = np.where(a > args.threshold)
        if len(xs) and len(ys):
            src = src.crop((int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1))
    flipped = src.transpose(Image.FLIP_TOP_BOTTOM)
    w, h = flipped.size
    ramp = np.linspace(args.fade_top, args.fade_bottom, h, dtype="float32")[:, None]
    arr = np.asarray(flipped, dtype="float32").copy()
    arr[:, :, 3] = arr[:, :, 3] * np.repeat(ramp, w, axis=1)
    out = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), "RGBA")
    if args.blur > 0:
        out = out.filter(ImageFilter.GaussianBlur(args.blur))
    dst = Path(args.out)
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, "PNG", optimize=True)
    print(f"已生成倒影 {dst} {out.size}（渐隐 {args.fade_top}→{args.fade_bottom}，模糊 {args.blur}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
