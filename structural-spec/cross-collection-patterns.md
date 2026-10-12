# Cross-Collection Knot Pattern Matching

**Date:** 2026-10-10
**Question (Charles):** Do specific knot *patterns* — sequences, structural arrangements — appear across different museum collections? If so, that's evidence of empire-wide bureaucratic standardization.

## Data & method

- **Source:** Open Khipu Repository database (`okr-khipu.db`): 619 quipu, 54,403 cords, 110,677 knots across ~50 normalized museum/collection labels.
- **Signature:** Per quipu, the ordered tuple of per-cord total decimal values (sum of knot values per cord, cords in deterministic cluster/cord order). 593 quipu yielded signatures.
- **Museum normalization:** spelling variants merged (e.g., "Museum für Völkerkunde, Berlin" + "Ethnologisches Museum, Berlin" → one Berlin collection; "Proyecto Incahuasi/Incahausi/Inahuasi" → one).
- **Tests:** (1) exact full-sequence matches across museums; (2) E-E-E "name marker" distribution; (3) longest-common-subsequence (LCS) distribution with permutation null; (4) duplicate-record integrity check on all reported pairs.

## Finding 1: No two quipu are identical across museums

**Zero exact full-sequence matches** across different museums (of 593 quipu). The permutation null (shuffled values, 5 trials) also yields zero — so this is the expected baseline, not a failure of the method.

**Interpretation:** Quipu are individual records, not pre-filled forms. Standardization lives at the *convention* level (how to record), not the *document* level (what was recorded). This is exactly what a functioning bureaucracy looks like: shared grammar, unique entries.

## Finding 2: The E-E-E convention is cross-collection

37 cords beginning with three consecutive figure-eight knots (E-E-E), in **16 quipu across 11 museums** on three continents:

| Museum | E-E-E cords |
|---|---|
| AMNH, New York | 8 |
| Proyecto Incahuasi (excavation) | 8 |
| Gothenburg (World Culture Museum) | 7 |
| Berlin (Ethnologisches Museum) | 4 |
| Centro Mallqui, Leymebamba | 3 |
| Puruchuco Museum | 2 |
| Univ. of Pennsylvania Museum | 1 |
| Munich (Museum Fünf Kontinente) | 1 |
| Museo Chileno de Arte Precolombino | 1 |
| Museo Regional de Ica | 1 |
| Museo de Sitio de Pachacamac | 1 |

This is a **shared scribal convention**, not a local habit. But its placement varies, which complicates Urton's "header/name marker" reading:

- **Puruchuco KH0255** (1000242, Urton's toponym candidate): E-E-E-E opens the *first* cord of a 4-cord quipu. Matches the header hypothesis.
- **AMNH 1000491**: 7 of 8 cords *each* begin E-E-E. Not a header — a per-entry label.
- **Gothenburg 1000320**: E-E-E cords at positions 1, 21, 23, 28, 36, 41, 44 of 49. Scattered — possibly group delimiters.
- Only **2 of 37** E-E-E cords are their quipu's first cord.

**Honest reading:** The triple-figure-eight opening is a genuine empire-wide convention (11 museums is not coincidence), but it is not a simple document header. It behaves more like a delimiter or entry-label — its function varies by quipu genre.

## Finding 3: Recurring quantity templates across museums

Filtering out trivial census runs (all 1s/2s), the most specific cross-museum numerical matches:

| Shared sequence | Museum A | Museum B | Proveniences |
|---|---|---|---|
| `(10×14)` fourteen cords of 10 | Museo Larco, Lima | Proyecto Incahuasi | Pueblo Libre / Incahuasi |
| `(10×11)` eleven cords of 10 | Munich | Proyecto Incahuasi | Huacho / Incahuasi |
| `(10×10)` ten cords of 10 | Munich | Proyecto Incahuasi | Huacho / Incahuasi |
| `(22,22,21,22,22,100×7)` | Quai Branly, Paris | Museo Nacional, Lima | — / unknown |
| `(110,10×7)` | Munich | Berlin | Huacho / Ica-Pisco |
| `(22×8)` | Berlin | Museo Nacional, Lima | Ica / unknown |
| `(2,5,24,2,2,2,2,2,2)` | Univ. of Pennsylvania | Museo Amano, Lima | — / — |

All pairs verified as **distinct physical quipu** (different investigator numbers, museum numbers, proveniences; none duplicate-flagged).

**Interpretation:** Runs of 10s are the tribute system made visible — decimal denominations produce runs of tens naturally, and the same quota structure (14×10, 11×10) recurs at sites hundreds of kilometers apart (Huacho to Incahuasi). The more specific sequences — `(22,22,21,22,22,100,100,...)` and `(110,10,10,...)` — are harder to explain by chance: the same multi-cord quantity template, in the same order, in Paris and Lima collections.

**Caveat (important):** 2,720 cross-museum pairs share LCS≥6, but the overwhelming majority are runs of 1s and 2s — the census genre, where every cord counts one person. Long runs of ones are *expected* wherever headcounts were taken. The table above excludes these. What remains is smaller but more meaningful: matching *denomination structures*, not just matching tallies.

## Finding 4: What this means for the standardization question

Charles's hypothesis — that knot patterns would match across collections, proving empire-wide standardization — gets a **split verdict**:

- **Document-level identity: NO.** No two quipu from different museums contain the same full numerical sequence. Each quipu records unique local content.
- **Convention-level standardization: YES.** The E-E-E marker convention spans 11 museums. Decimal tribute denominations (runs of 10s) recur across the coast. Multi-cord quantity templates repeat in far-flung collections.
- **The grammar is imperial; the sentences are local.** Quipucamayocs everywhere used the same scribal conventions to record different local realities. That is precisely how a standardized imperial bureaucracy should behave.

## Limitations

1. Cord ordering within quipu follows database cluster/cord ordinals, which reflect the recorder's judgment, not necessarily the original reading order. A different ordering could reveal or dissolve matches.
2. `knot_value_type = 0` (unknown/non-numeric) cords are included as zeros; their treatment is a judgment call.
3. 26 of 619 quipu had no knot data and were excluded.
4. Provenience is missing for many quipu (e.g., the Museo Nacional and Penn specimens), limiting geographic analysis of the matches.
5. The E-E-E functional interpretation (delimiter vs. label vs. name marker) cannot be resolved from pattern data alone — it needs the commodity-mapping work (Chu email) to anchor.

## Bottom line

Knot *patterns* do not repeat across collections at the document level — but knot *conventions* do. The empire standardized how to write, not what was written. The E-E-E marker in 11 museums and the recurring tribute-denomination templates are the strongest structural evidence yet that quipu literacy was an imperial administrative technology, not a set of local folk practices.
