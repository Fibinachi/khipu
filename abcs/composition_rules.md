# Composition Rules

Induced from 612 khipu, 54,403 cords, 110,677 knots.

## Rule 1: Cord Formation

A cord = [color] + [knot pattern] + [position].

- **Color**: One canonical color (64 options) decomposing to [family (10), intensity (1-5)].
  Optionally compound via operators (-, :, *, **, *_, %).
- **Knot pattern**: One of:
  - `(S-cluster)* (L|E)?` — decimal number. S-clusters (1-7) = tens through millions.
    L(n) with n=2..9 turns = ones digit. E = ones digit 1. Empty ones = 0.
  - `(TF)*` — unary tally. Each tuft = 1. No place value.
  - Empty — no knots. Structural (separator, placeholder, unchecked).
- **Position**: CORD_ORDINAL (sequence), CORD_LEVEL (1-6 hierarchy).

**Violations**: None found. Every cord conforms. L knots with >9 turns are
vanishingly rare (75 at 10, then near-zero) — the decimal boundary is enforced.

## Rule 2: Sequence

Cords are ordered by CORD_ORDINAL. At the color-family level, 102/121
possible bigrams occur. The 19 missing are all involving rare families
(Y, R, N) — absence due to rarity, not prohibition.

**Effective rule**: Any color can follow any color. Sequence carries
*document* structure (tables, journals), not *grammatical* constraints.

## Rule 3: Hierarchy

- Level 1: Primary pendants (71% of cords). Attach to main cord.
- Level 2: Subsidiaries (25%). Attach to Level 1 cords.
- Level 3: Sub-subsidiaries (3%). Attach to Level 2.
- Levels 4-6: Rare (<1% combined). Maximum observed depth: 6.
- Negative levels (-1 to -3): 232 cords. Purpose unclear — possibly
  top cords or repair attachments.

**Rule**: Depth ≤ 6. Each level attaches to the level above.
Subsidiaries typically share the parent's color family (not yet quantified).

## Rule 4: Repetition (Templates)

The fundamental composition operation. A template = [marker?] [constants]* [variables]*
repeated N times.

- **Marker**: Optional opening signal. Can be a value (BY=22), a color,
  or a white run. Identifies row/batch start.
- **Constants**: Fixed color+value at fixed positions across repetitions.
  These define the form.
- **Variables**: Positions where values differ across repetitions.
  These carry the data.

**Smallest repeating unit**: A single cord (color + knot pattern).
Templates are built by repeating multi-cord units.

**Corpus finding**: 113 khipu have strong templates. All 113 are unique.
Repetition is universal; specific templates are not.

## Rule 5: Delimiters

Three delimiter primitives identified:

1. **White runs** (3+ consecutive white cords): Section boundaries.
   Used in journals (48 khipu) and checklists.
2. **Value markers** ((color, value) repeating at intervals): Row/batch markers.
   Used in tabular khipu (119 khipu). E.g., BY=22 every 12 cords.
3. **Color cycles** (repeating color sequence): Column structure.
   Used in tabular khipu (33 khipu). E.g., BL→BY→MB→W.

**Rule**: Delimiters are drawn from the same primitives (colors, values)
as content. There is no separate "punctuation alphabet." Context
(position, repetition) disambiguates marker from data.

## Rule 6: Document Composition

Four document types from the same primitives:

| Type | Composition |
|------|-------------|
| Tabular | [header] ([marker] [row])* — color cycle defines columns |
| Journal | [delimiter] ([entry] [delimiter]?)* [delimiter] — sequential entries |
| Checklist | [header] ([section] [white-sep])* — graded marks per category |
| Code | [symbol]* [punct]* — categorical sequence with punctuation |

**Key finding**: The generator produces all four types from identical
primitives. No type requires unique atoms. The ABCs are universal.

## Rule 7: Value Encoding

Two number systems, mutually exclusive per khipu:

1. **Decimal** (99% of khipu): S/L/E with positional clustering.
   Max 7 digits observed.
2. **Unary** (1000522 only): TF tufts, each = 1. Max 4 per cord observed.

**Rule**: A khipu uses one system. No mixing observed.

## Summary: The ABCs

**15 color primitives**: 10 families + 5 intensities → 64 colors.
**4 knot primitives**: S, L(n), E, TF (+ rare regional variants).
**3 positional primitives**: sequence, hierarchy (1-6), cluster (decimal place).
**6 operators**: -, :, *, **, *_, % (for compound colors).
**7 composition rules**: cord formation, sequence, hierarchy, repetition,
delimiters, document composition, value encoding.

Total: ~28 primitives + 7 rules generate all 612 khipu.
