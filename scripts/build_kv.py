#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_kv.py — 按 JSON 规格确定性合成受支持画布的电商主视觉。

分工原则（本 skill 的核心）：
    * 画面（商品 / 场景 / 光线）来自实拍图、抠图或生图底图；
    * 信息（标题 / 卖点 / 参数 / 价格 / 活动时间 / 品牌字标）由本脚本排版渲染。
生图模型容易写错中文、价格与日期，所以文字一律不进生图提示词。

用法：
    python build_kv.py --spec work/spec/kv-cn.json --out work/render/KV-CN-4x5.png
    python build_kv.py --spec work/spec/kv-en.json --out work/render/KV-EN-4x5.png

规格字段见 references/spec-schema.md；骨架样例见 assets/templates/。
"""

from __future__ import annotations

import argparse
import json
import math
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFilter, ImageFont
except ImportError:  # pragma: no cover
    sys.exit("需要 Pillow：pip install pillow")


def use_utf8_stdio() -> None:
    """Windows 控制台默认 GBK，会把中文输出打成乱码。"""
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass


use_utf8_stdio()


# --------------------------------------------------------------------------- 字体

FONT_DIR = Path(os.environ.get("KV_FONT_DIR") or r"C:\Windows\Fonts")
EXTRA_FONT_DIRS = [
    FONT_DIR,
    Path("/Library/Fonts"),
    Path("/System/Library/Fonts"),
    Path("/usr/share/fonts"),
    Path("/usr/share/fonts/truetype"),
    Path("/usr/share/fonts/opentype"),
    Path.home() / ".fonts",
    Path.home() / "Library" / "Fonts",
]

# family / weight -> 候选字体文件（按优先级）
FONT_FILES = {
    ("cn", "light"): ["msyhl.ttc", "Deng.ttf", "NotoSansSC-VF.ttf", "msyh.ttc"],
    ("cn", "regular"): ["msyh.ttc", "NotoSansSC-VF.ttf", "Deng.ttf", "simhei.ttf", "simsun.ttc"],
    ("cn", "medium"): ["msyh.ttc", "NotoSansSC-VF.ttf", "Deng.ttf", "simhei.ttf"],
    ("cn", "bold"): ["msyhbd.ttc", "Dengb.ttf", "simhei.ttf", "msyh.ttc", "NotoSansSC-VF.ttf"],
    ("cn", "black"): ["msyhbd.ttc", "Dengb.ttf", "simhei.ttf", "msyh.ttc"],
    ("cn", "serif"): ["simsun.ttc", "NotoSerifSC-VF.ttf", "simsunb.ttf"],
    ("en", "light"): ["segoeuil.ttf", "segoeui.ttf", "arial.ttf", "NotoSansSC-VF.ttf"],
    ("en", "regular"): ["segoeui.ttf", "arial.ttf", "bahnschrift.ttf", "NotoSansSC-VF.ttf"],
    ("en", "medium"): ["seguisb.ttf", "segoeuib.ttf", "arialbd.ttf"],
    ("en", "bold"): ["segoeuib.ttf", "arialbd.ttf", "seguisb.ttf"],
    ("en", "black"): ["segoeuib.ttf", "arialbd.ttf", "ARIALNB.TTF", "bahnschrift.ttf"],
}

WARNINGS: list[str] = []
_font_file_cache: dict[str, Path | None] = {}
_font_cache: dict[tuple, ImageFont.FreeTypeFont] = {}
_warned: set[str] = set()


def warn(msg: str) -> None:
    if msg not in _warned:
        _warned.add(msg)
        WARNINGS.append(msg)
        print(f"[warn] {msg}", file=sys.stderr)


def _search_font(name: str) -> Path | None:
    if name in _font_file_cache:
        return _font_file_cache[name]
    found = None
    for d in EXTRA_FONT_DIRS:
        if not d.exists():
            continue
        cand = d / name
        if cand.exists():
            found = cand
            break
    if found is None:
        for d in EXTRA_FONT_DIRS:
            if not d.exists():
                continue
            try:
                hits = list(d.rglob(name))
            except OSError:
                hits = []
            if hits:
                found = hits[0]
                break
    _font_file_cache[name] = found
    return found


def resolve_font_file(name: str, overrides: dict) -> Path | None:
    if name in overrides:
        target = overrides[name]
        if isinstance(target, dict):
            target = target.get("path")
        p = Path(target).expanduser()
        if p.exists():
            return p
        # 只写了文件名、或该机器上路径不同：按文件名去系统字体目录里找
        return _search_font(p.name)
    return _search_font(name)


def _instantiate_font(path: Path, size: int, override) -> ImageFont.FreeTypeFont:
    """支持 {"path":..., "index":0, "variation":"Bold"} 形式的可变字体指定。"""
    index = 0
    variation = None
    if isinstance(override, dict):
        index = int(override.get("index", 0) or 0)
        variation = override.get("variation")
    font = ImageFont.truetype(str(path), int(size), index=index)
    if variation:
        try:
            if isinstance(variation, str):
                font.set_variation_by_name(variation)
            elif isinstance(variation, (list, tuple)):
                font.set_variation_by_axes([float(v) for v in variation])
            elif isinstance(variation, dict):
                axes = list(font.get_variation_axes())
                font.set_variation_by_axes([float(variation.get(a["name"].decode(), a["default"]))
                                            for a in axes])
        except Exception as exc:  # pragma: no cover
            warn(f"字体变体设置失败（{path.name} / {variation}）：{exc}，将使用默认字重")
    return font


def load_font(family: str, weight: str, size: int, overrides: dict) -> ImageFont.FreeTypeFont:
    key = (family, weight, int(size), json.dumps(overrides, sort_keys=True, ensure_ascii=False))
    if key in _font_cache:
        return _font_cache[key]
    for custom in (family, f"{family}-{weight}"):
        if custom in overrides:
            target = overrides[custom]
            path = resolve_font_file(custom, overrides)
            if path is not None:
                font = _instantiate_font(path, int(size), target)
                _font_cache[key] = font
                return font
            warn(f"自定义字体键 {custom} 指向的文件不存在，回退到系统字体")
    chain = list(FONT_FILES.get((family, weight), []))
    if weight != "regular":
        chain += [f for f in FONT_FILES.get((family, "regular"), []) if f not in chain]
    chain += [f for f in FONT_FILES[("cn", "regular")] if f not in chain]
    chain += [f for f in FONT_FILES[("en", "regular")] if f not in chain]
    for name in chain:
        path = resolve_font_file(name, overrides)
        if path is None:
            continue
        try:
            font = _instantiate_font(path, int(size), overrides.get(name))
        except OSError:
            continue
        _font_cache[key] = font
        return font
    warn(f"未找到可用字体（{family}/{weight}），回退为内置位图字体，字形可能异常")
    font = ImageFont.load_default()
    _font_cache[key] = font
    return font


# --------------------------------------------------------------------------- 基础工具

def parse_color(value, default=None):
    if value is None:
        return default
    if isinstance(value, (list, tuple)):
        vals = [int(v) for v in value]
        if len(vals) == 3:
            vals.append(255)
        return tuple(vals)
    s = str(value).strip()
    if s == "" or s.lower() in ("none", "transparent", "null"):
        return None
    if s.startswith("#"):
        h = s[1:]
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        if len(h) == 6:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
        if len(h) == 8:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), int(h[6:8], 16))
        raise ValueError(f"无法解析颜色：{value}")
    try:
        from PIL import ImageColor
        rgb = ImageColor.getrgb(s)
        if len(rgb) == 3:
            rgb = rgb + (255,)
        return rgb
    except Exception as exc:  # pragma: no cover
        raise ValueError(f"无法解析颜色：{value}") from exc


def apply_opacity(img: Image.Image, opacity: float) -> Image.Image:
    if opacity >= 0.999:
        return img
    alpha = img.getchannel("A").point(lambda v: int(v * max(0.0, min(1.0, opacity))))
    img.putalpha(alpha)
    return img


def box_of(layer: dict) -> tuple[int, int, int, int]:
    box = layer.get("box")
    if not box or len(box) != 4:
        raise ValueError(f"图层缺少 box [x,y,w,h]：{layer.get('type')} / {layer.get('text', '')[:20]}")
    x, y, w, h = (float(v) for v in box)
    return int(round(x)), int(round(y)), int(round(w)), int(round(h))


CJK_RANGES = (
    (0x1100, 0x11FF), (0x2E80, 0x2FDF), (0x3000, 0x303F), (0x3040, 0x30FF),
    (0x3130, 0x318F), (0x3400, 0x4DBF), (0x4E00, 0x9FFF), (0xA960, 0xA97F),
    (0xAC00, 0xD7AF), (0xF900, 0xFAFF), (0xFE30, 0xFE4F), (0xFF00, 0xFFEF),
)


def is_cjk(ch: str) -> bool:
    cp = ord(ch)
    return any(lo <= cp <= hi for lo, hi in CJK_RANGES)


def has_cjk(text: str) -> bool:
    return any(is_cjk(c) for c in text)


def pick_family(text: str, preferred: str) -> str:
    """文字含中文/日韩字符时强制用 CJK 字体，避免出现豆腐块（.notdef）。"""
    if has_cjk(text) and preferred in ("en",):
        return "cn"
    return preferred


def tokenize(text: str) -> list[dict]:
    """切成排版 token：硬换行 / 显式空格 / 单个 CJK 字符 / 拉丁词。"""
    tokens: list[dict] = []
    i, n = 0, len(text)
    while i < n:
        ch = text[i]
        if ch == "\n":
            tokens.append({"text": "\n", "break": True, "space": False})
            i += 1
        elif ch in (" ", "\t"):
            tokens.append({"text": " ", "space": True})
            i += 1
        elif is_cjk(ch):
            tokens.append({"text": ch, "space": False})
            i += 1
        else:
            j = i
            while j < n and text[j] not in (" ", "\t", "\n") and not is_cjk(text[j]):
                j += 1
            tokens.append({"text": text[i:j], "space": False})
            i = j
    return tokens


def run_width(text: str, font, letter_spacing: float, word_spacing: float = 1.0) -> float:
    if not text:
        return 0.0
    width = float(font.getlength(text))
    if word_spacing != 1.0 and text.strip() == "":
        width *= word_spacing
    return width + letter_spacing * (len(text) - 1)


def tok_width(text: str, font, letter_spacing: float, word_spacing: float, is_space: bool) -> float:
    return run_width(text, font, letter_spacing, word_spacing if is_space else 1.0)


def draw_run(draw: ImageDraw.ImageDraw, xy, text: str, font, fill, letter_spacing: float,
             anchor: str = "ls", stroke_width: int = 0, stroke_fill=None) -> None:
    x, y = xy
    if stroke_width and stroke_fill is not None:
        stroke_kwargs = {"stroke_width": int(stroke_width), "stroke_fill": stroke_fill}
    else:
        stroke_kwargs = {}
    if letter_spacing == 0:
        _safe_text(draw, (x, y), text, font, fill, anchor, stroke_kwargs)
        return
    cursor = x
    for ch in text:
        _safe_text(draw, (cursor, y), ch, font, fill, anchor, stroke_kwargs)
        cursor += float(font.getlength(ch)) + letter_spacing


def _safe_text(draw, xy, text, font, fill, anchor, stroke_kwargs) -> None:
    try:
        draw.text(xy, text, font=font, fill=fill, anchor=anchor, **stroke_kwargs)
    except (ValueError, TypeError):
        draw.text(xy, text, font=font, fill=fill, **stroke_kwargs)


# --------------------------------------------------------------------------- 文本排版引擎

class TextEngine:
    """把带样式的文字流按盒子宽度折行，并在盒子里做最小可读字号自适应。"""

    def __init__(self, layer: dict, ctx: "RenderContext"):
        self.layer = layer
        self.ctx = ctx
        self.letter_spacing = float(layer.get("letter_spacing", 0) or 0)
        self.line_spacing = float(layer.get("line_spacing", 1.14) or 1.14)
        self.word_spacing = float(layer.get("word_spacing", 1.0) or 1.0)
        self.max_lines = int(layer.get("max_lines", 0) or 0)
        self.spans = self._spans()
        self.min_size = int(layer.get("min_size", max(14, int(layer.get("size", 40) * 0.45))))

    def _spans(self) -> list[dict]:
        base_family = self.layer.get("font", "cn")
        base_weight = self.layer.get("weight", "regular")
        base_size = int(self.layer.get("size", 40))
        base_color = self.layer.get("color", "#111111")
        raw = self.layer.get("spans")
        if not raw:
            text = str(self.layer.get("text", ""))
            if self.layer.get("uppercase"):
                text = text.upper()
            raw = [{"text": text}]
        spans = []
        for sp in raw:
            text = str(sp.get("text", ""))
            if self.layer.get("uppercase") or sp.get("uppercase"):
                text = text.upper()
            family = sp.get("font", base_family)
            if has_cjk(text) and family == "en":
                warn(f"含中文的文本被指定为英文字体，已改用中文字体：{text[:12]}…")
                family = "cn"
            spans.append({
                "text": text,
                "family": family,
                "weight": sp.get("weight", base_weight),
                "size": float(sp.get("size", base_size)),
                "color": parse_color(sp.get("color"), parse_color(base_color, (17, 17, 17, 255))),
                "spacing": float(sp.get("letter_spacing", self.letter_spacing) or 0),
            })
        return spans

    def _stream(self) -> list[dict]:
        stream: list[dict] = []
        for idx, span in enumerate(self.spans):
            for tok in tokenize(span["text"]):
                tok = dict(tok)
                tok["span"] = idx
                stream.append(tok)
        return stream

    def layout(self, size_scale: float, box_w: int) -> dict:
        fonts, ascents, descents = [], [], []
        for span in self.spans:
            size = max(1, int(round(span["size"] * size_scale)))
            font = load_font(span["family"], span["weight"], size, self.ctx.font_overrides)
            fonts.append(font)
            a, d = font.getmetrics()
            ascents.append(a)
            descents.append(d)

        ascent = max(ascents)
        descent = max(descents)
        step = max(1, int(round((ascent + descent) * self.line_spacing)))

        stream = self._stream()
        lines: list[list[dict]] = [[]]
        widths: list[float] = [0.0]
        for tok in stream:
            if tok.get("break"):
                if lines[-1]:
                    lines.append([])
                    widths.append(0.0)
                continue
            span = self.spans[tok["span"]]
            font = fonts[tok["span"]]
            tw = tok_width(tok["text"], font, span["spacing"], self.word_spacing, tok["space"])
            current = lines[-1]
            if tok["space"] and not current:
                continue
            if widths[-1] + tw > box_w and current:
                while current and current[-1]["space"]:
                    widths[-1] -= tok_width(current[-1]["text"], fonts[current[-1]["span"]],
                                            self.spans[current[-1]["span"]]["spacing"],
                                            self.word_spacing, True)
                    current.pop()
                if not current:
                    lines[-1] = [tok]
                    widths[-1] = tw
                    continue
                lines.append([tok])
                widths.append(tw)
            else:
                current.append(tok)
                widths[-1] += tw
        while lines and not lines[-1]:
            lines.pop()
            widths.pop()
        if not lines:
            lines, widths = [[]], [0.0]
        total_h = (len(lines) - 1) * step + ascent + descent
        return {
            "fonts": fonts, "ascent": ascent, "descent": descent, "step": step,
            "lines": lines, "widths": widths, "total_h": total_h,
            "size_scale": size_scale,
        }

    def fit(self, box_w: int, box_h: int) -> dict:
        size = float(self.layer.get("size", 40))
        best = None
        scale = 1.0
        while scale >= max(0.05, self.min_size / max(size, 1)):
            data = self.layout(scale, box_w)
            if data["total_h"] <= box_h and (not self.max_lines or len(data["lines"]) <= self.max_lines):
                best = data
                break
            best = data
            scale -= 0.02
        assert best is not None
        if best["size_scale"] < 0.6:
            warn(f"文案过长，字号已压缩到 {int(best['size_scale'] * 100)}%："
                 f"{str(self.layer.get('text', ''))[:16]}…（建议改写或增大盒子）")
        if best["total_h"] > box_h:
            warn(f"文案高度超出盒子：{str(self.layer.get('text', ''))[:16]}…")
        if self.max_lines and len(best["lines"]) > self.max_lines:
            warn(f"文案行数超出 max_lines={self.max_lines}：{str(self.layer.get('text', ''))[:16]}…")
        return best


def render_text_layer(canvas: Image.Image, layer: dict, ctx: "RenderContext") -> None:
    x, y, w, h = box_of(layer)
    engine = TextEngine(layer, ctx)
    data = engine.fit(w, h)
    ascent, step = data["ascent"], data["step"]
    align = layer.get("align", "left")
    valign = layer.get("valign", "top")
    stroke = layer.get("stroke") or {}
    stroke_w = int(stroke.get("width", 0) or 0)
    shadow = layer.get("shadow") or {}

    pad = int(max(24, stroke_w * 2 + 6, float(shadow.get("blur", 0) or 0) * 2
                  + abs(float((shadow.get("offset") or [0, 0])[0])) + 12))
    local = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))

    y0 = pad
    if valign == "middle":
        y0 = pad + max(0, (h - data["total_h"]) // 2)
    elif valign == "bottom":
        y0 = pad + max(0, h - data["total_h"])

    def paint(target: Image.Image, color_override=None, dx: int = 0, dy: int = 0,
              force: bool = False) -> None:
        d = ImageDraw.Draw(target)
        for i, line in enumerate(data["lines"]):
            baseline = y0 + i * step + ascent + dy
            line_w = data["widths"][i]
            if align == "center":
                start_x = pad + (w - line_w) / 2
            elif align == "right":
                start_x = pad + (w - line_w)
            else:
                start_x = pad
            cursor = start_x + dx
            for tok in line:
                span = engine.spans[tok["span"]]
                font = data["fonts"][tok["span"]]
                color = color_override or span["color"]
                draw_run(d, (cursor, baseline), tok["text"], font, color, span["spacing"],
                         anchor="ls", stroke_width=stroke_w,
                         stroke_fill=parse_color(stroke.get("color"), (0, 0, 0, 255)))
                adv = tok_width(tok["text"], font, span["spacing"], engine.word_spacing, tok["space"])
                if force and (layer.get("strike") or layer.get("underline")):
                    tw = adv
                    size = span["size"] * data["size_scale"]
                    thickness = max(2, int(size * 0.06))
                    if layer.get("strike"):
                        ly = baseline - size * 0.30
                        d.rectangle([cursor, ly, cursor + tw, ly + thickness], fill=color)
                    if layer.get("underline"):
                        ly = baseline + size * 0.12
                        d.rectangle([cursor, ly, cursor + tw, ly + thickness], fill=color)
                cursor += adv

    if shadow:
        shadow_color = parse_color(shadow.get("color"), (0, 0, 0, 110))
        off = shadow.get("offset") or [0, 6]
        blur = float(shadow.get("blur", 0) or 0)
        shadow_layer = Image.new("RGBA", local.size, (0, 0, 0, 0))
        paint(shadow_layer, color_override=shadow_color,
              dx=int(off[0]), dy=int(off[1]))
        if blur > 0:
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur))
        local.alpha_composite(shadow_layer)

    paint(local, force=True)

    rotate = float(layer.get("rotate", 0) or 0)
    if rotate:
        local = local.rotate(rotate, resample=Image.BICUBIC, expand=False)

    apply_opacity(local, float(layer.get("opacity", 1) or 1))
    canvas.alpha_composite(local, (x - pad, y - pad))


# --------------------------------------------------------------------------- 其他图层

def fit_image(img: Image.Image, size, mode: str) -> Image.Image:
    tw, th = size
    iw, ih = img.size
    if mode == "stretch":
        return img.resize((tw, th), Image.LANCZOS)
    scale = max(tw / iw, th / ih) if mode == "cover" else min(tw / iw, th / ih)
    resized = img.resize((max(1, int(round(iw * scale))), max(1, int(round(ih * scale)))), Image.LANCZOS)
    out = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    out.alpha_composite(resized, ((tw - resized.width) // 2, (th - resized.height) // 2))
    return out


def load_image(path: str, layer: dict) -> Image.Image | None:
    p = Path(path).expanduser()
    if not p.exists():
        if layer.get("optional"):
            warn(f"可选图片不存在，已跳过：{p}")
            return None
        raise FileNotFoundError(f"图片不存在：{p}（如尚未准备底图，可先设 \"optional\": true 出布局确认稿）")
    return Image.open(p).convert("RGBA")


def draw_polyline(draw, points, color, width: int, dash=None) -> None:
    pts = [(float(p[0]), float(p[1])) for p in points]
    width = max(1, int(width))
    if not dash:
        draw.line(pts, fill=color, width=width, joint="curve")
        return
    on, off = (dash if isinstance(dash, (list, tuple)) and len(dash) == 2 else [dash, dash])
    on, off = max(1.0, float(on)), max(1.0, float(off))
    for i in range(len(pts) - 1):
        (x1, y1), (x2, y2) = pts[i], pts[i + 1]
        seg = math.hypot(x2 - x1, y2 - y1)
        if seg == 0:
            continue
        ux, uy = (x2 - x1) / seg, (y2 - y1) / seg
        pos = 0.0
        while pos < seg:
            end = min(pos + on, seg)
            draw.line([(x1 + ux * pos, y1 + uy * pos), (x1 + ux * end, y1 + uy * end)],
                      fill=color, width=width)
            pos = end + off


def draw_plus_node(draw, center, radius: float, fill, glyph_color) -> None:
    cx, cy = center
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius], fill=fill)
    arm = radius * 0.46
    w = max(2, int(radius * 0.20))
    draw.line([(cx - arm, cy), (cx + arm, cy)], fill=glyph_color, width=w)
    draw.line([(cx, cy - arm), (cx, cy + arm)], fill=glyph_color, width=w)


def render_shape_layer(layer: dict, ctx: "RenderContext") -> Image.Image:
    kind = layer["type"]
    size = ctx.canvas_size
    tmp = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(tmp)

    if kind in ("rect", "ellipse"):
        x, y, w, h = box_of(layer)
        fill = parse_color(layer.get("fill"))
        outline = parse_color(layer.get("outline", {}).get("color") if isinstance(layer.get("outline"), dict)
                              else layer.get("outline"))
        ow = int((layer.get("outline") or {}).get("width", layer.get("outline_width", 0)) or 0) \
            if isinstance(layer.get("outline"), dict) else int(layer.get("outline_width", 0) or 0)
        radius = layer.get("radius", 0)
        if isinstance(radius, str):
            radius = h / 2 if radius == "pill" else 0
        radius = int(radius or 0)
        rect = [x, y, x + w, y + h]
        if kind == "ellipse":
            draw.ellipse(rect, fill=fill, outline=outline, width=max(0, ow))
        elif radius <= 0:
            draw.rectangle(rect, fill=fill, outline=outline, width=max(0, ow))
        else:
            radius = int(min(radius, min(w, h) / 2))
            draw.rounded_rectangle(rect, radius=radius, fill=fill, outline=outline, width=max(0, ow))
        if layer.get("corners") == "top":
            draw.rectangle([x, y + radius, x + w, y + h], fill=fill)

    elif kind == "polygon":
        pts = [(float(p[0]), float(p[1])) for p in layer["points"]]
        draw.polygon(pts, fill=parse_color(layer.get("fill")), outline=parse_color(layer.get("outline_color")))

    elif kind == "line":
        draw_polyline(draw, layer["points"], parse_color(layer.get("color"), (0, 0, 0, 255)),
                      int(layer.get("width", 2) or 2), layer.get("dash"))

    elif kind == "image":
        img = load_image(layer["path"], layer)
        if img is None:
            return tmp
        x, y, w, h = box_of(layer)
        fitted = fit_image(img, (w, h), layer.get("fit", "cover"))
        brightness = float(layer.get("brightness", 1) or 1)
        if brightness != 1:
            from PIL import ImageEnhance
            rgb = fitted.convert("RGB")
            rgb = ImageEnhance.Brightness(rgb).enhance(brightness)
            fitted = rgb.convert("RGBA")
        radius = layer.get("corner_radius", 0)
        if radius:
            mask = Image.new("L", (w, h), 0)
            ImageDraw.Draw(mask).rounded_rectangle([0, 0, w, h], radius=int(radius), fill=255)
            fitted.putalpha(Image.composite(fitted.getchannel("A"), Image.new("L", (w, h), 0), mask))
        tmp.alpha_composite(fitted, (x, y))

    elif kind == "scrim":
        x, y, w, h = box_of(layer)
        direction = layer.get("direction", "bottom")
        start = float(layer.get("opacity_start", 0.0) or 0.0)
        end = float(layer.get("opacity_end", 0.75) or 0.0)
        color = parse_color(layer.get("color"), (0, 0, 0, 255))[:3]
        grad = Image.linear_gradient("L")
        if direction == "top":
            grad = grad.rotate(180)
        grad = grad.resize((w, h), Image.BILINEAR)
        span = max(end - start, 0.0)

        def mapped(v: int) -> int:
            return int(max(0.0, min(1.0, start + span * (v / 255.0))) * 255)

        alpha = grad.point(mapped)
        layer_img = Image.new("RGBA", (w, h), color + (255,))
        layer_img.putalpha(alpha)
        tmp.alpha_composite(layer_img, (x, y))

    elif kind == "shadow":
        img = load_image(layer["path"], layer)
        if img is None:
            return tmp
        x, y, w, h = box_of(layer)
        fitted = fit_image(img, (w, h), layer.get("fit", "contain"))
        alpha = fitted.getchannel("A")
        blur = float(layer.get("blur", 24) or 0)
        if blur > 0:
            alpha = alpha.filter(ImageFilter.GaussianBlur(blur))
        strength = float(layer.get("opacity", 0.4) or 0.4)
        alpha = alpha.point(lambda v: int(v * strength))
        color = parse_color(layer.get("color"), (40, 34, 28, 255))[:3]
        shadow_img = Image.new("RGBA", fitted.size, color + (255,))
        shadow_img.putalpha(alpha)
        off = layer.get("offset") or [0, 14]
        tmp.alpha_composite(shadow_img, (x + int(off[0]), y + int(off[1])))

    elif kind == "chip":
        x, y, w, h = box_of(layer)
        engine = TextEngine({**layer, "valign": "middle", "align": "left", "max_lines": 1}, ctx)
        text = str(layer.get("text", "")).replace("\n", " ").strip()
        size = int(layer.get("size", 32))
        font = load_font(engine.spans[0]["family"] if engine.spans else "cn",
                         layer.get("weight", "regular"), size, ctx.font_overrides)
        tw = run_width(text, font, float(layer.get("letter_spacing", 0) or 0))
        pad = int(layer.get("side_pad", max(20, size * 0.7)))
        auto = bool(layer.get("auto_width"))
        chip_w = int(tw + pad * 2) if auto else w
        if auto and layer.get("align") == "center":
            x = x + (w - chip_w) // 2
        elif auto and layer.get("align") == "right":
            x = x + w - chip_w
        radius = layer.get("radius", "pill")
        radius = int(chip_w / 2 if radius == "pill" else radius or 0)
        fill = parse_color(layer.get("fill"))
        outline = parse_color(layer.get("outline") if not isinstance(layer.get("outline"), dict)
                              else layer.get("outline", {}).get("color"))
        ow = int((layer.get("outline") or {}).get("width", 0) or 0) if isinstance(layer.get("outline"), dict) else 0
        rect = [x, y, x + chip_w, y + h]
        if radius > 0:
            draw.rounded_rectangle(rect, radius=int(min(radius, h / 2)), fill=fill, outline=outline, width=ow)
        else:
            draw.rectangle(rect, fill=fill, outline=outline, width=ow)
        a, d = font.getmetrics()
        baseline = y + (h + a - d) / 2
        draw_run(draw, (x + pad, baseline), text, font, parse_color(layer.get("color"), (255, 255, 255, 255)),
                 float(layer.get("letter_spacing", 0) or 0))
        icon = layer.get("icon", "none")
        gap = int(layer.get("icon_gap", 12))
        if icon == "plus_circle":
            r = int(max(12, h * 0.42))
            draw_plus_node(draw, (x + chip_w + gap + r, y + h / 2), r,
                           parse_color(layer.get("icon_color"), fill),
                           parse_color(layer.get("icon_glyph_color"), (255, 255, 255, 255)))
        elif icon == "plus":
            r = int(max(6, h * 0.22))
            color = parse_color(layer.get("icon_color"), (255, 255, 255, 255))
            cx = x + chip_w + gap + r
            cy = y + h / 2
            wdt = max(2, int(r * 0.4))
            draw.line([(cx - r, cy), (cx + r, cy)], fill=color, width=wdt)
            draw.line([(cx, cy - r), (cx, cy + r)], fill=color, width=wdt)
        elif icon == "dot":
            r = int(max(5, h * 0.16))
            draw.ellipse([x + chip_w + gap, y + h / 2 - r, x + chip_w + gap + 2 * r, y + h / 2 + r],
                         fill=parse_color(layer.get("icon_color"), (255, 255, 255, 255)))

    elif kind in ("list", "metrics", "callout"):
        render_structured_layer(tmp, layer, ctx, draw)

    elif kind == "circular_text":
        render_circular_text(tmp, layer, ctx)

    elif kind == "group":
        for sub in layer.get("layers", []):
            sub_img = Image.new("RGBA", ctx.canvas_size, (0, 0, 0, 0))
            render_layer(sub_img, sub, ctx, single=True)
            tmp.alpha_composite(sub_img)

    else:
        warn(f"未知图层类型，已跳过：{kind}")

    return apply_opacity(tmp, float(layer.get("opacity", 1) or 1))


def render_structured_layer(tmp: Image.Image, layer: dict, ctx: "RenderContext", draw) -> None:
    kind = layer["type"]
    x, y, w, h = box_of(layer)
    pad_local = 60
    min_x, min_y = x - pad_local, y - pad_local
    max_x, max_y = x + w + pad_local, y + h + pad_local
    anchor = layer.get("anchor")
    if anchor:
        node_cfg = layer.get("node") or {}
        reach = float(node_cfg.get("size", 15) or 15) + 24
        ax, ay = float(anchor[0]), float(anchor[1])
        min_x, min_y = min(min_x, ax - reach), min(min_y, ay - reach)
        max_x, max_y = max(max_x, ax + reach), max(max_y, ay + reach)
    min_x, min_y = int(math.floor(min_x)), int(math.floor(min_y))
    max_x, max_y = int(math.ceil(max_x)), int(math.ceil(max_y))
    local = Image.new("RGBA", (max_x - min_x, max_y - min_y), (0, 0, 0, 0))
    d = ImageDraw.Draw(local)
    origin = (x - min_x, y - min_y)

    if kind == "list":
        marker = layer.get("marker") or {}
        mtype = marker.get("type", "bar")
        mcolor = parse_color(marker.get("color"), parse_color(layer.get("marker_color"), (120, 120, 120, 255)))
        mgap = int(marker.get("gap", max(18, float(layer.get("size", 36)) * 0.6)))
        gutter = 0 if mtype == "none" else int(marker.get("width", 6) or 6) + mgap
        if mtype == "dot":
            gutter = int(marker.get("size", 18) or 18) + mgap
        if mtype == "plus":
            gutter = int(marker.get("size", 22) or 22) + mgap
        gap = int(layer.get("gap", 24) or 24)
        cursor = origin[1]
        for item in layer.get("items", []):
            text = str(item.get("text", item) if isinstance(item, dict) else item)
            engine = TextEngine({**layer, "text": text, "spans": None}, ctx)
            data = engine.fit(max(10, w - gutter), int(float(layer.get("size", 36)) * 3))
            ascent, step = data["ascent"], data["step"]
            mx = origin[0]
            if mtype == "bar":
                bw = int(marker.get("width", 6) or 6)
                d.rectangle([mx, cursor + 2, mx + bw, cursor + data["total_h"] - 2], fill=mcolor)
            elif mtype == "dot":
                r = int(marker.get("size", 18) or 18) // 2
                cy = cursor + ascent - (ascent + data["descent"]) / 2
                d.ellipse([mx, cy - r, mx + 2 * r, cy + r], fill=mcolor)
            elif mtype == "plus":
                r = int(marker.get("size", 22) or 22) // 2
                cy = cursor + ascent - (ascent + data["descent"]) / 2
                draw_plus_node(d, (mx + r, cy), r, mcolor,
                               parse_color(marker.get("glyph_color"), (255, 255, 255, 255)))
            for i, line in enumerate(data["lines"]):
                baseline = cursor + i * step + ascent
                cursor_x = origin[0] + gutter
                for tok in line:
                    span = engine.spans[tok["span"]]
                    font = data["fonts"][tok["span"]]
                    draw_run(d, (cursor_x, baseline), tok["text"], font, span["color"], span["spacing"])
                    cursor_x += run_width(tok["text"], font, span["spacing"])
            cursor += data["total_h"] + gap
        if cursor - gap - origin[1] > h:
            warn(f"列表内容超出盒子高度：{cursor - gap - origin[1]:.0f} > {h}")

    elif kind == "metrics":
        items = layer.get("items", [])
        gap = int(layer.get("gap", 70) or 70)
        val_size = int(layer.get("value_size", 92) or 92)
        unit_size = int(layer.get("unit_size", max(20, val_size * 0.34)) or max(20, val_size * 0.34))
        lab_size = int(layer.get("label_size", max(20, val_size * 0.28)) or max(20, val_size * 0.28))
        color = parse_color(layer.get("color"), (26, 26, 26, 255))
        lab_color = parse_color(layer.get("label_color"), (90, 90, 90, 255))
        lab_step = int(lab_size * 1.55)
        widths: list[float] = []
        ascent_max = 0
        lab_desc = 0
        for item in items:
            value_txt = str(item.get("value", "")).strip()
            unit_txt = str(item.get("unit", "")).strip()
            label_txt = str(item.get("label", "")).strip()
            vf = load_font(pick_family(value_txt, layer.get("font", "cn")),
                           layer.get("weight", "bold"), val_size, ctx.font_overrides)
            uf = load_font(pick_family(unit_txt, layer.get("unit_font", "en")), "medium",
                           unit_size, ctx.font_overrides)
            lf = load_font(pick_family(label_txt, layer.get("label_font", "cn")), "regular",
                           lab_size, ctx.font_overrides)
            vw = run_width(value_txt, vf, 0)
            uw = run_width(unit_txt, uf, 0) if unit_txt else 0
            lw = run_width(label_txt, lf, 0)
            widths.append(max(vw + (uw + 8 if uw else 0), lw))
            va, _ = vf.getmetrics()
            _, ld = lf.getmetrics()
            ascent_max = max(ascent_max, va)
            lab_desc = max(lab_desc, ld)
        total = sum(widths) + gap * (len(items) - 1)
        align = layer.get("align", "left")
        start_x = origin[0] + (0 if align == "left" else (w - total) / 2 if align == "center" else w - total)
        block_h = ascent_max + (lab_step if any(str(i.get("label", "")).strip() for i in items) else 0) + lab_desc
        valign = layer.get("valign", "top")
        if valign == "middle":
            base_y = origin[1] + (h - block_h) / 2 + ascent_max
        elif valign == "bottom":
            base_y = origin[1] + h - block_h + ascent_max
        else:
            base_y = origin[1] + ascent_max
        if valign != "middle" and block_h > h:
            warn(f"参数块高度 {block_h:.0f} 超出盒子 {h}：{items[:1]}")
        cx = start_x
        for idx, item in enumerate(items):
            value = str(item.get("value", "")).strip()
            unit = str(item.get("unit", "")).strip()
            label = str(item.get("label", "")).strip()
            vf = load_font(pick_family(value, layer.get("font", "cn")),
                           layer.get("weight", "bold"), val_size, ctx.font_overrides)
            uf = load_font(pick_family(unit, layer.get("unit_font", "en")), "medium",
                           unit_size, ctx.font_overrides)
            lf = load_font(pick_family(label, layer.get("label_font", "cn")), "regular",
                           lab_size, ctx.font_overrides)
            value_color = parse_color(item.get("color"), color)
            draw_run(d, (cx, base_y), value, vf, value_color, 0)
            vw = run_width(value, vf, 0)
            uw = 0.0
            if unit:
                uw = run_width(unit, uf, 0)
                draw_run(d, (cx + vw + 8, base_y), unit, uf,
                         parse_color(item.get("unit_color"), color), 0)
            if item.get("strike"):
                ly = base_y - val_size * 0.30
                thickness = max(2, int(val_size * 0.055))
                d.rectangle([cx, ly, cx + vw + (uw + 8 if uw else 0), ly + thickness], fill=value_color)
            if label:
                draw_run(d, (cx, base_y + lab_step), label, lf,
                         parse_color(item.get("label_color"), lab_color), 0)
            cx += widths[idx] + gap
            if idx < len(items) - 1 and layer.get("divider"):
                div = layer["divider"]
                dx = cx - gap / 2
                d.rectangle([dx, base_y - val_size * 0.72, dx + int(div.get("width", 2) or 2),
                             base_y + lab_size * 0.9], fill=parse_color(div.get("color"), (0, 0, 0, 60)))

    elif kind == "callout":
        index = str(layer.get("index", ""))
        title = str(layer.get("title", ""))
        index_size = int(layer.get("index_size", 96) or 96)
        title_size = int(layer.get("title_size", 34) or 34)
        title_color = parse_color(layer.get("title_color", layer.get("color")), (255, 255, 255, 255))
        index_color = parse_color(layer.get("index_color"), (255, 255, 255, 120))
        align = layer.get("align", "left")
        t_engine = TextEngine({"text": title, "font": layer.get("font", "cn"),
                               "weight": layer.get("title_weight", "medium"), "size": title_size,
                               "color": title_color, "line_spacing": layer.get("line_spacing", 1.2)}, ctx)
        t_data = t_engine.fit(w, int(title_size * 3))
        cursor_y = origin[1]
        for i, line in enumerate(t_data["lines"]):
            baseline = cursor_y + i * t_data["step"] + t_data["ascent"]
            lw = t_data["widths"][i]
            sx = origin[0] + (0 if align == "left" else (w - lw) / 2 if align == "center" else w - lw)
            cx = sx
            for tok in line:
                span = t_engine.spans[tok["span"]]
                font = t_data["fonts"][tok["span"]]
                draw_run(d, (cx, baseline), tok["text"], font, span["color"], span["spacing"])
                cx += run_width(tok["text"], font, span["spacing"])
        index_top = cursor_y + t_data["total_h"] + int(layer.get("index_gap", 14))
        f_idx = load_font(layer.get("font", "cn"), layer.get("index_weight", "bold"), index_size, ctx.font_overrides)
        _, idesc = f_idx.getmetrics()
        idx_h = index_size
        idx_baseline = index_top + idx_h * 0.78
        idx_x = origin[0] + (0 if align == "left" else (w - run_width(index, f_idx, 0)) / 2
                             if align == "center" else w - run_width(index, f_idx, 0))
        draw_run(d, (idx_x, idx_baseline), index, f_idx, index_color, 0)
        idx_center_y = index_top + idx_h * 0.42

        if anchor:
            ax, ay = float(anchor[0]) - min_x, float(anchor[1]) - min_y
            box_right = origin[0] + w
            box_left = origin[0]
            if ax > box_right:
                start = (box_right + int(layer.get("line_gap", 6)), idx_center_y)
            elif ax < box_left:
                start = (box_left - int(layer.get("line_gap", 6)), idx_center_y)
            else:
                start = (origin[0] + w / 2, origin[1] + h)
            mode = layer.get("elbow", "horizontal")
            if mode == "straight":
                pts = [start, (ax, ay)]
            elif mode == "vertical":
                pts = [start, (start[0], ay), (ax, ay)]
            else:
                pts = [start, (ax, start[1]), (ax, ay)]
            line_cfg = layer.get("line") or {}
            draw_polyline(d, pts, parse_color(line_cfg.get("color"), (255, 255, 255, 200)),
                          int(line_cfg.get("width", 2) or 2), line_cfg.get("dash"))
            node = layer.get("node") or {}
            nstyle = node.get("style", "plus")
            r = float(node.get("size", 15) or 15)
            nfill = parse_color(node.get("color"), parse_color(line_cfg.get("color"), (255, 255, 255, 230)))
            if nstyle == "plus":
                draw_plus_node(d, (ax, ay), r, nfill,
                               parse_color(node.get("glyph_color"), (30, 30, 30, 255)))
            elif nstyle == "dot":
                d.ellipse([ax - r, ay - r, ax + r, ay + r], fill=nfill)

    tmp.alpha_composite(local, (min_x, min_y))


def render_circular_text(image: Image.Image, layer: dict, ctx: "RenderContext") -> None:
    draw = ImageDraw.Draw(image)
    x, y, w, h = box_of(layer)
    cx, cy = x + w / 2, y + h / 2
    radius = float(layer.get("radius", min(w, h) / 2 - 30))
    text = str(layer.get("text", "")).replace("\n", " ").strip()
    size = int(layer.get("size", 28) or 28)
    spacing = float(layer.get("letter_spacing", 0) or 0)
    font = load_font(layer.get("font", "cn"), layer.get("weight", "medium"), size, ctx.font_overrides)
    color = parse_color(layer.get("color"), (255, 255, 255, 255))
    start = float(layer.get("start_angle", 0) or 0)
    sign = -1.0 if str(layer.get("direction", "cw")).lower() in ("ccw", "counter", "counterclockwise") else 1.0
    orient = str(layer.get("orient", "outward"))
    disc = layer.get("disc") or {}

    if disc.get("fill") or disc.get("outline"):
        fill = parse_color(disc.get("fill"))
        outline = parse_color((disc.get("outline") or {}).get("color"))
        ow = int((disc.get("outline") or {}).get("width", 0) or 0)
        r = float(disc.get("radius", radius + size * 0.9))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill, outline=outline, width=ow)
    inner = layer.get("inner_image")
    if inner and inner.get("path"):
        img = load_image(inner["path"], {**inner, "optional": True})
        if img is not None:
            ib = inner.get("box")
            if ib:
                ix, iy, iw, ih = (int(round(float(v))) for v in ib)
            else:
                side = float(inner.get("size", radius * 0.9) or radius * 0.9)
                ix, iy, iw, ih = int(cx - side / 2), int(cy - side / 2), int(side), int(side)
            fitted = fit_image(img, (iw, ih), inner.get("fit", "contain"))
            ctx.canvas.alpha_composite(fitted, (ix, iy))

    advanced = 0.0
    for ch in text:
        adv = float(font.getlength(ch)) + spacing
        half = adv / 2.0
        angle_deg = start + sign * math.degrees((advanced + half) / max(radius, 1))
        rad = math.radians(angle_deg)
        px = cx + radius * math.sin(rad)
        py = cy - radius * math.cos(rad)
        glyph_pad = int(size * 1.2) + 6
        glyph = Image.new("RGBA", (glyph_pad * 2, glyph_pad * 2), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glyph)
        try:
            gd.text((glyph_pad, glyph_pad), ch, font=font, fill=color, anchor="mm")
        except (ValueError, TypeError):
            gd.text((glyph_pad, glyph_pad), ch, font=font, fill=color)
        rot = math.degrees(rad) if orient == "inward" else -math.degrees(rad)
        glyph = glyph.rotate(rot, resample=Image.BICUBIC, expand=False)
        image.alpha_composite(glyph, (int(px - glyph_pad), int(py - glyph_pad)))
        advanced += adv
    if math.degrees(advanced / max(radius, 1)) > 350:
        warn(f"环形文字超过一圈，可能重叠：{text[:16]}…")


def render_layer(canvas: Image.Image, layer: dict, ctx: "RenderContext", single: bool = False) -> None:
    ltype = layer.get("type", "rect")
    if ltype == "text":
        render_text_layer(canvas, layer, ctx)
        return
    img = render_shape_layer(layer, ctx)
    if single:
        canvas.alpha_composite(img)
    else:
        canvas.alpha_composite(img)


# --------------------------------------------------------------------------- 规格处理

SCALAR_KEYS = {
    "size", "min_size", "letter_spacing", "gap", "index_gap", "line_gap", "icon_gap",
    "radius", "corner_radius", "side_pad", "stroke_width", "blur", "node_size",
    "index_size", "title_size", "value_size", "unit_size", "label_size", "marker_width",
    "icon_size", "thickness", "outline_width", "width", "height",
}
BOX_KEYS = {"box", "points", "center", "anchor", "offset"}


def scale_spec(node, factor: float):
    if isinstance(node, dict):
        out = {}
        for key, value in node.items():
            if key in BOX_KEYS and isinstance(value, (list, tuple)):
                if value and isinstance(value[0], (list, tuple)):
                    out[key] = [[int(round(float(v) * factor)) for v in pt] for pt in value]
                else:
                    out[key] = [int(round(float(v) * factor)) for v in value]
            elif key in SCALAR_KEYS and isinstance(value, (int, float)) and not isinstance(value, bool):
                out[key] = int(round(value * factor)) if abs(value) >= 1 else value * factor
            elif isinstance(value, (dict, list)):
                out[key] = scale_spec(value, factor)
            else:
                out[key] = value
        return out
    if isinstance(node, list):
        return [scale_spec(v, factor) for v in node]
    return node


def linear_gradient_image(size, c1, c2, direction="vertical") -> Image.Image:
    w, h = size
    grad = Image.linear_gradient("L") if direction == "vertical" else Image.linear_gradient("L").rotate(-90)
    grad = grad.resize((w, h), Image.BILINEAR)
    base = Image.new("RGBA", (w, h), c1 + (255,))
    overlay = Image.new("RGBA", (w, h), c2 + (255,))
    overlay.putalpha(grad)
    base.alpha_composite(overlay)
    return base


class RenderContext:
    def __init__(self, spec: dict, scale: float):
        canvas = spec.get("canvas", {})
        self.width = int(round(float(canvas.get("width", 1200)) * scale))
        self.height = int(round(float(canvas.get("height", 1500)) * scale))
        self.canvas_size = (self.width, self.height)
        self.font_overrides = dict(spec.get("fonts", {}) or {})
        self.canvas: Image.Image | None = None

    def new_canvas(self) -> Image.Image:
        return Image.new("RGBA", self.canvas_size, (0, 0, 0, 0))


def build(spec: dict, scale: float = 1.0, keep_alpha: bool = False) -> Image.Image:
    if not math.isfinite(scale) or scale <= 0:
        raise ValueError("导出倍率必须为正数")
    working = scale_spec(spec, scale)
    canvas_spec = working.get("canvas", {})
    width = int(canvas_spec.get("width", 1200))
    height = int(canvas_spec.get("height", 1500))
    if width <= 0 or height <= 0:
        raise ValueError("画布宽高必须为正整数")
    ratio = spec.get("canvas", {}).get("ratio", "4:5")
    if ratio not in ("4:5", "16:9"):
        raise ValueError(f"尚未验证的画布比例：{ratio}；当前仅支持 4:5、16:9")
    rw, rh = (4, 5) if ratio == "4:5" else (16, 9)
    source = spec.get("canvas", {})
    if int(source.get("width", 1200)) * rh != int(source.get("height", 1500)) * rw:
        raise ValueError(f"spec 画布尺寸与 {ratio} 不符")
    if min(width, height) < 1000 or width * rh != height * rw:
        raise ValueError(f"导出尺寸 {width}×{height} 不符合 {ratio} 且最短边 >=1000px 的要求")
    def check_image_fit(layers):
        for layer in layers:
            if layer.get("type") == "image" and layer.get("fit") == "stretch":
                raise ValueError("图片图层不能使用 stretch；商品使用 contain 以保持原始比例")
            if layer.get("type") == "group":
                check_image_fit(layer.get("layers", []))

    check_image_fit(working.get("layers", []))

    ctx = RenderContext(working, 1.0)
    ctx.width, ctx.height = width, height
    ctx.canvas_size = (width, height)

    bg_color = parse_color(canvas_spec.get("background"), (255, 255, 255, 255))
    base = Image.new("RGBA", (width, height), bg_color)
    if canvas_spec.get("background_gradient"):
        g = canvas_spec["background_gradient"]
        base = linear_gradient_image((width, height),
                                     parse_color(g.get("from"), (245, 243, 240, 255))[:3],
                                     parse_color(g.get("to"), (230, 228, 224, 255))[:3],
                                     g.get("direction", "vertical"))

    bg_image = working.get("background_image")
    if bg_image:
        if bg_image.get("fit") == "stretch":
            raise ValueError("底图不能使用 stretch；请按画布重新取景或等比裁切")
        img = load_image(bg_image["path"], bg_image)
        if img is not None:
            fitted = fit_image(img, (width, height), bg_image.get("fit", "cover"))
            brightness = float(bg_image.get("brightness", 1) or 1)
            if brightness != 1:
                from PIL import ImageEnhance
                fitted = ImageEnhance.Brightness(fitted.convert("RGB")).enhance(brightness).convert("RGBA")
            if bg_image.get("blur"):
                fitted = fitted.filter(ImageFilter.GaussianBlur(float(bg_image["blur"])))
            base.alpha_composite(fitted)

    for layer in working.get("layers", []):
        render_layer(base, layer, ctx)

    return base if keep_alpha else base.convert("RGB")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="按 JSON 规格合成 4:5 或 16:9 电商主视觉 PNG")
    ap.add_argument("--spec", required=True, help="规格 JSON 路径")
    ap.add_argument("--out", required=True, help="输出 PNG 路径")
    ap.add_argument("--scale", type=float, default=None, help="整体缩放（默认取 spec.output.scale 或 1.0）")
    ap.add_argument("--keep-alpha", action="store_true", help="保留透明通道（默认输出 RGB PNG）")
    ap.add_argument("--json-report", default=None, help="把渲染摘要写到 JSON 文件")
    ap.add_argument("--debug", action="store_true", help="出错时打印完整堆栈")
    args = ap.parse_args(argv)

    spec_path = Path(args.spec)
    if not spec_path.exists():
        print(f"规格文件不存在：{spec_path}", file=sys.stderr)
        return 2
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    scale = args.scale if args.scale is not None else float((spec.get("output") or {}).get("scale", 1.0) or 1.0)

    try:
        img = build(spec, scale=scale, keep_alpha=args.keep_alpha)
    except (FileNotFoundError, ValueError, KeyError) as exc:
        if args.debug:
            raise
        print(f"[error] {type(exc).__name__}: {exc}", file=sys.stderr)
        print("        检查 spec 里的路径、box 与颜色写法；references/spec-schema.md 有字段说明。",
              file=sys.stderr)
        return 3
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "PNG", optimize=True)
    report = {
        "spec": str(spec_path),
        "out": str(out_path),
        "size": list(img.size),
        "ratio": round(img.width / img.height, 4),
        "scale": scale,
        "lang": spec.get("lang"),
        "project": spec.get("project"),
        "warnings": WARNINGS,
    }
    if args.json_report:
        Path(args.json_report).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"已生成 {out_path}  {img.width}×{img.height}  warnings={len(WARNINGS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
