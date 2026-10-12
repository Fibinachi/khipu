# Huarochirí Quechua: Grammatical Profile

Natural-language baseline for khipu comparison. Source: Arguedas 1966 bilingual edition (Quechua original c. 1608).

## Corpus

| Metric | Value |
|---|---|
| Quechua paragraphs | 402 |
| Quechua words | 20,002 |
| Grammatical morpheme tokens | 3,595 |
| Grammatical morpheme types | 29 |
| Root tokens | 7,417 |
| Root types | 327 |
| Zipf slope (grammatical) | -1.605 |

## The "E" of Huarochirí Quechua

Ranked grammatical morphemes by frequency:

| Rank | Morpheme | Count | % | Type | Gloss |
|---|---|---|---|---|---|
| 1 | -ta | 820 | 22.8 | suffix | ACCusative |
| 2 | -si | 439 | 12.2 | enclitic | EVD.Reportative |
| 3 | -kuna | 321 | 8.9 | suffix | PLural |
| 4 | -pas | 246 | 6.8 | enclitic | ADDitive ("too") |
| 5 | -ri | 171 | 4.8 | suffix | INCHoative |
| 6 | -mi | 169 | 4.7 | enclitic | EVD.Direct |
| 7 | -spa | 159 | 4.4 | suffix | Switch-ref Same-Subject |
| 8 | -pi | 136 | 3.8 | suffix | LOCative |
| 9 | -na | 132 | 3.7 | suffix | NOMinalizer (obligation) |
| 10 | -pa | 117 | 3.3 | suffix | GENitive |
| 11 | -ni | 104 | 2.9 | suffix | 1SG subject |
| 12 | -lla | 104 | 2.9 | enclitic | EXCLusive ("only") |
| 13 | -ku | 97 | 2.7 | suffix | REFLEXive/middle |
| 14 | -nku | 86 | 2.4 | suffix | POSSessive 3PL |
| 15 | -chi | 85 | 2.4 | suffix | CAUSative |
| 16 | -mu | 83 | 2.3 | suffix | CISLocative ("hither") |
| 17 | -man | 78 | 2.2 | suffix | ALLative ("to") |
| 18 | -manta | 62 | 1.7 | suffix | ABLative ("from") |
| 19 | -wan | 61 | 1.7 | suffix | COMitative/INSTrumental |
| 20 | -cha | 45 | 1.3 | enclitic | EVD.Conjectural |

## Key observations

**1. Accusative dominance.** -ta accounts for nearly 1 in 4 grammatical morphemes. This is expected in SOV narrative with many transitive clauses. Any khipu grammatical tier should show a similarly dominant top unit.

**2. Reportative inflation.** -si (rank 2, 12.2%) is genre-specific. Huarochirí is mythological narrative ("they say..."). In administrative Quechua, -mi (direct evidential, rank 6 here) would outrank -si. This is the critical register mismatch: khipu are bureaucratic, Huarochirí is mythological.

**3. Case system fully represented.** Six of nine Quechua cases appear in the top 20: -ta (ACC), -pi (LOC), -pa (GEN), -man (ALL), -manta (ABL), -wan (COM/INST). Missing from top ranks: -paq (BEN, rank 29, only 1 token), -kama (LIM, rank 21), -q (GEN.alt).

**4. Evidentiality is frequent.** Combined evidentials (-si + -mi + -cha) = 653 tokens, 18.2% of grammatical morphemes. Nearly 1 in 5. This supports the khipu evidentiality hypothesis: if Quechua marks source-of-information this pervasively, a Quechua-based writing system should too.

**5. Top roots are deictic/narrative.** chay (1302), kay (784), ñispa (429, quotative), runa (340), mana (239), pacha (231). Demonstratives and the quotative dominate — again, narrative genre. Administrative text would show different roots (numbers, titles, commodities).

## Top bigrams

| Bigram | Count | Pattern |
|---|---|---|
| ROOT+ta | 623 | Object marking |
| ta+ROOT | 597 | (segmentation boundary) |
| si+ROOT | 428 | Reportative framing |
| ROOT+si | 395 | Reportative framing |
| ROOT+kuna | 316 | Plural marking |
| pas+ROOT | 214 | Additive |
| mi+ROOT | 158 | Direct evidential |

The ROOT+ta bigram (623) confirms accusative as the primary grammatical operation.

## Zipf note

Slope -1.605 is steeper than the natural-language ideal (-1.0). Likely causes: (a) genre homogeneity (single narrative collection), (b) only 29 grammatical types (closed class), (c) Arguedas orthography normalization artifacts. The khipu byte Zipf (-0.93) was computed over 51,147 tokens with more types. Not directly comparable, but both show the heavy-tailed distribution characteristic of linguistic systems.

## Register mismatch warning

Huarochirí is **mythological narrative**. Khipu are **administrative records**. The frequency rankings will differ:
- Narrative: -si > -mi, high quotatives, demonstratives
- Administrative (predicted): -mi > -si, high case markers, numbers, titles

The grammatical *inventory* (which morphemes exist) transfers. The *rankings* do not transfer directly. Use Huarochirí for the morpheme catalog and structural patterns; use Holguín's administrative examples for register-appropriate frequencies.
