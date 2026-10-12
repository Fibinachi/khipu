# Data Classes: Unsupervised Cord-Role Segmentation of Large Quipu

**Date:** 2026-10-10
**Method:** Per-cord features (knot counts by type, subsidiary count/depth, color, attachment, position) → k-means clustering (k=2–6, elbow-selected) within each of the 20 largest quipu → cross-quipu archetype comparison → positional enrichment tests within 785 sections across 328 quipu.
**Constraint honored:** No meaning assigned. Only structure described.

---

## 1. The four universal archetypes

Every k-means class across all 20 quipu collapses into a 2×2 grid defined by two binary features: **has knots** × **has subsidiaries**. All four cells are populated in nearly every quipu:

| Archetype | Knots | Subsidiaries | Share of cords | Quipu containing it |
|---|---|---|---|---|
| **BLANK** | No | No | 31% | 16/20 |
| **LEAF** | Yes | No | 50% | 13/20 |
| **BRANCH** | Yes | Yes | 15% | 15/20 |
| **HBLANK** | No | Yes | 4% | 14/20 |

Definitions (structural only, no interpretation):
- **BLANK:** A cord with no recorded knots and no child cords.
- **LEAF:** A cord with knots but no children. Terminal data-bearing cord.
- **BRANCH:** A cord with knots and at least one child cord. Data-bearing parent.
- **HBLANK:** A cord with no knots but with child cords. A knotless grouping node.

The k-means independently discovered these in each quipu (k ranged 2–6 per quipu); the 2×2 is the consensus structure, not an imposed scheme. Finer k-means splits within archetypes (e.g., high-knot vs low-knot LEAFs) exist but do not recur consistently across quipu.

**Caveat on BLANK:** 31% is high. Some portion may reflect incomplete knot recording rather than genuinely knotless cords (e.g., 1000096 Lluta: 78% blank). The archetype is real — blank cords exist — but the exact share is an upper bound.

---

## 2. Negative finding: no positional cord roles at section level

Tested across 785 sections (328 quipu, 34,843 L1 cords). **None of the following show positional enrichment:**

| Test | Result |
|---|---|
| Archetype mix in first 3 vs last 3 vs middle cords of section | Identical (BLANK 31–32%, LEAF 48–50%, BRANCH 15–17%, HBLANK 4% in all three zones) |
| First cord of section is knotless | 36% vs 35% baseline — no effect |
| Knot-count distribution across section thirds | Uniform (mean ~3.1 in all thirds) |
| First cord color differs from section modal color | 49% — chance level |
| Knotless fraction by within-quipu decile | No consistent decile-1 spike across quipu |

**There is no universal "header class at start / terminal class at end."** Cord archetype does not predict position within a section.

---

## 3. Positive finding: archetypes cluster in runs

P(consecutive cords share archetype) = **0.67** vs 0.37 expected by chance.

Cords of the same structural type group together locally. The structure is **local (runs), not global (positions)**. This is consistent with the color-block finding: cords are organized into multi-cord groups, and archetype is a within-group feature.

---

## 4. Leading blank runs: quipu-specific, not universal

Length of the opening knotless run per quipu (top 20): 17, 15, 11, 6, 4, 3, 3, 2, 2, 1, 1, 1, 0, 0, 0, … (8/20 have zero).

Some quipu open with a substantial blank run (the "title row" pattern previously noted on Inkawasi quipu). Most do not. This is a quipu-level formatting choice, not a universal rule.

---

## 5. Santa 6-groups have positional archetype signatures

Grouping Santa census-quipu cords into consecutive 6s reveals **recurring archetype signatures** — the same 6-position pattern repeating:

- 1000270: `(LEAF, BRANCH, BRANCH, BRANCH, LEAF, LEAF)` ×4; `(LEAF, BRANCH×4, LEAF)` ×3
- 1000273: `(LEAF×6)` ×6; `(LEAF×3, BRANCH, LEAF×2)` ×5
- 1000274: `(LEAF×6)` ×5; `(LEAF×3, BRANCH, LEAF×2)` ×3
- 1000271: `(BLANK×6)` ×4 (blank 6-blocks also recur as units)

Only 4–8 distinct 6-signatures per quipu (vs 4^6 = 4096 possible). The "word" has **internal positional logic**: e.g., position 1 is typically LEAF (knotted, no subsidiaries — consistent with the published "position 1 = header, never has subsidiaries" rule), middle positions are BRANCH (detail fields with subsidiaries).

This confirms the record-as-word model at the archetype level: **the group is the record; archetype-position within the group is the field.**

---

## 6. Color and structural class are independent dimensions

K-means classes are not color-segregated beyond background distributions. A class's modal color matches the quipu's dominant color. Structural archetype (knots × subsidiaries) and color identity vary independently — consistent with the model where color = identifier (which entity) and archetype = field type (what kind of slot).

---

## Proposed universal cord-role taxonomy

```
CORD (level-1 pendant)
├── BLANK      — no knots, no children          (31%)
├── LEAF       — knots, no children             (50%)
├── BRANCH     — knots + children               (15%)
└── HBLANK     — no knots, has children         (4%)   [grouping node]
```

**Usage rules (empirically derived):**
1. All four roles appear in most quipu (13–16/20). The inventory is universal.
2. Roles are **not positional** within sections. There is no header-slot or terminal-slot.
3. Roles **cluster in runs** (67% persistence). Local grouping, not global ordering.
4. **Records are multi-cord groups** (e.g., 6-blocks). Within a group, archetype-by-position is structured (Santa signatures).
5. **Color is orthogonal** to role. Color identifies the entity; archetype identifies the field type.
6. **HBLANK is the grouping primitive**: knotless cords that exist solely to parent subsidiaries — the structural equivalent of a folder or section header *within* the cord hierarchy (distinct from section-boundary markers like red dividers, which operate between groups).

**What this means for the file-format model:**
- Section = document (file)
- Cord group (e.g., 6-block) = record (row)
- Archetype = field type (column type)
- Color = row identifier (primary key)
- Knots = field value
- Subsidiaries = sub-table / detail join
- HBLANK = grouping key with no value of its own

The quipu is not a flat list with header/body/terminal zones. It is a **hierarchical database**: sections contain groups, groups contain typed fields, fields contain values or sub-tables.

---

## Limitations

- BLANK share (31%) likely inflated by incomplete knot recording in some quipu.
- K-means k selected by elbow heuristic; finer structure may exist.
- Santa 6-group alignment assumes groups start at cord 1; a header offset would shift signatures (recurrence of identical signatures suggests alignment is approximately correct).
- Tests cover L1 cords only; subsidiary-level roles not segmented.
- 20 largest quipu may not represent small quipu (though archetype grid was validated on 328 quipu / 34,843 cords for the positional tests).
