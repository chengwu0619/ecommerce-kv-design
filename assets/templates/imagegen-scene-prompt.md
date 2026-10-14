# 生图配景底图提示词模板

用于「编辑场景型」：先用生图产出**只有场景、没有商品、没有文字**的底图，再把 H1/H2 已批准、可检查的真实商品图叠加合成。
商品必须走批准的实拍/抠图或原始商品像素，不能用生图重画；没有可靠商品依据时，这个文件只能支持规划或明确标注的非保真布局概念。

## 使用步骤

1. 按下面骨架填空，存成 `work/brief/imagegen-scene-prompt.txt`。
2. 生成（本 skill 附带的 CLI，需要 `OPENAI_API_KEY`）：

```bash
python "$CODEX_HOME/skills/.system/imagegen/scripts/image_gen.py" generate \
  --prompt-file work/brief/imagegen-scene-prompt.txt \
  --size 1280x1600 --quality high \
  --out work/base/scene-generated.png --force
```

   没有 API key 时可以先做参数校验（不联网、不调用模型）：

```bash
python "$CODEX_HOME/skills/.system/imagegen/scripts/image_gen.py" generate \
  --prompt-file work/brief/imagegen-scene-prompt.txt --size 1280x1600 --dry-run
```

   也可以把提示词贴到任何生图工具（即梦、Seedream、Midjourney 等），只要满足下面的硬性约束即可。
3. 人工检查：有没有伪文字、logo 残影、畸形道具；支撑面顶面是否干净、位置是否符合 H2 批准布局；渐变有没有色带。此检查只是底图技术/视觉预览，不是 H3 批准。
4. 把选中的图放到 `work/base/base-cn.png`（中英共用），保持 spec 里 `background_image.path` 指向它，然后重渲染双版。
5. 商品接触投影由 spec 的 `shadow` 图层补上；生图底图里**不要**要求画阴影，避免和合成影重叠。

## 提示词骨架

```text
Use case: product-mockup
Asset type: e-commerce key-visual background plate, vertical 4:5 portrait, <像素尺寸>
Primary request: an empty still-life set for a product photo composite. The frame must contain NO product, so an H1/H2-approved product photo can be composited on top of the pedestal afterwards.
Scene/backdrop: <H2 冻结的场景材质与渐变；只描述场景，不推断商品颜色>；背景与台面交接位置按 H2 布局设置，过渡自然、无硬地平线
Subject: <台座/支撑面：形状、材质、H2 批准位置；顶面必须空且完整可见>；<配景 1–3 件：按 H2 批准区域放置>
Style/medium: photorealistic empty still-life background plate for product photography, matte and premium editorial, calm and restrained
Composition/framing: vertical 4:5, <H2-approved camera angle and scene framing>; place the empty support surface at <H2-approved position and scale>; reserve clean negative space only in the approved text zones
Lighting/mood: <光位>，柔和衰减，暖中性白平衡，无高光过曝
Color palette: <H2 冻结的颜色词；这里只描述场景，不声称商品颜色>
Materials/textures: <材质词>
Constraints: keep the H2-approved text zones empty and uncluttered; keep the support surface unobstructed where the approved product composite will contact it; use realistic soft scene shadows; seamless gradient with no banding; do not impose a fixed center or 80% height line
Avoid: any product, bottle, cup, packaging, box; any text, letters, numbers, handwriting, watermark, logo, label; people, hands, animals; harsh reflections, busy patterns, tilted horizon, heavy vignette, oversaturated color, fake-looking plastic props
```

## 硬性约束（缺一项就要重生成）

- 画面里**不能有商品**：商品要另外合成，生图重画会改造外形与 Logo 位置。
- 画面里**不能有文字/数字/水印/logo**：这些一律由 `build_kv.py` 渲染。
- H2 批准的文字区必须干净：主标题、卖点和促销信息（如任务涉及）只放在批准的留白区。
- 台座/支撑面顶面必须空且完整可见到足以完成批准的商品合成；位置、大小、高度和是否位于画面中心均由 H2 布局与真实支撑关系决定，不固定 80% 高度线或底部 1/5 配景带。
- 渐变不能有硬地平线或色带：文字压在渐变上，色带会立刻显脏。
- 浅底场景（mist 类）不要出现深色背景或强对比阴影，否则深色文字会读不清。
