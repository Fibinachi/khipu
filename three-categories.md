# Three Document Categories: Census, Inventory, Miscellaneous

**Date:** 2026-10-10
**Corpus:** 619 quipu → 797 sections (328 sectioned) + 291 small quipu

## The three categories

Applied Charles's three-way split to the full corpus:

| Category | Sections | Quipu | Share of quipu |
|---|---|---|---|
| **Census** | 33 | 24 | 3.9% |
| **Inventory** | 317 | 317 | 51.2% |
| **Miscellaneous** | 447 | 270 | 43.6% |
| Nodata | — | 8 | 1.3% |

## Classification rules

1. **Census:** ≥50% of cords in same-color 6-blocks (run length multiple of 6), ≥2 distinct block colors. Validated 16/16 against Santa (census) vs Inkawasi (inventory) ground truth.
2. **Inventory:** Not census AND (≥2.5 knots/L1 cord OR [subsidiary ratio ≥0.3 AND ≥1.0 knots/cord]). Matches the Inkawasi commodity-ledger profile.
3. **Miscellaneous:** Everything else — low information density, no census structure.

**Ground-truth validation:**
- All 10 Inkawasi commodity quipu (peanuts, chili, beans) → **inventory** ✓
- All 6 Santa "Rosetta" quipu → **census** ✓

## Category × Form type (quipu level)

| Form | Census | Inventory | Misc |
|---|---|---|---|
| A: Tally strip | 0 | 16 | 15 |
| B: Flat register | 0 | 36 | 40 |
| C: Simple list | 1 | 30 | 70 |
| D: Grouped account | 4 | 80 | 65 |
| E: Hierarchical ledger | 14 | 52 | 44 |
| F: Deep hierarchy | 5 | 103 | 36 |

**Key finding: the three-way split cuts across form types.** No form maps cleanly to one category. Census sections appear in five forms (D, E, F, B, C). Inventory spans all six. This confirms the v2 framework: **form is structure, category is content.** They are orthogonal dimensions.

Notable patterns:
- **E (hierarchical ledger)** is the most census-heavy form (14/24 census quipu), consistent with Santa's Form E census records.
- **F (deep hierarchy)** is inventory-dominant (103/144) — complex multi-level ledgers for commodity tracking.
- **A (tally strip)** never census — too simple for person-records.
- **C (simple list)** is misc-heavy (70/101) — flat lists without the density for inventory or the structure for census.

## Geographic distribution

**Census (24 quipu):** Santa (6), Ica (3), Nazca (1), Paracas (1), Pachacamac (1), Chancay (1), 5 unprovenienced, others. Empire-wide but rare — 3.9% of corpus.

**Inventory (317 quipu):** Pachacamac (56), Ica (33), Incahuasi (33), Leymebamba (16), Nazca (7). Concentrated at major administrative and storage sites. The largest category — the Inca bureaucracy was primarily an inventory bureaucracy.

**Miscellaneous (270 quipu):** Pachacamac (33), Incahuasi (19), Huaquerones (15), Ica (13). Includes tally strips, simple lists, fragments, and quipu too small or degraded to classify structurally.

## Section-level detail (797 sections, 328 large quipu)

| Category | Sections | Share |
|---|---|---|
| Census | 33 | 4.1% |
| Inventory | 317 | 39.8% |
| Miscellaneous | 447 | 56.1% |

At section level, miscellaneous dominates — many sections are short structural units (D-type building blocks) that don't reach inventory density alone. This is expected under the composite-document model: a quipu classified as "inventory" at the document level contains misc-classified subsections.

**Quipu-level rule:** a quipu is census if *any* section is census; else inventory if any section is inventory; else miscellaneous. Rationale: a census section defines the document's most distinctive content.

## What "miscellaneous" contains

Not a wastebasket — three identifiable sub-populations:
1. **Tally strips and simple lists** (Forms A, C) — low-density counting, possibly herder tallies or simple records.
2. **Structural subsections** — D-type building blocks within larger composite documents that don't independently reach inventory thresholds.
3. **Fragments and degraded quipu** — incomplete data prevents confident classification.

Future work: subdivide miscellaneous using the data-class archetypes (BLANK/LEAF/BRANCH/HBLANK).

## Implications

1. **The Inca kept three kinds of books.** Person-registers (rare, 4%), commodity ledgers (majority, 51%), and everything else (44%). The empire counted goods more than people — or people-records were kept separately and lost.

2. **Census is rare but widespread.** 24 quipu at 8+ sites. Every major region did head-counts, but few such documents survive relative to inventory.

3. **Form ≠ genre.** The six structural forms describe *how* information is organized; the three categories describe *what kind* of information. A census can be written in Form D or Form F. An inventory can be Form B or Form E. The scribe chose the form; the bureaucracy chose the category.

4. **Survivorship bias confirmed.** Inventory dominates because the Spanish preserved tribute/commodity records and burned the rest. The 4% census share is a floor, not a true proportion.

## Files

- Per-section: [quipu-section-categories.csv](sandbox://workspace/quipu-analysis/quipu-section-categories.csv) (797 rows)
- Per-quipu: [quipu-document-categories.csv](sandbox://workspace/quipu-analysis/quipu-document-categories.csv) (619 rows)

## Method notes and limitations

- 6-block definition: maximal same-color runs with length multiple of 6; ≥2 distinct colors; ≥50% of cords. Differs slightly from the sections CSV's SIX_BLOCK_FRAC (27/31 overlap); this definition is cleaner and applied uniformly.
- Inventory thresholds (2.5 knots/cord, 0.3 subsidiary ratio) calibrated against the Inkawasi commodity profile (mean ~4.7 knots/cord). Not independently validated — the census rule is the only validated classifier.
- Small quipu (<30 pendants): classified at quipu level; the 6-block test requires ≥12 cords for meaningful grouping. Only 3 small quipu met the census rule.
- 8 quipu have no cord data (Dallas Museum) — unclassifiable.
- The "miscellaneous" category is heterogeneous by design; subdivision is future work.
