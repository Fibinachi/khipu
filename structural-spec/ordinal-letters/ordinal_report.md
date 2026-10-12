# Ordinal-letter analysis: summary report

**Date:** 2026-10-11
**Corpus:** 593 khipu (hex corpus), 9,688 letter-tokens

## The alphabet

| Letter | Hex | Khipu pattern | Hypothesized Quechua | n |
|---|---|---|---|---|
| W | f8040000 | W single-knot Z L1 val=0 | -ta (accusative) | 4,786 |
| A | 20040000 | AB single-knot Z L1 val=0 | -mi (evidential) | 2,080 |
| M | a4040000 | MB single-knot Z L1 val=0 | -kuna (plural) | 1,828 |
| K | 84040000 | KB single-knot Z L1 val=0 | TBD | 994 |

## What we found

### 1. Letters repeat; they don't chain

The dominant sequential behavior is **self-repetition**, not cross-letter chaining:

| Transition | Count | P(to\|from) |
|---|---|---|
| W->W | 2,601 | 0.856 |
| A->A | 654 | 0.649 |
| M->M | 576 | 0.582 |
| K->K | 247 | 0.503 |

86% of W-tokens are followed by another W. Runs reach length 54 (all W). The top "words"
are singletons (W: 938, A: 658, M: 512, K: 350) and self-repetitions (WW: 317, AAA: 38).
No multi-letter word with distinct letters exceeds 43 occurrences (MW).

371 distinct letter-runs, 4,163 total runs. Run lengths: 2,458 singletons, 857 pairs,
then a long tail of W-runs out to length 54.

**Interpretation:** These are not morphemes chaining into words. They are the same marker
repeated down a cord sequence -- like applying the same cell format to every row of a
spreadsheet column. WW is the census paired-cord structure; longer W-runs are its extension.

### 2. No Quechua ordering

The critical test -- Quechua ROOT-PL-CASE-EVD predicts khipu [content]->M->W->A -- **fails**:

- **M->W->A trigram:** 14 observed vs 22 expected under permutation null (p=0.976, depleted).
  Scattered across 11 khipu (1000099, 1000247, 1000327, 1000508, 1000570, 1000571,
  1000588, 1000589, 1000609, 1000611, 1000617), no concentration.
- **Forward vs reverse bigrams symmetric:** Quechua-forward M->W/W->A/M->A (497)
  vs reverse W->M/A->W/A->M (476). No directional bias.
- **W->A significantly depleted** relative to permutation null (150 vs 235 expected,
  one-sided p=1.0, i.e. observed was the minimum across 500 permutations).
- **Content-precedes:** MWA trigrams preceded by a content cord at 6/14=0.429
  vs baseline 0.423 for any letter token. No difference.

### 3. Letters segregate by khipu

45% of letter-bearing khipu (188/416) are single-letter-dominated (>=80% one letter type).
Different letters occupy different khipu (and likely different sections within khipu).
This explains both the self-repetition dominance and the depletion of cross-letter
transitions: W and A rarely meet because they live in different documents.

All four letters skew toward the latter portion of khipu (mean normalized position
0.575-0.603; end-third counts highest), consistent with grammatical/summary cords
placed after content.

| Letter | n | mean pos | median pos | begin / mid / end |
|---|---|---|---|---|
| W (-ta) | 4,786 | 0.603 | 0.631 | 891 / 1730 / 2165 |
| A (-mi) | 2,080 | 0.596 | 0.623 | 413 / 707 / 960 |
| M (-kuna) | 1,828 | 0.575 | 0.603 | 413 / 638 / 777 |
| K (TBD) | 994 | 0.585 | 0.600 | 195 / 381 / 418 |

## Verdict

**The Hangman anchors are NOT validated as sequential morphemes.**

The frequency alignment was real -- both Quechua and khipu have a small set of
high-frequency function items atop a Zipfian distribution. That is a genuine structural
parallel, and one of several independent lines of evidence for language-like organization.

But the letters do not combine into words, and they do not follow Quechua morpheme order.
The frequency match reflects a shared statistical property (few frequent function items),
not a shared sequential grammar. The correct analogy for letter-tokens is not
"morpheme in a word" but "format applied down a column": repeated structural markers
whose meaning is positional and categorical, not compositional-sequential.

**What this kills:** the hypothesis that zero-value grammatical-tier cords chain together
into morpheme-like sequences readable in linear order.

**What this supports:** the spreadsheet model. Letters are column formats, section markers,
and categorical flags -- applied repeatedly, segregated by document, positioned after
content. Their "grammar" is tabular and spatial, not linear-sequential.

**What remains open:** the hierarchical (parent-subsidiary) relationship between letter-cords
and content cords was not tested here. If letters function as case/evidential markers, the
marking may operate through attachment (which content cord a letter-cord modifies) rather
than through linear adjacency. That is the next test. A second open question: the K letter
(TBD, rank-4) participates in cross-letter bigrams (K->W 91, W->K 105, K->A 85) at rates
comparable to other cross-letter transitions -- its role is as unresolved as the others.

## Files

- `letter_occurrences.csv` -- 9,688 rows: every letter-token with khipu, cord, position, neighbors
- `letter_words.csv` -- 371 distinct letter-runs with counts and khipu spread
- `positional_grammar.md` -- positional distributions and bigram transitions
- `ordering_test.md` -- Quechua-order hypothesis test with permutation statistics
- `ordinal_analysis.py` -- reproducible pipeline
