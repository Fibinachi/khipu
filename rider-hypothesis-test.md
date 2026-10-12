# Rider Hypothesis Test — Inkawasi Warehouse Quipu

**Date:** 2026-10-11
**Scope:** 18 Inkawasi quipu (OKR 1000597–1000614). 3,083 cords; 735 parent cords with 1,086 subsidiaries.
**Hypothesis:** Level-1 cords = house (warehouse's own) inventory; subsidiary "rider" cords = separate inventory from another source, co-located for administrative convenience. Subsidiaries are NOT detail of the parent.

**Method:** Hierarchy via CORD_LEVEL; parent linkage via PENDANT_FROM→CORD_ID (verified: 0 orphans); cord order via CORD_ORDINAL; values via type-aware decoder (`decoder.py`). All Inkawasi L-knots lack NUM_TURNS → units digits unrecoverable; all value tests use tens-and-up. 41.3% of cords decode NULL.

---

## Test 1: Color contrast — SUPPORTS rider hypothesis

- 69.1% of subsidiaries carry a **different** color than their parent (748/1,083 with color data).
- Null (reshuffled colors within quipu, 1,000 reps): mean 62.7%, sd 1.4%.
- **P < 0.001** — zero of 1,000 null draws reached the observed rate.
- Subsidiaries are systematically marked as *not-parent*. Under the old additive-detail model there is no reason for this; under the rider model it is the core prediction (rider goods visibly distinguished from house goods).

## Test 2: Value independence — SUPPORTS rider hypothesis

- 243 parent cords with fully decodable parent + subsidiary values.
- Correlation(parent value, summed subsidiary values): **r = 0.143** — essentially independent.
- Exact nonzero parent==subsidiary-sum matches: 16/243 (6.6%), consistent with coincidence at small values.
- Integer ratios: only the 16 exact matches (ratio 1); one ratio-4, one ratio-3. No systematic multiple.
- No summation, no ratio, no correlation. The two sets of numbers are unrelated stocks.

## Test 3: Subsidiary internal patterns — NEUTRAL, data-limited

- Top values are nearly identical across levels: L1 = {1, 10, 20, 101, 11, 1201…}, Sub = {1, 10, 20, 11, 21, 601…}.
- No distinct subsidiary value signature. This is *consistent* with rider = more of the same commodity (quantities, not a different document type), but does not discriminate between models.
- **Data limit:** Urton & Chu's repeating values (15/10/47/208) cannot be checked — without NUM_TURNS, 15→1x and 47→4x are unrecoverable; only the tens digit survives. The published values came from handling the physical quipu.

## Test 4: Compound enrichment revisited — MIXED

- Subsidiary compounds sharing ≥1 color with parent: 52.0%; sharing none: 48.0%. A coin flip.
- Under a strong "compound = external origin" reading, we would expect systematic difference. Not found.
- Qualitative note: examples show NB parents with AB:KB / AB:GG / MB:KB subsidiaries — subsidiaries *introduce* colors (KB, GG) absent from the parent. Suggestive of external marking, but not systematic enough to claim.
- Verdict: compounds mark *something* about subsidiaries (enrichment with depth is real: 13.6%→34.8%), but "origin" specifically is not established.

## Test 5: Commodity split — SUPPORTS rider hypothesis, with variation

Color-contrast rate (subsidiary ≠ parent) by quipu:

| Quipu | Commodity | Contrast |
|---|---|---|
| 1000607 | peanut | 93% |
| 1000610 | peanut | 84% |
| 1000611 | peanut | 95% |
| 1000612 | peanut | 89% |
| 1000614 | peanut | 48% |
| 1000608 | chili | 50% |
| 1000609 | chili | 64% |
| 1000597 | chili (inf) | 50% |
| 1000598 | chili (inf) | 50% |
| 1000613 | beans | 88% |

- Peanut and bean quipu show very high contrast (84–95%); chili quipu sit near 50–64%.
- The rider pattern is commodity-dependent: peanut/bean storage involved heavy outside deposits; chili less so. Plausible — different supply chains, different depositor structures.
- 1000614 (peanut, 48% contrast) is the outlier — and it was the peanut quipu assigned to cluster 5 (deep_sparse_mixed) rather than cluster 4. Structural and color evidence agree it is the odd one out.
- **Hierarchy profiles explained:** 1000611 (289 L1 / 41 sub) vs 1000612 (162 L1 / 219 sub). Under the old model this heterogeneity was a puzzle. Under the rider model it is natural: different house-to-rider ratios. 1000612 holds more deposited stock than own stock; 1000611 is mostly house inventory.

## Test 6: White gradient — QUALIFIED support

- White-involved cords: 36.3% (L1) → 20.7% (L2) → 9.8% (L3) → 4.3% (L4). Steep, real.
- But white is **not** absent from subsidiaries: 185 white-involved L2 cords, including **50 under colored (non-white) parents**.
- 152 white subsidiaries sit under white parents (consistent with house-detail or house-riders); 50 under colored parents complicate a clean "white=house, color=rider" split.
- Possible readings: (a) some riders are state goods (white riders under colored parents); (b) white marks something other than ownership at subsidiary level; (c) mixed practices.
- The gradient is the strongest structural signal in the data, but its *meaning* remains underdetermined.

---

## Verdict

**The rider hypothesis explains the Inkawasi structure better than the additive-detail model.** The additive model is dead: no summation, no correlation (r=0.14), no ratios. The rider model correctly predicts the two strongest findings — systematic color contrast (p<0.001) and value independence — and naturally accommodates the heterogeneity (cluster split, hierarchy-profile differences, commodity variation) that the old model could not.

**What the rider model does not yet explain:**
1. Compound semantics — enrichment with depth is real but "origin marking" is unproven (50/50 split).
2. White subsidiaries under colored parents (50 cases) — needs a sub-hypothesis (state riders?).
3. Why chili shows ~50% contrast vs ~90% for peanut/beans — supply-chain story is plausible but untested.

**Untestable with current data:**
- Full quantitative relationships (units digits gone — 41% NULL decode; need physical re-examination or NUM_TURNS recovery).
- Urton & Chu's repeating values 15/47/208 (tens-decode only).
- Whether "rider" = outside depositors vs. another institution's stock vs. state allocations — the data shows *separateness*, not *whose*.

**Bottom line:** Subsidiaries are separate stocks, not detail. The quipu is a co-location device: house inventory on the main cords, other parties' goods riding along, distinguished by color. The warehouse was a custodian, not just an owner.
