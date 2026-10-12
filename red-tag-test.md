# Red Cord Test: Tag vs. Divider vs. Commodity

**Date:** 2026-10-10
**Question:** Do red cords function as positional tags marking state/imperial authority?

## Hypothesis under test (Charles)

If red marks state/imperial authority, it should appear as a **tag** — in specific structural positions (first cord, top cord, header) rather than scattered randomly. Like a stamp saying "this is tribute."

Follow-up hypothesis: red might mark **partitions/sections** rather than tagging the whole document — sitting at boundaries between cord groups, like "this section is the king's share."

## Data

Open Khipu Repository (`okr-khipu.db`): 619 quipu, ~54K cords. Red tier split:
- **Strong reds** (tag candidates): SR (strong red), RM (moderate red), R (dark reddish orange)
- **Reddish browns** (ecological, for comparison): RB, RL, RD, R0

## Finding 1: Document-tag hypothesis FALSIFIED

Strong-red cords show **no positional bias** toward document start:

| Position | Observed | Null (uniform) |
|----------|----------|----------------|
| First decile | 12.9% | 10% |
| Last decile | 10.5% | 10% |
| Middle 80% | 76.6% | 80% |

Only 6 of 171 positioned red cords are the actual first pendant. Zero red cords on top cords (primary cord). Red is not a header stamp.

## Finding 2: Red cords are the same length as everything else

Median red-to-median-other length ratio: **1.00** (n=167). A physical tag (like a shorter marker cord) would differ in length. Red cords are structurally identical to their neighbors — the signal is purely chromatic.

## Finding 3: Red is overwhelmingly singleton — the divider signature

| Color | Singleton runs | Total runs | % singleton |
|-------|---------------|------------|-------------|
| SR (strong red) | 24 | 24 | **100%** |
| RM (moderate red) | 70 | 78 | **89.7%** |
| R (dark reddish orange) | 25 | 30 | 83.3% |
| W (white, undyed) | 2,216 | 3,758 | 59.0% |
| AB (light brown) | 1,776 | 2,737 | 64.9% |
| MB (moderate brown) | 1,655 | 2,437 | 67.9% |
| YB (yellowish brown) | 409 | 758 | 54.0% |

Commodity colors appear in multi-cord runs (you need several cords to record several entries of the same commodity). **Strong red never does.** 24 out of 24 SR runs are single cords. A color that always appears alone, between groups of other colors, is a divider — not a commodity.

## Finding 4: Red sits between different sections

Of 120 red cords at color boundaries in multi-color quipu:
- **81 (67.5%)** separate two *different* non-red colors
- 40 (32.5%) separate the same color on both sides

Red disproportionately appears at transitions between distinct sections, not as decoration within a uniform run.

## Finding 5: Weak value-regime signal

Red cords sit at order-of-magnitude value shifts 58.4% of the time vs 49.1% expected by chance. Modest elevation, consistent with section boundaries (different sections, different value scales). Not strong enough to stand alone, but corroborating.

## Finding 6: Red and E-E-E are independent systems

Only **1 of 46** quipu with strong-red cords also contains an E-E-E marker sequence. The two candidate "tagging" devices almost never co-occur. They are likely complementary, not redundant:
- **E-E-E** = label/header marker (appears at cord starts, per-entry or per-group)
- **Red singleton** = section divider (appears between groups)

Two different structural devices doing two different jobs.

## Interpretation

Charles's tag hypothesis is half-right. Red does mark something structural — but not the document. It marks **sections within the document**.

The refined model:
- **Knots** = how many (universal numerical system)
- **Colors** = what commodity/category (ecological patterning)
- **Red singleton** = section divider ("this section is distinct" — possibly the state/imperial share, per the frontier/Pachacamac finding)
- **E-E-E** = entry/group label

A quipucamayoc reading a quipu would see: color-banded sections of commodity entries, separated by red dividers, with E-E-E markers labeling specific entries. The red divider is the visual equivalent of a ruled line between ledger sections.

## What would confirm "the red section is the state's share"

1. **Inkawasi commodity mapping** (Chu's excavation records): if red-divided sections correspond to specific products (e.g., the imperial tribute goods vs. local storage), the divider's meaning is identified.
2. **Santa Valley tribute census**: the six matched quipu — do red dividers separate tribute categories?
3. **Value analysis**: are red-delimited sections systematically larger/smaller values than adjacent sections? (A "king's share" might be a fixed proportion.)

## Limitations

- Knot-value decoding used a simplified Ascher scheme; proper decimal decoding might shift the value-boundary result.
- 35 quipu with strong-red level-1 pendants is a modest sample.
- "Red" as a perceptual category spans SR/RM/R; the 100% singleton rate is specific to SR (n=24 runs).
- RL (light reddish brown) also shows high singleton rate (89.7%) — the reddish family may share divider function, or RL may be faded red. Dye analysis could resolve this.
