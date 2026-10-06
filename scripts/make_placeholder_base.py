#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_placeholder_base.py — 生成 4:5 占位底图，用于「先定版式、后换实拍」的流程。

商品实拍还没到位时，用占位底图先出布局确认稿，避免整条流程卡在等图上。
占位底图只提供色调、明暗与产品占位区，最终交付必须替换为实拍/正式底图。

用法：
    python make_placeholder_base.py --out work/base/base-cn.png --tone warm --label "PRODUCT PHOTO"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_kv import load_font, parse_color, use_utf8_stdio  # noqa: E402

use_utf8_stdio()

TONES = {
    "light": ("#F4F2EF", "#E4E1DC", (255, 255, 255)),
    "warm": ("#EFE6DA", "#DCCDBA", (255, 255, 255)),
    "cool": ("#EDF1F3", "#D5DDE1", (255, 255, 255)),
    "dark": ("#3B3A36", "#1E1D1B", (255, 255, 255)),
    "greige": ("#E9E4DC", "#CFC7BC", (255, 255, 255)),
}


def build(width: int, height: int, tone: str, label: str, product_area: str,
          product_ratio: float, scrim_strength: float) -> Image.Image:
    top, bottom, ink = TONES[tone]
    grad = Image.linear_gradient("L").resize((width, height), Image.BILINEAR)
    img = Image.new("RGBA", (width, height), parse_color(top)[:3] + (255,))
    overlay = Image.new("RGBA", (width, height), parse_color(bottom)[:3] + (255,))
    overlay.putalpha(grad)
    img.alpha_composite(overlay)

    if tone != "dark":
        vig = Image.new("L", (width, height), 0)
        pad_x, pad_y = int(width * 0.06), int(height * 0.05)
        ImageDraw.Draw(vig).ellipse([pad_x, pad_y, width - pad_x, height - pad_y], fill=255)
        vig = vig.filter(ImageFilter.GaussianBlur(width * 0.12))
        alpha = ImageChops.invert(vig).point(lambda v: int(v * 0.28))
        shade = Image.new("RGBA", (width, height), (60, 52, 44, 255))
        shade.putalpha(alpha)
        img.alpha_composite(shade)

    ph = int(height * product_ratio)
    if product_area == "top":
        y0 = int(height * 0.10)
    elif product_area == "bottom":
        y0 = height - ph - int(height * 0.16)
    else:
        y0 = (height - ph) // 2
    x0 = int(width * 0.10)
    box = [x0, y0, width - x0, y0 + ph]

    guide = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gd = ImageDraw.Draw(guide)
    dash_color = (90, 84, 76, 120) if tone != "dark" else (255, 255, 255, 110)
    radius = 24
    step = 26
    for x in range(box[0], box[2], step * 2):
        gd.line([(x, box[1]), (min(x + step, box[2]), box[1])], fill=dash_color, width=3)
        gd.line([(x, box[3]), (min(x + step, box[2]), box[3])], fill=dash_color, width=3)
    for y in range(box[1], box[3], step * 2):
        gd.line([(box[0], y), (box[0], min(y + step, box[3]))], fill=dash_color, width=3)
        gd.line([(box[2], y), (box[2], min(y + step, box[3]))], fill=dash_color, width=3)
    img.alpha_composite(guide)

    if scrim_strength > 0:
        sh = int(height * 0.42)
        g2 = Image.linear_gradient("L").resize((width, sh), Image.BILINEAR)
        dark = Image.new("RGBA", (width, sh), (0, 0, 0, 255))
        dark.putalpha(g2.point(lambda v: int(v * scrim_strength)))
        img.alpha_composite(dark, (0, height - sh))

    if label:
        font = load_font("en", "medium", max(22, int(width * 0.024)), {})
        d = ImageDraw.Draw(img)
        cx = (box[0] + box[2]) / 2
        cy = (box[1] + box[3]) / 2
        text = label.upper()
        try:
            tw = d.textlength(text, font=font)
            d.text((cx - tw / 2, cy), text, font=font, fill=parse_color(ink) + (170,))
        except Exception:
            pass
    img.info["kv_note"] = "占位底图：仅用于版式确认，交付前必须替换为实拍/正式底图"
    return img


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="生成 4:5 主视觉占位底图")
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=1200)
    ap.add_argument("--height", type=int, default=1500)
    ap.add_argument("--tone", default="greige", choices=sorted(TONES))
    ap.add_argument("--label", default="PRODUCT PHOTO AREA")
    ap.add_argument("--product-area", default="center", choices=["top", "center", "bottom"])
    ap.add_argument("--product-ratio", type=float, default=0.55)
    ap.add_argument("--scrim", type=float, default=0.5)
    args = ap.parse_args(argv)

    if abs(args.width / args.height - 0.8) > 0.002:
        print(f"[warn] 画布 {args.width}×{args.height} 不是 4:5", file=sys.stderr)
    img = build(args.width, args.height, args.tone, args.label, args.product_area,
                args.product_ratio, args.scrim)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.convert("RGB").save(out, "PNG", optimize=True)
    print(f"已生成占位底图 {out}  {img.width}×{img.height}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
