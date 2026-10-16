# Layout System

The A–H coordinates and type sizes below reference the default 1200×1500 (4:5) vertical canvas; the same vertical structure scaled to 1800×2250 can use `--scale 1.5`. When H1 approves 16:9, design independently at the real landscape width and height — do not scale, crop, or stretch a vertical template.

## Grid and safe areas

- For 4:5 the reference outer margin is 60px (5% of canvas width); for 16:9 re-derive the safe area from the width, height, and placement context, keeping in mind the tighter top and bottom edges, and do not carry the 60px vertical layout over directly.
- The three vertical bands (top brand row / middle product zone / bottom information zone) and the bottom information band are the baseline grid; the exact heights, whether promotion information appears, and where text areas sit are decided by the H2 layout.
- Product share of frame and centre of gravity are suggested ranges per skeleton; do not treat baseline figures such as 35%–65% or 38%/62% as hard limits that apply across skeletons.

For 16:9 you may use a left/right split or a well-justified centred composition: position the product's centre of gravity and share of frame, the primary and secondary text areas and negative space, the reading path, the actual contact line, and its shadow separately; choose legible type sizes again for a 1080px height, and do not simply crop away the vertical bottom information band. Chinese and English keep the same approved skeleton; long English copy only adjusts box width, type size, or line breaks.

## H2 visual and support-relationship checks

An H2 proposal must state the product position and share of frame, the actual support surface, the contact point/area, the contact shadow or reflection relationship, the scene medium, the main text areas, and the typography and palette strategy. Podium position, product base height, and prop-band proportion may only serve as suggested parameters of the chosen skeleton; the approved layout and the real support surface govern in the end.

- The product base must form a credible contact with the approved support surface; if the render shows obvious floating, a support surface whose scale or perspective does not match the product, or a contact shadow that has detached, visual QA rules it a rework.
- The medium relationship between real photographic product and illustration or procedural props must be explicitly approved at H2; an unapproved, obvious mixed-medium clash may not proceed to H3.

Judge the contact relationship in this order: actual contact line → support-surface perspective → light direction → how well the contact shadow fits and how soft or hard it is. Coordinates intersecting is only a positioning clue, never proof that the product is "supported". The darkest part of the contact shadow should hug the product base and fall off outward following the real base outline; apart from reflective materials such as water or mirrors, never use a reflection in place of a contact shadow.

When the product floats or the support relationship is not credible, first fix the scene's surface, the product's resting point, scale, and perspective, then fix the contact shadow, and only then do local blending. Never alter the real product's structure, proportions, colour, or key details to accommodate the scene. A photographic product should keep a consistent photographic medium with the podium, background, and shadow; a photography/illustration clash that H2 has not approved must be reworked.

## Substantive differences among the three H2 options

After H1 is approved, propose three options A/B/C by default. They should start from the product and the communication goal and differ across several key dimensions: photographic vs. editorial style, visual skeleton, product centre of gravity and share of frame, scene medium and support relationship, main text areas, Chinese/English typography strategy, primary/accent colour, and information hierarchy. Changing only colour, option name, or local decoration does not make a new option.

- Each option must be producible with the available assets and production capability, and must respect the same H1 facts, licensing, brand hard constraints, product fidelity, and platform limits.
- You may recommend the option that best fits the goal, but a recommendation is neither a selection nor an approval.
- A–H are a design resource library only: the three options may use different skeletons, substantively different strategies on the same skeleton, or no off-the-shelf skeleton at all; never fix on a particular trio of skeletons, and never force every product through the same three-style set.
- The side-by-side comparison must at least state the core strategy, composition/medium differences, main strengths, risks, and production cost. When the constraints only support fewer than three sound options, say so honestly instead of padding the count with fake differences.
- After the user requests an edit, a combination, or a new proposal, compare and confirm again as new option versions; only the approved version's core style, skeleton, typography strategy, and palette may enter production.

H2 concept previews use the H1-approved 4:5 or 16:9 canvas and the same factual baseline, and serve only direction comparison. Mode A uses simple shapes / the landscape concept template plus any necessary approved assets; Mode B generates product-free, text-free backgrounds only after explicit authorisation. Both are labelled afterwards with the option ID/version and `CONCEPT / NOT FINAL` and are saved only in `work/render/`; a preview is not an approval — see `workflow-and-brief.md`.

## Skeleton list (A–H)

The skeletons below are comparable layout candidates, not mandatory templates and not a fixed menu for the default three H2 options. F and H of `editorial-scene` are different parameter variants of one template; which one is used, or how it is adjusted, must be frozen at H2 and is bound by the H1 brand hard constraints, the available assets, the real support surface, and the target-platform limits. Every position, size, product proportion, and prop-band figure in these sections is a suggested parameter of that skeleton, not a universal hard limit across skeletons.

### A. Photographic atmosphere `scene-atmosphere`

Suited to home, furniture, lighting, and large goods; works best with real scene photography.

Skeleton: brand wordmark top left + badge top right | one or two annotation groups on each side (large translucent number + small caption + leader line + "+" node) | circular promise badge bottom right | a darkened bottom holding the series name + oversized main headline + one-line subtitle | price and promotion dates on a yellow/brand-colour bar.

Key points:

- Darken the scene base before setting type: a 0.40 scrim at the top and two stacked layers at the bottom (0→0.45, 0.36→0.92); a single layer often fails to hold down a light-coloured surface.
- Leader lines of the annotations end on product details, never in empty space; nodes are small "+" dots in the brand accent colour.
- The main headline uses an oversized 150–200px sans; dare to go large — this is where you differentiate from competitors.

### B. Light-background information `info-white`

Suited to glassware, tableware, small appliances, storage, and everyday consumables; leads with specifications and materials.

Skeleton: light grey / off-white ground | large headline top left (2–3 lines) | material chips (pills + "+" dots) | specification block (large number + unit + small label) | macro detail thumbnails | two or three bullet selling points | price and deadline on a solid bottom bar.

Key points:

- Text left, product right: text takes 45% of the left side, the cut-out product 55% of the right; the two must not overlap.
- At most two specification blocks, numbers 90–110px, units 30–36px, labels 26–30px; number and unit must share a baseline.
- Mark selling points with dots or short vertical bars, no more than 14 characters each and at most two lines.
- The bottom band uses the brand accent colour, with the price largest, the date next, and the footnote smallest.

### C. Hero subject `hero-subject`

Suited to maternal and baby, pet, 3C, cleaning appliances, and large goods; persuades through subject scale and key specifications.

Skeleton: light warm gradient ground + angled colour block | small prefix + main headline top left | pill label | two vertical-bar selling points on the left | large specification number (load capacity / volume / runtime) | dark information card top right (age range / model / capacity) | brand, price, and promotion dates on a white bottom bar.

Key points:

- Make the product image as large as possible, allowing it to overlap the edge of the angled colour block to create depth.
- The information card carries hard facts (age, model, specification), never adjectives.
- The left selling points plus the large specification number form two blocks of visual weight; give the specification block the heaviest weight.

### D. Editorial paper `editorial-paper`

Suited to higher-priced, strongly designed products that need a shared mood with the detail page; a magazine layout on a paper-texture ground with high-contrast serif headlines.

Skeleton: paper-texture ground (generated by `scripts/make_paper_base.py`) | brand icon + wordmark top left, small promo line top right | oversized serif main headline in two lines top left, the second line offset right in the accent colour | product centred on a fine circle with a contact shadow | left column: product name + two or three dot selling points under a hairline + price label and large number under a hairline + promotion dates | right column: letterspaced vertical English, ring data badge, crosshair circle, dashed scale marks | hairline at the bottom + short category note on the left + underlined call to action bottom right.

Key points:

- Use exactly one accent colour (copper `#B5773F` in this example); the brand colour appears only in the logo, and the accent must not clash with the product colour.
- The hairline system is the backbone of this style: `width 1–2px`, opacity 20%–60%, all colours taken from the accent or an ink tone.
- Headlines use a variable-weight serif (Noto Serif SC Black/Medium/Light in combination): 150–180px for Chinese, reduced for Latin by character count (about 110–120px).
- Letterspaced Latin labels must be paired with `word_spacing` (2–3.5), otherwise the tracking squashes word gaps into one long string.
- Give the product a `shadow` layer for a contact shadow so it carries weight on the paper; the shadow should sit low and skew warm.
- Vertical letterspaced English is done as "one character per line + `\n`" with a line height around 1.25, at most 12–15 lines.
- Ring badges carry hard facts (capacity, warranty years, serial), never adjectives.
- Moderate procedural decoration (fine circles, crosshairs, dashed rules, dots) is where this style gets its recognition, but ask of each addition "does this help the product read?".

### E. Editorial scene `editorial-scene`

The scenic upgrade of the paper style: the paper texture is replaced by a gradient echoing the product palette, and props are added. Suited to products with a clear colour that need scene atmosphere while keeping the mood.

Skeleton: an echoing gradient, darker at the top and lighter at the bottom (`scripts/make_scene_base.py`) | brand wordmark top left + small promo line top right | two-line oversized serif headline top left (second line offset and switched to the accent colour) | product centred, occupying over 60% of the frame, resting on a stone surface with a contact shadow | left column: product name + hairline + dot selling points + hairline + price label and large number + promotion dates | right column: letterspaced vertical English, ring data badge | brand lockup bottom left (logo + wordmark) and underlined call to action bottom right, both on the light surface zone.

Key points:

- **The gradient must match the product palette**: take a dark product component (cap / body / packaging) for the top band, a light component or the surface for the bottom, and add a warm transition in between.
- **Text safety band**: keep the gradient dark down to 78% of the height so the headline, selling points, price, and dates all sit on dark ground; the last 12% is the light surface and carries only the brand row and the call to action in dark ink. Mixing text across the boundary reliably produces illegible words.
- **Product share of frame**: subject height ≥ 1/2 of the frame, with 60–66% being the range that visibly overprints the text; the inner edges of the left and right text boxes must stay inside the product outline.
- **Props only along the bottom third and the lower corners**: stone surface, linen, dried fruit, bare branches sit on the surface; they never enter the text columns or cover the product outline.
- **One accent colour only**: amber/copper, used for the second headline line, hairlines, dots, price label, and the underline of the call to action; the brand colour stays in the logo and on the product itself.
- Never place a dark logo on a dark background: move the logo onto the light surface zone (brand lockup bottom left) and keep only the wordmark at the top.

Text on a complex photographic background should first be supported continuously by repositioning the text area, adjusting local brightness, or using a soft scrim or gradient transition, and only then by changing the text colour; avoid adding unnecessary hard-edged rectangles purely to "hold down" the background. Local support should serve legibility and must not change the true relationship between product, podium, and photographic lighting.

### F. Bright scene style (light mist · bamboo shadows on water)

The scene style on a light ground: light mist background + bamboo-leaf shadows + bamboo stems + terrazzo podium + water reflection, with dark text legible throughout. Suited to daily-use, personal-care, and small home goods.

Skeleton (1200×1500 baseline): pale sage mist gradient (`--palette mist`) | bamboo-leaf shadows on the upper-left wall | bamboo stems entering from the top-right corner | logo + wordmark top left | two-line headline top left (second line in a desaturated amber) | left column: product name, selling points, price, promotion dates | product centred near 0.70 with its base on the 80% height line, seated on a terrazzo cylinder | the bottom 1/5 is the water and podium prop band (reflection, ripples, optional second pedestal) | promo badge bottom left.

Key points:

- **Dark type on a light ground**: all text in deep ink green (`#2E3A2C`), the accent in a desaturated amber (`#B08A4A`), hairlines at 25% ink.
- **Product position**: centre near 0.70 (right third), base on the 80% height line; the centre of the podium top must align to that line for the product to "stand" on it.
- **The bottom 1/5 is the prop band**: water, podium, and reflection all live there and body copy must not intrude (a promo badge may sit bottom left).
- **Enlarge and bold the small information text**: body 30–34px / Bold, labels 24–28px / Medium; thin type on a light ground is the easiest to lose.
- **The headline may be slightly covered by the product**: covered height ≤ 1/4 of the character height, and a word must never be cut (English is especially prone to mid-word cuts).
- Both the water reflection and the bamboo shadows stay low contrast (opacity 15%–35%), otherwise they compete with the text.

### G. Photographic scene · side subject `scene-photo-side`

A finished-grade layout built on a real or generated photographic still-life base (studio wall, water surface, stone surface); the least likely to look over-designed.

Skeleton (1200×1500): photographic base filling the frame | logo + wordmark top left | two-line headline top left (second line in amber) | left column top to bottom: product name, selling points, price, promotion dates | product centred at 0.674 (right third) with its base on the 80% height line, standing on a podium | the bottom 1/5 holds the podium + water + reflection | small promo line bottom left.

Suggested parameters (usable as an H2 proposal; the approved layout and the real support surface govern in the end):

| Item | Value |
| --- | --- |
| Product centre, horizontal | 0.674 (right-third range) |
| Product base height | 0.80 (= 1/5 left as the prop band) |
| Product height share | 56–60% |
| Right edge of the left text column | ≤ x 620 (must not enter the product outline) |
| Product name / selling points | 36px Bold / 34px Bold (Latin 32 / 31) |
| Price figure / label | 146px / 28px (Latin 140 / 24) |
| Promotion dates | 27px Bold (Latin 30) |

Key points:

- Three sources for the base image: `build_scene_from_photo.py` (reconstruction from owned or licensed photography), `make_scene_base.py` (procedural), and image generation (`imagegen-scene-prompt-en.md`).
- **A product standing on water or a glossy stone surface must get a reflection** (`make_reflection.py`), otherwise it floats.
- The headline may be slightly covered by the product (≤ 1/4 of the character height), but a Latin word must never be cut beyond legibility: English headlines usually need to shrink to 92–98px and shift left.
- Small labels on a light ground use a deeper amber (`#8F6B33`); reserve `#B08A4A` for large headlines and dots.

### H. Editorial scene light-toned off-centre `editorial-scene` (current default scene style)

A modern layout with light tones, generous negative space, and an off-centre product; suited to fragrance, personal care, beverages, and tableware — lighter-mood products.

Skeleton: very pale mint/off-white gradient + heavily blurred foliage at the edges (shallow depth of field) | brand wordmark top left + small promo line top right | opposite text column: two-line oversized serif headline (second line in the accent colour), product name, hairline, dot selling points, hairline, price label and large number, promotion dates | product to the right (about 0.68) or to the left, slightly above the visual midline, resting on the top edge of the bottom prop band | the bottom ~1/5 is the prop band: satin/fabric + pine sprigs + small fruit + dried fruit | letterspaced vertical English plus a small colour dot at the right edge.

Key points:

- **Off-centre the product**: putting it on the central axis looks stiff and wastes the layout space on the other side. Once offset, the text column can be wider and the headline larger.
- **The bottom 1/5 prop band**: control its height with `--band 0.21`; the product base should land near the top edge of the band so it reads as "placed on top of it".
- **Text on a light ground**: use a deep sage ink (#2E3A2C-grade) for the body text and a single gold (#B08A4A-grade) for accents; never pure black, and never several colours.
- **Product on a light ground**: an ivory product on a pale cream ground has very weak contrast, so stack two `shadow` layers (wide and faint + narrow and solid) to press it onto the surface.
- **Blurred foliage**: edge foliage uses a large blur radius (20px or more) plus low opacity, appears only along the four edges and corners, and must not enter the text columns, where it instantly muddies the type.
- **Allowed overlap**: the last character of the headline may be slightly covered by the product (≤ 1/4 of the character height) as long as the whole phrase still reads; body copy, price, and dates may never be covered.

## Type scale (1200×1500 baseline)

| Level | Use | Size | Weight |
| --- | --- | --- | --- |
| L1 | Main headline / series name | 150–200 | black / bold |
| L2 | Large specification number | 80–110 | bold |
| L3 | Price | 62–80 | bold |
| L4 | Subtitle | 36–44 | medium |
| L5 | Selling-point body copy | 30–38 | regular |
| L6 | Spec labels / units / promotion dates | 26–34 | regular / medium |
| L7 | Badges, footnotes, disclaimers | 22–28 | regular |

Keep the total number of levels to four or fewer (use weight and colour for secondary differentiation). Never place two levels within 5px of each other in one image — they will not read as separate.

## Colour

- One brand primary + two neutrals + one accent (price, action bar, nodes).
- On dark photography: pure white text with a `shadow` (`#00000066`, offset [0,3], blur 8).
- On light grounds: body text at the #2E2D2A level, labels at the #6B6A66 level; avoid a clash of pure black against pure grey.
- Use the accent, not the brand primary, for price and the action bar so it does not fight the brand identity.
- Contrast: body text ≥ 4.5:1, large headlines and badges ≥ 3:1. If it fails, add a scrim rather than smearing it over with a stroke.
- Whether a CTA/call to action appears depends on the actual marketing goal; it may be text, an underline, or another lightweight cue, and a button is not mandatory. When present, keep it at a supporting level so it never outweighs the headline, product, or price; when not needed, delete the related text and decorative rules entirely.

## Component specifications

- **Annotations**: numbers 80–100px, translucent (60% white), captions 32–36px; leader lines 2px with a small "+" node of 13–16px at the end.
- **Circular badge**: diameter 200–240px, ring text 28–32px, carrying hard commitments such as warranty, certification, or origin inside the ring, no more than 10 characters.
- **Chip**: height 60–70px, fully rounded, 30–34px type, separated from the next chip by a "+" dot.
- **Specification block**: large number + unit + label, with an optional 2px vertical rule between two blocks.
- **Price trio**: the promo price largest; the regular price on the same baseline with a strikethrough, one step down in colour; the promotion dates and conditions on their own line at the smallest size.

## Brand rules

- When brand rules exist, place the logo according to them first (position, clear space, minimum size). When no official logo is provided, record "not provided"; a clearly labelled wordmark placeholder is allowed but must never be called the official logo.
- Never stretch, redraw, recolour, outline, or add glow to a logo; only a monochrome scene may use an officially supplied monochrome version.
- The font, tracking, and capitalisation of a wordmark must match the brand; do not arbitrarily switch the English edition to all caps.
- Official fonts, brand colours, and forbidden elements must be confirmed by a human at H1 and written into the Project Style Constraint Record; the fonts and colours listed here are candidate suggestions only.
- The AI's visual keywords, typography strategy, palette, and layout must be frozen by a human at H2; suggestions made before H2 do not constitute project style constraints.
- When no official fonts or palette are provided, record "not provided"; the fonts, colours, and templates in this file are candidate proposals only.

## Scope of product hero images versus promo KVs

- This skill's currently validated scope is bilingual CN/EN 4:5 (default) or the 16:9 PNG confirmed at H1; other ratios are not yet validated. Promotion fields are used only when the task involves one and they have been verified.
- Product hero images must still be checked against each target platform's rules on clear space, text, background, ratio, and forbidden elements; never claim that the two renders can go live as-is on every platform.
- The final hero image for a real product must use an approved, inspectable product reference image or original product pixels. Without a reliable basis, produce planning only or an explicitly labelled non-fidelity layout concept, and never call a product reconstructed from a text description "product-faithful".

## Common issues

- Text sits on a key product detail → move the text block, or deepen the scrim there; do not shrink the product to make room.
- Text is swallowed by photographic texture or tonal contrast → first adjust the text area or local brightness, then support it with a soft scrim/gradient; avoid unnecessary hard-edged rectangles.
- The product-to-podium relationship is not credible → check the scene, the product's resting point, perspective, and lighting first, then the contact shadow; never alter the real product's structure to accommodate the base image.
- Too much information → cut to one headline + ≤3 selling points + one price block + one date line first, and move the rest to the detail page.
- A Chinese headline longer than 14 characters → split it into two sentences: the headline gives the value, the subtitle gives the qualifier.
- Type is compressed by more than 40% → the box is too small or the copy too long; change the copy or the skeleton instead of forcing it.
