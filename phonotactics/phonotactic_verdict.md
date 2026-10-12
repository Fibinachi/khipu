# Phonotactic Verdict: Does 1000331 Obey Language-Like Constraints?

## Numbers

- Quechua forbidden-bigram rate: 41.3% (shuffled null 27.5%; effect +13.8%)
- 1000331 forbidden-bigram rate: 65.4% (shuffled null 58.3%; effect +7.2%)
- 1000331 constraint effect is 52% of Quechua's phonotactic effect
- Quechua vowel/consonant flexibility ratio: 1.71
- 1000331 flexibility asymmetry is inflated by singleton symbols;
  restricted to symbols with n>=5 the top/bottom ratio is ~2.3

## The headline finding: two-tier carrier/signal structure

1000331 is NOT a flat symbol sequence. It decomposes into:

- **Carrier tier**: AB (45.0%) + W (27.5%) = 72.5% of all cords.
  AB->AB (35x) is the top bigram; W->W (20x) is third. Over half of all
  bigrams (50.6%) involve only AB and W.
- **Signal tier**: MB (20), BG (13), PK:AB (6), plus rare compounds,
  embedded in the carrier at mean gaps of 2.6 cords.

Natural-language check: Quechua's top-2 phonemes account for 32.7% of
tokens. 1000331's top-2 "symbols" account for 72.5%. No spoken language
concentrates this heavily.

## Phonotactic geometry comparison (the kill)

| Feature | Quechua | 1000331 |
|---|---|---|
| Identical-adjacent rate (V->V analogue) | 2.0% (strongly disfavored) | AB->AB = 20.6% of all bigrams (the single most common bigram) |
| Dominant pattern | CV alternation (82% of bigrams) | Carrier repetition + binary signal alternation |
| Signal-channel structure | n/a | MB<->BG = 41% of signal transitions |
| Hard positional rules | e.g. no word-initial /r/ | BG occurs ONLY after AB (13/13) |

The single most common bigram in 1000331 (AB->AB) is the pattern most
strongly forbidden in Quechua phonotactics (V->V at 2%). The constraint
geometries are not just different in degree; they are opposite in kind.

## What the +7.2% constraint effect actually measures

The excess bigram constraint beyond the shuffled null is real but is
explained by structural rules, not phonotactics:

1. **BG-after-AB rule**: BG's sole predecessor is AB (hard positional
   constraint, like a section marker that must be "announced").
2. **Carrier/signal segregation**: rare symbols cluster in the signal
   tier rather than distributing randomly.
3. **Binary signal alternation**: MB and BG alternate at 41% in the
   signal channel, consistent with a two-state code or tick-tock pattern.

These are the fingerprints of a **coded or ritual sequence**, not of
spoken-language sound combination.

## Caveats

- Alphabet size: dedup to one FULL_COLOR per cord yields 9 symbols;
  raw join yields 14 (some cords carry multiple color records; the
  first-listed was taken deterministically). High-frequency results
  (AB, W, MB, BG) are robust to this choice.
- Domain: Quechua bigrams are within-word (roots + morphemes); the
  khipu sequence is running text. A morpheme-sequence-level comparison
  would be a stricter test and is recommended follow-up.
- This test addresses PHONOTACTICS only. It does not rule out
  morpheme- or word-level encoding under a different mapping.

## VERDICT: CONSTRAINED BUT NOT LANGUAGE-LIKE

1000331's color sequence has real sequential structure (+7.2% bigram
constraint beyond null), but its geometry contradicts natural-language
phonotactics on every comparable dimension: extreme symbol concentration
(72.5% in two symbols), dominant self-repetition (AB->AB top bigram vs
V->V at 2% in Quechua), and a binary-alternating signal channel.
The structure is consistent with a categorical, ritual, or binary-coded
sequence -- a code, not a phonotactic system. The "language encoded"
hypothesis FAILS at the phonotactic level for khipu 1000331.
