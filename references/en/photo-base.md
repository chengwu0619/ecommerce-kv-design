# Sourcing the base image

The visual quality of the hero image is decided by the base image. Choose among the paths below according to the material available, in descending order of preference.

## Product-fidelity boundary

- The final hero image for a real product may only rest on a product reference image, cut-out, or original product pixels that were approved at H1/H2 and can be inspected. The reference must support the final viewing angle, outline, colour, material, and key construction.
- Without a reliable product basis you may output planning, a base-image proposal, or an explicitly labelled non-fidelity layout concept only; never present it as a formal product delivery by marking it "to be confirmed".
- AI may generate a scene base with no product and no text, onto which the approved product image is then composited; it may not reconstruct a real product from a text description, invent a logo/structure/accessory, and then claim product fidelity.
- Placeholder bases and candidate renders are internal previews and stay in `work/render/` until H3.

## Checking the contact between product and support surface

Whether a product "stands" can never be decided by coinciding coordinates or by a passing script. Before and after compositing, check the following relationships:

1. **Actual contact line**: first confirm that the visible product base and the top surface of the support surface are both clearly visible in the full-size image; neither may be cropped, hidden by the front edge, or leave a visible gap at the bottom.
2. **Support-surface perspective**: the horizontal/elliptical form of the product base must agree with the perspective of the podium top; the product may not land on the back edge, beyond the front edge, or appear to sink into the surface. After changing the canvas crop, check again rather than reusing a conclusion from the old coordinates.
3. **Light direction**: the product highlights, the surface's light and shade, and the contact shadow must share a compatible main direction. If the background key light comes from the front left, the product's base shadow may not be cast independently to the front left.
4. **Contact shadow**: its darkest area should hug the actual contact line, softening and lightening outward while following the product's real footprint/base outline; a large, uniform ellipse with hard edges that floats away from the product base is not a valid contact shadow.
5. **When a reflection applies**: consider a reflection only on water, a mirror, or a material that genuinely reflects. Matte stone, wood, fabric, or an ordinary surface should use a natural contact shadow rather than a reflection added just to fill space.

### Rework priority for contact relationships

When the product floats, is misaligned, or the support relationship is not credible, rework in this order:

1. First check the base image's surface height, perspective, product resting point, and product scale, reconstructing the scene or repositioning the product if needed;
2. Then adjust the contact shadow's fit, softness, and light direction;
3. Only then do local blending (local brightness, colour temperature, or a gentle mask) and re-inspect the product edges and material;
4. Never solve a scene problem by stretching, tilting, redrawing, inventing structure, or changing the real product colour. The reference pixels and key construction stay untouched.

A photographic product, podium, background, and shadow should share one material and lighting logic. If a photographic product clashes obviously in medium with illustration or flat procedural props, rework the base image or props unless H2 has explicitly approved mixed media; do not hide the clash behind heavier shadows.

## Path one: real photography (preferred)

- With scene photography: reframe to the H1-approved canvas ratio. When cropping, keep the product complete and the horizon level first, then consider the H2-approved text clear space; when there is not enough material to reconstruct a landscape honestly, change or reshoot the asset rather than cropping the product.
- With only white-background or flat-lay photography: cut out first (keep the edge shadow), then composite on a procedural canvas: base gradient + surface + cast shadow + product. Build tonal contrast into the text area while compositing instead of rescuing it afterwards with heavy darkening.
- With multiple angles: use only one primary angle (front or 3/4) in the hero image and save the rest for the detail page.
- Resolution: the base image must be at least the H1-approved canvas size (1200×1500 by default, 1920×1080 suggested for landscape), with upscaling kept under 1.5× to avoid mushiness.

## Path two: generated base image

For when there is no photography but an atmospheric scene is needed. **Generation handles the picture only and writes no text at all.**

The editorial scene style needs a base with **scene only, no product**, onto which the product is later composited from photography or a cut-out. The prompt skeleton, hard constraints, and generation commands live in `assets/templates/imagegen-scene-prompt-en.md`.

Prompt structure (missing any one item causes a rework):

1. **Scene subject**: describe the material, proportion, and placement of podiums, surfaces, and props according to the H2-approved layout; do not describe the real product that will be composited later.
2. **Scene**: environment, props, surface material (for example a pale wood surface, an off-white wall, a grey stone plinth).
3. **Light**: light direction + softness (for example "soft light from the upper left, natural window light").
4. **Camera and composition**: at the H1-approved 4:5 or 16:9 canvas; design the camera angle, podium, scene centre of gravity, and text clear space independently for the H2 layout, and never force a vertical frame into landscape.
5. **Tone and style**: overall colour temperature, saturation, style keywords (for example "Nordic minimal", "warm high-end grey").
6. **Hard prohibitions**: any text, letters, numbers, watermark, logo, brand mark, price tag, or people (unless required).
7. **Output**: a realistic empty scene base at the H1 ratio; if the tool returns another ratio, only reconstruct/reframe the empty scene sensibly and never stretch a real product; this is not a product-faithful render.

Assembly example (replace each item before use; never copy brand names):

```text
Realistic empty still-life background plate for an e-commerce composite. No product or product-like object.
Place an empty <H2-approved support surface> in <H2-approved scene area> with <scene description>.
<light direction and softness> lighting, soft natural scene shadows. <H1-approved aspect ratio> composition with <H2-approved camera angle>
and clean negative space only where the approved layout requires text overlay.
<tone and style>. High resolution, coherent background plate, commercial editorial quality.
Absolutely no product, bottle, package, container, device, product silhouette, text, letters, numbers, watermark, logo, price tag, caption, or UI elements.
```

Check the generation for pseudo-text, logo ghosts, malformed structure, extra fingers/shadows, and distorted proportions. Regenerate rather than covering it up with retouching.

Both editions must use the **same** base image. When the two layouts need slightly different framing, change only the text layer coordinates, not the picture.

## Path three: placeholder base (to fix the layout first)

When photography is not ready and generation is inconvenient, use `scripts/make_placeholder_base.py` to produce a base at the H1 specification with a product placeholder frame, so the layout and information hierarchy can be confirmed (pass `--width 1920 --height 1080` for landscape; the existing placeholder frames are sketch-only and need adjusting for H2):

```bash
python scripts/make_placeholder_base.py --out work/base/base-cn.png --tone greige \
    --product-area center --product-ratio 0.55 --label "PRODUCT PHOTO AREA"
```

A placeholder draft may only be used for internal layout confirmation. The delivery notes must state that the base image is pending replacement, and an image still carrying "PRODUCT PHOTO AREA" may never be delivered.

## Path four: paper-texture base (editorial paper)

The editorial paper style (`editorial-paper`) needs a paper-texture base rather than a photograph:

```bash
python scripts/make_paper_base.py --out work/base/base-cn.png --tone paper \
    --grain 0.45 --blotch 0.35 --fiber 0.35 --vignette 0.35
```

`--tone` accepts `paper` (cream) / `ivory` (near white) / `kraft` / `cool` / `ink` (dark). The paper texture should be "visible but not readable": too much grain competes with the text, and pushing the blotch parameters produces banding, so render first and judge from the actual image. Both editions share one paper base (same seed).

## Path five: gradient + props (editorial scene)

When the product colour is clear and the scene needs atmosphere, use `scripts/make_scene_base.py` to generate an echoing gradient and props:

```bash
# Bright "bamboo shadows on water" scene: these numbers are a starting example to be adjusted at H2, not a fixed layout
python scripts/make_scene_base.py --out work/base/base-cn.png --palette mist --seed 20261005 \
    --props leafshadow,bamboo,water --podium-kind travertine \
    --pedestal 0.50 0.80 0.90 0.8667 --podium2 0.10 0.8267 0.34 0.8733 \
    --water 0.84 --band 0.20 --product-x 0.70 --grain 0.16 --vignette 0.12

# Dark echoing-colour scene (when the product's dark components dominate)
python scripts/make_scene_base.py --out work/base/base-cn.png --palette sage --seed 20261001 \
    --pedestal 0.30 0.9133 0.70 0.9583 --props linen,sprig,citrus
```

| Parameter | Effect |
| --- | --- |
| `--palette` | `mist` (light mist, pairs with dark text) / `mint` / `sage` / `olive` / `clay` / `ink` / `sand` |
| `--pedestal x0 y0 x1 y1` | Stone podium position (canvas fractions); set it from the H2-approved support surface and product resting point, with no fixed height |
| `--podium-kind` | `stone` (dark grey stone) / `travertine` (light terrazzo) |
| `--podium2 x0 y0 x1 y1` | A second pedestal (drawn first, creating front/back layering) |
| `--water <y>` | Water start height as a fraction, used together with `water` in props; generates a reflection and ripples |
| `--props` | `leafshadow` (bamboo-leaf shadows) / `bamboo` (bamboo stems) / `water` / `linen` / `sprig` / `citrus` / `pebble` / `drape` / `pine` / `fruit` / `pod` |
| `--glow` | Soft light pool `cx cy rx ry strength`; `strength` above 0.8 starts to blow out |
| `--band` / `--product-x` | Prop-band fraction / product centre horizontally; both are adjustable H2 option parameters, not universal fixed values |
| `--branch-base` / `--branch-length` | Branch root and length (canvas fractions) |
| `--band` | Suggested height fraction of the bottom prop band; adjust to the H2 layout |
| `--product-x` | Suggested horizontal centre of the product subject; adjust to the H2 layout and the real support surface |
| `--bokeh` | Strength of the edge-blurred foliage; around `1.0` is suggested for light-toned scenes |

A measured parameter set for the light-toned off-centre scene (matching the `editorial-scene` template):

```bash
python scripts/make_scene_base.py --out work/base/base-cn.png --palette mint \
    --props drape,pine,fruit,pod --no-pedestal --band 0.21 --product-x 0.68 \
    --bokeh 1.0 --grain 0.18 --vignette 0.10 --glow 0.62 0.34 0.44 0.36 0.5 --seed 20261002
```

Props are atmosphere only: their extent, the podium position, the product resting point, and the text areas must follow the H2-approved layout — they are not fixed to the lower third, and no particular height line is prescribed. The product itself must still be composited from approved photography/a cut-out, with a `shadow` layer matching the real support surface. Both editions share one scene base (same seed, same parameters). Without an approved product image, the base image can only serve planning or a non-fidelity layout concept.

## Path six: scene photography from the user or an asset library (recomposition)

Given a scene photo (studio still life, water surface, pedestal), use `scripts/build_scene_from_photo.py` to scale and crop it proportionally to the H1 canvas; for landscape pass the H1-confirmed size and let H2 decide the resting point, for example 1920×1080:

```bash
python scripts/build_scene_from_photo.py --src work/base/scene-photo-src.jpeg \
    --dst work/base/base-cn.png --width 1920 --height 1080 \
    --podium-px <surface x in source> --podium-py <surface y in source> --px <H2 target x fraction> --py <H2 target y fraction>
```

It scales proportionally until the canvas is covered, then aligns the surface as closely as possible and crops, avoiding black edges; when the source cannot satisfy both coverage and the target resting point it warns, so you must look at the actual resting point and never treat a coordinate input as proof of the contact relationship. `--podium-px/--podium-py` are the surface position in the source image (automatic detection easily mistakes a bright wall for a surface in light scenes).

Rules:

- Only proportional scaling, translation, and cropping — **no painting over, patching, or watermark removal**; unwanted elements (including watermarks) must be excluded from the frame by recomposition.
- Third-party photos must have confirmed licensing (own photography / purchased licence / AI generated); assets carrying a platform watermark are not usable for delivery by default — see `references/en/compliance-and-claims.md`.
- If the product stands on water, add a reflection layer (vertical mirror of the product image + fade + slight blur) so it does not float.

Generate reflections with the script rather than by hand:

```bash
python scripts/make_reflection.py --src work/base/product-cutout.png \
    --out work/base/product-reflection.png --fade-top 0.42 --blur 2.2
```

The resulting `product-reflection.png` is used as an ordinary image layer, with the box's y origin at the product's base height (for example `[655, 1196, 400, 900]`, `opacity` 0.5–0.6).

## Base-image asset naming

```text
work/base/base-cn.png         main base image (shared by CN and EN)
work/base/product-cutout.png  product cut-out (used by info-white and hero-subject)
work/base/detail-macro.png    macro detail
work/base/badge-icon.png      icon inside a badge (optional)
```

## Self-check

- Is the text area clean enough (evenly toned)? On complex photographic backgrounds, prefer local brightness adjustment, a soft scrim, or a gradient transition so the text area gets continuous tonal support; avoid unnecessary hard-edged rectangles. If local support still damages the scene or the hierarchy, change the base image or rearrange the text area.
- Has the subject lost key structure to cropping? Product completeness outranks compositional beauty.
- Does the base image's tone clash with the brand colour? When it does, unify it by laying a low-opacity brand-colour mask over the base.
- Is any third-party asset, someone else's watermark, or platform badge left in the frame?
