# Inkawasi Test: Coastal Exclusion Prediction

**Date:** 2026-10-10
**Question:** Do the Inkawasi quipu (coastal Inca state storehouse, Cañete Valley) lack blue/green cord colors as our coastal-exclusion pattern predicts?

## Short answer

**No — the strong exclusion claim does not survive.** 9 of 52 Inkawasi khipus (17%) have blue-family cords. But Inkawasi sits *between* the highland and other-coastal patterns, not on top of either. The picture is more complicated than "blue = highland."

## Data source

The Inkawasi cord-level color data was **not** in the 2012 Harvard KDB snapshot (excavations were 2013–14). It **is** in the current Open Khipu Repository:

- **52 khipus** with provenance "Incahuasi" (Proyecto Arqueologico Incahuasi = Chu's excavation project)
- **5,904 cord color records** in `ascher_cord_color`
- Database: OKR `khipu.db` (downloaded 2026-10-10, saved locally as `~/workspace/quipu-analysis/okr-khipu.db`)
- Note: OKR catalog assigns these KH0491–KH0509 (issued Feb 2024), but cord data is stored under numeric IDs 1000595–1000647

The Urton & Chu (2015) paper itself does **not** publish cord-by-cord color data. It mentions color patterning only in passing ("the colors or color patterns of the matching samples coincide as well") and explicitly prioritizes numerical over color matching. The color data exists only in the OKR database.

## Results

### Khipu-level color presence

| Color | Leymebamba highland (n=22) | Other coastal (n=183) | Inkawasi coastal (n=52) |
|-------|---------------------------|----------------------|------------------------|
| Blue family (BL/BG/GL) | 9/22 = 40.9% | 0/183 = 0% | 9/52 = 17.3% |
| Grayish green (GG) | 14/22 = 63.6% | 24/183 = 13.1% | 12/52 = 23.1% |
| Dark brown (KB) | 17/22 = 77.3% | 35/183 = 19.1% | 29/52 = 55.8% |

### Statistical tests (Fisher's exact)

- Inkawasi vs other-coastal (blue): **p = 7.1e-07** — Inkawasi has significantly MORE blue
- Inkawasi vs highland (blue): **p = 0.041** — Inkawasi has significantly LESS blue

Inkawasi is statistically distinct from both groups. It is intermediate.

### Cord-level detail

- 50 blue-family cord records across 9 khipus: BL (pale blue, 18), GL (moderate greenish blue, 27), BG (grayish blue, 5)
- Blue cords are on pendant cords (49/50), not primary cords — normal for data-bearing cords
- Operators: mostly mottled (:) or plain; one barber-pole (-)
- GG (grayish green): 105 cords across 12 khipus
- Dominant Inkawasi colors overall: AB (light brown, 1,657), W (white, 1,307), NB (1,019), MB (moderate brown, 755)

## Interpretation

Three possible explanations for the intermediate pattern:

### 1. Imperial site vs local sites (favored)

Inkawasi was an **Inca state installation** — a military garrison and storage facility built for imperial expansion. The other 183 coastal khipus come from diverse (mostly non-imperial) contexts: burials, local settlements, pilgrimage centers.

An imperial facility might use an **imperial-standard palette** that draws from a wider range of colors than local coastal practice. The khipukamayocs at Inkawasi were state functionaries, potentially trained in Cuzco and deployed to the coast. Their color vocabulary might reflect imperial convention, not local coastal convention.

This doesn't falsify the ecological pattern — it *refines* it. The claim becomes: "local coastal khipu practice excludes blue; imperial administrative practice does not."

### 2. Commodity encoding

The Inkawasi khipus were found in direct association with specific products:
- Aji (chili peppers): kallanka U.A. 7 (UR267A/UR267B)
- Peanuts: kallanka U.A. 4, 14 khipus (UR266, UR268, UR269, UR270, UR272 + others)
- Black beans: kallanka U.A. 5 (1 khipu)
- Maize: corridor deposits

If cord colors encode **commodity** (not ecology), a multi-commodity storehouse would naturally show a mixed palette. The blue cords might mark a specific product. **We cannot test this** because the OKR does not record which khipu was found with which product — that association exists only in the excavation records / Chu's field notes.

This is the most important follow-up: **linking specific khipu IDs to their findspot commodity associations** would let us test whether blue = a specific product.

### 3. The original exclusion was overstated

The 0/183 figure came from the 2012 KDB snapshot. That snapshot may have sampling biases (which coastal sites were included, recording completeness). The Inkawasi data is newer, more systematically recorded, and from a controlled excavation. It's possible the "clean" exclusion was partly an artifact of the older dataset.

However: p = 7.1e-07 for Inkawasi vs other-coastal is a very strong difference. Even if the original 0% was slightly understated, Inkawasi is genuinely different from the bulk coastal sample.

## What this means for the hypothesis

| Original claim | Status after Inkawasi |
|---|---|
| "Blue is absent from coastal khipus" | **Falsified** in strong form. Blue present at 17% of Inkawasi khipus. |
| "Blue is more common in highland khipus" | **Holds.** 41% highland vs 17% Inkawasi vs 0% other-coastal. Gradient is real. |
| "Cord colors are ecologically patterned" | **Refined.** Pattern exists but interacts with institutional context (imperial vs local). |
| "Knots = universal, colors = what" | **Untested by this data.** Still the best working model. |

## What's needed

1. **Khipu-to-commodity mapping for Inkawasi.** The excavation records (Chu's field notes, or a subsequent publication) should specify which khipu was found with which product. This would let us test the commodity-encoding hypothesis directly — the single most informative follow-up.

2. **Contact with Urton/Chu.** The color data is in the OKR, but the findspot associations are not. An email to Gary Urton (Harvard) or Alejandro Chu (Proyecto Arqueológico Incahuasi) requesting the khipu-to-context mapping would unlock the commodity test.

3. **More imperial vs local comparisons.** Are there other imperial installations with khipu archives? If imperial sites consistently show wider palettes than local sites, the institutional explanation is confirmed.

4. **Check the Pachacamac khipus.** Eeckhout (2012) excavated 9 khipus from a coastal storage structure at Pachacamac but couldn't open them. If those become available, they'd be another imperial-coastal test case.

## Bottom line

The Inkawasi test **complicates but does not kill** the color-ecology hypothesis. The strong exclusion claim ("no blue on the coast") is wrong. But the gradient (highland > imperial-coastal > local-coastal) is real and statistically robust. The most likely explanation is that **institutional context** (imperial vs local) mediates the ecological pattern — and the commodity-encoding hypothesis remains untested but promising.

This is how science is supposed to work: the prediction was specific enough to be falsified, and the falsification points to a more interesting question.
