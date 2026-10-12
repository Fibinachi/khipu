# Peanut Quipu vs. Santa Positional Structure

**Date:** 2026-10-10
**Question:** Do the five Inkawasi peanut quipu (UR266, UR268, UR269, UR270, UR272 / OKR 1000607, 1000610, 1000611, 1000612, 1000614) share the Santa census positional structure (position 1 = header, positions 2–5 = detail with subsidiaries, position 6 = terminal, repeating 6-cord groups)?

**Answer: No.** The Santa N-cord fixed-field schema does not transfer to commodity quipu. The general record logic does (header → body, subsidiaries = detail), but the fixed-group structure is census-specific.

---

## 1. No fixed N-cord groups

Tested periodicity N = 2–12 for subsidiary placement and color repetition on all five quipu. No N shows a clean repeating group:

- Subsidiary presence does not concentrate on specific residues for any N (spreads 0.13–0.45, no residue drops to clean zero except in small-sample noise).
- Color periodicity is low for UR266/268/269 (0.10–0.32) — colors alternate nearly every cord ("salt-and-pepper," 102–226 color runs, overwhelmingly run-length 1).
- UR270 shows high color periodicity (0.82–0.85) but across multiple candidate N (7, 9, 10, 11) — consistent with long color blocks, not fixed groups.

**There is no N for peanuts.** No repeating record unit was detected.

## 2. No header/detail/terminal positions

The Santa rule (subsidiaries on middle positions, never on first/last of a group) cannot apply — there are no groups. Subsidiary placement shows no positional regularity:

| Quipu | L1 pendants | With subsidiaries | Pattern |
|---|---|---|---|
| UR266 | 132 | 28 (21%) | Sparse, irregular |
| UR268 | 131 | 33 (25%) | Sparse, irregular |
| UR269 | 289 | 29 (10%) | Sparse, clustered in 3s |
| UR270 | 162 | 140 (86%) | Dense, nearly every cord |
| UR272 | 173 | 116 (67%) | Dense, most cords |

The five split into **two architectural families**, not one uniform structure:
- **Sparse-subsidiary** (UR266/268/269): 10–25% of cords have subsidiaries; salt-and-pepper colors; Form F/E sections.
- **Dense-subsidiary** (UR270/272): 67–86% of cords have subsidiaries; long color blocks; Form E/F sections.

Subsidiary-bearing cords carry slightly more knots than non-subsidiary cords (UR266: 6.2 vs 5.3; UR268: 10.8 vs 8.9; UR270: 4.9 vs 4.1), consistent with subsidiaries = breakdown of a larger entry. In UR272 the inversion is extreme: parent cords average 1.0 knots, subsidiaries carry the substantive data.

## 3. Document-level headers exist (the transferable principle)

While per-group headers don't exist, **document-level headers do**:

- **UR266:** cords 1–2 are completely knotless; knots begin at cord 3.
- **UR269:** cords 1–9 are completely knotless; knots begin at cord 10.
- **UR272:** cords 1–5 are MB:W, each carrying exactly one L-knot and **no subsidiaries**; from cord 6, subsidiaries and S-knots begin. A textbook 5-cord simplified header.

This matches the "knotless opening cords = title row" finding from the paired-Inkawasi analysis. The header → body principle transfers; the fixed-field group does not.

## 4. Zero census content

Section-level classification of all five quipu: 2–4 sections each, all Form E/F/D, **zero 6-block content** (maximum 0.25 on one small section of UR269). The peanut quipu are ledgers/inventories, not census-type documents. This is consistent with the finding that census is a content type, not a form type — and peanuts aren't it.

## 5. Why the schema doesn't transfer

The Santa 6-cord group exists because a **person has a fixed number of fields** (name, moiety, ayllu, tax owed, tax paid, …). Every tributary gets the same six slots.

A peanut inventory has no fixed-field record. It is a **list**, not a register: entries vary (different lots, sources, quantities), and subsidiaries provide ad-hoc breakdown where needed rather than filling fixed slots. The commodity quipu are ledgers; the census quipu are fixed-field registers. Different document logic for different administrative purposes.

## 6. What does transfer (the general record logic)

1. **Header → body:** simplified or knotless opening cords, then substantive entries.
2. **Subsidiaries = detail:** breakdown of the parent entry (not arithmetic subtotals — consistent with the Santa finding that subsidiaries don't sum to parents).
3. **Color = identifier:** name for people (Santa); likely source/batch/variety for goods (peanuts). The *role* of color transfers; the *mapping* is content-specific.

## Caveats

- NUM_TURNS, KNOT_ORDINAL, and CLUSTER_ORDINAL are empty for Inkawasi quipu in the OKR — no exact decimal decoding was possible. All value comparisons use knot-type counts, not decoded values.
- The 5-cord header on UR272 is structural (no subsidiaries, L-knots only) but its semantic content is unknown.
- UR270/272 vs UR266/268/269 may represent summary vs. detail of the same peanut stock (all found in the same room), but this was not tested.

## Bottom line

Charles's hypothesis — that the Santa positional logic could decode commodity quipu — is **falsified in its specific form** (no N-cord groups, no positional header/detail/terminal) but **confirmed in its general form** (headers, subsidiaries-as-detail, color-as-identifier). The fixed-field record is census-specific. Commodity quipu use a looser ledger logic: identify the lot (color), state the quantity (knots), break down where needed (subsidiaries).
