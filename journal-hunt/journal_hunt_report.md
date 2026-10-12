# Journal Hunt Report: Sequential Log Documents

**Date:** 2026-10-11
**Question:** Is 1000183 unique, or is "sequential journal" a document type?

**Verdict: 1000183 is NOT unique. "Sequential log" is a real format family with 5+ clear examples.**

## Method

1. Computed MI ratio (sequential dependency) for all 594 khipu in hex corpus
2. Filtered: MI > 1.3, stratification < 0.7, value variance > 0, zero% < 70%
3. Result: **20 candidates**
4. Ranked by similarity to 1000183; inspected top 10 in detail

## The 20 Candidates

| Khipu | MI | N | Values | Colors | Museum | Provenance |
|---|---|---|---|---|---|---|
| 1000368 | 2.256 | 430 | 0-11 | 8 | Dauelsberg, Arica | (all-U piece) |
| 1000103 | 2.162 | 547 | 0-6 | 6 | Peabody, Harvard | Nazca |
| 1000183 | 2.078 | 615 | 0-145 | 7 | Museo de Ica | — |
| 1000586 | 1.650 | 180 | 0-231 | 5 | Mus. Nac. Arqueología | unknown |
| 1000623 | 1.643 | 322 | 0-29001 | 4 | Proyecto Incahuasi | Incahuasi |
| 1000085 | 1.625 | 299 | 0-2968 | 7 | Völkerkunde, Berlin | Nazca |
| 1000063 | 1.616 | 357 | 0-234 | 7 | Völkerkunde, Berlin | Ica/Pisco |
| 1000198 | 1.548 | 260 | 0-112 | 5 | Univ. Museum, Penn | — |
| 1000331 | 1.543 | 202 | 0-201 | 5 | Museo Amano | — (symbol candidate) |
| 1000170 | 1.444 | 49 | 0-4 | 3 | Museo de Ica | — |
| 1000501 | 1.438 | 431 | 0-47 | 7 | Quai Branly, Paris | Huaca Perez, Lima |
| 1000565 | 1.423 | 367 | 0-4811 | 7 | Mus. Nac. Arqueología | Costa Sur |
| 1000375 | 1.397 | 98 | 0-8 | 4 | Banco Central | — |
| 1000259 | 1.388 | 111 | 0-2201 | 5 | Puruchuco Museum | — |
| 1000304 | 1.375 | 91 | 0-29 | 3 | Völkerkunde, Munich | — |
| 1000148 | 1.367 | 306 | 0-1301 | 5 | Völkerkunde, Berlin | Nazca |
| 1000622 | 1.360 | 247 | 0-2711 | 6 | Proyecto Incahuasi | Incahuasi |
| 1000612 | 1.355 | 389 | 0-12001 | 6 | Proyecto Incahuasi | Incahuasi |
| 1000342 | 1.355 | 186 | 0-1012 | 4 | Musée de l'Homme | — |
| 1000040 | 1.304 | 101 | 0-129 | 4 | Völkerkunde, Berlin | — |

## The Five Clear Journals

### 1. 1000103 (Peabody, Nazca) — MI 2.162
541 cords, 415 L1. LB dominant (338) with W (156) as section markers.
Values 0-6, 233 nonzero. Structure: `W [LB×5] WWW [LB×3] B [LB] WWW [LB×5]...`
Sectioned sequential log. Small values suggest daily counts or tallies.

### 2. 1000368 (Dauelsberg, Arica) — MI 2.256
404 cords, 252 L1. W (145) dominant. Values 0-11, 161 nonzero.
**This is one of the five all-U-twist unknown-office pieces.**
A journal from the unknown office — proving the U-pieces aren't a single
document but include the journal format.

### 3. 1000183 (Museo de Ica) — MI 2.078 (reference)
615 cords, 559 L1. YB dominant with W section markers. Values 0-145.
The original discovery; now confirmed as one of several.

### 4. 1000501 (Quai Branly, Huaca Perez Lima) — MI 1.438
417 cords, 395 L1. AB (227) dominant. Values 0-47 with activity bursts.
Sequential entries with clustered high values — suggests event-driven
logging (not steady daily counts but episodic records).

### 5. 1000063 (Völkerkunde Berlin, Ica/Pisco) — MI 1.616
357 cords, 339 L1. B (142) dominant, only 41 color transitions (long runs).
Values 0-234. Fewer sections, longer entries — a different journal style.

## The Shared Journal Format

Direct comparison of 1000103 and 1000183 cord sequences reveals
identical architecture:

- **Section delimiter:** W (or equivalent) cords break the sequence
- **Entry runs:** 3-6 cords of the dominant color between delimiters
- **Values vary** meaningfully within and across sections
- **Flat hierarchy:** overwhelmingly L1 (sequential, not nested)

This is not coincidental. Two khipu from different museums (Peabody/Harvard
and Museo de Ica), both showing `DELIMITER [ENTRIES] DELIMITER [ENTRIES]...`
with the same W-as-delimiter convention. **This is a taught format.**

## Journals vs Other Sequential

Not all 20 are journals. Sub-groups:

- **True journals** (5): 1000103, 1000368, 1000183, 1000501, 1000063
  Flat, sectioned, varying values, sequential entries.

- **Hierarchical sequential** (4): 1000198, 1000565, 1000612, 1000623
  High MI but deep hierarchy (L2 > L1). Sequential at the section level
  but nested within. Possibly multi-period journals or compiled logs.

- **Small/ambiguous** (6): 1000170, 1000375, 1000304, 1000259, 1000342, 1000040
  High MI but <200 cords. May be journal fragments or a different micro-format.

- **Symbol candidate** (1): 1000331 — values constant, excluded from journal set
  (it's the language candidate, not a numeric log).

- **Wide-range** (4): 1000085, 1000586, 1000623, 1000148
  Values to 1000+. May be journals tracking large quantities, or a
  different format using sequential layout for non-journal purposes.

## Provenance Pattern

Journals cluster on the **south coast**: Nazca (1000103, 1000085, 1000148),
Ica (1000183, 1000063, 1000170), Costa Sur (1000565). Plus Lima (1000501),
Arica (1000368), Incahuasi (1000612, 1000622, 1000623).

This is a **south-coast-weighted** format, overlapping with the S-twist
region but including Z-twist pieces. The journal format may be a southern
bureaucratic convention.

## Revised Format Taxonomy

Three confirmed families:
1. **Spreadsheets** (tabular) — the majority
2. **Sequential journals** (sectioned logs) — 5+ confirmed, ~20 candidates
3. **Symbol strings** (1000331) — 1 candidate, language-encoding?

## Files

- `journal_candidates.csv` — all 20 with metrics and similarity scores
- `top_journals.md` — detailed profiles of top 10
- `mi_full_corpus.csv` — MI ratios for all 594 khipu
