# khipu

Computational khipu research: data recovery, structural grammar, and generative encoding.

## What's here

This repository has two main components:

### 1. Harvard Khipu Database (KDB) Recovery Record

A recovery record for the legacy Harvard Khipu Database (`khipukamayuq.fas.harvard.edu`;
Gary Urton, PI; Carrie Brezine, database manager), which went offline. In July 2026,
**345 uniquely archived data files** were enumerated and recovered from Internet
Archive Wayback Machine captures — hand-curated per-khipu Excel recording sheets,
catalogs, and a full 2012 SQL dump.

The recovery establishes what was recovered, from which snapshots, with what
checksums, and how the recovery can be reproduced and validated. It deliberately
does **not** republish the recovered files themselves — those are the intellectual
work of the Harvard Khipu Database Project.

Key files are under `structural-spec/` (alongside the grammar work):

| File | Description |
|---|---|
| `MANIFEST.csv` | One row per recovered file (357 rows): path, source, original URL, Wayback snapshot timestamp, size, SHA-256 |
| `recover_kdb_wayback.py` | Recovery tool (Python, MIT license): enumerates via the Wayback CDX API, downloads latest captures, regenerates the manifest. Idempotent |
| `07_kdb_corpus_findings.md` | Validation of 274 Brezine-format sheets (26,108 cord rows, zero parse errors), cross-validated against the OKR |
| `10_field_sheet_findings.md` | Validation of 66 raw field-recording sheets (6,686 cord rows), 99.99% per-cord value agreement with the OKR |

Full documentation: [`structural-spec/README.md`](structural-spec/README.md)

**Authors:** Edinson Sánchez (independent researcher, Ecuador) · Claude (AI collaborator).
`recover_kdb_wayback.py` under MIT; all other recovery files under CC BY 4.0.

### 2. Document Specification for Inca Accounting Khipu (v0.2)

A formal document specification for Inca accounting khipu, modeled on ECMA-404 (JSON spec).
If the spec is complete, we can encode — not just decode.

**Scope:** administrative and accounting khipu only. Funerary khipu (26 in the OKR,
a distinct document class) are excluded from the structural analysis, as are
post-conquest phonetic khipu. The claim is about the Inca state's bureaucratic
record-keeping, not about every knotted cord ever tied.

**The six rules:**

| Rule | Statement | OKR result | KFG out-of-sample |
|---|---|---|---|
| R1 | Exactly one primary cord | 612/612 (100%) | 66/66 (100%) |
| R2 | Direct pendants at level 1 or negative top level | 193/193 (100%) | 66/66 (100%) |
| R3 | Subsidiaries do not attach directly to primary | 403/403 (100%) | 49/49 (100%) |
| R4 | Every cord has recorded color | 439/612 (71.7%) | 66/66 (100%) |
| R5 | At least one knotted cord | 593/612 (96.9%) | 65/66 (98.5%) |
| R6 | Top cords form a valid tree above the primary | 4/25 (16%) | Not testable |

R1–R3 are structural universals: they hold at 100% on the OKR corpus and
replicate at 100% on an independent dataset (Khipu Field Guide, 66 khipu
absent from the OKR snapshot). They also hold at 100% on 22 Leymebamba
funerary khipu — a distinct document class excluded from the accounting
analysis — suggesting the structural core describes khipu construction
generally, not just bureaucratic convention.

On the failures: every R4/R5 non-conformant specimen examined is an
incomplete database record, not a structural violation. The worst offenders
(e.g., 1000088: 195 cords, zero knots, zero colors) are data-entry stubs
where cord counts were logged but never filled in. R6 failures trace to
misattributed parent IDs in the source data — top cords on khipu 1000024
carry PENDANT_FROM values pointing at khipu 1000023, a cross-contamination
between consecutive records, not a real attachment violation. No examined
khipu in either corpus violates the structural rules; the non-conformance
is in the data, not in the khipu. R4–R5 remain reported with rates as a
data-quality caveat. R6 is unresolved pending source verification.

**Key files** (under `structural-spec/`):

| File | Description |
|---|---|
| `spreadsheet_to_khipu.py` | **Spreadsheet-to-khipu encoder.** Takes tabular data and generates a structurally valid khipu tree (JSON + ASCII visualization), with Inca-style decimal knot clusters. The generative proof of the spec |
| `conformance_test_v2.py` | Six-rule conformance test against the OKR database (619 khipu) |
| `conformance_test_kfg.py` | Out-of-sample conformance test against Khipu Field Guide data (66 khipu) |
| `khipu_catalog_khipu.json` | **Meta-khipu**: a khipu encoding the entire khipu database — 4 pendants, 619 subsidiaries each, knot-encoded totals (54,403 cords, 37,082 knotted) |
| `meta_khipu_diagram.png` | Diagram of the meta-khipu |
| `funerary-side-by-side.html` | Side-by-side visualization of 26 funerary khipu |
| `scripts/download_kfg.py` | Khipu Field Guide download tool |
| `scripts/parse_kfg.py` | Khipu Field Guide parser |

**Quick start — encode your own spreadsheet as a khipu:**

```bash
cd structural-spec
python3 spreadsheet_to_khipu.py my_data.csv
```

The encoder maps spreadsheet columns to pendant cords (color-coded), cell values
to Inca-style decimal knot clusters, and rows to subsidiary cords. Output is a
JSON khipu tree plus ASCII visualization, with a spec conformance check.

**Data sources:**

- Open Khipu Repository (OKR): https://github.com/khipulab/open-khipu-repository
- Khipu Field Guide: source files parsed via `scripts/download_kfg.py` (66 Excel files)

The SQLite databases (`okr-khipu.db`, `kfg-khipu.db`) are excluded from version
control — rebuild them from the scripts and source data.

## References

- Medrano, M., & Urton, G. (2018). Toward the Decipherment of a Set of Mid-Colonial Khipus from the Santa Valley. *Ethnohistory*, 65(1), 1–23.
- Urton, G., & Brezine, C. J. (2005). Khipu Accounting in Ancient Peru. *Science*, 309(5737), 1065–1067.
- Thompson, K. M. (2025). A Numerical Connection Between Two Khipus. *Ñawpa Pacha*, 45(1), 83–104.
- Open Khipu Repository: https://github.com/khipulab/open-khipu-repository

## License

The structural spec, encoder, and associated work are **CC BY 4.0** — use it for
anything, including commercially, with attribution. If you can monetize turning
a spreadsheet into a khipu, you deserve the money. See [LICENSE](LICENSE).
