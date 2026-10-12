# Recovery Record of the Harvard Khipu Database (KDB) Legacy Archive

**Edinson Sánchez¹ · Claude²**
¹ Independent researcher, Ecuador — esanchezf777@gmail.com
² AI research collaborator (Claude Fable 5, Anthropic)

**Version 1.0 — July 2026**

## What this deposit is

The original Harvard Khipu Database website (`khipukamayuq.fas.harvard.edu`; Gary
Urton, PI; Carrie Brezine, database manager) went offline, and its `DataTables/`
holdings — hand-curated per-khipu Excel recording sheets, catalogs, and a full 2012
SQL dump of the database — survive only as Internet Archive Wayback Machine captures.
In July 2026 we enumerated and recovered **all 345 uniquely archived data files**
(xls/xlsx/doc/docx/zip; the CDX index lists 346 capture URLs, one a host:port alias
of another — the raw CDX response is preserved alongside the manifest in the source
repository as `CDX_RESPONSE.txt`).

This deposit is the **recovery record**: it establishes what was recovered, from
which snapshots, with what checksums, and how the recovery can be reproduced and
validated. It deliberately does **not** republish the recovered files themselves —
those are the intellectual work of the Harvard Khipu Database Project and are being
offered to the Open Khipu Repository (OKR) maintainers through their own channel.
The SHA-256 manifest here allows any future holder of the files to verify content
identity against this record.

## Contents

| File | Description |
|---|---|
| `MANIFEST.csv` | One row per recovered file (357 rows: 345 unique Wayback recoveries + 6 convenience duplicates + 6 Khipu Field Guide exports, each labeled by source): path, source, original URL, Wayback snapshot timestamp, size in bytes, SHA-256 |
| `recover_kdb_wayback.py` | The recovery tool (Python, MIT license): enumerates the archive via the Wayback CDX API, downloads the latest capture of each file with content-type verification via magic bytes, and regenerates the manifest. Idempotent |
| `07_kdb_corpus_findings.md` | Validation record for the 274 Brezine-format sheets (2004–05 vintage): parsed with zero errors (26,108 cord rows) and cross-validated against the OKR (274/274 khipus matched via alias-aware resolution of the OKR's compound designations; level-1 cord counts 241/274 exact) |
| `10_field_sheet_findings.md` | Validation record for the 66 raw field-recording sheets (later vintage): 6,686 cord rows, zero parse errors; 66/66 khipus aligned to the OKR with total cord counts matching 66/66 and per-cord value agreement of 99.99% (6,685 linked cords, one disagreement) |

## Why the recovered archive matters

- **The sheets carry hand-curated per-cord computed values and attachment codes** for
  340 khipus, at a fidelity the modern OKR extraction does not uniformly preserve for
  the 2004–05 vintage (validation details in the findings documents).
- **The 2012 SQL dump (snapshot 2015-09-10 of a 2012-01-22 export) preserves material
  the modern OKR does not hold**: **14 dropped recordings (2,323 cords)** —
  independent assessments of khipus the OKR merged under compound designations
  (`AS070/UR035`, `AS068/UR281`, …), where the OKR kept the other recording — one
  khipu for which the OKR holds no data (AB001: catalogued by the OKR as KH0701
  since 2025-12-19, but with no cord records in the database — the recovered 2012
  recording, 156 cords, is to our knowledge the only digitized data for it), and Gary Urton's per-khipu
  classification table (`URTON_KHIPU_TYPE`, 356 rows) with his archive groupings,
  which has no OKR counterpart. Thompson (2025) demonstrates on KH0083 — whose
  dropped AS070 assessment (590 cords) is among the fourteen — precisely why
  alternate assessments of a single khipu are scientifically valuable.
- The sheets are the **primary field documents** behind the corresponding OKR records
  (e.g., UR281's sheet underlies OKR KH0081), at a fidelity the OKR extraction does
  not uniformly preserve for the 2004–05 vintage.
- The material includes original recording sheets for the six Santa Valley khipus
  (UR087–UR092) analyzed by Medrano & Urton (2018) and FitzPatrick (2024), and for
  khipu AS070/UR035 (KH0083), one of the two khipus connected numerically by
  Thompson (2025) — whose alternate 2012 assessment is among those preserved.

## Rights

- The recovered files (not included here) are the intellectual work of the Harvard
  Khipu Database Project; this record documents their recovery from public web
  archives for research and preservation.
- The contents of this deposit (manifest, tooling, validation documents) are by the
  authors: `recover_kdb_wayback.py` under the MIT license; all other files under
  CC BY 4.0.

## How to verify

1. Obtain the recovered files (from the OKR maintainers, or by re-running
   `recover_kdb_wayback.py`, which re-downloads from the Wayback Machine — latest
   capture per file; this manifest records the snapshots used here).
2. Compute SHA-256 per file and compare against `MANIFEST.csv`.

## Authorship note

This deposit is a sustained human–AI collaboration and is credited accordingly:
E. Sánchez directed the work and takes responsibility for the content; Claude
(Fable 5, an AI system by Anthropic) contributed design, implementation, and
documentation. The co-author listing reflects that substantive contribution and the
project's standing credit policy, and is not a claim of legal authorship.

## References

- Medrano, M., & Urton, G. (2018). Toward the Decipherment of a Set of Mid-Colonial
  Khipus from the Santa Valley, Coastal Peru. *Ethnohistory*, 65(1), 1–23.
- FitzPatrick, M. (2024). New Insights on Cord Attachment and Social Hierarchy in Six
  Khipus from the Santa Valley, Peru. *Ethnohistory*, 71(4), 443–469.
- Thompson, K. M. (2025). A Numerical Connection Between Two Khipus. *Ñawpa Pacha*,
  45(1), 83–104. (Published online November 2024.)
- Urton, G., & Brezine, C. J. (2005). Khipu Accounting in Ancient Peru. *Science*,
  309(5737), 1065–1067.
- Open Khipu Repository: https://github.com/khipulab/open-khipu-repository
