# Distributional Isomorphism Results

**Method:** per `isomorphism/README.md` 5-step join. Khipu features (170, 3,184 cords, `turns:*` excluded, 63 color-compound tautologies excluded) vs Quechua morphemes (216 total, 121 administrative incl. 13 military; 1,411 word-forms: 23 attested + 1,388 rule-generated templates, administrative/military roots 3x weighted).

**SCOPE ASSUMPTION (researcher constraint):** khipu were written by scribes for the administrative elite; the society was not broadly literate. The encoded vocabulary is assumed to be STATE vocabulary — tribute, census, storage, labor, military, religious administration. The Quechua side therefore weights the 121 administrative-domain morphemes heaviest: 1560/1608-attested roots in numbers, agriculture, animals, social organization, colors, materials, PLUS 13 military roots (auca/enemy, aucacona/warriors, atiy/to conquer, fuyuchak/captain, wach'i/arrow, champi/war club, pukara/fortress, etc., oldest attested forms used per the oldest-variant rule), and prefers Holguin's Cuzco court paradigms (formal administrative register). Candidate alignments are scored with an administrative boost (+1.0 when the Quechua side contains an administrative/military morpheme). This search targets state-administrative vocabulary alignment, NOT general Quechua. A null result here would not rule out alignment with everyday vocabulary — but everyday vocabulary is not expected in khipu.

**OLDEST-VARIANT RULE (researcher constraint):** for every Quechua root, the morpheme label uses the oldest attested FORM: 1560 Santo Tomas > 1608 Holguin > modern. The `oldest_form` and `form_src` columns in `quechua_morphemes.csv` record the variant and its provenance. Military roots use 1560/1608 forms as primary labels (e.g., `auca` not `awqa`, `auccay` not `awqay`). Where only a modern form exists, it is used but flagged 'lower confidence'. Rationale: khipu encode Inca-period Quechua; every century of language change moves the target.

**Join key:** distributional SHAPE = (promiscuity percentile rank a, promiscuity percentile rank b, PMI z-score). Nearest-neighbor matching, Euclidean distance < 0.22.

**Null test:** 500 iterations drawing random Quechua-like shapes from independent marginals (uniform pct ranks, empirical z distribution): mean 722.7 matches (sd 79.2) vs 1305 observed (z = 7.35).

> Observed matches exceed the permutation null at z = 7.35. Some signal above chance is present, but individual candidates still require human review.

## A. Mutually-exclusive set alignments (paradigmatic)

The strongest predicted shape: grammatical paradigms are mutually exclusive sets. Quechua evidentials (=mi/=si/=cha) never co-occur; khipu twist directions (dir:Es/dir:u) never co-occur.

- Quechua {-kuna, -qa}
- Quechua {=si, =cha, =mi, -chu}
- Quechua {-ta, -pi}

- Khipu {color:AB, color:YB}
- Khipu {level:L1, level:L2, level:L3}
- Khipu {color:W, color:?}
- Khipu {struct:pendant, struct:subsidiary, struct:header}
- Khipu {dir:Es, dir:u}
- Khipu {dir:SPu, dir:s}
- Khipu {dir:Ls, dir:Lu}

**Assessment:**

1. **Evidential paradigm -> twist-direction paradigm (STRONGEST CANDIDATE).**
   - Quechua: {=mi, =si, =cha} — 3-way mutually exclusive, clause-final, discourse-level (64/62/62 words).
   - Khipu: {dir:Es, dir:u} + {dir:Ls, dir:Lu} — 2-way mutually exclusive twist oppositions (192/579 and 396/296 cords).
   - Shape match: both are small closed paradigms (2-3 members), mid-promiscuity (combine with many partners but never each other), discourse-level function.
   - If true: twist direction encodes evidential/register information, NOT lexical content. Consistent with the independent finding that twist marks funerary vs non-funerary register (p=10^-16).
   - Caveat: paradigm SIZES differ (3 vs 2). The khipu side may conflate two Quechua categories, or the third member is unobserved in this corpus.

2. **Case paradigm -> color paradigm (SUGGESTIVE).**
   - Quechua: {-ta, -pa, -pi, -man, ...} — mutually exclusive, promiscuous (attach to any noun).
   - Khipu: {color:AB, color:YB, color:B, ...} — mutually exclusive as simple colors, highly promiscuous (AB: 626 cords/113 partners).
   - Shape match: large open paradigms, mutually exclusive within the set, high promiscuity = relational/attributive function.
   - If true: cord color functions like Quechua case — marking the grammatical RELATION of the cord's referent, not its identity. This reframes 'color = noun' as 'color = case role'.

## B. PMI-pair shape matches (ranked)

`admin` = Quechua side contains a state-administrative morpheme (+1.0 boost). Per the scope assumption, admin-flagged candidates are the priority for human review.

| # | Khipu pair | Quechua pair | kPMI | qPMI | shape_d | seq_valid | admin | qtype | score | assessment |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | axis:U + dir:SPu | -rqa + -n_agr | 4.89 | 4.16 | 0.044 | q | - | affix-affix | 1.052 | suggestive |
| 2 | dir:SPu + knot:SP | -rqa + -n_agr | 4.87 | 4.16 | 0.041 | q | - | affix-affix | 1.05 | suggestive |
| 3 | axis:U + knot:SP | -sqa + -yku_agr | 4.87 | 4.22 | 0.061 | q | - | affix-affix | 1.03 | suggestive |
| 4 | axis:U + knot:SP | -rqa + -n_agr | 4.87 | 4.16 | 0.059 | q | - | affix-affix | 1.013 | suggestive |
| 5 | axis:U + dir:SPu | -sqa + -yku_agr | 4.89 | 4.22 | 0.079 | q | - | affix-affix | 1.002 | suggestive |
| 6 | dir:SPu + knot:SP | -sqa + -yku_agr | 4.87 | 4.22 | 0.087 | q | - | affix-affix | 0.978 | suggestive |
| 7 | axis:U + dir:SPu | -chka + -n_agr | 4.89 | 4.38 | 0.13 | q | - | affix-affix | 0.953 | suggestive |
| 8 | axis:U + dir:SPu | -sqa + -ni | 4.89 | 4.34 | 0.123 | q | - | affix-affix | 0.953 | suggestive |
| 9 | axis:U + dir:SPu | -nqa + -ni | 4.89 | 4.38 | 0.132 | q | - | affix-affix | 0.951 | suggestive |
| 10 | axis:U + dir:SPu | -shaq + -ni | 4.89 | 4.38 | 0.133 | q | - | affix-affix | 0.948 | suggestive |
| 11 | axis:U + knot:SP | -sqa + -ni | 4.87 | 4.34 | 0.124 | q | - | affix-affix | 0.943 | suggestive |
| 12 | dir:SPu + knot:SP | -sqa + -ni | 4.87 | 4.34 | 0.139 | q | - | affix-affix | 0.913 | suggestive |
| 13 | dir:SPu + knot:SP | -nqa + -ni | 4.87 | 4.38 | 0.151 | q | - | affix-affix | 0.904 | suggestive |
| 14 | dir:SPu + knot:SP | -chka + -n_agr | 4.87 | 4.38 | 0.151 | q | - | affix-affix | 0.904 | suggestive |
| 15 | dir:SPu + knot:SP | -shaq + -ni | 4.87 | 4.38 | 0.152 | q | - | affix-affix | 0.902 | suggestive |
| 16 | axis:U + dir:SPu | -rqa + -yku_agr | 4.89 | 4.46 | 0.185 | q | - | affix-affix | 0.869 | suggestive |
| 17 | axis:U + knot:SP | -shaq + -ni | 4.87 | 4.38 | 0.168 | q | - | affix-affix | 0.869 | suggestive |
| 18 | axis:U + knot:SP | -nqa + -ni | 4.87 | 4.38 | 0.172 | q | - | affix-affix | 0.862 | suggestive |
| 19 | axis:U + knot:SP | -chka + -n_agr | 4.87 | 4.38 | 0.175 | q | - | affix-affix | 0.856 | suggestive |
| 20 | compound:B:GG + dir:Eu | -paq + -nku | 4.57 | 3.97 | 0.067 | q | - | affix-affix | 0.843 | suggestive |
| 21 | dir:SPu + knot:SP | -rqa + -yku_agr | 4.87 | 4.46 | 0.204 | q | - | affix-affix | 0.823 | suggestive |
| 22 | compound:B:GG + dir:Eu | -man + -nku | 4.57 | 3.95 | 0.074 | q | - | affix-affix | 0.821 | suggestive |
| 23 | compound:B:GG + dir:Eu | -paq + -nchis | 4.57 | 3.99 | 0.083 | q | - | affix-affix | 0.817 | suggestive |
| 24 | axis:U + knot:SP | -rqa + -yku_agr | 4.87 | 4.46 | 0.21 | q | - | affix-affix | 0.812 | suggestive |
| 25 | compound:B:GG + dir:Eu | -ta + -yku | 4.57 | 3.83 | 0.061 | q | - | affix-affix | 0.81 | suggestive |
| 26 | compound:B:GG + dir:Eu | -pa + -nchis | 4.57 | 3.95 | 0.087 | q | - | affix-affix | 0.796 | suggestive |
| 27 | compound:B:GG + dir:Eu | -manta + -n_poss | 4.57 | 3.95 | 0.091 | q | - | affix-affix | 0.787 | suggestive |
| 28 | dir:SPu + knot:SP | -paq + -nchis | 4.87 | 3.99 | 0.159 | q | - | affix-affix | 0.756 | suggestive |
| 29 | axis:U + dir:SPu | -paq + -nchis | 4.89 | 3.99 | 0.178 | q | - | affix-affix | 0.728 | suggestive |
| 30 | compound:B:GG + dir:Eu | -pa + -yki | 4.57 | 3.93 | 0.12 | q | - | affix-affix | 0.724 | suggestive |
| 31 | dir:SPu + knot:SP | -paq + -nku | 4.87 | 3.97 | 0.176 | q | - | affix-affix | 0.717 | suggestive |
| 32 | compound:B:GG + dir:Eu | -pi + -yki | 4.57 | 3.94 | 0.127 | q | - | affix-affix | 0.712 | suggestive |
| 33 | axis:U + dir:SPu | -paq + -nku | 4.89 | 3.97 | 0.194 | q | - | affix-affix | 0.69 | suggestive |
| 34 | dir:SPu + knot:SP | -pi + -yki | 4.87 | 3.94 | 0.19 | q | - | affix-affix | 0.679 | suggestive |
| 35 | dir:SPu + knot:SP | -pa + -yki | 4.87 | 3.93 | 0.192 | q | - | affix-affix | 0.671 | suggestive |
| 36 | dir:SPu + knot:SP | -pa + -nchis | 4.87 | 3.95 | 0.204 | q | - | affix-affix | 0.654 | suggestive |
| 37 | compound:B:GG + dir:Eu | -wan + -yku | 4.57 | 3.98 | 0.167 | q | - | affix-affix | 0.647 | suggestive |
| 38 | axis:U + dir:SPu | -pi + -yki | 4.89 | 3.94 | 0.21 | q | - | affix-affix | 0.646 | suggestive |
| 39 | dir:SPu + knot:SP | -man + -nku | 4.87 | 3.95 | 0.207 | q | - | affix-affix | 0.646 | suggestive |
| 40 | compound:B:GG + dir:Eu | -wan + -n_poss | 4.57 | 3.98 | 0.167 | q | - | affix-affix | 0.645 | suggestive |

**Note on `qtype`:** `affix-affix` pairs reflect real Quechua morphological constraints (suffix order, mutual exclusivity) and are valid for isomorphism. `root-involved` pairs are discounted (-2.0): the specific root-affix combinations are artifacts of deterministic template cycling, not linguistic facts.

## C. Interpretation guide

- **candidate**: shape match + sequential validation on both sides + score > 1. Worth human review for gloss assignment.
- **suggestive**: shape match without full validation, or lower score. May be chance (see null test).
- **weak**: shape match only, near the null expectation. Do not cite.

## D. What would falsify the 'writing conveys language' theory

- If the paradigmatic alignments (A.1, A.2) fail validation on larger corpora.
- If khipu PMI structure is fully explained by constructional tautology (level:L1 <-> struct:pendant) with no residual grammatical shape.
- If expanded Quechua natural-text corpora produce DIFFERENT shapes than the template-generated ones here (i.e., our Quechua side misrepresents usage).

## E. Limitations

1. Quechua side is 98% rule-generated templates, not natural text. Shapes reflect grammatical DESCRIPTION, not usage frequencies. Administrative weighting (3x templates, +1.0 score boost) implements the researcher's state-vocabulary constraint but does not create natural-text data.
2. Khipu corpus is 20 ANOMALOUS khipu (3,184 cords) — not representative of the full 593. Anomalous khipu may over-represent non-standard features.
3. `turns:*` excluded from khipu side; numerals have no Quechua counterpart here.
4. 63 color-compound tautological pairs excluded (constructional, not linguistic).
5. Permutation null shuffles shape assignments, preserving marginal distributions — a conservative null.
6. No khipu-to-Quechua gloss is proposed. These are structural candidates only.
7. The administrative scope assumption is a RESEARCHER CONSTRAINT, not a finding. If khipu encoded non-state vocabulary, this search is misaimed.
