# Constraint Geometry Comparison: Quechua vs Khipu 1000331

## Forbidden bigram rates

| system | symbols | possible | observed | forbidden | rate |
|---|---|---|---|---|---|
| Quechua phonemes | 24 | 576 | 338 | 238 | 41.3% |
| 1000331 colors | 9 | 81 | 28 | 53 | 65.4% |

- 1000331 null (shuffled) forbidden rate: 58.3% (observed 65.4%)
- Quechua null (shuffled phonemes) forbidden rate: 27.5% (observed 41.3%)

## Repeat (X->X) bigrams

- Quechua: 12/24 phonemes allow self-transition
- 1000331: 3/9 colors allow self-transition

## Vowel/consonant-like split

- Quechua vowels (n=3): mean flexibility 44.3
- Quechua consonants (n=21): mean flexibility 25.9
- 1000331 flexible half (6): AB(15), W(12), MB(8), BG(6), AB:PK(4), PK:AB(4)
- 1000331 restricted half (3): MB:AB(3), NONE(3), W:BG(1)

## Quechua class transitions (for reference)

- C->C: 16.0%
- C->V: 44.1%
- V->C: 37.9%
- V->V: 2.0%

## 1000331 flexible/restricted transitions

- F->F: 93.5%
- F->R: 2.9%
- R->F: 3.5%
