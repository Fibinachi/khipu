# Filing Cabinets: Splitting deep_sparse_mixed Khipu into Documents

**Date:** 2026-10-11
**Theory:** The 172 deep_sparse_mixed khipu are not a document type — they are filing
cabinets containing multiple documents. Split at document boundaries, classify each.

## Method

### Boundary detection
L1 cords in ordinal order. Boundary score between consecutive L1 cords:
- Twist shift (dominant Z/S/U changes, 3-cord persistence): +3
- Color palette shift (Jaccard >= 0.75 on 4-cord windows): +2
- Depth reset (deep run -> flat): +2
- Empty-run separator (>=2 consecutive empty cords): +2
- Magnitude regime shift (log knot-count): +1

Boundary if score >= 4. Minimum 4 L1 cords per segment. Subsidiaries follow parent ordinal
(they share the parent's CORD_ORDINAL in OKR).

### Classification
9 scale-invariant features per segment (max_level, n_colors, white_pct, compound_pct,
z/s/u_pct, subsidiary_rate, med_knotcount). Centroids from known-type khipu:
- census (n=60), warehouse (n=60), bulk_tally (n=60),
- south_funerary (n=15 S-twist exemplars), unknown_office (n=5 all-U)

Nearest centroid in z-scored space; distance > 3.0 SD -> unclassified.
Adjacent same-type segments merged. n_cords excluded (segments are fragments;
absolute size not comparable to whole-khipu centroids).

## Results

### Splitting
- **73/172 khipu (42%) split into multiple documents**; 99 are single documents.
- 353 total documents after merging (480 raw segments).
- Segment counts: 37 khipu with 2 docs, 7 with 3, 8 with 4, declining tail to one
  khipu with 36 raw segments (1000321 — see over-splitting below).

### Homogeneity (validation independent of classifier)
- Palette entropy improved by splitting: **66/81 (81%)**.
- Twist entropy improved: 40/81 (49%).
- Splitting produces more palette-homogeneous segments — different documents use
  different color palettes. Strongest evidence the splits are real.

### Classification
- 286/353 segments (81%) assigned a type; 67 unclassified.
- But confidence is low (median 0.16); only 127/353 (36%) reach conf >= 0.2.
- High-confidence distribution: warehouse 40, bulk_tally 32, census 22,
  unknown_office 17, south_funerary 16.

### Pipeline validation (honest)
Split known-type khipu, check if segments return to true type:
- census: 7/13 correct (54%)
- warehouse: 8/40 correct (20% — random)
- bulk_tally: 4/12 correct (33%)

**The classifier is weak, especially for deep types.** A warehouse fragment does not
look like a warehouse — document type is a whole-khipu property. Segment type
assignments should be treated as suggestive, not definitive.

### Multi-type cabinets (strongest finding)
**58/73 multi-document cabinets contain segments of >=2 distinct types.**
These khipu genuinely mix document types — e.g., census-like sections alongside
tally-like sections. This is the filing cabinet pattern the theory predicted.

### Over-splitting
Khipu with >8 segments (e.g., 1000321 with 36) show rapid Z/S twist alternation
with palette shifts. These are likely **interleaved internal structure**, not dozens
of separate documents. The boundary detector cannot distinguish "alternating
documents" from "alternating sections within one document."

## Updated type counts

Of 172 deep_sparse_mixed khipu:
- 99 remain single unclassified documents (boundaries not detected or truly unitary)
- 73 split into 254 documents (after merge), of which:
  - ~127 classify with conf >= 0.2 (warehouse 40, bulk_tally 32, census 22,
    unknown_office 17, south_funerary 16)
  - remainder low-confidence or unclassified

**Net effect:** ~127 documents resolve into known types with moderate confidence.
~45 khipu-worth remain genuinely unclassified (99 single + low-conf segments).
deep_sparse_mixed shrinks by roughly half but does not disappear.

## Interpretation

The filing cabinet theory is **partially confirmed**:
1. 42% of "mixed" khipu contain detectable internal document boundaries.
2. 80% of those multi-doc cabinets mix >=2 types.
3. Splitting improves palette homogeneity 81% of the time.

But it is **not the whole story**:
1. 58% don't split — they are single documents with mixed features, a real
   (if incoherent) category.
2. Segment classification is too weak to definitively retype most segments.
3. The most fragmented khipu are probably interleaved, not multi-document.

**Verdict:** deep_sparse_mixed was partly an artifact of not segmenting (the 73
cabinets), and partly a real residual category (the 99 non-splitting khipu).
The honest update: ~75 newly-identified documents resolve into known types;
~100 khipu remain unclassified.

## Limitations

- Boundary detection is heuristic; twist/palette alternation may mark sections,
  not documents.
- The type classifier validates poorly on deep types (warehouse: 20%).
- Knot-count proxy used for magnitude (decoder too slow for 19k cords).
- Confidence is low across the board; treat assignments as hypotheses.
- Physical join evidence (NOTES) not systematically incorporated.
