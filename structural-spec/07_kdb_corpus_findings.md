# The Recovered KDB Sheet Corpus — Findings

**Analysis:** `notebooks/07_kdb_sheet_corpus.ipynb` (executed, zero errors)
**Data recovered:** 345/345 unique files from Wayback Machine snapshots of the defunct
`khipukamayuq.fas.harvard.edu/DataTables/` (enumerated via the CDX API; the CDX lists 346 capture URLs, one a host:port alias
of another). Per-file provenance: `data/raw_data/kdb_sheets/MANIFEST.csv`.
**Date:** July 2026 (revised after adversarial audit, 2026-07-18 — see
`knowledge_base/08_audit_response.md`)

---

## What was recovered

| Asset | Contents |
|---|---|
| 274 Brezine-format sheets (242 UR + 32 HP) | Hand-curated per-cord data incl. computed decimal **Value** column, 2004–05 |
| 66 raw field sheets (43 UR255+ `.xlsx`, 23 JC) | Different layout (knot-cluster notation, no computed values); **not yet parsed** |
| `KhipuDB_SQL.zip` → `data/raw_data/khipudb_2012.db` | Full Harvard KhipuDB (2012-01-22): 548 khipus, 37 tables, converted MySQL→SQLite |
| `Abbreviations.xls` | Codebook (attachment, termination, fiber, knot, cord-type codes) |
| UR Masterlist (2009), Khipu Inventory (2018) | Catalog documents |

## Extraction (task: `src/kdb_sheets.py`)

All 274 pendant-format sheets share one exact layout (survey-verified: header row 5,
12 columns). Full label grammar decoded via the codebook: main pendants, section-prefixed
mains (composite khipus, e.g. UR022 sections A–F), subsidiary chains (`4s1s1`), top cords
(`T`), top loop pendants (`TPA`), loop pendants (`PA`), markers (`M`), primary-cord knots
(`K`), unattached (`X`). **26,108 cord rows, 0 parse errors, 0 unclassified labels.**

Outputs: `data/processed_data/07_kdb_sheet_cords.csv` (per-cord),
`07_kdb_sheet_khipus.csv` (per-khipu summary).

## Validation against the OKR

- **274/274 sheets matched to an OKR khipu** (alias-aware: the OKR merges duplicate
  recordings under compound designations like `AS070/UR035`; exact-string matching —
  used in an earlier version of this document — missed 10 of them).
- Level-1 cord counts: **241/274 exact, 260/274 within ±2.** Residuals have two
  identified causes, neither a parse defect: the OKR is inconsistent about counting top
  cords/markers as level-1, and some recordings were updated after the 2005 export
  (e.g. UR001 gained 17 cords).

## Value fidelity — the headline number

Per-khipu hand-curated sheet value sums vs OKR knot-derived sums (n = 263):

- **Median disagreement: 0%. 91% of khipus agree within 5%.**
- But a heavy tail: ~2% of khipus are more than 2× off. UR090 is the worst case that
  matters: OKR-derived 14,953 vs sheet 2,271 — the exact artifact that sank Phase A's
  blind test and inflated the Santa archive sum to ~1029.

So: the OKR is fine for most khipus, but for value-critical work (document matching,
sum tests) the sheets are the instrument, and we now have a per-khipu reliability map
(`07_value_fidelity.png`) identifying exactly which OKR khipus can't be trusted.

## What the 2012 database preserves that the OKR does not

**Correction (2026-07-21, Zenodo deposit verification):** an earlier version claimed
"27 khipus absent from the modern OKR" via exact-string comparison. Alias-aware
matching shows those are almost all present under the OKR's merged compound
designations. What is genuinely preserved:

- **14 dropped recordings (2,323 cords)** — independent assessments (mostly
  Ascher-era) of khipus the OKR merged under compound designations, where the OKR
  kept the *other* recording; these exist today only in the 2012 DB. Thompson (2025,
  *Ñawpa Pacha* 45(1)) shows on KH0083 — whose dropped AS070 assessment (590 cords)
  is among these — why alternate assessments of one khipu are scientifically
  valuable. (A further 12 merged-name recordings, 1,991 cords, survive in the OKR
  under the same KHIPU_ID and are *not* unique material.)
- **1 khipu for which the OKR holds no data**: AB001 (156 cords in the 2012 DB; the
  current OKR catalog lists it as KH0701, number issued 2025-12-19, but the database
  contains no cord records for it). (QU13–QU19 exist in the OKR as KH0601–KH0607 but
  are empty placeholder records in both databases.)
- All 274 Brezine sheets now match an OKR khipu (274/274).

## Urton's expert labels validate the notebook 04 feature definitions (blind)

`URTON_KHIPU_TYPE` (2012 DB, dropped from OKR): Urton's typing table covering
356 khipus (144 with at least one positive label) — BANDED, SERIATED, ANOMALOUS, DECIMAL_NUM, CENSUS, POSITIONAL, etc.
These labels predate our features by ~20 years; the notebook 04 features were built
without any knowledge of them. Cross-validation (274 overlapping khipus, permutation
p-values, 10k shuffles):

| Our feature (notebook 04) | Urton label | AUC | p |
|---|---|---|---|
| `banding_index` | BANDED | **0.901** | 0.0001 |
| `banding_index` | SERIATED (expect inverse) | 0.330 | (significantly inverse, as predicted) |
| `locke_violation_rate` | ANOMALOUS | **0.900** | 0.0002 (n_pos = 6) |
| `locke_violation_rate` | DECIMAL_NUM (expect inverse) | 0.563 | 0.17 — no signal |

The banded/seriated axis and the Locke-anomaly flag we derived from raw structure
recover Urton's expert judgments almost perfectly. (Caveat: ANOMALOUS has only 6
positives; DECIMAL_NUM shows no relationship — his "decimal" label is not the inverse
of our violation rate.)

## Ground-truth archives for Phase B

`ARCHIVE_NUM` gives Urton's own archive groupings: 6 real archives with ≥2 khipus —
Ica (37), Pachacamac (30), Huaquerones/Puruchuco (22), Leymebamba (21), Circum-Ica (16),
Nazca (8). (Names here are majority-provenance strings; the DB's own `ARCHIVE_DC`
labels archives 301/201 as "Puruchuco" and "Circum-Ica".) (Archive 0, n = 222, is the unassigned bucket.) These are the natural units
for archive-level document matching — no more guessing what counts as an archive.

## What this changes

1. **Phase B gets its instrument:** sheet-fidelity values + expert archive groupings +
   a reliability map for the OKR. Sum-style tests can now be run at the fidelity that
   made notebook 06 work, for ~274 khipus instead of 6.
2. **Notebook 04's feature definitions are externally validated** by expert labels they
   never saw (convergent validity; the taxonomy's *claims* — continuum, 7.7% tail — are
   validated separately, see notebook 08).
3. **The recovered 2012 DB is a preservation contribution in its own right** (14
   dropped alternate recordings + AB001 + Urton's label tables, none of which the
   modern OKR holds) — offered to the OKR maintainers.

## Limitations

- The 66 raw field sheets (UR255–294, JC) are unparsed; they lack computed values and
  need their own parser + validation strategy.
- Sheet vintage is 2004–05: khipus recorded after that exist only in the OKR; where
  sheets and OKR disagree on *content* (not typing), the later recording may be the
  corrected one — disagreement direction is documented per khipu, not adjudicated.
- 2006 vs 2010 Wayback snapshot version drift not audited (we take the latest capture).
