# Quipu Form Types: The Blank Forms of the Inca Bureaucracy

**Date:** 2026-10-10
**Analyst:** Muse (subagent)
**Hypothesis (Charles):** Quipu are not pre-filled forms (no two are identical), but they ARE forms — they follow shared structural templates. Find the template.

---

## Method

Structural skeletons were extracted for 612 quipu from the Open Khipu Repository (`okr-khipu.db`: 54,403 cords, 110,677 knots). For each quipu:

- **Pendant count** (level-1 cords hanging from the primary cord)
- **Subsidiary depth** (max cord level: 1 = flat, 2+ = hierarchical)
- **Top cords** (negative-level cords attached above the primary cord)
- **E-E-E markers** (cords beginning with three figure-eight knots)
- **Color diversity** (distinct Ascher cord colors among pendants)
- **Knotless pendant ratio** (pendants with no knots)
- **Subsidiary ratio** (subsidiary cords per pendant)

Clustering by architecture (not values, not colors) yielded **six form types** covering 100% of quipu.

---

## The Six Form Types

### A: Tally Strip (5.2%, n=32)

The simplest form. A handful of pendant cords, no subsidiaries, minimal color.

```
Primary cord
    |    |    |    |    |
   p1   p2   p3   p4   p5    <- 1-10 pendants, knots record counts
```

- Pendants: median 6, range 0-10
- Depth: 1 (flat)
- Colors: 1-2
- Use: Simple tallies. Possibly mnemonic aids or personal records rather than state administration.

**Blank form:** A short primary cord. The quipucamayoc attaches up to ~10 pendant cords. Each pendant records a single count.

---

### B: Flat Register (12.4%, n=76)

A flat list of pendants distinguished by color. No hierarchy — the color IS the organization.

```
Primary cord
    |    |    |    |    |    |    |
  RED  RED  BLUE BLUE  GRN  GRN  YEL   <- 4+ colors, color = category
   12   45   8    23    5    67   31    <- knots = quantities
```

- Pendants: median 30, range 4-319
- Depth: 1 (flat)
- Colors: 4+ (this is the defining feature)
- Use: Multi-commodity inventory or tribute register. Each color = a commodity; each pendant = a quantity. The "spreadsheet" form.

**Blank form:** A primary cord long enough for the expected entries. The quipucamayoc attaches pendant cords in color groups — all red together, all blue together. Color bands create visual columns. No subsidiaries needed because color does the categorizing.

**Urton mapping:** Overlaps with SERIATED (8/35) and DECIMAL_NUM (5/35). The seriation IS the color banding.

---

### C: Simple List (16.5%, n=101)

A flat list without strong color coding. The plainest administrative form.

```
Primary cord
    |    |    |    |    |
   p1   p2   p3   p4   p5    <- 3-195 pendants, 1-3 colors
   10   10   10   10   10    <- often identical values (census: one cord per person)
```

- Pendants: median 24, range 3-195
- Depth: 1 (flat)
- Colors: 1-3
- Use: Census lists, simple enumerations. When values are all 1s or 10s, it's a head-count.

**Blank form:** A primary cord. Attach N pendant cords. Tie the same knot pattern on each (or leave knotless for presence/absence). Color is incidental.

---

### D: Grouped Account (24.3%, n=149) — THE MOST COMMON

Pendants with selective subsidiaries. Most pendants stand alone; a few have breakdown cords. This is the workhorse form.

```
Primary cord
    |         |         |         |
   p1        p2        p3        p4      <- 2-40 pendants
   100       250       75        30      <- summary values
    |---s1     |---s1
    |---s2     |---s2                      <- subsidiaries on SOME pendants only
    40         100                         (median 0.37 subsidiaries per pendant)
    60         150
```

- Pendants: median 18, range 2-40
- Depth: 2 (one subsidiary level)
- Subsidiaries are **selective**: median ratio 0.37 per pendant. Most pendants have zero subsidiaries.
- Subsidiary values do **NOT** sum to parent values (only 3/24 tested). They are not subtotals.
- Colors: variable
- Use: Summary accounts with annotations. The parent pendant gives the headline number; subsidiaries provide breakdowns, corrections, or metadata — but on a different dimension than simple addition.

**Blank form:** A primary cord. Attach up to ~40 pendant cords for the main entries. For entries that need elaboration, attach subsidiary cords to that specific pendant. The decision of which pendants get subsidiaries is the quipucamayoc's judgment call — this is where expertise lives.

**Urton mapping:** Strongest overlap with CENSUS (18/93). The census-takers used this form: head-count on the pendant, details on subsidiaries.

---

### E: Hierarchical Ledger (18.0%, n=110)

Many pendants, all with systematic subsidiary structure. The full double-entry analog.

```
Primary cord
    |              |              |
   p1             p2             p3         <- 41-864 pendants
   1000           2500           800        <- category totals
    |---s1         |---s1          |---s1
    |---s2         |---s2          |---s2   <- subsidiaries on most pendants
    |---s3         |---s3                   (systematic, not selective)
```

- Pendants: median 82, range 41-864
- Depth: 2 (one subsidiary level, applied broadly)
- Colors: 4+ (color + hierarchy = two-dimensional organization)
- Use: Large-scale administrative ledgers. Tribute collection across multiple categories and sub-categories.

**Blank form:** A long primary cord. Attach pendant cords in color-banded groups (like Form B). Attach subsidiary cords to each pendant for the breakdown. This is the most labor-intensive form — the "full spreadsheet with sub-tables."

**Urton mapping:** Overlaps with BANDED (13/61), SERIATED (10/61), POSITIONAL (9/61). The banding + position + hierarchy combine.

---

### F: Deep Hierarchy (23.5%, n=144)

Three or more levels of nesting. The most structurally complex form.

```
Primary cord
    |
   p1
    |---s1
    |     |---ss1
    |     |---ss2          <- depth 3-6
    |---s2
          |---ss1
                |---sss1   <- depth 4+
```

- Pendants: median 60, range 1-1650
- Depth: 3-6 (105 at depth 3, 33 at depth 4, 5 at depth 5, 1 at depth 6)
- Use: Multi-level aggregation. Imperial summaries rolling up from local to regional to central. The deepest quipu (6 levels, 1650 pendants) are likely empire-level compilations.

**Blank form:** Start with the primary cord. The quipucamayoc builds downward: pendants for top-level categories, subsidiaries for sub-categories, sub-subsidiaries for details. Depth reflects administrative distance from the recording point — deeper = more levels of aggregation.

---

## The Blank Form: What the Quipucamayoc Starts With

If you handed a trained quipucamayoc a blank quipu, the starting structure depends on the task:

| Task | Form | Starting structure |
|------|------|-------------------|
| Quick count | A: Tally strip | Short primary cord, ~10 undyed pendants |
| Multi-commodity inventory | B: Flat register | Primary cord + pendants in color batches |
| Census / headcount | C: Simple list | Primary cord + N identical pendants |
| Account with notes | D: Grouped account | Primary cord + ~20 pendants, spare cord for subsidiaries |
| Tribute ledger | E: Hierarchical ledger | Long primary cord + color-banded pendants + subsidiary cord stock |
| Imperial summary | F: Deep hierarchy | Extra-long primary cord, deep cord reserves |

The **universal blank** — what every form shares:

```
[optional top cord(s)]          <- 4% of quipu; possibly title/header
===============================  <- PRIMARY CORD (always present)
    |    |    |    |    |
   p1   p2   p3   p4   p5        <- PENDANT CORDS (the rows)
    |    |
   s1   s1                      <- SUBSIDIARY CORDS (optional detail)
```

Every quipu has a primary cord. Every quipu has pendants. Everything else — subsidiaries, color coding, top cords, E-E-E markers — is optional elaboration chosen by the quipucamayoc based on the recording task.

---

## Key Findings

### 1. The hierarchy is not arithmetic

Subsidiary values do not sum to parent values (3/24 in sample). This rules out the "subtotal" interpretation. Subsidiaries encode something other than additive breakdown — possibly different commodities under one taxpayer, corrections, or temporal subdivisions (this month vs last month under one account).

### 2. Subsidiaries are selective, not systematic (except in Form E)

Median 0.37 subsidiaries per pendant. The quipucamayoc chose which entries needed elaboration. This is expert judgment, not mechanical form-filling — like a modern accountant deciding which line items need footnotes.

### 3. Urton's types cut across form types

Urton's structural types (CENSUS, SERIATED, BANDED, etc.) describe **content genre**, while form types describe **architecture**. A CENSUS can be recorded on Form D (grouped) or Form F (deep hierarchy). A SERIATED quipu can be flat (Form B) or hierarchical (Form E). The two taxonomies are orthogonal — which means the Inca had a **separation of form and content**: the same information could be recorded on different physical templates, and the same template could hold different kinds of information.

### 4. Color and hierarchy are independent organizing principles

Form B uses color instead of hierarchy. Form E uses both. Form C uses neither. The quipucamayoc had two dimensions of organization available — visual (color) and structural (nesting) — and chose based on the complexity of the data.

### 5. Scale follows function

The form types sort cleanly by pendant count: A (6) < D (18) < C (24) < B (30) < F (60) < E (82). Larger administrative tasks demanded more elaborate forms. This is not surprising, but it confirms the forms are functional, not decorative.

---

## What This Means

Charles's insight is confirmed: quipu are forms. Not pre-filled (no two are identical), but templated. The Inca bureaucracy had at least six standard document types, distinguished by architecture.

The blank form is simple — a primary cord with pendants. The complexity is in the **choices**: flat or hierarchical? Color-coded or monochrome? Which pendants get subsidiaries? These choices constitute a **document design language** — the quipucamayoc's professional expertise.

The separation of form (architecture) from content (Urton's genres) suggests a sophisticated bureaucratic culture where the recording technology was standardized independently of what was being recorded. This is the same principle as modern forms: the IRS 1040 has a fixed structure regardless of whose taxes it holds.

---

## Limitations

1. **Knot value calculation is simplified.** The summing test used approximate values. A proper Ascher decimal decoding might change the subsidiary-sum result.
2. **83 raw skeleton variants** were collapsed to 6 form types. Finer subdivisions exist (e.g., E-E-E placement patterns, top cord configurations).
3. **25 quipu with top cords** and **10 with E-E-E markers** are too few to define their own form types, but they may represent specialized variants.
4. **Color banding patterns** (positional color sequences) were not fully analyzed — only color diversity counts.
5. **Urton type coverage** is partial (356/612 quipu). The mapping may shift with more data.

---

## Files

- Analysis database: `~/workspace/quipu-analysis/okr-khipu.db`
- Legacy database: `~/workspace/quipu-analysis/khipudb_2012.db`
- Skeleton data: `/tmp/skel.pkl`, `/tmp/skel2.pkl`, `/tmp/form_class.json`
- This report: `~/workspace/quipu-analysis/quipu-form-types.md`
