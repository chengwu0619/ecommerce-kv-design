# 底图获取

主视觉的画面质量由底图决定。按可用素材走三条路，优先级从高到低。

## 路径一：实拍图（首选）

- 有场景实拍：直接裁成 4:5 使用。裁切时先保证商品完整、水平线不歪，再考虑留白位置——文字区要落在相对干净的区域。
- 只有白底/平铺实拍：先抠图（保留边缘阴影），再用程序化画布合成：底色渐变 + 台面 + 投影 + 商品。合成时给文字区预留明暗差，不要事后靠重压暗补救。
- 多角度实拍：主视觉只用一张主角度图（正面或 3/4 侧），其余角度留给详情页。
- 分辨率：底图不低于画布尺寸（1200×1500），放大倍数控制在 1.5 倍以内，避免糊。

## 路径二：生图底图

用于没有实拍又需要氛围画面的情况。**生图只负责画面，不写任何文字。**

「编辑场景型」要的是**只有场景、没有商品**的底图，商品随后用实拍/抠图叠上去。提示词骨架、硬性约束与生成命令见 `assets/templates/imagegen-scene-prompt.md`。

提示词结构（缺一项都会导致返工）：

1. **主体**：商品形态、材质、颜色、比例、摆放角度。
2. **场景**：环境、道具、台面材质（如浅色木台面、米白墙、灰色石台）。
3. **光线**：光源方向 + 柔硬（如"左上侧柔光，落地窗自然光"）。
4. **机位与构图**：竖版 4:5、平视或略俯视、主体居中偏下、上下留出文字空间。
5. **色调与风格**：整体色温、饱和度、风格关键词（如"北欧极简""暖调高级灰"）。
6. **硬性禁止**：任何文字、字母、数字、水印、logo、品牌标识、价格标签、人像（除非需要）。
7. **输出**：4:5 竖版、高分辨率、写实产品摄影。

组装示例（按项替换后使用，不要照抄品牌名）：

```text
Realistic product photography of <商品主体描述>. Placed on <台面材质> in <场景描述>.
<光源方向与柔硬> lighting, soft natural shadows. Vertical 4:5 composition, <机位>,
product occupying the lower two thirds, clean negative space at top and bottom for text overlay.
<色调与风格>. High resolution, sharp focus on the product, commercial catalog quality.
Absolutely no text, no letters, no numbers, no watermark, no logo, no price tag, no caption, no UI elements.
```

生图后的检查：有没有出现伪文字、logo 残影、结构畸形、多余手指/影子、比例失真。出现就重生成，不要用修图掩盖。

中英双版必须用**同一张**底图。需要两版构图微调时，只改文字层坐标，不改画面。

## 路径三：占位底图（先定版式）

实拍还没到位、生图不方便时，用 `scripts/make_placeholder_base.py` 生成带产品占位框的 4:5 占位底图，先把版式和信息层级确认下来：

```bash
python scripts/make_placeholder_base.py --out work/base/base-cn.png --tone greige \
    --product-area center --product-ratio 0.55 --label "PRODUCT PHOTO AREA"
```

占位稿只能用于内部确认版式。交付说明里必须写明底图待替换，最终交付不允许把带 `PRODUCT PHOTO AREA` 字样的图交出去。

## 路径四：纸感底纹（编辑纸感型）

编辑纸感风（`editorial-paper`）需要一张纸纹底，而不是照片：

```bash
python scripts/make_paper_base.py --out work/base/base-cn.png --tone paper \
    --grain 0.45 --blotch 0.35 --fiber 0.35 --vignette 0.35
```

`--tone` 可选 `paper`（米黄）/`ivory`（近白）/`kraft`（牛皮）/`cool`/`ink`（深色）。纸纹要"看得见但读不出"：颗粒过强会与文字抢注意力，斑驳参数调大容易出现条带感，先渲染再判断。中英双版共用同一张纸纹底（同 seed）。

## 路径五：渐变 + 配景（编辑场景型）

商品颜色明确、需要场景氛围时，用 `scripts/make_scene_base.py` 生成呼应色渐变与配景：

```bash
# 明亮「竹影水面」场景：浅雾背景 + 竹叶投影 + 竹枝 + 两座水磨石圆台 + 水面倒影
python scripts/make_scene_base.py --out work/base/base-cn.png --palette mist --seed 20261005 \
    --props leafshadow,bamboo,water --podium-kind travertine \
    --pedestal 0.50 0.80 0.90 0.8667 --podium2 0.10 0.8267 0.34 0.8733 \
    --water 0.84 --band 0.20 --product-x 0.70 --grain 0.16 --vignette 0.12

# 深色呼应色场景（商品深色部件主导时）
python scripts/make_scene_base.py --out work/base/base-cn.png --palette sage --seed 20261001 \
    --pedestal 0.30 0.9133 0.70 0.9583 --props linen,sprig,citrus
```

| 参数 | 作用 |
| --- | --- |
| `--palette` | `mist`（浅雾，配深色字）/`mint`/`sage`/`olive`/`clay`/`ink`/`sand` |
| `--pedestal x0 y0 x1 y1` | 石台位置（画布比例）；`y0` 要等于商品底部高度，商品才"落在"台面上 |
| `--podium-kind` | `stone` 深灰石 / `travertine` 浅色水磨石 |
| `--podium2 x0 y0 x1 y1` | 第二座台（先绘制，形成前后层次） |
| `--water <y>` | 水面起始高度比例，配合 props 里的 `water`；会生成倒影与涟漪 |
| `--props` | `leafshadow`（竹叶投影）/`bamboo`（竹枝）/`water`（水面）/`linen`/`sprig`/`citrus`/`pebble`/`drape`/`pine`/`fruit`/`pod` |
| `--glow` | 柔光池 `cx cy rx ry strength`；`strength` 超过 0.8 开始过曝 |
| `--band` / `--product-x` | 底部配景带占高比例（0.2 = 五分之一）/ 商品中心横向位置（0.70 = 右 1/3） |
| `--branch-base` / `--branch-length` | 枝条根部与长度（画布比例） |
| `--band` | 底部配景带高度比例，默认 `0.21`（约图高 1/5） |
| `--product-x` | 商品主体中心横向位置，用于摆放配景（默认 `0.68`，偏右） |
| `--bokeh` | 边缘虚化枝叶强度，浅调场景建议 `1.0` |

浅调偏侧场景的一套实测参数（对应 `editorial-scene` 模板）：

```bash
python scripts/make_scene_base.py --out work/base/base-cn.png --palette mint \
    --props drape,pine,fruit,pod --no-pedestal --band 0.21 --product-x 0.68 \
    --bokeh 1.0 --grain 0.18 --vignette 0.10 --glow 0.62 0.34 0.44 0.36 0.5 --seed 20261002
```

配景只做氛围：默认铺在画面下 1/3 与左右下角，不进左右两列文字区。商品本身仍需用实拍/抠图叠加，并配 `shadow` 图层做接触投影。中英双版共用同一张场景底（同 seed、同参数）。

## 路径六：用户/素材库提供的场景照片（重新构图）

拿到一张竖向场景照（摄影棚静物、水台、台座那种），用 `scripts/build_scene_from_photo.py` 把它重构成 4:5 底图：

```bash
python scripts/build_scene_from_photo.py --src work/base/scene-photo-src.jpeg \
    --dst work/base/base-cn.png --podium-px 548 --podium-py 878 --px 0.674 --py 0.80
```

它做三件事：**按宽度铺满 → 平移让指定台面中心落到目标点（默认商品落点 0.674/0.80）→ 多余部分裁出画面**；平移留下的窄条用紧邻像素镜像补齐。`--podium-px/--podium-py` 是源图里"商品要站的台面"的像素坐标，看图目测即可（自动检测在浅色场景下容易把亮墙误判成台面）。

规矩：

- 只做缩放/平移/裁切/窄条补齐，**不做涂抹、修补或去水印**；不想要的元素（含水印）靠重新构图排除到画外。
- 第三方照片必须确认授权（自有拍摄 / 已购授权 / AI 生成）；带平台水印的素材默认不可用于交付，详见 `references/compliance-and-claims.md`。
- 商品若站在水面上，补一层倒影（商品图纵向镜像 + 渐隐 + 轻模糊）才不"浮"。

倒影用脚本生成，别手工做：

```bash
python scripts/make_reflection.py --src work/base/product-cutout.png \
    --out work/base/product-reflection.png --fade-top 0.42 --blur 2.2
```

生成的 `product-reflection.png` 当普通 image 图层用，box 的 y 起点取商品底部所在高度（例如 `[655, 1196, 400, 900]`，`opacity` 0.5–0.6）。

## 底图素材命名

```text
work/base/base-cn.png        主底图（中英共用）
work/base/product-cutout.png 商品抠图（白底信息型、大主体型用）
work/base/detail-macro.png   细节微距
work/base/badge-icon.png     徽章内图标（可选）
```

## 自检

- 文字区是不是足够干净（深浅均匀）？不干净就加 scrim 或换底图。
- 主体有没有被裁掉关键结构？商品完整性优先于构图美观。
- 底图色调与品牌色冲不冲突？冲突时统一在底图上压一层品牌色低透明遮罩。
- 有没有第三方素材、他人水印、平台角标残留？
