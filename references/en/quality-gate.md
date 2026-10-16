# Delivery acceptance checklist

## Technical QA (not human approval)

```bash
python scripts/verify_kv.py --cn work/render/KV-CN-4x5.png --en work/render/KV-EN-4x5.png \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json --expected-width 1200 --expected-height 1500

# Mandatory when the client supplied a bilingual content master table
python scripts/check_copy.py --master work/brief/content-master.json \
    --spec-cn work/spec/kv-cn.json --spec-en work/spec/kv-en.json
```

For 16:9, change the file names to `KV-*-16x9.png` and the expected width/height to the H1-approved values (1920×1080 suggested); when rendering with `--scale`, pass the same multiplier for both editions to QA. A non-zero exit code means a rework.

What the script checks: the files exist, are PNG, match the spec and the explicitly supplied H1 dimensions at 4:5/16:9, have a shortest side ≥1000px, are not a flat colour, keep text boxes inside the canvas and actually drawn, declare matching sizes/base images across CN and EN without reusing one file for both, and reject an explicit `stretch` on image layers and the base image.

The explicit arguments must come from a genuine H1 approval record; the script itself cannot verify that an approval is real, that the base images really are the same picture, or that product assets were not pre-stretched or unreasonably cropped — compare the source images against the render by eye. It also does not verify copy semantics, facts, translation, or marketing claims; exit code 0 does not mean visual or commercial acceptance.

`check_copy.py` compares the content master item by item: whether every piece of information in the master made it into the corresponding language edition, and whether the English edition still contains Chinese. When master completeness is a client hard requirement, there must be zero omissions. Verify prices, promotion dates, and conditions only when the task actually involves a promotion; when it does not, never add promotion fields just to satisfy a template.

## H3 preconditions and human review

Once technical QA is done, the AI may only submit H3 — it may not declare a formal delivery. The H3 submission package must contain the actual rendered full-size CN/EN images, thumbnails, the corresponding spec/base-image versions, the technical QA report, the issue list, the approved product-reference comparison, the support-contact and contact-shadow checks, the photography/illustration medium-consistency check, and promotion fact sources where applicable. End the reply after submitting and wait for a new user message.

H3 must be confirmed by a human for product fidelity, composition and product prominence, text hierarchy, legibility, real scene/contact relationships, brand hard constraints, and cross-edition factual consistency. The decision can only be `Approved`, `Changes requested`, or `Returned`; there must be an explicit user message bound to the submitted actual image version and approved scope, otherwise it is `Pending` and nothing enters `outputs/`. An `Approved` the model writes into the brief, a report, or the delivery notes is not approval evidence.

After an H3 `Changes requested`, the next submission package adds a short rework log stating, item by item:

- `Issue`: the specific problem the user raised and the affected area;
- `Correction`: the local fix made this round and where it belongs (base image/product position, contact shadow, local blending, or text support);
- `Preserved`: the approved design elements retained (product reference, skeleton, cross-edition relationship, factual copy, and so on);
- `Recheck`: the full-size images and thumbnails re-inspected after the rework, plus the risks that still need human confirmation.

Rework addresses the scene, product position, and support relationship first, then the contact shadow and local blending; never solve a scene problem by altering the real product structure. After reworking you must inspect both the affected area at full size and the whole thumbnail, confirming the local fix did not create new hierarchy, cropping, contrast, or cross-edition consistency problems.

- `Changes requested`: return to the base image/product composite or the spec/render stage according to where the problem belongs, redo technical QA, and submit H3 again.
- `Returned`: return to steps 3–4 when the direction or facts do not hold, and to steps 1–2 when the evidence has become invalid.
- When the product is visibly detached from the intended support surface, the contact shadow does not hold, the product looks like it floats, or a real photographic product clashes with an illustrated scene without explicit H2 approval of mixed media, mark it `COMMERCIAL LAYOUT REQUIRES REVISION` and do not submit H3.
- Only when the next turn brings an explicit H3 `Approved` message bound to the matching actual image version may the render and delivery notes enter `outputs/`; all other candidates and reports stay in `work/render/`.

## Then walk the images item by item (what scripts cannot check)

**Specification**

- [ ] One Chinese edition and one English edition, named as specified
- [ ] Actual width/height/orientation/ratio equal the H1-approved Canvas Specification; 4:5 defaults to 1200×1500 and 16:9 is suggested at 1920×1080; CN and EN match
- [ ] The safe area follows the current canvas and platform (a 60px outer margin for the 1200-wide vertical reference), with no elements accidentally touching the edge or bleeding

**Information hierarchy**

- [ ] Within 3 seconds a viewer can say what this image is selling
- [ ] The main headline carries exactly one core value and is the largest type in the image
- [ ] The main headline is enlarged enough to hold the image; when the task involves a promotion the price is clearly presented too; where it overlaps the product, the covered height is ≤ 1/4 of the character height and the keyword stays recognisable
- [ ] Whether a CTA/call to action exists follows the actual marketing goal; when present a button is not mandatory and its visual weight must not outweigh the headline, product, or price; when not needed it is completely absent (both the text layer and the underline layer deleted)
- [ ] At most three supporting selling points, each no longer than two lines
- [ ] At most four hierarchy levels; when the task involves a promotion, the price and promotion dates are instantly legible
- [ ] No type size shrunk to illegibility just to fit more information in
- [ ] Small information text is enlarged and bolded: body ≥30px, labels ≥24px, weight Bold/Medium (1200-wide baseline)

**Subject and picture**

- [ ] Product share of frame and prominence match the H2-approved skeleton suggestions and the communication goal
- [ ] Where the product stands on a podium, water, or another support surface, there is a contact shadow/reflection matching the real support relationship; support is never invented just because a generic template asks for it
- [ ] An off-centre or centred product has an H2-approved compositional reason, and the relationship between the text columns and the product is clear
- [ ] The bottom prop band and the product's resting point follow the H2-approved layout and the real support surface, with no fixed 1/5 or fixed height line used as the pass condition
- [ ] The product base genuinely contacts the support surface; no visible floating gap
- [ ] The contact shadow/reflection fits the actual contact relationship and is not a decorative shadow detached from the product or podium
- [ ] A real photographic product is consistent with the scene medium; when a photographic product obviously clashes with illustration or procedural props, either H2 has explicitly approved mixed media or it has been reworked
- [ ] The two text columns are not covered by the product outline (check the text block edges line by line)
- [ ] The product is complete, not malformed, and no key structure is cropped
- [ ] Compare against the approved original to confirm the product's proportions are preserved and nothing was cropped unreasonably; the technical script can only reject an explicit `stretch` on an image layer or base image, and cannot prove the source was not deformed beforehand
- [ ] The product is the visual centre of gravity, with an area and position matching the chosen skeleton
- [ ] No text sits on a key product detail
- [ ] Every text area has sufficient background contrast (body ≥4.5:1); complex backgrounds use continuous local brightness adjustment, a soft mask, or a gradient, with no unnecessary hard-edged rectangles
- [ ] Text on a gradient never straddles a light/dark boundary: light type stays entirely in the dark zone and dark type entirely on the light surface zone
- [ ] The base image has no pseudo-text, no third-party watermark, and no platform badge
- [ ] The final hero image for a real product rests on an H1/H2-approved, inspectable product reference; images without a reliable basis are explicitly labelled as planning or non-fidelity concepts
- [ ] Product outline, colour, material, logo, and key structure match the approved reference, with no real product reconstructed or invented from a text description
- [ ] The real scene relationship among product, surface, shadow, reflection, and light is credible: the actual contact line, support-surface perspective, light direction, and shadow softness agree, and it does not pass merely because a script or the coordinates line up

**Brand**

- [ ] Logo position, proportion, and clear space follow the brand rules, with no stretching or recolouring
- [ ] Brand colours and fonts match the rules
- [ ] Badge content is a verified hard commitment

**Copy and facts**

- [ ] Every item of the content master entered the corresponding language edition (zero omissions)
- [ ] Items the user confirmed for removal are registered in the master's `waived` list (`check_copy.py` reports them as "waived")
- [ ] When the task involves a promotion: price, struck-through price, and final-price conditions are correct and consistent
- [ ] When the task involves a promotion: the promotion dates match the backend, including the year or a cutoff time
- [ ] No typos, no stray spaces, no mixing of full-width and half-width characters
- [ ] No prohibited superlatives, no invented sales figures, certifications, or performance claims
- [ ] The English edition has no leftover Chinese, no Chinglish, and localised units and date formats
- [ ] The facts in the Chinese and English editions are exactly the same

**Paired delivery**

- [ ] Both editions use the same base image and the same skeleton
- [ ] Side by side they read as one set of material, not two different designs
- [ ] The English edition is not a word-for-word translation of the Chinese

**Files**

- [ ] Before H3, candidates, previews, and reports live only in `work/render/`
- [ ] `outputs/` contains only H3-approved deliverables whose version matches, with no intermediate drafts
- [ ] `work/spec/*.json` are the specs that produced the final images
- [ ] The delivery notes state the audience, proposition, evidence sources, promotion price and date sources where applicable, and the H1/H2/H3 decisions and result versions
- [ ] Every H1/H2/H3 `Approved` has corresponding user message evidence; a model-authored approval record cannot replace a user message

## Common rework causes

| Symptom | Root cause | Fix |
| --- | --- | --- |
| Tofu boxes / rectangles in the render | A font without the needed glyphs | Use the `cn` font family, or let `pick_family` switch automatically (already built into the script) |
| The price is unreadable after the strikethrough | The strikethrough matches the price colour and is too thick | Step the strikethrough colour down one level and keep the thickness ≤ 6% of the value size |
| Copy is cropped | The box is too small, or an anchor/leader line falls outside the canvas | Change the box, change the anchor, or shorten the copy |
| Text is illegible on a complex background | Background texture/tonality crosses the text, or the support layer is too hard | Adjust the text area or local brightness first, then support it with a soft scrim/gradient; avoid unnecessary hard-edged rectangles, and re-inspect at full size and as a thumbnail |
| The product looks like it floats | Only coordinates were aligned; the contact line, surface perspective, and light were never checked | Check the scene and product position first, then fix the contact shadow's position, softness, and direction; never alter the product structure |
| The shadow looks like a decorative ellipse | Its width/hardness ignores the product footprint, or it does not hug the base | Make the darkest area hug the actual contact line, narrow it to the base outline, and soften it outward; do not add a reflection on a non-reflective material |
| A photographic product clashes with the scene style | A photographic product composited onto illustration/flat props without H2 approval of mixed media | Rework the base image or props to unify material, lighting, and depth of field; do not mask it with heavier shadows |
| The two editions do not look like a set | The English edition changed the skeleton or base image | Return to one set of coordinates and change only the copy |
| Blurry after printing or scaling up | A bitmap was upscaled | Re-render with `--scale` instead of stretching the exported PNG |
| The listing was rejected | Prohibited superlatives, promotion wording, or a missing price basis | Clean it item by item against `references/en/compliance-and-claims.md` |
