# Tag Search Report: Finding 1000331's Filing Cabinet

**Date:** 2026-10-11
**Question:** Do other khipu use 1000331's 23-codepoint tag vocabulary? Same shorthand,
same office, more documents?

## Method

Computed full cord signatures `(color1, color2, dominant_knot_type, dominant_twist)`
for all 612 khipu (54,403 cords). Scored overlap with 1000331's signatures via Jaccard
+ weighted overlap, plus three structural markers: AB+BG compound terminator, WWW
triplet, BG two-type knot split (E/Z vs L/S).

**Caveat:** Compound-color cords have multiple color rows; "primary" color depends on
row order, so signature counts vary slightly between runs (±1–4). Results are robust
to this for the structural markers.

## Headline: 4 other khipu share the punctuation system, but not the tag meanings

Five khipu (including 1000331) have all three structural markers. They share a
**scribal formatting convention**, not a shared lexicon:

| Khipu | Provenance | Cords | Shared vocab | Note |
|---|---|---|---|---|
| 1000331 | — (Museo Amano) | 171 | 100% (ref) | 13 sections, MB boundary labels |
| 1000396 | Huaura Valley | 221 | 63% | Closest match; 4 sections; MB not a label |
| 1000507 | Pachacamac | 132 | 52% | Markers present, different organization |
| 1000321 | — (Radicati) | 1,227 | 73% of cords | Filing cabinet; shared tags are a subset |
| 1000659 | Armatambo | 56 | 27% | Same punctuation, different vocabulary |

## Key findings

1. **AB+BG as compound section terminator is a real convention** — 43/612 khipu (7%).
   Not unique to 1000331, but distinctive.

2. **BG two-type split is very rare** — 5/612 khipu (0.8%). The E/Z-knotted vs L/S-knotted
   BG terminator appears to be a binary section-mode flag. This is the strongest shared
   signal and the best lead for further work.

3. **Tag roles don't transfer.** MB labels sections only in 1000331 (68% near markers
   vs 0–15% elsewhere). Carrier proportions differ in every khipu. The abbreviations
   are document-specific.

4. **1000321 is probably a filing cabinet** containing 1000331-like material among a
   much larger vocabulary (144 signatures). Worth sectional analysis.

5. **1000659 proves punctuation ≠ vocabulary.** Same three markers, but only 27%
   weighted overlap — the formatting convention traveled without the tag meanings.

## The filing cabinet: not found

We did not find 1000331's office. We found its **scribal tradition** — a formatting
convention (AB+BG terminators, two-mode BG split) shared across at least 5 khipu from
Huaura Valley, Pachacamac, Armatambo, and unknown provenances. But shared punctuation
without shared tag roles means we cannot triangulate tag meanings.

## What's needed

Two khipu from the **same provenance** sharing **both** punctuation and tag roles.
Huaura Valley / Lima area is the search zone. The BG mode-split (E/Z vs L/S sections)
is the most testable hypothesis: do the two modes differ in content?

## Deliverables

- [signature_profiles.csv](sandbox://workspace/quipu-analysis/tag-search/signature_profiles.csv) — per-khipu signature vocabularies (612 khipu)
- [overlap_scores.csv](sandbox://workspace/quipu-analysis/tag-search/overlap_scores.csv) — Jaccard, weighted overlap, marker flags, provenance
- [top_candidates.md](sandbox://workspace/quipu-analysis/tag-search/top_candidates.md) — the 5 all-marker khipu in detail
- [tag_concordance.csv](sandbox://workspace/quipu-analysis/tag-search/tag_concordance.csv) — shared-signature contexts across the 5
- [triangulation.md](sandbox://workspace/quipu-analysis/tag-search/triangulation.md) — role comparison and meaning hypotheses
- Scripts: `build_profiles.py`, `investigate.py`, `triangulate.py`
- Reference: `ref_1000331_signatures.json`
