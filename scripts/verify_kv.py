#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""verify_kv.py — 交付前硬性校验：比例、尺寸、清晰度、文案是否真的渲染上去了、中英是否成对。

用法：
    python verify_kv.py --cn outputs/KV-CN-4x5.png --en outputs/KV-EN-4x5.png \
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


def check_file(path: Path, label: str, spec_path: Path | None, expect_lang: str | None) -> dict:
    info: dict = {"label": label, "path": str(path)}
    if not path.exists():
        fail(f"{label}：文件不存在 {path}")
        return info
    size_kb = path.stat().st_size / 1024
    info["size_kb"] = round(size_kb, 1)
    if size_kb < 30:
        fail(f"{label}：文件仅 {size_kb:.1f}KB，疑似空白或导出失败")
    img = Image.open(path)
    info["format"] = img.format
    info["mode"] = img.mode
    info["size"] = list(img.size)
    if img.format != "PNG":
        fail(f"{label}：格式为 {img.format}，要求 PNG")
    w, h = img.size
    if abs(w / h - 0.8) > 0.002:
        fail(f"{label}：比例 {w}×{h} = {w / h:.4f}，要求竖版 4:5（0.8）")
    else:
        ok(f"{label}：4:5 {w}×{h}")
    if min(w, h) < 1000:
        fail(f"{label}：最短边 {min(w, h)}px < 1000px，清晰度不足")
    gray = img.convert("L")
    stddev = ImageStat.Stat(gray).stddev[0]
    if stddev < 3:
        fail(f"{label}：画面几乎为纯色（stddev={stddev:.2f}），成图异常")
    info["stddev"] = round(stddev, 2)

    if spec_path:
        if not spec_path.exists():
            note(f"{label}：规格文件缺失，跳过文案与尺寸一致性检查（{spec_path}）")
        else:
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            canvas = spec.get("canvas", {})
            base_w = float(canvas.get("width", 1200))
            factor = w / base_w if base_w else 1.0
            declared = float((spec.get("output") or {}).get("scale", 1.0) or 1.0)
            if abs(factor - declared) / max(declared, 1e-6) > 0.01:
                note(f"{label}：成图按 {factor:.2f}× 规格导出（spec.output.scale={declared}）。"
                     f"命令行 --scale 属正常；否则确认 spec 与导出参数同源")
            else:
                ok(f"{label}：导出倍率 {factor:.2f}× 与规格一致")
            boxes = collect_text_boxes(spec)
            blank = []
            for box, text, opacity in boxes:
                x, y, bw, bh = (int(round(float(v) * factor)) for v in box)
                x0, y0 = max(0, x), max(0, y)
                x1, y1 = min(w, x + max(bw, 1)), min(h, y + max(bh, 1))
                if x1 <= x0 or y1 <= y0 or float(opacity or 1) < 0.05:
                    continue
                region = gray.crop((x0, y0, x1, y1))
                if ImageStat.Stat(region).stddev[0] < 2.0:
                    blank.append(text[:14])
            if blank:
                fail(f"{label}：以下文案区域没有任何笔迹，可能字体缺失或位置错误：{'、'.join(blank)}")
            else:
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
    return info


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="校验电商主视觉交付件")
    ap.add_argument("--cn", required=True, help="中文版 PNG")
    ap.add_argument("--en", required=True, help="英文版 PNG")
    ap.add_argument("--spec-cn", default=None)
    ap.add_argument("--spec-en", default=None)
    args = ap.parse_args(argv)

    cn, en = Path(args.cn), Path(args.en)
    check_file(cn, "中文版", Path(args.spec_cn) if args.spec_cn else None, "zh")
    check_file(en, "英文版", Path(args.spec_en) if args.spec_en else None, "en")

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
