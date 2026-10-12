# Testimony Tags: Using Colonial Testimony as Inventory Labels for Document Types

**Date:** 2026-10-10
**Premise (Charles):** Khipukamayuq shaded the NUMBERS but told the truth about the document TYPE. The Spanish could verify the category (census, tribute account, inventory) — they just couldn't verify the figures. Testimony labels are therefore "inventory tags": noisy on values, reliable on genre.

---

## 1. The Six Testimony Tags

Extracted from `testimony-game-theory.md`. Each case = one claimed document type.

| # | Case | Date | Claimed document type | Spanish question |
|---|---|---|---|---|
| 1 | Wanka lord, Hatun Xauxa | 1533 / 1558–61 | **Storehouse inventory** — provisions given vs. stolen, by Andean category | "Show us what the storehouses held / what was taken" |
| 2 | Vaca de Castro inquest, Cuzco | 1542 | **Historical narrative** — Inca origins and dynastic history | "Were the Incas native or foreign? Who ruled?" |
| 3 | Chucuito visita | 1567 | **Census** — 20,080 households, section-by-section, moiety copies | "Do the two moiety khipu match?" |
| 4 | Sacaca case | 1579 | **Tribute account** — coca-field production and tribute paid | "Was tribute excessive?" |
| 5 | Canta case | 1593 | **Tribute/liquidation account** — tribute rates, community contributions, official misconduct | "Did the outgoing official skim?" |
| 6 | Xauxa road account | 1602 | **Surveillance log / chronicle** — travelers on the royal road, events good and bad | (none — discovered, not elicited) |

Three genre families emerge: **inventory** (1), **census/tribute** (3, 4, 5), **narrative/chronicle** (2, 6).

---

## 2. Expected Structural Signatures per Tag

Derived from the v2 section-level framework (`form-types-v2.md`), data classes (`data-classes.md`), and the census/inventory analyses.

### Tag 1 — Storehouse inventory
- **Form:** F (deep hierarchy) or E (hierarchical ledger) sections — multi-level aggregation suits stock accounting
- **Values:** Bulk quantities (large knots/cord — observed mean ~4.4 on Inkawasi commodity quipu)
- **Color:** Family = ecological zone of the good's origin (86–93% zone accuracy); specific palette = production batch
- **Subsidiaries:** Breakdown/detail cords (observed subsid/cord 0.05–1.88, highly variable)
- **Grouping:** No fixed N-cord record unit (peanut quipu: no clean N for 2–12 tested)
- **R/V:** Typically single-side dominant

### Tags 3/4/5 — Census / tribute account
- **Form:** Any (D, E, F, C, B — census is a content type spanning forms)
- **Values:** Small per-cord quantities — individual/household-level amounts (observed mean ~1.6 knots/cord on Santa)
- **Color:** = identifier bucket (name for census; field/owner for tribute); 6-block grouping where the record unit is the person
- **Grouping:** Fixed N-cord record groups (N=6 for Santa census — the "word")
- **R/V:** Mixed — moiety marking (verso = hanan, recto = hurin)
- **Archetype signature:** Positional within the group (Santa: position 1 = LEAF/subsidiary-free header)

### Tag 2 — Historical narrative
- **Expected:** Unknown. No physical anchor exists.
- **Hypothesis (flagged speculative):** Narrative quipu — if they exist in the corpus — should show elevated non-numerical knot symbols (the rare 0.5% of the 16-symbol alphabet: SP, TF, EE, LL, BL), irregular structure not matching A–F cleanly, possibly E-knot/EE-heavy marker sequences. Urton's "up to a third" estimate suggests they are numerous but unrecognized.

### Tag 6 — Surveillance log / chronicle
- **Expected:** Unknown. No physical anchor exists.
- **Hypothesis (flagged speculative):** Chronological structure — regular sequential runs, possibly date-like periodic markers; uniform record units in time order rather than grouped by category.

---

## 3. Anchoring: Which Tags Have Physical Quipu

| Tag | Physical anchor | Source |
|---|---|---|
| 1 — Storehouse inventory | **YES:** 10 Inkawasi quipu with excavated commodity associations | Urton & Chu 2015 |
| 3 — Census | **YES:** 6 Santa quipu matched to 1670 revisita; 31 census-like sections corpus-wide | Medrano & Urton 2018 |
| 4/5 — Tribute account | **PARTIAL:** Santa quipu encode tax owed/paid per person — census and tribute collapse structurally; no standalone tribute quipu (Sacaca, Canta) survive | Medrano & Urton 2018 (Santa); testimony only (Sacaca, Canta) |
| 2 — Narrative | **NO** | — |
| 6 — Surveillance log | **NO** | — |

**Key structural finding:** Tags 3, 4, and 5 are **one structural class**. The testimony distinguishes census (headcount) from tribute (production/rates), but the Santa quipu show both functions in the same documents — the 6-cord person-record carries tax fields. At the structural level, "census/tribute" is a single genre: small-value, person-or-household-level records with identifier-color coding.

This leaves **two anchored structural classes**: **inventory** (bulk, deep, no fixed record unit) and **census/tribute** (small-value, fixed record groups, identifier color).

---

## 4. Cross-Check: Do the Anchored Classes Separate?

16 quipu, 2 classes, measured this session:

| Feature | Census/tribute (Santa, n=6) | Storehouse inventory (Inkawasi, n=10) |
|---|---|---|
| Exact-6-block fraction | 0.61–1.00 (all ≥0.6) | 0.00–0.06 (all ≤0.06) |
| Knots per L1 cord (mean) | 0.8–2.7 (mean ~1.6) | 0.9–9.3 (mean ~4.4) |
| Subsidiaries per L1 cord | 0.02–0.89 | 0.05–1.88 |
| R/V attachment | Mixed (moiety) | Mostly single-side |
| Color function | Identifier bucket (name) | Origin zone (family) + batch (palette) |
| Fixed record unit | Yes (N=6) | No (tested N=2–12, none) |
| Whole-quipu form | E (all six) | F (9/10), E (1/10) |

**The exact-6-block fraction alone separates the classes perfectly** (threshold 0.3–0.5; observed gap 0.06 vs 0.61). Value scale provides a secondary, noisier signal (means differ 2.75× but ranges overlap at the margins: Santa max 2.7 vs Inkawasi min 0.9).

Note on circularity: the Santa six *define* the 6-block census signature (Medrano & Urton), so their high scores are expected. The independent confirmation is the Inkawasi side — 10 quipu with archaeologically fixed commodity function score ~0 — plus the corpus-wide census search finding 31 sections at 12 proveniences, showing the signature generalizes beyond Santa.

---

## 5. Proof-of-Concept Classifier

**Task:** Given structural features, predict the testimony tag (document type).

**Classes:** 2 (the anchored ones). The 4 unanchored tags cannot train anything.

**Training set:** n=16 quipu (6 census/tribute, 10 inventory). At section level: 31 census-like sections + 10 inventory quipu (sections not separately scored for inventory; n=41 items).

**Rule (interpretable, single-feature):**
```
IF exact_6block_fraction >= 0.5 → CENSUS/TRIBUTE
ELSE → INVENTORY (or other — see limits)
```

**Accuracy on training set:** 16/16 (100%).

**Honest limits — read before using:**
1. **n=16 is tiny.** This is a demonstration, not a validated classifier. A proper validation needs held-out quipu with independent functional ground truth (excavation context or document match).
2. **"INVENTORY" is really "not-census."** The rule's negative class lumps storehouse inventory with every other non-census genre (tribute ledgers without 6-block, tallies, unknown). It detects the census signature; it does not positively identify inventory.
3. **Tribute without census structure is invisible.** If Sacaca-style tribute accounts (field-level, not person-level) lack 6-blocks, this rule files them as "inventory." The testimony says tribute is its own genre; structurally we cannot yet separate it from inventory.
4. **Narrative and surveillance tags are untestable.** No physical anchors. The classifier has no opinion on them.
5. **The 6-block threshold (0.5) is tuned on the training set.** The observed gap (0.06/0.61) is wide enough that any threshold in 0.1–0.5 works, but an independent sample could narrow it.
6. **Value scale is a weak secondary feature.** Do not use knots/cord alone — ranges overlap.

**What would validate it:** A newly excavated quipu with clear archaeological context (e.g., found with goods = inventory; found in a census archive = census). Predict the tag from structure *before* looking at context. One clean hit is worth more than 16 training points.

---

## 6. Testable Predictions for Unanchored Tags

If the testimony-tag model is right, these follow — all flagged as hypotheses awaiting physical anchors:

1. **Narrative quipu (Tag 2)** should be findable as structural outliers: quipu where the rare 0.5% knot alphabet (SP, TF, EE, LL, BL) is elevated, 6-block ~0, value scale irregular, and form classification is low-confidence. **Search procedure:** rank corpus quipu by rare-symbol density; inspect top 20 for non-numerical patterning.
2. **Surveillance/chronicle quipu (Tag 6)** should show chronological record structure: uniform record units in strict sequence, no category grouping, possibly periodic marker cords at regular intervals. **Search procedure:** look for long single-form sections with metronomic color cycling and no 6-block.
3. **Tribute-without-census (Tags 4/5 pure form)** — if Sacaca-type field-level tribute quipu exist in the corpus, they should score 6-block ~0 (like inventory) but show small-to-medium values and owner/field identifier colors (like census). They would be the classifier's informative failure mode: currently misfiled as "inventory."

---

## 7. What This Establishes

1. **Charles's premise is operationalized.** Six testimony tags extracted; two anchored to physical quipu; the anchored pair separates cleanly on structure (6-block fraction: 100% train accuracy, wide margin).
2. **Census and tribute are one structural genre.** The testimony's three-way split (census / tribute / tribute-liquidation) collapses to a single small-value, identifier-coded, fixed-record-unit class. The Spanish asked different questions; the quipu answered with the same document type.
3. **The bridge works in one direction.** Testimony tags validate structural classes (census ↔ 6-block; inventory ↔ deep bulk hierarchy). The reverse — using structure to label an unknown quipu's genre — is a proof of concept with n=16, not a production tool.
4. **Four tags remain dark.** Narrative, surveillance, and pure field-tribute have no physical anchors. Their expected signatures are hypotheses, and §6 gives the search procedures to test them.

## 8. Limitations

- n=6 testimony tags; n=2 anchored classes; n=16 training quipu. Everything here is pilot-scale.
- Anchors are single-site each (Santa; Inkawasi). Regional variation in genre conventions is unmeasured.
- The 1542 narrative testimony is the most strategically shaped in the corpus (Case 2) — its tag ("historical narrative") is reliable as a *claimed* type, but the content was likely tailored. Type truthful, content suspect — consistent with Charles's premise.
- No decimal value decoding was used (Inkawasi KNOT_ORDINAL/TURNS empty in OKR). Value scale uses knot counts as proxy.
- The classifier was not cross-validated (n too small for meaningful folds). The 100% figure is in-sample.
