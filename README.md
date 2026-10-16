# ecommerce-kv-design

一个 Codex Skill：把品牌规范、商品资料、卖点与活动价格，做成**可交付的电商商品营销主视觉**——固定产出**中文版 + 英文版**两张图，默认竖版 4:5 PNG（H1 明确选择时支持横版 16:9）。

A Codex Skill that turns brand rules, product facts, selling points and promotion terms into **deliverable e-commerce key visuals** — one Chinese and one English PNG, vertical 4:5 by default (landscape 16:9 when H1 explicitly chooses it).

![KV-CN](assets/showcase/kv-scene-cn-4x5.png)
![KV-EN](assets/showcase/kv-scene-en-4x5.png)

## 交付契约 / Deliverable contract

| 项 | 要求 |
| --- | --- |
| 双版 | 中文版 1 张 + 英文版 1 张 |
| 画布 | 默认竖版 4:5（1200×1500）；H1 批准后可用横版 16:9（建议 1920×1080）；最短边 ≥1000px |
| 格式 | PNG（RGB） |
| 双版关系 | 同一底图、同一骨架、同一事实；英文版是本地化重排，不是逐字翻译 |
| 附带 | 交付说明：受众、主张、证据来源、价格与活动时间来源（如适用）、H1/H2/H3 成果版本 |

| Item | Requirement |
| --- | --- |
| Editions | One Chinese + one English |
| Canvas | Vertical 4:5 (1200×1500) by default; landscape 16:9 (1920×1080 suggested) after H1 approval; shortest side ≥1000px |
| Format | PNG (RGB) |
| Relationship | Same base image, same skeleton, same facts; the English edition is a localised re-layout, not a word-for-word translation |
| Companion | Delivery notes: audience, proposition, evidence sources, price and date sources where applicable, H1/H2/H3 result versions |

## 安装 / Install

```bash
git clone https://github.com/chengwu0619/ecommerce-kv-design.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/ecommerce-kv-design"
```

Windows (PowerShell):

```powershell
git clone https://github.com/chengwu0619/ecommerce-kv-design.git "$env:USERPROFILE\.codex\skills\ecommerce-kv-design"
```

安装后即可用 `$ecommerce-kv-design`；涉及"商品主视觉 / KV / 中英双版商品营销图"的任务会自动匹配（必要时开一轮新会话刷新技能列表）。

## 目录 / Contents

```
SKILL.md                      中文主文档：交付契约、七步流程、三个人工 Gate、硬性规则、字体、脚本用法、模板清单
SKILL.en.md                   English companion: same contract, workflow, gates, rules, fonts, scripts, templates
agents/openai.yaml            UI 元数据 / UI metadata
scripts/                      8 个脚本：渲染、校验、母本核对、底图生成、倒影
assets/templates/             5 套骨架的中英孪生 JSON + 16:9 横版概念起稿 + 生图提示词模板（中英各一份）
assets/fonts/                 Playfair Display 可变字体 + OFL 授权文本
assets/showcase/              示例图（全部由本 skill 与程序化素材渲染）
references/                   7 份中文参考：工作流、版式系统、规格字段、底图、文案、合规、验收
references/en/                7 份英文参考（与中文一一对应）
```

## 脚本 / Scripts

| 脚本 | 作用 |
| --- | --- |
| `build_kv.py` | 按 JSON 规格确定性渲染成图；标题/参数/价格/日期全在文字层，不进生图模型 |
| `verify_kv.py` | 技术校验：文件与格式、尺寸比例、文字框是否真正落到图上、双版是否同规格同底图、是否显式拉伸 |
| `check_copy.py` | 内容母本逐项核对，支持用户确认后的豁免登记 |
| `make_scene_base.py` | 程序化生成场景底图：呼应色渐变 + 台座/织物/枝叶/水面配景 |
| `build_scene_from_photo.py` | 把场景照片等比重构到目标画布，对齐台面落点 |
| `make_reflection.py` | 给商品抠图补水台/台面倒影 |
| `make_paper_base.py` | 纸感底纹（编辑纸感风） |
| `make_placeholder_base.py` | 实拍未到位时的占位底图 |

## 依赖 / Requirements

- Python 3 + Pillow（唯一硬依赖）
- 字体：中文建议思源宋体（Noto Serif SC）；拉丁默认用仓库自带的 `assets/fonts/PlayfairDisplay-VF.ttf`
- 可选：生图底图需要 `OPENAI_API_KEY`（走 imagegen 的 CLI）或任意生图工具

## 快速开始 / Quick start

```bash
# 1) 起稿
cp assets/templates/scene-photo-side.json     work/spec/kv-cn.json
cp assets/templates/scene-photo-side-en.json  work/spec/kv-en.json

# 2) 底图（任选）：照片重构 / 程序化 / 生图
python scripts/build_scene_from_photo.py --src work/base/scene.jpg \
    --dst work/base/base-cn.png --podium-px 548 --podium-py 878 --px 0.674 --py 0.80

# 3) 商品与倒影
python scripts/make_reflection.py --src work/base/product-cutout.png \
    --out work/base/product-reflection.png

# 4) 渲染 + 技术校验
python scripts/build_kv.py --spec work/spec/kv-cn.json --out outputs/KV-CN-4x5.png
python scripts/build_kv.py --spec work/spec/kv-en.json --out outputs/KV-EN-4x5.png
python scripts/verify_kv.py --cn outputs/KV-CN-4x5.png --en outputs/KV-EN-4x5.png \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json \
    --expected-width 1200 --expected-height 1500
python scripts/check_copy.py --master work/brief/content-master.json \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json
```

## 文档地图 / Documentation map

| 主题 / Topic | 中文 | English |
| --- | --- | --- |
| 主文档 / Main document | `SKILL.md` | `SKILL.en.md` |
| 工作流、brief、目录约定 / Workflow, brief, directories | `references/workflow-and-brief.md` | `references/en/workflow-and-brief.md` |
| 版式系统与 A–H 骨架 / Layout system, skeletons A–H | `references/visual-system.md` | `references/en/visual-system.md` |
| 规格 JSON 字段 / Spec JSON fields | `references/spec-schema.md` | `references/en/spec-schema.md` |
| 底图与接触关系 / Base images, contact relationships | `references/photo-base.md` | `references/en/photo-base.md` |
| 中英文案与术语 / Bilingual copy and terminology | `references/copy-cn-en.md` | `references/en/copy-cn-en.md` |
| 合规与事实边界 / Compliance and factual boundaries | `references/compliance-and-claims.md` | `references/en/compliance-and-claims.md` |
| 验收清单 / Acceptance checklist | `references/quality-gate.md` | `references/en/quality-gate.md` |
| 生图提示词模板 / Image-gen prompt template | `assets/templates/imagegen-scene-prompt.md` | `assets/templates/imagegen-scene-prompt-en.md` |

中英文档描述同一套脚本与模板；若两者出现不一致，以中文文档为准。
Both editions describe the same scripts and templates; if they ever diverge, the Chinese documents are the source of truth.

## 三个人工 Gate / Three human gates

流程跨轮次执行，每轮最多推进到下一个尚未获得真实用户批准的 Gate 就停轮。The workflow spans turns: each turn stops at the next gate that has no genuine user approval.

- **H1 输入基线 / Input baseline**：素材与事实清单、产品保真模式、品牌硬约束、画布规格（用途/平台/比例/像素/方向/平台限制）。
- **H2 方向与风格冻结 / Direction and style freeze**：默认并列提交 A/B/C 三套实质不同方案与横向比较；可批准、修改、组合、重新提案，或请求模式 A/B 低保真预览。
- **H3 实际成图审核 / Real-render review**：提交实际全尺寸 CN/EN 图、缩略图、技术 QA、问题清单与事实来源，由人确认后才进入 `outputs/`。

脚本 `PASS`、`READY`、退出码 0，或模型自行写入的 `Approved`，都不构成人工批准。

## 硬性规则要点 / House rules

- **文字不进生图提示词**：标题、卖点、价格、日期一律由 `build_kv.py` 渲染，保证可改、可核、可复现。
- 一个主标题只讲一个核心价值；卖点 ≤3 条；信息层级 ≤4 级。
- 商品必须与真实支撑面形成可信接触；悬空、接触阴影脱离、未经批准的摄影/插画混合媒介都要返工。
- 信息小字不做"小字排版"：1200 宽基准下正文 30–34px、标签 24–28px，字重 Bold/Medium。
- 价格、划线价、活动时间、认证、销量、功效只在有已核验来源时出现；无依据就删除或转规划。
- 内容母本必须逐项进入对应语言版本；用户要求删除时在母本 `waived` 里登记，不静默省略。
- 素材授权：只用自有拍摄、明确授权或本 skill 生成的素材；带平台水印的图片不得作为交付底图，也不得涂抹去水印。

## 示例 / Showcase

`assets/showcase/` 内的示例图全部由本 skill 的程序化底图 + JSON 规格渲染，不含第三方图片素材。

| 文件 | 骨架 |
| --- | --- |
| `kv-cn-4x5.png` / `kv-en-4x5.png` | 实景氛围型 / scene-atmosphere |
| `kv-scene-cn-4x5.png` / `kv-scene-en-4x5.png` | 编辑场景型 / editorial-scene |
| `kv-editorial-cn-4x5.png` / `kv-editorial-en-4x5.png` | 编辑纸感型 / editorial-paper |
| `kv-scene-dark-cn-4x5.png` / `kv-scene-dark-en-4x5.png` | 深色呼应色场景变体 / dark scene variant |

## 许可与致谢 / License & credits

- 字体：**Playfair Display**（SIL Open Font License 1.1），授权文本见 `assets/fonts/OFL-PlayfairDisplay.txt`；中文排版使用系统安装的思源宋体 / Noto Serif SC。
- `assets/showcase/` 中的示例图由本 skill 的程序化底图 + JSON 规格渲染，不含任何第三方版权图片。
- 本仓库文档与脚本的授权尚未指定（默认保留所有权利）。如需允许他人使用/修改，请补充 MIT 或 Apache-2.0 等许可证文件。

- Fonts: **Playfair Display** (SIL Open Font License 1.1); licence text in `assets/fonts/OFL-PlayfairDisplay.txt`. Chinese typesetting uses a system-installed Noto Serif SC.
- `assets/showcase/` renders are produced by this skill's procedural bases plus JSON specs and contain no third-party copyrighted imagery.
- No licence is currently declared for the documentation and scripts (all rights reserved by default). To let others use or modify them, add an MIT or Apache-2.0 `LICENSE` file.
