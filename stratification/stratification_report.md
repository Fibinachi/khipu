# Color-Magnitude Stratification Report

**Date:** 2026-10-11
**Question:** Is the color-magnitude stratification found in the 1000265-269
tied set a general warehouse/inventory signature?

## Method

For all 593 non-funerary khipu: decoded every cord value (decoder.py),
grouped by color (COLOR_CD_1), computed per-color median/IQR (n≥5 per color).
For khipu with ≥3 qualifying colors: ranked colors by median, computed
stratification score = 1 − (IQR overlap / total range). Score > 0.7 =
stratified. Kruskal-Wallis for significance.

**Coverage:** 276/593 khipu met the threshold.

## Key findings

### 1. The tied set confirms the signature — per document

| Khipu | Score | W median | AB median | RL median | RB median |
|---|---|---|---|---|---|
| 1000265 | 0.650 | 819 | 339 | 380 | 9.5 |
| 1000266 | 0.916 | 32.5 | 10 | 15 | 26 |
| 1000267 | 0.802 | 52.5 | 8 | 14 | 16 |
| 1000268 | 0.716 | 81 | 25 | 18 | 19 |
| 1000269 | 0.636 | 13 | 5 | 3 | 4 |

Three of five exceed 0.7 individually. Critically, the **magnitude levels
differ across documents** (W median ranges 13–819) while the **color roles
are consistent** (W always highest or near-highest). Same template, different
scales — consistent with multi-commodity inventory (different goods, different
quantities) or the same goods at different times.

### 2. Stratification is NOT warehouse-specific

| Type | Mean score | Frac > 0.7 |
|---|---|---|
| deep_sparse_mixed | 0.535 | 0.434 |
| census_format_paired | 0.495 | 0.371 |
| large_value_flat | 0.478 | 0.421 |
| deep_hierarchical_grouped (warehouse) | 0.405 | 0.288 |

Warehouse khipu have the **lowest** stratification. The signature is
widespread: 38.4% of tested khipu are stratified, 70 with KW p < 0.05,
spanning all types. 45 khipu have perfect scores (1.000).

### 3. Why: same math, different meaning

Color-magnitude separation arises whenever colors encode categories with
naturally different quantities:
- **Census:** demographic groups (adults vs children differ in count)
- **Warehouse:** commodities (maize vs chili differ in volume)
- **Tally:** whatever is being counted, by category

Stratification is a **property of how khipu use color**, not a document-type
diagnostic. The raw score cannot distinguish inventory from census.

### 4. New candidates: 50 khipu

50 khipu with score > 0.7, KW p < 0.05, not currently warehouse, not tied set.
Most promising:
- **7 from Incahuasi** (1000604, 1000605, 1000615, 1000616, 1000617, 1000618,
  1000637): deep_sparse_mixed, perfect 1.000 scores, from the warehouse site.
  **Recommend re-examination as potential warehouse documents.**
- **1000510** (Pachacamac): most significant separation in corpus (p=4.59e-14).
- 23 additional deep_sparse_mixed with strong stratification.

See [new_candidates.md](sandbox://workspace/quipu-analysis/stratification/new_candidates.md)
for the full list with provenance.

## Verdict

**The tied set did NOT reveal a general warehouse diagnostic.** The
stratification score alone cannot distinguish document types — it measures
a universal property of color-coded khipu.

**What the tied set DID reveal:** the *specific* 4-color magnitude-ordered
template (W/AB/RL/RB in consistent roles, different scales per document,
physically tied) is the inventory signature. The template, not the score.

**Practical outcome:** 7 Incahuasi deep_sparse_mixed khipu with perfect
stratification are strong reclassification candidates. The stratification
analysis also provides a new feature for region-aware classification:
stratification + Incahuasi provenance + deep_sparse_mixed cluster =
likely warehouse.

## Deliverables

- [color_magnitudes.csv](sandbox://workspace/quipu-analysis/stratification/color_magnitudes.csv) — 2,783 rows: per-khipu per-color stats
- [stratification_scores.csv](sandbox://workspace/quipu-analysis/stratification/stratification_scores.csv) — 593 khipu: scores, KW p, cluster
- [stratification_by_type.md](sandbox://workspace/quipu-analysis/stratification/stratification_by_type.md) — cross-type comparison
- [new_candidates.md](sandbox://workspace/quipu-analysis/stratification/new_candidates.md) — 50 candidates with provenance
- `stratify.py` — reproducible pipeline
