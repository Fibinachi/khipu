# Khipu Document Types — File-Type Analysis

**Date:** 2026-10-11
**Corpus:** 593 non-funerary khipu (26 Leymebamba/burial excluded; 17 blank stubs excluded from typing)
**Theoretical frame:** Khipu are file types — header (primary cord), body (pendants), physical EOF.
**Method:** 5 unsupervised clusters (khipu-clusters-2026-10-11.csv) + header/body specs from primary_cord and cord tables + published anchors (Santa census, Inkawasi warehouse).

## A revision to the file-type frame

The data revises the naive "magic-number header" version of the theory:

- **The header carries allocation, not type identity.** Primary cord length correlates with pendant count (r=0.67, n=597), but primary cord color, fiber, termination, and beginning codes overlap heavily across all types (W/AB/MB everywhere; K-termination and T-beginning dominant in every cluster). There is no color or construction signature that identifies the document type.
- **Type identity lives in the body structure** — depth, cord-grouping conventions, value scale, color-group regularity.
- Better analogy: **pre-sized blank + structural template**, not magic-number header. The maker cuts the cord to fit the expected file (allocation metadata), then fills a conventional body layout. The "file type" is the body template.
- **EOF is physical** — no terminator structures found; the file ends where the cord ends.

---

## Type 1 — Census Register (paired color-group format)

| Aspect | Spec |
|---|---|
| **Cluster** | census_format_paired, n=250 (largest family) |
| **Header** | Short primary cord (median 38, IQR 25–54). Colors: W (52), AB (29), MB (13) — unmarked/plain palette. K-termination / T-beginning dominant. Cotton fiber. |
| **Body** | ~20 L1 cords (IQR 11–35), shallow (max level 1–2). **Fixed 2-cord color groups** (62% consistency). Values small: median 2, max ~22, 99% < 20. ~29% zeros (sparse fields). Subsidiaries rare (median 0). |
| **Function** | Population/tribute register. The Santa format: each color-group = one person/household; cord positions within group = fields (tribute assessed, components, status). Anchored by 6 published Santa quipu (Medrano & Urton 2018) whose position-1 values decode to published constants. |
| **Geography** | Empire-wide: Puruchuco, South/Central Coast, Nazca, Pachacamac, Ica. Not Santa-specific. |
| **Confidence** | **High** — published anchor + structural replication across 250 specimens. |
| **Key evidence** | Santa decoder validation (1000270→9, 1000271→4); 2-cord group regularity; small-value profile; moiety encoding (recto/verso) documented in literature. |
| **Open questions** | Field labels for positions 2–6 (Medrano & Urton 2018 paywalled); whether the 133rd group on Santa quipu is a header block; the composite structure of 1000274 (internal R/V flip). |

---

## Type 2 — Bulk Tally / Summary Sheet (large-value flat) — *undescribed type*

| Aspect | Spec |
|---|---|
| **Cluster** | large_value_flat, n=78 |
| **Header** | Primary cord median 44 (IQR 28–62) — slightly longer than census. Colors: W (16), AB (9), YB (5) — plain palette like census. Same K/T construction idiom. |
| **Body** | ~15 L1 cords (IQR 7–30), shallow (max level 1–2). **No color grouping** (19% compounds, no fixed pairs). Values warehouse-scale: median 80, max ~981, only 27% < 20. **15.5% of values divisible by 10** (vs 2.4% census, 5.8% deep-grouped) — rounding suggests estimation/aggregation, not precise counts. |
| **Function** | **Proposed: bulk commodity tallies or summary sheets.** Flat (no hierarchy) + large values + no color grouping + round-number tendency = single-level aggregate records. Candidates: (a) warehouse intake totals by commodity; (b) tribute summaries rolled up by category; (c) regional rollup sheets consolidating multiple registers. The absence of color grouping is diagnostic — there are no entities to label, only amounts to total. |
| **Geography** | Mostly Pachacamac/Ica. |
| **Confidence** | **Medium** — structural coherence is real (tightest value profile of any cluster); function is inferred, not anchored. |
| **Key evidence** | Value scale (100× census medians) with census-like flatness; round-number enrichment; no color-group idiom; 67/78 were "unclassified" under the old scheme — the type the two-bucket model missed. |
| **Open questions** | Archaeological context for Pachacamac/Ica specimens (do they come from storage contexts?); whether values match known tribute quotas or warehouse capacities; whether these are summaries *of* Type 3 ledgers (same site, flat rollup of a deep record?). |

---

## Type 3 — Custodial Warehouse Ledger (deep hierarchical, color-grouped)

| Aspect | Spec |
|---|---|
| **Cluster** | deep_hierarchical_grouped, n=76 |
| **Header** | Longest primary cords (median 72, IQR 52–110, max 514). Colors: AB (10), W (9), MB (5). Same construction idiom. |
| **Body** | ~97 L1 cords (IQR 56–146), ~57 subsidiaries, depth 3–4 (46% subsidiary rate). Large values (max ~1444). **Fixed 2-cord color groups (66%)** — the census idiom inside a warehouse document. 7-color palettes. |
| **Function** | **Multi-party custodial inventory.** House stock on main cords; other parties' goods riding as subsidiaries, distinguished by color. Established by: (a) 69.1% subsidiary color contrast vs parent (p<0.001, rider-hypothesis-test.md); (b) value independence, r=0.14 — no summation; (c) Urton & Chu 2015 anchors (10 of the 18 high-confidence warehouse quipu sit here). The warehouse was a custodian, not just an owner — the Inca equivalent of a village granary holding many farmers' grain. |
| **Geography** | Inkawasi anchors; others scattered. |
| **Confidence** | **High** for structure; **medium-high** for the custodial function (anchored + statistically tested, but "whose goods" is undetermined — tribute, deposit, or inter-institutional transfer all fit). |
| **Key evidence** | Rider tests (contrast, independence); Urton & Chu commodity ground truth; repeating tax/deduction values (15/10/47/208) in publication; recto/verso opposition noted in the paper. |
| **Open questions** | Compound semantics (enriched with depth but "origin" unproven, 50/50); white subsidiaries under colored parents (50 cases — state riders?); why chili shows ~50% contrast vs ~90% for peanut/beans; full quantities unrecoverable (NUM_TURNS missing). **Caution:** 5 Inkawasi quipu fall in the census cluster and 3 in deep-sparse — "from the warehouse ≠ is a warehouse inventory." The type narrows to ~10 quipu, not 18. |

---

## Type 4 — Sparse Working Ledger (deep_sparse_mixed) — *resists clean typing*

| Aspect | Spec |
|---|---|
| **Cluster** | deep_sparse_mixed, n=172 |
| **Header** | Primary cord median 58 (IQR 35–84). Unremarkable; same idiom. |
| **Body** | ~60 L1 cords, ~9 subsidiaries, max level 2–3. **56% zeros.** Small nonzero values (median 0 overall, max ~83). 8–9 colors, no grouping. |
| **Subdivision probe** | Does not split cleanly. By zero-rate: ≥70% (53) / 40–70% (53) / <40% (66) — roughly thirds, no natural break. By max value: ≥500 (39) vs <100 (85) — continuous, not bimodal. Hi-zero group leans Incahuasi (11/53); lo-zero group is scattered (Pachacamac, Huaquerones, Santa, Nazca). |
| **Proposed reading** | **Not a fourth administrative type but a condition, not a kind.** Two hypotheses, both consistent with the data: (a) **Active working documents** — quipu still in use, with unwritten fields (the 56% zeros are blank cells in a live ledger, not missing data); (b) **Degraded specimens** — damaged or partially recorded quipu from Types 1–3 that lost their diagnostic structure. The Incahuasi-leaning hi-zero subgroup favors (b) for warehouse types; the scattered lo-zero subgroup favors (a) or census degradation. |
| **Confidence** | **Low** for any single function; **medium** that this is "state of the document" rather than "type of document." |
| **Key evidence** | Failure to subdivide on any structural axis; provenance mix; zero-rate continuum. |
| **Open questions** | Physical examination could resolve this fast: are the zero-value cords truly empty (never knotted → working document) or damaged (broken/missing knots → degraded)? The database cannot distinguish. |

---

## Excluded: Blank stubs (n=17)

Cords recorded, zero knots, zero colors. Fifteen are consecutive IDs from the Dallas Museum of Art with no provenance — likely incomplete data entry, not blank forms. Cannot distinguish "no knots exist" from "knots not entered." Excluded from typing; must be filtered from value analyses.

---

## Summary table

| Type | n | Depth | Values | Color groups | Header (primary) | Function | Confidence |
|---|---|---|---|---|---|---|---|
| 1. Census register | 250 | 1–2 | tiny (med 2) | fixed pairs | short (38) | population/tribute | High |
| 2. Bulk tally | 78 | 1–2 | large (med 80) | none | short (44) | summaries/aggregates | Medium |
| 3. Custodial ledger | 76 | 3–4 | large | fixed pairs | long (72) | multi-party inventory | Med-High |
| 4. Sparse working | 172 | 2–3 | small/sparse | none | medium (58) | active or degraded | Low |

## Cross-cutting findings

1. **The color-group idiom crosses types** (Types 1 and 3). It is a pan-administrative record-keeping convention — fixed N-cord groups per entity — not a census-specific feature. The Santa 6-block is one parameterization; warehouse 2-groups are another.
2. **White is local, structure is general.** White-as-triage holds at Inkawasi only; mains > subsidiaries in value holds everywhere (white-theory-test.md).
3. **Red is not administrative.** Median 0% in every cluster; a funerary phenomenon.
4. **The old two-bucket scheme missed Type 2 entirely** and misassigned 18 funerary quipu as inventory.

## What would strengthen or break this typology

- **Physical re-examination** of Inkawasi quipu for NUM_TURNS (unlocks full values; tests Type 3 function quantitatively).
- **Archaeological context** for Type 2 specimens (Pachacamac/Ica) — storage vs residential vs burial context decides between tally/summary hypotheses.
- **Section-level analysis** within Type 1 (the 1000274 composite shows single quipu can contain multiple documents).
- **The 133rd-group problem** on Santa quipu — if it's a header block, the file-type frame gains a within-body header spec.
