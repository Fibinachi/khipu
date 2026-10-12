# Color-Magnitude Stratification by Document Type

**Date:** 2026-10-11
**Method:** For each khipu with ≥3 colors (each n≥5 cords), rank colors by median
value, compute IQR overlap. Score = 1 − (overlap / total range). Score > 0.7 =
"stratified" (colors occupy distinct magnitude bands). Kruskal-Wallis p for
significance.

**Coverage:** 276/593 khipu met the ≥3 colors × n≥5 threshold.

## Results

| Document type | n tested | Mean score | Median score | Frac > 0.7 |
|---|---|---|---|---|
| deep_sparse_mixed | 129 | 0.535 | 0.650 | 0.434 |
| census_format_paired | 62 | 0.495 | 0.575 | 0.371 |
| large_value_flat | 19 | 0.478 | 0.500 | 0.421 |
| deep_hierarchical_grouped (warehouse) | 66 | 0.405 | 0.407 | 0.288 |

**Overall:** mean 0.491, median 0.567, 38.4% stratified.

## Stratified + significant (KW p < 0.05), by type

| Document type | n |
|---|---|
| deep_sparse_mixed | 33 |
| deep_hierarchical_grouped | 17 |
| census_format_paired | 13 |
| large_value_flat | 7 |
| **Total** | **70** |

## Interpretation

**Stratification is NOT warehouse-specific.** Warehouse khipu
(deep_hierarchical_grouped) have the *lowest* mean stratification (0.405).
The signature appears across all document types.

Why: the statistical signature (colors at different magnitude bands) has
different causes per type:
- **Census:** colors = demographic categories. Adult males vs children
  naturally have different counts. Stratification reflects population structure.
- **Warehouse:** colors = commodities. Different goods have different
  quantities. Stratification reflects inventory composition.
- **Tally/sparse:** colors = categories of whatever is being tracked.

The same math, different meaning. Color-magnitude stratification is a
*property of how khipu use color*, not a diagnostic of document type.

**What IS specific:** the tied set's *particular* stratification pattern —
4 colors (W/AB/RL/RB) in consistent structural roles, magnitude-ordered,
physically tied as a multi-document set — is the inventory signature, not
the raw stratification score. The score alone doesn't distinguish.
