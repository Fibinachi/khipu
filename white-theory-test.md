# White-Theory Test: Does "white = unimportant source" hold corpus-wide?

**Theory under test:** White cord color marks sources too small/insignificant to merit
color-marking. The keeper spends color (the expensive signal) on significant depositors;
small ones get white — counted but not distinguished.

**Origin:** Inkawasi subsidiaries showed white median value 1 vs colored median 21
(n=59 white, 165 colored, nonzero decoded values). Reproduced exactly in this run.

**Scope:** 51,147 cords across 593 non-funerary quipu (26 funerary excluded).
NULL decode rate 8.2% corpus-wide (vs 41% at Inkawasi — other sites have NUM_TURNS data).
Methods: CORD_LEVEL for hierarchy, CORD_ORDINAL for order, type-aware decoder
(L-turns=units, S-counts=tens+). White-involved = W as a color component; colored =
recorded color with no W; missing = no color record (kept separate).

---

## Test 1: Corpus-wide subsidiary value test — FAILS

Subsidiary cords (level > 1), nonzero decoded values, all 593 quipu:

| Color     | n    | median | mean |
|-----------|------|--------|------|
| white     | 2641 | 3      | 121  |
| colored   | 4681 | 3      | 237  |
| missing   | 24   | 12     | 45   |

Medians are **identical** (3 vs 3). Mann-Whitney: white is not stochastically less
than colored (z=+4.21, one-sided p=1.0). The mean gap (121 vs 237) is a tail effect,
not a location shift — colored has a heavier right tail, but the typical white and
typical colored subsidiary are the same size.

By cluster family:

| Cluster | white (n, med) | colored (n, med) | MW p (white<colored) |
|---------|---------------|-------------------|----------------------|
| 2 census_format_paired | 327, 2 | 819, 2 | 0.73 |
| 3 large_value_flat | 28, 9 | 69, 37 | 0.51 |
| 4 deep_hierarchical_grouped | 1450, 6 | 2341, 5 | 1.00 |
| 5 deep_sparse_mixed | 836, 2 | 1452, 2 | 0.33 |

No cluster family reproduces the Inkawasi pattern. The effect is Inkawasi-specific.

## Test 2: White gradient by level — FAILS corpus-wide

White-involved % by CORD_LEVEL, all 593 quipu:

| Level | n     | white % | colored % | missing % |
|-------|-------|---------|-----------|-----------|
| 1     | 36816 | 39.8    | 56.9      | 3.3       |
| 2     | 12431 | 36.3    | 63.1      | 0.6       |
| 3     | 1480  | 42.1    | 57.2      | 0.7       |
| 4     | 238   | 48.7    | 50.8      | 0.4       |
| 5     | 23    | 60.9    | 39.1      | 0.0       |

No monotonic decrease. If anything white **increases** with depth (39.8% → 48.7%
at level 4). The Inkawasi gradient (36% → 4%) is a local phenomenon, not a general
administrative rule. (156 cords carry negative levels, -2/-1, concentrated in 5
quipu — likely a top-cord convention; too few to affect results.)

## Test 3: White mains vs white subsidiaries — HOLDS STRONGLY

| Group | n    | median | mean |
|-------|------|--------|------|
| white level-1 (mains) | 7383 | 11 | 516 |
| white level>1 (subs)  | 2641 | 3  | 121 |

Mann-Whitney: white subsidiaries stochastically less than white mains,
z=-25.8, p<0.0001. This is the one piece of the theory that generalizes:
house stock dwarfs rider stock even when both are white. The structural fact
(mains > subsidiaries) holds independent of color semantics.

## Test 4: Confound check (within-level) — FAILS

The critical control: within a single level, does white vs colored separate by value?

| Level | white (n, med) | colored (n, med) | MW p (white<colored) |
|-------|---------------|-------------------|----------------------|
| 2     | 2223, 3       | 4181, 3           | 0.998                |
| 3     | 339, 5        | 431, 3            | 1.000                |

No separation. At level 3 the white median is actually *higher* (5 vs 3).
"White = small" is not hiding behind a level confound — it simply isn't present
outside Inkawasi at any level.

## Test 5: Census-format check — FAILS

Cluster 2 (census_format_paired, n=250 quipu) subsidiaries:
white median 2 (n=327) vs colored median 2 (n=819), MW p=0.73.
White % by level within census format: L1 35.4%, L2 25.7%, L3 35.5% — no gradient.
The theory does not transfer to census-type documents at all.

---

## Verdict

| Test | Result |
|------|--------|
| 1. White subsidiaries < colored, corpus-wide | **FAILS** — medians identical (3 vs 3) |
| 2. White gradient (enriched at L1) | **FAILS** — flat/rising corpus-wide (40%→49%) |
| 3. White mains > white subsidiaries | **HOLDS** — median 11 vs 3, p<0.0001 |
| 4. Within-level white/colored separation | **FAILS** — no separation at L2 or L3 |
| 5. Theory transfers to census format | **FAILS** — no effect in cluster 2 |

## Interpretation

The "white = unimportant source" reading is **an Inkawasi-local scribal convention,
not a general khipu grammar.** At the Inkawasi warehouse the keepers operated a
triage system: color-mark the significant depositors, white-mark the small ones
(median 1 vs 21). Everywhere else, white is simply a frequent color (~40% of cords
at every level) with no value significance.

What generalizes is structural, not chromatic: main cords carry larger values than
subsidiaries regardless of color (Test 3). The house-vs-rider distinction is real
corpus-wide; the white-as-triage marking is how one warehouse chose to signal it.

**Strongest alternative for the failures:** White is the default cord color —
cheap, undyed cotton — and its meaning is set locally by each administrative
context. At a multi-party warehouse, "default" gets recruited as "not worth
marking." In census records, where color marks household/category rather than
source importance, white carries no triage meaning because there is nothing to
triage. The color's semantics are downstream of the document type, not fixed.

## Caveats

- 8.2% NULL decode rate corpus-wide; Inkawasi units digits remain unrecoverable.
- Heavy value ties (1, 2, 3, 10, 20) from the decoder limit MW test power; medians
  are the more reliable comparator and they are equal outside Inkawasi.
- Cluster 3 (large_value_flat) shows a white<colored median gap (9 vs 37) but
  n=28/69 is too small for significance (p=0.51) — worth revisiting with more data.
- Negative CORD_LEVEL values (-2, -1; 156 cords, 5 quipu) not investigated.
