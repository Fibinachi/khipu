# The Raw Field-Sheet Corpus — Findings

**Analysis:** `notebooks/10_field_sheet_corpus.ipynb` (executed, zero errors)
**Parser:** `src/kdb_field_sheets.py`
**Data:** the 66 raw field-recording sheets recovered from the KDB site (notebook 07
parked them as "different layout, not yet parsed"): 43 UR255+ `.xlsx` + 23 JC series.
**Date:** July 2026

---

## Headline

**The recovered-KDB data layer is now complete.** All 345 recovered files are parsed
(274 Brezine sheets, notebook 07; 66 field sheets, here) or catalogued (5 misc).
Combined sheet coverage: **340 khipus**, now with per-cord OKR linkage — the
instrument the khipu↔khipu summation-hierarchy search (Phase B) will run on.
*(Correction 2026-07-21: an earlier version claimed UR281 "exists in no other known
source"; the OKR contains it as `AS068/UR281`/KH0081 — see below.)*

## Format decoded

Single uniform layout across all 66 files (one tab `Khipu_<NAME>`; the tab, not the
filename, is canonical — UR291.xlsx holds UR291A). Three non-obvious semantics,
each validated against the OKR:

1. **Rows are a depth-first field traversal** (pendant, then its subsidiary subtree);
   `element pos-n` is a *sibling index* (CLUSTER_ORDINAL for pendants, within-parent
   index for subsidiaries). Cord level is not stored; we transfer it from the OKR by
   depth-first alignment (pendants by CLUSTER_ID/CLUSTER_ORDINAL, children by
   ATTACH_POS), which reproduces the sheet row order essentially exactly.
2. **Knot-cluster notation** `(2S/5/Z), 200` = 2 single knots at 5 cm, Z-tied, decimal
   contribution 200. The trailing number is the recorder's computed value per cluster.
3. **Two long-knot conventions coexist**: the JC series writes turns as the count
   (`(3L…), 3`); UR255+ writes one knot with the value carrying the turns
   (`(1L…), 5`). Both are internally consistent once recognized.

Unlike the Brezine sheets, these carry per-element `value`, `algo val`, `certain`,
length, thickness, color(s), and attach position — a richer record per cord.

## Validation

- **6,686 cord rows, 0 parse errors**; 17 unparseable cluster cells (kept raw).
- **Structure:** 66/66 khipus found in the OKR (alias-aware lookup) with total cord
  counts matching **66/66 exactly**; 66/66 aligned row-by-row (65 strict DFS, 1 LCS
  fallback for UR292A, where one cluster was recorded out of the OKR's sort order).
- **Internal arithmetic:** 99.83% of knot-bearing rows re-derive their recorded value
  from their own knot specs; 100% of knotless rows have value 0; 99.71% of row values
  equal the sum of their cluster values (14 discrepant rows, enumerated in the
  notebook — unparsed cells or recorder edits).
- **Per-cord fidelity vs the OKR:** 6,685 cords carry OKR ids via the alignment
  (all 66 khipus, incl. UR281 = KH0081); sheet value == OKR knot-derived value for
  **99.99%** (exactly 1 disagreement, magnitude 5, on JC005). For this later-vintage corpus the OKR and the sheets are
  the same lineage — unlike the 2004-05 Brezine era, where notebook 07 found a heavy
  tail of OKR value corruption (e.g. UR090).

## UR281 in context — a correction

**Correction (2026-07-21, Zenodo deposit verification):** the original claim that
UR281 "exists nowhere else" was wrong. The OKR contains it as **`AS068/UR281`**
(KH0081, 216 cords, entered 2017), and the 2012 database holds the Ascher-era
assessment (`AS068`). The failure was exact-string lookup against the OKR's compound
designation; the alignment module is now alias-aware and UR281 aligns like every
other khipu (66/66). The honest statement: the recovered sheet is the **primary field
document** behind OKR KH0081 — the corpus now carries three assessments of this one
object (Ascher-era, the field sheet, the OKR ingestion). 216 cords, all valued
(total 53,096), overwhelmingly recto (215/216), S-knotted, colors AB/W/MB.

## What this changes

1. **Phase B has its full instrument**: 340 sheet-fidelity khipus, per-cord values,
   and OKR linkage for colors/knots — plus Urton's archive groupings (notebook 07)
   as search units.
2. **A fidelity map with a boundary**: OKR values are trustworthy for the UR255+/JC
   vintage (99.99%) but not uniformly for the 2004-05 vintage — sum-based analyses
   now know exactly which lineage to trust per khipu.
3. **The preservation case for the OKR maintainers** rests on: the primary field
   documents themselves, the 14 dropped alternate assessments in the 2012 DB (2,323
   cords), AB001, and Urton's classification tables — not on unique khipus
   (corrected 2026-07-21, verification rounds 1–2).

## Limitations

- Cord levels are *transferred from the OKR*, not recorded in the sheets.
- The `algo val` / `accept algo val` columns (the recorders' own algorithm-vs-hand
  reconciliation) are parsed but not yet analyzed — a possible window into how the
  original team resolved ambiguous readings.
- 14 value discrepancies and 17 unparsed cluster cells remain, enumerated but not
  adjudicated.
