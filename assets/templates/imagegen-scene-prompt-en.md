# Image-generation prompt template for scene background plates

For the editorial scene style: first generate a base with **scene only — no product, no text**, then composite the H1/H2-approved, inspectable real product image on top.
The product must come from approved photography, a cut-out, or original product pixels; it may never be redrawn by generation. Without a reliable product basis, this file can only support planning or an explicitly labelled non-fidelity layout concept.

## How to use

1. Fill in the skeleton below and save it as `work/brief/imagegen-scene-prompt.txt`.
2. Generate (the CLI shipped with this skill; `OPENAI_API_KEY` required):

```bash
python "$CODEX_HOME/skills/.system/imagegen/scripts/image_gen.py" generate \
  --prompt-file work/brief/imagegen-scene-prompt.txt \
  --size 1280x1600 --quality high \
  --out work/base/scene-generated.png --force
```

   Without an API key you can still validate the parameters (no network, no model call):

```bash
python "$CODEX_HOME/skills/.system/imagegen/scripts/image_gen.py" generate \
  --prompt-file work/brief/imagegen-scene-prompt.txt --size 1280x1600 --dry-run
```

   You may also paste the prompt into any image-generation tool (Jimeng, Seedream, Midjourney, and so on) as long as it satisfies the hard constraints below.
3. Human check: any pseudo-text, logo ghosts, or malformed props; whether the support surface's top face is clean and positioned per the H2-approved layout; any banding in the gradient. This check is a technical/visual preview of the base image only, not H3 approval.
4. Put the chosen image at `work/base/base-cn.png` (shared by CN and EN), keep the spec's `background_image.path` pointing at it, then re-render both editions.
5. The product contact shadow is added by the spec's `shadow` layer; do **not** ask the generated base image to draw a shadow, or it will double up with the composited one.

## Prompt skeleton

```text
Use case: product-mockup
Asset type: e-commerce key-visual background plate, <H1-approved 4:5 portrait or 16:9 landscape>, <H1-approved pixel dimensions>
Primary request: an empty still-life set for a product photo composite. The frame must contain NO product, so an H1/H2-approved product photo can be composited on top of the pedestal afterwards.
Scene/backdrop: <H2-frozen scene material and gradient; describe the scene only and do not infer product colour>; the background-to-surface transition follows the H2 layout, natural and with no hard horizon line
Subject: <podium/support surface: shape, material, H2-approved position; its top face must be empty and fully visible>; <1–3 props: placed in the H2-approved area>
Style/medium: photorealistic empty still-life background plate for product photography, matte and premium editorial, calm and restrained
Composition/framing: <H1-approved aspect ratio>, <H2-approved camera angle and scene framing>; place the empty support surface at <H2-approved position and scale>; reserve clean negative space only in the approved text zones; compose landscape independently rather than crop a portrait frame
Lighting/mood: <light position>, soft falloff, warm neutral white balance, no blown highlights
Color palette: <H2-frozen colour words; describe the scene only and make no claim about product colour>
Materials/textures: <material words>
Constraints: keep the H2-approved text zones empty and uncluttered; keep the support surface unobstructed where the approved product composite will contact it; use realistic soft scene shadows; seamless gradient with no banding; do not impose a fixed center or 80% height line
Avoid: any product, bottle, cup, packaging, box; any text, letters, numbers, handwriting, watermark, logo, label; people, hands, animals; harsh reflections, busy patterns, tilted horizon, heavy vignette, oversaturated color, fake-looking plastic props
```

## Hard constraints (regenerate if any is missing)

- **No product in the frame**: the product is composited separately, and redrawing it by generation would alter its form and logo placement.
- **No text/numbers/watermark/logo in the frame**: all of that is rendered by `build_kv.py`.
- The H2-approved text zones must stay clean: the headline, selling points, and promotion information (where the task involves one) sit only in the approved clear space.
- The podium/support surface's top face must be empty and visible enough to accept the approved product composite; its position, size, height, and whether it sits at the centre are all decided by the H2 layout and the real support relationship, with no fixed 80% height line or bottom-1/5 prop band.
- The gradient must have no hard horizon line or banding: text sits on the gradient, and banding instantly muddies it.
- Light-toned scenes (mist family) must not contain a dark background or strongly contrasting shadows, or dark text becomes illegible.
