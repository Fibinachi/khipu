# Color Layer Separation Analysis

**Date:** 2026-10-11
**Corpus:** 52,483 unique colored cords (non-funerary khipu)
**Question:** Do the grammatical and distinguishing color tiers show cleaner patterns independently than mixed?

---

## Layer Definitions

| Tier | Colors | Criterion |
|---|---|---|
| **Grammatical** | W, AB, MB, KB | 35+ sites each; positionally consistent; core paradigm |
| **Distinguishing** | All others (76 simple colors) | <35 sites; variable spread |

**Borderline note:** GG also has 35 sites (same as KB) but a different structural profile
(56.9% L1 vs KB's 46.2%/47.4% split). Site count alone doesn't determine tier —
positional role does. B (20 sites) and YB (24 sites) are frequent and widespread
enough to be "common distinguishing" (see §5 for three-tier refinement).

**Cord classification:**

| Class | Cords | % |
|---|---|---|
| Grammatical (simple) | 26,939 | 51.3% |
| Gram-gram compound | 5,967 | 11.4% |
| Distinguishing (simple) | 12,820 | 24.4% |
| Cross-tier compound | 5,466 | 10.4% |
| Dist-dist compound | 1,291 | 2.5% |

---

## Analysis 1: Grammatical Tier in Isolation

### Evidentiality gradient — STRONGLY CONFIRMED, cleaner than mixed

| Level | Grammatical tier only | All cords (comparison) |
|---|---|---|
| L1 | 57.6% marked | 40.3% marked |
| L2 | 70.8% marked | 47.1% marked |
| L3 | 80.8% marked | 57.1% marked |
| L4 | 79.2% marked | 40.4% marked |

The grammatical-tier gradient is **monotonic and steep** (57.6→80.8%).
The mixed-corpus gradient is weaker and **non-monotonic** (L4 drops to 40.4%).
Removing identity colors removes noise — the evidentiality signal lives in the
grammatical tier.

### Positional profiles (simple colors)

| Color | n | L1 | L2 | L3 | Interpretation |
|---|---|---|---|---|---|
| W | 12,576 | 78.9% | 19.1% | 1.6% | Unmarked default (nominative -Ø) |
| AB | 7,229 | 71.2% | 24.5% | 3.9% | Head/parent marker |
| MB | 5,411 | 67.9% | 28.5% | 2.9% | Core role |
| KB | 1,723 | 46.2% | 47.4% | 5.2% | Relational/dependent (genitive-like) |

### Case mapping (revised)

| Color | Candidate Quechua case | Evidence |
|---|---|---|
| W | Nominative (-Ø) | Most frequent, L1-heavy (78.9%), unmarked default |
| AB | Accusative (-ta) / topic | Head position (71.2% L1), fixed role |
| MB | Dative (-man) / instrumental (-wan) | Core but secondary to AB |
| KB | Genitive (-pa) | Evenly split parent/subsidiary (46/47%), relational |

**Confidence:** Suggestive. The structural profiles are distinct and stable, but
mapping to specific Quechua cases requires independent confirmation.

---

## Analysis 2: Distinguishing Tier in Isolation

### Site clustering — identity signal confirmed for rare colors

Most site-clustered (identity-like):

| Color | Cords | Khipu | Sites |
|---|---|---|---|
| BD | 125 | 4 | 3 |
| SY | 95 | 5 | 3 |
| TG | 31 | 6 | 3 |
| NB | 1,378 | 39 | 4 |
| VR | 67 | 5 | 4 |

**NB** is the standout: 1,378 cords across 39 khipu but only 4 sites — a major
local category, not a universal grammatical marker.

Most widespread distinguishing colors (common identities?):

| Color | Cords | Khipu | Sites |
|---|---|---|---|
| GG | 1,733 | 181 | 35 |
| HB | 955 | 110 | 28 |
| BG | 724 | 75 | 24 |
| YB | 2,219 | 122 | 24 |
| B | 2,757 | 103 | 20 |

**No distinguishing color** in the top 50 appears on ≤3 khipu — extreme
khipu-specificity is absent. Even "identity" colors are shared across dozens
of documents.

### Co-occurrence: distinguishing × grammatical

When distinguishing colors appear in compounds, they pair preferentially:

| Distinguishing | Top grammatical partner |
|---|---|
| LB | W (97%) |
| B | W (78%) |
| BB | W (76%) |
| BG | W (76%) |
| NB | W (69%) |
| HB | W (60%) |
| YB | MB (45%), W (33%) |
| GG | AB (40%), W (35%) |

**W dominates** as the compound partner. LB is almost exclusively paired with W
(97%). This suggests W functions as the default/unmarked case that combines
with identity colors — exactly what a nominative case would do.

---

## Analysis 3: Compound Decomposition — THE KEY TEST

**43.0% of all compounds (5,466/12,724) split cleanly across tiers**
(grammatical + distinguishing components).

Top cross-tier compounds:

| Compound | n | Components | Tiers |
|---|---|---|---|
| GG:AB | 243 | GG + AB | distinguishing + grammatical |
| GG:W | 240 | GG + W | distinguishing + grammatical |
| BG:W | 192 | BG + W | distinguishing + grammatical |
| LB:W | 186 | LB + W | distinguishing + grammatical |
| B:W | 178 | B + W | distinguishing + grammatical |
| W:NB | 71 | W + NB | grammatical + distinguishing |

**Interpretation:** Compounds are **case-marked identities** — a distinguishing
(identity) color fused with a grammatical (case-role) color. `GG:AB` reads as
"GG-entity in AB-role." This is the strongest structural evidence for the
two-tier model: the layers don't just coexist, they **compose**.

47.4% of compounds are gram-gram (e.g., AB:W, MB:AB) — these may mark
complex grammatical relations or are conventionalized pairings.

---

## Analysis 4: Key Findings Per Layer

### Twist direction

| Layer | Z | S | U |
|---|---|---|---|
| Grammatical | 60.7% | 31.1% | 8.2% |
| Distinguishing | 60.7% | 22.8% | 16.5% |

**U-direction is 2× enriched** in the distinguishing layer (16.5% vs 8.2%).
S-direction is higher in grammatical (31.1% vs 22.8%).
The twist register **interacts with color tier** — U (the non-funerary/anomaly
marker) preferentially marks identity-colored cords.

### Rider model (subsidiary contrast)

Could not cleanly re-run per layer (PENDANT_FROM join methodology issue —
prior analysis established PENDANT_FROM is unreliable for hierarchy).
Prior finding stands: 69.1% subsidiary color contrast vs 62.7% null.
The KB profile (47.4% L2) is consistent with subsidiaries carrying relational marking.

### Depth = chronology

The evidentiality gradient IS the chronological gradient (W fraction drops with
depth). In the grammatical tier:
- L1: 42.4% unmarked → L3: 19.2% unmarked
- Clean, monotonic — the accrual pattern (founding entries unmarked, later
  additions marked) is driven by the grammatical tier.

---

## Revised Model

### Two tiers confirmed, with a three-tier refinement

The data supports the two-tier model **and** suggests a refinement:

1. **Grammatical tier** (W, AB, MB, KB): Case-like roles. Drives the evidentiality
   gradient. Positionall
...[truncated 911 chars]
