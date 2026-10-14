---
name: ecommerce-kv-design
description: 把有可靠商品参考依据的资料做成中文版 + 英文版两张电商营销主视觉（默认竖版 4:5，可按任务要求适配横板 16:9 等比例）；也可在缺少商品依据时做明确标注的规划或非保真布局概念。当用户要做促销 KV、活动首图或中英双版商品营销图时使用；商品主图还须服从目标平台的额外限制，不声称所有平台均可直接上架。只做视觉策划、文案规划、商品图精修或详情页长图时不使用。
metadata:
  short-description: 电商商品主视觉：中英双版 PNG 成图（默认 4:5，可适配 16:9）
---

# 电商商品营销主视觉（KV）

把商品资料变成两张经人工批准后可作为交付候选的成图：**中文版 1 张 + 英文版 1 张**，竖版 4:5，PNG。促销 KV 与商品主图都在当前范围内，但商品主图仍需单独核对目标平台的商品主图限制；不得把本 Skill 的 4:5 交付范围表述为所有平台均可直接上架。

工作方式是"画面 + 信息"分层：商品与场景由实拍、抠图或生图底图提供；标题、卖点、参数、价格、活动时间、编号标注全部由 `scripts/build_kv.py` 按 JSON 规格确定性渲染。**不要把中文、价格、日期交给生图模型**——它写不对，而且没法改。

## 交付契约（硬性）

| 项 | 要求 |
| --- | --- |
| 中文版 | `outputs/KV-CN-4x5.png` |
| 英文版 | `outputs/KV-EN-4x5.png` |
| 画布 | 默认竖版 4:5（1200×1500），最短边 ≥1000px；任务明确要求横板（如 16:9）时，spec 的 canvas 加 `allow_other_ratio: true`，并把校验的比例项改成对应比例 |
| 格式 | PNG（RGB） |
| 双版关系 | 同一底图、同一骨架、同一事实；英文版是本地化重排，不是逐字翻译 |
| 附带 | `outputs/交付说明.md`：受众、单一核心价值、卖点证据、促销价格与活动时间来源（如适用）、H1/H2/H3 成果版本 |

## 工作目录（固定约定）

```text
<项目根>/
├─ outputs/                     只放交付物
│  ├─ KV-CN-4x5.png
│  ├─ KV-EN-4x5.png
│  └─ 交付说明.md
└─ work/
   ├─ input/                    用户原始素材（实拍、logo、资质、活动截图）
   ├─ brief/kv-brief.md         结构化 brief
   ├─ spec/kv-cn.json           中文版规格（排版唯一真相源）
   ├─ spec/kv-en.json           英文版规格（同坐标，只换文案）
   ├─ base/                     底图 base-cn.png（中英共用）与可选细节图
   └─ render/                   迭代稿、对比图、report.json
```

改图 = 改 spec 后重渲染，不要直接编辑 PNG。中间产物一律留在 `work/`。

## 七步流程（跨轮次执行）

本流程不是一次回复内的流水线。每轮最多执行到下一个尚未取得真实用户批准的 Human Gate；提交该 Gate 的材料后，必须结束当前回复并等待用户的新消息。没有明确指向提交版本和批准范围的用户消息，不得推进，也不得由模型补写历史批准。

1. **建档收料与事实分析**：建目录，把用户素材放 `work/input/`；检查可用的商品参考图、品牌资产、事实与文案。图片素材先看清楚内容再引用，不靠文件名猜。
2. **写 brief，提交 H1 输入基线确认并停轮**：按 `references/workflow-and-brief.md` 的模板产出 `work/brief/kv-brief.md`，完成 Reference/Facts Inventory、产品保真模式和 Project Style Constraint Record 初稿。只在任务实际涉及促销时核验价格、活动时间及条件；未核验的促销事实不得进入正式交付。提交 H1 后结束当前回复；未收到用户明确批准，不得进入步骤 3 或正式创意设计。
3. **定受众与单一主张**：一句话写清「给谁 / 什么场景 / 解决什么 / 为什么现在买」。主标题只承载 1 个核心价值，支撑卖点 ≤3 条；在 H1 已确认的品牌硬约束内形成可追溯的沟通层级。
4. **选骨架与创意方向，提交 H2 冻结并停轮**：仅在 H1 获批后执行。从 `references/visual-system.md` 的骨架列表中选择一套并说明理由，提交视觉关键词、商品位置与占比、实际支撑面与接触关系、场景媒介/风格、主要文字区域、字体策略、配色、版式、底图与产品组合计划。H2 通过前不得生成背景或成图；提交 H2 后结束当前回复。
5. **定底图并制作**：仅在 H2 获批后执行。实拍/可检查的批准商品参考优先；没有可靠商品依据时只能做规划或明确标注的非保真布局概念。AI 可生成无商品、无文字的场景底图，不能从文字重构真实商品后宣称产品保真。中英双版共用同一张底图。
6. **写规格并渲染**：把最接近的 `assets/templates/*.json` 复制到 `work/spec/kv-cn.json` 改造，然后用 `scripts/build_kv.py` 渲染。候选图和技术报告先留在 `work/render/`；必须打开实际成图并完成视觉 QA，再决定修订 spec 或提交 H3。
7. **技术 QA、提交 H3 实际成图审核并停轮**：跑 `scripts/verify_kv.py`，逐条过 `references/quality-gate.md`。若支撑接触、接触阴影或媒介关系不成立，必须返工，不能提交 H3。通过技术与视觉 QA 后提交实际 CN/EN 图、缩略图、版本和问题清单，结束当前回复。只有下一轮收到用户针对对应实际图像版本的明确 H3 批准，才可将成图与说明复制到 `outputs/`。

## 三个人工 Gate

Gate 是人工决策点，不等同于脚本状态、`READY`、`PASS` 或 `verify_kv.py` 退出码 0。批准证据只能来自用户在提交材料之后发送的明确确认消息，且必须指向对应版本和批准范围。模型写入 Brief、报告或交付说明的 `Approved` 不是批准证据；“请完成整个任务”等一般授权也不构成三个 Gate 的预先批准。每个 Gate 只记录：提交版本、用户消息证据、批准范围、决策人/日期（如适用）和成果版本。

### H1：输入基线确认（步骤 1–2 之后）

- AI 提交：素材与事实清单、可检查的商品参考图/品牌资产状态、确认文案与促销相关性、产品保真模式、缺口/冲突，以及 Project Style Constraint Record 初稿。
- 人确认：哪些证据可用；官方字体、品牌色、禁用元素；商品名称/型号与必要事实；任务是促销 KV 还是受平台限制的商品主图。价格、活动时间只有在任务涉及促销时才要求核验。
- 结果只能是 `Approved`、`Changes requested` 或 `Returned`。没有真实用户批准消息时一律为 `Pending`，不得进入步骤 3。
- `Changes requested` 返回步骤 1 的资料/事实分析或步骤 2 的 brief；`Returned`（证据不可用、冲突或任务边界不清）返回步骤 1，必要时改为规划模式。

### H2：创意方向与项目风格冻结（步骤 3–4 之后、步骤 5 正式制作前）

- AI 提交：受众与主张、选定骨架、视觉方向、视觉关键词、字体策略、配色、版式、底图/商品组合计划、保真风险，以及更新后的 Project Style Constraint Record。
- 人确认：创意方向、字体策略、配色、版式和允许/禁用元素；确认记录中的 AI 建议是否冻结为本项目约束。全局硬约束和 H1 已确认的品牌硬约束不可被建议覆盖。
- 结果只能是 `Approved`、`Changes requested` 或 `Returned`。没有真实用户批准消息时一律为 `Pending`，不得生成背景、正式制作素材或进入步骤 5。
- `Changes requested` 返回步骤 3–4 重写主张、骨架或风格记录；`Returned`（方向依赖缺失证据或超出范围）返回步骤 1–2。

### H3：实际成图审核（步骤 7 的技术 QA 之后）

- AI 提交：实际渲染的 CN/EN 全尺寸图与缩略图、对应 spec/底图版本、技术 QA 报告、视觉问题清单、产品参考对照和促销事实来源（如任务涉及）。
- 人确认：实际商品是否与批准参考一致；构图、产品显著性、文字层级、可读性、真实场景/接触关系、品牌约束、双版事实一致性，以及是否批准进入 `outputs/`。
- 结果只能是 `Approved`、`Changes requested` 或 `Returned`。没有真实用户批准消息时一律为 `Pending`，不得把候选图当作正式交付，也不得移动到 `outputs/`。
- `Changes requested` 返回步骤 5（底图/合成）或步骤 6（spec/渲染），按问题归属修订后重新 QA/H3；`Returned`（方向或事实根本不成立）返回步骤 3–4，若证据失效则返回步骤 1–2。若商品与支撑面分离、接触阴影不成立，或摄影商品与插画场景冲突且 H2 未批准混合媒介，必须在步骤 5–6 返工，不得提交 H3。

人工批准必须针对实际图像和匹配版本；AI 技术检查通过绝不等同于人工批准。

## 硬性规则

- 文字不进生图提示词；一切文字、价格、日期由 spec 渲染。
- 一个主标题只讲一个价值；卖点 ≤3 条；信息层级 ≤4 级。
- 商品位置、主体高度、文字对侧关系、底部配景带和台座位置不设跨骨架的固定值；使用所选骨架的建议参数作为 H2 提案，最终服从 H2 批准的方案、商品参考图和真实支撑面。
- 左右两列文字不得被商品轮廓压住。
- 商品是否偏左/偏右、是否略高于视觉中线、文字列放在哪一侧，按 H2 批准的骨架和阅读顺序决定；不得把示例坐标当成通用硬限制。
- 底部配景带、台座/支撑面和商品接触位置按真实支撑关系与 H2 布局决定；“约 1/5”及其他高度数值只属于相应骨架的建议参数。
- 画布默认 4:5 精确；最短边 ≥1000px；导出 PNG；放大用 `--scale` 重渲染，不拉伸位图。任务要求其它比例（如 16:9）时，在 spec 的 `canvas` 里加 `allow_other_ratio: true`，并同步改写 `verify_kv.py` 的比例检查（或使用等价校验）——不得在未改校验的情况下把非 4:5 当成通过。
- 价格、划线价、到手价条件、活动时间只在任务实际涉及促销信息时核验；认证、销量、功效等只写用户提供或可核验的事实。缺证据时删除或停在规划阶段，不得用“待确认”支持未经批准的正式交付（见 `references/compliance-and-claims.md`）。
- 真实商品的正式主视觉必须依据已批准、可检查的商品参考图。没有可靠商品依据时，只输出规划或明确标注的非保真布局概念稿，不得宣称产品保真。
- 真实商品必须与 H2 批准的支撑面形成可信接触；明显悬空、接触阴影脱离或支撑关系不成立时判为需要返工，不得提交 H3。
- 商品必须真正落在支撑面/地面上，四周留出可见的支撑面：不得紧贴墙角、夹在墙角与配景之间、顶到壁龛或台座边缘等“夹缝”位置；可以适当遮挡配景，但主体四周要留呼吸距离。
- 接触阴影必须贴住商品底部的真实接触线：`shadow` 图层是“整张轮廓模糊后铺色”，对竖高/组合商品会被本体几乎完全遮住、只剩一圈淡边，读起来像悬空。落地类商品改用独立生成的贴地阴影图（取商品 alpha 底部真实接触行做压扁+模糊，或按底部轮廓画软椭圆），以 `image` 图层压在商品之下，最深处对准接触线并向下/侧向柔化；商品底部与阴影之间不得有亮缝。生成前先量商品 alpha 的真实接触行（用 alpha 阈值，不要用含淡裙边的包围盒底边）。
- 真实摄影商品与插画/程序化配景的媒介关系必须在 H2 明确批准；未批准的明显冲突先返工。
- H3 前的候选图、预览和报告只放 `work/render/`；只有下一轮收到用户针对匹配实际图像版本的明确 H3 批准后，才可进入 `outputs/`。
- 品牌 logo 不拉伸、不重绘、不改色；无 logo 时用字标占位并在交付说明标注。
- 未提供官方字体、Logo 或配色时，在 Project Style Constraint Record 中记录“未提供”；可以提出候选，但候选不是官方规范，字标占位也不得称为官方 Logo。
- 甲方提供内容母本（中英对照表）时，母本每一项都必须完整进入对应语言版本，用 `scripts/check_copy.py` 核对到 0 漏项。
- 英文版不得出现中文字符与全角标点；中文版不留英文占位。
- 中英双版的事实与数值必须完全一致。
- 深色/渐变背景上只用一种强调色；浅色字全走深色区，深色字全走浅色台面区，不跨区混排。
- 重要文字（主标题、价格、活动时间）优先放大；允许被商品挡住一部分，但被遮高度不超过字符高度的 1/4，且不能把一个词或一个字切断到读不出。放大后逐行核对左右两列文字的可见范围。
- 信息小字（产品名、卖点、参数、活动时间）不要用"小字排版"：1200 宽基准下正文 30–34px、标签 24–28px，字重 Bold/Medium；宁可精简文案，也不要把字号压到读不清。
- 行动语（立即选购 / Shop now）是可选图层：用户未要求、或明确要求画面不出现时，删掉文字层与下划线层，右下保持留白。
- 用户要求删减内容母本里的某一项时，不要默默省略：在母本 JSON 的 `waived` 里登记 field 与原因，`check_copy.py` 会把它单列为「豁免」而不是漏项。
- 脚本的 `[warn]` 都要处理，或在交付说明里写明原因。

## 字体

- 中文标题优先思源宋体（Noto Serif SC，可变字重 `variation` 取 `Black`/`Medium`/`Light`）。
- 拉丁标题用 `assets/fonts/PlayfairDisplay-VF.ttf`（Didone 风格高对比衬线，SIL OFL 可商用，授权文本同目录）。
- 例图上的中文大标题通常是商业授权宋体/明朝体，自由字体里最接近的是思源宋体 Heavy；用户指定字体时以用户字体为准，并把文件收进 `assets/fonts/` 保证可复现。
- spec 引用字体：复制到 `work/base/fonts/` 用相对路径，或直接写系统字体绝对路径；文件缺失时脚本告警并回退。

## 脚本用法

```bash
# 渲染（中英使用相同 --scale，同步放大坐标与字号）
python scripts/build_kv.py --spec work/spec/kv-cn.json --out work/render/KV-CN-4x5.png --scale 1.0
python scripts/build_kv.py --spec work/spec/kv-en.json --out work/render/KV-EN-4x5.png --scale 1.0

# 技术校验（候选渲染：比例、尺寸、文字像素落点、双版是否成对；不验证文字语义或视觉关系）
python scripts/verify_kv.py --cn work/render/KV-CN-4x5.png --en work/render/KV-EN-4x5.png \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json

# 内容母本完整性核对（甲方给了中英母本表时必跑）
python scripts/check_copy.py --master work/brief/content-master.json \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json

# 编辑纸感风的纸纹底图
python scripts/make_paper_base.py --out work/base/base-cn.png --tone paper

# 编辑场景风的渐变 + 配景底图（与商品配色呼应）
python scripts/make_scene_base.py --out work/base/base-cn.png --palette sage --seed 20261001

# 拿到场景照片时：重构成底图（默认 4:5；横板 16:9 用 --width 1920 --height 1080），
# 并把台面中心对到商品落点。方图转 16:9 必然纵向裁切，按“文字区留净墙、商品脚下留地板”选窗口。
python scripts/build_scene_from_photo.py --src work/base/scene-photo-src.jpeg \
    --dst work/base/base-cn.png --podium-px 548 --podium-py 878 --px 0.674 --py 0.80

# 落地商品的贴地阴影：不要用 shadow 图层整图模糊（会被本体遮住）。用 PIL 按商品 alpha 底部
# 真实接触行生成 soft 椭圆/压扁脚印位图，作为 image 图层压在商品之下（见 references/photo-base.md）。

# 商品站在水面/亮面石材上时补倒影（scene-photo-side 模板依赖它）
python scripts/make_reflection.py --src work/base/product-cutout.png \
    --out work/base/product-reflection.png

# 实拍未到位时的 4:5 占位底图
python scripts/make_placeholder_base.py --out work/base/base-cn.png --tone greige
```

脚本只依赖 Pillow；字体自动从系统字体目录解析，可用 `fonts` 字段或 `KV_FONT_DIR` 指定。

## 骨架模板（与 `references/visual-system.md` 的 A–H 列表对应）

| 文件 | 骨架 | 适用 |
| --- | --- | --- |
| `assets/templates/scene-atmosphere.json` | 实景氛围型（编号标注 + 底部超大标题） | 家居、家具、灯具、大件 |
| `assets/templates/scene-atmosphere-en.json` | 上者的英文孪生版（同坐标换文案） | 中英成对交付 |
| `assets/templates/info-white.json` | 浅底信息型（参数块 + 芯片 + 细节图） | 玻璃器皿、餐具、小家电、收纳 |
| `assets/templates/hero-subject.json` | 大主体型（斜切色块 + 信息卡 + 大参数） | 母婴、宠物、3C、清洁电器 |
| `assets/templates/editorial-paper.json` | 编辑纸感型（纸纹 + 超大衬线标题 + 铜色细线体系） | 高客单、重调性、要与详情页统一气质 |
| `assets/templates/editorial-paper-en.json` | 上者的英文孪生版（同坐标换文案） | 中英成对交付 |
| `assets/templates/editorial-scene.json` | 编辑场景型（浅调渐变 + 边缘虚化枝叶 + 底部配景带 1/5 + 商品偏侧略高） | 商品颜色明确、要场景感又要调性 |
| `assets/templates/editorial-scene-en.json` | 上者的英文孪生版（同坐标换文案） | 中英成对交付 |
| `assets/templates/scene-photo-side.json` | 摄影场景·侧置主体型（建议商品右 1/3、建议底部配景带、商品站台座） | 有棚拍静物/水台类底图，要成品级版面 |
| `assets/templates/scene-photo-side-en.json` | 上者的英文孪生版（同坐标换文案） | 中英成对交付 |

`visual-system.md` 中的 F、H 是 `editorial-scene` 的参数变体，不新增模板文件。示例文案只为演示版式，交付前必须替换为真实且已确认的商品信息；英文替换不得添加未经证实的销量、效果或“畅销”宣称。

## 参考文件路由

| 需要处理 | 读 |
| --- | --- |
| 目录约定、brief 模板、缺口处理、交付说明模板 | `references/workflow-and-brief.md` |
| 选骨架、网格、字号阶梯、色彩、可读性、品牌规范 | `references/visual-system.md` |
| 写或改 spec JSON、图层字段、命令行参数 | `references/spec-schema.md` |
| 底图从哪来、生图提示词结构、占位底图、落地接触阴影怎么造 | `references/photo-base.md` |
| 中英文字数预算、术语对照、本地化写法 | `references/copy-cn-en.md` |
| 极限词、价格与活动表述、类目敏感、平台差异 | `references/compliance-and-claims.md` |
| 交付前逐条验收、常见返工原因 | `references/quality-gate.md` |

## 边界

- 不发布、不上架、不改动用户平台账号；只产出文件与说明。
- 不编造资料；缺关键信息时先问，不猜价格与时间。
- 只做这一张主视觉时不要顺带做详情页长图、Listing 文案、广告投放方案，除非用户要求。
- 平台规则有时效性；涉及当前审核口径时查官方最新来源，查不到就标"未核验"。
