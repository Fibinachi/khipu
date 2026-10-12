# Khipu Document Reclassification Report
**Date:** 2026-10-10
**Scope:** 593 non-funerary khipu (26 Leymebamba/burial excluded)
**Output:** `reclassification-2026-10-10.csv`

## Method

### 1. Number decoder (new, type-aware)
Built from Ascher & Ascher / Urton conventions, accounting for knot type:
- **Units** (nearest free end = largest START_POS): L/SP/LL/BL → NUM_TURNS (2–9); E/EE → 1; empty → 0
- **Tens/hundreds/thousands**: count of S knots = digit; empty → 0
- Returns confidence: 'high' only for fully standard encodings

**Validation:** Santa quipu position-1 cords decode to published constants (1000270→9, 1000271→4). All high confidence.

**Critical data limitation found:** 100% of L knots on Inkawasi quipu (1,486) have NULL NUM_TURNS. Units digits unrecoverable from database. Published Urton-Chu values were read from physical quipu, not OKR. Across corpus: 391/593 (66%) full turn data, 61 partial, 92 none, 49 no L knots.

### 2. Cord ordering
Verified: CORD_ORDINAL (not CORD_ID) for physical order. START_POS descending = top-to-bottom along pendant. PENDANT_FROM is set on ALL cords including level-1 (points to main cord); CORD_LEVEL is the reliable hierarchy indicator.

### 3. Classification
Anchors: Santa (census, 6 quipu), Inkawasi (warehouse, 18 quipu).
Features per quipu: decode rate, value distributions, color group regularity, hierarchy depth, subsidiary rate, provenance.

**Rules:**
- `census`: Santa anchor (high confidence)
- `census-like`: 3+ census signals (fixed color groups, >70% values <20, shallow ≤2 levels, 15-60% zeros), ≤1 warehouse signal → medium
- `warehouse`: Inkawasi anchor (high confidence)
- `warehouse-like`: 3+ warehouse signals (deep ≥3 levels, values >1000, >20% subsidiary rate, Inkawasi provenance), ≤1 census signal → medium
- `unclassified`: mixed signals, weak signals, or no diagnostic features

## Results

| Type | Count | Confidence |
|------|------:|-----------|
| census | 6 | high (anchors) |
| census-like | 205 | medium |
| warehouse | 18 | high (anchors) |
| warehouse-like | 14 | medium |
| unclassified | 350 | 7 high / 75 medium / 268 low |

**Key finding:** 59% unclassified. This is honest — the classifier does not force quipu into categories. Many have mixed signals (e.g., census-like color groups but warehouse-like large values) suggesting either hybrid documents or undescribed types.

**Census-like geographic spread:** 159 unknown provenance, 16 Puruchuco, 11 South Coast, 11 Central Coast, 5 Nazca. Not concentrated in one region — the census format may have been widespread.

## Limitations
1. Inkawasi units digits unrecoverable (NULL turns) — warehouse classification relies on structure, not full values
2. 205 census-like at medium confidence may include false positives; thresholds were set to be inclusive
3. Color regularity detection limited to first 300 cords
4. 7 quipu have no cord/knot records at all
5. 19 quipu have cords but no knots

## Files
- Decoder: `decoder.py`
- Classifier: `classify.py`
- Results: `reclassification-2026-10-10.csv`
- Prior (discarded): `quipu-document-categories.csv`
