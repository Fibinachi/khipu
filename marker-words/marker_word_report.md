# Marker-Word Test: Does 22 Label Something?

**Question:** If 22 is a logogram (stands for a word), it should keep the same
company everywhere. Same neighboring colors, same contexts, across khipu.
If it's just a structural code, its companions will vary.

**Verdict: 22 does NOT label something consistent. It is not a logogram.**

## Data

- 700 occurrences of values {22, 23, 32, 33, 34} across 185 khipu
- Full context captured per occurrence: own color, ±3 neighbors, doc type,
  data regime, region, tertile position

## Test 1: Color consistency (is 22 tied to one color?)

No. 22 appears on **29 distinct colors**. 23 on 22 colors. The top color for
all five markers is W (white), at 30–39% — but white is 28% of all cords
corpus-wide, so this is only modest enrichment, not locking.

BY=22 (the 1000344 row marker) accounts for just 14/218 (6.4%) of all 22s.
1000344's use is idiosyncratic, not the corpus norm.

## Test 2: Neighbor consistency (fixed expressions?)

No. Per marker value:
- 53–106 **distinct** (prev, own, next) trigrams
- Top trigram covers only 15–19% of occurrences
- Top-3 trigrams cover 24–37%

The most common "trigram" for every marker is (W,W,W), (MB,MB,MB), or
(AB,AB,AB) — the marker sitting inside a same-color run. This is not a fixed
expression; it's the marker value appearing within monochromatic sequences,
which are common anyway.

Cross-khipu recurrence is weak: only 19 trigrams for marker 22 appear in
more than one khipu, and those are the trivial same-color runs.

## Test 3: Positional consistency (structural marker?)

No. Tertile distribution is essentially uniform (begin/mid/end ≈ 33/33/33
for all markers). If 22 were a row-start marker corpus-wide, it would
concentrate at structural boundaries. It doesn't — except in 1000344
specifically, where Charles found it.

## Test 4: Regime and regional specificity

Markers appear across all data regimes (2, 3, 4, 5, 6) and all document
types. Not regime-specific. Regional data is sparse (mostly blank), but
markers appear on Central Coast, South Coast, and Puruchuco khipu — not
obviously local.

## Test 5: Khipu-level clustering (admin code?)

**Yes — heavy skew.** 1000344 alone holds 95/700 (13.6%) of all marker
occurrences. The next heaviest user (1000501) has 27. A long tail of khipu
use markers rarely (1–3 times).

This is the strongest signal: markers are not evenly spread. A few scribes
use them intensively; most barely do.

## Distinguishing the three hypotheses

| Hypothesis | Prediction | Result |
|---|---|---|
| Logogram (22 = word) | High companion consistency, fixed expressions, color-locked | **REJECTED.** 29 colors, 106 trigrams, no fixed expression. |
| Structural code (22 = row marker) | Positional concentration at boundaries | **REJECTED corpus-wide.** Tertile uniform. (True locally in 1000344.) |
| Admin code / conventional value | Uneven use, some heavy users, appears as both data and marker | **SUPPORTED.** Heavy skew, appears in variable positions (41% of khipu) and structural roles (1000344). |

## Interpretation

22/23/32/33/34 are **high-frequency small integers** in the Inca
administrative number system — common values that come up a lot, like 1, 2,
5, 10 in modern records. They are:

1. **Data** in most khipu (variable-field values, 41% of khipu)
2. **Convenient markers** for scribes who need a distinctive row/batch flag
   (1000344's BY=22/BY=23 is the clearest case — but it's that scribe's
   convention, not a corpus-wide grammar)
3. **Slightly white-enriched** (30–39% vs 28% background), consistent with
   white's role as header/summary color

Charles's "22 to 23 forms thing" is real but **local**: 1000344's scribe used
22/23 to distinguish batches. Other scribes used the same numbers as ordinary
data values. There is no corpus-wide 22/23 grammatical rule.

## Caveats

- Decode confidence varies (Inkawasi long knots lower)
- Regional metadata is sparse (most khipu lack region tags)
- "Unknown" doc_cluster (89/218 for marker 22) reflects khipu not in the
  template analysis, not a real category
- The neighbor-color chi-square was computed but is confounded by color-run
  structure; trigram analysis is the cleaner test
