# The Quipu Knot Alphabet

**Enumeration of every distinct knot symbol in the OKR corpus (110,677 knots)**

Date: 2026-10-10
Database: `okr-khipu.db` (knot table, knot_type_dc)

---

## The Alphabet

### Base Symbols (TYPE_CODE)

| Symbol | Name | Count | % of corpus | Standard function |
|--------|------|------:|------------:|-------------------|
| S | Single knot | 75,055 | 67.8% | Tens/hundreds/thousands by vertical position |
| L | Long knot | 26,380 | 23.8% | Digits 2–9 by number of turns |
| E | Figure-eight knot | 8,356 | 7.5% | Digit 1 |
| SP | Spiral knot | 247 | 0.22% | Coded as long knot (digit by turns) |
| TF | Tufted knot | 128 | 0.12% | Coded as positional (10/100/1000); value = 1 |
| EE | Double figure-eight | 75 | 0.07% | Coded as 1 (like E) |
| LL | Double long knot | 17 | 0.015% | Coded as long knot; "two axes" (Aschers) |
| BL | Belted long knot | 14 | 0.013% | Long knot with extra outer wrap; on UR035 |
| — | Uncoded (empty/NULL) | ~405 | 0.37% | Missing data |

### Direction Modifier (DIRECTION field)

Every knot also carries a direction: the slant of the knot (S = right-leaning, Z = left-leaning).

| Direction | Count | % of directed knots |
|-----------|------:|--------------------:|
| Z | 66,028 | 67.3% |
| S | 32,082 | 32.7% |
| U / unknown / null | ~12,567 | — |

**Direction is NOT random.** It correlates with knot type:

| Knot type | % S-direction | Interpretation |
|-----------|--------------:|----------------|
| S (single) | 26.4% | Z-dominant |
| L (long) | 52.4% | Balanced |
| E (fig-eight) | 27.3% | Z-dominant |
| SP (spiral) | 1.0% | Almost exclusively Z |
| EE (dbl fig-8) | 24.4% | Z-dominant |
| TF (tufted) | 100.0% | Exclusively S |

If direction were incidental (an artifact of handedness), it would be consistent across types or ~50/50. Instead, each knot type has a characteristic direction ratio. **Direction is part of the symbol.** The effective alphabet is at least 16 symbols (8 types × 2 directions), not 8.

This supports Urton's binary-coding hypothesis at the corpus scale: S/Z is a meaningful bit, not noise.

---

## Anomalies: Symbols That Don't Fit

### 1. Long knots with >9 turns

Standard decimal: L knots encode digits 2–9 via turns. But:

| Turns | Count |
|-------|------:|
| 10 | 75 |
| 11 | 43 |
| 12 | 19 |
| 13 | 11 |
| 14 | 2 |
| 15 | 2 |
| 16 | 1 |
| 20 | 1 |
| 23 | 1 |

A 23-turn "long knot" is not a digit. These concentrate on specific quipu: 1000314 (32 cords affected), 1000504 (29), 1000493 (29), 1000376 (18). Either data-entry errors, a distinct knot type miscoded as L, or a non-decimal use.

### 2. Long knots with 0 or NULL turns (4,673)

4,487 L knots have NULL turns; 186 have 0.0 turns. A 0-turn long knot is a contradiction — it may be an uncoded knot, a placeholder, or a different structure.

### 3. TF: the single-quipu knot

All 128 tufted knots appear on ONE quipu: 1000522 (Ica/Pisco, Berlin). 100% S-direction. No other quipu in the corpus uses TF.

This is either a local knot dialect (one maker's idiosyncratic symbol) or a specialized notation. The database assigns TF positional values (10/100/1000), treating it as a single-knot equivalent — but its exclusivity suggests it meant something specific to that recorder.

### 4. SP clusters on commodity quipu

Spiral knots are rare (247 total) but appear on the Inkawasi commodity quipu:
- **1000613 (beans, UR271):** all 8 SP knots on a SINGLE cord (cord ordinal 10), which is colored 0R (strong red)
- **1000608 (chili, UR267A):** all 10 SP knots on a SINGLE white cord
- **1000605 (blue quipu, UR264):** all 9 SP knots on a SINGLE MB cord
- **1000598 (inferred chili, UR256):** 1 SP knot on AB cord

SP knots are not distributed — they cluster on individual cords. On the bean quipu, they sit on a red cord (red = section divider elsewhere). Eight spiral knots on one red cord is not a number; it looks like a marker or label.

SP is 99% Z-direction, the inverse of TF's 100% S. The two rare types are directionally polarized.

### 5. EE: the solitary knot

Double figure-eight knots (75 total, across 25 quipu) frequently appear as the ONLY knot(s) on a cord:
- Multiple cords have exactly 1 EE as their sole knot
- Several have exactly 2 EE as their only knots

A solitary knot is not encoding a multi-digit number. EE may function as a marker, a "1" flag, or a non-numerical sign. The database assigns it value=1 (like E), but its positional isolation suggests otherwise.

### 6. LL: concentrated on the 40-section quipu

13 of 17 double-long knots are on 1000096 — the Lluta Valley quipu with 40 sections. The remaining 4 are scattered (1000635, 1000624, 1000382). LL may be a regional or idiosyncratic variant.

---

## Context-Specific Symbols

| Finding | Detail |
|---------|--------|
| Zero knots on primary cords | Confirmed: 0/110,677. Primary cords are knot-free by rule. |
| TF exclusive to 1000522 | Single-quipu symbol; Ica/Pisco |
| SP clusters on single cords | Not distributed; appears as cord-level marker |
| SP on red cord (beans) | 8 SP on one 0R cord of 1000613 — red + unusual knot type |
| LL concentrated on 1000096 | 76% on the 40-section Lluta quipu |
| BL on 4 quipu only | 1000504 (8), 1000279 (3), 1000514 (2), 1000317 (1) |

---

## The Effective Alphabet

Counting type × direction as distinct symbols (excluding uncoded):

**16 primary symbols:**
S-S, S-Z, L-S, L-Z, E-S, E-Z, SP-S, SP-Z, TF-S, TF-Z, EE-S, EE-Z, LL-S, LL-Z, BL-S, BL-Z

**Plus positional information** (which decimal place) **and turn count** (for L: 2–9+).

In practice, the working alphabet for 99.5% of knots is 6 symbols:
S-S, S-Z, L-S, L-Z, E-S, E-Z

The remaining 10 symbols (involving SP, TF, EE, LL, BL) constitute 0.5% of knots but are **non-randomly distributed** — they cluster on specific quipu, specific cords, and specific colors. They are the most likely carriers of non-numerical information.

---

## Implications for Decipherment

1. **Direction is a bit.** S/Z ratios vary systematically by knot type. Any decoding that ignores direction discards ~1 bit per knot.

2. **Rare types are signals, not noise.** SP, TF, EE, LL, BL cluster too tightly to be random variation. TF's single-quipu exclusivity and SP's cord-level clustering (especially on the bean quipu's red cord) suggest marker/label functions.

3. **The >9-turn L knots need re-examination.** Either the database has errors on specific quipu, or these are a distinct symbol. 1000314, 1000504, and 1000493 should be visually inspected.

4. **EE as solitary marker.** When a cord has only one double figure-eight knot, it's probably not the number 1 — it's a flag.

5. **The bean quipu's red cord with 8 spiral knots** (1000613, cord 10) is the single most anomalous knot-level feature found in the commodity-mapped quipu. If any knot pattern encodes commodity identity, this is the candidate.

---

## Limitations

- DIRECTION = 'U' (~8,000 knots) means undetermined; true S/Z ratios may shift.
- KNOT_ORDINAL and CLUSTER_ORDINAL are empty for Inkawasi quipu — positional analysis within cords was limited.
- NUM_TURNS is NULL for 4,487 L knots — digit values unknown.
- The database encoders forced all types into numerical values; non-numerical functions are inferred from distribution, not from decoder notes.
- No visual inspection of actual knots was performed; all analysis is from database records.
