# Case↔Color Hypothesis Test

**Date:** 2026-10-11
**Question:** Do khipu colors mark grammatical case roles (not noun identity)?
**Corpus:** 593 non-funerary khipu; 37,373 simple-color cords; 12,362 compound cords.

---

## Test 1: Color Inventory Size

Quechua has ~10 productive cases (nominative -Ø, accusative -ta, genitive -pa/-q,
dative -man, locative -pi, ablative -manta, instrumental -wan, comitative -ntin,
terminative -kama, perlative -nta).

| Metric | Value |
|---|---|
| Distinct simple colors | 64 |
| Colors for 90% of cords | 13 |
| Median palette per khipu | 4 (mean 4.4) |
| Top color (W) share | 33.8% |
| Top 3 (W+AB+MB) share | 61.7% |

**Verdict: MIXED.** 13 colors for 90% is in the right ballpark for a case system
plus a few extras, and median 4 per khipu matches "each document uses a subset of
cases." But 64 total is far too many for pure case marking, and the distribution
is extremely skewed (W+AB+MB = 62%; the remaining 61 colors split 38%). A case
paradigm would be more balanced. The long tail (51 colors for 10%) must be
explained by any case theory.

**Color families** (last character of Ascher code): 13 families. B (brown) = 55.6%,
W (white) = 33.8%; together 89.4%. The other 11 families are each <5%. This does
NOT resemble a case paradigm — it resembles a binary marked/unmarked system with
a long tail of variants.

## Test 2: Color by Structural Role

Cramer's V for color×level (top 10 colors): **0.125** (weak).
Cramer's V for family×level (13 families): **0.094** (weaker).

Most colors follow the baseline level distribution (L1 ~73%). The standout:

| Color | L1 | L2 | L3+ | Note |
|---|---|---|---|---|
| KB | 48% | 48% | 4% | Evenly split parent/subsidiary — unique |
| W | 79% | 19% | 2% | L1-heavy (unmarked default?) |
| AB | 73% | 23% | 4% | Baseline |
| NB | 65% | 30% | 4% | Baseline-ish |

**Verdict: WEAK.** If colors were cases, we'd expect stronger level associations
(e.g., genitive clustering on subsidiaries). Only KB shows a distinctive profile.
The A family (n=77) is 51% L2 / 21% L3+ — heavily subsidiary — but the sample is
tiny.

## Test 3: Cross-Khipu Consistency

**Palette sharing:** Top colors are widespread, not khipu-specific.
- W: 425/569 khipu (75%)
- MB: 298/569 (52%), AB: 292/569 (51%)
- KB: 186/569 (33%)

**Positional consistency** (subsidiary-fraction across 10 khipu per color):
- AB: mean 0.06, sd 0.09 — **CONSISTENT** (almost always L1/parent)
- MB: mean 0.25, sd 0.31 — moderate
- KB: mean 0.43, sd 0.43 — **VARIABLE** (role differs by khipu)

**Verdict: MIXED, informative.** AB behaves like a fixed grammatical role
(always the "head"). KB does not behave like a fixed case — its function varies
by document. This is the opposite of what a clean case theory predicts (all
cases should be positionally consistent).

## Test 4: Quechua Case Mapping Attempt

Speculative mapping based on structural profiles:

| Khipu color | Candidate Quechua case | Evidence | Confidence |
|---|---|---|---|
| W (33.8%) | Nominative (-Ø, unmarked) | Most frequent, L1-heavy, widespread (49 sites). The default. | Suggestive |
| AB (16.9%) | Accusative (-ta) or topic | Positionall
...[truncated 3947 chars]