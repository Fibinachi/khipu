# The ABCs: Generative Grammar of Khipu

## What are the ABCs?

**28 primitives + 7 composition rules** from which all 612 khipu can be generated.

### Color Primitives (15 → 64)

Not 64 arbitrary colors. **10 families × 5 intensities**:

| Family | Name | Colors | Share |
|--------|------|--------|-------|
| B | Brown | 22 | 58% |
| A | White | 1 | 26% |
| G | Green | 7 | 3% |
| H | Blue | 7 | 2% |
| Z | Black | 3 | 2% |
| M | Gray | 8 | 2% |
| L | Olive | 5 | 1% |
| R | Red | 4 | 1% |
| N | Orange | 4 | <1% |
| Y | Yellow | 3 | <1% |

The primitive is not "AB" — it's **[BROWN, LIGHT]**. Like phonology:
phonemes decompose into features. Colors decompose into [family, intensity].

Compounds via 6 operators: `-` (barber pole), `:` (mottled), `*`/`**`/`*_`
(special), `%` (con elemento).

### Knot Primitives (4)

| Symbol | Name | Function | Count |
|--------|------|----------|-------|
| S | Single | Decade unit (tens, hundreds...) | 75,055 |
| L(n) | Long (n turns) | Ones digit 2-9 | 26,380 |
| E | Figure-eight | Ones digit 1 | 8,356 |
| TF | Tufted | Unary tally (each = 1) | 128 |

**Is L(7) one primitive or seven?** One parameterized primitive.
Evidence: turns distribution drops sharply at 9 (decimal boundary).
If it were 7 independent twists, no boundary would exist.

**Is E a degenerate L?** No — distinct motor operation (figure-eight vs
wrapped turns). Treated as separate primitive.

### Positional Primitives (3)

1. **Sequence** (CORD_ORDINAL): linear order. Almost unconstrained
   (102/121 family bigrams legal).
2. **Hierarchy** (CORD_LEVEL 1-6): nesting. 71% L1, 25% L2, 3% L3.
3. **Cluster** (decimal place): S-knot grouping. 1-7 clusters per cord.

### Composition Rules (7)

1. **Cord formation**: [color] + [knot pattern] + [position]
2. **Sequence**: any color follows any color
3. **Hierarchy**: depth ≤ 6, each level attaches above
4. **Repetition**: [marker?] [constants]* [variables]* repeated
5. **Delimiters**: white runs, value markers, color cycles (from same primitives)
6. **Document composition**: 4 types from same atoms
7. **Value encoding**: decimal XOR unary per khipu

## How Many Primitives?

| Category | Count |
|----------|-------|
| Color families | 10 |
| Intensity levels | 5 |
| Knot types | 4 |
| Positional | 3 |
| Operators | 6 |
| **Total** | **28** |

28 primitives + 7 rules → 612 khipu.

## What's the Learning Order?

Evidence from restricted-primitive khipu:

**Day 1: The knot.** 34 khipu use a single knot type. The motor skill —
tying S, L, E — comes first. You learn to make the marks before you
learn what they mean.

**Day 2: The number.** Decimal encoding (S-clusters + L/E ones).
Or unary (TF tufts) for simple tallies. 1000522 (checklist) uses
only TF — the simplest number system.

**Day 3: The color.** 42 khipu use a single color. Color-as-key is
a separate learning step from knot-as-value. White (A) first —
it's the default, the undyed baseline.

**Day 4: The sequence.** 208 khipu are flat (level 1 only).
Linear order before hierarchy.

**Day 5: The hierarchy.** Subsidiaries (levels 2-3). Nesting.

**Day 6: The template.** Repetition with variation. Constants vs
variables. The form concept.

**Day 7: The document.** Combining templates, delimiters, sections
into complete administrative records.

This is inferred from simplicity gradients, not direct evidence.
But the 55 minimal khipu (≤2 colors, ≤2 knot types, flat) cluster
at 1-10 cords — they look like exercises or fragments, not full
documents.

## What Did the Teacher Teach on Day One?

**How to tie a knot.** Not what colors mean, not how to lay out a
table, not the decimal system. The motor skill. S, L, E — the hand
learns before the mind.

The ABCs aren't "white means X." They're: *this is how you wrap
cord around cord to make a turn. Do it seven times. That's seven.*

Everything else — colors, templates, documents — is built on
trained hands.
