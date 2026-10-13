# Known Failures Log

**Purpose:** A record of hypotheses tested and abandoned, solutions
tried that did not work, and null results. Reconstructed 2026-10-12 from
the test reports — this is a retrospective compilation, not a contemporaneous
lab notebook. Every entry closes with what the failure taught us.

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

**What we learned:** a failing rule is not always a wrong rule — sometimes
it is a dirty dataset. The discipline is to distinguish the two before
discarding either. R6 stays out of the spec until the source records are
verified, not because the idea is dead but because we cannot tell yet.

### R4 (color recording) — PROBABILISTIC, not universal
Holds at 71.7% on OKR, 100% on KFG, 22.7% on funerary khipu. Every examined
failure is an incomplete database record (e.g., 1000088: 195 cords, zero
knots, zero colors — a data-entry stub). The rule describes data completeness,
not khipu structure. Reported with rates as a data-quality caveat.

**What we learned:** conformance rates measure the database as much as the
khipu. A rule that "fails" only on empty records is telling you about
cataloguing practice, not about Inca bureaucracy. Always inspect the failures
before reporting the rate.

---

## Killed hypotheses

### Compound color order as routing signal — FAILED at Inkawasi
Corpus-wide AB:W/W:AB asymmetry (11.3:1) collapses to 1.2:1 within the
Inkawasi warehouse. The signal is driven entirely by non-warehouse khipu.
Verdict: local pattern, not khipu grammar.

**What we learned:** always stratify by context before claiming a universal.
A corpus-wide signal that vanishes inside the best-documented subsite was
never a grammar — it was an artifact of mixing populations.

### "Compounds are always subsidiaries" — FAILED as absolute
13.6% of compound-color cords sit at level 1. A depth gradient holds
(13.6% → 34.8% with depth), but the absolute version is false.

**What we learned:** gradients are more honest than binaries. The absolute
claim was false; the gradient version is true and more informative. When a
rule fails as stated, check whether it holds as a tendency before discarding
it entirely.

### Parent = sum of subsidiaries — FAILED at Inkawasi
Exact nonzero parent–subsidiary sum matches essentially never occur.
Summation is a top-cord phenomenon (Ascher & Ascher), not a general
parent–subsidiary rule. This contradicts the Smarthistory/Quave
"corrections, exceptions, subsets" reading as a universal.

**What we learned:** this failure produced the rider model — subsidiaries as
independent stocks, not additive detail. The most productive failures are the
ones that force a replacement theory, not just a retraction. Killing
parent=sum is what made the custodial-warehouse interpretation possible.

### White = unimportant source — LOCAL ONLY, fails corpus-wide
Holds at Inkawasi (white subsidiaries median 1 vs colored 21). Fails
corpus-wide (white vs colored subsidiary medians 3 vs 3, n=2641/4681;
no gradient outside Inkawasi). Verdict: local scribal convention, not
khipu grammar. What generalizes is structural (mains > subsidiaries,
median 11 vs 3, p<0.0001).

**What we learned:** the local/global distinction is the most important cut
in this whole project. A pattern that holds at one site and vanishes
everywhere else is a scribe's habit, not a civilization's grammar. Test
every "universal" against geographic stratification.

### Red as administrative section divider — NO SUPPORT
Red appears in only 80/593 khipu; median 0% in every cluster. Appears
to be a funerary/Leymebamba phenomenon, not an administrative convention.

**What we learned:** absence is data. The systematic non-appearance of red
in administrative khipu is itself a finding — it tells you red meant
something the accountants did not need. Negative results map the boundaries
of a system.

### Red-tag document markers — FALSIFIED
Strong-red cords show no positional bias toward document start.
The document-tag hypothesis is dead.

**What we learned:** positional hypotheses are cheap to test and clean to
kill. When a theory predicts "X appears at position Y," the test is a
histogram, not an essay. More hypotheses should be framed this way.

### Pre-cut standard cord blanks — REJECTED
Tested whether primary cords cluster at standard lengths (evidence of
pre-cut blanks). No length clustering at round sizes within file types.
Primary cord length correlates with pendant count (r=0.67) — cord is
cut to fit the file, not selected from blanks.

**What we learned:** the khipu maker was not pulling from inventory; each
document got a cord cut for its expected size. That is allocation metadata
in physical form — the header carries the file's expected length. This
rejection is what produced the pre-sized-blank frame.

### Conklin strict construction sequence — CONTRADICTED
Conklin's proposed spin → ply → attach → knot → attach subsidiaries
sequence, as a claim about original construction order, is contradicted
by the data. The weaker "khipu as living document" version (cords added,
tied, removed after initial construction) is supported instead.

**What we learned:** khipu were maintained, not just manufactured. A living
document breaks any theory that assumes a single moment of creation. This
matters for the sparse working ledgers (Type 4) — the zeros may be blank
cells in an active file, not missing data.

### Garcilaso commodity-color mappings — UNTESTABLE / WEAK
Gold = yellow and silver = white cannot be tested: no surviving khipu
from gold or silver producing regions, tiny yellow-cord sample (n=9),
and tribute portability breaks the provenience logic. Red = soldiers
needs broadening to state presence generally. The 400-year-old hypothesis
survives only in its weakest form (colors encode something systematic).

**What we learned:** some hypotheses are structurally untestable with
surviving data, and saying so is a result. "Cannot be tested because no
khipu survive from gold regions" is more honest and more useful than a
weak correlation dressed up as a finding. Inconclusive is not failure.

### 1000588 restoration — UNVALIDATED
The arithmetic of the proposed restoration does not close. Dividers may
be category labels rather than structural elements. Do not cite as
a successful restoration.

**What we learned:** a restoration that does not close arithmetically is
not a restoration. The standard for "we fixed it" is that the numbers
work, not that the diagram looks plausible.

---

## Null and inconclusive results (reported, not buried)

- **Quechua syntax test:** value ordering and boundary marking both NULL.
  The postpositional-order claim rests on 70–75% subsidiary/parent color
  contrast with no permutation baseline yet — flagged as needing one.
  **Lesson:** a result without a null model is a description, not a test.
- **Hangman hypothesis:** letter cords are document-level formatting, not
  Quechua morphemes. Dead.
  **Lesson:** the simplest reading of a feature (formatting, not language)
  is usually right. Do not multiply linguistic entities.
- **Evidentiality test:** knot direction (Z/U/S) shows a three-way
  distinction, not the predicted binary marked/unmarked split. Z is
  neutral, U weakly enriched on marked cords, S disproportionately on
  unmarked white cords. The original hypothesis was misaimed.
  **Lesson:** when the data shows three categories and your theory predicts
  two, the theory is wrong, not the data. Do not collapse distinctions to
  save a hypothesis.
- **Direction test:** "repaired" in catalog notes means physical damage,
  not use-life additions. The test measured damage, not chronology.
  Inconclusive as designed, but informative: depth is a design feature,
  not a preservation accident.
  **Lesson:** read the field definitions before designing the test. A test
  built on a misunderstood variable measures the misunderstanding.
- **Inkawasi a=b+c equations:** published values unrecoverable from OKR
  — every Inkawasi long knot lacks NUM_TURNS. 41% of Inkawasi cords
  decode NULL under the type-aware decoder. Any quantitative Inkawasi
  claim from OKR alone is crippled.
  **Lesson:** know what your database cannot tell you. The OKR is a
  transcription of transcriptions; some published results came from
  physical inspection and cannot be replicated from the database alone.
  State the boundary instead of working around it silently.

---

## Solutions tried and abandoned

- **PENDANT_FROM as hierarchy indicator:** abandoned. The field is set on
  all cords including top level (verified 54/54 on Santa 1000270).
  CORD_LEVEL is the reliable hierarchy field. This corrects analyses
  built on PENDANT_FROM.
  **Lesson:** verify field semantics against known specimens before building
  on them. A field named for hierarchy that ignores hierarchy will
  corrupt every analysis that trusts the name.
- **Database CORD_ID as physical order:** abandoned. Physical order is
  CORD_ORDINAL, not CORD_ID.
  **Lesson:** database row order is not physical order. Obvious in
  retrospect; invisible until it breaks something.
- **Magic-number header frame:** revised. The primary cord carries
  allocation (length ~ pendant count), not type identity. Type lives
  in body structure. Reframed as pre-sized blank + structural template.
  **Lesson:** the data revises the metaphor, not the other way around.
  When the header does not identify the type, do not insist that it does —
  ask what it actually carries.
- **Two-bucket typology (census vs inventory):** abandoned. Missed the
  Bulk Tally type entirely (78 khipu) and misassigned 18 funerary khipu
  as inventory. Replaced by four-type document analysis.
  **Lesson:** a typology that cannot see a quarter of its corpus is not
  a simplification, it is a blind spot. The 78 unclassified khipu were
  the most informative specimens — they were the ones the old scheme
  could not describe.
- **"First new khipu" framing:** narrowed. Replicas exist; the claim is
  now "first khipu generated from a formal computational specification."
  **Lesson:** scope the novelty claim to what is actually novel. A broad
  "first" invites pedantic demolition; a narrow one is defensible.
- **"Formal grammar" framing:** narrowed to "document specification for
  Inca accounting khipu." R1–R3 subsequently confirmed as khipu-wide
  (funerary holds at 100%), but the document typology and generative
  spec remain accounting-scoped.
  **Lesson:** the right scope is the one the data supports, not the one
  that sounds most impressive. Narrowing a claim in response to evidence
  is not retreat — it is the work.

---

## Typology note: four document types vs six form types

Two different classifications operate at different levels. The **six form
types** (A–F: tally strip, flat register, simple list, grouped account,
hierarchical ledger, deep hierarchy) classify by architectural structure —
depth, pendant count, color count. The **four document types** (census
register, bulk tally, custodial warehouse ledger, sparse working ledger)
classify by inferred function, combining structure with value profiles,
color-group idioms, and published anchors (Santa, Inkawasi). Form is
observable; function is inferred. A single form type can serve multiple
document types and vice versa.

---

## Methodological caveats (acknowledged, not yet fixed)

1. **Multiple comparisons:** ~40 reports, dozens of tests, no correction.
   Core structural claims (R1–R3) rest on universal quantification, not
   p-values, and are unaffected. The interpretive layer (syntax tests,
   contrast claims) needs permutation baselines.
2. **Asymmetric failure attribution:** when R4/R6 fail, the data is blamed
   (stub records, misattributed IDs); when R1–R3 pass, structure is credited.
   Without pre-registered data-quality exclusions, any rule can survive this
   way. The honest fix is to define exclusion criteria before testing, not
   after inspecting failures. Not yet done.
3. **R1–R3 circularity risk:** the rules were derived from OKR data and
   tested on OKR data. The KFG out-of-sample test (n=66) and funerary test
   (n=22) are the independent evidence, and both samples are small. A larger
   independent corpus would strengthen this substantially.
4. **Pre-sized blank untested against size:** primary cord length correlates
   with pendant count (r=0.67), but more pendants mechanically need more cord.
   The allocation-metadata reading needs a test controlling for pendant count
   (e.g., residual length after regressing on count, compared across document
   types). Not yet done.
5. **Spreadsheet-model arithmetic scan:** 361/612 khipu (59%) show same-color
   arithmetic matches, reported without a null baseline. With mostly zero and
   small values, chance matches should be common. Needs a permutation test
   before any claim is made from it.
6. **Reproducibility:** hardcoded paths, gitignored database, no
   requirements file, 60+ one-off scripts. Pipeline is not runnable
   from a clean clone.
7. **Cluster stability:** six form types have silhouette scores and
   95.6% tree agreement but no bootstrap or alternate-k test.
8. **Site non-independence:** khipu from the same site/collection are
   not independent observations. KFG out-of-sample replication partially
   mitigates for structural rules; not addressed for interpretive claims.
