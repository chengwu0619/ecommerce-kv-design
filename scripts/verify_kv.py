#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_kv.py — 技术校验：画布、格式、文案区域像素和中英成对情况。

用法：
    python verify_kv.py --cn work/render/KV-CN-4x5.png --en work/render/KV-EN-4x5.png \
        --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json

退出码 0 = 通过；1 = 有硬性不合格项。警告不阻塞交付，但要在交付说明里写清楚。
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageStat

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

FAILS: list[str] = []
WARNS: list[str] = []


def fail(msg: str) -> None:
    FAILS.append(msg)
    print(f"[FAIL] {msg}")


def note(msg: str) -> None:
    WARNS.append(msg)
    print(f"[warn] {msg}")


def ok(msg: str) -> None:
    print(f"[ ok ] {msg}")


TEXT_TYPES = ("text", "chip", "list", "metrics", "callout")


def layer_text(layer: dict) -> str:
    t = layer.get("type")
    if t == "text":
        if layer.get("spans"):
            return "".join(str(s.get("text", "")) for s in layer["spans"])
        return str(layer.get("text", ""))
    if t == "chip":
        return str(layer.get("text", ""))
    if t == "list":
        return " ".join(str(i.get("text", i)) if isinstance(i, dict) else str(i)
                        for i in layer.get("items", []))
    if t == "metrics":
        return " ".join(f"{i.get('value', '')}{i.get('unit', '')}{i.get('label', '')}"
                        for i in layer.get("items", []))
    if t == "callout":
        return f"{layer.get('title', '')}{layer.get('index', '')}"
    return ""


def collect_text_boxes(spec: dict) -> list[tuple]:
    found: list[tuple] = []

    def walk(layers):
        for layer in layers:
            if layer.get("type") in TEXT_TYPES and layer.get("box"):
                text = layer_text(layer)
                if text.strip():
                    found.append((layer["box"], text, layer.get("opacity", 1)))
            if layer.get("type") == "group":
                walk(layer.get("layers", []))

    walk(spec.get("layers", []))
    return found


def has_stretched_image(layers: list[dict]) -> bool:
    return any((layer.get("type") == "image" and layer.get("fit") == "stretch") or
               (layer.get("type") == "group" and has_stretched_image(layer.get("layers", [])))
               for layer in layers)


def check_file(path: Path, label: str, spec_path: Path, expect_lang: str,
               expected: tuple[int, int] | None, scale_override: float | None) -> dict:
    info: dict = {"label": label, "path": str(path)}
    if not path.exists():
        fail(f"{label}：文件不存在 {path}")
        return info
    size_kb = path.stat().st_size / 1024
    info["size_kb"] = round(size_kb, 1)
    if size_kb < 30:
        fail(f"{label}：文件仅 {size_kb:.1f}KB，疑似空白或导出失败")
    try:
        img = Image.open(path)
        img.load()
    except (OSError, ValueError) as exc:
        fail(f"{label}：无法读取图片：{exc}")
        return info
    info["format"] = img.format
    info["mode"] = img.mode
    info["size"] = list(img.size)
    if img.format != "PNG":
        fail(f"{label}：格式为 {img.format}，要求 PNG")
    w, h = img.size
    if min(w, h) < 1000:
        fail(f"{label}：最短边 {min(w, h)}px < 1000px，清晰度不足")
    gray = img.convert("L")
    stddev = ImageStat.Stat(gray).stddev[0]
    if stddev < 3:
        fail(f"{label}：画面几乎为纯色（stddev={stddev:.2f}），成图异常")
    info["stddev"] = round(stddev, 2)

    if not spec_path.exists():
        fail(f"{label}：规格文件缺失，无法校验尺寸和文案：{spec_path}")
    else:
        try:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            if has_stretched_image(spec.get("layers", [])):
                fail(f"{label}：图片图层使用 stretch，可能拉伸商品")
            if (spec.get("background_image") or {}).get("fit") == "stretch":
                fail(f"{label}：底图使用 stretch，可能拉伸商品或场景")
            canvas = spec.get("canvas", {})
            base_w, base_h = int(canvas.get("width", 1200)), int(canvas.get("height", 1500))
            ratio = canvas.get("ratio", "4:5")
            if ratio not in ("4:5", "16:9"):
                fail(f"{label}：spec 比例 {ratio} 未获当前技术支持")
            else:
                rw, rh = (4, 5) if ratio == "4:5" else (16, 9)
                suffix = "4x5" if ratio == "4:5" else "16x9"
                if f"-{suffix}" not in path.stem.lower():
                    fail(f"{label}：文件名 {path.name} 未对应 {ratio}（需包含 -{suffix}）")
                if base_w <= 0 or base_h <= 0 or base_w * rh != base_h * rw:
                    fail(f"{label}：spec 尺寸 {base_w}×{base_h} 与 {ratio} 不符")
                if w * rh != h * rw:
                    fail(f"{label}：成图比例 {w}×{h} 与 {ratio} 不符")
            factor = (scale_override if scale_override is not None else
                      float((spec.get("output") or {}).get("scale", 1.0) or 1.0))
            if factor <= 0:
                fail(f"{label}：导出倍率必须为正数")
            elif (w, h) != (round(base_w * factor), round(base_h * factor)):
                fail(f"{label}：成图 {w}×{h} 与 spec {base_w}×{base_h} × {factor:g} 不一致")
            else:
                ok(f"{label}：{ratio} {w}×{h} 与 spec 导出倍率 {factor:g} 一致")
            if expected is not None and (w, h) != expected:
                fail(f"{label}：成图 {w}×{h} 与 H1 输入规格 {expected[0]}×{expected[1]} 不符")
            boxes = collect_text_boxes(spec)
            blank = []
            outside = []
            for box, text, opacity in boxes:
                x, y, bw, bh = (round(float(v) * factor) for v in box)
                if bw <= 0 or bh <= 0 or x < 0 or y < 0 or x + bw > w or y + bh > h:
                    outside.append(text[:14])
                    continue
                x0, y0 = max(0, x), max(0, y)
                x1, y1 = min(w, x + max(bw, 1)), min(h, y + max(bh, 1))
                if x1 <= x0 or y1 <= y0 or float(opacity or 1) < 0.05:
                    continue
                region = gray.crop((x0, y0, x1, y1))
                if ImageStat.Stat(region).stddev[0] < 2.0:
                    blank.append(text[:14])
            if blank:
                fail(f"{label}：以下文案区域没有任何笔迹，可能字体缺失或位置错误：{'、'.join(blank)}")
            if outside:
                fail(f"{label}：以下文案框越界或尺寸无效：{'、'.join(outside)}")
            if not blank and not outside:
                ok(f"{label}：{len(boxes)} 处文案区域均已渲染")
            lang = spec.get("lang")
            if expect_lang and lang and lang != expect_lang:
                note(f"{label}：spec.lang = {lang}，与预期 {expect_lang} 不一致")
            if expect_lang == "zh":
                joined = " ".join(layer_text(l) for l in spec.get("layers", []) if l.get("type") in TEXT_TYPES)
                if any("\u4e00" <= c <= "\u9fff" for c in joined):
                    ok(f"{label}：中文文案已写入规格")
                else:
                    note(f"{label}：规格里没有检测到中文字符，确认中文版是否漏了中文信息")
        except (OSError, ValueError, TypeError, KeyError) as exc:
            fail(f"{label}：规格读取或字段无效：{exc}")
    return info


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="校验电商主视觉交付件")
    ap.add_argument("--cn", required=True, help="中文版 PNG")
    ap.add_argument("--en", required=True, help="英文版 PNG")
    ap.add_argument("--spec-cn", required=True)
    ap.add_argument("--spec-en", required=True)
    ap.add_argument("--expected-width", type=int, help="H1 批准的实际交付宽度；须与 --expected-height 同时提供")
    ap.add_argument("--expected-height", type=int, help="H1 批准的实际交付高度")
    ap.add_argument("--scale", type=float, help="渲染时命令行覆盖的双版统一倍率；不传则读取 spec.output.scale")
    args = ap.parse_args(argv)
    if (args.expected_width is None) != (args.expected_height is None):
        ap.error("--expected-width 与 --expected-height 必须同时提供")
    expected = ((args.expected_width, args.expected_height)
                if args.expected_width is not None else None)

    cn, en = Path(args.cn), Path(args.en)
    check_file(cn, "中文版", Path(args.spec_cn), "zh", expected, args.scale)
    check_file(en, "英文版", Path(args.spec_en), "en", expected, args.scale)
    if cn.exists() and en.exists():
        try:
            sc = json.loads(Path(args.spec_cn).read_text(encoding="utf-8"))
            se = json.loads(Path(args.spec_en).read_text(encoding="utf-8"))
            if sc.get("canvas") != se.get("canvas"):
                fail("中英版 spec.canvas 不一致")
            if sc.get("background_image") != se.get("background_image"):
                fail("中英版 background_image 不一致，须使用同一底图")
        except (OSError, ValueError) as exc:
            fail(f"中英规格无法交叉核对：{exc}")

    if cn.exists() and en.exists():
        a, b = Image.open(cn).convert("RGB"), Image.open(en).convert("RGB")
        if a.size != b.size:
            fail(f"中英双版尺寸不一致：{a.size} vs {b.size}（应共用同一骨架）")
        else:
            ok(f"中英双版尺寸一致 {a.size}")
        diff = ImageChops.difference(a, b)
        if diff.getbbox() is None:
            fail("中英双版画面完全相同，英文版未做本地化重排")
        else:
            changed = ImageStat.Stat(diff.convert("L")).mean[0]
            ok(f"中英双版为两张不同成图（差异均值 {changed:.2f}）")
    for name, path in (("中文版", cn.name), ("英文版", en.name)):
        if ("CN" if name == "中文版" else "EN") not in path.upper():
            note(f"{name}文件名建议包含 -CN- / -EN- 便于区分：{path}")

    print()
    print(f"结果：{'通过' if not FAILS else '未通过'}；硬性问题 {len(FAILS)} 项，提示 {len(WARNS)} 项")
    return 1 if FAILS else 0


if __name__ == "__main__":
    raise SystemExit(main())
