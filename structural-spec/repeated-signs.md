# Repeated Signs in Anomalous Khipu: Mining for Recurring "Words"

**Date:** 2026-10-11
**Data:** 20 anomalous khipu, 3,184 transcribed cords (`anomalous-transcriptions.csv`)
**Method:** Normalized signatures (level + color + knot-sequence + flags; cord indices dropped).
1,230 distinct signatures. 534 cords (17%) are standard decimal numerals.

---

## HEADLINE FINDING: Knot-twist direction marks funerary vs non-funerary

The strongest "linguistic" pattern in the anomalous corpus is not a repeated word —
it is a **directional code** that cleanly separates funerary from non-funerary khipu:

| Sign | Funerary cords | Non-funerary cords | Expected (random) | z-score |
|------|---------------|-------------------|-------------------|---------|
| `Eu` (u-twist fig-8) | **0** | **115** | 31.5 fun | p = 10^-16.3 |
| `Lu` (u-twist long) | **1** | **325** | 89.1 fun | z = -11.6 |
| `Es` (s-twist fig-8) | **142** | 51 | 52.7 fun | z = +14.9 |
| `Ls` (s-twist long) | 114 (13.1%) | 285 (12.3%) | — | neutral |

**Reading:** u-twist knots are **exclusive** to non-funerary anomalous khipu (440 tokens,
1 exception). s-twist figure-eights are **7.4x enriched** on funerary khipu. s-twist
long knots are neutral (equal rates) — the direction effect is specific to the
figure-eight and to u-twist generally.

**Color compounds with direction form the actual "words":**
- `AB:Es` — 83 tokens, the dominant funerary subsidiary sign (AB color + s-twist fig-8)
- `B:Eu` — 50 tokens, the dominant non-funerary anomalous sign (B color + u-twist fig-8)
- `W:Es` / `W:Eu` — white versions crossing the boundary (16 / 22 tokens)

A figure-eight normally reads as "1" — but a *direction-marked* figure-eight on a
subsidiary, recurring 31 times across 3 khipu with identical color, is not the
number 1. It is a lexical/marker sign. **Assessment: LIKELY WORD** (both `AB:Es`
and `B:Eu`).

---

## Top 20 repeated cord signatures

(Frequencies across all 20 khipu; "khipu" = distinct documents containing the sign.)

| # | Count | Khipu | Signature | Assessment |
|---|------:|------:|-----------|------------|
| 1 | 248 | 5 | `L1:YB:∅` | STRUCTURAL — 239/248 on 1000183 alone (single-khipu run) |
| 2 | 125 | 13 | `L1:W:∅` | STRUCTURAL — empty white cords widespread; blank-slot convention |
| 3 | 94 | 7 | `L2:W:∅` | STRUCTURAL — empty white subsidiaries |
| 4 | 77 | 6 | `L1:AB:∅` | STRUCTURAL — empty AB cords |
| 5 | 65 | 1 | `L1:YB:E` | NUMERAL — plain "1" on YB, single khipu |
| 6 | 50 | 10 | `L1:?:∅` | DATA — unrecorded color, not a sign |
| 7 | 48 | 5 | `L2:MB:∅` | STRUCTURAL |
| 8 | 42 | 1 | `L1:BB:∅` | STRUCTURAL, single khipu |
| 9 | 37 | 7 | `L1:MB:∅` | STRUCTURAL |
| 10 | 37 | 1 | `L2:W:MB:∅` | STRUCTURAL, single khipu |
| 11 | 32 | 3 | `L2:AB:∅` | STRUCTURAL |
| 12 | 31 | 3 | `L2:AB:Es` | **LIKELY WORD** — funerary subsidiary marker (see above) |
| 13 | 31 | 3 | `L2:W:Es` | **LIKELY WORD** — funerary subsidiary marker, white version |
| 14 | 27 | 2 | `L1:W:E` | NUMERAL — plain "1" |
| 15 | 23 | 2 | `L2:B:W:Eu` | **LIKELY WORD** — non-funerary marker, compound color + u-twist |
| 16 | 21 | 3 | `L1:W:L4u` | **LIKELY WORD** — u-twist long-4, cross-khipu, non-standard |
| 17 | 20 | 4 | `L1:AB:L2` | NUMERAL — standard "20"-class |
| 18 | 20 | 3 | `L1:AB:Es` | **LIKELY WORD** — funerary marker on main cord |
| 19 | 19 | 3 | `L2:AB:L2` | NUMERAL |
| 20 | 19 | 3 | `L1:B:∅` | STRUCTURAL |

**Key caveat on empty cords (`∅`):** They dominate raw frequencies but are
concentrated, not shared vocabulary. `L1:YB:∅` (rank 1) is 96% on one khipu
(1000183). Empty cords are *structural* (blank slots, spacers, or unknotted
placeholders), not words. The permutation test confirms: top empty-cord
signatures land on *fewer* khipu than chance (concentrated), not more.

---

## Repeated bigrams/trigrams (level-1 sequences, consecutive cords)

19 bigrams and 4 trigrams repeat on 2+ khipu (of 1,404 / 1,605 total).

**Strongest (observed vs expected under unigram independence):**

| Bigram | Obs | Exp | Ratio | Khipu | Assessment |
|--------|----:|----:|------:|-------|------------|
| `L1:B:L2u` / `L1:B:L2u` | 7 | 0.07 | 100x | 1000197, 1000198 | COINCIDENCE — joined khipu (one document) |
| `L1:B:∅` / `L1:B:∅` | 7 | 0.17 | 41x | 1000144, 1000198 | POSSIBLY STRUCTURAL |
| `L1:AB:∅` / `L1:AB:∅` | 37 | 2.78 | 13x | 1000018, 1000567 | POSSIBLY WORD-PHRASE (see below) |
| `L1:AB:∅` / `L1:AB:Es` | 8 | 0.72 | 11x | 1000009, 1000018 | **LIKELY PHRASE** — empty-AB followed by AB:Es marker |
| `L1:AB:Es` / `L1:AB:∅` | 7 | 0.72 | 10x | 1000009, 1000018 | **LIKELY PHRASE** — mirror of above |
| `L1:YB:∅` / `L1:YB:∅` | 88 | 28.9 | 3x | 1000183, 1000583 | STRUCTURAL — long empty runs |

**Trigrams:**
- `L1:AB:∅` × 3: 22x on 1000018 + 1000567 (funerary + unknown)
- `L1:AB:∅, L1:AB:Es, L1:AB:∅`: 3x on 1000009 + 1000018 (both funerary)

**Reading:** If color is a lexical channel, then `AB:∅, AB:∅, AB:∅` is a repeated
three-unit color sequence — a "phrase" — shared between a funerary khipu and
1000567. The `∅,Es,∅` sandwich (empty, marker, empty) on two funerary khipu
looks like a **framed sign**: the Es marker delimited by blank AB cords.
**Assessment: SUGGESTIVE** — needs the color-lexicon hypothesis to be a "phrase,"
but the framing pattern is real (11x over independence null).

**Coincidence baseline note:** The independence null is conservative-wrong for
within-khipu sequences (cords on one khipu are never independent). The probative
cases are the cross-khipu repetitions. Of the 19 cross-khipu bigrams, discount
the 1000197/1000198 pair (physically joined = one document). The funerary
`AB:∅/AB:Es` alternation on 1000009+1000018 (two *separate* Leymebamba khipu)
is the cleanest cross-document phrase candidate.

---

## Rare shared signs ("Z" characters): 2–5 occurrences on 2+ khipu

59 signatures meet the criterion. Every one is direction-anomalous or
structurally marked — **zero** plain standard numerals qualify, which itself
confirms that rare shared signs are non-numerical by nature.

**Most significant (by khipu spread):**

| Sign | Count | Khipu | Notes |
|------|------:|-------|-------|
| `H:W:∅` | 5 | 5 | Empty white HEADER on 5 khipu — shared blank-title-page convention |
| `L2:MB:L2s` | 5 | 3 | s-twist long on MB subsidiary |
| `L1:W:Su-L2u` | 3 | 3 | Paired direction-anomalous knots (Su then L2u), white |
| `L3:AB:Es` | 4 | 3 | Funerary marker at level 3 — the sign works at depth |
| `H:AB:∅` | 2 | 2 | Empty AB header — header-color variant of `H:W:∅` |
| `H:YB:∅` | 2 | 2 | Empty YB header — third header-color variant |
| `L1:W:Ss-L5s` | 3 | 2 | s-twist pair, white |
| `L2:KB:W:Es` | 2 | 2 | Compound color + Es — compound version of funerary marker |
| `L2:BL:MB:Es` | 2 | 2 | Double compound + Es |

**The empty-header series** (`H:W:∅`, `H:AB:∅`, `H:YB:∅`) is notable: 9 occurrences
across 7+ khipu of an *unknotted primary cord* in white, AB, or YB. Either a
shared "blank title page" convention or headers whose knots were never tied /
not recorded. **Assessment: POSSIBLY STRUCTURAL.**

---

## Position analysis

**Level-1 shared signs are positionally DIFFUSE** (spread 0.7–1.0 across the cord):
`L1:AB:Es` appears at 11%–99% of cord length; `L1:W:Su` at 1%–98%. They are
*not* positional markers (not headers, not footers). They occur anywhere.

**Subsidiary shared signs have no L1 position** (they're off the main cord) but
are consistent in *level + color + direction* — the sign's identity is fully
specified without position. This matches a lexical item better than a positional
marker: the "word" is the same wherever it attaches.

---

## Coincidence baseline: formal statement

1. **Bigram independence null:** 8/19 cross-khipu bigrams exceed 10x expected.
   The null is anti-conservative within khipu but the cross-khipu cases
   (especially funerary `AB:∅/AB:Es` on two separate documents) survive it.

2. **Permutation null (2,000 shuffles of khipu labels):** Top empty-cord
   signatures are *concentrated* (fewer khipu than chance, p≈1.0 upper tail) —
   confirming they are local structural features, not shared vocabulary.

3. **Direction × funerary (Fisher's exact / hypergeometric):**
   - Eu: 0/115 on funerary — p = 10^-16.3 under random assignment
   - Es: 142/193 on funerary vs 52.7 expected — z = +14.9
   - Lu: 1/326 on funerary vs 89.1 expected — z = -11.6
   None are remotely consistent with chance.

---

## Summary assessments

| Finding | Verdict |
|---------|---------|
| `AB:Es` / `W:Es` on subsidiaries = funerary marker signs | **LIKELY WORD** |
| `B:Eu` / `W:Eu`, `Lu` = non-funerary anomalous marker signs | **LIKELY WORD** |
| u-twist exclusivity to non-funerary (440:1) | **SYSTEMATIC** (p=10^-16) |
| s-twist fig-8 enrichment on funerary (7.4x) | **SYSTEMATIC** (z=14.9) |
| Funerary `AB:∅ / AB:Es` bigram phrase | **SUGGESTIVE** |
| Empty-cord runs (`YB:∅` ×239 etc.) | STRUCTURAL, single-khipu |
| Empty headers (`H:W:∅` etc., 5+ khipu) | POSSIBLY STRUCTURAL (shared convention) |
| `L1:B:L2u` bigram "repetition" | COINCIDENCE (joined khipu) |
| L1 shared signs as positional markers | REFUTED (diffuse positions) |

**Bottom line for the "word documents" hypothesis:** The anomalous khipu do
reuse signs across documents, and the reuse is statistically undeniable for
twist-direction. But the clearest "lexicon" found is a **two-sign directional
code** (s-twist = funerary-associated, u-twist = non-funerary-anomalous),
compounded with color — not a large vocabulary. It looks less like a
95-word language and more like a **binary register marker**: which *kind* of
document this is, signaled at the knot level. The actual "words," if they exist,
may be the colors themselves in sequence — the `AB,AB,AB` runs — with direction
as the channel marker telling the reader which register they're in.
