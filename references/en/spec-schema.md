# Spec JSON reference

One spec = one render. `work/spec/kv-cn.json` and `work/spec/kv-en.json` should be identical apart from copy and the box widths / type sizes the copy genuinely requires.

Sample copy in this document is written in English; the schema itself is identical for both language editions. When the copy is Chinese, set the layer's `font` to `"cn"`.

## Top-level fields

```json
{
  "project": "kv-dawn-cn",
  "lang": "zh",
  "canvas": { "ratio": "4:5", "width": 1200, "height": 1500, "background": "#F4F2EF" },
  "fonts": { "cn-bold": "C:/path/to/font.otf", "en-black": ["segoeuib.ttf", "arialbd.ttf"] },
  "background_image": { "path": "work/base/base-cn.png", "fit": "cover", "optional": true },
  "layers": []
}
```

| Field | Description |
| --- | --- |
| `canvas.ratio/width/height` | With no ratio, `4:5` / 1200×1500 is assumed (older templates stay compatible); with an explicit `16:9`, 1920×1080 is recommended. Width and height must be an exact ratio with a shortest side ≥1000, and the render size must match the H1-approved value. Any other ratio is refused at render time |
| `canvas.background` | Flat colour; `canvas.background_gradient: {from, to, direction}` also works |
| `fonts` | Custom fonts: see "Specifying fonts" below |
| `background_image` | The product scene base; with `optional: true` a missing file only raises a warning (useful for laying out a draft first) |
| `layers` | Layer array, composited in order, later entries covering earlier ones |
| `output.scale` | Default export multiplier, overridable from the command line with `--scale` (1.25 / 1.5 / 2 are common) |

Colour syntax: `#RRGGBB`, `#RRGGBBAA`, `[r,g,b]`, `"none"`.

### Specifying fonts

Three forms:

```json
{
  "fonts": {
    "cn-bold": ["msyhbd.ttc", "simhei.ttf"],
    "serif-display": { "path": "C:/Windows/Fonts/NotoSerifSC-VF.ttf", "variation": "Black" },
    "serif-light": { "path": "NotoSerifSC-VF.ttf", "variation": "300" }
  }
}
```

1. `{"cn-bold": [...]} / "cn-bold": "path"`: overrides by `family-weight`, and after the override any layer with `"font": "cn"` picks it up automatically.
2. `{"serif-display": {"path": ..., "index": 0, "variation": "Black"}}`: a custom font key; layers call it directly with `"font": "serif-display"`. `variation` accepts a variable-font weight name (`ExtraLight`…`Black`), a number, or an axis dictionary.
3. A bare file name (no full path) also works: the script tries the path first, then searches the system font directories for that file name (`KV_FONT_DIR` can point at another directory).

When a font file is missing, or the weight name does not exist, the script warns and falls back to a system font — act on every `[warn]`, or you may get tofu boxes.

The skill ships `assets/fonts/PlayfairDisplay-VF.ttf` (a Didone-style Latin serif, SIL OFL). Two ways to use it: copy it into `work/base/fonts/` and reference it by relative path, or install it system-wide and use the bare file name. The licence text sits alongside it in `OFL-PlayfairDisplay.txt`.

## Common layer fields

- `box: [x, y, w, h]`: top-left corner plus width and height, in px, in the current spec's canvas coordinates. Every example below uses 1200×1500 vertical parameters and does not apply to landscape. For 16:9 see `assets/templates/landscape-concept-*.json` and re-lay it out independently for H2.
- `opacity: 0–1`: applies to the whole layer, including the anti-aliased edges of text.

## Layer types

### text

```json
{ "type": "text", "text": "No installation needed\nReady out of the box", "box": [60, 420, 330, 205],
  "font": "en", "weight": "bold", "size": 34, "min_size": 20, "max_lines": 2,
  "color": "#FFFFFF", "align": "left", "valign": "top",
  "line_spacing": 1.2, "letter_spacing": 2, "uppercase": false,
  "stroke": { "color": "#000000", "width": 0 },
  "shadow": { "color": "#00000066", "offset": [0, 3], "blur": 8 },
  "strike": false, "underline": false, "rotate": 0 }
```

- `\n` inside `text` is a hard line break; a space is an explicit space; CJK breaks per character and Latin breaks per word.
- `size` is the target type size; when it does not fit, the script steps down by 2% until `min_size` (default `size×0.45`), and warns past 40% compression.
- `font`: `cn` / `en`; `weight`: `light`/`regular`/`medium`/`bold`/`black`/`serif`.
- `letter_spacing` is tracking; once tracking grows you must pair it with `word_spacing` (1–3.5) to widen word gaps, otherwise Latin words run together.
- Mixed sizes use `spans` (baseline-aligned within one line):

```json
{ "type": "text", "box": [60, 1035, 1080, 195], "align": "center", "valign": "middle",
  "spans": [
    { "text": "Dawnlight", "size": 176, "weight": "black", "font": "en", "color": "#FFFFFF" },
    { "text": " series", "size": 68, "weight": "medium", "font": "en", "color": "#FFFFFF" }
  ] }
```

### rect / ellipse

```json
{ "type": "rect", "box": [0, 1330, 1200, 170], "fill": "#F2C230",
  "radius": 8, "outline": { "color": "#FFFFFF", "width": 2 } }
```

`radius: "pill"` gives fully rounded ends. A bottom action bar uses a `box` that reaches the canvas edge (`x=0, w=canvas.width`).

Fine circles, data-badge rings, and crosshair circles all use `ellipse` with only an `outline` (no `fill`); a stroke width of 1–2px with some transparency is enough.

### polygon

```json
{ "type": "polygon", "points": [[0, 1180], [1200, 1010], [1200, 1500], [0, 1500]], "fill": "#C8AE86" }
```

### line

```json
{ "type": "line", "points": [[100, 300], [400, 300], [400, 500]],
  "color": "#FFFFFF", "width": 2, "dash": [12, 10] }
```

### scrim (gradient mask that darkens the base so text stays legible)

```json
{ "type": "scrim", "box": [0, 980, 1200, 520], "direction": "bottom",
  "opacity_start": 0.36, "opacity_end": 0.92, "color": "#100E0C" }
```

| direction | edge matching opacity_start | edge matching opacity_end |
| --- | --- | --- |
| `bottom` | top edge | bottom edge |
| `top` | bottom edge | top edge |

When a light surface will not hold down, stack two layers — it looks more natural than pushing a single layer's values up.

### image

```json
{ "type": "image", "path": "work/base/product-cutout.png", "box": [500, 290, 680, 880],
  "fit": "contain", "corner_radius": 14, "brightness": 1.0, "optional": false }
```

`fit`: `cover` (crop to fill) / `contain` (fit whole, transparent padding). `stretch` is disabled for image layers; use `contain` for product cut-outs, and still compare completeness and original proportions by eye.

### shadow (contact shadow)

```json
{ "type": "shadow", "path": "work/base/product-cutout.png", "box": [223, 446, 755, 943],
  "fit": "contain", "blur": 30, "offset": [8, 22], "opacity": 0.30, "color": "#3A3226" }
```

Takes the product image's alpha channel, blurs it, and fills it with colour to give the weight of "a product sitting on paper / a surface". Place it before the product layer; keep `offset` low (positive y) and take the colour from an environmental dark tone rather than pure black.

### chip

```json
{ "type": "chip", "text": "Glass", "box": [70, 505, 200, 62], "size": 32,
  "fill": "#7E8B72", "color": "#FFFFFF", "auto_width": true,
  "radius": "pill", "side_pad": 24, "icon": "plus_circle", "icon_color": "#7E8B72", "icon_gap": 14 }
```

With `auto_width: true` the width follows the text, and `align` decides left/centre/right alignment inside the box. `icon`: `none`/`dot`/`plus`/`plus_circle`.

### list

```json
{ "type": "list", "box": [70, 1200, 540, 250], "size": 34, "gap": 26, "color": "#2E2D2A",
  "line_spacing": 1.2,
  "marker": { "type": "bar", "color": "#8A8069", "width": 6, "size": 18, "gap": 18 },
  "items": ["Sealed gasket keeps dry goods crisp", "Straight-walled body suits open kitchens"] }
```

`marker.type`: `bar` / `dot` / `plus` / `none`. Each item may also be an object `{ "text": "...", "label": "..." }`.

### metrics (specification blocks / price group)

```json
{ "type": "metrics", "box": [70, 620, 540, 190], "align": "left", "gap": 90,
  "value_size": 96, "unit_size": 34, "label_size": 28,
  "color": "#1F1F1D", "label_color": "#6B6A66",
  "divider": { "color": "#00000033", "width": 2 },
  "items": [
    { "value": "3", "unit": "pcs", "label": "In the set" },
    { "value": "$129", "label": "Regular price", "color": "#8A8175", "strike": true }
  ] }
```

- The number and unit share a baseline; `strike: true` draws a strikethrough (for a regular price).
- Give `box.h` enough room: `value ascender + label size ×1.55 + label descender`; otherwise it warns and spills outside the box.
- Units default to the Latin font (kg, ml, шт) and switch to the Chinese font automatically when they contain CJK characters.

### callout

```json
{ "type": "callout", "index": "01", "title": "Hidden light guide\nSoft, not glaring",
  "box": [810, 300, 330, 200], "anchor": [722, 430],
  "index_size": 96, "title_size": 34, "index_color": "#FFFFFF99", "title_color": "#FFFFFF",
  "index_gap": 14, "elbow": "horizontal",
  "line": { "color": "#FFFFFFCC", "width": 2 },
  "node": { "style": "plus", "size": 15, "color": "#EBC58A", "glyph_color": "#2B2B2B" } }
```

- `anchor` is the product detail being pointed at; `elbow`: `horizontal`/`vertical`/`straight`.
- `node.style`: `plus`/`dot`/`none`. The anchor must lie inside the canvas; beyond the edge it is clipped.

### circular_text (ring text / circular badge)

```json
{ "type": "circular_text", "text": "3-year warranty", "box": [890, 750, 240, 240],
  "radius": 92, "size": 30, "start_angle": -40, "direction": "cw", "orient": "outward",
  "color": "#5A4322", "letter_spacing": 0,
  "disc": { "fill": "#E7C48A", "radius": 108, "outline": { "color": "#FFFFFF", "width": 0 } },
  "inner_image": { "path": "work/base/badge-icon.png", "size": 90, "fit": "contain" } }
```

`start_angle` 0° = straight up, positive clockwise; `direction`: `cw`/`ccw`; `orient`: `outward`/`inward`.

### group

```json
{ "type": "group", "opacity": 0.9, "layers": [ { "type": "rect", "...": "..." } ] }
```

## Command line

```bash
# Render (both editions use the same spec canvas and multiplier; land in work/render first)
python scripts/build_kv.py --spec work/spec/kv-cn.json --out work/render/KV-CN-4x5.png
python scripts/build_kv.py --spec work/spec/kv-en.json --out work/render/KV-EN-4x5.png

# Delivery check
python scripts/verify_kv.py --cn work/render/KV-CN-4x5.png --en work/render/KV-EN-4x5.png \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json --expected-width 1200 --expected-height 1500

# Content-master completeness check
python scripts/check_copy.py --master work/brief/content-master.json \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json

# Paper-texture base (editorial paper)
python scripts/make_paper_base.py --out work/base/base-cn.png --tone paper --seed 20261001

# Gradient + props base (editorial scene)
python scripts/make_scene_base.py --out work/base/base-cn.png --palette sage --seed 20261001

# Placeholder base (to fix the layout while photography is pending)
python scripts/make_placeholder_base.py --out work/base/base-cn.png --tone greige
```

A non-zero script exit code means hard failures that must be fixed before delivery. Every `[warn]` must be handled or explained in the delivery notes.

When H1 approves landscape, the spec uses `"ratio":"16:9","width":1920,"height":1080`, the files become `KV-CN-16x9.png` / `KV-EN-16x9.png`, and the QA arguments become `--expected-width 1920 --expected-height 1080`. Custom widths and heights must be passed as the H1-approved values too; if the build overrides the multiplier with `--scale`, QA must pass the same `--scale` for both editions. A command-line value is not approval evidence. The landscape concept templates contain placeholder copy, so production must replace them with approved product assets and real facts and re-lay out the scene and support relationship; they may never be delivered as-is.
