#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""make_scene_base.py — 生成 4:5 商品场景底图（渐变色背景 + 与商品配色相配的配景）。

用途：主视觉需要"商品摆在场景里"时，用它生成与商品配色呼应的渐变色背景、地面、
石台与配景（亚麻、干柑橘、枯枝、小石），再把真实商品图叠上去。
配景只做氛围，不承载信息；文字与价格仍由 build_kv.py 渲染。

默认版式把画面分成三段，保证文字安全：
    上 78%：深色渐变区，放标题与左右两列文字
    78–88%：中调过渡区，放商品主体下半段
    88–100%：浅色地面区，放石台与配景

用法：
    python make_scene_base.py --out work/base/base-cn.png --palette sage --seed 7
    python make_scene_base.py --out work/base/base-cn.png --palette clay --props linen,citrus
"""

from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# 渐变停靠点 (位置 0–1, RGB)：上深下浅；深色区承载文字，浅色地面承载石台与配景
PALETTES = {
    # 明亮雾面：浅鼠尾草到浅青灰，深色文字全程可读（对应"竹影水面"类场景）
    "mist":  [(0.00, (241, 245, 239)), (0.28, (231, 237, 224)), (0.52, (218, 228, 208)),
              (0.72, (205, 217, 194)), (0.86, (192, 205, 182)), (1.00, (179, 193, 169))],
    "sage":  [(0.00, (44, 54, 42)), (0.30, (58, 70, 52)), (0.58, (78, 86, 62)),
              (0.78, (100, 97, 78)), (0.86, (152, 142, 118)), (0.92, (190, 180, 154)),
              (1.00, (224, 215, 194))],
    "olive": [(0.00, (56, 55, 38)), (0.32, (78, 76, 50)), (0.62, (108, 102, 68)),
              (0.82, (146, 136, 102)), (0.90, (186, 175, 146)), (1.00, (224, 215, 192))],
    "clay":  [(0.00, (72, 50, 40)), (0.32, (104, 74, 56)), (0.62, (140, 106, 80)),
              (0.82, (176, 146, 116)), (0.90, (208, 184, 156)), (1.00, (234, 219, 198))],
    "ink":   [(0.00, (32, 36, 33)), (0.32, (46, 52, 46)), (0.62, (66, 72, 62)),
              (0.82, (100, 100, 88)), (0.90, (150, 144, 126)), (1.00, (206, 198, 178))],
    "sand":  [(0.00, (96, 88, 70)), (0.32, (124, 114, 92)), (0.62, (152, 142, 118)),
              (0.82, (180, 170, 146)), (0.90, (206, 196, 174)), (1.00, (232, 224, 206))],
    # 浅调：极浅薄荷/米白背景，适合"商品偏侧 + 底部配景带"的轻调版面
    "mint":  [(0.00, (221, 231, 220)), (0.34, (233, 239, 229)), (0.68, (241, 244, 238)),
              (0.86, (238, 241, 233)), (1.00, (228, 234, 225))],
}

STONE_TOP = (186, 176, 154)
STONE_SIDE = (150, 141, 122)
TRAVERTINE_TOP = (234, 229, 215)
TRAVERTINE_SIDE = (215, 208, 191)
LINEN = (232, 223, 202)
WOOD = (122, 100, 66)
CITRUS = (198, 152, 96)
BAMBOO = (110, 138, 90)
LEAF_SHADOW = (150, 168, 138)
DRAPE = (110, 124, 84)
PINE = (86, 108, 74)
PINE_LIGHT = (154, 172, 138)
FRUIT = (128, 146, 88)
POD = (150, 132, 96)


def blur_noise(rng, w: int, h: int, radius: float, scale: float = 40.0) -> np.ndarray:
    noise = rng.normal(0, 1, (h, w)).astype("float32")
    encoded = np.clip(noise * scale + 128.0, 0, 255).astype("uint8")
    blurred = Image.fromarray(encoded, mode="L").filter(ImageFilter.GaussianBlur(radius))
    return (np.asarray(blurred, dtype="float32") - 128.0) / scale


def gradient(w: int, h: int, stops) -> np.ndarray:
    ys = np.linspace(0, 1, h, dtype="float32")
    out = np.zeros((h, 3), dtype="float32")
    for i in range(len(stops) - 1):
        p0, c0 = stops[i]
        p1, c1 = stops[i + 1]
        mask = (ys >= p0) & (ys <= p1)
        if mask.any():
            t = ((ys[mask] - p0) / max(p1 - p0, 1e-6))[:, None]
            out[mask] = np.array(c0, dtype="float32") * (1 - t) + np.array(c1, dtype="float32") * t
    out[ys < stops[0][0]] = np.array(stops[0][1], dtype="float32")
    out[ys > stops[-1][0]] = np.array(stops[-1][1], dtype="float32")
    return np.repeat(out[:, None, :], w, axis=1)


def add_pool(canvas: np.ndarray, cx, cy, rx, ry, strength=0.12, tint=(255, 244, 220)) -> None:
    """柔光池：只把背景提亮几个百分点，避免过曝成光斑。"""
    h, w = canvas.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype("float32")
    d = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
    mask = (np.clip(1.0 - d, 0, 1) ** 2.2)[:, :, None]
    base = canvas / 255.0
    light = np.array(tint, dtype="float32") / 255.0
    canvas[:] = np.clip((base * (1 - mask * strength) + light * mask * strength) * 255, 0, 255)


def soft_shadow(img: Image.Image, box, strength=110, blur=26) -> None:
    x0, y0, x1, y1 = box
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse([x0, y0, x1, y1], fill=(46, 42, 34, strength))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def _lens(center, length: float, width: float, angle: float) -> list:
    """细长梭形（竹叶）多边形点集。"""
    cx, cy = center
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    pts = []
    steps = 16
    for i in range(steps + 1):
        t = -1 + 2 * i / steps
        x = t * length / 2
        y = (1 - abs(t)) ** 0.55 * width / 2
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    for i in range(steps + 1):
        t = 1 - 2 * i / steps
        x = t * length / 2
        y = -((1 - abs(t)) ** 0.55) * width / 2
        pts.append((cx + x * ca - y * sa, cy + x * sa + y * ca))
    return pts


def draw_bamboo(img: Image.Image, rng, origin=(1200, 210), spread=(300, 460)) -> None:
    """右上方竹枝：竹竿 + 细长竹叶，浅绿、微反差。"""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x0, y0 = origin
    # 主枝：从右侧画面外向左上延伸
    stem = []
    for i in range(25):
        t = i / 24
        stem.append((x0 - spread[0] * t + math.sin(t * 2.4) * 18,
                     y0 + spread[1] * 0.35 * t - spread[1] * 0.55 * t))
    for i in range(len(stem) - 1):
        d.line([stem[i], stem[i + 1]], fill=(140, 160, 116, 255),
               width=int(max(1.5, 4.5 * (1 - i / len(stem)) + 1)))
    # 叶簇
    for k in range(16):
        t = 0.18 + 0.82 * (k / 15)
        idx = min(int(t * (len(stem) - 1)), len(stem) - 2)
        bx, by = stem[idx]
        for sign in (-1, 1):
            if rng.random() < 0.25:
                continue
            length = rng.uniform(96, 168)
            width = rng.uniform(13, 22)
            ang = -28 + sign * rng.uniform(28, 74) + t * 10
            tone = tuple(int(np.clip(c * rng.uniform(0.94, 1.12), 0, 255)) for c in BAMBOO)
            pts = _lens((bx + math.cos(math.radians(ang)) * length * 0.42,
                         by + math.sin(math.radians(ang)) * length * 0.42), length, width, ang)
            d.polygon(pts, fill=tone + (int(rng.integers(225, 248)),))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.9)))


def draw_leaf_shadows(img: Image.Image, rng, count: int = 9) -> None:
    """墙面上的竹叶投影：大模糊、低对比。"""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(count):
        cx = rng.uniform(0.04, 0.52) * img.width
        cy = rng.uniform(0.04, 0.52) * img.height
        length = rng.uniform(150, 320)
        width = rng.uniform(22, 44)
        ang = rng.uniform(-38, 42)
        pts = _lens((cx, cy), length, width, ang)
        d.polygon(pts, fill=LEAF_SHADOW + (int(rng.integers(26, 54)),))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(26)))


def draw_water(img: Image.Image, water_y: int, rng) -> None:
    """水面：柔化过渡底色 + 倒影（带波纹位移）+ 涟漪线。"""
    w, h = img.size
    band = h - water_y
    if band <= 10:
        return
    base = np.zeros((band, w, 4), dtype="float32")
    base[:, :, :3] = np.array((198, 211, 188), dtype="float32")
    ramp = np.clip(np.linspace(0.0, 1.0, band, dtype="float32") * 1.5, 0, 1)
    base[:, :, 3] = ramp[:, None] * 210
    img.alpha_composite(Image.fromarray(base.astype("uint8"), "RGBA"), (0, water_y))

    src_h = min(band, water_y)
    src = img.crop((0, water_y - src_h, w, water_y)).transpose(Image.FLIP_TOP_BOTTOM)
    src = src.filter(ImageFilter.GaussianBlur(5))
    disp = Image.new("RGBA", (w, src_h), (0, 0, 0, 0))
    for y in range(src_h):
        shift = int(math.sin(y / 16.0) * 8 + math.sin(y / 6.0) * 3)
        disp.paste(src.crop((0, y, w, y + 1)), (shift, y))
    # 水线处不要突变：从 0 迅速到峰值再衰减
    x_ramp = np.linspace(0.0, 1.0, src_h, dtype="float32")
    alpha = np.clip(np.minimum(x_ramp / 0.10, 1.0), 0, 1) * (0.34 * np.exp(-x_ramp * 2.4) + 0.02)
    disp.putalpha(Image.fromarray((np.repeat(alpha[:, None], w, axis=1) * 255).astype("uint8"), "L"))
    img.alpha_composite(disp, (0, water_y))

    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for _ in range(16):
        y = water_y + rng.uniform(6, max(9, band - 8))
        amp, freq, phase = rng.uniform(1, 4), rng.uniform(40, 150), rng.uniform(0, 6.28)
        pts = [(x, y + math.sin(x / freq * 6.28 + phase) * amp) for x in range(0, w + 1, 12)]
        d.line(pts, fill=(255, 255, 255, int(rng.integers(30, 66))),
               width=int(rng.integers(1, 3)))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(1.2)))


def draw_pedestal(img: Image.Image, cx: float, top_y: float, rx: float, ry: float,
                  depth: float, rng, kind: str = "stone") -> None:
    """挤出式台座：底盘椭圆 + 侧面圆柱 + 顶面椭圆。kind=travertine 时用水磨石浅色。"""
    top_tone = TRAVERTINE_TOP if kind == "travertine" else STONE_TOP
    side_tone = TRAVERTINE_SIDE if kind == "travertine" else STONE_SIDE
    soft_shadow(img, (cx - rx * 1.15, top_y + depth - ry * 0.7,
                      cx + rx * 1.15, top_y + depth + ry * 2.0),
                strength=70 if kind == "travertine" else 120,
                blur=max(8.0, depth * 0.28))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - rx, top_y + depth - ry, cx + rx, top_y + depth + ry], fill=side_tone + (255,))
    d.rectangle([cx - rx, top_y, cx + rx, top_y + depth], fill=side_tone + (255,))
    # 侧面左暗右亮的竖向过渡
    grad = np.linspace(-14, 9, max(2, int(rx * 2)), dtype="float32")[None, :, None]
    arr = np.zeros((max(2, int(depth)), max(2, int(rx * 2)), 4), dtype="float32")
    arr[:, :, :3] = np.array(side_tone, dtype="float32") + grad
    arr[:, :, 3] = 255
    side = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"), mode="RGBA")
    layer.alpha_composite(side, (int(cx - rx), int(top_y)))
    d.ellipse([cx - rx, top_y - ry, cx + rx, top_y + ry], fill=top_tone + (255,))
    d.arc([cx - rx, top_y - ry, cx + rx, top_y + ry], start=188, end=352,
          fill=tuple(min(255, int(c * 1.06)) for c in top_tone) + (255,), width=3)
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(1.1)))

    # 石材颗粒
    pad = 14
    bx0, by0 = int(cx - rx - pad), int(top_y - ry - pad)
    bx1, by1 = int(cx + rx + pad), int(top_y + depth + ry + pad)
    bw, bh = bx1 - bx0, by1 - by0
    stone_mask = Image.new("L", (bw, bh), 0)
    sd = ImageDraw.Draw(stone_mask)
    sd.ellipse([cx - rx - bx0, top_y + depth - ry - by0, cx + rx - bx0, top_y + depth + ry - by0], fill=255)
    sd.rectangle([cx - rx - bx0, top_y - by0, cx + rx - bx0, top_y + depth - by0], fill=255)
    sd.ellipse([cx - rx - bx0, top_y - ry - by0, cx + rx - bx0, top_y + ry - by0], fill=255)
    stone_mask = stone_mask.filter(ImageFilter.GaussianBlur(2.0))
    m = np.asarray(stone_mask, dtype="float32") / 255.0
    if kind == "travertine":
        fine = blur_noise(rng, bw, bh, 0.8) * 5 + blur_noise(rng, bw, bh, 3) * 4
    else:
        fine = blur_noise(rng, bw, bh, 0.8) * 8 + blur_noise(rng, bw, bh, 7) * 5
    patch = np.asarray(img.crop((bx0, by0, bx1, by1)).convert("RGB"), dtype="float32")
    patch = np.clip(patch + fine[:, :, None] * m[:, :, None], 0, 255)
    img.paste(Image.fromarray(patch.astype("uint8"), mode="RGB"), (bx0, by0))


def draw_linen(img: Image.Image, box, rng) -> None:
    """有机形亚麻：波浪上沿 + 柔化边缘 + 褶皱明暗 + 布纹。"""
    w, h = img.size
    x0, y0, x1, y1 = box
    mask = Image.new("L", (w, h), 0)
    md = ImageDraw.Draw(mask)
    top = []
    for x in range(int(x0), int(x1) + 1, 6):
        t = (x - x0) / max(x1 - x0, 1)
        top.append((x, y0 + math.sin(t * 5.2 + 0.7) * 26 + math.sin(t * 11.0 + 2.1) * 11 - t * 22))
    md.polygon(top + [(x1, y1), (x0, y1)], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(7))

    layer = Image.new("RGBA", (w, h), LINEN + (0,))
    draw = ImageDraw.Draw(layer)
    for i in range(9):
        amp = rng.uniform(14, 34)
        freq = rng.uniform(1.0, 2.2)
        phase = rng.uniform(0, 6.28)
        base_y = y0 + (y1 - y0) * (0.06 + 0.105 * i)
        shade = int(rng.normal(0, 13))
        colour = tuple(int(np.clip(c + shade, 0, 255)) for c in LINEN) + (215,)
        pts = [(x, base_y + math.sin(x / max(x1 - x0, 1) * freq * 6.28 + phase) * amp)
               for x in range(int(x0), int(x1) + 1, 8)]
        draw.line(pts, fill=colour, width=int(rng.uniform(16, 42)), joint="curve")
    layer = layer.filter(ImageFilter.GaussianBlur(3))
    weave = blur_noise(rng, w, h, 0.6, 30) * 9
    arr = np.asarray(layer, dtype="float32")
    arr[:, :, :3] = np.clip(arr[:, :, :3] + weave[:, :, None], 0, 255)
    arr[:, :, 3] = np.asarray(mask, dtype="float32")
    img.alpha_composite(Image.fromarray(arr.astype("uint8"), mode="RGBA"))


def draw_branch(img: Image.Image, base, length: float, angle: float, side: int, rng,
                leaves: int = 5, scale: float = 0.85, tone=None, blur: float = 0.7,
                alpha: float = 1.0) -> None:
    tone = tone or WOOD
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = base
    segs = 30
    pts = []
    for i in range(segs + 1):
        t = i / segs
        bend = math.sin(t * math.pi * 0.85) * length * 0.18
        pts.append((x + side * math.sin(math.radians(angle)) * length * t + bend * 0.6 * side,
                    y - math.cos(math.radians(angle)) * length * t))
    for i in range(segs):
        w0 = max(1.2, (4.2 * (1 - i / segs) + 1.0) * scale)
        d.line([pts[i], pts[i + 1]], fill=tone + (255,), width=int(round(w0)))
    for k in range(leaves):
        idx = int(3 + (segs - 6) * (k / max(leaves - 1, 1)))
        lx, ly = pts[idx]
        px, py = pts[max(0, idx - 1)]
        stem_deg = math.degrees(math.atan2(ly - py, lx - px))
        for sign in (-1, 1):
            leaf_len = rng.uniform(52, 104) * scale
            leaf_w = leaf_len * rng.uniform(0.30, 0.42)
            leaf_tone = tuple(int(np.clip(c * rng.uniform(0.82, 1.14), 0, 255)) for c in tone)
            leaf = Image.new("RGBA", (int(leaf_len) + 26, int(leaf_w) + 26), (0, 0, 0, 0))
            ld = ImageDraw.Draw(leaf)
            cx, cy = leaf.width / 2, leaf.height / 2
            ld.ellipse([cx - leaf_len / 2, cy - leaf_w / 2, cx + leaf_len / 2, cy + leaf_w / 2],
                       fill=leaf_tone + (int(rng.integers(205, 250)),))
            ld.line([(cx - leaf_len / 2 + 5, cy), (cx + leaf_len / 2 - 5, cy)],
                    fill=tuple(int(c * 0.72) for c in leaf_tone) + (120,), width=2)
            rot = stem_deg - 90 + sign * rng.uniform(26, 62)
            leaf = leaf.rotate(-rot, resample=Image.BICUBIC, expand=True)
            lx2 = lx + math.cos(math.radians(rot)) * leaf_len * 0.36
            ly2 = ly - math.sin(math.radians(rot)) * leaf_len * 0.36
            layer.alpha_composite(leaf, (int(lx2 - leaf.width / 2), int(ly2 - leaf.height / 2)))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    if alpha < 1.0:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(layer)


def draw_citrus(img: Image.Image, center, radius: float, rng) -> None:
    cx, cy = center
    soft_shadow(img, (cx - radius * 1.3, cy + radius * 0.5, cx + radius * 1.5, cy + radius * 1.5),
                strength=95, blur=radius * 0.5)
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
              fill=tuple(int(c * 0.80) for c in CITRUS) + (255,))
    d.ellipse([cx - radius * 0.87, cy - radius * 0.87, cx + radius * 0.87, cy + radius * 0.87],
              fill=CITRUS + (255,))
    for i in range(9):
        a = 2 * math.pi * i / 9 + 0.2
        d.line([(cx + math.cos(a) * radius * 0.14, cy + math.sin(a) * radius * 0.14),
                (cx + math.cos(a) * radius * 0.78, cy + math.sin(a) * radius * 0.78)],
               fill=(158, 112, 62, 190), width=max(2, int(radius * 0.045)))
    d.ellipse([cx - radius * 0.15, cy - radius * 0.15, cx + radius * 0.15, cy + radius * 0.15],
              fill=(228, 196, 150, 255))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(1.0)))


def draw_pebble(img: Image.Image, center, rx: float, ry: float, rng) -> None:
    cx, cy = center
    soft_shadow(img, (cx - rx * 1.2, cy + ry * 0.2, cx + rx * 1.4, cy + ry * 1.9),
                strength=85, blur=max(6.0, rx * 0.45))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pts = []
    for i in range(28):
        a = 2 * math.pi * i / 28
        j = 1.0 + float(rng.normal(0, 0.05))
        pts.append((cx + math.cos(a) * rx * j, cy + math.sin(a) * ry * j))
    d.polygon(pts, fill=tuple(int(c * 0.92) for c in STONE_TOP) + (255,))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(1.2)))


def draw_drape(img: Image.Image, height: float, band: float, rng) -> None:
    """底部缎面/织物带：占图高 band，带柔和褶皱与高光，作为配景底座。"""
    w = img.width
    y0 = int(height * (1.0 - band))
    h = height - y0
    mask = Image.new("L", (w, height), 0)
    md = ImageDraw.Draw(mask)
    top = []
    for x in range(0, w + 1, 6):
        t = x / w
        y = y0 + math.sin(t * 3.4 + 0.6) * h * 0.10 + math.sin(t * 9.0 + 2.2) * h * 0.045
        top.append((x, y))
    md.polygon(top + [(w, height), (0, height)], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(10))

    layer = Image.new("RGBA", (w, height), DRAPE + (0,))
    d = ImageDraw.Draw(layer)
    # 顶部受光边：织物边缘的高光，让底带读成布料而不是山坡
    d.line([(x, y + rng.uniform(3, 7)) for (x, y) in top],
           fill=tuple(min(255, int(c * 1.5)) for c in DRAPE) + (110,), width=6, joint="curve")
    # 左侧布堆：一大一小两处隆起
    for (fx, fw, fh) in ((0.16, 0.20, 0.42), (0.40, 0.13, 0.24)):
        ex, ey = fx * w, y0 + h * 0.30
        d.ellipse([ex - fw * w / 2, ey - fh * h / 2, ex + fw * w / 2, ey + fh * h / 2],
                  fill=tuple(min(255, int(c * 1.18)) for c in DRAPE) + (150,))
    for i in range(6):
        base_y = y0 + h * (0.14 + 0.16 * i)
        amp = rng.uniform(14, 30)
        freq = rng.uniform(0.7, 1.5)
        phase = rng.uniform(0, 6.28)
        shade = int(rng.normal(4, 8))
        colour = tuple(int(np.clip(c + shade, 0, 255)) for c in DRAPE) + (200,)
        pts = [(x, base_y + math.sin(x / w * freq * 6.28 + phase) * amp) for x in range(0, w + 1, 8)]
        d.line(pts, fill=colour, width=int(rng.uniform(34, 74)), joint="curve")
    # 缎面高光
    for i in range(3):
        base_y = y0 + h * rng.uniform(0.22, 0.72)
        pts = [(x, base_y + math.sin(x / w * rng.uniform(1.0, 1.8) * 6.28 + rng.uniform(0, 6)) * h * 0.05)
               for x in range(0, w + 1, 10)]
        d.line(pts, fill=tuple(min(255, int(c * 1.45)) for c in DRAPE) + (80,),
               width=int(rng.uniform(18, 40)), joint="curve")
    layer = layer.filter(ImageFilter.GaussianBlur(13))
    weave = blur_noise(rng, w, height, 1.0, 26) * 9
    arr = np.asarray(layer, dtype="float32")
    arr[:, :, :3] = np.clip(arr[:, :, :3] + weave[:, :, None], 0, 255)
    arr[:, :, 3] = np.asarray(mask, dtype="float32")
    img.alpha_composite(Image.fromarray(arr.astype("uint8"), mode="RGBA"))


def draw_pine_spray(img: Image.Image, base, length: float, angle: float, side: int, rng,
                    blur: float = 7.0, tone=PINE, alpha: float = 1.0, needles: int = 12) -> None:
    """松/杉枝条：细枝 + 短针叶簇，整体虚化，模拟浅景深。"""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = base
    segs = 22
    pts = []
    for i in range(segs + 1):
        t = i / segs
        bend = math.sin(t * math.pi * 0.8) * length * 0.16
        pts.append((x + side * math.sin(math.radians(angle)) * length * t + bend * 0.7 * side,
                    y - math.cos(math.radians(angle)) * length * t))
    for i in range(segs):
        d.line([pts[i], pts[i + 1]], fill=tone + (255,), width=max(1, int(2.4 * (1 - i / segs) + 1)))
        for k in range(needles):
            t = i / segs
            n_len = rng.uniform(18, 40) * (1.25 - 0.5 * t)
            n_ang = rng.uniform(28, 88) * (1 if k % 2 == 0 else -1)
            bx, by = pts[i]
            ex = bx + math.cos(math.radians(90 - n_ang + side * 20)) * n_len * side
            ey = by - math.sin(math.radians(60 - n_ang * 0.4)) * n_len
            shade = int(rng.normal(0, 16))
            col = tuple(int(np.clip(c + shade, 0, 255)) for c in tone)
            d.line([(bx, by), (ex, ey)], fill=col + (int(rng.integers(170, 240)),),
                   width=max(1, int(rng.uniform(1.2, 2.6))))
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    if alpha < 1.0:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * alpha)))
    img.alpha_composite(layer)


def draw_fruit(img: Image.Image, center, r: float, rng) -> None:
    cx, cy = center
    soft_shadow(img, (cx - r * 1.1, cy + r * 0.45, cx + r * 1.3, cy + r * 1.5),
                strength=70, blur=max(4.0, r * 0.4))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    tone = tuple(int(np.clip(c * rng.uniform(0.85, 1.12), 0, 255)) for c in FRUIT)
    d.ellipse([cx - r, cy - r * 0.92, cx + r, cy + r * 0.92], fill=tone + (255,))
    d.ellipse([cx - r * 0.55, cy - r * 0.65, cx + r * 0.05, cy - r * 0.12],
              fill=tuple(min(255, int(c * 1.35)) for c in tone) + (120,))
    d.line([(cx, cy - r * 0.95), (cx + r * 0.18, cy - r * 1.35)],
           fill=tuple(int(c * 0.8) for c in tone) + (200,), width=max(1, int(r * 0.14)))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(1.4)))


def draw_pod(img: Image.Image, center, r: float, rng) -> None:
    """干果/轮状种子：参考图中的小轮形道具。"""
    cx, cy = center
    soft_shadow(img, (cx - r * 1.1, cy + r * 0.4, cx + r * 1.3, cy + r * 1.4), strength=60,
                blur=max(4.0, r * 0.4))
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=POD + (255,))
    d.ellipse([cx - r * 0.78, cy - r * 0.78, cx + r * 0.78, cy + r * 0.78],
              fill=tuple(int(c * 0.82) for c in POD) + (255,))
    for i in range(8):
        a = 2 * math.pi * i / 8
        d.line([(cx, cy), (cx + math.cos(a) * r * 0.74, cy + math.sin(a) * r * 0.74)],
               fill=tuple(int(c * 0.6) for c in POD) + (210,), width=max(2, int(r * 0.13)))
    d.ellipse([cx - r * 0.2, cy - r * 0.2, cx + r * 0.2, cy + r * 0.2],
              fill=tuple(int(c * 0.72) for c in POD) + (255,))
    img.alpha_composite(layer.filter(ImageFilter.GaussianBlur(1.2)))


def add_bokeh(img: Image.Image, specs, rng) -> None:
    """边缘虚化枝叶：重度虚化的叶簇做浅景深背景，只出现在画面四边与角落。"""
    for (bx, by, length, angle, side, alpha) in specs:
        draw_branch(img, (bx, by), length, angle, side, rng, leaves=7, scale=0.62,
                    tone=PINE_LIGHT, blur=30.0, alpha=alpha)


def build(width, height, palette, props, floor, pedestal, branch_side, branch_base,
          branch_length, glow, grain, vignette, seed, band: float = 0.21,
          product_x: float = 0.68, bokeh: float = 0.0,
          podium_kind: str = "stone", water_y: float = None,
          podium2=None) -> Image.Image:
    rng = np.random.default_rng(seed)
    canvas = gradient(width, height, PALETTES[palette])
    add_pool(canvas, glow[0] * width, glow[1] * height, glow[2] * width, glow[3] * height,
             strength=glow[4] * 0.22)
    field = blur_noise(rng, width, height, 2.5) * grain * 1.6 + blur_noise(rng, width, height, 46) * grain * 3.0
    canvas = np.clip(canvas + field[:, :, None], 0, 255)
    yy, xx = np.mgrid[0:height, 0:width].astype("float32")
    r = np.sqrt(((xx - width / 2) / (width / 2)) ** 2 + ((yy - height / 2) / (height / 2)) ** 2)
    canvas = np.clip(canvas - np.clip(r - 0.62, 0, None)[:, :, None] ** 2 * 255 * vignette, 0, 255)
    img = Image.fromarray(canvas.astype("uint8"), mode="RGB").convert("RGBA")

    if bokeh > 0:
        w, h = width, height
        add_bokeh(img, [
            (0.99 * w, 0.03 * h, 0.30 * h, 210, 1, 0.30 * bokeh),
            (0.09 * w, 0.18 * h, 0.24 * h, 200, -1, 0.22 * bokeh),
            (0.01 * w, 0.54 * h, 0.20 * h, 195, 1, 0.18 * bokeh),
            (1.02 * w, 0.42 * h, 0.22 * h, 205, -1, 0.20 * bokeh),
        ], rng)
    if "drape" in props:
        draw_drape(img, height, band, rng)
    if "linen" in props:
        draw_linen(img, (int(-0.03 * width), int(0.875 * height),
                         int(0.40 * width), int(1.03 * height)), rng)
    if "leafshadow" in props:
        draw_leaf_shadows(img, rng)
    if "bamboo" in props:
        draw_bamboo(img, rng)
    if podium2:
        cx2 = (podium2[0] + podium2[2]) / 2 * width
        rx2 = max(24.0, (podium2[2] - podium2[0]) / 2 * width)
        top2 = podium2[1] * height
        depth2 = max(20.0, (podium2[3] - podium2[1]) * height)
        draw_pedestal(img, cx2, top2, rx2, rx2 * 0.17, depth2, rng, kind=podium_kind)
    if pedestal:
        cx = (pedestal[0] + pedestal[2]) / 2 * width
        rx = (pedestal[2] - pedestal[0]) / 2 * width
        top_y = pedestal[1] * height
        depth = max(24.0, (pedestal[3] - pedestal[1]) * height)
        draw_pedestal(img, cx, top_y, rx, rx * 0.17, depth, rng, kind=podium_kind)
    if "water" in props and water_y:
        draw_water(img, int(water_y * height), rng)
    if "branch" in props or "sprig" in props:
        side = -1 if branch_side == "left" else 1
        draw_branch(img, (width * branch_base[0], height * branch_base[1]),
                    height * branch_length, 18 if side > 0 else -18, side, rng,
                    leaves=6, scale=1.0)
    if "pine" in props:
        draw_branch(img, (product_x * width - 0.225 * width, 0.905 * height),
                    0.16 * height, 24, 1, rng, leaves=9, scale=0.62, tone=PINE, blur=3.2)
        draw_branch(img, (product_x * width + 0.215 * width, 0.925 * height),
                    0.14 * height, 22, -1, rng, leaves=8, scale=0.58, tone=PINE, blur=4.5)
        draw_branch(img, (0.27 * width, 0.975 * height),
                    0.11 * height, 18, 1, rng, leaves=7, scale=0.52, tone=PINE, blur=2.4)
    if "fruit" in props:
        top = (1.0 - band) * height
        for (dx, r) in ((-0.17, 0.026), (-0.09, 0.020), (0.135, 0.023), (0.205, 0.017)):
            draw_fruit(img, (product_x * width + dx * width, top + band * height * (0.62 if dx < 0 else 0.78)),
                       r * width, rng)
    if "pod" in props:
        top = (1.0 - band) * height
        draw_pod(img, (product_x * width - 0.245 * width, top + band * height * 0.72),
                 0.036 * width, rng)
    if "citrus" in props:
        draw_citrus(img, (0.63 * width, 0.925 * height), 0.045 * width, rng)
    if "pebble" in props:
        draw_pebble(img, (0.115 * width, 0.945 * height), 0.036 * width, 0.021 * width, rng)
        draw_pebble(img, (0.90 * width, 0.972 * height), 0.028 * width, 0.017 * width, rng)
    return img.convert("RGB")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="生成指定尺寸的商品场景底图（渐变 + 配景）")
    ap.add_argument("--out", required=True)
    ap.add_argument("--width", type=int, default=1200)
    ap.add_argument("--height", type=int, default=1500)
    ap.add_argument("--palette", default="sage", choices=sorted(PALETTES))
    ap.add_argument("--props", default="linen,sprig,citrus",
                    help="配景，逗号分隔：drape,linen,sprig,citrus,pebble,pine,fruit,pod")
    ap.add_argument("--branch-side", default="right", choices=["left", "right", "none"])
    ap.add_argument("--branch-base", nargs=2, type=float, default=[0.74, 0.945], help="枝条根部 x y（比例）")
    ap.add_argument("--branch-length", type=float, default=0.20, help="枝条长度（画布高度比例）")
    ap.add_argument("--floor", nargs=2, type=float, default=[0.0, 0.88], help="保留参数，第二个值为地面高度比例")
    ap.add_argument("--pedestal", nargs=4, type=float, default=[0.28, 0.9213, 0.72, 0.9813],
                    help="石台 x0 y0 x1 y1（画布比例）")
    ap.add_argument("--no-pedestal", action="store_true")
    ap.add_argument("--glow", nargs=5, type=float, default=[0.50, 0.42, 0.46, 0.36, 0.55],
                    help="柔光池 cx cy rx ry strength（比例）")
    ap.add_argument("--grain", type=float, default=0.22)
    ap.add_argument("--vignette", type=float, default=0.28)
    ap.add_argument("--band", type=float, default=0.21, help="底部配景带占图高比例（0.2 = 五分之一）")
    ap.add_argument("--product-x", type=float, default=0.68, help="商品主体中心横向位置（0–1），用于摆放配景")
    ap.add_argument("--bokeh", type=float, default=0.0, help="边缘虚化枝叶强度 0–1.5")
    ap.add_argument("--podium-kind", default="stone", choices=["stone", "travertine"],
                    help="台座材质：stone 深灰石 / travertine 浅水磨石")
    ap.add_argument("--podium2", nargs=4, type=float, default=None,
                    help="第二座台（先于主台绘制，做前后层次）x0 y0 x1 y1（画布比例）")
    ap.add_argument("--water", type=float, default=None,
                    help="水面起始高度比例（例 0.84），配合 --props 里的 water")
    ap.add_argument("--seed", type=int, default=20261001)
    args = ap.parse_args(argv)

    if args.width <= 0 or args.height <= 0:
        ap.error("宽高必须为正整数")
    props = [p.strip() for p in args.props.split(",") if p.strip()]
    img = build(args.width, args.height, args.palette, props, args.floor,
                None if args.no_pedestal else args.pedestal, args.branch_side,
                args.branch_base, args.branch_length, args.glow, args.grain,
                args.vignette, args.seed, band=args.band, product_x=args.product_x,
                bokeh=args.bokeh, podium_kind=args.podium_kind,
                water_y=args.water, podium2=args.podium2)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print(f"已生成场景底图 {out}  {img.width}×{img.height}  palette={args.palette}  props={props}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
