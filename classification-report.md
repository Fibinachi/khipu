# Quipu Form-Type Classification: Definitive Assignment

**Date:** 2026-10-10
**Corpus:** Open Khipu Repository (`okr-khipu.db`), 619 quipu

---

## Summary

Every quipu in the corpus has been assigned to exactly one of the six structural form types. 612 of 619 (98.9%) are classified; 7 have no cord data and cannot be classified.

| Type | Description | Count | % of classified |
|------|-------------|------:|----------------:|
| A | Tally strip | 32 | 5.2% |
| B | Flat register | 76 | 12.4% |
| C | Simple list | 101 | 16.5% |
| D | Grouped account | 149 | 24.3% |
| E | Hierarchical ledger | 110 | 18.0% |
| F | Deep hierarchy | 144 | 23.5% |
| UNCLASSIFIED | No cord data | 7 | — |

The distribution **exactly matches** the original cluster estimates from `quipu-form-types.md`. This is expected: the cluster labels are retained as the authoritative assignment, and this report adds an auditable decision tree, confidence ratings, and edge-case documentation.

---

## Method

### Primary assignment: original clustering

The six types were derived by architectural clustering of 612 quipu (`/tmp/form_class.json`, produced 2026-10-10). Those labels are retained as the published classification.

### Audit: deterministic decision tree

To make the classification auditable and reproducible, a decision tree was reverse-engineered from the cluster centroids:

```
1. max_depth >= 3                    → F (Deep hierarchy)
2. max_depth == 2:
     pendants <= 40                  → D (Grouped account)
     pendants > 40                   → E (Hierarchical ledger)
3. max_depth == 1 (flat):
     pendants <= 10 AND colors <= 2  → A (Tally strip)
     colors >= 4                     → B (Flat register)
     otherwise                       → C (Simple list)
```

The tree reproduces the cluster labels at **95.6% agreement** (585/612). The tree is published here so that any future quipu — from new excavations or museum cataloguing — can be classified without re-running the clustering.

### Confidence ratings

- **High** (585 quipu): cluster label and decision tree agree.
- **Medium** (27 quipu): cluster says C, tree says B. These are flat quipu with 4+ colors that the clustering placed in C based on features the tree does not use (knot patterns, attachment mix). The cluster label is retained; the ambiguity is noted per-quipu in the CSV.
- **Low** (1 quipu): 1000367 has an anomalous structure (see Edge Cases).
- **N/A** (7 quipu): no cord data; unclassifiable.

---

## Edge Cases

### 1. The B/C boundary (27 quipu, Medium confidence)

All mismatches are cluster=C / tree=B: flat quipu with 4+ colors. The report's stated criterion for B was "4+ colors (this is the defining feature)" and for C "1-3 colors," but the actual cluster data shows C colors ranging 0–22 (median 3). The boundary is genuinely fuzzy — a flat quipu with 5 colors could be a color-organized register (B) or a simple list that happens to use varied cord (C). The clustering used knot-pattern and attachment features that the tree ignores. **Resolution:** retain cluster labels, flag as Medium confidence. A future refinement could use color *banding* (positional runs) rather than color *count* as the B criterion.

### 2. The D/E boundary (15 quipu near the threshold)

The D/E split falls cleanly at 40/41 pendants in the cluster data — no tree mismatches. However, 15 quipu sit within 35–44 pendants. The pendant-count boundary is a clustering artifact, not a natural break; a quipu with 40 pendants and one with 41 are functionally identical. **Resolution:** retain labels, but treat the D/E boundary as a continuum in any analysis that is sensitive to it. The more meaningful D/E distinction may be subsidiary *selectivity* (D: some pendants have subsidiaries; E: most do), which the pendant count proxies imperfectly.

### 3. Narrow-but-deep F quipu (9 quipu)

Nine quipu are classified F (depth 3+) but have only 1–8 pendants (e.g., 1000062: 1 pendant, depth 3). These are deep chains rather than broad hierarchies — a single line of nested detail rather than a branching tree. They satisfy the F depth criterion, but they are structurally unlike the typical F (median 60 pendants). **Resolution:** retain F labels. A future refinement might distinguish "deep-chain" from "deep-tree" as F-subtypes.

### 4. Quipu 1000367 (Low confidence)

0 pendants, 60 top cords, depth 1, classified A. This is structurally bizarre — either a data-entry artifact (cords recorded at the wrong attachment level) or a genuinely inverted quipu. **Resolution:** flagged Low confidence in the CSV. Recommend verifying against the source record before using this quipu in any analysis.

### 5. Unclassifiable quipu (7)

1000464–1000470, all Dallas Museum of Art, have no cord records in the OKR or the legacy Harvard KDB. They cannot be assessed structurally. If cord data becomes available, apply the decision tree above.

---

## What the classification enables

1. **Stratified analysis.** Any structural, color, or numerical analysis can now be run within form type, controlling for document architecture.
2. **New-quipu classification.** The decision tree classifies future quipu without re-clustering.
3. **Form–content separation.** Cross-tabulating form type against Urton's genre types (CENSUS, SERIATED, etc.) tests whether the Inca separated document architecture from content genre.
4. **Ecological analysis.** Form-type distributions can be compared across highland/coastal/imperial contexts.

---

## Files

- Full classification: `~/workspace/quipu-analysis/quipu-classification.csv`
  (columns: KHIPU_ID, FORM_TYPE, CONFIDENCE, NOTES)
- This report: `~/workspace/quipu-analysis/classification-report.md`
- Original cluster labels: `/tmp/form_class.json` (612 quipu)
- Structural features: `/tmp/skel2.pkl`
- Database: `~/workspace/quipu-analysis/okr-khipu.db` (619 quipu)

---

## Limitations

1. The decision tree uses only three features (depth, pendant count, color count). The original clustering used additional features (knot patterns, attachment mix, E-E-E markers, top cords); 4.4% of labels depend on those.
2. Color counts use Ascher color codes as recorded; faded or ambiguous cords may be misclassified.
3. The 7 unclassified quipu are excluded from all percentage calculations.
4. Knot-value decoding was not used in classification (architecture only, by design).
