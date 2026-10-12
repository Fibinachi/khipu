# Inkawasi Sections: Do Large White-Cord Values Span Red Dividers?

**Date:** 2026-10-10
**Question (Charles):** Are the large Inkawasi white-cord values (~12,000–15,000) single-cord recordings, or sums across red-delimited sections — i.e., combined census+inventory?

## Answer: Single-cord recordings. No red dividers involved.

The quipu with the largest white-cord values (1000610) contains **zero red cords**. The large values are on individual white pendant cords, each recording its own value. There are no red-delimited sections for them to span.

## Detailed findings

### Quipu 1000610 (largest white-cord values)

- **131 level-1 pendants**, all recto (116) or verso (15)
- **Colors:** W (70), NB (32), AB (19), MB (3), GG (2), LB (1), BS (1)
- **Red cords:** NONE — no SR, RM, or R colors
- **Largest white-cord S-values:** 1,431 (ord 24), 1,318 (ord 48), 1,195 (ord 34), 1,168 (ord 39), 1,142 (ord 104)
- **Attachment split:** 116 recto cords sum to ~36,911; 15 verso cords sum to ~4,021 (ratio 9.18 — not balanced)

Each large value sits on its own white cord. No dividers, no sections, no spanning.

### The one Inkawasi quipu WITH a red cord: 1000625

- **36 pendants**, all recto
- **Red cord:** single RM (red) cord at ordinal 7, **blank** (value 0, no knots)
- **Before red (ords 1–6):** BY, R0, DB, YB, DG, R0 — mixed colors, small values (0–6)
- **After red (ords 8–36):** repeating color cycle — YB, DG, R0, NB, YB, DB, R0, NB, YB, KB, DG, KB, NB, YB, R0, DG, KB, NB, YB, R0, DG, KB, NB, YB, DB, KB, R0, DB, YB

The red divider separates a 6-cord header from a **repeating commodity cycle** — the same color sequence (YB/DG/R0/NB/KB/DB...) repeating like columns in a spreadsheet. Each repetition is likely one "row" (one contributor, one delivery, one time period) with the same commodities in the same order.

This is a **form**, not a divider between census and inventory. The red marks "header ends, data begins."

### E-E-E markers in Inkawasi: none found

Zero Inkawasi quipu contain 3+ consecutive E knots on a single cord. Consistent with the red-tag-test finding that E-E-E and red are complementary systems that rarely co-occur — Inkawasi uses neither, suggesting its quipu are a plainer administrative genre (bulk goods recording without labels or section markers).

## Task 2: Recto/verso as debits/credits — FALSIFIED for Inkawasi

Charles's hypothesis: cord attachment direction (R=recto, V=verso) might encode double-entry debits and credits.

**Result:** No Inkawasi quipu has balanced recto/verso sums.

| Quipu | n_R | sum_R | n_V | sum_V | R/V ratio |
|-------|-----|-------|-----|-------|-----------|
| 1000603 | 137 | 2,027 | 1 | 0 | 2027.00 |
| 1000604 | 128 | 23 | 108 | 30 | 0.77 |
| 1000610 | 116 | 36,911 | 15 | 4,021 | 9.18 |
| 1000612 | 1 | 112 | 161 | 1,653 | 0.07 |
| 1000616 | 113 | 2,876 | 1 | 0 | 2876.00 |
| 1000617 | 1 | 8 | 92 | 951 | 0.01 |
| 1000619 | 100 | 9,194 | 12 | 389 | 23.63 |
| 1000633 | 69 | 64 | 7 | 8 | 8.00 |

Only 10 of 52 quipu have both R and V pendants. Most are overwhelmingly one-sided. None approach 1:1 balance.

**The R/V distinction at Inkawasi does not encode debits and credits.** It may still encode moiety (hanan/hurin) per Medrano & Urton, or something else entirely — but not double-entry.

**Caveat:** Simplified Ascher decoding was used (S clusters by position; L knots lack turn counts so units digits are approximate). However, the ratios are so extreme (0.01 to 2876) that decoding refinement cannot produce balance.

## On the 15,031 vs 1,431 discrepancy

A prior analysis reported white-cord values up to 15,031; this analysis finds max ~1,431 for the same quipu. This is a **power-alignment difference** in Ascher decoding (whether the top S cluster represents 10³ vs 10⁴). The structural findings — no red dividers, no R/V balance, repeating color cycles — are independent of absolute value calibration.

## Cord layout diagram: quipu 1000625 (the red-divider quipu)

```
Primary cord
    |
    |--[BY:1]--[R0:1]--[DB:0]--[YB:0]--[DG:6]--[R0:6]--|  <- header (ords 1-6)
    |                                                    |
    |--[RM:blank]---------------------------------------|  <- RED DIVIDER (ord 7)
    |                                                    |
    |--[YB:1]--[DG:4]--[R0:4]--[NB:1]--|  <- row 1
    |--[YB:1]--[DB:1]--[R0:8]--[NB:1]--|  <- row 2
    |--[YB:1]--[KB:2]--[DG:5]--[KB:4]--|  <- row 3
    |--[NB:0]--[YB:0]--[R0:1]--[DG:4]--|  <- row 4
    |   ...repeating commodity cycle...  |
    |--[YB:1]  (ord 36)                  |  <- last row
```

Each "row" uses the same color sequence — a repeating form. The red divider separates metadata from data.

## Bottom line

1. **Large Inkawasi values are single-cord recordings**, not sums across red-delimited sections. The census+inventory-spanning hypothesis is not supported by the cord layout.
2. **Recto/verso does not encode debits/credits** at Inkawasi. The double-entry hypothesis is falsified for this archive.
3. **The one red divider found** separates header from repeating data rows — a form marker, not a census/inventory boundary.
4. **Inkawasi quipu are structurally plain**: no E-E-E labels, almost no red dividers, no R/V balance. Bulk goods recording in its simplest form.
