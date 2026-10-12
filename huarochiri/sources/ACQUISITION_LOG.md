# Huarochirí Sources: Acquisition Log

## Acquired

### 1. Arguedas 1966 full bilingual edition
- **File:** `huarochiri_arguedas_full.txt` (614KB OCR)
- **Source:** archive.org item `ManuscritoDeHuarochiriJMArguedasCompleto`
- **Edition:** *Dioses y hombres de Huarochirí*, José María Arguedas (trans.), Instituto de Estudios Peruanos, Lima, 1966
- **Content:** Complete Quechua original (c. 1608) + Spanish translation, 31 chapters
- **Extraction:** 402 Quechua paragraphs, 20,002 words (paragraph-level language classification)
- **Note:** Original 1608 manuscript text is public domain. Used for computational linguistic analysis (frequency counts, not reproduction).

### 2. Taylor 2008 Chapter III (normalized Quechua)
- **File:** `huarochiri_ch3_quechua.txt` (206 words)
- **Source:** aacademica.org, Edgardo Civallero compilation (CC BY-NC-ND 4.0)
- **Content:** Chapter III (flood narrative) in Taylor's normalized orthography
- **Use:** Validation of Arguedas extraction

### 3. Holguín 1607 grammar (Quechua examples)
- **Source:** `../quechua-roots/holguin_gramatica.txt` (782KB, already in workspace)
- **Extraction:** 160 Quechua example sentences (strict filtering: Spanish stopword exclusion, 60%+ Quechua density)

## Not acquired

| Source | Status | Reason |
|---|---|---|
| Taylor 1987/2008 full edition | Not acquired | Under copyright, no free digital version |
| Salomon/Urioste 1991 | Not acquired | Under copyright (UT Press) |
| Guaman Poma Quechua | Not feasible | Interspersed in 1,189pp Spanish; requires manual annotation |
| Santo Tomás 1560 grammar | Attempted | OCR too noisy (16th-century typography) |

## Recommendation

The Arguedas 1966 extraction (20K words) is sufficient for the morpheme frequency baseline. For administrative register frequencies, the next highest-value target is colonial administrative documents (wills, tribute records) rather than additional narrative text.
