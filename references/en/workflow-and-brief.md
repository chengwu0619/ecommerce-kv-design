# Workflow and Brief

## Working directories (fixed convention)

All artifacts live under the project root. Before H3, candidate renders, previews, and reports go only into `work/render/`; only H3-approved renders whose version matches the approved one, together with the delivery notes, enter `outputs/`.

```text
<project root>/
├─ outputs/                        final deliverables (only what is here goes to the client)
│  ├─ KV-CN-4x5.png                H3-approved Chinese hero image
│  ├─ KV-EN-4x5.png                H3-approved English hero image
│  ├─ KV-CN-16x9.png               only when H1 approved the 16:9 canvas
│  ├─ KV-EN-16x9.png               never overwrite an existing render at another ratio
│  └─ 交付说明.md                   audience / proposition / evidence / price & schedule sources / approved versions
└─ work/
   ├─ input/                       raw client material: packshots, photos, logo, certificates, promo-rule screenshots
   ├─ brief/kv-brief.md            structured brief (single source of truth for requirements)
   ├─ spec/kv-cn.json              Chinese layout spec (single source of truth for layout)
   ├─ spec/kv-en.json              English layout spec (same coordinates as CN, copy swapped only)
   ├─ base/                        base image: base-cn.png (photo / cut-out composite / generated) plus optional detail shots
   └─ render/                      iterations, comparison sheets, report.json
```

Rules:

- The spec JSON is the single source of truth. Changing an image = change the spec and re-render; never edit the PNG directly or by hand.
- Both language editions share the H1-approved ratio, pixel size, base image, and core skeleton. The English edition may change text-box width, type size, and line breaks, but not the canvas or the product proportions.
- Base images always live in `work/base/` and never enter `outputs/`.

For an English-language project you may name the delivery notes `outputs/delivery-notes.md` instead of `outputs/交付说明.md`; pick one name per project and use it consistently.

## Seven-step workflow (executed across turns)

The seven steps span multiple replies. In any single turn, go no further than the next Human Gate that has not yet received genuine user approval; once you submit the material for that gate you must end the reply and wait for a new user message. An `Approved` that the model writes into the brief, a report, or the delivery notes is not approval evidence, and a general "please complete the whole task" is not advance approval either.

1. **Set up the project and analyse the facts**: create the directories and put the client's material in `work/input/`; inspect product reference images, brand assets, facts, and copy. When a source is an image, look at its actual content before citing it — never guess from the file name.
2. **Write the brief, submit it for H1 input-baseline confirmation, and stop the turn**: include the Reference/Facts Inventory, the product-fidelity mode, the Project Style Constraint Record, and a first draft of the Canvas Specification. Vertical 4:5 is the default; when the user explicitly asks for 16:9 you must not revert to vertical, and when it conflicts with a hard limit of the target platform, raise it for confirmation at H1. Verify prices and schedules only when the task actually involves a promotion. You may not enter step 3 without user approval bound to that submitted version.
3. **Fix the audience and the single proposition**: state in one sentence "who it is for / in what situation / what it solves / why buy now". The main headline carries exactly one core value, with at most three supporting selling points; build the communication hierarchy inside the H1 constraints.
4. **Propose creative directions, submit them for H2 selection/freeze, and stop the turn**: only after H1 is approved. By default, submit three substantially different options A, B, C, each composed independently for the approved canvas, plus a short comparison; weigh centre of gravity, text areas, support surfaces, negative space, information hierarchy, and reading path for the actual orientation, and never stretch or crop a vertical skeleton into a landscape layout. After submitting, keep H2 `Pending`; no production work beyond concept previews the user explicitly asked for.
5. **Decide the base image and build it**: only after H2 is approved. Approved photography / product references come first; with a product shot but no scene, cut out the product and composite it onto the canvas; AI generation may only supply a scene base with no product and no text. Without a reliable product reference, output planning only or an explicitly labelled non-fidelity layout concept (see `references/en/photo-base.md`). Both language editions share one base image.
6. **Write the specs and render**: rework an existing template for vertical, or lay out landscape independently from `landscape-concept-*.json` or the approved landscape direction and replace every placeholder. CN and EN keep the same size, base image, skeleton, and `--scale`. Candidate renders go only into `work/render/`, and you must open the actual rendered image and look at it.
7. **Run technical QA, submit the real renders for H3 review, and stop the turn**: run `scripts/verify_kv.py` and walk through `references/en/quality-gate.md` line by line, then let a human review the actual CN/EN renders. If the support contact, contact shadow, or medium relationship does not hold, rework first — never submit H3 on top of it. End the reply after submitting H3; only when the next turn brings explicit user approval bound to that actual image version may you write the delivery notes and place files in `outputs/`.

## Human Gate record contract

All three gates must be written into the existing brief, visual strategy document, rendered-QA notes, or delivery notes, recording at least: `Submitted version`, `User message evidence`, `Approved scope`, `Decision`, `Result version`, and date/decision maker where applicable. With no genuine user approval message, record `Pending` and do not proceed; AI technical QA, a script `PASS`, `READY`, or a model-authored `Approved` are never human approval.

### H1 Input-baseline confirmation

- AI submits: the material/facts/copy inventory, the status of product reference images and brand assets, whether a promotion is involved, the fidelity mode, gaps and conflicts, plus the first draft of the Project Style Constraint Record and the Canvas Specification; end the reply after submitting.
- Human confirms: available evidence, official fonts / brand colours / forbidden elements, essential product facts, and the task type, plus canvas purpose / target platform, ratio, pixel size, orientation, PNG, platform-specific extra limits, and the source of the specification.
- Decision: `Approved` / `Changes requested` / `Returned`; there must be an explicit user message bound to that submitted version and scope, otherwise it is `Pending` and you stop at step 2.
- Fallback: `Changes requested` returns to steps 1–2; `Returned` returns to step 1 and, if necessary, switches to planning mode.

### H2 Creative direction and project style freeze

- AI submits: by default all three creative options A/B/C plus a side-by-side comparison in one go, updating the candidate entries of the Style Constraint Record; you may recommend one with reasons, but you may not choose, freeze, or mark it `Approved` yourself. When the user explicitly asks for only one or two options, follow that; when the real constraints cannot support three sound options, explain why instead of inventing differences to fill the count. After submitting, the same reply must end with all four interaction entries, and the turn must end.
- Human confirms: approve one specific version of A/B/C, choose one and request local edits, combine strategies from different options, ask for a new proposal, or request a low-fidelity preview of all or some options. Global hard constraints and the H1 brand hard constraints always take precedence.
- Decision: `Approved` / `Changes requested` / `Returned`; the direction can only be frozen when the user, after seeing the submitted material, explicitly approves a specific option ID, version, and scope. "Please continue", "please complete the task", "generate something and let me see", a model-recorded approval, and "authorised to build a concept preview" are all not H2 `Approved`.
- Fallback: edits, combinations, and re-proposals are `Changes requested` and return to steps 3–4 to produce a new option ID/version that is submitted again; `Returned` goes back to steps 1–2. While H2 is `Pending`, generating a production background, a production render, or entering step 5 is forbidden, apart from concept previews that were explicitly requested.

#### Mandatory interaction format at the end of an H2 reply

Every time you submit H2 options, the reply must close with all four interaction entries below, not merely an approval entry for the option the AI recommends:

1. **Direct approval**: approve a specific option ID/version.
2. **Edit / combine / re-propose**: state the option ID/version to edit, the parts to combine, or ask for a new proposal.
3. **Mode A preview**: build low-fidelity layout sketches with local scripts, templates, and simple shapes; no online image generation.
4. **Mode B preview**: after explicit user authorisation, call the available image-generation tool to build a low-fidelity scene-atmosphere preview.

For both Mode A and Mode B, state clearly that the user may name only some options or preview all of them, that a preview is still part of the H2 decision stage, that authorising a preview is not formal approval, that H2 therefore stays `Pending`, and that production must not start early. By default no images are generated at all; only an explicit user request triggers them, and Mode B additionally needs explicit authorisation. Even after previews are delivered, the user must still send `Approved` against a specific option ID/version before the direction can be frozen.

Close with examples that can be copied verbatim, for example:

```text
Approved A-v1
Change the headline font of B-v1
Combine the composition of A-v1 with the information hierarchy of C-v1
Preview A-v1, B-v1, C-v1 with mode A
Authorise a mode B preview of B-v1
```

#### H2 option structure and side-by-side comparison

Use the same compact structure for every option so the user can compare them:

1. Option ID, version, and name.
2. Style keywords, core proposition, and target audience.
3. Visual skeleton, product position, and product share of frame.
4. Scene medium, real support surface, contact relationship, and light direction.
5. Chinese/English font candidates, primary and accent colours.
6. Information hierarchy for headline, selling points, price, and CTA; list only the fields the task actually needs and never add promotion fields just to fill a template.
7. Strengths, potential risks, and production feasibility.

The three options must differ substantially across several key dimensions — photographic vs. editorial strategy, visual skeleton, composition, scene, typography, palette, or information hierarchy — and not merely in colour, name, or decoration. Each one must respect the H1-confirmed product facts, brand hard constraints, asset licensing, product fidelity, and target-platform limits; the A–H skeletons are candidate resources only, so there is no requirement to use three fixed skeletons, nor to apply the same three-style set to every product. Follow the options with a short comparison table that names the main differences, the goals each suits, the risks, and the cost, then stop the reply and keep H2 `Pending`.

#### Selecting, editing, and freezing

- When the user directly approves an option, the approval message must point to the option ID and version; record `User message evidence`, the approved scope, and the resulting version, and only then freeze that direction.
- "Pick B but change the font" is an edit request, not approval of the original B; produce a new version of B and wait for confirmation again.
- When combining A's composition with C's typography, create a new combined option ID/version, spell out what is inherited and what changed, and submit H2 again.
- Production uses only the frozen option; never smuggle in an unselected candidate. Fine-tuning type size, spacing, and position inside the approved scope does not require reopening H2, but changing the core style, skeleton, typography strategy, or palette direction requires a new version and fresh approval.

#### Optional low-fidelity H2 concept previews

A preview is decision support inside H2 and does not create a new gate. By default none is generated; only an explicit user request that names the options to preview authorises one. The user may preview only part of A/B/C.

**Mode A: lightweight composition and style sketch**

- Prefer existing Python scripts, templates, or simple shapes; do not call an online image-generation model.
- May show product placeholders, colour blocks, text areas, visual centre of gravity, font candidates, palette, and scene placement. With an approved product reference image you may use the original; otherwise use only explicitly labelled product placeholder frames.
- Compares layout and style structure only, and claims no full photographic realism.

**Mode B: AI atmosphere concept preview**

- Call the available image-generation tool only after explicit Mode B authorisation; generate scene backgrounds with no product and no text only, and never reconstruct the real product, logo, or product structure.
- An approved real product asset may be composited onto that background to form a concept preview; full bilingual production is never triggered by default.

Both modes use the H1-approved canvas ratio and product facts. For landscape, Mode A may lay out text areas, product placeholders, support surfaces, and the option ID with simple shapes on the same 16:9 canvas in order to compare layouts, and may not stretch a vertical placeholder. Mode B should plan the scene at the approved ratio; if the tool only returns another size, reconstruct the empty scene sensibly rather than stretching the real product. Keep resolution, number of calls, and cost to the minimum needed for comparison, and add the option ID, version, and `CONCEPT / NOT FINAL` afterwards. Previews live only in `work/render/`, never in `outputs/` or H3; end the reply after showing them and keep H2 `Pending`. Authorising a preview is not approval.

If Mode B hits a permission error, an incompatible interface, or another service failure, stop retrying that failing path and report the cause and the work already done honestly, keeping the three proposals and H2 `Pending`. You may suggest switching to Mode A; without the user's consent you may not switch to stock photography, another generation service, or fabricated preview results. An unavailable external service neither means H2 passed nor means the options themselves failed.

### H3 Real-render review

- AI submits: the actual full-size CN/EN images and thumbnails, the corresponding spec/base-image versions, the technical QA report, the visual issue list, the product-reference comparison, the support-contact and shadow checks, the medium-consistency check, and promotion fact sources where applicable; end the reply after submitting.
- Human confirms: product fidelity, composition, product prominence, text hierarchy, legibility, real scene relationships, brand constraints, cross-edition factual consistency, and whether the images may enter `outputs/`.
- Decision: `Approved` / `Changes requested` / `Returned`; there must be an explicit user message bound to the actual image version and scope, otherwise it is `Pending` and the candidates stay in `work/render/`.
- Fallback: `Changes requested` returns to step 5 (base image/composite) or step 6 (spec/render); a detached support surface, a contact shadow that does not hold, or an unapproved photography/illustration medium clash must go back to steps 5–6. `Returned` goes back to steps 3–4, and to steps 1–2 when the facts or evidence have become invalid.

## Brief template

```markdown
# Hero Image Brief

## 1. Product
- Product name / model:
- Category and platform:
- Brand and brand rules:        # logo file, primary colour, fonts, forbidden colours, fixed badge position
- Product form, size, and weight:
- Material and finish:
- Product reference image ID / inspectable path:
- Product fidelity mode: `Reference-backed` / `Planning-only` / `Non-fidelity concept`

## 2. Target audience
- Audience profile:
- Usage occasion:
- Decision blockers (why they hesitate):
- The words they would search with:

## 3. Proposition and selling points
- Single core value (main headline):
- Supporting points 1 / 2 / 3 (each with its evidence source):
- Differentiation:              # the one thing that most sets it apart from similar products

## 4. Price and promotion
- Regular price / promo price / final price (with conditions):
- Basis for the struck-through price:
- Promotion start and end:
- Gifts, bundle discounts, limited quantities (with conditions):

## 5. Trust and credentials
- Test reports / certifications / patents / quality inspection (number and issuer):
- After-sales commitments (warranty / returns):

## 6. Assets
- Product photography (angles / resolution / commercial-use rights):
- Scene photography:
- Macro details:
- Whether bilingual editions and native-language review are needed:

## 7. Open items
- ...
```

## Canvas Specification (brief-level record, confirmed at H1)

| Field | H1 draft default / how it is confirmed |
| --- | --- |
| Purpose / target platform | State the actual purpose and platform; when unknown, record that it was not provided |
| ratio / width / height | Default `4:5` / `1200` / `1500`; when the user explicitly asks for landscape, propose `16:9` / `1920` / `1080`; other concrete sizes at the same supported ratio with a shortest side ≥1000px may also be confirmed |
| Orientation / format | Vertical or landscape, consistent with the ratio / PNG (RGB) |
| Platform-specific extra limits | Record each one; report conflicts at H1 and wait for confirmation rather than promising that the image can go live on every platform as-is |
| Specification source / user confirmation | Source, submitted version plus approval message evidence, scope, resulting version; anything without a genuine message stays `Pending` |

The H1-approved Canvas Specification is the common baseline for H2 proposals and previews, both spec files, QA, and H3 delivery. `verify_kv.py --expected-width ... --expected-height ...` only compares against numbers a human typed from the approval record; neither the spec itself nor a command-line argument proves that the user ever approved anything. Changing the canvas ratio or the platform limits reopens H1; proposals already submitted and versions already approved in existing projects do not change automatically because the skill was updated.

## 8. Project Style Constraint Record

Label every entry with source, category, status, and version; never write a candidate font or template as if it were a brand rule.

| Category | What is recorded | Source / authority | Status | Version |
| --- | --- | --- | --- | --- |
| Skill global hard constraints | Default 4:5, H1-selectable verified 16:9, bilingual editions, no invented facts, all text rendered from the spec, nothing in outputs before H3, and so on | This skill | Fixed | `skill-v1` |
| Confirmed brand hard constraints | Official fonts, brand colours, logo usage, forbidden elements, platform limits; explicitly record "not provided" for missing items | H1 human-confirmed brand material / user requirements | Frozen after H1 | `brand-v...` |
| AI style recommendations | Visual keywords, typography-strategy candidates, palette candidates, layout and skeleton suggestions per option | AI proposal | Every version is a candidate before H2; only the user-approved option/version freezes after H2 | `direction-[ID]-v...` |

H1 must confirm the official fonts, brand colours, and forbidden elements; H2 must record the approved option ID/version, the user message evidence, and the approved scope, and freeze that option's visual keywords, typography strategy, palette, and layout. Unselected options and concept previews are outside the freeze scope; existing fonts and visual templates are candidates only and are not imposed unless H1/H2 explicitly approve them.

## Gap handling rules

| Gap | Handling |
| --- | --- |
| The task involves a promotion but there is no price/schedule | Blocking item, you must ask; guessing is forbidden and "to be confirmed" cannot support a formal delivery |
| The task involves no promotion | Price/schedule is not required; never fill promotion fields just because a template has them |
| No evidence for a selling point | State objective product attributes only (material, dimensions, construction), no performance promises |
| No official logo | Record "not provided"; a clearly labelled wordmark placeholder is allowed, and the delivery notes must say it is not the official logo |
| No reliable product reference image | Planning only, or an explicitly labelled non-fidelity layout concept; a scene base with no product and no text may still be used for planning |
| Audience unclear | Infer from platform + category + price band, write it into the brief, and mark it "inferred" |
| Bilingual editions but the English information is missing | Localise and rewrite from the Chinese facts as the source of truth; add no new facts |
| The client supplied a bilingual content master table | Turn it into `work/brief/content-master.json` and, after rendering, verify zero omissions with `scripts/check_copy.py` |

## Delivery notes template

```markdown
# Delivery Notes

## Deliverables
- KV-CN-<4x5 or 16x9>.png: H3-approved version, PNG at the H1-approved size/ratio
- KV-EN-<same as above>.png: H3-approved PNG at the same size/ratio
- H3 approved scope / result version:

## Audience and proposition
- Audience:
- Single core value:
- Supporting selling points and evidence:

## Provenance of information
- Source of price and promotion dates:
- Source of credentials and commitments:

## Specifications and assets
- Canvas Specification: purpose / platform / ratio / width and height / orientation / PNG / extra limits / source / H1 approval message:
- Base image source (photographed / generated / placeholder):
- Basis for fonts and brand rules:
- Render spec files: work/spec/kv-cn.json, work/spec/kv-en.json

## Gate record
- H1 input baseline: user message evidence / decision / approved scope / result version:
- H2 direction and style freeze: user message evidence / decision / approved scope / result version:
- H3 real-render review: user message evidence / decision / approved scope / result version:

## Open items / risks
- ...
- Technical QA covers only what a script can check: format, dimensions, and copy placement. Product fidelity, composition, text hierarchy, legibility, and real scene relationships must be confirmed by a human at H3.
- `verify_kv.py` does not verify copy semantics, factual accuracy, translation quality, product-to-support contact, or the photography/illustration medium relationship.
```
