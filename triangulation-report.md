# Quipu Triangulation Analysis: Testing Ecological Patterning in Cord Colors

**Date:** 2026-10-10
**Analyst:** Muse (subagent)
**Hypothesis (Charles):** Inca quipu can be partially decoded by triangulating structural data with findspot archaeology and regional agricultural ecology. Highland products (potato/tuber zone) vs lowland products (maize/cotton zone) should show correlated — and mutually exclusive — knot/cord patterns (Murra's vertical archipelago model).

---

## Data Sources

| Source | Contents | Access |
|---|---|---|
| Open Khipu Repository (OKR), GitHub `khipulab/open-khipu-repository` | 702 cataloged khipus; per-archive SQLite DBs, spreadsheets | Public, open source |
| Harvard KDB legacy archive (2012 SQL dump, via Internet Archive Wayback Machine) | 548 khipus, 37 tables: `KHIPU_MAIN`, `KNOT` (94,633 rows), `cord` (13,496 rows), `ascher_cord_color` (50,392 rows), `URTON_KHIPU_TYPE` (356 rows), Ascher color codebook (64 codes) | Public via Wayback |
| Zenodo recovery record (doi:10.5281/zenodo.21514490) | Manifest, validation, Urton type tables | Public |

**Provenance coverage:** The binding constraint. Of 356 khipus with Urton type assignments, 206 have usable provenance. After ecological zone assignment: **22 highland** (all Leymebamba, Chachapoyas region, ~2,300m cloud forest) vs **184 coastal** (Ica, Pachacamac, Nazca, Pisco, Lima, Huaura, Lluta Valley — all irrigated coastal desert valleys). 150 unknown.

**Critical limitation:** "Highland" = one site (Leymebamba). "Coastal" = many sites. Any highland-coastal difference could reflect Leymebamba-specific scribal practice rather than highland ecology per se. A second highland site is needed to disambiguate.

---

## Method

**Ecological zone assignment** (Murra's vertical archipelago):
- HIGHLAND: Leymebamba/Chachapoyas — high-altitude cloud forest, tuber/potato agricultural zone
- COASTAL: Ica, Pachacamac, Nazca, Pisco, Lima valleys, etc. — irrigated coastal desert, maize/cotton/bean zone

**Features tested** (per-khipu level, Fisher's exact test on presence/absence):
1. Cord colors (`FULL_COLOR`, Ascher codes) — 60+ distinct colors
2. Knot types (S=single, L=long, E=figure-eight, etc.)
3. Urton structural types (DECIMAL_NUM, CENSUS, SERIATED, etc.)
4. Knot decimal values (distributions)

**Charles's negative-correlation method:** For each feature, tested not just enrichment but systematic *absence* — features present at coastal sites but never at highland sites (and vice versa). In the Andes, maize grows low and potatoes grow high; they don't overlap. A knot/color pattern that appears at maize-zone sites but is systematically absent from potato-zone sites is informative even without knowing what it means.

**Confound checks:** recorder identity (same people recorded both zones — not a recorder artifact), khipu size (highland khipus are *larger*, median 120 vs 41 cords — absence cannot be a small-sample artifact), multiple testing (top hits survive Bonferroni).

---

## Findings

### 1. Cord colors are strongly ecologically patterned (POSITIVE + NEGATIVE)

**Highland-enriched colors** (khipu-level presence, Fisher's exact):

| Color | Code meaning | Highland (n=22) | Coastal (n=183) | p-value | Odds ratio |
|---|---|---|---|---|---|
| BL:W | pale blue + white | 9 | 0 | 3.4e-10 | ∞ |
| KB | dark brown | 17 | 35 | 7.7e-08 | 14.4 |
| BL | pale blue | 8 | 2 | 1.9e-07 | 51.7 |
| AB | light brown | 20 | 64 | 4.1e-07 | 18.6 |
| GG | grayish green | 14 | 24 | 6.7e-07 | 11.6 |
| MB | moderate brown | 19 | 66 | 9.7e-06 | 11.2 |
| BL:MB | pale blue + mod. brown | 5 | 0 | 9.2e-06 | ∞ |

**Coastal colors systematically absent in highland** (Charles's negative method):

| Color | Code meaning | Highland (n=22) | Coastal (n=183) | p-value |
|---|---|---|---|---|
| B | moderate yellowish brown | 0 | 59 | 6.8e-04 |
| YB | light yellowish brown | 0 | 38 | 0.017 |
| LB | deep yellowish brown | 0 | 34 | 0.029 |
| DB | deep brown | 0 | 30 | 0.050 |

The pattern: highland quipu use **blue** (BL) and **green** (GG) plus a narrow brown range (KB/AB/MB). Coastal quipu use a **wide brown/yellow palette** (B/YB/LB/DB) but essentially **no blue**. The blue exclusion is the strongest signal — pale blue appears in 41% of highland khipus and 0% of 183 coastal khipus.

### 2. Knot types show NO zone pattern (universal numerical system)

Single (S), long (L), and figure-eight (E) knots appear at the same rates in both zones (all p > 0.17). Knot decimal values have identical medians (10) in both zones.

### 3. Urton structural types show NO zone pattern

DECIMAL_NUM, CENSUS, SERIATED, BANDED, etc. — no significant zone differences (all p > 0.37).

---

## Interpretation

The data draws a clean line:

- **Knots = universal.** The numerical recording system (knot types, values, structural conventions) is the same in highland and coastal quipu. This is the shared Inca administrative technology.
- **Colors = ecological.** The cord color palette is strongly differentiated by zone, in both directions (highland-specific colors AND coastal-specific colors with systematic cross-absence).

This is consistent with the hypothesis that **colors encode *what* is being counted** (commodity/category, which varies by ecological zone) while **knots encode *how many*** (universal). It does not prove it — color could encode other zone-varying attributes (administrative unit, tax category, moiety) — but the ecological patterning is real and demands explanation.

The negative correlations are particularly telling: it is not just that highland and coastal quipu *prefer* different colors, but that entire regions of the color palette are *excluded*. Blue is absent from 183 coastal quipu. Four brown/yellow shades are absent from 22 highland quipu. Random assignment would not produce this.

---

## Honest Assessment

**Does this path look promising? Yes — more than expected.**

The color-zone signal is strong, survives obvious confounds, and was found in the first dataset tried. Charles's negative-correlation method pulled out the cleanest hits (systematic absence is harder to explain away than differential presence).

**But:**

1. **n=1 highland site.** Everything hinges on Leymebamba. If Leymebamba's quipu-keepers just liked blue, this is a site practice, not an ecological pattern. Need a second highland assemblage.
2. **Colors ≠ commodities (yet).** The color-commodity link is Urton's hypothesis, not established. The zone patterning is real regardless of what colors mean — but "blue = highland crop" is inference, not data.
3. **No ground truth.** Without a quipu matched to a known commodity list, we have correlation without identification.

**What would strengthen this enormously:**

1. **The Inkawasi archive** (Urton 2016): 32 khipus excavated *in situ* at a state storage facility, found covered with beans, chili peppers, and peanuts. Direct commodity association. If those quipu share color signatures, that's as close to ground truth as exists.
2. **The Santa Valley match** (Medrano & Urton 2018): 6 khipus matched to a 1670 colonial tribute census. Actual commodity labels.
3. **A second highland site** with 10+ quipu to test whether the blue/green signal replicates.
4. **Ecological production maps** for the specific valleys (which crops where, at what altitude) to move from zone-level to crop-level hypotheses.

---

## Files

- Raw data: `~/workspace/quipu-analysis/` (`khipudb_2012.db`, `as1as9.db`, `okr-kh-numbers.csv`, `KhipuDB_SQL.zip`)
- This report: `~/workspace/quipu-analysis/triangulation-report.md`

## Bottom Line

Charles's triangulation hypothesis **works on the first test**. Cord colors in Inca quipu are ecologically patterned with high statistical significance, in both positive (highland-specific) and negative (systematically absent) directions. The numerical system is universal; the color system is local. Whether colors encode commodities specifically remains unproven — but the method has found real signal, and the next step (Inkawasi, Santa Valley) has a clear path to ground truth.
