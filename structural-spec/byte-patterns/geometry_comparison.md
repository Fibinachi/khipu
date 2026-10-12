# Repetition Geometry Comparison: Khipu Bytes vs Quechua Morphemes

## Summary

Khipu byte n-grams show **natural-language-like Zipf distributions** (slope ≈ -0.93).
Quechua template-generated n-grams show artificially flat slopes (≈ -0.54, -0.32).
The Quechua side cannot serve as a valid comparison baseline due to 98% template
generation. However, the khipu side alone provides strong evidence of language-like
structure.

## Khipu Byte N-grams (593 non-funerary khipu, 51,147 cord-tokens)

| N-gram size | Types | Tokens | Zipf slope | Top pattern | Top in N khipu |
|-------------|-------|--------|------------|-------------|----------------|
| 4 bytes (1 cord) | 7,316 | 51,147 | -0.930 | `f8040000` (W:S:Z:L1=0) | 287 (48%) |
| 8 bytes (2 cords) | 26,096 | 50,561 | -0.935 | `f8040000f8040000` (W,W) | 135 (23%) |
| 12 bytes (3 cords) | 35,861 | 49,976 | -0.899 | `f8040000`×3 (W,W,W) | 75 (13%) |

**Zipf slopes (-0.93, -0.94, -0.90) are within the natural language range (≈ -1.0).**
This is not expected for random data or purely numerical tallies. It indicates
a combinatorial system with a small set of high-frequency structural elements
and a long tail of rare content elements — exactly the function-word/content-word
distinction in natural language.

### Positional distribution (top 50 n-grams)
- Front (0-33%): 0.25-0.28
- Middle (33-67%): 0.35
- Back (67-100%): 0.37-0.40

Slight back-weighting. Structural patterns (empty cords) tend toward later positions,
consistent with the accrual model (later additions use more structural scaffolding).

### Cross-document sharing (top 100 n-grams)
- 4-byte: mean share 7.3%, max 48.4% (f8040000 in 287/593 khipu)
- 8-byte: mean share 3.4%, max 22.8%
- Zero single-document n-grams in top 100 (4-byte): the most frequent patterns are
  shared across the corpus, indicating a common structural grammar.

## Quechua Morpheme N-grams (1,411 phrases)

| N-gram | Types | Tokens | Zipf slope |
|--------|-------|--------|------------|
| Bigrams | 1,365 | 3,920 | -0.544 |
| Trigrams | 1,622 | 2,509 | -0.323 |

**These slopes are artificially flat** due to 98% rule-generated templates producing
uniform bigram frequencies (43, 43, 43...). They do NOT represent natural Quechua
usage and cannot serve as a comparison baseline.

Positional: heavily middle-weighted (0.82 for bigrams) — a template artifact.

## Verdict

**The repetition geometries do not directly rhyme** because the Quechua side is
invalid as a natural-language baseline. However:

1. **Khipu byte patterns independently show language-like Zipf structure** (-0.93).
   This is evidence FOR the "writing conveys language" hypothesis from a completely
   independent angle (byte statistics, not grammatical analysis).

2. **The most frequent khipu patterns are structural, not lexical** — empty cords
   in grammatical-tier colors (W, AB, MB, KB). This confirms the two-tier color
   model at the byte level: the grammatical tier IS the function-word layer.

3. **A valid comparison requires natural Quechua text**, not templates. The
   infrastructure is built; rerunning against a Quechua text corpus (e.g.,
   transcribed oral narratives) would provide the real test.

## Key numbers for citation
- Khipu 4-byte Zipf slope: -0.930 (n=7,316 types, 51,147 tokens, 593 documents)
- Most frequent cord: W:S:Z:L1=0 — 4,786 occurrences in 287 khipu (48%)
- Most frequent pair: (W:S:Z:L1=0)² — 2,601 occurrences in 135 khipu
