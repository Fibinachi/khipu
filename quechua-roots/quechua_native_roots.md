# Pre-Contact Quechua Native Root Lexicon

**Purpose:** Reference vocabulary for future khipu sign definitions. Khipu are pre-contact artifacts; they cannot encode Spanish loanwords. This lexicon strips borrowings and keeps the native inherited root stock, with earliest attestation as the confidence signal.

**Built:** 2026-10-11
**Companion file:** `quechua_native_roots.csv` (2,827 entries)

---

## Methodology

### Sources (in priority order)

1. **Santo Tomás, *Lexicon, o Vocabulario de la lengua general del Peru* (1560)** — earliest Quechua vocabulary, within living memory of first contact. Spanish→Quechua. Digitized from archive.org (`lexiconovocabula00domi`).
2. **González Holguín, *Vocabulario de la lengua general* (1608)** — "corregido y renovado conforme a la propriedad cortesana del Cuzco." The court Quechua of Cuzco. Two books: Libro Primero (Quechua→Spanish, ~12,700 parsed entries), Libro Segundo (Spanish→Quechua). Digitized from archive.org (`vocabulariodelal01gonz`).
3. **Wiktionary Quechua lemmas** — 2,254 modern lemmas pulled via API with POS, gloss, and etymology. Used as the clean base lexicon; colonial sources provide attestation dating.

### Loanword identification

Spanish loans were removed using three independent signals:

1. **Wiktionary etymology flags** — entries categorized as "borrowed from Spanish" or with Spanish etymologies (69 directly flagged).
2. **Phonological rules** — Quechua native phonology lacks:
   - /f/ (never native)
   - Word-initial /b/, /d/, /g/, /r/
   - Spanish consonant clusters (br, cr, dr, gr, pr, tr, bl, cl, gl, pl)
   - Non-native geminates (bb, dd, gg, ff, vv)
3. **Santo Tomás's own testimony** (1560, prologue): *"carecen los Indios de todos los vocablos de las cosas que no tenian ni se usavan en aquellas tierras"* — the Indians lack all words for things they didn't have or use in those lands. Post-contact introductions (horse, cow, wheat, iron, church) are loans by definition.

**Removed:** 110 loanwords from the Wiktionary set.

### Attestation dating

Each root carries its earliest attestation:
- **1560** — found in Santo Tomás (203 roots). Highest confidence: pre-contact vocabulary.
- **1608** — found in Holguín but not Santo Tomás (945 roots). High confidence: colonial Cuzco court Quechua.
- **modern** — Wiktionary only (1,679 roots). Probably native (passed phonological filter) but unattested in colonial sources.

### Colonial-only roots

683 roots appear in Holguín (1608) but have no modern Wiktionary equivalent. These are potentially **lost vocabulary** — words that died out between 1608 and the present. They are the most khipu-relevant subset after the 1560-attested roots, because they represent the Inca-period lexicon directly.

**Caveat:** Colonial OCR is noisy. Holguín-only entries were filtered aggressively (single word, 4–20 chars, Quechua phonotactics, coherent Spanish gloss) but some OCR artifacts may remain. Confidence is marked `certain_native` based on 1608 attestation, but individual entries should be verified against the original before citation.

---

## Coverage statistics

| Category | Count |
|---|---|
| Total native roots | 2,827 |
| Attested 1560 (Santo Tomás) | 203 |
| Attested 1608 (Holguín) | 945 |
| Modern only | 1,679 |
| Colonial-attested (1560+1608) | 1,148 |
| Holguín-only (lost vocabulary) | 683 |
| Spanish loans removed | 110 |

### By semantic domain

| Domain | Count | Khipu relevance |
|---|---|---|
| other (unclassified) | 1,713 | — |
| actions (verbs) | 261 | Medium — but khipu may lack verbs |
| numbers | 176 | High — quantitative vocabulary |
| body | 166 | Low |
| kinship | 149 | Medium — social organization |
| natural_world | 93 | Medium — place/entity names |
| time | 48 | Medium — chronological marking |
| agriculture | 47 | High — tribute commodities |
| space/direction | 44 | Medium — spatial organization |
| animals | 35 | High — tribute goods (camelids) |
| colors | 26 | High — color-noun mapping |
| materials | 14 | Medium — goods classification |
| social_organization | 12 | High — ayllu, curaca, mita |
| warfare | 11 | Low |
| food | 11 | Medium — stored goods |
| textiles | 10 | Medium — tribute goods |
| religion | 6 | Low-Medium |
| administration | 5 | **Highest** — but underrepresented |

**Note on "administration":** Only 5 roots classified here, which reflects the keyword-based classification, not the actual administrative vocabulary. Many administrative terms (tribute goods, counting, storing) are classified under agriculture, animals, numbers, or materials. A manual review of the 1560/1608-attested roots for administrative relevance is recommended future work.

**Note on "other":** 1,713 roots (61%) could not be domain-classified from their glosses via keyword matching. This is a limitation of automated classification, not of the lexicon. The glosses are present in the CSV for manual review.

---

## The administrative-vocabulary subset

For khipu work, the highest-priority roots are those attested in 1560/1608 in these domains:
- **Numbers and counting** (176 roots) — the quantitative core
- **Agriculture and animals** (82 roots combined) — tribute commodities
- **Social organization** (12 roots) — ayllu, curaca, mita structures
- **Colors** (26 roots) — potential color-noun correspondences
- **Storage and materials** (19 roots combined) — warehouse vocabulary

Filter the CSV with: `earliest_attestation IN (1560, 1608)` AND `semantic_domain IN ('numbers','agriculture','animals','social_organization','colors','materials','administration')`.

---

## Limitations

1. **OCR noise in colonial sources.** 17th-century Spanish typography (long s, ligatures) degrades OCR. Attestation matching used fuzzy normalization, but false negatives are likely (a root may be in Holguín but not matched due to OCR errors). False positives are less likely (matching requires the normalized form to appear).

2. **Wiktionary coverage.** 2,254 lemmas is a fraction of the full Quechua lexicon. Many common words may be missing. The lexicon is a reference sample, not a complete dictionary.

3. **Dialect.** The colonial sources document Cuzco/Collao (Southern Quechua II-C). Ancash, Huancayo, and other varieties are not represented in the attestation dating. Wiktionary lemmas may reflect mixed dialects; `dialect_notes` is populated only where the source specifies.

4. **No definitions matched to khipu.** This lexicon is the *target vocabulary* for future definition work. No claim is made that any specific khipu sign corresponds to any specific root. That matching is a separate research phase.

5. **Semantic domains are approximate.** Automated keyword classification from Spanish/English glosses. Manual review recommended for the administrative subset.

---

## Sources cited

- Santo Tomás, Domingo de. *Lexicon, o Vocabulario de la lengua general del Peru.* Valladolid, 1560. Digitized: archive.org, `lexiconovocabula00domi`.
- Santo Tomás, Domingo de. *Grammatica, o Arte de la lengua general de los Indios de los Reynos del Peru.* Valladolid, 1560. Digitized: archive.org, `grammaticaoarted00domi`.
- González Holguín, Diego. *Vocabulario de la lengua general de todo el Peru llamada lengua Qquichua, o del Inca.* Lima, 1608. Digitized: archive.org, `vocabulariodelal01gonz`.
- González Holguín, Diego. *Gramatica y arte nueva de la lengua general de todo el Peru.* Lima, 1607 (1842 reprint digitized: archive.org, `gramticayartenue00gonz`).
- Wiktionary, Category:Quechua_lemmas (2,254 entries, accessed 2026-10-11 via API).
