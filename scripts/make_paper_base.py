#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_paper_base.py — 生成指定尺寸纸感底纹底图，用于编辑风/杂志风主视觉。

纸感底图的用法：把抠好的商品图叠在纸纹上，再加一层投影（spec 里的 shadow 图层），
就能得到"商品摆在纸上"的质感。底纹是氛围，不承载信息，所以文字仍由 build_kv.py 渲染。

用法：
    python make_paper_base.py --out work/base/base-cn.png --tone paper
    python make_paper_base.py --out work/base/base-cn.png --tone paper --grain 0.5 --seed 7
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

# 纸色 / 温度偏移（R,B 通道微调）
TONES = {
    "paper": ((238, 231, 219), (1.0, 0.98, 0.94)),
    "ivory": ((247, 244, 238), (1.0, 0.99, 0.97)),
    "kraft": ((226, 213, 190), (1.0, 0.97, 0.90)),
    "cool": ((236, 238, 236), (0.99, 1.0, 1.01)),
    "ink": ((52, 50, 47), (1.0, 0.98, 0.95)),
}


def _blur_noise(rng, width: int, height: int, radius: float, scale: float = 40.0) -> np.ndarray:
    """全分辨率噪声 + 大半径模糊：得到自然的纸浆斑驳，避免放大小噪声产生条带。"""
    noise = rng.normal(0, 1, (height, width)).astype("float32")
    encoded = np.clip(noise * scale + 128.0, 0, 255).astype("uint8")
    blurred = Image.fromarray(encoded, mode="L").filter(ImageFilter.GaussianBlur(radius))
    return (np.asarray(blurred, dtype="float32") - 128.0) / scale


def build(width: int, height: int, tone: str, grain: float, blotch: float,
          fiber: float, vignette: float, seed: int) -> Image.Image:
    base_rgb, temp = TONES[tone]
    rng = np.random.default_rng(seed)

    # 纸浆斑驳：细斑 + 粗斑两层
    mottle = _blur_noise(rng, width, height, 14) * 0.75 + _blur_noise(rng, width, height, 55) * 0.55

    # 细颗粒
    fine = rng.normal(0, 1, (height, width)).astype("float32")

    # 纤维：稀疏的水平短纹
    fibers = np.zeros((height, width), dtype="float32")
    for _ in range(int(width * height / 9000)):
        y = int(rng.integers(0, height))
        x = int(rng.integers(0, width))
        length = int(rng.integers(12, 90))
        fibers[y, x:min(width, x + length)] += float(rng.normal(0, 1))
    # PIL 的 GaussianBlur 不支持 F 模式，先偏移到 L 模式再模糊回来
    encoded = np.clip(fibers * 20.0 + 128.0, 0, 255).astype("uint8")
    blurred = Image.fromarray(encoded, mode="L").filter(ImageFilter.GaussianBlur(1.2))
    fibers = (np.asarray(blurred, dtype="float32") - 128.0) / 20.0

    field = mottle * blotch * 6.0 + fine * grain * 2.6 + fibers * fiber * 5.0

    # 柔和暗角
    yy, xx = np.mgrid[0:height, 0:width].astype("float32")
    cx, cy = width / 2.0, height / 2.0
    r = np.sqrt(((xx - cx) / cx) ** 2 + ((yy - cy) / cy) ** 2)
    field -= np.clip(r - 0.72, 0, None) ** 2 * 255 * vignette

    # 极轻的上下渐变，避免整张纸太平
    field += np.linspace(-3.5, 2.5, height, dtype="float32")[:, None] * (1.0 if tone != "ink" else 0.4)

    out = np.empty((height, width, 3), dtype="float32")
    for i, (channel, tint) in enumerate(zip(base_rgb, temp)):
        out[:, :, i] = channel * tint + field
    return Image.fromarray(np.clip(out, 0, 255).astype("uint8"), mode="RGB")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="生成指定尺寸的纸感底纹底图")
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=1200)
    ap.add_argument("--height", type=int, default=1500)
    ap.add_argument("--tone", default="paper", choices=sorted(TONES))
    ap.add_argument("--grain", type=float, default=0.45, help="细颗粒强度 0–1.5")
    ap.add_argument("--blotch", type=float, default=0.35, help="纸浆斑驳强度 0–1.5")
    ap.add_argument("--fiber", type=float, default=0.35, help="纤维纹理强度 0–1.5")
    ap.add_argument("--vignette", type=float, default=0.35, help="暗角强度 0–1.5")
    ap.add_argument("--seed", type=int, default=20261001)
    args = ap.parse_args(argv)

    if args.width <= 0 or args.height <= 0:
        ap.error("宽高必须为正整数")
    img = build(args.width, args.height, args.tone, args.grain, args.blotch,
                args.fiber, args.vignette, args.seed)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"已生成纸感底图 {out}  {img.width}×{img.height}  tone={args.tone}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
