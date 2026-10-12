# Khipu Spreadsheet Conversion Report

**Date:** 2026-10-12
**Pipeline:** `~/workspace/quipu-analysis/build_spreadsheets.py`
**Output:** `~/workspace/quipu-analysis/spreadsheets/by_khipu/` (619 CSVs) + `spreadsheet_index.csv`

## What this is

Every khipu in the Open Khipu Repository database, exported as a spreadsheet. No decipherment — just structure, numbers, and metadata. The Inca database, exported to CSV.

Each file opens with `#` comment lines carrying the metadata (provenance, region, museum, format, data regime, template, segmentation method), followed by the data table.

## Conversion results

| Format | Count | Description |
|--------|-------|-------------|
| `.tab` | 191 | True spreadsheets: rows × color-coded columns |
| `.flat` | 410 | Flat cord lists (no row structure) |
| `.log` | 5 | Journals with ENTRY/DELIMITER roles |
| `.cod` | 5 | Code khipu (categorical tag systems) |
| `.chk` | 1 | Checklist (1000522) |
| no cords | 7 | In catalog, no cord data (1000464–1000470) |
| **Total** | **619** | |

### `.tab` by segmentation method

| Method | Count | How rows are defined |
|--------|-------|---------------------|
| value_marker | 110 | Repeating (color, value) pair at regular intervals (e.g. BY=22) |
| white_dividers | 48 | Sections split by 3+ white cord runs |
| color_cycle | 33 | Dominant color bigram rotation (e.g. BL→BY→MB→W) |

- Median `.tab`: 8 rows × 10 columns. Largest: 67 rows; widest: 117 columns.
- `.tab` files carry a second header row annotating each column as MARKER, CONSTANT, or VARIABLE.
- `ROW_ID`, `IS_MARKER_ROW`, `SECTION` metadata columns on every `.tab`.
- For `value_marker` khipu, overlong leading fragments are chunked to the median row length so the positional pivot stays meaningful (e.g. 1000344 went from 15×126 to 33×12).

### `.flat` (410 khipu)

Columns: ORDINAL, LEVEL, COLOR1, COLOR2, VALUE, KNOTS. Median 21 cords; largest 864. This is the unpivotable set: hierarchical khipu, unstructured pieces, fragments, and the 26 funerary-context khipu.

### `.log` (5 journals)

1000103, 1000183, 1000368, 1000501, 1000063. Same flat columns plus ROLE (ENTRY vs DELIMITER, where delimiters are 3+ white runs).

### Data regime coverage

165 of the 200 templated khipu carry a data-regime label (DC1–DC6); 35 are marked `unclustered` (<10 variable values). Regimes describe *what scale* of numbers a khipu records, independent of its layout.

## Known limitations

1. **TF unary override.** One khipu (1000522) uses tufted knots as a unary tally. The decimal decoder mangles these (4 tufts → 1110), so pure-TF cords report tuft counts instead. Flagged in the file's metadata.
2. **Duplicate ordinals.** Some khipu have multiple cord rows per ordinal (e.g. 1000368: 404 rows, 252 ordinals). Spreadsheets use one row per unique ordinal (first-seen wins for color/level; knots aggregated across duplicates).
3. **Zero vs blank.** Empty cells mean zero or no value. The distinction between "recorded zero" and "empty position" is not always recoverable from the database.
4. **Positional pivot assumption.** `.tab` columns assume position-within-row corresponds to the same field across rows. True for regular templates; approximate for variable-length rows.
5. **Column names unknown.** Headers are color codes (W, AB, MB...), the de facto field identifiers. The actual field labels (what the colors *mean*) remain the unsolved problem.
6. **Inkawasi decode confidence.** Long-knot values from Inkawasi khipu lack NUM_TURNS in the source; treated per existing decoder behavior.

## How to use

- **Browse:** open `spreadsheet_index.csv`, filter by format/regime/region, open any `by_khipu/{id}.csv`.
- **Example — the form:** `by_khipu/1000344.csv` shows the template directly (BY=22 markers, constant columns, one variable field).
- **Example — the journal:** `by_khipu/1000368.csv` shows ENTRY/DELIMITER structure.
- **Example — the checklist:** `by_khipu/1000522.csv` shows the tuft-graded inspection form.
