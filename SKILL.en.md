---
name: ecommerce-kv-design
description: Turn well-sourced product material into a bilingual Chinese/English e-commerce hero image (KV), vertical 4:5 by default and landscape 16:9 when H1 explicitly chooses it; when no reliable product reference exists, produce planning or an explicitly labelled non-fidelity concept only. Use when the user asks for a promotional KV, campaign hero image, or bilingual product marketing image; product hero images must also respect the target platform's extra limits, so never claim every platform accepts the render as-is. Do not use for visual planning only, copy planning only, product retouching, or long detail-page images.
metadata:
  short-description: E-commerce hero image: bilingual 4:5 or 16:9 PNG
---

# E-commerce product hero image (KV)

Turn product material into two human-approved, deliverable images: **one Chinese edition + one English edition**, vertical 4:5 by default and landscape 16:9 only when H1 explicitly chooses it, as PNG. Product hero images must still be checked against the target platform's own limits; never claim the renders can go live on every platform as-is.

This is an English companion to `SKILL.md`. Both editions describe the same workflow, scripts, and templates; only the documentation language differs. Read the English references under `references/en/` (the Chinese ones under `references/` are the source of truth if the two ever diverge).

The method separates **picture** from **information**: the product and scene come from photography, a cut-out, or a generated base; headlines, selling points, specifications, price, promotion dates, and annotations are all rendered deterministically from a JSON spec by `scripts/build_kv.py`. **Never hand Chinese copy, prices, or dates to an image-generation model** — it writes them wrong and they cannot be edited afterwards.

## Delivery contract (hard)

| Item | Requirement |
| --- | --- |
| Chinese edition | `outputs/KV-CN-4x5.png`; with an approved 16:9, `outputs/KV-CN-16x9.png` |
| English edition | `outputs/KV-EN-4x5.png`; with an approved 16:9, `outputs/KV-EN-16x9.png` |
| Canvas | Vertical 4:5 at 1200×1500 by default; with an H1-confirmed 16:9, landscape at 1920×1080 suggested; shortest side ≥1000px |
| Format | PNG (RGB) |
| Relationship | Same base image, same skeleton, same facts; the English edition is a localised re-layout, not a word-for-word translation |
| Companion | `outputs/交付说明.md` (an English project may use `outputs/delivery-notes.md`): audience, single core value, selling-point evidence, promotion price and date sources where applicable, H1/H2/H3 result versions |

## Working directories (fixed convention)

```text
<project root>/
├─ outputs/                     deliverables only
│  ├─ KV-CN-4x5.png
│  ├─ KV-EN-4x5.png
│  ├─ KV-CN-16x9.png            only with an approved 16:9; never overwrites the 4x5
│  ├─ KV-EN-16x9.png
│  └─ 交付说明.md
└─ work/
   ├─ input/                    the user's raw material (photos, logo, credentials, campaign screenshots)
   ├─ brief/kv-brief.md         structured brief
   ├─ spec/kv-cn.json           Chinese spec (the single source of truth for layout)
   ├─ spec/kv-en.json           English spec (same coordinates, copy swapped only)
   ├─ base/                     base-cn.png (shared by CN and EN) plus optional detail images
   └─ render/                   iterations, comparison sheets, report.json
```

Changing an image = change the spec and re-render; never edit a PNG directly. Intermediate artifacts always stay in `work/`.

## Seven-step workflow (across turns)

This is not a pipeline inside one reply. In any single turn, go no further than the next Human Gate that has not received genuine user approval; once you submit the material for that gate, you must end the reply and wait for a new user message. Without an explicit user message naming the submitted version and the approved scope, you may not proceed, and you may never backfill an approval history yourself.

1. **Set up and analyse the facts**: create the directories and put the user's material in `work/input/`; inspect the available product references, brand assets, facts, and copy. Look at image assets before citing them — never guess content from a file name.
2. **Write the brief, submit the H1 input baseline, and stop the turn**: per `references/en/workflow-and-brief.md`, record the Reference/Facts Inventory, the product-fidelity mode, the Project Style Constraint Record, and the Canvas Specification (purpose/platform, ratio/pixels, orientation, PNG, platform limits, source, and confirming message). Vertical 4:5 is the default; a user-specified 16:9 must not be reverted to vertical. Report conflicting platform specifications and ask for confirmation first. Verify prices and dates only when a promotion is involved. Stop the turn after submitting; step 3 is forbidden without approval.
3. **Fix the audience and the single proposition**: write in one sentence "for whom / in what situation / solving what / why buy now". The main headline carries exactly one core value, with at most three supporting selling points; build a traceable communication hierarchy inside the H1-confirmed brand hard constraints.
4. **Propose creative directions, submit the H2 selection/freeze, and stop the turn**: only after H1 is approved. By default submit three substantially different options A, B, C plus a comparison; each must design its product centre of gravity/share of frame, real support surface, scene, text areas, reading path, typography, palette, information hierarchy, risks, and feasibility for the approved Canvas Specification. A landscape canvas may not be made by scaling or cropping the vertical skeleton; A–H are candidates only. Close the reply with the four interaction entries (approve, edit/combine/re-propose, mode A, mode B) and stop the turn; when the user asks for fewer than three options or the constraints are insufficient, handle it as the real situation dictates.
5. **Decide and build the base image**: only after H2 is approved. Approved, inspectable product photography comes first; without a reliable product basis you may only produce planning or an explicitly labelled non-fidelity layout concept. AI may generate scene bases with no product and no text, but may not reconstruct a real product from a text description and call it product-faithful. Both language editions share one base image.
6. **Write the specs and render**: 4:5 may rework an existing template; 16:9 starts from the landscape spec and is re-laid out per H2, never converted from old coordinates. The CN and EN specs have the same canvas size, base image, and skeleton, with the English edition adjusting only text-box width, type size, and line breaks for copy length. Candidate renders stay in `work/render/`; open the actual images and finish visual QA before submitting H3.
7. **Technical QA, submit the H3 real renders, and stop the turn**: run `scripts/verify_kv.py` and walk `references/en/quality-gate.md` item by item. If the support contact, contact shadow, or medium relationship does not hold, rework — never submit H3 on top of it. After technical and visual QA, submit the actual CN/EN images, thumbnails, versions, and issue list, and end the reply. Only when the next turn brings explicit H3 approval bound to the corresponding actual image version may the renders and notes be copied into `outputs/`.

## Three human gates

A gate is a human decision point. It is not equivalent to a script state, `READY`, `PASS`, or `verify_kv.py` exiting 0. Approval evidence can only come from an explicit confirmation message the user sends after the material was submitted, and it must point at the corresponding version and approved scope. An `Approved` the model writes into the brief, a report, or the delivery notes is not approval evidence; a general authorisation such as "please complete the whole task" is not advance approval of the three gates either. Each gate records only: submitted version, user message evidence, approved scope, decision maker/date where applicable, and result version.

### H1: input baseline confirmation (after steps 1–2)

- AI submits: the material and facts inventory, the status of inspectable product reference images / brand assets, the product-fidelity mode, gaps and conflicts, and the first draft of the Project Style Constraint Record and Canvas Specification.
- Human confirms: evidence, official fonts / brand colours / forbidden elements, essential product facts, the task type, and the canvas purpose / target platform, ratio, pixel size, orientation, PNG, plus any extra platform limits and their source. Prices and promotion dates are verified only when the task involves a promotion.
- The result can only be `Approved`, `Changes requested`, or `Returned`. With no genuine user approval message it stays `Pending`, and step 3 is forbidden.
- `Changes requested` returns to the material/facts analysis of step 1 or the brief of step 2; `Returned` (unusable evidence, conflicts, or an unclear task boundary) returns to step 1 and, if necessary, switches to planning mode.

### H2: creative direction and project style freeze (after steps 3–4, before production starts at step 5)

- AI submits: three options A/B/C plus a short side-by-side comparison by default; the option fields and version rules are in `references/en/workflow-and-brief.md`. The three options must respect the H1 facts, brand hard constraints, licensing, product fidelity, and platform limits, and may not differ only by colour or name. The AI may give a reasoned recommendation, but may not choose, freeze, or write `Approved` itself.
- Human confirms: approve a specific ID/version outright, request local edits, combine parts of different options, ask for a re-proposal, or name an option and request a low-fidelity preview. An edit or combination must produce a new option version and be confirmed again; only when the user explicitly approves a specific option and version does its approved scope enter the Project Style Constraint Record. Global hard constraints and the H1-confirmed brand hard constraints cannot be overridden by a suggestion.
- Optional previews: by default deliver text and composition strategy only. Preview only after the user names both the options and the mode; mode A uses local scripts/simple shapes (with a labelled placeholder frame when there is no product basis), mode B additionally requires explicit authorisation and generates product-free, text-free backgrounds only. Previews use the H1-approved ratio and are labelled afterwards with the option ID/version and `CONCEPT / NOT FINAL`; they stay in `work/render/` and never become full bilingual production or H3. When generated images come back at the wrong size, rebuild the scene composition only — never stretch the product.
- The result can only be `Approved`, `Changes requested`, or `Returned`. With no genuine user approval message naming an explicit option and version, it stays `Pending`; "please continue", "please complete the task", "generate something and let me see", and preview authorisation are not approval. While H2 is `Pending`, apart from the concept previews the user explicitly requested, no background or render for production may be generated and step 5 may not begin.
- `Changes requested` returns to steps 3–4 and re-submits H2 once a new version exists; `Returned` (a direction that depends on missing evidence or exceeds scope) returns to steps 1–2. If an image-generation preview fails because of permissions, an interface, or a service, stop retrying, report honestly, keep H2 `Pending`, and you may suggest mode A; without consent, never switch to stock photography, another generation service, or fabricated results.

#### Mandatory closing interaction format for an H2 reply

After submitting H2 options, the reply must tell the user they can:

- approve a specific option ID/version outright;
- edit, combine, or re-propose options;
- request mode A: low-fidelity composition sketches built with local scripts, templates, and simple shapes, with no online image generation;
- request mode B: after explicit user authorisation, call the available image-generation tool to build a low-fidelity scene-atmosphere preview.

Modes A and B may be requested for some or all options; a preview is still part of the H2 decision stage, authorising it is not formal approval, H2 stays `Pending`, and production may not start early. No preview is generated by default. Close with examples that can be copied directly:

```text
Approved A-v1
Change the headline font of B-v1
Combine the composition of A-v1 with the information hierarchy of C-v1
Preview A-v1, B-v1, C-v1 with mode A
Authorise a mode B preview of B-v1
```

### H3: real-render review (after the technical QA of step 7)

- AI submits: the actual rendered full-size CN/EN images and thumbnails, the corresponding spec/base versions, the technical QA report, the visual issue list, the product-reference comparison, and promotion fact sources (when the task involves a promotion).
- Human confirms: whether the actual product matches the approved reference; composition, product prominence, text hierarchy, legibility, real scene/contact relationships, brand constraints, cross-edition factual consistency, and whether the images may enter `outputs/`.
- The result can only be `Approved`, `Changes requested`, or `Returned`. With no genuine user approval message it stays `Pending`; candidates may not be treated as formal deliverables nor moved into `outputs/`.
- `Changes requested` returns to step 5 (base image/composite) or step 6 (spec/render) according to where the problem belongs, then re-runs QA/H3; `Returned` (the direction or facts simply do not hold) returns to steps 3–4, and to steps 1–2 when the evidence has become invalid. If the product is detached from its support surface, the contact shadow does not hold, or a photographic product clashes with an illustrated scene without H2 approval of mixed media, rework at steps 5–6 and do not submit H3.

Human approval must target the actual image and a matching version; a passing AI technical check is never human approval.

## Hard rules

- Text never enters an image-generation prompt; all text, prices, and dates are rendered from the spec.
- One headline carries one value; ≤3 selling points; ≤4 hierarchy levels.
- Product position, subject height, the text-to-opposite-side relationship, the bottom prop band, and podium position have no fixed cross-skeleton values; use the chosen skeleton's suggested parameters as the H2 proposal, and let the H2-approved option, the product reference, and the real support surface govern in the end.
- The left and right text columns may never be covered by the product outline.
- Whether the product sits left or right of centre, slightly above the visual midline, and which side the text column takes are decided by the H2-approved skeleton and reading order; never treat example coordinates as universal hard limits.
- The bottom prop band, the podium/support surface, and the product's contact position follow the real support relationship and the H2 layout; "about 1/5" and other height figures belong only to the suggested parameters of a specific skeleton.
- Only the exact 4:5 or 16:9 confirmed at H1 is supported, with a shortest side ≥1000px, as PNG; the user may specify exact dimensions as long as they match the ratio. `--scale` must be identical across both editions and the final size must equal the H1 specification; never stretch the product or the rendered bitmap.
- Verify prices, struck-through prices, final-price conditions, and promotion dates only when the task actually involves promotional information; certifications, sales figures, and performance claims only as user-provided or verifiable facts. When evidence is missing, delete it or stop in planning — never use "to be confirmed" to support an unapproved formal delivery (see `references/en/compliance-and-claims.md`).
- The formal hero image for a real product must rest on an approved, inspectable product reference. Without a reliable product basis, output planning or an explicitly labelled non-fidelity layout concept only, and never claim product fidelity.
- A real product must form a credible contact with the H2-approved support surface; obvious floating, a detached contact shadow, or a support relationship that does not hold means a rework and no H3 submission.
- The medium relationship between real photographic product and illustration or procedural props must be explicitly approved at H2; an unapproved obvious clash is reworked first.
- Candidate renders, previews, and reports stay in `work/render/` before H3; only after an explicit H3 approval bound to the matching actual image version may anything enter `outputs/`.
- Brand logos are never stretched, redrawn, or recoloured; with no logo, use a wordmark placeholder and note it in the delivery notes.
- When no official font, logo, or palette is provided, record "not provided" in the Project Style Constraint Record; candidates may be proposed, but a candidate is not an official rule, and a wordmark placeholder may not be called the official logo.
- When the client supplies a bilingual content master table, every entry must appear in the corresponding language edition, verified to zero omissions with `scripts/check_copy.py`.
- The English edition may contain no CJK characters or full-width punctuation; the Chinese edition keeps no English placeholders.
- Facts and figures must be exactly identical across the two editions.
- On dark or gradient backgrounds use exactly one accent colour; light type stays entirely in the dark zone and dark type entirely on the light surface zone, never straddling the boundary.
- Enlarge important text (headline, price, promotion dates) first; it may be partly covered by the product, but the covered height may not exceed 1/4 of the character height, and a word or character may not be cut beyond legibility. After enlarging, check the visible extent of both text columns line by line.
- Information text (product name, selling points, specifications, promotion dates) must not be set as "small print": at the 1200-wide baseline body is 30–34px, labels 24–28px, weight Bold/Medium; rather than shrink type to unreadability, cut the copy.
- A call to action (Shop now / 立即选购) is an optional layer: when the user did not ask for it, or explicitly asked that none appear, delete both the text layer and the underline layer and leave the bottom right empty.
- When the user asks to drop an entry from the content master, never omit it silently: register the field and reason in the master JSON's `waived` list, and `check_copy.py` will report it separately as "waived" rather than as an omission.
- Every script `[warn]` must be handled or explained in the delivery notes.

## Fonts

- Prefer Noto Serif SC for Chinese headlines (variable weight via `variation`: `Black`/`Medium`/`Light`).
- Latin headlines use `assets/fonts/PlayfairDisplay-VF.ttf` (Didone-style high-contrast serif, SIL OFL, commercially usable; the licence text sits alongside it).
- Large Chinese headlines in the samples are usually a commercially licensed Song/Ming face; among free fonts, Noto Serif SC Heavy is the closest. When the user specifies a font, that font wins — collect the file into `assets/fonts/` so the render stays reproducible.
- Spec font references: copy the file into `work/base/fonts/` and use a relative path, or write the absolute system path; when a file is missing the script warns and falls back.

## Script usage

```bash
# Render (same --scale for CN and EN; coordinates and type sizes scale together)
python scripts/build_kv.py --spec work/spec/kv-cn.json --out work/render/KV-CN-4x5.png --scale 1.0
python scripts/build_kv.py --spec work/spec/kv-en.json --out work/render/KV-EN-4x5.png --scale 1.0

# Technical check (fill expected width/height with the H1-approved output size; it does not verify semantics or visual relationships)
python scripts/verify_kv.py --cn work/render/KV-CN-4x5.png --en work/render/KV-EN-4x5.png \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json --expected-width 1200 --expected-height 1500

# After H1 approves 1920x1080: rework the landscape template, render both editions at the same size and base, then verify against the approved spec
python scripts/build_kv.py --spec work/spec/kv-cn.json --out work/render/KV-CN-16x9.png
python scripts/build_kv.py --spec work/spec/kv-en.json --out work/render/KV-EN-16x9.png
python scripts/verify_kv.py --cn work/render/KV-CN-16x9.png --en work/render/KV-EN-16x9.png \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json --expected-width 1920 --expected-height 1080

# Content-master completeness check (mandatory when the client supplied a bilingual master)
python scripts/check_copy.py --master work/brief/content-master.json \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json

# Paper-texture base for the editorial paper style
python scripts/make_paper_base.py --out work/base/base-cn.png --tone paper

# Gradient + prop base for the editorial scene style (echoing the product palette)
python scripts/make_scene_base.py --out work/base/base-cn.png --palette sage --seed 20261001

# Crop a scene photo proportionally to the H1 canvas; H2 decides the surface coordinates, so re-check the real resting point after cropping
python scripts/build_scene_from_photo.py --src work/base/scene-photo-src.jpeg \
    --dst work/base/base-cn.png --podium-px 548 --podium-py 878 --px 0.674 --py 0.80

# Reflection for a product standing on water or a reflective stone surface (the scene-photo-side template depends on it)
python scripts/make_reflection.py --src work/base/product-cutout.png \
    --out work/base/product-reflection.png

# Default 4:5 placeholder base while photography is pending (pass --width 1920 --height 1080 for landscape)
python scripts/make_placeholder_base.py --out work/base/base-cn.png --tone greige
```

The scripts depend on Pillow only; fonts resolve from the system font directories automatically and can be pointed at with the `fonts` field or `KV_FONT_DIR`.

## Skeleton templates (matching the A–H list in `references/en/visual-system.md`)

| File | Skeleton | Suited to |
| --- | --- | --- |
| `assets/templates/scene-atmosphere.json` | Photographic atmosphere (annotations + oversized bottom headline) | Home, furniture, lighting, large goods |
| `assets/templates/scene-atmosphere-en.json` | The English twin of the above (same coordinates, copy swapped) | Paired CN/EN delivery |
| `assets/templates/info-white.json` | Light-background information (spec block + chips + detail shots) | Glassware, tableware, small appliances, storage |
| `assets/templates/hero-subject.json` | Hero subject (angled colour block + information card + large specification) | Maternal/baby, pet, 3C, cleaning appliances |
| `assets/templates/editorial-paper.json` | Editorial paper (paper texture + oversized serif headline + copper hairline system) | Higher price points, strong mood, must match the detail page |
| `assets/templates/editorial-paper-en.json` | The English twin of the above (same coordinates, copy swapped) | Paired CN/EN delivery |
| `assets/templates/editorial-scene.json` | Editorial scene (light gradient + edge-blurred foliage + bottom prop band 1/5 + off-centre product set slightly high) | Clear product colour, needs scene atmosphere and mood |
| `assets/templates/editorial-scene-en.json` | The English twin of the above (same coordinates, copy swapped) | Paired CN/EN delivery |
| `assets/templates/scene-photo-side.json` | Photographic scene, side subject (product suggested in the right third, suggested bottom prop band, product on a podium) | Studio still-life or water-surface basis, finished-grade layout |
| `assets/templates/scene-photo-side-en.json` | The English twin of the above (same coordinates, copy swapped) | Paired CN/EN delivery |
| `assets/templates/landscape-concept-cn.json`, `landscape-concept-en.json` | 16:9 landscape concept starter; the product placeholder, copy, and support surface must be swapped per H2 | H2 mode A or a landscape starter; never deliverable as-is |

F and H in `visual-system.md` are parameter variants of `editorial-scene` and add no template file. Sample copy demonstrates layout only and must be replaced with real, confirmed product information before delivery; English replacements may not add unverified sales, performance, or "bestseller" claims.

All older templates are 1200×1500 vertical; landscape is not a coordinate-scaled version and must be composed independently per H2. Existing project options and approved versions do not change automatically because the skill rules were updated.

## English documentation map

| Edition | File |
| --- | --- |
| Skill overview (this file) | `SKILL.en.md` |
| Workflow, directories, brief template, gap handling, delivery notes template | `references/en/workflow-and-brief.md` |
| Skeleton selection, grid, type scale, colour, legibility, brand rules | `references/en/visual-system.md` |
| Writing or editing spec JSON, layer fields, command-line arguments | `references/en/spec-schema.md` |
| Where base images come from, prompt structure, placeholder bases | `references/en/photo-base.md` |
| Character budgets, terminology, localisation practice | `references/en/copy-cn-en.md` |
| Prohibited superlatives, price and promotion wording, category sensitivities, platform differences | `references/en/compliance-and-claims.md` |
| Item-by-item acceptance and common rework causes | `references/en/quality-gate.md` |
| Image-generation prompt template for scene bases | `assets/templates/imagegen-scene-prompt-en.md` |

## Boundaries

- Do not publish, list, or modify the user's platform accounts; produce files and documentation only.
- Do not fabricate material; when key information is missing, ask first and never guess a price or a date.
- When the task is only this one hero image, do not also produce a long detail-page image, listing copy, or an ad plan unless the user asks.
- Platform rules change over time; for the current review standard, check the latest official source, and mark it "not verified" when you cannot find it.
