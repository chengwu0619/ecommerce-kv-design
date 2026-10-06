# 生图配景底图提示词模板

用于「编辑场景型」：先用生图产出**只有场景、没有商品、没有文字**的底图，再把真实商品图叠加合成。
商品必须走实拍/抠图，不能用生图重画——否则外形、颜色、Logo 位置会被改造，违反品牌规范。

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
3. 人工检查：有没有伪文字、logo 残影、畸形道具；石台顶面是否干净、位置是否落在下 1/3；渐变有没有色带。
4. 把选中的图放到 `work/base/base-cn.png`（中英共用），保持 spec 里 `background_image.path` 指向它，然后重渲染双版。
5. 商品接触投影由 spec 的 `shadow` 图层补上；生图底图里**不要**要求画阴影，避免和合成影重叠。

## 提示词骨架

```text
Use case: product-mockup
Asset type: e-commerce key-visual background plate, vertical 4:5 portrait, <像素尺寸>
Primary request: an empty still-life set for a product photo composite. The frame must contain NO product, so a real product photo can be composited on top of the pedestal afterwards.
Scene/backdrop: <背景材质与渐变：从商品深色部件对应的颜色 → 商品浅色部件/台面对应的颜色>；背景在画面下 1/5 左右与台面交接，过渡自然、无硬地平线
Subject: <台座：形状、材质、位置；顶面必须空且完整可见>；<配景 1–3 件：亚麻/干果/枯枝等，放在画面下 1/3 与左右下角>
Style/medium: photorealistic still-life product photography, matte and premium editorial, calm and restrained
Composition/framing: vertical 4:5, camera slightly above eye level, pedestal centered on the vertical axis; the upper 60 percent of the frame is clean empty backdrop for typography
Lighting/mood: <光位>，柔和衰减，暖中性白平衡，无高光过曝
Color palette: <颜色词>
Materials/textures: <材质词>
Constraints: keep the upper 60 percent empty and uncluttered for text overlay; the pedestal top must stay unobstructed; realistic soft contact shadows; seamless gradient with no banding
Avoid: any product, bottle, cup, packaging, box; any text, letters, numbers, handwriting, watermark, logo, label; people, hands, animals; harsh reflections, busy patterns, tilted horizon, heavy vignette, oversaturated color, fake-looking plastic props
```

## 硬性约束（缺一项就要重生成）

- 画面里**不能有商品**：商品要另外合成，生图重画会改造外形与 Logo 位置。
- 画面里**不能有文字/数字/水印/logo**：这些一律由 `build_kv.py` 渲染。
- 上 60% 必须干净：主标题、卖点、价格都压在这块。
- 台座顶面必须空且完整可见，并落在画面 **80% 高度线**上（底部留出 1/5 做配景带）：商品要站在上面。
- 渐变不能有硬地平线或色带：文字压在渐变上，色带会立刻显脏。
- 浅底场景（mist 类）不要出现深色背景或强对比阴影，否则深色文字会读不清。
