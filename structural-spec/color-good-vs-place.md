# Color Encodes Good's Origin, Not Good's Identity or Recording Site

**Date:** 2026-10-10
**Question:** Does quipu cord color describe the specific good being recorded, or the place it comes from?

## The Three Hypotheses

| Hypothesis | Prediction |
|---|---|
| **H1: Color = good identity** | Each commodity has a distinct, consistent palette. All peanut quipu share "peanut colors." |
| **H2: Color = recording site** | All quipu at Inkawasi (coastal) use coastal palette, regardless of commodity. |
| **H3: Color = good's ecological origin** | Lowland goods use coastal palette; highland goods use highland colors — regardless of where the quipu was made. |

## Test 1: Same Site, Different Goods (Inkawasi)

All ten commodity-associated quipu are from Inkawasi (coastal site, ~300m elevation).

### Black beans (1000613) — highland crop
| Color | Cords | % |
|---|---|---|
| GG-YB | 33 | 35.5% |
| KB-W | 26 | 28.0% |
| YB | 10 | 10.8% |
| 0R | 7 | 7.5% |

**35.5% grayish green — unique among all 52 Inkawasi quipu** (next highest: 8.7%).

### Chili peppers (1000608, 1000609) — lowland crop
**1000608:** W (52), AB (22), AB-MB (12)
**1000609:** W (70), AB (30), MB (14), AB-MB (9)

Plain white + light brown. No GG. No distinctive "chili color."

### Chili peppers, inferred (1000597, 1000598) — lowland crop
**1000597:** AB (84), MB (2)
**1000598:** AB (136), MB (33)

AB-dominated. **Notably different from 1000608/1000609** despite recording the same commodity.

### Peanuts (1000607, 1000610, 1000611, 1000612, 1000614) — lowland crop
**1000607:** YB (53), W (25), HB (23), MB-KB (15) — YB-led, diverse
**1000610:** NB (34), W (33), W-MB (26), MB (23), AB (22) — mixed
**1000611:** NB (95), W (80), AB (60), MB (40) — NB-led
**1000612:** W (173), NB (113), KB (34) — W-dominant
**1000614:** W (196), AB (63), MB-W (24), YB (14) — W-dominant

**Five quipu, five different palettes.** All within the coastal brown/white/yellow family, but no shared "peanut color."

### Test 1 Verdict

| Hypothesis | Result |
|---|---|
| H1 (color = good) | **FALSIFIED.** Five peanut quipu use five different palettes. Two chili pairs (1000608/9 vs 1000597/8) use different palettes for the same commodity. |
| H2 (color = site) | **FALSIFIED.** Bean quipu (1000613) uses highland GG at a coastal site. If color followed the recording site, it would use coastal palette like the others. |
| H3 (color = origin) | **SUPPORTED.** Lowland goods (peanuts, chili) → coastal palette (W, AB, NB, YB, MB). Highland goods (beans) → highland color (GG). |

## Test 2: Highland Site, Highland Goods (Leymebamba)

22 Leymebamba quipu (highland site, ~2800m). Sample color distributions:

| Quipu | Top colors | BL? | GG? |
|---|---|---|---|
| 1000002 | AB, W, BL(5), GG(3) | Yes | Yes |
| 1000004 | W, AB, GG(18) | No | Yes |
| 1000007 | W, KB, MB, AB, BL(35), GG(22) | Yes | Yes |
| 1000009 | AB, MB, KB, W, BL(10) | Yes | No |

Highland quipu use BL and GG alongside browns. This is consistent with H3 (highland goods → highland colors) but does not discriminate between hypotheses — both H2 and H3 predict highland colors at a highland site.

## Test 3: Other Commodity Contexts

Searched OKR `khipu_main.NOTES` for commodity mentions (bean, peanut, chili, aji, maize, corn, potato). Only Inkawasi quipu returned commodity associations:
- 1000608: "Nickname: Khipu del Aji" (Chili Khipu)
- 1000609: "Nickname: Khipu del Aji"

No other excavated quipu in the database have associated goods. Test 3 cannot be extended beyond Inkawasi with current data.

## The Critical Case: The Bean Quipu Disambiguates

**1000613 (UR271)** is the single most informative quipu in the color debate:

| Attribute | Value |
|---|---|
| Recording site | Inkawasi — coastal (~300m) |
| Associated good | Black beans (*Phaseolus vulgaris*) — highland/mid-altitude crop |
| Distinctive color | GG (grayish green) — 35.5% of cords |
| GG at Inkawasi | Unique — next highest quipu is 8.7% |
| GG corpus-wide | Highland-associated (p=6.7e-07, zone-validation.md) |

**Logic:**
- If color = recording site (H2): bean quipu should use coastal palette. **It doesn't.**
- If color = good identity (H1): cannot be tested with n=1, but the peanut/chili data already falsifies H1.
- If color = good's origin (H3): highland crop → highland color, despite coastal recording site. **Confirmed.**

The bean quipu breaks the recording-site hypothesis. The color follows the good's ecological origin, not where the quipu was tied.

## Refined Model: Two-Level Color Encoding

The data support a two-level model:

### Level 1: Color FAMILY = ecological zone of the good's origin
- Coastal/lowland goods → brown/white/yellow family (W, AB, MB, NB, YB, KB)
- Highland goods → blue/green family (BL, GG)
- This is the **content** signal — it tells you where the thing came from.

### Level 2: Specific PALETTE = production variation
- The five peanut quipu share the coastal family but differ in dominant color
- This is **not** content — it's who made it, when, with what string batch
- Same room, same peanuts, five different palettes = five production events

### Why this explains the coastal BL anomalies
Coastal BL at Pachacamac, Inkawasi, Armatambo (zone-validation.md) now makes sense:
- These are imperial/state centers handling goods from across the empire
- Highland goods arriving at a coastal storehouse retain their highland color coding
- OR: state-level records use highland-associated colors as an administrative marker
- Either way, BL marks highland origin or state context — not the recording site's geography

## What This Does NOT Explain

1. **The specific palette variation** among the five peanut quipu. We attribute this to production (different makers/batches), but cannot rule out other encodings (tribute source, time period, peanut variety).

2. **Whether GG on the bean quipu is the good's origin or something else.** The convergence of botanical fact (beans = highland crop), statistical fact (GG = highland-associated, p=6.7e-07), and empirical fact (unique GG at Inkawasi) is strong, but n=1 for beans.

3. **Color combinations.** Many cords use two colors (e.g., GG-YB, KB-W). The combinatorial logic is unresolved.

## Bottom Line

**Color does not identify the commodity.** Five peanut quipu, five palettes — there is no "peanut color."

**Color does not follow the recording site.** The bean quipu uses highland GG at coastal Inkawasi.

**Color encodes the ecological zone of the good's origin.** Lowland goods → coastal palette. Highland goods → highland colors. The quipu records where the thing came from, not what it is or where the record was made.

This is consistent with an imperial tribute system: goods flow from diverse ecological zones to central storehouses, and the color coding preserves the origin information through the accounting chain.

---

*Analysis by subagent, 2026-10-10. Data: okr-khipu.db, urton-chu-2015-extraction.md, zone-validation.md, peanut-colors.md.*
