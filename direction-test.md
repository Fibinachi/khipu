# Knot Direction vs Color-Marking Test (Unclassified Khipu Only)

**Date:** 2026-10-11
**Scope correction applied:** Excludes funerary (26), warehouse/custodial (18 Inkawasi + 14 warehouse-like + 76 deep_hierarchical_grouped), census (6 + 205 census-like + 250 census_format_paired). Analysis runs on 191 unclassified/other khipu only (67 large_value_flat, 114 deep_sparse_mixed, 10 blank_empty_stubs).

**Rationale for scope:** Well-understood administrative types are numerical; the linguistic/direction channel is sought where document function is unknown.

## Data

- 30,068 knots with S/U/Z direction on included khipu
- Direction inventory: **S=7,467 (25%), U=3,719 (12%), Z=18,882 (63%)**
- Z is modal. No database reference table defines the direction codes; U is non-standard textile terminology.

## Test 1: Direction vs color-marking (basic association)

At cord level, excluding cords with missing color data:

| Direction class | On marked cords | On unmarked cords | Chi-square | p |
|---|---|---|---|---|
| U-direction | 15.3% (n=7,092) | 12.3% (n=2,066) | 11.8 | 6.0e-04 |
| non-Z (S+U) | 47.7% | 60.6% | 107.2 | 4.1e-25 |

**Result:** U alone shows a weak positive association with marking. But non-Z shows a STRONG INVERSE association — because **S-direction knots are disproportionately on unmarked (white) cords**. This is a three-way distinction, not a binary marked/unmarked split:
- Z (modal): neutral
- U (rare): weakly enriched on marked cords
- S: strongly enriched on unmarked cords

## Test 3: Within-level control

| Level | Marked+U | Unmarked+U | p |
|---|---|---|---|
| L1 | 14.0% | 12.3% | 0.076 (marginal) |
| L2 | 19.2% | 11.7% | 7.2e-04 (significant) |
| L3 | 9.3% | 12.0% | 0.67 (ns, reversed) |

The U-marking association is driven by Level 2 only. Not robust across levels.

## Test 5: Does U-direction increase with depth? (evidentiality parallel)

| Level | U-rate | Marking rate |
|---|---|---|
| L1 | 13.7% (n=6,851) | 75.7% |
| L2 | 17.8% (n=2,109) | 82.6% |
| L3 | 9.7% (n=176) | 85.8% |

**Result: NO.** Marking increases monotonically with depth (the evidentiality gradient). U-direction does not — it peaks at L2 then drops. **U-direction is not tracking evidential distance.** If direction is semantic, it is on a different channel.

## Test 4: Anomaly overlap

- 68 included quipu have at least one U-direction knot
- 20 anomalous transcriptions parsed; 6 are in the included set
- Overlap: **3** (1000183, 1000344, 1000583)
- 17 anomalous have no U-direction

**Critical finding:** U-direction is NOT primarily an anomaly marker. Five quipu are ~100% U-direction:

| Khipu | U-knots | S/Z knots | Museum |
|---|---|---|---|
| 1000029 | 242 | 0 | Museum of Science, Buffalo |
| 1000034 | 137 | 0 | Joslyn Art Museum, Omaha |
| 1000345 | 255 | 0 | Museo Nacional, Lima |
| 1000361 | 575 | 0 | Private, Lima |
| 1000368 | 164 | 0 | Private, Arica |

On these pieces U is the scribal NORM, not an exception. Different museums, different collections, no shared provenance — not one scribal school. All are deep_sparse_mixed / unclassified.

## Verdict

**The hypothesis FAILS as stated.** Knot direction (U) does not align with the evidentiality gradient on unclassified khipu:
1. U-rate does not increase monotonically with depth (marking does)
2. The U-marking association is weak (p=6e-04) and level-dependent (L2 only)
3. U is the default — not the exception — on multiple quipu, undermining the "marked status" reading

**However, direction is doing SOMETHING.** Two findings need explanation:
1. **S-direction ↔ unmarked cords** (p=4e-25, strong). If Z is the default and U is rare, what is S doing on white cords specifically?
2. **All-U quipu** as a distinct scribal habit. If direction were purely biomechanical (handedness), we would expect S/Z splits, not a third value dominating entire pieces. The existence of U-monolingual quipu from dispersed collections suggests U is a legitimate systemic variant, not noise.

**Recommended next steps:**
- Investigate the S↔unmarked association: is S the "default" twist and Z the marked one? (Inverts the assumed polarity.)
- Check whether all-U quipu share other features (values, colors, structure) — do they form a sub-type?
- Test direction against the recto/verso moiety hypothesis (Hyland) rather than evidentiality — direction may encode social categories, not information source.

**Caveats:** 8.2% of cords lack color data (excluded, not lumped with white); negative CORD_LEVEL values (-2, -1) exist with small n, unexplored; no database documentation for what U denotes in textile terms.
