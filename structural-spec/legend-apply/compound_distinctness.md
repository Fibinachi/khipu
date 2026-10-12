# Compound Distinctness: Are the Legend Compounds Distinct Codes?

**Question:** In khipu that use 1000368's legend compounds, do different compounds (e.g. W+KB vs W+SR) behave as distinct codes, or are they interchangeable variants?

## Data

### 1000368 (legend source)
The legend block (ordinals 184-220) defines 17 compounds by systematic enumeration:
- W × {DB, VB, 0G, KB, SR, SY}
- BS × {DB, VB, 0G, KB, SR, SY}
- DB × {VB, 0G, KB, SR, SY}

All values zero, no knots. The enumeration itself treats each pair as a distinct
vocabulary entry — the khipukamayuq tied each combination separately, in order.
**Within the legend, the compounds are presented as distinct by construction.**

### 1000096 (Lluta Valley, 2,210 cords) — the heaviest external user
Legend compounds present: W+KB, W+SR, W+SY, W+0G, BS+KB.

| Compound | n | Ordinal span | Max gap | Values |
|---|---|---|---|---|
| BS+KB | 3 | 98–647 | 324 | all 0 |
| W+0G | 7 | 50–1520 | 375 | all 0 |
| W+KB | 13 | 2–1482 | 359 | all 0 |
| W+SR | 23 | 18–1599 | 176 | all 0 |
| W+SY | 17 | 66–1592 | 220 | one 18, rest 0 |

**They are scattered, not clustered.** Max gaps of 176–375 ordinals between
occurrences. No enumeration block. The compounds are used as working vocabulary
throughout the document, not defined in one place.

**Values are uniformly zero** (one exception). Like the legend, these compounds
carry categorical/structural meaning, not quantities.

**Distributional separation: WEAK.** All five compounds show the same profile:
scattered, zero-value, no positional clustering. With the available data we
cannot distinguish W+KB from W+SR behaviorally in 1000096 — they occupy the
same distributional niche (sparse structural markers in a large document).
The sample sizes (3–23 occurrences across 2,210 cords) are too small for a
strong distinctness test.

### Corpus-wide second-color base rates
Of 13,422 compound cords corpus-wide, the top second colors are:
W (51.6%), AB (14.9%), MB (8.9%), KB (3.0%), GG (2.2%)...

The legend's +KB compounds transfer most because **KB is a common modifier
generally**, not because the legend vocabulary is shared. W+KB (141 cords
outside 1000368) is the most common legend pair precisely because both W
(as base) and KB (as modifier) are frequent.

## Verdict

**The legend does not define a transferable vocabulary.** 9 of 17 compounds
appear nowhere else in the corpus. The 8 that do appear are:
1. Dominated by 1000096 (a 2,210-cord outlier where overlap is expected by chance),
2. Skewed toward +KB, which is a common modifier independently of the legend,
3. Used as scattered working vocabulary, never in enumeration blocks.

**The compounds are distinct codes within 1000368** (the enumeration proves
the maker treated each pair as a separate entry), **but that distinctness does
not transfer** — other khipu use a subset of the same pairs without the
legend's systematic framing, and we cannot confirm they mean the same things.

The legend is a local vocabulary definition, not a corpus-wide standard.
