# Residuals Report: Structure in the Unclassified Khipu

**Date:** 2026-10-11
**Set:** 147 khipu (114 sup-unclassified + deep_sparse_mixed; 14 cabinet no-split;
17 rare-knot; 20 anomalous-transcription; 3 EE-heavy; 5 all-U; overlapping)

## Headline

The unclassified are not noise and not a single population. They decompose into
regional knot dialects, a candidate dense-value document type, stubs, funerary
contamination, and ~40-50 true unknowns. The "weird symbols" are systematic:
rare knot types map to regions (SP to Incahuasi/South Coast, LL to Lluta,
TF to Ica/Pisco, S-twist to the south coast generally). Rarity is geography,
not error.

## 1. Population profile

| Feature (median) | Residual (n=147) |
|---|---|
| cords | 72 |
| colors | 8 |
| max level | 2 |
| zero-value % | 60.8% |
| small-value % (<20) | 93.0% |
| decode rate | 100% |
| white % | 40.3% |
| S-knot % | 60.5% |

Provenance: 35 no provenance, 20 "unknown", Incahuasi 19, Pachacamac 18,
Leymebamba 5 (funerary), Ica 4, Nazca 3.

Supervised labels inside the set: 124 unclassified, 13 census-like, 4 warehouse,
1 warehouse-like, 5 unknown (funerary, not in 593).

## 2. Byte-level structure

Serialized 147 khipu (20,448 cord-tokens, headers stripped):

| n-gram | Distinct | Zipf slope | Full-corpus slope |
|---|---|---|---|
| 4-byte | 2,983 | **-1.094** | -0.930 |
| 8-byte | 9,877 | -0.830 | -0.935 |
| 12-byte | — | -0.899 (ref) | -0.899 |

The residuals show STEEPER Zipf (-1.094) than the main corpus: more repetitive,
more formulaic. W:0 (`f8040000`) at 14.7% of tokens vs 9.4% corpus-wide.
Doubling (`f8040000f8040000`) at 8.8% vs 5.1%. The top 4-byte patterns are the
same grammatical-tier zero cords. The "weird" khipu lean HARDER on the standard
structural vocabulary, not less. Whatever makes them unclassified, it is not
absence of structure.

## 3. Sub-clustering (n=147, 23 features, Ward)

Silhouettes weak (0.11-0.135), but stable groups emerge across k=3..6:

- **9-group** (1000265-69, 1000344, 1000443, 1000446, 1000608): 9% zeros
  (vs 61% median), 4 colors, S-twist heavy, sequential IDs. Candidate
  dense-value document type; S-twist predicts south-coast origin for the
  5 unprovenanced members.
- **13-group** (rare-knot): 260 median cords, SP/LL/BL/EE knots, large.
  Regional knot-variant offices.
- **23-group** (stubs): 32 cords, 4 colors, 95% zeros. Fragments/minimal records.
- **44-group** (twist-anomalous): U/S-dominant, Nazca, Leymebamba funerary,
  all-U pieces. Twist proportions match full corpus exactly.
- **44-group** (large): 100 cords, 12 colors, Incahuasi/Pachacamac heavy.

## 4. Rare feature census (113 feature-instances)

| Feature | Khipu | Pattern |
|---|---|---|
| twist-S-dominant | 38 | south coast (Costa Sur, Paracas, Nazca, Ica, Mollepampa) |
| twist-U-dominant | 29 | scattered; 3 unknown-prov of 10 sampled |
| rare-knot-SP | 10 | Incahuasi (4) + South Coast (3) |
| rare-knot-EE | 7 | scattered |
| rare-knot-BL | 4 | scattered |
| rare-knot-LL | 4 | Lluta Valley |
| rare-knot-TF | 1 | Ica/Pisco (tufted unary tally) |
| long-knot->9-turns | 2 | 1000504, 1000514 (both SP-knot khipu) |
| many-uncolored-cords | 12 | scattered |
| deep-hierarchy (5+) | 3 | 1000279, 1000574, 1000624 |

Most anomalous single khipu: **1000514** (4 rare features: SP+BL+EE+>9-turn long
knots; unknown provenance; Incahuasi/South Coast SP-dialect suspected).

Key control: twist-dominance proportions in residuals (S 26%, U 20%, Z 54%)
are IDENTICAL to the full corpus (S 24%, U 21%, Z 55%). Twist does not define
the residuals; it is corpus-wide.

## 5. Decomposition of the 147

| Hypothesis | N (approx) | Status |
|---|---|---|
| H1 Regional dialects (SP/LL/TF/S-twist) | ~45 | Strong: knots map to regions |
| H2 Dense-value type (9-group) | 9 | Candidate new type |
| H3 Stubs/fragments (95% zeros) | ~23 | Completeness, not type |
| H4 Funerary contamination (Leymebamba) | 5 | Exclude from admin analysis |
| H5 Twist-anomalous (needs moiety test) | ~20 | Awaiting disambiguation |
| H6 Classified-but-weird (regional execution) | 18 | Structure normal, knots local |
| H7 True residuals | ~40-50 | Genuinely unclassified |

(Overlapping; approximate.)

## 6. Verdict

**The prior ("failed normal khipu") is rejected.** The residuals contain:
1. **Regional paperwork dialects** — the strongest signal. Rare knots are
   not errors; they are local office conventions (SP=Incahuasi/South Coast,
   LL=Lluta, S-twist=south coast).
2. **A candidate new document type** — the 9-group dense-value khipu
   (91% nonzero values, minimal structural overhead).
3. **No loss of structure** — steeper Zipf, higher formulaic repetition
   than the classified corpus.

**What this means for the classification:** the supervised classifier was
trained on central-coast norms. South-coast and valley offices used different
knot/direction conventions for the same document types. "Unclassified" often
means "non-standard region," not "unknown type."

**Recommended next steps:**
1. Exclude the 5 Leymebamba funerary khipu from residual analysis.
2. Test H1: predict SP knots at Incahuasi, LL at Lluta, S-twist on south coast
   in newly excavated or unanalyzed khipu.
3. Investigate the 9-group as a document type: compare against known south-coast
   administrative contexts; check Ascher databook notes for 1000265-69.
4. Re-run supervised classification with region-aware features (knot dialect
   as a covariate, not an anomaly).
5. 1000514 deserves individual study: 4 rare features, unknown provenance.

## Deliverables

- [unclassified_set.csv](sandbox://workspace/quipu-analysis/residuals/unclassified_set.csv)
- [residual_profile.md](sandbox://workspace/quipu-analysis/residuals/residual_profile.md)
- [residual_ngrams.md](sandbox://workspace/quipu-analysis/residuals/residual_ngrams.md)
- [residual_clusters.md](sandbox://workspace/quipu-analysis/residuals/residual_clusters.md)
- [rare_features.csv](sandbox://workspace/quipu-analysis/residuals/rare_features.csv)
- [residual_hypotheses.md](sandbox://workspace/quipu-analysis/residuals/residual_hypotheses.md)
