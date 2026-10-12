# Santa Valley Census Encoding Schema ("Rosetta" Quipus)

**Date:** 2026-10-10
**Sources:** Medrano & Urton (2018), *Ethnohistory* 65(1):1–23; FitzPatrick (2024), *Ethnohistory* 71(4):443–469; Urton (2017), *Inka History in Knots*, ch. 9; FitzPatrick (2025), khipufieldguide.ghost.io; Contreras (2026), arxiv:2607.00185; Wikipedia "Santa Valley quipus"; Google Arts & Culture "Khipus and Written Documents"; direct OKR database analysis (this report).

**The six quipus:** Museo Temple Radicati, Lima (Radicati collection). Harvard numbers UR087–UR092; OKR KH0323–KH0328; our database IDs 1000270–1000275. Mid-colonial, radiocarbon dated ~1608–1640 (pre-dating the 1670 revisita — possibly reused or recording an earlier tribute round).

**The matching document:** 1670 Spanish *revisita* (census) of San Pedro de Corongo, Santa Valley. Lists 132 named tributaries in six *pachacas* (lineage groups). Published in Zevallos Quiñones (1991), "Padrón de Indios Tributarios Recuayes: Conchucos 1670." The revisita explicitly orders the tribute to be "put into khipu(s)" (*lo ponga por quipo*).

---

## 1. Document-Level Structure

| Feature | Value | Source |
|---|---|---|
| Total cords | 804 (133 six-cord groups) | Medrano & Urton 2018 |
| Tributaries in revisita | 132 named individuals | Zevallos Quiñones 1991 |
| Six *pachacas* | Namus (18), Corongo (23), Cuyuchin (9), Cusca (7), Guauyan (41), Ucore (32) | FitzPatrick 2024 |
| Total tribute (revisita) | 367 *pesos* | Urton 2017 |
| Total tribute (khipu, 1st-cord sums) | ~367 *pesos* (close match) | Urton 2017 |

The 133rd six-cord group (one more than 132 tributaries) is unexplained — possibly a summary, header, or blank.

## 2. The Six-Cord Person Record

Each tributary is encoded as a **block of 6 pendant cords sharing one color**. The color identifies the individual (see §3). Within each block, cord positions 1–6 carry different fields.

### Cord-to-field mapping

| Position | Field (published) | Field (inferred from OKR data) | Encoding method | Confidence |
|---|---|---|---|---|
| 1 | **Tribute amount** (assessed) | Constant within 4/6 quipu (values 9, 4, 5, 4); varies on 2 R-heavy quipu | Knot value (decimal). Sum across blocks ≈ 367 pesos total | **High** (published) |
| 2 | *Not specified in literature* | Varies per block (L-knots, 2–9 turns); has subsidiaries | Knot value + detail cords | Medium (structural) |
| 3 | *Not specified* | Varies per block; most subsidiaries attach here | Knot value + detail cords | Medium (structural) |
| 4 | *Not specified* | S-knot cluster + L-knot (multi-digit structure); has subsidiaries | Knot value (possibly tens+units) | Medium (structural) |
| 5 | *Not specified* | Varies per block; has subsidiaries | Knot value + detail cords | Medium (structural) |
| 6 | *Not specified* | Varies; **never has subsidiaries** (terminal position) | Knot value only | Medium (structural) |

**Key structural finding (from OKR data, this analysis):** Subsidiaries (level-2 detail cords) attach to positions 2, 3, 4, 5 — **never to position 1 or position 6**. Position 1 is a header/summary field (no breakdown needed). Position 6 is terminal (no further detail). Positions 2–5 carry itemized detail.

**Honest gap:** The full 2018 paper was not accessed (Duke UP paywall). Positions 2–6 field labels above are inferred from database structure, not from the published cord-to-field mapping. The paper may specify these; direct access would confirm.

### What the six positions likely encode (hypothesis)

Based on the revisita containing name + tribute assessment per individual, and the structural pattern:

| Position | Likely field | Reasoning |
|---|---|---|
| 1 | Tribute assessed (in pesos) | Published: sums match revisita total |
| 2–5 | Tribute components (by type: goods, labor, etc.) or household members | Have subsidiaries = itemized detail |
| 6 | Total paid, balance, or status code | Terminal, no subsidiaries |

**This is inference, not published fact.** The revisita would confirm — it lists per-person tribute obligations that may break down by type.

## 3. Name Encoding: Color = Person

**Published (Medrano & Urton 2018):** Each individual's **first name** is encoded by cord color. All six cords in a person's block share the color assigned to their first name.

**Method (from Medrano's NPR interview):** Count first-name frequencies in the revisita (e.g., 12 Joses, 8 Felipes). Count cords by color. The counts match — the number of cords in "light brown" equals the number of people named José, etc.

**This is a lookup table, not phonetic spelling.** Each distinct first name maps to one color. It distinguishes individuals within the census; it does not spell names.

**Implication for Charles's project:** This only works because the census provides the name list. For Inca-period quipus without matching documents, color-to-name mapping cannot be recovered — but color-to-*category* mapping (ecological zone, commodity type) may be recoverable structurally, as our corpus analysis suggests.

## 4. Moiety Encoding: Recto/Verso = Hanan/Hurin

**2018 (Medrano & Urton):** Pendant cord attachment direction encodes moiety. 63 recto groups, 70 verso groups. Initially proposed: verso = Corongo+Guauyan+Cusca pachacas; recto = Namus+Cuyuchin+Ucore.

**2024 (FitzPatrick, refined):** Stronger alignment using markedness theory:
- **Verso = *hanan* (upper moiety)** — unmarked, primary, default
- **Recto = *hurin* (lower moiety)** — marked, secondary
- Revised pachaca grouping: verso = Namus+Cuyuchin+Guauyan; recto = Corongo+Cusca+Ucore
- The six pachacas follow a bipartite (3+3) and tripartite (2×3) hierarchy matching known Andean social models (cf. Zuidema's *ceque* system: Collana/Payan/Cayao)

**Tassel (*kayte*) confirmation:** KH0327 (all-verso) has a single pale-yellow tassel; KH0323 (all-recto) has pale-yellow + orange. Yellow = unmarked (*hanan*); yellow+orange = marked (*hurin*). Consistent with Clindaniel's color markedness ranking.

**Tribute asymmetry (FitzPatrick 2024):** The khipus reveal the verso (*hanan*) moiety paid ~381 pesos total (~5.45/person) while the recto (*hurin*) moiety paid ~86 pesos (~1.4/person). **The Spanish revisita does not record this split** — it is visible only in the khipu. This is a case where the khipu contains information absent from the colonial document.

**Computational verification (Contreras 2026):** Independent replication from OKR data alone: 49.0% recto / 51.0% verso aggregate (vs ~47%/53% published). Five of six quipus are pure (all-R or all-V); KH0326 is the sole mixed specimen (40R/69V). Confirms the moiety structure is real and machine-detectable.

**Our data (this analysis):**
- 1000270: V-heavy (53V/1U) — *hanan*
- 1000271: all-V (90V) — *hanan*
- 1000272: R-heavy (55R/5U) — *hurin*
- 1000273: R-heavy (290R/16U) — *hurin*
- 1000274: mixed (40R/68V) — composite (see below)
- 1000275: V-heavy (204V/2U) — *hanan*

## 5. Knot Value Ranges

From OKR data (simplified decoding; exact decimal values require positional analysis):
- **L-knots (long):** 2–9 turns (units digits)
- **E-knots (figure-eight):** = 1
- **S-knots (single):** 0 turns recorded (tens/hundreds markers; value from position)
- **Per-cord values:** small (published max ~15 per cord on Santa quipus; our simplified sums give similar ranges)
- **Position-1 values by quipu:** 1000270→9, 1000271→4, 1000274→5, 1000275→4 (constants); 1000272→{1,2}, 1000273→{0,1,2,4,7,10,11,12,13,15,20,22} (varying)

**Note:** The constant position-1 values on V-heavy (*hanan*) quipus vs. varying values on R-heavy (*hurin*) quipus may reflect different tribute structures between moieties — consistent with FitzPatrick's finding of asymmetric per-person tribute (5.45 vs 1.4 pesos).

## 6. Composite Structure Alert

**1000274** (one of the six) has an internal R/V flip at cord 51/108: left section 82% 6-blocked (7 colors), right section 53% 6-blocked (12 colors). The published "132 tributaries" may aggregate across sections with different formatting. **The 6-cords-per-person rule may apply at the section level, not the whole-quipu level.**

This means the "Rosetta" decipherment itself needs section-level reanalysis — a finding from our composite-document work that feeds back into the published match.

## 7. Applying the Schema to Livestock and Agricultural Goods

Charles's proposed method: use the person-encoding as a template for decoding commodity records. The structural logic transfers:

| Person census (Santa) | Commodity record (hypothesis) |
|---|---|
| 6 cords = 1 person | N cords = 1 commodity lot / herd / field |
| Color = person's name | Color = commodity type or origin zone |
| Position 1 = tribute assessed | Position 1 = total quantity (or quota) |
| Positions 2–5 = tribute components | Positions 2–5 = breakdowns (by source, type, time) |
| Position 6 = total/status | Position 6 = summary |
| Recto/verso = moiety | Recto/verso = in/out, or source/destination |
| Subsidiaries = detail entries | Subsidiaries = sub-lots |

**What transfers directly:**
- The **record format** (fixed N-cord groups per entity)
- The **positional logic** (header field + detail fields + terminal field)
- The **subsidiary rule** (detail attaches to middle positions, not header/terminal)
- The **color-as-identifier** principle (color labels the entity, not the value)
- The **binary attachment** principle (recto/verso marks a categorical distinction)

**What does NOT transfer directly:**
- 6 cords per entity is Santa-specific (census format). Commodity records may use different group sizes.
- Color = name is census-specific. For commodities, color likely = type/zone (as our ecological analysis suggests).
- The specific moiety mapping (hanan/hurin) is social. For goods, recto/verso may encode debit/credit, in/out, or assessed/delivered.

**Recommended next step:** Find commodity quipus with regular color-banded groups (like the Santa 6-block but for goods). The Inkawasi peanut quipus (5 quipus, same commodity, different palettes) are the test case — if they share a positional structure despite different colors, the format is confirmed independent of palette.

## 8. Sources Not Accessed (Gaps)

1. **Medrano & Urton (2018) full text** — Duke UP paywall (doi:10.1215/00141801-4260638). Would confirm positions 2–6 field labels and the color-to-name table.
2. **FitzPatrick (2024) full text** — Duke UP paywall (doi:10.1215/00141801-11266328). Would confirm the revised moiety-pachaca alignment table.
3. **The 1670 revisita** — Zevallos Quiñones (1991), "Padrón de Indios Tributarios Recuayes." Would provide the 132 named individuals for direct cord-group matching.
4. **Urton (2017), ch. 9** — *Inka History in Knots* (UT Press). May have additional detail on the 367-peso calculation.

## 9. Key Numbers Summary

| Metric | Value |
|---|---|
| Six-cord groups (khipu) | 133 |
| Named tributaries (revisita) | 132 |
| Six *pachacas* | Namus 18, Corongo 23, Cuyuchin 9, Cusca 7, Guauyan 41, Ucore 32 |
| Total tribute (revisita) | 367 pesos |
| Recto groups (Medrano) | 63 |
| Verso groups (Medrano) | 70 |
| Verso moiety total (FitzPatrick) | ~381 pesos (~5.45/person) |
| Recto moiety total (FitzPatrick) | ~86 pesos (~1.4/person) |
| Verso = | *hanan* (upper, unmarked) |
| Recto = | *hurin* (lower, marked) |
