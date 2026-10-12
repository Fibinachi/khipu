# Khipu Document-Likeness Clustering — Report

**Date:** 2026-10-11
**Corpus:** 593 non-funerary khipu (26 Leymebamba/burial quipu excluded)
**Question:** sorting by structural similarity instead of forcing census/warehouse buckets, what natural groups emerge?

## Method

- 23 features per quipu: structure (cord counts, max CORD_LEVEL, subsidiary rate), color
  (palette size, compound %, red-family %, color-run regularity), knots (S/L/E mix,
  knots per cord), decoded values (log-median, log-max, zero %, small %, uniqueness,
  decode rate). log1p on count/magnitude features, then z-scored.
- Values from the type-aware decoder (`decoder.py`): L-turns = units, S-counts = tens+.
  Cord order via CORD_ORDINAL; hierarchy via CORD_LEVEL (PENDANT_FROM is unreliable).
- Hierarchical clustering (Ward) and k-means (5 restarts, best silhouette kept), k = 2–15.

## Cluster quality (honest)

Silhouette scores are **weak-to-moderate**, not clean:

| method | k=2 | k=3 | k=4 | k=5 | k=6 | k=8 |
|---|---|---|---|---|---|---|
| Ward | 0.100 | 0.117 | 0.131 | 0.111 | 0.100 | 0.118 |
| k-means | 0.362* | 0.145 | 0.159 | 0.145 | 0.141 | 0.133 |

\* k-means k=2 (0.362) is the blank-stub outlier group (n=20) vs everything else — real but trivial.
No resolution gives tight, well-separated clusters. This is a **continuum with dense cores**,
not five clean boxes. That said, the same five cores appear in both methods at multiple
resolutions, so they are structural, not algorithmic artifacts. Primary assignment below
uses Ward k=5 (stable; each core also present in k-means).

## The five emergent document families

### 1. Blank stubs — n=17
Cords recorded, **zero knots, zero color records**. Median values 0, 96% zeros.
Region: "Inka, Late Horizon" (15/17). All previously "unclassified".
Representatives: 1000458, 1000460, 1000462.
Interpretation: unfinished quipu, blanks, or data-entry stubs — not a document type,
but a real and distinct subpopulation. Must be filtered from any value-based analysis.

### 2. Paired color-group census format — n=250
Shallow (max level 1, ~20 top cords), **fixed 2-cord color groups** (consistency 62%),
small values (median 2, max ~22, 99% < 20), ~29% zeros (sparse fields).
Geography: widespread — Puruchuco, South/Central Coast, Nazca, Pachacamac, Ica.
Old labels: 139 census-like, 104 unclassified, 1 census anchor, 5 warehouse.
Representatives: 1000296, 1000475, 1000162.
Interpretation: the Santa format, and it was **empire-wide**, not Santa-specific.
The single largest coherent document family in the corpus.

### 3. Large-value flat tallies — n=78
Shallow (max level 1, ~15 top cords) but **values in the hundreds–thousands**
(median 60, max ~981, only 27% < 20). No color grouping; 19% compound colors.
Mostly Pachacamac/Ica. Old labels: 67 unclassified, 10 census-like.
Representatives: 1000243, 1000496, 1000161.
Interpretation: **undescribed type**. Flat like census, but the magnitudes are
warehouse-scale. Bulk-commodity tallies? Single-level summary sheets? This family
is the strongest evidence that the old two-bucket scheme missed real document types.

### 4. Deep hierarchical, color-grouped — n=76
Deep (max level 3, ~98 top cords, ~57 subsidiaries, 46% subsidiary rate),
large values (max ~1444), 7 colors, and **fixed 2-cord color groups** (66%).
14 from Incahuasi. Old labels: 10 warehouse, 10 warehouse-like, 48 unclassified.
Representatives: 1000094, 1000079, 1000524.
Interpretation: the Inkawasi warehouse format — deep detail + the census-style
color grouping. Suggests the color-group convention crossed document types
(possibly a pan-administrative record-keeping idiom, not census-specific).

### 5. Deep/sparse mixed ledgers — n=172
Moderate depth (level 2, ~60 top cords, ~10 subsidiaries), **56% zeros**,
small values otherwise (median 0, max ~83), 8–9 colors, no color grouping.
Pachacamac/Incahuasi heavy. Old labels: 114 unclassified, 49 census-like.
Representatives: 1000433, 1000263, 1000521.
Interpretation: the fuzziest core — possibly sparse multi-purpose ledgers, or
a mix of degraded census and warehouse records. Needs subdivision with better data.

## What happened to the 350 "unclassified"

They are **not** a residue — they form coherent families of their own:

| family | n | unclassified in it |
|---|---|---|
| blank stubs | 17 | 17 |
| census format | 250 | 104 |
| large-value flat | 78 | 67 |
| deep grouped | 76 | 48 |
| deep/sparse | 172 | 114 |

104 of the 350 belong to the census format (the old classifier under-detected it);
67 belong to the new large-value-flat family; the rest sit in the deep families.

## Notable negatives

- **Red is rare** in the non-funerary corpus: only 80/593 quipu have any red-family
  cords, median red % is 0 in every cluster. Red-as-divider is a funerary/Leymebamba
  phenomenon (or at least not a general administrative one).
- **Census and warehouse are not opposites**: the deep-grouped family combines
  warehouse depth with census color-grouping. The old buckets were too rigid.
- 10 quipu have no cord records at all (nodata) — they scatter into the deep/sparse
  family on zero-vectors; treat as missing data, not a type.

## Files

- [khipu-clusters-2026-10-11.csv](sandbox://workspace/quipu-analysis/khipu-clusters-2026-10-11.csv) —
  KHIPU_ID, CLUSTER_ID, CLUSTER_NAME, OLD_LABEL (reference only)
- Scripts: `cluster_step1_features.py`, `cluster_step2_cluster.py`, `cluster_step3_describe.py`
- Feature cache: `/tmp/cluster_feats.pkl` (ephemeral; re-run step 1 to regenerate)

## Caveats

- Silhouettes ~0.1–0.16: cores are real but boundaries are soft; expect reassignments
  with better features (section segmentation, knot-type sequences, color-slot order).
- Inkawasi values are structurally inferred (NUM_TURNS missing in OKR) — family 4
  rests on hierarchy/color, not full numbers.
- 213+ quipu lack REGION data; geographic claims are provisional.
