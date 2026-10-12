# Corpus-wide Form Template Extraction

**Date:** 2026-10-12
**Method:** Generalized from 1000344 (rows 2-7 as six instances of one form with constants BL=66, BY=32, MB=33, BY=12 and one variable field).

## Headline

**Templates are instance-specific, not curriculum-standardized.** 113 khipu show strong template structure (rows repeating with >30% constant positions), but all 113 templates are unique — at every level of abstraction tested. The "curriculum" lives at the document-type level (census, warehouse, etc.), not the form level. Each office/scribe laid out their own template.

## Pipeline

1. **Bulk decode:** 54,403 cords across 612 khipu decoded via `decoder.py` (~15 min), cached to `cache.pkl`.
2. **Row segmentation** (593 non-funerary khipu):
   - `color_cycle` (33): dominant color bigram cycle covering >60% of transitions (e.g., BL→BY→MB→W), pivoted into rows at cycle boundaries.
   - `value_marker` (119): (color, value) pairs repeating at regular ordinal intervals (e.g., BY=22 every ~12 cords), rows split at markers.
   - `white_dividers` (48): runs of 3+ white cords as section dividers (journal-style).
   - `none` (393): no row structure — hierarchical, code, or unstructured.
3. **Template extraction** (200 khipu with ≥3 rows): rows aligned by position; each position classified as CONSTANT (>80% same color+value), VARIABLE (same color, differing values), MIXED, or MARKER (position 0).
4. **Clustering:** exact signature match + fuzzy structural match + constant-color-sequence match + abstract (color-set, var-bucket, len-bucket) match.

## Key numbers

| Metric | Count |
|---|---|
| Khipu analyzed | 593 |
| With row structure | 200 (34%) |
| Without row structure | 393 (66%) |
| Templates extracted | 200 |
| Strong templates (const_rate ≥ 0.3, len ≥ 8) | 113 |
| Distinct exact templates | 199/200 |
| Distinct constant-color sequences | 113/113 |
| Distinct abstract templates | 105/108 |
| Templates shared by >1 khipu (any level) | 1 weak group of 4* |

*The single shared abstract group (1000239, 1000390, 1000555, 1000576: constants {AB,MB}, few variables, long rows) matches on color sets only — not a true shared form.

## What this means

**The 1000344 pattern does not generalize as a shared form.** Its template (BL=66, BY=32, MB=33 constants) is unique to 1000344. No other khipu uses it.

**But the template *concept* generalizes.** 113 khipu (19% of corpus) show the same structural signature: rows repeating with high constancy (median 0.84), a mix of fixed template positions and variable data fields. The *idea* of a form — constants as template, variables as data — is widespread. The *specific* forms are not shared.

**Analogy:** Every office writes memos (document type = curriculum), but each office designs its own memo header (template = instance). The Inca bureaucracy standardized *what kind* of document to create, not the exact layout.

**Within-cluster vs cross-cluster template similarity:** 0.147 vs 0.137 — essentially no difference. Templates don't cluster by document type either. A census khipu from Pachacamac and a warehouse khipu from Incahuasi are no more likely to share a template than two random khipu.

## Segmentation method distribution

| Method | n | Primary clusters |
|---|---|---|
| value_marker | 119 | deep_sparse_mixed (38), census_format_paired (24), deep_hierarchical_grouped (16) |
| white_dividers | 48 | deep_sparse_mixed (14), deep_hierarchical_grouped (10), census_format_paired (7) |
| color_cycle | 33 | mixed |
| none | 393 | all (hierarchical/journals/codes don't have rows) |

## Strong templates by provenance

46 unknown, Pachacamac 14, Ica 9, Incahuasi 7, Nazca 5, Santa 5. Templates appear wherever tabular khipu appear — no regional monopoly on the form concept.

## Limitations

1. **Segmentation is heuristic.** The value_marker method may find spurious regularity in noisy data. The 113 "strong" forms (const_rate ≥ 0.3) are the reliable subset.
2. **Row alignment assumes positional correspondence.** If a scribe inserted an extra cord mid-row, alignment breaks and constancy drops. True shared forms with minor variations would be missed.
3. **393 khipu have no row structure.** The template concept only applies to tabular khipu (34%). Hierarchical (warehouse), sequential (journal), and symbolic (code) khipu need different structural analysis.
4. **Decode confidence varies.** Inkawasi long knots without NUM_TURNS produce uncertain values; constants based on uncertain values are less reliable.

## Files

- `cache.pkl` — bulk-decoded cords (612 khipu, 54,403 cords)
- `row_segmentation.csv` — per-khipu segmentation method and row count
- `template_signatures.csv` — per-khipu template with const/var/marker counts
- `template_catalog.csv` — exact (T001–T199) and fuzzy (F001–F199) template groups
- `extract_templates.py` — reproducible pipeline
- `pipeline.log` — run log
