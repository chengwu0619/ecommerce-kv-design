---
name: ecommerce-kv-design
description: 把有可靠商品参考依据的资料做成中英双版电商营销主视觉，默认竖版 4:5，H1 明确选择时支持横版 16:9；缺少商品依据时只做标注的规划或非保真概念。当用户要做促销 KV、活动首图或中英双版商品营销图时使用；商品主图还须服从目标平台的额外限制，不声称所有平台均可直接上架。只做视觉策划、文案规划、商品图精修或详情页长图时不使用。
metadata:
  short-description: 电商商品主视觉：中英双版 4:5 或 16:9 PNG
---

# 电商商品营销主视觉（KV）

把商品资料变成两张经人工批准后可交付的成图：**中文版 1 张 + 英文版 1 张**，默认竖版 4:5；H1 明确选择后可用横版 16:9，PNG。商品主图仍须单独核对目标平台的限制；不声称成图可在所有平台直接上架。

工作方式是"画面 + 信息"分层：商品与场景由实拍、抠图或生图底图提供；标题、卖点、参数、价格、活动时间、编号标注全部由 `scripts/build_kv.py` 按 JSON 规格确定性渲染。**不要把中文、价格、日期交给生图模型**——它写不对，而且没法改。

英文版：`SKILL.en.md` 是同一流程的英文文档，英文参考文档在 `references/en/`，生图提示词模板另有英文版 `assets/templates/imagegen-scene-prompt-en.md`。中英文档描述同一套脚本与模板；若两者出现不一致，以中文文档为准。

## 交付契约（硬性）

| 项 | 要求 |
| --- | --- |
| 中文版 | `outputs/KV-CN-4x5.png`；H1 批准 16:9 时为 `outputs/KV-CN-16x9.png` |
| 英文版 | `outputs/KV-EN-4x5.png`；H1 批准 16:9 时为 `outputs/KV-EN-16x9.png` |
| 画布 | 默认竖版 4:5、1200×1500；H1 可确认横版 16:9、建议 1920×1080；最短边 ≥1000px |
| 格式 | PNG（RGB） |
| 双版关系 | 同一底图、同一骨架、同一事实；英文版是本地化重排，不是逐字翻译 |
| 附带 | `outputs/交付说明.md`：受众、单一核心价值、卖点证据、促销价格与活动时间来源（如适用）、H1/H2/H3 成果版本 |

## 工作目录（固定约定）

```text
<项目根>/
├─ outputs/                     只放交付物
│  ├─ KV-CN-4x5.png
│  ├─ KV-EN-4x5.png
│  ├─ KV-CN-16x9.png            仅在批准 16:9 时；不覆盖 4x5
│  ├─ KV-EN-16x9.png
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
2. **写 brief，提交 H1 输入基线确认并停轮**：按 `references/workflow-and-brief.md` 记录 Reference/Facts Inventory、产品保真模式、Project Style Constraint Record 和 Canvas Specification（用途/平台、比例/像素、方向、PNG、平台限制、来源与确认消息）。默认 4:5；用户指定 16:9 不得改回竖版。平台规格冲突先报告并求确认。只在涉及促销时核验价格和时间；提交后停轮，未获批准不得进入步骤 3。
3. **定受众与单一主张**：一句话写清「给谁 / 什么场景 / 解决什么 / 为什么现在买」。主标题只承载 1 个核心价值，支撑卖点 ≤3 条；在 H1 已确认的品牌硬约束内形成可追溯的沟通层级。
4. **提出创意方向，提交 H2 选择/冻结并停轮**：仅在 H1 获批后执行。默认并列提交 A、B、C 三套实质不同的方案和比较；每套必须针对获批 Canvas Specification 分别设计商品重心/占比、真实支撑面、场景、文字区、视觉动线、字体、配色、信息层级、风险与可行性。横版不能缩放/裁切竖版骨架；A–H 仅是候选。回复末尾展示批准、修改/组合/重提、模式 A、模式 B 四类入口并停轮；用户指定少于三套或约束不足时按实际情况处理。
5. **定底图并制作**：仅在 H2 获批后执行。实拍/可检查的批准商品参考优先；没有可靠商品依据时只能做规划或明确标注的非保真布局概念。AI 可生成无商品、无文字的场景底图，不能从文字重构真实商品后宣称产品保真。中英双版共用同一张底图。
6. **写规格并渲染**：4:5 可改造旧模板；16:9 从横版规格起稿并按 H2 重排，不转换旧坐标。CN/EN spec 画布尺寸、底图、骨架相同，英文仅按文字长度调整文字框、字号和换行；渲染候选只留 `work/render/`，打开实际成图完成视觉 QA 后再提交 H3。
7. **技术 QA、提交 H3 实际成图审核并停轮**：跑 `scripts/verify_kv.py`，逐条过 `references/quality-gate.md`。若支撑接触、接触阴影或媒介关系不成立，必须返工，不能提交 H3。通过技术与视觉 QA 后提交实际 CN/EN 图、缩略图、版本和问题清单，结束当前回复。只有下一轮收到用户针对对应实际图像版本的明确 H3 批准，才可将成图与说明复制到 `outputs/`。

## 三个人工 Gate

Gate 是人工决策点，不等同于脚本状态、`READY`、`PASS` 或 `verify_kv.py` 退出码 0。批准证据只能来自用户在提交材料之后发送的明确确认消息，且必须指向对应版本和批准范围。模型写入 Brief、报告或交付说明的 `Approved` 不是批准证据；“请完成整个任务”等一般授权也不构成三个 Gate 的预先批准。每个 Gate 只记录：提交版本、用户消息证据、批准范围、决策人/日期（如适用）和成果版本。

### H1：输入基线确认（步骤 1–2 之后）

- AI 提交：素材与事实清单、可检查的商品参考图/品牌资产状态、产品保真模式、缺口/冲突、Project Style Constraint Record 与 Canvas Specification 初稿。
- 人确认：证据、官方字体/品牌色/禁用元素、必要商品事实、任务类型，以及画布用途/目标平台、比例、像素尺寸、方向、PNG 与平台额外限制和来源。价格/活动时间仅在任务涉及促销时核验。
- 结果只能是 `Approved`、`Changes requested` 或 `Returned`。没有真实用户批准消息时一律为 `Pending`，不得进入步骤 3。
- `Changes requested` 返回步骤 1 的资料/事实分析或步骤 2 的 brief；`Returned`（证据不可用、冲突或任务边界不清）返回步骤 1，必要时改为规划模式。

### H2：创意方向与项目风格冻结（步骤 3–4 之后、步骤 5 正式制作前）

- AI 提交：默认一次性提交 A/B/C 三套方案及简短横向比较；方案字段与版本规则见 `references/workflow-and-brief.md`。三套方案必须遵守 H1 的事实、品牌硬约束、授权、产品保真与平台限制，且不能只换颜色或名称。AI 可给出有理由的推荐，但不得自行选择、冻结或写成 `Approved`。
- 人确认：可直接批准某个明确 ID/版本，也可要求局部修改、组合不同方案、重新提案，或点名方案请求低保真预览。修改或组合必须形成新方案版本并再次确认；只有用户明确批准具体方案及版本，才把其批准范围写入 Project Style Constraint Record。全局硬约束和 H1 已确认的品牌硬约束不可被建议覆盖。
- 可选预览：默认只交文字与构图策略。用户明确指定方案与模式后才预览；模式 A 使用本地脚本/简单图形（无商品依据则用标注的占位框），模式 B 另须明确授权，生图只出无商品、无文字的背景。预览使用 H1 批准的比例，后期标注方案 ID/版本与 `CONCEPT / NOT FINAL`，只进 `work/render/`，不做完整双语生产或 H3。生图尺寸不符时只重构场景构图，不拉伸商品。
- 结果只能是 `Approved`、`Changes requested` 或 `Returned`。没有真实用户对明确方案及版本的批准消息时一律为 `Pending`；“请继续”“请完成任务”“先生成看看”和预览授权都不等于批准。H2 `Pending` 时，除用户明确请求的上述概念预览外，不得生成用于正式制作的背景或成图，不得进入步骤 5。
- `Changes requested` 返回步骤 3–4，产出新版本后重新提交 H2；`Returned`（方向依赖缺失证据或超出范围）返回步骤 1–2。图片生成预览若因权限、接口或服务问题失败，停止重复调用，如实报告并保留 H2 `Pending`，可建议模式 A；未经同意不得改用图库、其他生图服务或虚构结果。

#### H2 回复末尾标准交互格式（必须）

每次提交 H2 方案后，结尾必须明确告诉用户可以：

- 直接批准某个明确方案 ID/版本；
- 修改、组合或重新提出方案；
- 请求模式 A：用本地脚本、模板和简单图形制作低保真构图草图，不调用在线生图；
- 请求模式 B：在用户明确授权后，调用可用图片生成工具制作低保真场景氛围预览。

模式 A/B 均可只指定部分方案或全部方案；预览仍属于 H2 决策阶段，预览授权不等于正式批准，H2 保持 `Pending`，正式制作不得提前开始。默认不生成任何预览。结尾应附可直接复制的示例：

```text
批准 A-v1
修改 B-v1 的标题字体
结合 A-v1 的构图与 C-v1 的信息层级
使用模式 A 预览 A-v1、B-v1、C-v1
授权使用模式 B 预览 B-v1
```

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
- 只支持 H1 确认的精确 4:5 或 16:9，最短边 ≥1000px，PNG；具体宽高可由用户指定且须符合比例。`--scale` 双版一致且最终尺寸须等于 H1 规格；不拉伸商品或成图位图。
- 价格、划线价、到手价条件、活动时间只在任务实际涉及促销信息时核验；认证、销量、功效等只写用户提供或可核验的事实。缺证据时删除或停在规划阶段，不得用“待确认”支持未经批准的正式交付（见 `references/compliance-and-claims.md`）。
- 真实商品的正式主视觉必须依据已批准、可检查的商品参考图。没有可靠商品依据时，只输出规划或明确标注的非保真布局概念稿，不得宣称产品保真。
- 真实商品必须与 H2 批准的支撑面形成可信接触；明显悬空、接触阴影脱离或支撑关系不成立时判为需要返工，不得提交 H3。
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

# 技术校验（将 expected 宽高填写为 H1 批准的实际输出尺寸；不验证语义或视觉关系）
python scripts/verify_kv.py --cn work/render/KV-CN-4x5.png --en work/render/KV-EN-4x5.png \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json --expected-width 1200 --expected-height 1500

# H1 批准 1920x1080 后：改造横版模板、同尺寸同底图渲染，再按批准规格校验
python scripts/build_kv.py --spec work/spec/kv-cn.json --out work/render/KV-CN-16x9.png
python scripts/build_kv.py --spec work/spec/kv-en.json --out work/render/KV-EN-16x9.png
python scripts/verify_kv.py --cn work/render/KV-CN-16x9.png --en work/render/KV-EN-16x9.png \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json --expected-width 1920 --expected-height 1080

# 内容母本完整性核对（甲方给了中英母本表时必跑）
python scripts/check_copy.py --master work/brief/content-master.json \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json

# 编辑纸感风的纸纹底图
python scripts/make_paper_base.py --out work/base/base-cn.png --tone paper

# 编辑场景风的渐变 + 配景底图（与商品配色呼应）
python scripts/make_scene_base.py --out work/base/base-cn.png --palette sage --seed 20261001

# 场景照片等比裁切为 H1 画布；台面坐标由 H2 决定，裁切后复核真实落点
python scripts/build_scene_from_photo.py --src work/base/scene-photo-src.jpeg \
    --dst work/base/base-cn.png --podium-px 548 --podium-py 878 --px 0.674 --py 0.80

# 商品站在水面/亮面石材上时补倒影（scene-photo-side 模板依赖它）
python scripts/make_reflection.py --src work/base/product-cutout.png \
    --out work/base/product-reflection.png

# 实拍未到位时的默认 4:5 占位底图（横版传 --width 1920 --height 1080）
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
| `assets/templates/landscape-concept-cn.json`、`landscape-concept-en.json` | 16:9 横版概念起稿；必须按 H2 换商品占位、文字与支撑面 | H2 模式 A 或横版起稿，不能直接正式交付 |

`visual-system.md` 中的 F、H 是 `editorial-scene` 的参数变体，不新增模板文件。示例文案只为演示版式，交付前必须替换为真实且已确认的商品信息；英文替换不得添加未经证实的销量、效果或“畅销”宣称。
旧模板均为 1200×1500 竖版；横版不是坐标缩放版，必须依据 H2 独立构图。已有项目的方案和批准版本不因 Skill 规则更新而自动变化。

## 参考文件路由

| 需要处理 | 读 |
| --- | --- |
| 目录约定、brief 模板、缺口处理、交付说明模板 | `references/workflow-and-brief.md` |
| 选骨架、网格、字号阶梯、色彩、可读性、品牌规范 | `references/visual-system.md` |
| 写或改 spec JSON、图层字段、命令行参数 | `references/spec-schema.md` |
| 底图从哪来、生图提示词结构、占位底图 | `references/photo-base.md` |
| 中英文字数预算、术语对照、本地化写法 | `references/copy-cn-en.md` |
| 极限词、价格与活动表述、类目敏感、平台差异 | `references/compliance-and-claims.md` |
| 交付前逐条验收、常见返工原因 | `references/quality-gate.md` |
| 英文版文档（同等内容） | `SKILL.en.md`、`references/en/*.md`、`assets/templates/imagegen-scene-prompt-en.md` |

## 边界

- 不发布、不上架、不改动用户平台账号；只产出文件与说明。
- 不编造资料；缺关键信息时先问，不猜价格与时间。
- 只做这一张主视觉时不要顺带做详情页长图、Listing 文案、广告投放方案，除非用户要求。
- 平台规则有时效性；涉及当前审核口径时查官方最新来源，查不到就标"未核验"。
