# ecommerce-kv-design

一个 Codex Skill：把品牌规范、商品资料、核心卖点、活动价格与时间，做成**可直接上架的电商商品营销主视觉**，固定交付**中文版 + 英文版两张竖版 4:5 PNG**。

A Codex Skill that turns brand rules, product facts, selling points and promotion terms into **publish-ready e-commerce key visuals** — one Chinese and one English 4:5 vertical PNG.

## 交付契约 / Deliverable contract

| 项 | 要求 |
| --- | --- |
| 成图 | 中文版 1 张 + 英文版 1 张 |
| 画布 | 竖版 4:5，默认 1200×1500，最短边 ≥ 1000px |
| 格式 | PNG |
| 双版关系 | 同一底图、同一骨架、同一事实；英文版是本地化重排，不是逐字翻译 |
| 附带 | 交付说明（受众、主张、证据来源、价格与时间来源、待确认项） |

## 安装 / Install

```bash
git clone https://github.com/<your-account>/ecommerce-kv-design.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/ecommerce-kv-design"
```

Windows (PowerShell):

```powershell
git clone https://github.com/<your-account>/ecommerce-kv-design.git "$env:USERPROFILE\.codex\skills\ecommerce-kv-design"
```

安装后：显式调用 `$ecommerce-kv-design`，或在聊到"商品主视觉 / 主图 / 中英双版商品营销图"时会自动匹配（必要时重启一次 Codex 刷新技能列表）。

## 目录 / Contents

```
SKILL.md                      技能主体：交付契约、七步流程、硬性规则、字体规范、脚本用法、模板表
agents/openai.yaml            UI 元数据
scripts/                      8 个脚本（见下表）
assets/templates/             5 套骨架的中英孪生对 + 生图提示词模板
assets/fonts/                 Playfair Display 可变字体 + OFL 授权文本
assets/showcase/              风格锚点（均为本仓库自生成的演示素材）
references/                   7 份按需加载的参考：版式系统、规格字段、底图与配景、文案、合规、验收
```

| 脚本 | 作用 |
| --- | --- |
| `build_kv.py` | 按 JSON 规格确定性渲染成图（文字/价格/日期全部走这里，不交给生图模型） |
| `verify_kv.py` | 交付校验：比例、尺寸、文案是否真的渲染、双版是否成对 |
| `check_copy.py` | 内容母本完整性核对，支持用户确认后的豁免登记 |
| `make_scene_base.py` | 程序化生成场景底图（渐变 + 台座/亚麻/竹枝/水面等配景） |
| `build_scene_from_photo.py` | 把竖向场景照片重构成 4:5，并把台面中心对到商品落点 |
| `make_reflection.py` | 由商品抠图生成水面/台面倒影 |
| `make_paper_base.py` | 纸感底纹（编辑纸感风） |
| `make_placeholder_base.py` | 实拍未到位时的 4:5 占位底图 |

## 依赖 / Requirements

- Python 3 + Pillow（仅此一个硬依赖）
- 字体：中文用系统思源宋体（Noto Serif SC）；拉丁用仓库自带的 `assets/fonts/PlayfairDisplay-VF.ttf`
- 可选：生图底图需要 `OPENAI_API_KEY`（走 imagegen 的 CLI 回退路径）

## 快速开始 / Quick start

```bash
# 1) 骨架
cp assets/templates/scene-photo-side.json     work/spec/kv-cn.json
cp assets/templates/scene-photo-side-en.json  work/spec/kv-en.json

# 2) 底图（三选一：照片重构 / 程序化 / 生图）
python scripts/build_scene_from_photo.py --src work/base/scene.jpg \
    --dst work/base/base-cn.png --podium-px 548 --podium-py 878 --px 0.674 --py 0.80

# 3) 商品与倒影
python scripts/make_reflection.py --src work/base/product-cutout.png \
    --out work/base/product-reflection.png

# 4) 渲染 + 双闸验收
python scripts/build_kv.py --spec work/spec/kv-cn.json --out outputs/KV-CN-4x5.png
python scripts/build_kv.py --spec work/spec/kv-en.json --out outputs/KV-EN-4x5.png
python scripts/verify_kv.py --cn outputs/KV-CN-4x5.png --en outputs/KV-EN-4x5.png \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json
python scripts/check_copy.py --master work/brief/content-master.json \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json
```

## 核心规则 / House rules

- **文字不进生图提示词**：标题、卖点、价格、日期一律由 `build_kv.py` 渲染，保证可改、可核、不出错字。
- 一个主标题只讲一个价值，卖点 ≤3 条，信息层级 ≤4 级。
- 商品主体高度 ≥ 画面 1/2；场景型默认商品居中偏右（约 0.674），底部留 1/5 作配景带，商品必须站在台座上。
- 信息小字不缩到读不清：正文 30–34px、标签 24–28px，字重 Bold/Medium（1200 宽基准）。
- 价格、划线价、活动时间、认证、销量、功效只写用户提供或可核验的事实。
- 内容母本（中英对照表）必须逐项进入对应语言版本；用户要求删减时在母本 `waived` 里登记，不静默省略。
- 第三方照片必须确认授权；带平台水印的素材不得作交付底图，也不得用涂抹/修复去水印。

## 许可与致谢 / License & credits

- 字体：**Playfair Display**（SIL Open Font License 1.1，授权文本见 `assets/fonts/OFL-PlayfairDisplay.txt`）；中文排版使用系统安装的思源宋体 / Noto Serif SC。
- `assets/showcase/` 中的演示图均由本仓库代码 + 自生成素材渲染，不含任何第三方版权图片。
- 本仓库暂未指定开源许可证（LICENSE 未添加）。如需允许他人自由使用/修改，请补充 MIT 或 Apache-2.0 等许可证文件。
