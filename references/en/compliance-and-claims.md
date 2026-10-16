# Compliance and factual boundaries

A hero image is marketing material, and every number on it is a commitment. There is one rule: **write nothing beyond what the user supplied and what has been verified.**

Platform rules, prohibited-word lists, and category restrictions all change. Where a specific platform's review standard is involved, check that platform's latest official rules first; if you cannot find them, take the conservative route and mark it "not verified" in the delivery notes.

## Never invent

- Prices, discounts, final-price conditions, promotion start and end times
- Sales volume, rankings, positive-review rates, repurchase rates, buyer counts
- Test report numbers, certification names, patent numbers, awards
- Efficacy, therapeutic effects, safety conclusions, promises about who a product suits
- Material content, country of origin, brand licensing relationships

If it is not in the material, either drop it or state it as an objective attribute ("glass bottle body") — never upgrade it into a performance promise ("keeps fresh for 30 days").

## Prohibited superlatives (Chinese copy)

Remove or rewrite into verifiable language any of the following on a hero image:

最, 最佳, 最好, 最优, 最强, 第一, 首个, 唯一, 顶级, 极致, 绝对, 100%, 全网最低, 国家级, 世界级, 王牌, 冠军, 史无前例, 绝无仅有, 永久, 终生, 根治, 治愈, 零风险, 包治, 万能.

Replacements: turn absolute judgements into facts and conditions — "passed test XX (report no. XXX)", "3-year warranty on the whole unit", "8 hours of runtime per charge (laboratory data)".

## Price and promotion

- A struck-through (regular) price needs a basis (historical selling price, tag price, official list price); without one, no struck-through price at all.
- A "final price" must state its conditions: after coupon, after bundle discount, limited-time flash sale — the condition text appears together with the price.
- Promotion dates must be stated and must match the backend; include the year across a year boundary, and give an explicit cutoff where the time zone matters (for example `October 31, 24:00`).
- Gifts state the quantity and conditions ("buy 2, get 1 free"), never unverifiable phrasing such as "while stocks last".

## Category sensitivities

| Category | Extra care needed |
| --- | --- |
| Food / supplements | No efficacy, treatment, or drug-replacement claims; "0 additives" needs a basis |
| Cosmetics / personal care | No medical-effect claims; ingredient and efficacy wording must match the filing |
| Medical devices / health | Qualification and filing information required; do not overstate the scope of application |
| Maternal, baby, and children | Age and safety warnings must be accurate; never promise absolute safety |
| Appliances / 3C | Specifications must match the manual; energy ratings and certifications need reports |
| Cross-border | Target-market language and regulatory differences; avoid unsupported phrasings such as FDA approved or clinically proven |

## Platform differences (directional reminders — verify against the latest rules)

- Taobao / Tmall: hero images may not be packed with text like a noticeboard, may not use non-official authorisation marks, and may not exaggerate promotions; white-background hero images and marketing hero images serve different purposes.
- JD: hero images carry extra limits on text area and on how promotions are displayed.
- Pinduoduo: price and promotion wording must match the campaign; beware the risk of comparative phrasings like "lowest price".
- Douyin Shop: short-video and livestream covers follow different rules from product hero images; keep spoken promises consistent with the images.
- Amazon / Shopify / TikTok Shop: hero images usually disallow promotional text and badges, so marketing KVs belong in A+, secondary listing images, or ad creative; avoid unsupported certifications and comparative/superlative claims.

## Language compliance (English edition)

- Do not use unsupported claims such as `best`, `No.1`, `world's leading`, `guaranteed`, or `100%`.
- `FDA approved`, `clinically proven`, `medical grade` and the like require verifiable evidence.
- State the term and conditions for warranties and returns: `3-year warranty (registration required)` rather than `lifetime guarantee`.

## How to handle an uncertain claim

Work through uncertain wording in this order:

1. A basis can be found in the user's material → keep it and record the source in the delivery notes.
2. No basis can be found → rewrite it as an objective attribute or delete it.
3. Deleting it leaves too little information → write it into the delivery notes as an open item; never fill the gap with vague wording.

The "Open items / risks" section of the delivery notes is mandatory — do not omit it.

## Image asset licensing

- Base images and props may only come from: the client's own photography / clearly licensed stock assets / this skill's own output (procedural or generated).
- Images carrying a platform watermark (Xiaohongshu, Douyin, ZCOOL, and so on) or of unknown origin **may never be used as a delivery base image**; removing the watermark by painting, patching, or content-aware fill is equally forbidden — that circumvents attribution, and the risk outweighs the benefit.
- When a reference image's composition is worth keeping, the right move is to **reframe so that it falls outside the picture** (`build_scene_from_photo.py`), or to switch to an equivalent licensed asset or a generated remake, and to state the asset source and licence status in the delivery notes.
- A generated base image must be marked "AI generated" in the delivery notes, and the commercial terms of the service used must be confirmed.
