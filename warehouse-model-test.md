# Warehouse Tag Model Test — Inkawasi (18 quipu, OKR 1000597–1000614)

**Date:** 2026-10-11
**Method corrections applied:** hierarchy via CORD_LEVEL (not PENDANT_FROM); cord order via CORD_ORDINAL; type-aware knot decoder (`decoder.py`: L-turns=units, S-counts=tens+); funerary quipu excluded.
**Critical data limit:** ALL Inkawasi L-knots lack NUM_TURNS in OKR. Units digits are unrecoverable from the database. 1272/3083 cords (41%) decode to NULL. Published Urton & Chu values came from physical inspection.

---

## Claim 1: Attached goods supply the commodity ("what")

**Verdict: HOLDS (not re-tested; archaeological).**
From Urton & Chu 2015: beans (1000613), chili (1000608/1000609), peanuts (1000607, 1000610–1000612, 1000614), inferred chili (1000597/1000598). Associations are by physical proximity, stated in the paper itself. Not in question.

---

## Claim 2a: Compound color ORDER is meaningful (first=origin, second=destination)

**Verdict: FAILS within Inkawasi.**

Corpus-wide (excluding Inkawasi): AB:W=1268 vs W:AB=112 (ratio 11.3).
Inkawasi-only: AB:W=31 vs W:AB=26 (ratio 1.2).

The corpus-wide asymmetry is driven *entirely* by non-warehouse quipu. Within the warehouse, the highest-volume pairs are symmetric:

| Pair | Forward | Reverse | Ratio |
|---|---|---|---|
| AB:W / W:AB | 31 | 26 | 1.2 |
| MB:W / W:MB | 33 | 31 | 1.1 |
| AB:MB / MB:AB | 31 | 28 | 1.1 |
| NB:W / W:NB | 30 | 11 | 2.7 |

Some low-count pairs show asymmetry (GG:YB 36:0, MB-KB 15:1, KB:W 12:2), but these are khipu-specific conventions — all 36 GG:YB cords are on the single bean quipu 1000613. That is a local scribal habit, not a general routing grammar.

**What kills it:** the exact pair (AB:W) that motivated the routing hypothesis shows no order signal at the warehouse itself. If first=origin/second=destination were the warehouse's encoding rule, it would show up here. It doesn't.

---

## Claim 2b: Compound-color cords are subsidiaries

**Verdict: FAILS as stated; a weaker gradient version holds.**

Old claim: "compounds are always subsidiaries" (was based on the broken PENDANT_FROM test).

| CORD_LEVEL | Compound | Total | % |
|---|---|---|---|
| 1 | 268 | 1967 | 13.6% |
| 2 | 177 | 901 | 19.6% |
| 3 | 40 | 166 | 24.1% |
| 4 | 8 | 23 | 34.8% |

**What kills the absolute claim:** 268 compound-color cords sit at level 1. "Always" is dead.

**What survives:** compounds are monotonically enriched with depth. A routing/attachment marker that *tends* to appear on subsidiary detail cords is consistent with the gradient — but 13.6% at top level means compounds also serve a parent-level function.

---

## Claim 2c: White denotes the state (on parent/ownership cords)

**Verdict: structural pattern HOLDS; semantic gloss ("state") UNTESTABLE.**

| CORD_LEVEL | White-involved | Total | % |
|---|---|---|---|
| 1 | 715 | 1967 | 36.3% |
| 2 | 189 | 901 | 21.0% |
| 3 | 17 | 166 | 10.2% |
| 4 | 1 | 23 | 4.3% |

White is strongly concentrated on level-1 cords and decays with depth. Level-1 white rate (36.3%) is nearly double the combined deeper rate (19.0%). This is the model's strongest surviving result.

**Limit:** the data establishes "white marks parent-level cords." Nothing in the database tests *state* specifically vs. any other parent-level owner (ayllu head, warehouse manager, etc.). The semantic leap to "state" needs documentary evidence this test cannot supply.

---

## Claim 3: Knots encode inventory quantities

**Verdict: HOLDS in principle; UNTESTABLE in full from OKR.**

- 1811/3083 cords decode; 1272 (41%) NULL — units digits gone with the missing NUM_TURNS.
- Decoded range: 0–224,001 (tens and up); median 0; 65.5% zeros.
- The 65.5% zero rate is partly decoder artifact: cords with non-standard units knots get digit=0 with low confidence rather than NULL.
- Urton & Chu's repeating values (15/10/47/208, the tax/deduction patterns) are *consistent* with tens-decodes where visible: 1000608 (chili) shows value 10 repeating 3× at level 1 (15 → tens-decode 10).

**What this means:** the quantities are real (the paper's physical readings prove it), but OKR cannot reproduce them. Any quantitative test built on OKR decodes alone — including parts of this report — is working with one hand tied. The model is not refuted; it is starved of data.

---

## Claim 4: Subsidiaries represent deposits/claims/allocations (detail attached to parents)

**Verdict: FAILS in summation form; non-summation detail roles UNTESTED.**

Parent value vs. sum of decoded level-2 children (non-trivial cases):

| Khipu | Example parent | Sum(children) |
|---|---|---|
| 1000610 (peanut) | 16201 | 0 |
| 1000609 (chili) | 1401 | 1 |
| 1000607 (peanut) | 0 | 1151 |
| 1000612 (peanut) | 10 | 501 |
| 1000613 (beans) | 20 | 40 (×3 parents) |

Exact parent==sum(children) matches are nearly all trivial 0==0. Where both sides are nonzero, summation essentially never holds. The 1000613 beans pattern (20 vs 40, three parents) suggests *ratio* relationships, not summation — but with units missing, even that is tentative.

**What kills it:** if subsidiaries were additive detail of the parent's quantity, nonzero parents would equal (or systematically relate to) the sum of nonzero children. They don't.

**What survives:** subsidiaries as non-additive detail (allocations, claims, earmarks) is neither confirmed nor refuted — and cannot be, with 41% NULL values.

---

## Test D: Structural coherence — the 18 split across 3 clusters

**The model does not predict this heterogeneity, and the heterogeneity is real.**

| Cluster | Quipu | Commodity-linked |
|---|---|---|
| deep_hierarchical_grouped (4) | 1000597, 1000598, 1000603, 1000607–1000613 | 9 of 10 paper quipu |
| census_format_paired (2) | 1000599–1000602, 1000606 | none |
| deep_sparse_mixed (5) | 1000604, 1000605, 1000614 | 1000614 (peanuts) |

Three facts the monolithic "Inkawasi = warehouse tags" framing cannot absorb:

1. **The 8 non-paper quipu were never analyzed by Urton & Chu.** The model's evidence base is their 10 quipu (9 in cluster 4, 1 in cluster 5). The 5 census-formatted ones (1000599–1000602, 1000606) are small (13–48 cords), shallow, mostly single-color — they look like census tallies, not inventory tags. They are *from* the warehouse site; nothing says they *are* warehouse inventories. A warehouse complex generates multiple document types (labor, tribute, storage).

2. **Same commodity, same pile, different structures.** The 5 peanut quipu came from one peanut-covered group in kallanka U.A. 4. Their hierarchy profiles:
   - 1000611: 289 L1 / 37 L2 (top-heavy)
   - 1000612: 162 L1 / 200 L2 (subsidiary-heavy)
   - 1000614: 173 L1 / 176 L2 (balanced; alone in cluster 5)
   
   One commodity, one pile, three structural profiles. "One warehouse tag form" does not survive this.

3. **Cluster ≠ commodity.** Peanuts span clusters 4 and 5; chili sits only in 4; beans only in 4. Structure does not track commodity, so whatever the clusters capture (function? scribe? recording event?), it isn't "what good."

**Verdict:** the model, strictly construed as Urton & Chu's claims about their 10 quipu, is not refuted by the other 8 — but the broader "Inkawasi = warehouse tags" generalization is. The 8 non-paper quipu need independent functional analysis, not assimilation.

---

## Summary verdicts

| Claim | Verdict |
|---|---|
| 1. Goods = commodity (archaeological) | **Holds** |
| 2a. Compound order = routing (origin/destination) | **Fails** at Inkawasi — the AB:W asymmetry is entirely non-warehouse |
| 2b. Compounds are subsidiaries | **Fails** as absolute (268 at level 1); gradient with depth holds |
| 2c. White = state, on parent cords | **Structural pattern holds** (36%→4% by level); "state" gloss untestable |
| 3. Knots = quantities | **Holds in principle**; untestable in full from OKR (41% NULL, units gone) |
| 4. Subsidiaries = additive detail | **Fails** — parents ≠ sum(children) wherever both nonzero |
| D. One warehouse tag form | **Fails** — 3 clusters; same commodity/pile spans structures |

## What the model needs

1. **Narrow it** to what Urton & Chu demonstrated on their 10 quipu. Stop generalizing to all 18.
2. **Drop the routing-order rule** for the warehouse context. It has no signal here. (It may hold for the census corpus — that's a separate test.)
3. **Replace "compounds are subsidiaries"** with "compounds enriched with depth; 13.6% at top level need their own explanation."
4. **Treat the 8 non-paper Inkawasi quipu as unknown documents** at a warehouse site, not as warehouse tags. The 5 census-formatted ones especially.
5. **Get NUM_TURNS data.** Every quantitative claim about Inkawasi is crippled without it. OKR alone cannot do this work — the physical quipu (or Urton & Chu's unpublished readings) are required.

## Caveats on this test

- 41% of cord values unrecoverable; all arithmetic findings are tens-and-up only.
- 65.5% zero rate partly reflects decoder's digit=0 fallback for non-standard units.
- Cluster silhouettes are weak (0.10–0.16); families are dense cores in a continuum.
- Parent–child linkage used PENDANT_FROM→CORD_ID mapping with CORD_LEVEL filtering; hierarchy semantics of levels 3+ at Inkawasi not independently validated.
