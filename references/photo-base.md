# 底图获取

主视觉的画面质量由底图决定。按可用素材选择下列路径，优先级从高到低。

## 产品保真边界

- 真实商品的最终主视觉只能依据 H1/H2 已批准且可检查的商品参考图、抠图或原始商品像素。参考图必须能支持最终使用的视角、轮廓、颜色、材质和关键结构。
- 没有可靠商品依据时，只能输出规划、底图方案或明确标注的非保真布局概念；不得用“待确认”把它当作正式产品交付。
- AI 可以生成无商品、无文字的场景底图，再叠加批准的商品图；不得从文字描述重构真实商品、补造 Logo/结构/配件后宣称产品保真。
- 占位底图和候选成图均属于内部预览，H3 前留在 `work/render/`。

## 商品与支撑面的接触检查

商品是否“站住”不能由坐标重合或脚本通过单独判定。合成前后按下面的关系检查：

1. **实际接触线**：先确认商品可见底部与支撑面顶面在全尺寸图中都清楚可见；不能被裁切、前缘遮住，或在底部留下可见空隙。
2. **支撑面透视**：商品底部的水平/椭圆形态应与台面顶面的透视方向一致；商品不能落在台面后缘、前缘之外，或看起来穿入台面。改变画布裁切后要重新检查，而不是沿用原坐标结论。
3. **光线方向**：商品高光、台面明暗和接触阴影的主要方向必须相容。若背景主光从左前方来，商品底部阴影不能独立向左前方投射。
4. **接触阴影**：最深处应贴近真实接触线，向外逐渐变软、变淡，并服从商品实际脚印/底部轮廓；大而均匀、边缘生硬或脱离商品底部的椭圆阴影不算有效接触阴影。
5. **倒影条件**：只有水面、镜面或明确具有反射能力的材质才考虑倒影；哑光石材、木材、织物或普通台面优先使用自然接触阴影，不为填空而添加倒影。

### 接触关系的修正优先级

出现悬空、错位或支撑关系不可信时，按以下顺序返工：

1. 先检查底图的台面高度、透视、商品落点和商品比例，必要时重构场景或重新定位商品；
2. 再调整接触阴影的贴合位置、软硬和光线方向；
3. 最后才做局部融合（局部明度、色温或轻柔遮罩），并复查商品边缘和材质；
4. 不得通过拉伸、倾斜、重绘、补造结构或改变真实商品颜色来解决场景问题。商品参考像素和关键结构保持不变。

摄影商品、台座、背景和阴影应共享同一套材质与光线逻辑。若摄影商品与插画/扁平程序化道具出现明显媒介冲突，除非 H2 已明确批准混合媒介，否则应返工底图或配景，不应靠加重阴影掩盖冲突。

### 贴地接触阴影的生成（避免悬空感）

`shadow` 图层是“整张商品轮廓模糊后铺色”，对竖高 / 组合商品（如机器人 + 基站）会被商品本体几乎完全遮住，只剩一圈淡边，成图看起来像悬浮。落地类商品按下面做独立贴地阴影：

1. **量真实接触线**：读商品图 alpha，按阈值（如 alpha>40）找最底一行作为接触线；不要用 `getbbox()` 的底边——它常含一层极淡的裙边，会把接触线带偏到下面几行、让阴影错位。
2. **造阴影位图**：在画布坐标系（或与商品图同尺寸的坐标系）里，以接触线为中心画“软椭圆 / 压扁脚印”（最深处贴近接触线，向外柔化），或取商品 alpha 底部一行做横向模糊；输出 RGBA 位图，深色、低饱和。
3. **放对层级**：以 `image` 图层放在背景之后、商品 `image` 图层之前；阴影最深处对准接触线，并略向下 / 侧向偏移以配合来光方向。
4. **验收**：放大看商品底部与阴影之间无亮缝，明暗从接触线单调衰减到地板原色；必要时逐列取样对比成图与底图确认。

## 路径一：实拍图（首选）

- 有场景实拍：直接裁成 4:5 使用。裁切时先保证商品完整、水平线不歪，再考虑留白位置——文字区要落在相对干净的区域。
- 只有白底/平铺实拍：先抠图（保留边缘阴影），再用程序化画布合成：底色渐变 + 台面 + 投影 + 商品。合成时给文字区预留明暗差，不要事后靠重压暗补救。
- 多角度实拍：主视觉只用一张主角度图（正面或 3/4 侧），其余角度留给详情页。
- 分辨率：底图不低于画布尺寸（1200×1500），放大倍数控制在 1.5 倍以内，避免糊。

## 路径二：生图底图

用于没有实拍又需要氛围画面的情况。**生图只负责画面，不写任何文字。**

「编辑场景型」要的是**只有场景、没有商品**的底图，商品随后用实拍/抠图叠上去。提示词骨架、硬性约束与生成命令见 `assets/templates/imagegen-scene-prompt.md`。

提示词结构（缺一项都会导致返工）：

1. **场景主体**：按 H2 批准布局描述台座、台面和配景的材质、比例、摆放区域；不要描述要由后续合成的真实商品。
2. **场景**：环境、道具、台面材质（如浅色木台面、米白墙、灰色石台）。
3. **光线**：光源方向 + 柔硬（如"左上侧柔光，落地窗自然光"）。
4. **机位与构图**：竖版 4:5；机位、台座位置、场景重心和文字留白按 H2 批准布局设置，不固定居中或固定高度。
5. **色调与风格**：整体色温、饱和度、风格关键词（如"北欧极简""暖调高级灰"）。
6. **硬性禁止**：任何文字、字母、数字、水印、logo、品牌标识、价格标签、人像（除非需要）。
7. **输出**：4:5 竖版、高分辨率、写实静物场景底图；这是背景板，不是产品保真成图。

组装示例（按项替换后使用，不要照抄品牌名）：

```text
Realistic empty still-life background plate for an e-commerce composite. No product or product-like object.
Place an empty <H2-approved support surface> in <H2-approved scene area> with <场景描述>.
<光源方向与柔硬> lighting, soft natural scene shadows. Vertical 4:5 composition with <H2-approved camera angle>
and clean negative space only where the approved layout requires text overlay.
<色调与风格>. High resolution, coherent background plate, commercial editorial quality.
Absolutely no product, bottle, package, container, device, product silhouette, text, letters, numbers, watermark, logo, price tag, caption, or UI elements.
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
# 明亮「竹影水面」场景：以下数值只是待 H2 调整的起始示例，不是固定布局
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
| `--pedestal x0 y0 x1 y1` | 石台位置（画布比例）；按 H2 批准的支撑面与商品落点设置，不固定高度 |
| `--podium-kind` | `stone` 深灰石 / `travertine` 浅色水磨石 |
| `--podium2 x0 y0 x1 y1` | 第二座台（先绘制，形成前后层次） |
| `--water <y>` | 水面起始高度比例，配合 props 里的 `water`；会生成倒影与涟漪 |
| `--props` | `leafshadow`（竹叶投影）/`bamboo`（竹枝）/`water`（水面）/`linen`/`sprig`/`citrus`/`pebble`/`drape`/`pine`/`fruit`/`pod` |
| `--glow` | 柔光池 `cx cy rx ry strength`；`strength` 超过 0.8 开始过曝 |
| `--band` / `--product-x` | 配景带比例 / 商品中心横向位置；均为 H2 方案的可调参数，不是通用固定值 |
| `--branch-base` / `--branch-length` | 枝条根部与长度（画布比例） |
| `--band` | 底部配景带高度比例建议值；按 H2 布局调整 |
| `--product-x` | 商品主体中心横向位置建议值；按 H2 布局和真实支撑面调整 |
| `--bokeh` | 边缘虚化枝叶强度，浅调场景建议 `1.0` |

浅调偏侧场景的一套实测参数（对应 `editorial-scene` 模板）：

```bash
python scripts/make_scene_base.py --out work/base/base-cn.png --palette mint \
    --props drape,pine,fruit,pod --no-pedestal --band 0.21 --product-x 0.68 \
    --bokeh 1.0 --grain 0.18 --vignette 0.10 --glow 0.62 0.34 0.44 0.36 0.5 --seed 20261002
```

配景只做氛围：其范围、台座位置、商品落点和文字区必须按 H2 批准布局设置，不固定铺在下 1/3，也不固定使用某一高度线。商品本身仍需用已批准的实拍/抠图叠加，并配符合真实支撑面的 `shadow` 图层。中英双版共用同一张场景底（同 seed、同参数）。没有批准商品图时，底图只能服务于规划或非保真布局概念。

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

- 文字区是不是足够干净（深浅均匀）？复杂摄影背景上可优先使用局部明度调整、柔和 scrim 或渐变过渡，令文字区获得连续的明暗承托；避免无必要的硬边矩形贴片。若局部承托仍破坏场景或层级，应换底图或重新安排文字区。
- 主体有没有被裁掉关键结构？商品完整性优先于构图美观。
- 底图色调与品牌色冲不冲突？冲突时统一在底图上压一层品牌色低透明遮罩。
- 有没有第三方素材、他人水印、平台角标残留？
