# 规格 JSON 说明

一份 spec = 一张成图。`work/spec/kv-cn.json` 与 `work/spec/kv-en.json` 除文案与必要的框宽/字号外应完全一致。

## 顶层字段

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

| 字段 | 说明 |
| --- | --- |
| `canvas.ratio/width/height` | 不填 ratio 默认 `4:5` / 1200×1500（兼容旧模板）；明确 `16:9` 时建议 1920×1080。宽高须为精确比例、最短边 ≥1000；成图尺寸须匹配 H1 批准值。其他比例会拒绝渲染 |
| `canvas.background` | 底色；也可用 `canvas.background_gradient: {from, to, direction}` |
| `fonts` | 自定义字体：见下方「字体指定」 |
| `background_image` | 商品场景底图；`optional: true` 时文件缺失只告警（用于先出布局稿） |
| `layers` | 图层数组，按顺序叠加，后写的压前面的 |
| `output.scale` | 默认导出倍率，可被命令行 `--scale` 覆盖（1.25 / 1.5 / 2 常用） |

颜色写法：`#RRGGBB`、`#RRGGBBAA`、`[r,g,b]`、`"none"`。

### 字体指定

三种写法：

```json
{
  "fonts": {
    "cn-bold": ["msyhbd.ttc", "simhei.ttf"],
    "serif-display": { "path": "C:/Windows/Fonts/NotoSerifSC-VF.ttf", "variation": "Black" },
    "serif-light": { "path": "NotoSerifSC-VF.ttf", "variation": "300" }
  }
}
```

1. `{"cn-bold": [...]} / "cn-bold": "path"`：按 `字体族-字重` 覆盖，覆盖后 `"font": "cn"` 的图层自动生效。
2. `{"serif-display": {"path": ..., "index": 0, "variation": "Black"}}`：自定义字体键，图层里写 `"font": "serif-display"` 直接调用；`variation` 支持可变字体字重名（`ExtraLight`…`Black`）、数值或轴字典。
3. 只写文件名（不写完整路径）也可以：脚本会先按路径找，找不到就按文件名在系统字体目录里搜（`KV_FONT_DIR` 可指定目录）。

字体文件缺失或字重名不存在时脚本会告警并回退系统字体——看到 `[warn]` 就要处理，否则可能出豆腐块。

skill 自带 `assets/fonts/PlayfairDisplay-VF.ttf`（拉丁 Didone 风格衬线，SIL OFL）。用法二选一：复制到 `work/base/fonts/` 后用相对路径引用，或安装到系统后只写文件名。授权文本同目录 `OFL-PlayfairDisplay.txt`。

## 通用图层字段

- `box: [x, y, w, h]`：左上角坐标 + 宽高，单位 px，按当前 spec 的画布坐标；以下示例均为 1200×1500 竖版参数，不适用横版。16:9 参见 `assets/templates/landscape-concept-*.json` 并按 H2 独立重排。
- `opacity: 0–1`：作用于整个图层（含文字抗锯齿边缘）。

## 图层类型

### text 文字

```json
{ "type": "text", "text": "免安装设计\n开箱即用", "box": [60, 420, 330, 205],
  "font": "cn", "weight": "bold", "size": 34, "min_size": 20, "max_lines": 2,
  "color": "#FFFFFF", "align": "left", "valign": "top",
  "line_spacing": 1.2, "letter_spacing": 2, "uppercase": false,
  "stroke": { "color": "#000000", "width": 0 },
  "shadow": { "color": "#00000066", "offset": [0, 3], "blur": 8 },
  "strike": false, "underline": false, "rotate": 0 }
```

- `text` 中的 `\n` 是硬换行；空格是显式空格；CJK 逐字断行、拉丁按词断行。
- `size` 是目标字号；放不下会自动按 2% 步进缩小到 `min_size`（默认 `size×0.45`），压缩超过 40% 会告警。
- `font`: `cn` / `en`；`weight`: `light`/`regular`/`medium`/`bold`/`black`/`serif`。
- `letter_spacing` 是字距；字距放大后必须配 `word_spacing`（1–3.5）拉宽词间距，否则拉丁词会连成一串。
- 混合字号用 `spans`（同一行内基线对齐）：

```json
{ "type": "text", "box": [60, 1035, 1080, 195], "align": "center", "valign": "middle",
  "spans": [
    { "text": "晨光", "size": 176, "weight": "black", "font": "cn", "color": "#FFFFFF" },
    { "text": " 系列", "size": 68, "weight": "medium", "font": "cn", "color": "#FFFFFF" }
  ] }
```

### rect / ellipse 色块

```json
{ "type": "rect", "box": [0, 1330, 1200, 170], "fill": "#F2C230",
  "radius": 8, "outline": { "color": "#FFFFFF", "width": 2 } }
```

`radius: "pill"` 得到全圆角。底部行动条用 `box` 顶到画布边缘（`x=0, w=canvas.width`）。

细线圆形、数据徽章环、坐标圆都用 `ellipse` + 只给 `outline`（不给 `fill`）；描边宽度 1–2px、颜色带透明度即可。

### polygon 斜切块

```json
{ "type": "polygon", "points": [[0, 1180], [1200, 1010], [1200, 1500], [0, 1500]], "fill": "#C8AE86" }
```

### line 直线 / 引导线

```json
{ "type": "line", "points": [[100, 300], [400, 300], [400, 500]],
  "color": "#FFFFFF", "width": 2, "dash": [12, 10] }
```

### scrim 渐变遮罩（压暗底图让文字可读）

```json
{ "type": "scrim", "box": [0, 980, 1200, 520], "direction": "bottom",
  "opacity_start": 0.36, "opacity_end": 0.92, "color": "#100E0C" }
```

| direction | opacity_start 对应边 | opacity_end 对应边 |
| --- | --- | --- |
| `bottom` | 上边缘 | 下边缘 |
| `top` | 下边缘 | 上边缘 |

浅色台面压不住时叠两层，比单层加大数值更自然。

### image 图片

```json
{ "type": "image", "path": "work/base/product-cutout.png", "box": [500, 290, 680, 880],
  "fit": "contain", "corner_radius": 14, "brightness": 1.0, "optional": false }
```

`fit`: `cover`（裁切填满）/ `contain`（完整放入，透明留白）。图片图层禁用 `stretch`；商品抠图用 `contain`，仍需人工比对完整性与原始比例。

### shadow 接触投影

```json
{ "type": "shadow", "path": "work/base/product-cutout.png", "box": [223, 446, 755, 943],
  "fit": "contain", "blur": 30, "offset": [8, 22], "opacity": 0.30, "color": "#3A3226" }
```

取商品图的 alpha 通道模糊后铺色，用来做"商品放在纸面/台面上"的重量感。放在商品图层前面；`offset` 建议偏下（y 为正值），颜色取环境暗色而不是纯黑。

### chip 芯片

```json
{ "type": "chip", "text": "玻璃", "box": [70, 505, 200, 62], "size": 32,
  "fill": "#7E8B72", "color": "#FFFFFF", "auto_width": true,
  "radius": "pill", "side_pad": 24, "icon": "plus_circle", "icon_color": "#7E8B72", "icon_gap": 14 }
```

`auto_width: true` 时宽度按文字自动计算，`align` 决定在 box 内左/中/右对齐。`icon`: `none`/`dot`/`plus`/`plus_circle`。

### list 卖点列表

```json
{ "type": "list", "box": [70, 1200, 540, 250], "size": 34, "gap": 26, "color": "#2E2D2A",
  "line_spacing": 1.2,
  "marker": { "type": "bar", "color": "#8A8069", "width": 6, "size": 18, "gap": 18 },
  "items": ["密封胶圈防潮，干货不回软", "直纹瓶身，开放式厨房也好看"] }
```

`marker.type`: `bar`（竖条）/ `dot`（圆点）/ `plus`（“+”圆点）/ `none`。每个 item 也可写成对象 `{ "text": "...", "label": "..." }`。

### metrics 参数块 / 价格组

```json
{ "type": "metrics", "box": [70, 620, 540, 190], "align": "left", "gap": 90,
  "value_size": 96, "unit_size": 34, "label_size": 28,
  "color": "#1F1F1D", "label_color": "#6B6A66",
  "divider": { "color": "#00000033", "width": 2 },
  "items": [
    { "value": "3", "unit": "件", "label": "组合数量" },
    { "value": "¥129", "label": "日常价", "color": "#8A8175", "strike": true }
  ] }
```

- 数字与单位共用基线；`strike: true` 画删除线（用于划线价）。
- `box.h` 要留够：`值字号升部 + 标签字号×1.55 + 标签降部`，不够会告警并压到框外。
- 单位默认走英文字体（kg、ml、шт），含中文字符时自动切中文字体。

### callout 编号标注

```json
{ "type": "callout", "index": "01", "title": "隐藏式导光\n柔和不刺眼",
  "box": [810, 300, 330, 200], "anchor": [722, 430],
  "index_size": 96, "title_size": 34, "index_color": "#FFFFFF99", "title_color": "#FFFFFF",
  "index_gap": 14, "elbow": "horizontal",
  "line": { "color": "#FFFFFFCC", "width": 2 },
  "node": { "style": "plus", "size": 15, "color": "#EBC58A", "glyph_color": "#2B2B2B" } }
```

- `anchor` 是要指的产品细节坐标；`elbow`: `horizontal`/`vertical`/`straight`。
- `node.style`: `plus`/`dot`/`none`。锚点必须在画布内，超出会被裁掉。

### circular_text 环形文字 / 圆徽章

```json
{ "type": "circular_text", "text": "整机质保三年", "box": [890, 750, 240, 240],
  "radius": 92, "size": 30, "start_angle": -40, "direction": "cw", "orient": "outward",
  "color": "#5A4322", "letter_spacing": 0,
  "disc": { "fill": "#E7C48A", "radius": 108, "outline": { "color": "#FFFFFF", "width": 0 } },
  "inner_image": { "path": "work/base/badge-icon.png", "size": 90, "fit": "contain" } }
```

`start_angle` 0° = 正上方，顺时针为正；`direction`: `cw`/`ccw`；`orient`: `outward`/`inward`。

### group 分组

```json
{ "type": "group", "opacity": 0.9, "layers": [ { "type": "rect", "...": "..." } ] }
```

## 命令行

```bash
# 渲染（两版使用相同 spec 画布及倍率；先留在 work/render）
python scripts/build_kv.py --spec work/spec/kv-cn.json --out work/render/KV-CN-4x5.png
python scripts/build_kv.py --spec work/spec/kv-en.json --out work/render/KV-EN-4x5.png

# 交付校验
python scripts/verify_kv.py --cn work/render/KV-CN-4x5.png --en work/render/KV-EN-4x5.png \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json --expected-width 1200 --expected-height 1500

# 内容母本完整性核对
python scripts/check_copy.py --master work/brief/content-master.json \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json

# 纸感底纹（编辑纸感型）
python scripts/make_paper_base.py --out work/base/base-cn.png --tone paper --seed 20261001

# 渐变 + 配景（编辑场景型）
python scripts/make_scene_base.py --out work/base/base-cn.png --palette sage --seed 20261001

# 占位底图（等实拍时先定版式）
python scripts/make_placeholder_base.py --out work/base/base-cn.png --tone greige
```

脚本退出码非 0 = 有硬性不合格项，必须修完再交付。所有 `[warn]` 都要处理，或在交付说明里写明原因。
H1 批准横版时使用 spec `"ratio":"16:9","width":1920,"height":1080`，文件改为 `KV-CN-16x9.png` / `KV-EN-16x9.png`，QA 参数改为 `--expected-width 1920 --expected-height 1080`。自定义宽高也要按 H1 批准值传入；若构建时通过 `--scale` 覆盖倍率，QA 两版须传相同 `--scale`。命令行值不是批准证据。横版概念模板含占位文案，正式制作须换成获批商品素材与实际事实、重排场景和支撑关系；不得直接交付。
