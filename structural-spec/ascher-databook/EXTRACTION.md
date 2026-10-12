# Ascher Databook Extraction Report

Source: Ascher & Ascher, *Code of the Quipu: Databook* (1978) and *Databook II* (1988),
digitized at https://courses.cit.cornell.edu/quipu/

Method: 206 PDFs downloaded, OCR'd with Tesseract 5.3.4 (PSM 6, 200 DPI),
parsed into structured records. See `~/workspace/ascher-work/` for pipeline scripts.

## Priority entries: the five all-U quipu

| OKR ID | Ascher | Holder | Provenance finding |
|--------|--------|--------|-------------------|
| 1000029 | AS207A | Museum of Science, Buffalo (C14459) | **No provenance.** Part of a 3-quipu set (AS207A/B/C) tied to one main cord. |
| 1000030 | AS207B | Museum of Science, Buffalo (C14459) | **No provenance.** Smaller quipu tied to AS207A's main cord. |
| 1000031 | AS207C | Museum of Science, Buffalo (C14459) | **No provenance.** Smaller quipu tied to AS207A's main cord. |
| 1000034 | AS212 | Joslyn Art Museum, Omaha (No. 1958-57) | **No provenance.** Museum acquisition only. |
| 1000345 | AS44 | Museo Nacional, Lima (No. 17/579) | **No provenance.** Museum catalog number only. |
| 1000361 | AS50 | Private: Ana Maria Soldi, Lima | **No provenance.** Private collection, Lima. |
| 1000368 | AS71 | Private: Percy Dauelsberg, Arica, Chile | **EXCAVATED by Percy Dauelsberg in 1965.** Northern Chile (Arica region). |

### Key finding: AS71 provenance

The databook observations for AS71 state: "AS69, AS70, and AS71 were excavated
by their owner, Percy Dauelsberg, in 1965."

This is the only one of the five all-U quipu with archaeological provenance.
Dauelsberg was based in Arica, northern Chile. The excavation was in 1965,
placing these quipu in the far southern Andes — Qullasuyu, the Inca Empire's
southern quarter.

**Implication for the dialect hypothesis:** If the all-U twist pattern reflects
a regional scribal tradition, northern Chile / the south coast is the candidate
region. However, the other four all-U quipu have no provenance, so this remains
a single data point, not a cluster.

### Key finding: AS207 is three quipu

The databook entry AS207 contains THREE physically associated quipu:
- **AS207A** (OKR 1000029): the main quipu, 193 cords, all-U twist
- **AS207B** (OKR 1000030): smaller quipu tied to AS207A's main cord, 21 cords
- **AS207C** (OKR 1000031): smaller quipu tied to AS207A's main cord, 14 cords

The databook notes: "Between Groups 9 and 10, there are 2 smaller quipus tied
to the main cord. We hypothesize that this was preplanned as there is space on
the main cord between these 2 groups but not between other adjacent groups."

OKR cataloged these as three separate records. The databook treats them as one
entry with sub-components.

**Twist direction check (from OKR):** All three are 100% U-direction:
- 1000029: 242 U, 0 S, 0 Z
- 1000030: 35 U, 0 S, 0 Z
- 1000031: 18 U, 0 S, 0 Z

The entire physically-associated complex uses U-twist exclusively. This
strengthens the case that all-U is a deliberate scribal convention, not a
one-off anomaly — three separate quipu, tied together, all by the same hand
or school using the same twist norm.

## Extraction statistics

**Status as of 2026-10-11 ~21:30 EDT:** 58 of 206 PDFs processed (28%).
Full OCR running in background with 2 workers; estimated completion ~2 hours.

Current totals:
- Khipu records parsed: 58
- Cord-level records: 4,503
- Structural observations: 188
- Holder types: 54 museum, 2 private, 2 unknown
- Records with excavation history: 1 (AS71 only)
- Records with explicit provenance field: 0 (the Aschers embed provenance in museum ID + observations, not a separate field)

**Geographic distribution of holders (current sample):**
Heavily European/American museums — the Aschers worked from museum collections,
not field excavations. Top holders include Museum für Völkerkunde (Berlin),
Niedersächsische Landesmuseum (Hanover), and various US museums.
Full distribution pending complete run.

[To be updated after full OCR run]
- Total PDFs: 206 (AS10–AS215)
- Total quipu records parsed: [pending]
- Records with provenance info: [pending]

## Provenance summary

[To be completed after full OCR run]

## Contradictions / additions vs OKR

[To be completed after full OCR run]

### Known so far:
- AS207A/B/C: OKR has 3 separate records; databook has 1 entry with 3 components.
  Cross-reference is maintained in `okr_id` field (semicolon-separated).
- AS207A's OKR ID 1000029 was identified as "all-U" in the twist analysis.
  AS207B and AS207C should be checked for twist direction.

## Ascher notation system

See `~/workspace/ascher-work/NOTATION.md` for the full reverse-engineered
notation guide, including:
- Cord identifiers (pendant, subsidiary, top cord)
- Knot notation (s/L/E types, position measurements)
- Color abbreviations and compound codes
- Value column (Aschers' computed decimal readings)
- Length units (¢ = pendant, b = broken)
- Observation formats

## Files

- `ascher_provenance.json` — full structured records (one per quipu)
- `ascher_khipu.csv` — khipu-level metadata with OKR cross-reference
- `ascher_cords.csv` — cord-by-cord data (knots, length, color, Ascher value)
- `ascher_observations.csv` — structural/arithmetic observations

## Limitations

- OCR errors: systematic misreads (e.g. "2s1" as "2sl", "1" as "l") are
  partially corrected but some remain. Cord-level data should be spot-checked
  against the PDFs for critical entries.
- The Aschers' "Value" column reflects their decimal interpretation, which
  may differ from the corrected decoder for edge cases (long-knot turns, etc.).
- Provenance is sparse: most entries list only museum/owner, not archaeological
  origin. The Aschers worked primarily from museum collections.
- Color abbreviations (B, LB, MB, DB, W, YB, etc.) do not directly map to OKR
  color codes. A mapping table is needed.
