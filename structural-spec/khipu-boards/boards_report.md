# Khipu Boards as Lexicon Sources

**Date:** 2026-10-11
**Status:** Research complete. Honest assessment: boards provide less lexical data than hoped, but one verified structural mapping of high value.

---

## 1. What khipu boards are

Hybrid khipu/alphabetic texts developed in 16th-century Peru by Mercedarian missionaries (Diego de Porres, ca. 1572-1579) to track Indigenous participation in catechesis and church festivals. A wooden board covered with paper lists names in alphabetic script; next to each name is a hole through which hangs a knotted cord recording that person's obligations or fulfillment status. Used in the Central Andes into the 1950s.

**Critical structural fact:** the cords do NOT encode the written names. The name is in ink; the cord encodes what that person *did or owed* (attendance, labor, goods, ritual items). A khipu board is therefore not a word-to-knot dictionary in the naive sense. It is a bilingual *document* in which one channel (alphabetic) gives identity and the other (cord) gives status/obligation.

---

## 2. Catalog of known boards

Seven boards or board-traditions identified. Only one (Mangas) has published cord-level analysis.

| Board | Date | Location | Cord-level data? |
|---|---|---|---|
| Mangas (MANGAS-01) | 1800-1900 | Ancash, Peru → MALI Lima | Yes — Hyland et al. 2014 |
| Ayacucho (AYACUCHO-01) | 19th c.? | Unknown provenance | No — brief description only |
| Casta (CASTA-01) | early 20th c., used to 1950s | Huarochirí, Peru | No — board hidden; Entablo ms. only |
| Cotacachi (COTACACHI-01) | observed 1863 | Ecuador | No — eyewitness only |
| Pari (PARI-01) | used to 1950s | Central Andes | No — name only |
| Arica (ARICA-01) | unknown | Chile | No — name only |
| Collata hybrid (COLLATA-HYBRID-01) | used to 1940s | near Collata, Peru | No — popular press only |

Full catalog: `boards_catalog.csv`.

---

## 3. Verified mappings (high confidence)

Exactly **two** mappings are verified to scholarly standards, both from the Mangas board (Hyland, Ware & Clark 2014, *Latin American Antiquity* 25(2)):

| Meaning | Knot pattern | Evidence |
|---|---|---|
| Upper moiety (Hanan / Cotosh) | S-direction knot | 15/15 on moiety-known names; 63.9% S-knots mirrors 64.5% Cotosh names; p<0.01 |
| Lower moiety (Urin / Allaucay) | Z-direction knot | Same study, inverse |

This is the single most important result. It confirms Urton's hypothesis that knot direction encodes moiety, and it was the first structural (non-numerical) decipherment since Locke 1923.

**One caveat:** a single exception exists (Mariana Santos, Cotosh surname with Z-knot), attributed by the authors to cord damage — the original end-knot was lost and the surviving knot is not the terminal one. Plausible but post-hoc.

An additional **operational** mapping is verified by eyewitness (Hassaurek 1866, Cotacachi; depicted in Martínez Compañón 1789 watercolor):

| Meaning | Cord state |
|---|---|
| Obligation fulfilled | Cord pulled tight to board, held by end-knot |
| Obligation unfulfilled | Cord left hanging loose (punishment followed) |

This is a *state*, not a knot pattern, but it is directly relevant to the evidentiality/marking analysis: physical manipulation of the cord as a fulfillment marker.

---

## 4. Proposed but unverified mappings

**Cord construction → contribution type (Mangas).** Of 87 cords, 33 distinct constructions; the most common (deep pink + black, 14 cords across 9 surnames) and others repeat in ways suggesting categorical meaning — Hyland proposes contribution types (cloth, wood, food). But no specific construction has been tied to a specific good. **Confidence: proposed, not verified.**

**Knots → sequential task completion (Casta).** Bennison 2025 preprint hypothesizes that knots on Casta wankaunas recorded completion of work tasks in sequence during canal-cleaning. The board itself is hidden by villagers and has not been studied at cord level. **Confidence: hypothesis.**

**Entablo contextual categories (Casta).** The 1921 Entablo manuscript describes *what* was tracked — two kinds of maize beer by ayllu, conduct assessments by gender, household-level vs individual duties, punishment triggers — but the cord encodings are unknown. **Confidence: context only, no knot mapping.**

---

## 5. What boards do NOT provide

- **No word-to-knot dictionary.** Names are written alphabetically; cords encode obligations, not identities.
- **No color → commodity mapping.** The Mangas cord-construction repetitions *suggest* this exists but no mapping is confirmed.
- **No color → place mapping.**
- **No numerical decoding beyond Locke.** Board cords mostly have single end-knots (fulfillment markers), not decimal arrays.
- **The Collata 95-sign claim** (Hyland 2017, *Current Anthropology*) concerns patrimonial khipus, not boards, and the lineage-name readings are unverified.

---

## 6. Transferability to Inca-period khipu

| Mapping | Time gap | Transferability | Rationale |
|---|---|---|---|
| S = upper moiety / Z = lower moiety | ~270-370 yrs (Mangas 1800s → Inca pre-1532) | **Moderate-high** | Directly supports Urton's Puruchuco hypothesis (UR66/UR67 paired khipu). Moiety organization is pre-Inca and persistent. But: Mangas moieties are Cotosh/Allaucay (local), not Hanan/Urin (imperial) — the *principle* transfers, the *labels* may not. |
| Tight = fulfilled / loose = unfulfilled | ~330 yrs (1863 obs.) | **Moderate** | Operational logic likely conservative, but Inca-period khipu were archival records, not public display boards. The physical mechanism may not transfer even if the concept does. |
| Cord construction = contribution type | ~270-370 yrs | **Low-moderate** | Unverified even for the board itself. Cannot project an unconfirmed mapping backward. |
| Sequential knots = task phases | ~400 yrs | **Low** | Hypothesis only, no surviving board to verify against. |

**Key limitation:** all boards postdate the Inca by 270+ years. The moiety finding is the strongest bridge because (a) it is statistically verified, (b) it confirms a prediction made from Inca-period material (Puruchuco), and (c) moiety dualism is documented as continuous from pre-Inca through republican periods.

---

## 7. Implications for the seed lexicon

The honest seed lexicon from boards is **small**:

1. **S-knot ↔ upper/higher-ranked member of a social pair** (verified, Mangas)
2. **Z-knot ↔ lower-ranked member** (verified, Mangas)
3. **Cord tightened ↔ fulfilled/recorded-complete** (eyewitness, Cotacachi)
4. **Cord loose ↔ unfulfilled/pending** (eyewitness, Cotacachi)

Everything else in `board_lexicon.csv` is marked proposed/hypothesis/context-only.

**What this means for the project:**

- The moiety mapping is directly usable: in Inca-period khipu, S/Z knot direction on identity cords is now a *verified* social-rank marker, not just a hypothesis. This constrains the evidentiality analysis — some S/Z patterning previously attributed to evidentiality or register may be moiety marking.
- The tight/loose finding suggests that cord *manipulation state* (not just knot type) carried meaning. Inca-period khipu in OKR are static museum objects; we cannot observe their manipulation state. This is a data gap, not a refutation.
- Boards do **not** solve the color lexicon. The commodity/place mappings must come from elsewhere (Santa census labels, Inkawasi context, archival provenance).
- The Entablo is the richest contextual source for *what kinds of things* were tracked (beer types by ayllu, gendered conduct, household vs individual duties). Even without knot mappings, it provides a vocabulary of obligation-types to look for in Inca-period labor/tribute khipu.

---

## 8. Gaps and recommended follow-ups

1. **Ayacucho board** — no provenance, no cord analysis. If locatable, its simplicity (single variable) could provide a clean test case.
2. **Casta board** — hidden by villagers. The Entablo describes its *use* in detail; physical access would be the single highest-value board study possible.
3. **Mangas cord constructions** — Hyland has the data (33 constructions, 87 cords). A published construction-to-surname cross-tabulation could test whether specific constructions map to specific kin groups or contribution types. Worth requesting from the author.
4. **Mercedarian archives** — Hyland (2014) notes ongoing research in Mercedarian archives. Early (16th-17th c.) board descriptions would shrink the time gap significantly.
5. **Martínez Compañón watercolors (1789)** — depict boards in use; may contain visual detail on cord arrangements not available elsewhere.

---

## Sources

- Hyland, Sabine, Gene A. Ware & Madison Clark. 2014. "Knot Direction in a Khipu/Alphabetic Text from the Central Andes." *Latin American Antiquity* 25(2): 189-197.
- Hyland, Sabine, Sarah Bennison & William P. Hyland. 2021. "Khipus, khipu boards and sacred texts: toward a philology of Andean knotted cords." *Latin American Research Review* 56(2): 400-416.
- Bennison, Sarah. 2025. "Notes on the leather khipu boards or 'wankaunas' of San Pedro de Casta, Peru." Figshare preprint.
- Robles Mendoza, Román. 1982. *Quipu y mashas en la comunidad de Mangas.* UNMSM, Lima.
- Hassaurek, Friedrich. 1967 [1866]. *Four Years among the Ecuadorians.*
- Salomon, Frank. 2004. *The Cord Keepers.* Duke UP.
- Hyland, Sabine. 2017. "Unraveling an Ancient Code." *Current Anthropology* (Collata khipu).
- Khipu historiography overview: OpenEdition Presses de l'Inalco.

**Copyright note:** All summaries above are original paraphrase. No extended quotation from copyrighted works.
