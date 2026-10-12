# Binary Color Switch Test: Is "Mixed vs Solid" Itself Meaningful?

**Question (Charles):** Does the distinction between two-color and single-color cords function as a binary switch — a flag independent of the specific colors?

**Answer: No.** "Mixed vs solid" is redundant with color identity. It is not a separate signaling channel.

## The decisive tests

### 1. Two-color status changes only when the color changes: 6777 to 9

Across 38,854 level-1 pendant cords, every adjacent-cord transition where two-color status flips was checked against whether FULL_COLOR also changed:

- 6,777 transitions: two-color status change **coincides** with a color change
- 9 transitions: two-color status changes **alone**

All 9 exceptions are database coding artifacts (e.g., `LB-BL` vs `LB:BL` for the same visual color, `KB:W` recorded with both `:` and empty operators on adjacent cords, three-color cords like `W:AB:PB`). There are **zero genuine cases** of the switch flipping independently.

### 2. Color blocks are uniform in mixed/solid status: 1758 to 2

1,760 color blocks (≥3 consecutive cords of identical FULL_COLOR) across 186 quipu:

- 1,758 blocks: every cord in the block shares the same two-color status
- 2 blocks: mixed status within the block

The switch operates at the **color-block level**, never the cord level. A block is either a mixed color or a solid color — the way a block is either blue or brown.

### 3. No independent correlates

| Test | Result |
|---|---|
| Recto/verso alignment (n=78 quipu) | mean diff −0.01 — none |
| Position deciles | flat ~20% across all deciles — none |
| Section starts (n=798) | 20.3% vs 20.7% baseline — none |
| Knots per cord | 2.25 vs 2.21 — none |
| Subsidiaries per cord | 0.34 vs 0.35 — none |
| First cord | 16.7% (slightly below 21.3% avg) |
| Last cord | 21.1% (at average) |

### 4. Two-color cords cluster — but only because colors cluster

Adjacent two-color excess of +3.67 over chance (n=331 quipu) initially looked like grouping behavior. But 974 of 1,355 multi-cord runs mix different FULL_COLORs, and the Santa case shows why: on Santa 1000271, 6-blocks alternate between solid (W×6, AB×6, RB×6) and mixed (MB:W×6, LK:AB×6, RB:W×6) — each block uniform, the *blocks* alternating. The clustering is color-block structure, not an independent switch.

## What "mixed" actually is

Mixedness is an **attribute of the color**, like hue — not a flag applied to it. The khipukamayuq's palette contained entries like `MB:W`, `KB:W`, `AB:W` as distinct color choices. Selecting `MB:W` is selecting a color, the same act as selecting `MB`.

Consequences:

- **Site variation** (Santa 36.5%, Atarco 0%, Playa Miller 57%, Pachacamac 24.7%, Inkawasi 13.0%) reflects **palette composition** — which colors each office/scribe stocked — not a switch being thrown more often. This is consistent with the earlier finding that two-color rates reflect fiber supply and production practice.
- **Form A (tally strips)** uses fewer mixed colors (10.9%) — small simple documents use simpler palettes.
- **Block-level content differences are negligible**: mixed blocks average 1.81 knots/cord vs 2.05 for solid; 0.39 vs 0.34 subsidiaries. Too small to be a content signal; likely reflects which colors get mixed (often white-paired, often used in headers/labels).

## Bottom line

Charles's hypothesis is falsified in its strong form. There is no binary "mixed vs solid" channel operating independently of color. The Inca color system is a single palette in which some entries happen to combine two hues. The switch Charles was looking for does not exist — but the palette-composition differences across sites (the *choice* of how many mixed colors to stock) remain real production-level variation.

## Method notes

- 38,854 level-1 pendant cords, 582 quipu with ≥5 cords; two-color = OPERATOR_1 in (`:`,`-`) or non-empty COLOR_CD_2; 8,042 two-color (20.7%).
- Fixed a truthiness bug in an early pass (`or` returning the operand instead of bool); all reported numbers from the clean rebuild.
- knot_cluster.TOTAL_VALUE is unpopulated (0/NULL); knot counts per cord used as the value proxy.
- FULL_COLOR string collisions (e.g., `LB-BL` vs `LB:BL`) are recorder inconsistencies, verified by inspection of all 9 exceptions.
