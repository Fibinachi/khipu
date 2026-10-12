# Ecological Zone Validation: Corpus-Wide Test

**Date:** 2026-10-10
**Task:** Validate the ecological color model against all quipu with known provenience.

---

## Datasets

| Dataset | Provenienced quipu | Highland | Coastal |
|---------|-------------------|----------|---------|
| Harvard KDB 2012 | 85 | 22 | 63 |
| Open Khipu Repository | 388 | 25 | 363 |

Highland = Leymebamba, Cuzco, Huari, Mollepampa (>2000m).
Coastal = all Peruvian/Chilean coastal valley sites.

---

## Key Finding: True Blue (BL) Is the Signal

| Color | KDB: Highland | KDB: Coastal | OKR: Highland | OKR: Coastal |
|-------|--------------|--------------|---------------|--------------|
| **BL** (pale blue) | 45.5% | **0.0%** | 40.0% | **3.6%** |
| **GG** (grayish green) | 63.6% | 9.5% | 60.0% | 29.5% |
| **KB** (dark brown) | 81.8% | 15.9% | — | — |
| **BG** (blue-gray) | 13.6% | 1.6% | 12.0% | 13.5% |

**BL is the cleanest ecological marker.** In the KDB, zero coastal quipu have true blue — perfect exclusion. In the broader OKR, only 3.6% of coastal quipu have BL (96.4% specificity).

**BG (blue-gray) is NOT ecological.** It appears at equal rates in both zones (12-13.5% in OKR). The original "blue family" finding was contaminated by BG. The signal is specifically BL.

**GG is moderately ecological** but common enough on the coast (29.5% in OKR) that it cannot serve as a zone classifier alone.

---

## Classifier Accuracy

**BL-only predictor** (BL present → highland):

| Dataset | Accuracy | Highland recall | Coastal specificity |
|---------|----------|-----------------|---------------------|
| KDB 2012 | 85.9% | 45.5% | 100.0% |
| OKR | 92.8% | 40.0% | 96.4% |

BL is a high-specificity, moderate-sensitivity marker. Its absence does not prove coastal (60% of highland quipu lack BL), but its presence strongly predicts highland-or-imperial context.

---

## The Coastal BL Anomalies: Institutional, Not Geographic

13 coastal quipu in the OKR have true blue. They are not random:

| Site | BL quipu | Site character |
|------|----------|----------------|
| Pachacamac | 3/89 | Empire's premier religious center |
| Incahuasi | 3/52 | Imperial state storehouse |
| Armatambo | 2/13 | Major Lima-valley administrative center |
| Nazca | 2/13 | Regional center |
| Huacho, Santa, others | 1 each | Various |

**Pattern:** Coastal BL appears at major administrative, religious, or imperial sites — not at small villages or cemeteries. This supports the refined hypothesis: **BL marks highland origin OR imperial/state context**, not geography alone.

The KDB's perfect 0% coastal BL rate was an artifact of its narrower site coverage (fewer major centers). The OKR's broader data reveals the institutional dimension.

---

## Highland Anomalies (No Blue/Green)

5 of 25 highland quipu lack both blue and green:

- 4 from Leymebamba (colors: W only; MB+W; AB+MB+W; AB+KB+MB+W)
- 1 from Huari (AB+B)

These use only white and brown — the default palette. Possible explanations: different recorder, different accounting purpose (census vs. commodity), or simply quipu that did not need color differentiation.

---

## Refined Model

The original claim — "blue is absent from coastal quipu" — was overstated. The refined model:

1. **BL (true blue) is strongly highland-associated** (96-100% coastal specificity) but also appears at coastal imperial/administrative centers.
2. **BG (blue-gray) is zone-neutral** and should not be grouped with BL.
3. **GG (grayish green) is moderately highland-associated** but too common on the coast for clean classification.
4. **The ecological signal is real but mediated by institutional context.** Highland sites use BL; coastal *villages* avoid it; coastal *state centers* use it.

This is consistent with the broader finding: quipu colors encode ecological origin AND administrative context, not geography alone.

---

## Limitations

1. **n=25 highland quipu** across both datasets (22 Leymebamba + 3 others). The highland sample remains thin.
2. **Provenience quality varies.** Some entries are precise ("Leymebamba"); others are vague ("Peru," excluded) or dealer attributions.
3. **No elevation data** for most sites — zone assignment is by known site location, not measured altitude.
4. **Temporal mixing.** The datasets span Inca and early colonial periods; color conventions may have shifted.

---

## Bottom Line

The ecological color model **holds corpus-wide** with an important refinement: it is specifically **true blue (BL)**, not the broader blue family, that marks highland origin. The model achieves 86-93% accuracy as a zone classifier. Coastal exceptions cluster at imperial/administrative centers, supporting the institutional-context refinement over pure geography.
