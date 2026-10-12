# Section-Level Classification of Large Quipu

**Date:** 2026-10-10
**Corpus:** 328 quipu with ≥30 level-1 pendants (Open Khipu Repository)
**Output:** `~/workspace/quipu-analysis/quipu-sections.csv` (797 sections)

---

## Summary

Quipu are composite documents. **60% of large quipu (196/328) contain multiple sections**, with section boundaries marked by red dividers, recto/verso flips, color shifts, and structural breaks. Whole-quipu form classification masks this internal structure: only 53% of sections match their quipu's whole-document type.

The most common section-level form is **D (grouped account)** at 30% — the basic building block of Inca bureaucratic documents. Complex whole-quipu types (E, F) decompose into simpler constituent sections.

---

## Method

### Boundary detection (level-1 pendants, in cord-ordinal order)

Four independent signals, merged with an 8-cord proximity window:

| Signal | Definition | Sections started |
|--------|-----------|-----------------:|
| STRUCT_BREAK | Subsidiary presence flips or knot density changes 3×+ (15-cord windows) | 231 |
| COLOR_SHIFT | Jaccard similarity of color sets < 0.30 (20-cord windows) | 180 |
| RED_DIVIDER | Strong-red singleton (SR/RM/R) between different colors | 65 |
| RV_FLIP | Recto/verso dominance flips at 70% threshold (15-cord windows) | 49 |

Multiple signals at the same location are recorded as combined boundary types (e.g., COLOR_SHIFT+STRUCT_BREAK: 30 cases).

### Section classification

Each section classified with the decision tree from `classification-report.md`:
- max_depth ≥ 3 → F; max_depth = 2 → D (≤40 pendants) / E (>40); flat → A (≤10 pendants, ≤2 colors) / B (≥4 colors) / C (else)

### Validation

- Single-section quipu: 97% section/whole-type agreement (128/132) — the tree is consistent.
- Only 12/797 sections have <6 pendants; 5.8% have <10. Over-segmentation is minimal.

---

## Key Findings

### 1. Most large quipu are composite

- **132 single-section** (40%), **196 multi-section** (60%)
- Sections per quipu: 2 (98 quipu), 3 (47), 4 (26), 5–7 (15), 8+ (10)
- **46% of sections differ in form from their quipu's whole-document type**

### 2. Section forms differ from whole-quipu forms

| Form | Sections | Whole-quipu (section-weighted) |
|------|---------|-------------------------------|
| A (tally strip) | 0.6% | 0.0% |
| B (flat register) | 17.1% | 8.3% |
| C (simple list) | 10.8% | 8.7% |
| D (grouped account) | **29.9%** | 4.5% |
| E (hierarchical ledger) | 18.4% | 36.9% |
| F (deep hierarchy) | 23.2% | 41.7% |

Whole-quipu classification is dominated by the most complex section. Breaking into sections reveals **D (grouped account) as the fundamental unit** — the standard Inca bureaucratic form from which larger documents are assembled.

### 3. Common section combinations

Most frequent multi-section patterns:
- D+F (14), F+F (12), B+B (11), D+D (10), D+E (9)
- Same-form repeats (F+F, B+B, D+D) suggest **filing related documents together**
- Mixed-form (D+F, D+E) suggest **composite reports combining detail + summary**

### 4. Census sections: typically embedded, not standalone

31 census-like sections (6-block ≥ 50%):
- **5 standalone** (single-section quipu), **26 embedded** (84%)
- Forms: D (12), E (8), F (6), C (3), B (2) — census is **not** a single form type
- Proveniences: Santa (12), Paracas (3), Ica (2), Nazca (1), Pachacamac (1), Leymebamba (1), Chancay (1), Costa Sur (2), + others
- Census content appears **across the empire**, in sections of varying architecture

The Santa "Rosetta" quipu (1000274) is itself composite: sec1 = D (100% 6-block), sec2 = E (71% 6-block), separated by COLOR_SHIFT. The published "132 tributaries" aggregates across sections.

### 5. Red dividers separate same-form sections

Red singleton dividers most commonly separate sections of the **same** form type (D→D, F→F, B→B). Red marks **sub-divisions within a document type** (chapters), not form changes. Notable: 1000446 and 1000564 each have 6–9 consecutive D→D red-divided sections of 8–10 pendants — suggesting standardized sub-units.

### 6. R/V flips are general section markers

48 R/V flip boundaries, mostly separating same-form sections (F→F, D→D, B→B). Only 3 have census-like 6-block fractions. Confirms: **R/V flip = "new section," not census-specific.**

### 7. Extreme composite: 1000096 (Lluta Valley)

40 sections cycling through all six forms (A through F), mostly 13–99 pendants each, 11 red-divider boundaries. This is a **cord-bound archive** — dozens of distinct documents tied to one primary cord. The southern imperial fringe used the most extreme composite format.

---

## Implications for the composite-document model

1. **Form classification must be section-level.** Whole-quipu types conflate distinct documents.
2. **D (grouped account) is the atomic unit.** Most complex documents are assemblies of D-type sections plus specialized components.
3. **Census is a content type, not a form type.** Census sections appear in D, E, F, B, C architectures. The 6-block is the census signature, independent of structural form.
4. **Red and R/V are filing conventions**, not content markers. They organize multi-section documents the way headings organize a report.
5. **The quipu is a file folder.** The primary cord binds multiple related documents — the Andean equivalent of stapling reports together.

---

## Limitations

1. Boundary detection uses fixed thresholds (70% R/V, 0.30 Jaccard, 3× knot density). Subtler boundaries may be missed; some detected boundaries may be scribal variation rather than intentional sections.
2. The 8-cord merge window may combine distinct nearby boundaries.
3. 46 sections (5.8%) have <10 pendants — some may be fragments rather than intentional sections.
4. Color data uses Ascher codes as recorded; faded cords may create false COLOR_SHIFT boundaries.
5. Structural breaks depend on knot counts, which are incomplete for some quipu (e.g., Inkawasi NUM_TURNS empty).

---

## Files

- Sections CSV: `~/workspace/quipu-analysis/quipu-sections.csv`
  (columns: KHIPU_ID, SECTION_NUM, START_CORD, END_CORD, N_PENDANTS, FORM_TYPE, BOUNDARY_TYPE, N_COLORS, SIX_BLOCK_FRAC, WHOLE_TYPE, NOTES)
- This report: `~/workspace/quipu-analysis/section-classification.md`
- Script: `/tmp/section_classify2.py`
