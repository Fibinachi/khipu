# Khipu 1000331 "Colorotactic" Constraint Profile

- Sequence length: 171 cords
- Symbol inventory: 9 distinct FULL_COLOR values
- Possible bigrams: 81
- Observed bigrams: 28
- Forbidden bigrams: 53 (65.4%)
- Bigram tokens: 170
- Repeat bigrams (X->X): 3/9

## Symbol frequencies

| symbol | count | pct |
|---|---|---|
| AB | 77 | 45.0% |
| W | 47 | 27.5% |
| MB | 20 | 11.7% |
| BG | 13 | 7.6% |
| PK:AB | 6 | 3.5% |
| NONE | 3 | 1.8% |
| MB:AB | 2 | 1.2% |
| AB:PK | 2 | 1.2% |
| W:BG | 1 | 0.6% |

## Flexibility (distinct followers, distinct predecessors)

| symbol | followers | predecessors | total |
|---|---|---|---|
| AB | 6 | 9 | 15 |
| W | 5 | 7 | 12 |
| MB | 4 | 4 | 8 |
| BG | 5 | 1 | 6 |
| AB:PK | 2 | 2 | 4 |
| PK:AB | 2 | 2 | 4 |
| MB:AB | 1 | 2 | 3 |
| NONE | 2 | 1 | 3 |
| W:BG | 1 | 0 | 1 |

## Top 20 bigrams

- AB -> AB: 35
- W -> AB: 23
- W -> W: 20
- AB -> MB: 15
- AB -> BG: 13
- MB -> AB: 12
- AB -> W: 8
- BG -> W: 6
- MB -> W: 5
- PK:AB -> W: 5
- AB -> PK:AB: 3
- BG -> PK:AB: 3
- AB -> NONE: 3
- MB:AB -> AB: 2
- MB -> MB: 2
- NONE -> W: 2
- W -> MB: 2
- W:BG -> AB: 1
- PK:AB -> AB: 1
- W -> MB:AB: 1

## Top 15 trigrams (syllable candidates)

- W -> W -> AB: 15
- AB -> AB -> AB: 15
- W -> AB -> AB: 13
- AB -> MB -> AB: 8
- AB -> AB -> BG: 8
- AB -> AB -> MB: 7
- MB -> AB -> AB: 7
- W -> AB -> MB: 6
- AB -> BG -> W: 6
- BG -> W -> W: 6
- PK:AB -> W -> W: 5
- W -> W -> W: 5
- AB -> AB -> W: 5
- AB -> W -> AB: 4
- AB -> MB -> W: 4
