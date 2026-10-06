#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""check_copy.py — 核对「内容母本」是否完整进入对应语言的成图规格。

甲方给了中英对照内容母本表时，"母本必须完整准确进入对应语言版本"是硬要求。
这个脚本把母本与 spec 逐项比对，漏项直接报出来。

母本 JSON 格式（每个信息项给 zh 和/或 en，缺的语言自动跳过）：
{
  "items": [
    { "field": "主标题", "zh": "轻装出行 温度随行", "en": "Travel Light. Keep It Warm." },
    { "field": "活动价", "zh": "秋日出行价 129 元", "en": "Autumn Travel Price CNY 129" }
  ],
  "waived": [
    { "field": "行动提示", "reason": "用户要求画面不出现行动语" }
  ]
}

`waived` 里的信息项视为"用户已确认不进画面"，跳过比对但会在结果里单列，不能拿它偷偷省略内容。

用法：
    python check_copy.py --master work/brief/content-master.json \
        --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

CJK = re.compile(r"[\u4e00-\u9fff]")


def normalize(text: str) -> str:
    """比对时忽略空白、分隔点与拉丁大小写：小字距大写标签属于排版处理，词句不变。"""
    return re.sub(r"[\s·]+", "", str(text)).lower()


def spec_text(path: Path) -> str:
    spec = json.loads(path.read_text(encoding="utf-8"))
    chunks: list[str] = []
    for layer in spec.get("layers", []):
        kind = layer.get("type")
        if kind == "text":
            if layer.get("spans"):
                chunks.append("".join(str(s.get("text", "")) for s in layer["spans"]))
            chunks.append(str(layer.get("text", "")))
        elif kind == "list":
            chunks += [str(i.get("text", i)) if isinstance(i, dict) else str(i)
                       for i in layer.get("items", [])]
        elif kind == "metrics":
            for item in layer.get("items", []):
                chunks.append(f"{item.get('value', '')}{item.get('unit', '')}{item.get('label', '')}")
        elif kind == "chip":
            chunks.append(str(layer.get("text", "")))
    return normalize(" ".join(chunks))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="核对内容母本完整性")
    ap.add_argument("--master", required=True, help="内容母本 JSON")
    ap.add_argument("--spec-cn", default=None, help="中文版 spec")
    ap.add_argument("--spec-en", default=None, help="英文版 spec")
    ap.add_argument("--allow-missing", action="append", default=[],
                    help="额外豁免的信息项 field（可重复），与母本里 waived 等价")
    args = ap.parse_args(argv)

    if not args.spec_cn and not args.spec_en:
        print("至少提供 --spec-cn 或 --spec-en 之一", file=sys.stderr)
        return 2

    master = json.loads(Path(args.master).read_text(encoding="utf-8"))
    items = master.get("items", [])
    if not items:
        print("母本 JSON 里没有 items", file=sys.stderr)
        return 2

    waived: dict[str, str] = {}
    for entry in master.get("waived", []):
        if isinstance(entry, dict):
            waived[str(entry.get("field", ""))] = str(entry.get("reason", ""))
        else:
            waived[str(entry)] = ""
    for field in args.allow_missing:
        waived.setdefault(str(field), "命令行豁免")

    blobs: dict[str, str] = {}
    if args.spec_cn:
        blobs["zh"] = spec_text(Path(args.spec_cn))
    if args.spec_en:
        blobs["en"] = spec_text(Path(args.spec_en))

    fails: list[str] = []
    checked = 0
    skipped: list[str] = []
    for item in items:
        if str(item.get("field")) in waived:
            skipped.append(str(item.get("field")))
            continue
        for lang, blob in blobs.items():
            want = item.get(lang)
            if not want:
                continue
            checked += 1
            if normalize(want) not in blob:
                fails.append(f"{item.get('field', '?')} [{lang}] 未进入成图：{want}")
    if "zh" in blobs and not CJK.search(blobs["zh"]):
        fails.append("中文版规格里没有检测到中文字符")
    if "en" in blobs and CJK.search(blobs["en"]):
        fails.append("英文版规格里出现中文字符")

    print(f"内容母本核对：{checked - len(fails)}/{checked} 项通过")
    for f in fails:
        print(f"[FAIL] {f}")
    for field in sorted(set(skipped)):
        reason = waived.get(field) or "未注明原因"
        print(f"[豁免] {field}：{reason}")
    if not fails:
        print("（比对已忽略空白、分隔点与拉丁大小写）")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
