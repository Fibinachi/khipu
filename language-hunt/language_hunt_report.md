# Language Hunt: Verdict

**Date:** 2026-10-11
**Question:** Does the khipu corpus contain documents that encode sequential
language rather than tabular/spreadsheet data?

## Short answer

**One strong candidate (1000331).** No confirmed language-encoding khipu.
The null hypothesis ("all khipu are spreadsheets/tabular") is weakened but
not rejected.

## What was done

1. Started from 147 unclassified residuals.
2. Excluded 89 with spreadsheet signatures (stratification, zero-heavy, column repetition).
3. Remaining 49 scored on: Shannon entropy, n-gram uniqueness, hapax rate.
4. Top candidates tested for sequential dependency via mutual information
   (observed MI vs shuffled-MI baseline).
5. Highest-MI candidates inspected cord-by-cord.

## Key finding: the MI test

Most khipu show MI ratio ≈ 1.0: cord order is statistically independent,
consistent with spreadsheet rows. Five khipu show MI ratio > 1.3:

| Khipu | Cords | MI ratio | Provenance | Assessment |
|---|---|---|---|---|
| 1000183 | 615 | 2.13 | Museo de Ica, no prov. | Sequential log/journal (numeric) |
| 1000176 | 38 | 1.55 | Museo de Ica, no prov. | Possible fragment |
| 1000331 | 198 | 1.50 | Museo Amano, no prov. | **Symbol encoding (best candidate)** |
| 1000382 | 76 | 1.39 | Museo Temple Radicati | Ambiguous |
| 1000083 | 183 | 1.33 | Ica (Berlin) | Binary encoding |

## The 1000331 case

- 142 of 198 values = exactly 2 (constant). Numeric channel carries no information.
- 14 distinct color/symbol types in sequence: AB, W, MB, AB+SY, BG, PK+AB...
- Sequential order is non-random (MI 1.5x baseline).
- This is NOT a spreadsheet (no columns, no varying values, no stratification).
- This IS a sequential symbol string.

**What it could be:**
1. Symbolic language (colors as words/morphemes) — unproven
2. Categorical event log (colors as event types in order) — plausible
3. Ritual sequence (colors as ceremonial elements) — plausible

**What would distinguish:** grammatical constraints in the symbol sequence
(e.g., certain symbols only follow certain others in rule-like ways, beyond
simple alternation). Not yet tested. External context (provenance, associated
artifacts) unavailable.

## The 1000183 case (important negative)

Highest MI ratio (2.13) but clearly NOT language: 559 sequential entries with
meaningful numeric values (0-71). This is a **time-series** or **journal** —
sequential data, but numeric. It proves that "non-spreadsheet" ≠ "language."
Sequential numeric logs exist as a third format family.

## Revised format taxonomy

The hunt suggests THREE format families, not two:

1. **Spreadsheets** (tabular): census, warehouse, tally. Columns, rows, headers.
2. **Sequential logs** (time-series): 1000183-type. Ordered entries, numeric values, no columns.
3. **Symbol strings** (sequential symbolic): 1000331-type. Ordered symbols, constant/filler values.

Only family 3 is a candidate for language encoding. N=1 confirmed, a few
more possibles (1000029, 1000287 need deeper inspection).

## Limitations

- No provenance for 1000331 (Museo Amano, Lima; no excavation context).
- Symbol-grammar test not performed (would need bigger N or clearer patterns).
- The "all-U" khipu (1000029 etc.) overlap with high-MI set; unknown-office
  connection unexplored.
- 89 excluded as "spreadsheet-positive" by heuristic thresholds; some may
  deserve re-examination.

## Deliverables

- [spreadsheet_negative.csv](sandbox://workspace/quipu-analysis/language-hunt/spreadsheet_negative.csv) — 49 candidates passing spreadsheet-negative filter
- [language_positive.csv](sandbox://workspace/quipu-analysis/language-hunt/language_positive.csv) — ranked by language-likeness score
- [mi_analysis.csv](sandbox://workspace/quipu-analysis/language-hunt/mi_analysis.csv) — MI ratios for all 49
- [top_candidates.md](sandbox://workspace/quipu-analysis/language-hunt/top_candidates.md) — detailed profiles
- [candidate_sequences.txt](sandbox://workspace/quipu-analysis/language-hunt/candidate_sequences.txt) — raw cord sequences for top 15
- Scripts: `hunt.py`, `inspect.py`, `mi_test.py`, `inspect_mi.py` (all reproducible)

## Recommendation

**1000331 deserves dedicated study.** Pull the physical khipu (Museo Amano),
check for associated context, test the symbol sequence for grammatical
constraints. If the color sequence shows rule-like dependencies (not just
alternation), it may be the first identified language-encoding khipu.

**1000183 deserves reclassification** as sequential-log format, not
deep_sparse_mixed. It may represent a document type (journal/diary) distinct
from both spreadsheets and symbol strings.
