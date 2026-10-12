# Top Candidates: Non-Spreadsheet, Language-Like Khipu

## Method
Started from 147 residuals. Applied spreadsheet-negative filter (excluded 89 with
stratification >0.7, zero-heavy >70%, or column repetition). For remaining 49,
computed mutual information (MI) between adjacent cords vs shuffled baseline.
MI ratio >1.0 means sequential order matters (not independent rows).

## Ranked by MI ratio (sequential dependency)

### TIER 1: Symbol-encoding candidates

**1000331** — Museo Amano, Lima. No provenance. 198 cords, MI ratio 1.50.
- Values: 142/198 cords = exactly 2. Values are CONSTANT.
- Colors vary: AB(82), W(46), MB(21), AB+SY(15), BG(13), PK+AB(6).
- When values don't vary, ALL information is in the color sequence.
- This is symbol encoding: each cord = one symbol, sequence = message.
- NOT tabular (no columns, no stratification). NOT numeric (values are filler).
- Strongest language-like candidate in the corpus.
- Open question: is the color sequence grammatical (language) or categorical (coded log)?

### TIER 2: Sequential data (journal/log format, not spreadsheet, not language)

**1000183** — Museo de Ica. No provenance. 615 cords, MI ratio 2.13 (highest).
- 559 L1 entries in sequence. Mostly YB, values 0-5. W as section markers.
- Reads as a sequential log: entry after entry, order matters.
- But values are numeric and vary meaningfully. This is TIME-SERIES data,
  not a spreadsheet (no columns) and not language (numeric, not symbolic).
- Possible: daily log, transaction journal, sequential tally.

**1000083** — Ica. Museum für Völkerkunde, Berlin. 183 cords, MI ratio 1.33.
- Binary W/B alternation with 0/1 values under CB+W parent.
- Binary encoding. Not spreadsheet, not language — a binary system.

### TIER 3: Interesting but ambiguous

**1000029** — Museum of Science, Buffalo. No provenance. 271 cords, MI 1.18.
- One of the five all-U-twist pieces (unknown office).
- Already flagged. High MI suggests sequential structure worth investigating.

**1000287** — Nazca. Museum for World Culture, Gothenburg. 303 cords, MI 1.19.
- Nazca provenance connects to south-coast tradition.

**1000508** — Pachacamac. Ethnologisches Museum, Berlin. 262 cords, MI 1.30.
- Pachacamac provenance. Worth deeper look.

**1000176** — Museo de Ica. No provenance. 38 cords, MI 1.55.
- Small but high MI ratio. Possible fragment of a larger sequential document.

## What "language-like" means here (honest calibration)

**1000331** is the ONLY khipu where:
1. Spreadsheet tests fail (not stratified, not zero-heavy, not column-repetitive)
2. Numeric content is absent (values constant = no numeric information)
3. Sequential order matters (MI 1.5x shuffled baseline)
4. Symbol variety is high (14 distinct color/symbol types)

This is necessary but NOT sufficient for "language encoding." It could be:
- (a) True symbolic language (colors = words/morphemes in sequence)
- (b) Categorical event log (colors = event types in chronological order)
- (c) Ritual/ceremonial sequence (colors = ritual elements in prescribed order)

Distinguishing (a) from (b)/(c) requires: grammatical constraints in the
sequence (which we haven't tested), or external context (which we don't have).

## Bottom line

One khipu (1000331) genuinely looks like sequential symbol encoding rather
than tabular data. It is the best candidate for "language encoded" in the
corpus. But "symbol sequence" ≠ "language" — we cannot claim grammar, syntax,
or readability. It is a lead, not a decipherment.
