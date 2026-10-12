# Quechua ordering hypothesis test

Quechua morpheme order: ROOT-PL-CASE-EVD. Predicted khipu order: [content] -> M(-kuna) -> W(-ta) -> A(-mi).

Letter-token marginals: {'K': 994, 'M': 1828, 'W': 4786, 'A': 2080} (total 9688)

## Bigram/trigram counts vs null

| pattern | observed | expected (independence) | perm-mean | perm p (one-sided, greater) |
|---|---|---|---|
| M->W | 196 | 515.0 | 200.4 | 0.6607 |
| W->A | 150 | 586.0 | 234.9 | 1.0000 |
| M->W->A | 14 | 76.4 | 22.0 | 0.9760 |

Adjacent letter pairs total: 5525; adjacent letter triples total: 3820.

## Content-precedes check (ROOT before PL-CASE-EVD)

M->W->A trigrams preceded by content cord: 6/14 = 0.429
Baseline (any letter token preceded by content): 4044/9569 = 0.423

## Verdict: Quechua ordering hypothesis NOT supported

**Forward vs reverse dissimilar bigrams are symmetric:**
- Quechua-forward (M->W, W->A, M->A): 196+150+151 = 497
- Reverse (W->M, A->W, A->M): 182+155+139 = 476
- No directional preference. Adjacent letters show no ordering bias.

**M->W->A trigram: 14 observed vs 22 expected under permutation (p=0.976, depleted).**
Scattered across 11 khipu with no concentration. Consistent with chance.

**W->A significantly depleted** (150 vs 235 perm-mean, p=1.0 one-sided greater = observed minimum).
W and A avoid adjacency.

**Content-precedes check fails:** MWA trigrams preceded by content 6/14=0.429 vs baseline 0.423. No difference.

**Structural explanation:** 45% of letter-bearing khipu are single-letter-dominated (>=80% one letter).
Different letters occupy different khipu/sections, so cross-letter transitions are rare and directionless.
The dominant pattern is self-repetition (W->W: P=0.856), i.e. the same marker repeated down a cord
sequence -- spreadsheet-column formatting, not morpheme chaining.

**Conclusion:** The Hangman frequency alignment identified real high-frequency function items on both
sides (a Zipfian universal), but the 4-letter alphabet does NOT combine into Quechua-ordered sequences.
The frequency match was real; the structural analogy (morpheme chain) was wrong.
