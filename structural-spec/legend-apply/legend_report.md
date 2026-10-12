# Legend Report: Does 1000368's Color-Combination Legend Generalize?

**Date:** 2026-10-12
**Question:** 1000368 (ordinals 184-220) systematically enumerates 17 compound
colors (BS/W/DB × {DB, VB, 0G, KB, SR, SY}). Does this legend define a vocabulary
used across the corpus?

## Verdict: NO — the legend is local to 1000368.

Three independent tests, all negative:

### Test 1: Compound overlap (295 cords in 8 pairs, 9 pairs absent)
Of the 17 legend compounds, 9 appear **nowhere else** in the 619-khipu corpus:
W+VB, BS+DB, BS+VB, BS+0G, BS+SR, BS+SY, DB+VB, DB+0G, DB+SY.

The 8 that do appear total 295 cords, dominated by:
- W+KB (141): KB is the 4th most common modifier corpus-wide — coincidental
- W+SR (69): 68 of them in a single khipu (1000096)
- The rest are singletons or near-singletons

### Test 2: Enumeration format (unique to 1000368)
A corpus-wide SQL scan for the legend's *format* — blocks of 4+ consecutive
cords sharing color1 with distinct color2 modifiers — found **exactly one
khipu: 1000368**. No other document defines compound vocabulary this way.

### Test 3: Heaviest user is a chance overlap
1000096 (Lluta Valley, 2,210 cords, 22 distinct compounds) shares 5 legend
pairs. But at 2,210 cords with 22 compound types, 5 overlapping pairs is
expected by chance. The pairs are scattered (not in definition blocks) and
behaviorally indistinguishable from each other.

## What the legend IS

A **local vocabulary definition** for a single document. The khipukamayuq who
made 1000368 defined their compound-color shorthand inline, in multiple
enumeration blocks throughout the khipu (ordinals ~22, 40, 59, 97, 112, 119,
144, 154, 161, 169, 178, 184-220, 204, 211, 218, 237, 245) — not just at
184-220.

**1000368 is a self-documenting file.** It interleaves vocabulary definitions
with journal entries. Each definition block introduces the compound colors
used in the following section. This is the bureaucratic equivalent of defining
abbreviations at the top of each memo section.

## What pops out (the real finding)

The legend doesn't transfer — but the *practice* is the discovery:

1. **Compound colors are office shorthand.** 1000368's maker needed 17 compound
   codes and defined them inline. Other offices would have their own compounds,
   defined their own way (or not at all).

2. **Look for definition blocks, not shared vocabularies.** The search for
   "which khipu use 1000368's compounds" was the wrong question. The right
   question: "which khipu define their own compounds inline?" The SQL pattern
   (4+ consecutive same-base/different-modifier) is now a reusable detector
   for self-documenting khipu.

3. **1000096 deserves a second look.** It uses 5 legend-like pairs scattered
   across 2,210 cords. If it has its own definition blocks (with different
   compounds), it's another self-documenting file from a different office.

## Deliverables
- `legend_vocab.csv` — 21 pairs from 1000368 ordinals 175-225
- `compound_overlap.csv` — all 612 khipu scored
- `top_legend_users.md` — top 20 by overlap
- `compound_distinctness.md` — distinctness analysis
- `legend_report.md` — this file
- `scan_corpus2.py` — reproducible overlap scan
