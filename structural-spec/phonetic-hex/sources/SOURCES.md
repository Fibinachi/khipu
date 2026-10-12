# Sources for Phonetic-Hex Project

## Target sources (attempted)

### Huarochiri Manuscript (c. 1608)
- **Status**: NOT ACQUIRED. Full Quechua text not freely available digitally.
- The Salomon/Urioste 1991 edition (University of Texas Press) is under
  copyright. The archive.org copy ("Mitos de Huarochiri") is a modern
  Spanish academic article about the manuscript, not the Quechua text.
- **Impact**: The single best source of natural colonial Quechua prose
  remains inaccessible for computational analysis.

### Guaman Poma, Nueva coronica y buen gobierno (1615)
- **Status**: PARTIALLY SURVEYED. Digital transcription available at
  poma.kb.dk (Royal Library of Denmark), but the text is primarily
  colonial Spanish with Quechua words/phrases interspersed.
- Extracting running Quechua text would require manual annotation of
  1,189 pages. Not feasible for this task.
- The kb.dk Quechua glossary-index was noted but not extracted (word
  list, not running text).

### Ollantay (colonial Quechua drama)
- **Status**: ATTEMPTED, INSUFFICIENT. The 1880 Pacheco Zegarra edition
  was downloaded from archive.org (ID: ollntaydramaenve00unse, 210KB).
- The Quechua verses are buried in Spanish/French commentary with noisy
  19th-century OCR. Automated extraction yielded only proper nouns.
- Saved as: /tmp/phx/ollantay_djvu.txt (not copied to sources/ due to
  low utility).

## Actual sources used

### 1. Morpheme inventory (216 items)
- `../isomorphism/quechua_morphemes.csv`
- Compiled from Faller 2002 (evidentiality), Cusihuaman (case/tense),
  Mannheim 1998. Verified linguistic sources.

### 2. Native roots (2,827 items)
- `../quechua-roots/quechua_native_roots.csv`
- Roots with earliest attestation 1560/1608/modern. Spanish loans removed.

### 3. Attested phrases (23 items, 114 morpheme tokens)
- `../isomorphism/quechua_phrases.csv` (origin=attested)
- Morpheme-segmented natural Quechua phrases from grammar examples.

### 4. Holguin-extracted tokens (425 items)
- `holguin_extracted_quechua_tokens.csv` (in this directory)
- Extracted from Gonzalez Holguin 1607 grammar (OCR text in
  ../quechua-roots/holguin_gramatica.txt) via longest-match morpheme
  segmentation. Each token segments into 2+ known morphemes/roots.

### 5. Template phrases (1,388 items, 5,217 tokens) -- FLAGGED
- `../isomorphism/quechua_phrases.csv` (origin=template)
- Grammatically valid Quechua generated from templates. Phoneme
  sequences are valid; frequency distributions are generator-controlled.
  Used for phonotactic analysis with explicit caveats.

## Recommendation

The Huarochiri Quechua text remains the highest-value unacquired resource
for this research program. If a digitized version becomes available
(e.g., through a library partnership or a published open-access edition),
it should replace Corpus D as the natural-language phonetic baseline.
