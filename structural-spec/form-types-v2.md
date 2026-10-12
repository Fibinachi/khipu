# Quipu Form Types v2: The Section-Level Framework

**Date:** 2026-10-10 (revised from v1 same date)
**Corpus:** Open Khipu Repository (`okr-khipu.db`), 619 quipu → 797 sections
**Status:** This is the paper-ready framework. Supersedes `quipu-form-types.md` (v1).

---

## What Changed from v1

The v1 framework classified each quipu as exactly one of six form types (A–F).
That was wrong — or rather, it was right about the types but wrong about the unit.

**Section-level analysis of 328 large quipu (≥30 pendants) reveals that 60%
(196/328) are composite documents** containing multiple sections of different
form types. Only 53% of sections match their quipu's whole-document type.

**The six form types describe sections, not quipu.** A quipu is a cord-bound
file folder containing one or more sections, each section conforming to one
form type.

This document revises the framework accordingly. The six types are retained
(they are real), but redefined as **section-level forms**. All distributions
are regenerated at section level.

---

## The Composite-Document Model

```
┌─────────────────────────────────────────────────┐
│  QUIPU (the physical object / file folder)      │
│  Primary cord binds N sections together         │
│                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│  │Section 1 │  │Section 2 │  │Section 3 │       │
│  │ Form D   │  │ Form F   │  │ Form D   │  ...  │
│  │ 21 cords │  │ 45 cords │  │ 18 cords │       │
│  └──────────┘  └──────────┘  └──────────┘       │
│       ↑ red divider    ↑ R/V flip                │
│       (section boundaries)                      │
└─────────────────────────────────────────────────┘
```

**Key principles:**

1. **The quipu is the file; the section is the document.** Just as a modern
   folder contains multiple reports, a quipu's primary cord binds multiple
   related records.

2. **Section boundaries are marked by scribal conventions:**
   - **Red singleton dividers** — strong-red cords between sections (65 boundaries)
   - **Recto/verso flips** — attachment side changes (49 boundaries)
   - **Color shifts** — abrupt palette changes, Jaccard < 0.30 (180 boundaries)
   - **Structural breaks** — subsidiary depth or knot density changes (231 boundaries)

3. **Red and R/V are filing conventions, not content markers.** They
   predominantly separate same-form sections (D→D, F→F). Red = "new chapter,"
   not "new document type."

4. **Same-form repeats suggest filing related documents together**
   (F+F, B+B, D+D). Mixed-form combinations (D+F, D+E) suggest composite
   reports combining detail sections with summary sections.

---

## The Six Section-Level Form Types

### A: Tally Strip

| Attribute | Value |
|-----------|-------|
| Sections | 5 (0.6% of sections) |
| Avg length | 4.2 pendants (median 3) |
| Sites | 5 |
| Structure | Flat, ≤10 pendants, ≤2 colors |

The simplest form. A handful of pendant cords recording basic counts.
Rare as a section — usually a brief addition to a larger document.

**Blank section:** A short run of undyed pendant cords. Each records one count.

---

### B: Flat Register

| Attribute | Value |
|-----------|-------|
| Sections | 136 (17.1% of sections) |
| Avg length | 40.1 pendants (median 32) |
| Sites | 25 |
| Top sites | Pachacamac, Ica, Leymebamba |
| Structure | Flat, 4+ colors (color = category) |

A flat list where **color is the organizing principle**. No hierarchy —
color bands create visual columns. Each color = a category; each pendant = a quantity.

**Blank section:** Pendants attached in color batches. The quipucamayoc
pre-sorts cord by color before attaching.

**v1 → v2 change:** B rises from 12.4% (whole-quipu) to 17.1% (section-level).
Many B sections were hidden inside quipu classified as E or F.

---

### C: Simple List

| Attribute | Value |
|-----------|-------|
| Sections | 86 (10.8% of sections) |
| Avg length | 43.7 pendants (median 28) |
| Sites | 19 |
| Structure | Flat, 1–3 colors, no hierarchy |

The plainest form. A flat enumeration without strong color coding or
subsidiary structure. Used for simple lists where order, not category, matters.

**Blank section:** N pendant cords attached in sequence. Color incidental.

**v1 → v2 change:** C drops from 16.5% to 10.8%. Some C-classified quipu
decompose into B or D sections upon closer inspection.

---

### D: Grouped Account — THE ATOMIC UNIT

| Attribute | Value |
|-----------|-------|
| Sections | 238 (29.9% of sections) |
| Avg length | 22.2 pendants (median 21) |
| Sites | 30 (most widespread) |
| Structure | Depth 2, selective subsidiaries (median 0.37/pendant) |

**D is the fundamental building block of Inca bureaucratic documents.**
At 29.9% of sections (vs. 24.3% of whole quipu in v1, and only 4.5%
section-weighted), D dominates the section level. Complex documents (E, F)
decompose into D-type sections plus specialized components.

Structure: pendants with **selective** subsidiaries. Most pendants stand alone;
a few have breakdown cords. Subsidiary values do NOT sum to parents —
they encode annotations, corrections, or cross-references, not subtotals.

**Blank section:** ~20 pendant cords. Spare cord stock for subsidiaries.
The quipucamayoc decides which entries need elaboration — this is where
professional judgment lives.

**v1 → v2 change:** This is the most significant revision. D was the most
common whole-quipu type (24.3%) but is even more dominant at section level
(29.9%). The v1 framework undercounted D because complex quipu containing
D sections were classified by their most elaborate component.

---

### E: Hierarchical Ledger

| Attribute | Value |
|-----------|-------|
| Sections | 147 (18.4% of sections) |
| Avg length | 73.1 pendants (median 63) |
| Sites | 23 |
| Structure | Depth 2, >40 pendants, systematic subsidiaries |

Many pendants with **systematic** (not selective) subsidiary structure.
The full administrative ledger: color-banded groups with breakdown cords
on most pendants.

**Blank section:** Long cord run. Pendants in color batches. Subsidiary
cord stock for systematic breakdown.

**v1 → v2 change:** E holds steady (18.0% → 18.4%). E sections tend to be
standalone — they are already "complete" documents that don't need assembly.

---

### F: Deep Hierarchy

| Attribute | Value |
|-----------|-------|
| Sections | 185 (23.2% of sections) |
| Avg length | 51.8 pendants (median 35) |
| Sites | 29 |
| Structure | Depth 3–6, multi-level nesting |

Three or more levels of cord nesting. Multi-level aggregation —
imperial summaries rolling up from local to regional to central.

**Blank section:** The quipucamayoc builds downward: pendants for top-level
categories, subsidiaries for sub-categories, sub-subsidiaries for detail.
Depth reflects administrative distance.

**v1 → v2 change:** F holds steady (23.5% → 23.2%). Like E, F sections are
often standalone complex documents.

---

## Section-Level vs. Whole-Quipu Distributions

| Form | v1 (whole-quipu) | v2 (section-level) | Change |
|------|-----------------|-------------------|--------|
| A: Tally strip | 5.2% (n=32) | 0.6% (n=5) | −4.6pp |
| B: Flat register | 12.4% (n=76) | 17.1% (n=136) | +4.7pp |
| C: Simple list | 16.5% (n=101) | 10.8% (n=86) | −5.7pp |
| D: Grouped account | 24.3% (n=149) | **29.9% (n=238)** | +5.6pp |
| E: Hierarchical ledger | 18.0% (n=110) | 18.4% (n=147) | +0.4pp |
| F: Deep hierarchy | 23.5% (n=144) | 23.2% (n=185) | −0.3pp |

**Reading the changes:**
- **D rises** because it was hidden inside complex quipu.
- **B rises** for the same reason — flat color-organized sections inside larger documents.
- **A nearly vanishes** at section level — tally strips are whole small quipu, rarely sections of larger ones.
- **C drops** — some C quipu decompose into more specific section types.
- **E and F are stable** — they tend to be standalone, not assembled from parts.

---

## Census as Content Type (Not Form Type)

**Critical v2 finding:** Census is not a form type. It is a **content type**
that spans multiple forms.

31 census-like sections identified (6-block color grouping ≥50%):
- **Forms:** D (12), E (8), F (6), C (3), B (2)
- **84% embedded** within larger quipu (26/31), not standalone
- **12 proveniences** empire-wide: Santa (12), Paracas (3), Ica (2),
  Nazca (1), Pachacamac (1), Leymebamba (1), Chancay (1), Costa Sur (2), + others

**The census signature** (independent of form):
1. Pendants grouped in same-color blocks of 6 (the 6-block)
2. Mixed recto/verso attachment (moiety marking: verso = hanan, recto = hurin)
3. Small per-cord values (individual tax amounts, not bulk totals)
4. Color = name bucket (per Medrano & Urton 2018)

**The Santa "Rosetta" quipu (1000274)** — one of the six Medrano & Urton
census quipu — is itself composite: Section 1 = D (100% 6-block),
Section 2 = E (71% 6-block), separated by a color shift. The published
"132 tributaries" aggregates across sections.

**Implication:** The Inca census was a **document genre**, not a physical
template. The same census content could be recorded on D, E, F, B, or C
architecture. This confirms the v1 finding that **form and content are
orthogonal** — and extends it to the section level.

---

## Decision Tree (Section-Level)

Classify any quipu **section** (a contiguous run of pendants between
boundaries):

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

**To classify a quipu:**
1. Detect section boundaries (red dividers, R/V flips, color shifts, structural breaks)
2. Apply the tree to each section independently
3. Record the section form sequence (e.g., "D+F", "B+B+D")

**Validation:** 97% agreement on single-section quipu (128/132).
The tree is consistent; the v1 whole-quipu labels were conflating sections.

---

## Composite Patterns

### Most common section sequences

| Sequence | Count | Interpretation |
|----------|------:|---------------|
| E (single) | 36 | Standalone ledger |
| B (single) | 27 | Standalone register |
| F (single) | 27 | Standalone deep hierarchy |
| C (single) | 22 | Standalone list |
| D (single) | 20 | Standalone grouped account |
| D+F | 14 | Detail + imperial summary |
| F+F | 12 | Related deep documents filed together |
| B+B | 11 | Related registers filed together |
| D+D | 10 | Related accounts filed together |
| D+E | 9 | Detail + systematic ledger |

### Same-form repeats = filing

When a quipu contains B+B or F+F or D+D, it is likely **multiple related
documents bound together** — the Andean equivalent of stapling reports.
The sections are independent; they share a primary cord for storage.

### Mixed-form = composite report

D+F or D+E combinations suggest **a single administrative product** combining
different levels of detail — summary sections alongside breakdown sections.

### Extreme case: 1000096 (Lluta Valley)

40 sections cycling through all six forms (A–F), 11 red-divider boundaries.
This is not a document — it is a **cord-bound archive**. Dozens of distinct
records tied to one primary cord. The southern imperial fringe used the most
extreme composite format.

---

## Geographic Distribution (Section-Level)

All six forms appear at 5–30 distinct sites each. No form is site-specific.

| Form | Sites | Interpretation |
|------|------:|---------------|
| D | 30 | Universal — the standard bureaucratic unit everywhere |
| F | 29 | Universal — deep hierarchy used empire-wide |
| B | 25 | Widespread — color-register convention |
| E | 23 | Widespread — systematic ledger convention |
| C | 19 | Common — simple list |
| A | 5 | Rare — tally strips are local/personal |

**The toolkit was imperially standardized.** Every region used the same six
section forms. What varied was **which forms were combined** and **in what
proportions** — institutional usage patterns, not regional dialects.

---

## What This Means (v2)

### 1. The quipu is a file folder

The primary cord is a binding mechanism, not a document boundary. A quipu
contains one or more sections; each section is a document conforming to one
of six form types.

### 2. D is the atomic unit of Inca bureaucracy

At 29.9% of sections across 30 sites, the grouped account (D) is the
standard building block. Complex documents are assembled from D-type
sections plus specialized components (E for systematic breakdown, F for
deep aggregation, B for color-organized registers).

### 3. Form and content are fully orthogonal

Census content appears in D, E, F, B, and C sections. The same information
can be recorded on different architectures; the same architecture can hold
different information. This is the hallmark of a mature bureaucratic writing
system — like modern forms where the IRS 1040 has fixed structure regardless
of whose taxes it holds.

### 4. The blank form is simpler than v1 suggested

The quipucamayoc does not choose one of six templates for a whole quipu.
They assemble sections: "I need a D section for the accounts, a B section
for the color-coded inventory, and an F section for the imperial summary."
The six types are **section templates**, not document templates.

### 5. Red and R/V are punctuation, not content

Red dividers and recto/verso flips are the quipu equivalent of headings
and page breaks. They organize multi-section documents. They do not encode
commodity type, value, or administrative level.

---

## Files

- This framework: `~/workspace/quipu-analysis/form-types-v2.md`
- v1 framework (superseded): `~/workspace/quipu-analysis/quipu-form-types.md`
- Section data: `~/workspace/quipu-analysis/quipu-sections.csv` (797 sections)
- Section summary: `~/workspace/quipu-analysis/section-summary.csv` (per form type)
- Quipu section index: `~/workspace/quipu-analysis/quipu-section-index.csv` (per quipu)
- Updated classification: `~/workspace/quipu-analysis/quipu-classification.csv`
  (now includes IS_COMPOSITE, SECTION_FORMS, N_SECTIONS)
- Section analysis: `~/workspace/quipu-analysis/section-classification.md`
- Census analysis: `~/workspace/quipu-analysis/census-search.md`
- Database: `~/workspace/quipu-analysis/okr-khipu.db`

---

## Limitations

1. Section boundary detection uses fixed thresholds. Subtler boundaries may
   be missed; some detected boundaries may reflect scribal variation.
2. 291 quipu with <30 pendants were not sectioned (assumed single-section).
   Some may contain undetected internal boundaries.
3. The D/E boundary at 40/41 pendants remains a clustering artifact.
4. Knot-value decoding was not used in section classification.
5. Color data uses Ascher codes as recorded; fading may create false boundaries.
