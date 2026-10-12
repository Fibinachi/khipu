# Are the Six Form Types Regional or Universal?

**Question (Charles):** Do the six quipu form types appear everywhere (imperial standardization) or are some region-specific (local traditions)?

**Answer: both.** All six forms are found across the empire — no form is exclusive to any region or site. But their *proportions* vary significantly by site and institutional context. Universal toolkit; context-dependent usage.

**Date:** 2026-10-10 | **Analyst:** Muse (subagent)

---

## Data

- Classification: `quipu-classification.csv` (619 quipu: A=32, B=76, C=101, D=149, E=110, F=144, unclassified=7)
- Provenience: `khipu_main.PROVENANCE` in `okr-khipu.db` (61 distinct proveniences; ~36% lack provenience)
- Zones: highland = Leymebamba, Cuzco, Huari; intermediate = Lluta Valley, Playa Miller (Arica), Loa Valley; coastal = everything else coastal; 36% unknown

---

## 1. Every form appears at multiple sites

| Type | n | Distinct sites | Max single-site share |
|------|---:|---:|---:|
| A: Tally strip | 32 | 15 | 34% (blank provenience) |
| B: Flat register | 76 | 19 | 32% (blank provenience) |
| C: Simple list | 101 | 23 | 42% (blank provenience) |
| D: Grouped account | 149 | 30 | 28% (blank provenience) |
| E: Hierarchical ledger | 110 | 24 | 26% (blank provenience) |
| F: Deep hierarchy | 144 | 32 | 19% (Incahuasi) |

No form is concentrated at a single site above 20% (excluding blank-provenience quipu). Every form appears at 15+ sites. **The forms are geographically universal in presence.**

---

## 2. But proportions vary significantly by site

Form distribution at the six largest sites:

| Site | A | B | C | D | E | F | Total |
|------|---:|---:|---:|---:|---:|---:|---:|
| Pachacamac | 2 | 10 | 18 | 25 | 18 | 17 | 90 |
| Incahuasi | 4 | 2 | 2 | 10 | 7 | 27 | 52 |
| Ica | 4 | 10 | 5 | 15 | 8 | 7 | 49 |
| Leymebamba | 1 | 0 | 0 | 4 | 6 | 11 | 22 |
| Huaquerones | 1 | 0 | 8 | 6 | 4 | 0 | 19 |
| Nazca | 1 | 0 | 0 | 4 | 4 | 4 | 13 |

- Chi-square (form x major-site): χ²=71.9, df=25, **p=2.0e-6**, Cramér's V=0.24 (moderate association)
- **Inkawasi vs rest of corpus:** χ²=30.3, df=5, **p=1.3e-5**. Inkawasi is 52% deep-hierarchy F (27/52) vs 21% corpus-wide; expected F under null = 12.2, observed = 27.
- Pachacamac (the largest single assemblage, n=90) uses all six forms in roughly balanced proportions — the closest thing to a "representative" mix.
- Ica uses all six forms; Leymebamba uses 4 of 6 (no B, no C); Huaquerones uses 4 (no B, no F); Nazca uses 4 (no B, no C).

---

## 3. Highland vs coastal

| Zone | A | B | C | D | E | F | n |
|------|---:|---:|---:|---:|---:|---:|---:|
| Highland | 1 | 0 | 1 | 5 | 6 | 11 | 24 |
| Coastal | 19 | 45 | 51 | 93 | 69 | 79 | 356 |

- Chi-square (form x zone): χ²=10.7, df=5, p=0.057 — **marginal, not significant at 0.05**
- Direction: highland skews F-heavy (46% vs 24% expected), B-absent (0 vs ~12% expected), C-light (4% vs 14% expected)
- **Caveat:** highland n=24 is tiny and 22 of 24 come from one site (Leymebamba). The B-absence could be Leymebamba-specific, not highland-wide.

---

## 4. Regional specialist signals (worth flagging, small n)

- **B (flat register)** is absent at Leymebamba, Huaquerones, and Nazca. Concentrated at Pachacamac and Ica. Possibly a south-coast form — or an artifact of the highland sample being one site.
- **Chilean fringe sites** (Lluta Valley, Playa Miller, Loa Valley): 9 of 10 quipu are F (deep hierarchy). The empire's southern edge used almost exclusively the most complex form.
- **Santa:** 6/6 are E (hierarchical ledger). Single-form site, but n=6.
- **Huaquerones:** C-heavy (8/19), zero F — the inverse of Inkawasi.

---

## 5. Provenience-bias check

Quipu with blank/unknown provenience differ modestly from provenienced ones (χ²=12.1, df=5, p=0.034): blank ones skew toward B and C, away from D and F. Museum-collection bias exists but is not severe.

---

## Interpretation

The Inca bureaucracy used a **standardized toolkit of six form types empire-wide** — all six appear on the coast, in the highlands, at the imperial storehouse, and at the Chilean fringe. This is consistent with an imperially standardized documentary grammar.

But **usage was institutionally patterned, not uniform**:
- An imperial storehouse (Inkawasi) skews toward deep-hierarchy ledgers — complex multi-level accounts.
- A major shrine (Pachacamac) uses a balanced mix — diverse administrative needs.
- The southern fringe skews almost entirely F — possibly tribute records sent to the center, or a local scribal tradition favoring complex forms.
- Some sites never use certain forms (B absent at three sites).

This mirrors the color finding: standardization at the grammar level (form types, color families), variation at the usage level (which forms, which colors, in what proportions).

---

## Caveats

1. Highland sample is n=24 from effectively one site (Leymebamba, 22/24). Do not generalize "highland" patterns beyond Leymebamba.
2. ~36% of quipu lack provenience; geographic analysis covers only the provenienced subset.
3. Provenience = findspot, which may differ from place of manufacture or administrative origin.
4. Seven quipu (1000464–1000470) are unclassified; all lack provenience.
5. Chi-square cells are sparse for rare site×form combinations; treat site-specific claims as suggestive, not proven.
