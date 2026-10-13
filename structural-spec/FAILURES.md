# Exploration Failures Log

**Purpose:** A complete record of hypotheses tested and abandoned, solutions
tried that did not work, and null results. This is the other half of the
research record — what we tried, not just what survived.

**Date:** 2026-10-12
**Corpus:** Open Khipu Repository (612 khipu), Khipu Field Guide (66 khipu)

---

## Structural rules

### R6 (top-cord tree) — FAILED as stated
The proposed rule that top cords form a valid attachment tree above the
primary cord holds on only 4/25 OKR khipu (16%) and 1/4 funerary khipu
(25%). Investigation showed the failures trace to misattributed PENDANT_FROM
values in the source data (top cords on khipu 1000024 carry parent IDs
pointing at khipu 1000023), not to real structural violations. Status:
unresolved pending source verification. Not part of the spec.

### R4 (color recording) — PROBABILISTIC, not universal
Holds at 71.7% on OKR, 100% on KFG, 22.7% on funerary khipu. Every examined
failure is an incomplete database record (e.g., 1000088: 195 cords, zero
knots, zero colors — a data-entry stub). The rule describes data completeness,
not khipu structure. Reported with rates as a data-quality caveat.

---

## Killed hypotheses

### Compound color order as routing signal — FAILED at Inkawasi
Corpus-wide AB:W/W:AB asymmetry (11.3:1) collapses to 1.2:1 within the
Inkawasi warehouse. The signal is driven entirely by non-warehouse khipu.
Verdict: local pattern, not khipu grammar.

### "Compounds are always subsidiaries" — FAILED as absolute
13.6% of compound-color cords sit at level 1. A depth gradient holds
(13.6% → 34.8% with depth), but the absolute version is false.

### Parent = sum of subsidiaries — FAILED at Inkawasi
Exact nonzero parent–subsidiary sum matches essentially never occur.
Summation is a top-cord phenomenon (Ascher & Ascher), not a general
parent–subsidiary rule. This contradicts the Smarthistory/Quave
"corrections, exceptions, subsets" reading as a universal.

### White = unimportant source — LOCAL ONLY, fails corpus-wide
Holds at Inkawasi (white subsidiaries median 1 vs colored 21). Fails
corpus-wide (white vs colored subsidiary medians 3 vs 3, n=2641/4681;
no gradient outside Inkawasi). Verdict: local scribal convention, not
khipu grammar. What generalizes is structural (mains > subsidiaries,
median 11 vs 3, p<0.0001).

### Red as administrative section divider — NO SUPPORT
Red appears in only 80/593 khipu; median 0% in every cluster. Appears
to be a funerary/Leymebamba phenomenon, not an administrative convention.

### Red-tag document markers — FALSIFIED
Strong-red cords show no positional bias toward document start.
The document-tag hypothesis is dead.

### Pre-cut standard cord blanks — REJECTED
Tested whether primary cords cluster at standard lengths (evidence of
pre-cut blanks). No length clustering at round sizes within file types.
Primary cord length correlates with pendant count (r=0.67) — cord is
cut to fit the file, not selected from blanks.

### Conklin strict construction sequence — CONTRADICTED
Conklin's proposed spin → ply → attach → knot → attach subsidiaries
sequence, as a claim about original construction order, is contradicted
by the data. The weaker "khipu as living document" version (cords added,
tied, removed after initial construction) is supported instead.

### Garcilaso commodity-color mappings — UNTESTABLE / WEAK
Gold = yellow and silver = white cannot be tested: no surviving khipu
from gold or silver producing regions, tiny yellow-cord sample (n=9),
and tribute portability breaks the provenience logic. Red = soldiers
needs broadening to state presence generally. The 400-year-old hypothesis
survives only in its weakest form (colors encode something systematic).

### 1000588 restoration — UNVALIDATED
The arithmetic of the proposed restoration does not close. Dividers may
be category labels rather than structural elements. Do not cite as
a successful restoration.

---

## Null and inconclusive results (reported, not buried)

- **Quechua syntax test:** value ordering and boundary marking both NULL.
  The postpositional-order claim rests on 70–75% subsidiary/parent color
  contrast with no permutation baseline yet — flagged as needing one.
- **Hangman hypothesis:** letter cords are document-level formatting, not
  Quechua morphemes. Dead.
- **Evidentiality test:** knot direction (Z/U/S) shows a three-way
  distinction, not the predicted binary marked/unmarked split. Z is
  neutral, U weakly enriched on marked cords, S disproportionately on
  unmarked white cords. The original hypothesis was misaimed.
- **Direction test:** "repaired" in catalog notes means physical damage,
  not use-life additions. The test measured damage, not chronology.
  Inconclusive as designed, but informative: depth is a design feature,
  not a preservation accident.
- **Inkawasi a=b+c equations:** published values unrecoverable from OKR
  — every Inkawasi long knot lacks NUM_TURNS. 41% of Inkawasi cords
  decode NULL under the type-aware decoder. Any quantitative Inkawasi
  claim from OKR alone is crippled.

---

## Solutions tried and abandoned

- **PENDANT_FROM as hierarchy indicator:** abandoned. The field is set on
  all cords including top level (verified 54/54 on Santa 1000270).
  CORD_LEVEL is the reliable hierarchy field. This corrects analyses
  built on PENDANT_FROM.
- **Database CORD_ID as physical order:** abandoned. Physical order is
  CORD_ORDINAL, not CORD_ID.
- **Magic-number header frame:** revised. The primary cord carries
  allocation (length ~ pendant count), not type identity. Type lives
  in body structure. Reframed as pre-sized blank + structural template.
- **Two-bucket typology (census vs inventory):** abandoned. Missed the
  Bulk Tally type entirely (78 khipu) and misassigned 18 funerary khipu
  as inventory. Replaced by four-type document analysis.
- **"First new khipu" framing:** narrowed. Replicas exist; the claim is
  now "first khipu generated from a formal computational specification."
- **"Formal grammar" framing:** narrowed to "document specification for
  Inca accounting khipu." R1–R3 subsequently confirmed as khipu-wide
  (funerary holds at 100%), but the document typology and generative
  spec remain accounting-scoped.

---

## Methodological caveats (acknowledged, not yet fixed)

1. **Multiple comparisons:** ~40 reports, dozens of tests, no correction.
   Core structural claims (R1–R3) rest on universal quantification, not
   p-values, and are unaffected. The interpretive layer (syntax tests,
   contrast claims) needs permutation baselines.
2. **Reproducibility:** hardcoded paths, gitignored database, no
   requirements file, 60+ one-off scripts. Pipeline is not runnable
   from a clean clone.
3. **Cluster stability:** six form types have silhouette scores and
   95.6% tree agreement but no bootstrap or alternate-k test.
4. **Site non-independence:** khipu from the same site/collection are
   not independent observations. KFG out-of-sample replication partially
   mitigates for structural rules; not addressed for interpretive claims.
