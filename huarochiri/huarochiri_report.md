# Huarochirí Linguistic Analysis: Final Report

## What was acquired

**Full Huarochirí Manuscript Quechua text** from the Arguedas 1966 bilingual edition (*Dioses y hombres de Huarochirí*), via archive.org OCR.

- 402 Quechua paragraphs extracted (paragraph-level language classification)
- 20,002 Quechua words
- 3,595 grammatical morpheme tokens across 29 types
- 7,417 root tokens across 327 types

This replaces the rule-generated templates (which produced artificially flat distributions) with natural colonial Quechua prose from c. 1608.

### Also acquired
- Huarochirí Chapter III in Taylor's normalized orthography (206 words, from aacademica.org) — used for validation
- 160 Holguín grammar Quechua example sentences (filtered from 782KB grammar text)

### What was NOT acquired
- Taylor's full edition (1987/2008): under copyright, not freely available
- Salomon/Urioste 1991 edition: under copyright
- Guaman Poma Quechua: interspersed across 1,189 pages of Spanish, not extractable automatically

## Data quality

**Strengths:**
- 20K words is sufficient for stable frequency rankings of the top 20 morphemes
- Arguedas 1966 is a respected scholarly edition
- The Quechua is natural narrative prose, not grammar examples

**Limitations:**
- OCR noise: the 1966 edition was scanned; character recognition errors affect ~5-10% of words
- Arguedas orthography differs from modern: normalized via rule-based mapping (c/qu→k, hu→w, etc.)
- Single genre: mythological narrative. This inflates -si (reportative), quotatives, and demonstratives
- "chaymanta" (187×) was captured as a root rather than chay+manta — a segmentation gap
- "cwri" (91×) is likely an OCR artifact

**Segmentation method:** Root-first longest-match using 2,827 native roots + 216 grammatical morphemes. Unknown morpheme rate not separately tracked in final run; manual spot-checks suggest ~85-90% of tokens segment cleanly.

## Key findings

### 1. The "E" is -ta (accusative), at 22.8%

The accusative case marker dominates Huarochirí Quechua. Nearly 1 in 4 grammatical morphemes is -ta. This is the single most frequent grammatical operation in the language.

**Hangman implication:** The most frequent khipu byte pattern (W:0, 4,786 tokens) should correspond to the most frequent grammatical function. If khipu encodes Quechua grammar, W:0 is the best candidate for accusative/case-role marking.

### 2. Evidentiality is pervasive (18.2%)

-si (reportative) + -mi (direct) + -cha (conjectural) = 653/3,595 tokens. Nearly 1 in 5 morphemes marks information source. This is independent confirmation that evidentiality is central to Quechua grammar — supporting the khipu evidentiality-marking hypothesis.

**Caveat:** -si is inflated by the narrative genre. In administrative text, -mi would dominate.

### 3. The case system maps to the color tier

Six Quechua cases in the top 20 morphemes: -ta, -pi, -pa, -man, -manta, -wan. The khipu grammatical tier has four main colors (W, AB, MB, KB). The Hangman table proposes initial alignments, but the mapping is not 1:1 (6 cases vs 4 colors). Possible resolutions: some cases share a color, or some cases are marked by knot type rather than color.

### 4. Register mismatch is real and quantified

| Feature | Huarochirí (narrative) | Predicted admin |
|---|---|---|
| Top evidential | -si (439) | -mi |
| Top roots | chay, kay, ñispa | numbers, titles |
| Quotatives | high (429) | low |
| Case markers | high | higher |

The Huarochirí gives us the **morpheme inventory** and **structural patterns**. It does NOT give us administrative **frequency rankings**. Those must come from Holguín's administrative examples or colonial bureaucratic documents.

## Deliverables

| File | Description |
|---|---|
| `sources/` | Arguedas 1966 full text, Taylor Ch.III, extraction log |
| `morpheme_frequencies.csv` | 29 morphemes ranked by frequency |
| `root_frequencies.csv` | Top 100 roots by frequency |
| `morpheme_bigrams.csv` | Top 60 morpheme bigrams |
| `hangman_table.csv` | 29-rank Quechua-to-khipu alignment with hypotheses |
| `admin_register.csv` | 403 bureaucratic vocabulary entries from Holguín + roots |
| `grammar_profile.md` | Distributional analysis |
| `corpus_stats.json` | Corpus statistics |

## The Hangman: current state

The table aligns 29 Quechua morpheme ranks against 29 khipu byte-pattern ranks. Strongest hypotheses:

1. **W:0 = accusative/case role** (rank-1 both, 22.8% vs top khipu pattern)
2. **AB:0 = evidentiality** (rank-2 both; genre-adjusted to -mi for admin)
3. **MB:0 = plurality** (rank-3 both: -kuna PL vs MB:0)
4. **Color tier = case system** (structural, not yet 1:1)

These are **hypotheses for testing**, not established mappings. The next step is to test each against positional and distributional constraints.

## Admin register

403 entries across 13 semantic domains. Largest: numbers (176), time (48), agriculture (47), space/direction (44). Includes 13 grammatical morphemes (9 case, 4 evidential). All entries include earliest attestation (1560/1608/modern) with Holguín 1608 prioritized per researcher directive.

## What's still needed

1. **Administrative Quechua frequencies:** Mine colonial administrative documents (wills, tribute lists, court records) for register-appropriate rankings
2. **Holguín example mining:** The 160 filtered sentences are a start; the full grammar has more
3. **Segmentation refinement:** Fix compound roots (chaymanta), OCR artifacts (cwri)
4. **Positional analysis:** Where do top morphemes occur in the word? (Started, not completed)
5. **Hypothesis testing:** Test the four Hangman alignments against khipu distributional data
