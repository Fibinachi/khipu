# Khipu Feature Database — Isomorphism Join Spec

**Purpose:** Khipu-side feature co-occurrence data for distributional
isomorphism matching against Quechua morpheme co-occurrence data.
Theory: where co-occurrence patterns align across the two systems
(e.g., feature 52 precedes feature 31 at 10x chance in BOTH), that's a
candidate meaning alignment — no glosses required.

**Data:** 3,184 transcribed cords from 20 anomalous khipu
(`../anomalous-transcriptions.csv`), parsed per
`../transcription-notation.md`. 170 atomic features.

## Files

| File | Contents |
|------|----------|
| `feature_ids.csv` | Stable integer ID map: `id,feature_type,feature_value,description`. Feature types: `color, compound, knot, dir, turns, axis, level, struct, flag`. |
| `khipu_features.csv` | Every cord: `khipu_id, cord_ord, level, parent_ord, feature_ids` (semicolon-separated, sorted ascending), `feature_names`. |
| `within_cord_pmi.csv` | Top 200 within-cord feature pairs by PMI (min co-occurrence 3): `pmi, cooccur, feat_a, id_a, feat_b, id_b, count_a, count_b`. |
| `sequential_bigrams.csv` | Top 200 ordered adjacent-cord feature pairs: `count, pmi, feat_from, id_from, feat_to, id_to`. Two sequences merged: L1 physical order + depth-first (parent then subsidiaries). |
| `hierarchical_pairs.csv` | Top 200 parent->subsidiary feature pairs: `count, pmi, parent_feat, parent_id, subsidiary_feat, subsidiary_id`. |
| `sanity_report.md` | Vocabulary size, promiscuity ranking, restriction ranking, complementary-distribution candidates. |
| `build_khipu_features.py` | Reproducible build script. |

## How the Quechua side should format for joining

Produce the **same six files** with morpheme features instead of cord features:

1. **`feature_ids.csv`** — identical columns. Feature types for Quechua:
   `morpheme` (root/affix ID), `pos` (part of speech), `mtype`
   (root/suffix/enclitic), `domain` (semantic domain). The integer IDs
   live in a **separate namespace** from khipu IDs — the join is on
   *pattern shape*, not ID equality.

2. **`khipu_features.csv` equivalent** — call it `quechua_phrases.csv`:
   `source_id, phrase_ord, feature_ids, feature_names` where each row is
   one Quechua word or phrase decomposed into morpheme-feature IDs,
   in surface order.

3. **`within_cord_pmi.csv` equivalent** — `within_word_pmi.csv`: morpheme
   pairs co-occurring in the SAME word/phrase, with PMI vs independence.
   Same columns, same min-count filter (>=3).

4. **`sequential_bigrams.csv`** — morpheme pairs on ADJACENT words in
   running text (or adjacent morphemes within words — document which).
   Same columns.

5. **`hierarchical_pairs.csv` equivalent** — for Quechua this is
   head->dependent pairs (e.g., noun->possessive suffix,
   verb->evidential enclitic). Same columns.

6. **`sanity_report.md`** — same sections.

## The join procedure (mechanical, once both sides exist)

1. For each side, take the top-N pairs by PMI from `within_*_pmi.csv`.
2. Represent each pair as `(rank_of_feat_a_by_promiscuity,
   rank_of_feat_b_by_promiscuity, pmi_bin)` — i.e., abstract away the
   actual features, keep only the *distributional shape*.
3. Find pairs whose shapes match across systems within tolerance.
   A match = candidate alignment between a khipu feature-bundle and a
   Quechua morpheme-bundle.
4. Validate: matched bundles should ALSO align on the sequential and
   hierarchical matrices. A bundle that matches within-word but not
   across-word is weaker.
5. Output: ranked candidate alignments with the supporting PMI evidence
   from both sides. Human review assigns glosses.

## Known properties of the khipu side (for the Quechua team)

- 170 features; most promiscuous: `knot:L`, `level:L1`, `color:W`,
  `knot:S` (syllable-like: combine freely).
- Most restricted: specific compound colors, `struct:missing`,
  `level:H` (grammatical-marker-like: narrow distribution).
- Strong complementary pairs: `color:AB` vs `color:YB` (626/463 cords,
  never co-occur as simple colors); `dir:Es` vs `dir:u` (funerary vs
  non-funerary twist split); `dir:Ls` vs `dir:Lu`.
- Twist direction (`dir:*`) behaves as a register/genre channel, not a
  lexical one — expect it to align with Quechua *discourse-level*
  features (evidentials, register markers), not roots.
- `turns:*` features are numerical and should be EXCLUDED from
  isomorphism matching (they encode quantities, not language).
  Recommended: drop all `turns:` features before joining.
- `struct:empty` (1,068 cords) is a blank-slot convention, not a sign.

## Build

```
python3 build_khipu_features.py
```

Deterministic: feature IDs assigned by sorted `(type, value)`.
Re-running on the same input reproduces all files byte-identically.
