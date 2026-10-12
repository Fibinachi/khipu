# Phonetic-to-Hex Encoding Scheme for Colonial Quechua

## Rationale

To compare Quechua SOUND STRUCTURE against khipu BYTE STRUCTURE without
presupposing any meaning mapping, each Quechua phoneme is assigned one byte.
Phonetically similar segments receive numerically adjacent values, so that
similar-sounding morphemes produce similar hex strings. This makes the
encoding sensitive to phonotactic patterning rather than arbitrary.

## Phoneme inventory

Based on the colonial descriptions (Santo Tomas 1560, Gonzalez Holguin
1607-1608) of the southern Quechua prestige variety ("lengua general"):

- 3 vowels: /a, i, u/
- 16 consonants: /p, t, k, q, ch, s, sh, h, m, n, ny, l, ll, r, w, y/

## Byte assignments

### Vowels (by height)

| Phoneme | Byte | Notes |
|---------|------|-------|
| a | 0x01 | low |
| i | 0x02 | high front |
| u | 0x03 | high back |

### Consonants (by place of articulation)

| Place | Phoneme | Byte |
|-------|---------|------|
| Labial | p | 0x10 |
| Labial | m | 0x11 |
| Labial | w | 0x12 |
| Dental/alveolar | t | 0x14 |
| Dental/alveolar | n | 0x15 |
| Dental/alveolar | s | 0x16 |
| Dental/alveolar | l | 0x17 |
| Dental/alveolar | r | 0x18 |
| Palatal | ch | 0x1A |
| Palatal | ny | 0x1B |
| Palatal | ll | 0x1C |
| Palatal | y | 0x1D |
| Palatal | sh | 0x1E |
| Velar | k | 0x20 |
| Uvular | q | 0x23 |
| Glottal | h | 0x24 |

Digraphs (ch, ll, sh, qu) are matched before single characters during
tokenization. Morpheme boundary markers (=, -) are stripped before encoding.

## Examples

| Morpheme | Gloss | Phonemes | Hex | Skeleton | Bytes |
|----------|-------|----------|-----|----------|-------|
| =mi | EVD.Direct | m-i | 1102 | CV | 2 |
| =si | EVD.Reportative | s-i | 1602 | CV | 2 |
| =cha | EVD.Conjectural | ch-a | 1a01 | CV | 2 |
| -ta | ACC | t-a | 1401 | CV | 2 |
| -pi | LOC | p-i | 1002 | CV | 2 |
| -man | ALL | m-a-n | 110115 | CVC | 3 |
| -kuna | PL | k-u-n-a | 20031501 | CVCV | 4 |
| -manta | ABL | m-a-n-t-a | 1101151401 | CVCVCV | 6 |

## Key property

Function morphemes (suffixes, enclitics) are overwhelmingly short:
44 of 50 are 1-3 bytes, and the dominant shape is CV (2 bytes). Content
morphemes (roots) range 2-13 bytes with a peak at 4 bytes. This length
asymmetry between grammatical and lexical items is the phonetic analogue
of the khipu pattern where grammatical-tier cords are structurally simple
(4 bytes, zero value) and content cords carry payload.

## Limitations

1. Colonial orthography is inconsistent; the encoding normalizes to a
   phonemic ideal that smooths over dialectal and diachronic variation.
2. The uvular/velar distinction (k vs q) had already begun merging in
   some varieties by 1600; the encoding preserves the colonial contrast.
3. Stress and vowel length are not encoded (Quechua stress is predictable:
   penultimate).
