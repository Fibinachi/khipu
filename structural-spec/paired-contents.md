# Paired Inkawasi Quipu: Contents and Form Classification

**Date:** 2026-10-10
**Analyst:** Muse (subagent)
**Question (Charles):** What do the paired/bundled Inkawasi quipu actually contain? Do they match the six form types seen elsewhere, or are they Inkawasi-specific?

---

## The Four Quipu

| Quipu | Pair | Cords | Depth | Colors | Attachment |
|-------|------|-------|-------|--------|------------|
| 1000605 (UR264) | tied to UR265 | 211 pendants + 2 subs | 2 (effectively flat) | 9 | all recto |
| 1000606 (UR265) | tied to 1000605 | 14 pendants + 11 subs | 3 | 2 | all recto |
| 1000628 (JC004) | attached to JC005 | 18 pendants + 14 subs | 3 | 10 | all verso |
| 1000629 (JC005) | attached to 1000628 | 149 pendants + 44 subs | 3 | 10 | recto |

---

## Classification Against the Six Form Types

### 1000605 (UR264) — Form B: Flat Register ✓ clean fit

- 211 pendants (Form B range: 4–319), 9 colors (B requires 4+), effectively depth 1
- The 2 subsidiaries are both **knotless** — blank cords, likely placeholders or markers, not data
- **Color is seried in a repeating 6-position cycle:** KB – MB – AB – AB – AB – BL, repeating ~35 times
- **Blue is not just a divider:** BL cords carry the highest knot counts of any color (avg 4.25 knots/cord vs 1.4–2.6 for others). The 6th position holds the largest entries.
- First ~9 cords are knotless — a blank header section before data begins
- Knot types: S (316), L (90), E (15) — full decimal range, real quantities

### 1000606 (UR265) — D/F boundary: small deep form

- 14 pendants, depth 3, 11 subsidiaries concentrated on just 3 pendants (one pendant has 7 subs)
- 2 colors (AB, MB), all recto
- Only L and E knots — no S knots — suggesting small values throughout
- Too deep for Form D (depth 2), too small for typical Form F (median 60 pendants)
- Reads as a detail sheet or elaboration: one entry exploded into 7 sub-entries

### 1000628 (JC004) — D/F boundary: small deep form

- 18 pendants, depth 3, 14 subsidiaries on 4 pendants, **10 colors**, **all verso**
- Same small-deep architecture as 1000606, but high color diversity and verso attachment
- L and E knots only — small values
- The all-verso attachment is its most distinctive feature (see below)

### 1000629 (JC005) — Form F: Deep Hierarchy (selective subsidiaries)

- 149 pendants, depth 3, 44 subsidiaries at 0.30/pendant (selective, D-like ratio, but F depth)
- 10 colors, recto, 2 BL cords (one NB-BL, one BL-NB)
- Color sequence is **mixed, not cyclic** — color codes categories but not in a repeating series
- First ~10 cords knotless (header section, same as 1000605)
- 49/149 pendants knotless (33%) — many blank or zero entries
- Knot types: S (173), L (80), E (41) — full decimal range

---

## Comparison Table

| Quipu | Form type | Key features | Matches elsewhere? |
|-------|-----------|--------------|-------------------|
| 1000605 | **B** (flat register) | 211 pendants, 6-color cycle, BL = highest values, knotless header | Yes — color cycles in flat registers at Ica (1000053: 4-cycle), Ocucaje (1000124) |
| 1000606 | **D/F** (small deep) | 14 pendants, depth 3, one entry with 7 subs, small values | Yes — 24/612 quipu (3.9%) are small-deep; found at Ica, Pisco, Arica |
| 1000628 | **D/F** (small deep) | 18 pendants, depth 3, 10 colors, all verso | Yes — same small-deep population; verso-only is unusual but not unique |
| 1000629 | **F** (deep hierarchy) | 149 pendants, depth 3, selective subs, mixed colors, knotless header | Yes — Form F is 23.5% of corpus |

**No E-E-E markers** on any of the four quipu.

---

## Key Findings

### 1. The pairs are architecturally different from each other

- Pair 1: Form B (211-pendant flat register) + small-deep form (14 pendants). Completely different documents.
- Pair 2: small-deep form (18 pendants, verso) + Form F (149 pendants, recto). Different scale, mirror attachment.
- This confirms the earlier finding: pairs are filed together, not calculated together. No evidence of cross-checking, summarizing, or duplicating.

### 2. Nothing here is Inkawasi-specific

Every architecture appears in the broader corpus:
- The 6-color cycle: Ica and Ocucaje flat registers use the same convention (4- and 5-position cycles)
- Small-deep forms: 24 quipu across Ica, Pisco, Arica, and unknown provenience
- Form F deep hierarchy: 23.5% of all quipu

What IS distinctive is the **pairing** — physically tying architecturally different documents together. That is an archival practice (filing), not a form type.

### 3. Blue carries the largest values on 1000605

The earlier "blue as divider" finding needs revision for this quipu. BL cords don't just mark every 6th position — they hold ~2–4× the knots of other colors. Blue marks the 6th category AND that category runs larger quantities. (What the 6 categories are remains unknown.)

### 4. Knotless opening cords = headers

Both large quipu (1000605, 1000629) open with ~9–10 knotless cords before data begins. These are likely label/header cords — the quipu equivalent of a title row. The ~30% knotless rate overall (63/211, 49/149) suggests blank/zero entries were left in place rather than removed.

### 5. The recto/verso mirror (1000628 vs 1000629)

1000628 hangs entirely verso; its pair 1000629 hangs entirely recto. Values don't balance, so this is not debit/credit. It is a document-level classifier — the strongest candidate being **two sides of one account** (e.g., two storehouses, two time periods, two tribute sources) filed as a pair. The small quipu (1000628) may be the index or summary key to the large one (1000629), or they may record complementary halves.

### 6. 1000606 may be the "footnote" to 1000605

1000606 (14 pendants, depth 3, tied to 1000605) has the architecture of an elaboration — a few entries exploded into detail. It is not a summary (values don't match) or a duplicate. The most plausible reading: it records metadata, corrections, or breakdowns for specific entries in 1000605 that needed more than the flat register could hold.

---

## Limitations

1. **No exact decimal decoding.** NUM_TURNS, KNOT_ORDINAL, CLUSTER_ORDINAL are empty for Inkawasi quipu in OKR. All value comparisons use knot counts by type (S/L/E), not decoded numbers. Relative comparisons (BL cords have more knots) are robust; absolute values are not available.
2. **1000606 = UR265 is inferred** from shared museum number + "Attached to UR264" note, not explicitly confirmed in the database.
3. **Color sequence analysis** was done for 1000605 and 1000629 (the large quipu). The small quipu (1000606, 1000628) were not examined cord-by-cord for color order.
4. **Form classification** uses the summary criteria from quipu-form-types.md, not the original cluster assignments. D/F-boundary cases (1000606, 1000628) reflect genuine architectural ambiguity, not measurement error.
5. **Knotless = zero vs. blank** cannot be distinguished from the data. Headers, zero-values, and placeholders look identical.

---

## Files

- Analysis database: `~/workspace/quipu-analysis/okr-khipu.db`
- Form types: `~/workspace/quipu-analysis/quipu-form-types.md`
- Pair analysis: `~/workspace/quipu-analysis/paired-quipu.md`
- This report: `~/workspace/quipu-analysis/paired-contents.md`
