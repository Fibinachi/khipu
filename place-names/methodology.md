# Methodology: Colonial Place-Name Gazetteer for Khipu Identity Matching

## Purpose
Build a reference gazetteer of Inca place names (wamani/provinces organized by suyu) to cross-reference against the geographic distribution of distinguishing-tier khipu colors. If colors encode place identities, tightly-clustered colors should map to specific wamani.

## Sources used

### Primary (colonial)
- **González Holguín (1608), *Vocabulario*** — consulted via the quechua-roots project; place names extracted where present. (Full toponymic extraction from Holguín not yet complete — flagged as future work.)
- **Guaman Poma (1615), *Nueva corónica*** — geographic descriptions referenced for provincial organization. Full place-name extraction not attempted (1,200-page manuscript; beyond current scope).
- **Cieza de León, *Crónica del Perú*** — route descriptions with settlement names. Referenced for major waypoints, not systematically extracted.

### Secondary (modern synthesis)
- **Wikipedia suyu articles** (Chinchay Suyu, Kunti Suyu, Kollasuyo, Government of the Inca Empire) — wamani province lists. These compile colonial sources (D'Altroy 2005, Steward & Faron 1959). Used as the backbone of the gazetteer.
- **Medrano & Urton (2018)** — Santa Valley khipu-census match; place context (Santa River Valley, Recuay, San Pedro de Corongo).
- **Urton & Chu (2015)** — Inkawasi commodity associations (beans/chili/peanuts by khipu ID); used to check color→commodity vs color→place.

### Database
- **OKR (okr-khipu.db)** — color→site mapping from `ascher_cord_color` joined to `khipu_main.PROVENANCE`. 447/619 khipu (72%) have provenance data.

## Key limitations

### 1. Provenance bottleneck (severe)
- 28% of khipu have no usable provenance (blank, "Unknown," or "unknown").
- Provenance = find-spot, not origin. Museum-held khipu (especially US/European collections) often lack any geographic data.
- The five all-U quipu (1000029, 1000034, 1000345, 1000361, 1000368): zero provenance in OKR or Ascher databooks.
- **Result:** 0 of 66 colors have complete geographic data. The best (NB) has 4 sites; most have 10+ sites or heavy "unknown" components.

### 2. Warehouse problem
Incahuasi, Pachacamac, and other storage/administrative sites contain khipu recording goods/people FROM elsewhere. A color concentrated at a warehouse likely encodes ORIGIN, not the warehouse location. This inverts the naive reading: NB at Incahuasi ≠ "NB means Incahuasi."

There is no database field distinguishing "khipu found where used" from "khipu found where archived." Archaeological context (excavated vs collected) is inconsistently recorded.

### 3. Commodity/place ambiguity
Urton & Chu's Inkawasi work shows colors may encode COMMODITIES (beans, chili, peanuts), not places. NB is prominent in peanut khipu; GG in bean khipu. Every "tight cluster" has a competing commodity reading that cannot be ruled out on geographic data alone.

The color-layers analysis (three-tier model) suggests B, YB, GG, HB, BG are "major commodities" — if correct, these are not place candidates at all.

### 4. Colonial source gaps
- Full toponymic extraction from Holguín, Guaman Poma, and Cieza not yet done. The gazetteer uses modern-compiled wamani lists, not primary colonial place-name extraction.
- Wamani boundaries are approximate; some wamani names are ethnonyms (Chanca, Chimu) not toponyms.
- Post-conquest administrative reorganization may have renamed or merged Inca provinces.

### 5. Temporal mismatch
Khipu are Inca-period (pre-1532). The best place-name sources are colonial (post-1532). Some Inca place names were lost; some colonial names are Spanish impositions. The 1560/1608 dictionaries help but are not gazetteers.

## What would strengthen this

1. **Archaeological context coding:** Distinguish excavated (known context) from collected (unknown context) khipu in the database. Excavated khipu anchor geography; collected khipu float.
2. **Full Holguín toponym extraction:** Systematic place-name harvest from the 1608 *Vocabulario* and 1607 *Arte*.
3. **Guaman Poma place-name index:** The manuscript contains hundreds of toponyms with approximate locations.
4. **Commodity disambiguation:** For each tightly-clustered color, test commodity vs place by checking whether the color appears on khipu with known commodity associations (Urton & Chu method extended).
5. **Provenance research:** Archival work on museum acquisition records for the 28% without provenance, especially the all-U quipu.

## Honest assessment

The gazetteer is built. The color geography is mapped. The alignment produces candidates but no conclusions. The provenance bottleneck is the binding constraint — we cannot do place-name decipherment without knowing where khipu (and the things they record) came from. This is an archival problem, not a computational one.
