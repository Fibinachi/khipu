# Phonetic-to-Knot Mapping Hypothesis

## The proposal

A khipu cord is structurally analogous to a Quechua morpheme, but the
analogy is GRAMMATICAL, not phonetic. Specifically:

| Khipu cord component | Quechua morpheme component | Role |
|----------------------|---------------------------|------|
| Bytes 0-1: color, knot type, direction, level | Phonetic shape (CV, CVC, etc.) | Identity/signature: WHICH unit this is |
| Bytes 2-3: numerical value | Semantic payload | Content: WHAT information it carries |

For **function units**, the payload is empty:
- Quechua: =mi (1102) — 2 bytes, CV shape, carries grammatical role
  (evidentiality), no lexical meaning
- Khipu: f8040000 (W:S:Z:L1=0) — 4 bytes, zero value, carries grammatical
  role (structural position), no numerical content

For **content units**, the payload is full:
- Quechua: root + suffixes (e.g., wasi-yki "your house") — longer phonetic
  shape, carries lexical meaning
- Khipu: distinguishing-color cord with non-zero value — carries the
  recorded quantity/identity

## Why phonetic identity fails but structural identity holds

The khipu does not SPELL Quechua sounds. Instead, both systems independently
evolved (or were designed) with the same deep architecture:

1. **Combinatorial units**: Both combine a small inventory of minimal
   elements (phonemes / cord-features) into morphemes/cords.
2. **Function/content split**: Both reserve the shortest, most frequent
   forms for grammatical operations and longer, rarer forms for content.
3. **Zipfian distribution**: Both show slope approx -1.0, the signature
   of a system balancing speaker/writer economy against listener/reader
   clarity.
4. **Positional grammar**: Both place function markers in predictable
   positions relative to content (Quechua suffixes after roots; khipu
   subsidiary cords after parents).

## Specific testable predictions

If this hypothesis is correct:

1. **Cord "syllable" count**: The number of distinct feature-dimensions
   active on a cord (color+knot+direction+level = up to 4) should
   correlate with morpheme phoneme count. Function cords use fewer
   active dimensions; content cords use more. TESTABLE against the
   existing feature database.

2. **Value as "vowel"**: In Quechua, vowels carry the sonority peak of
   each syllable. In khipu, the value bytes carry the information peak
   of each cord. Cords with zero value are like syllables without
   vowels — structurally present but informationally empty. This
   predicts that zero-value cords should pattern with grammatical
   (not content) positions. TESTABLE: already supported by the
   finding that zero-value cords concentrate in grammatical-tier colors.

3. **Doubling as reduplication**: The khipu doubling signature
   (f8040000f8040000, 2,601x) is structurally parallel to Quechua
   morphological reduplication (e.g., intensive or distributive
   marking). If khipu doubling serves a grammatical function
   (intensification, distribution, pairing), it should occur in
   predictable grammatical contexts, not randomly. TESTABLE against
   cord-level annotations.

4. **Color as "consonant", knot as "vowel"**: If bytes 0-1 encode the
   "pronunciation" of the cord, then color (6 bits, 64 values) has the
   informational capacity of a consonant inventory, while knot type
   (3 bits, 8 values) has the capacity of a vowel inventory. This
   predicts that color should distinguish lexical identity (like
   consonants distinguish roots) while knot type should distinguish
   grammatical role (like vowels mark inflectional patterns in
   Semitic, or tone in other systems). PARTIALLY SUPPORTED: the
   color-tier analysis already found grammatical vs identity tiers.

## What would falsify this

- If function-cord byte patterns do NOT show the same frequency
  rank-order across document types (i.e., if W:0 is dominant in
  census but absent in warehouse, the "function word" analogy breaks).
- If cord value distributions do NOT separate cleanly by color tier
  (i.e., if grammatical-tier colors carry large values as often as
  distinguishing-tier colors).
- If a direct phonetic reading IS found (e.g., a khipu board with
  confirmed sound-values for knots), this structural hypothesis
  becomes unnecessary.

## Bottom line

Khipu and Quechua are not the same code. They are two implementations
of the same deep grammatical architecture: minimal function markers
+ content payloads, Zipfian distributions, positional grammar. The
khipu does not spell Quechua; it THINKS like Quechua. This is why
typological comparison succeeds where direct decipherment stalls.
