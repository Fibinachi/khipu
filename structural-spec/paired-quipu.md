# Paired/Bundled Inkawasi Quipu: Numerical Relationship Analysis

**Date:** 2026-10-10
**Question (Charles):** Several Inkawasi quipu were found physically paired. Is there a numerical relationship between them — summary vs detail, duplicate for verification, or audit cross-check?

## The Pairs

| Pair | Quipu A | Quipu B | Physical relationship |
|------|---------|---------|----------------------|
| 1 | 1000605 (UR264) | 1000606 (UR265) | Tied together by a single cord; long incomplete + short complete |
| 2 | 1000628 (JC004) | 1000629 (JC005) | 1000628 has "knotted attachment on JC 005" |
| 3 | 1000603 (UR262) | 1000604 (UR263) | Wrapped together; UR262 described as "smaller" |

## Structural Comparison

| Pair | A: pendants | B: pendants | A: subsidiaries | B: subsidiaries |
|------|-------------|-------------|-----------------|-----------------|
| 1 | 211 | 14 | 2 | 10 |
| 2 | 18 | 149 | 11 | 43 |
| 3 | 138 | 236 | 247 | 1 |

In every pair, the two quipu are dramatically different in scale and architecture. These are not duplicates.

## Finding 1: No summary/detail relationship

Knot-type patterns show minimal overlap between paired quipu:
- Pair 1: 2 of 3 unique patterns in B appear in A (but B has only 3 patterns total — too few to be meaningful)
- Pair 2: 1 of 2 patterns overlap
- Pair 3: 3 of 34 unique patterns overlap

The pairs do not share enough structural similarity for one to be a summary of the other. They are different documents recording different things.

## Finding 2: Attachment direction splits by pair (Pair 2)

The most striking finding:

| Quipu | Recto (R) | Verso (V) |
|-------|-----------|-----------|
| 1000628 (JC004) | 0 | **18 (all)** |
| 1000629 (JC005) | **148** | 0 |

JC004 hangs **entirely** from the verso side; JC005 hangs **entirely** from the recto side. They are mirror images.

For comparison:
- 1000605 + 1000606: both all recto (no split)
- 1000603: all recto; 1000604: mixed (128 R, 108 V)

The R/V split does **not** encode debit/credit — values do not balance between sides (tested separately; ratios range from 0.01 to 2876). But the systematic all-R vs all-V pairing in JC004/JC005 suggests attachment direction distinguishes **document type or administrative function**, not accounting sides.

Notably, 1000604 (UR263) is the only quipu in the set with substantial mixed R/V (128/108) — and it was wrapped together with 1000603 (all R). The mixed quipu may itself contain two sub-documents distinguished by attachment side.

## Finding 3: Blue cords mark position, not value (1000605)

The 12 BL:AB cords in 1000605 appear at strikingly regular intervals:

**Cords 6, 12, 18, 24, 30, 36, [43], 55, 60, 66, 77, 82**

Roughly every 6th cord. Their knot contents vary (some blank, some S-clusters, some E+L) — blue does not mark specific values. It marks **position**: a periodic visual divider, like ruled lines every 6 rows in a ledger.

This is consistent with blue as a structural/formatting device rather than a commodity code, at least in this quipu.

## Finding 4: Colors differ between pairs

- **Pair 1:** 1000606's palette (MB, AB) is a subset of 1000605's broader palette. Consistent with the smaller quipu being related but simpler.
- **Pair 2:** Sharply different palettes. 1000628 uses RL, FB, GL, GG; 1000629 uses YB, NB, FB, AB. Minimal overlap beyond FB/NB.
- **Pair 3:** Both NB/AB dominant, similar family. Most color-compatible pair.

## Interpretation

The paired quipu are **not** cross-checks, duplicates, or summaries of each other. They are distinct documents that were stored or transported together — possibly because they relate to the same administrative event, time period, or responsible official.

The physical pairing (tied, wrapped, knotted together) is an **archival** relationship, not an **accounting** relationship. Think: two reports from the same quarter filed together, not two copies of the same report.

The JC004/JC005 recto/verso mirror is the most intriguing finding — it suggests the Inca used attachment side as a document-level classifier. What the classification means (tribute vs census? incoming vs outgoing? two moieties' records?) cannot be determined from this data alone.

## Limitations

- NUM_TURNS, KNOT_ORDINAL, and CLUSTER_ORDINAL are empty for Inkawasi quipu in the OKR database — precise decimal decoding of L-knots was not possible. Comparisons used knot-type patterns, not exact values.
- Only 3 pairs identified from excavation notes; there may be additional physical associations not documented in the NOTES field.
- The UR ID to OKR ID mapping for UR265 → 1000606 is inferred from shared museum number (12703-2014) and the "Attached to UR264" note, not explicitly confirmed.

## Bottom Line

Paired quipu are filed together, not calculated together. The physical bundling reflects archival practice — keeping related documents together — not audit procedure. The real discovery is the systematic recto/verso split in Pair 2 and the periodic blue positioning in 1000605, both of which reveal previously unrecognized structural conventions.
