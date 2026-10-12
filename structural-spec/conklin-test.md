# Testing Conklin's Construction-Sequence Rule

**Date:** 2026-10-11
**Rule under test:** Conklin 2002 ("A Khipu Information String Theory") — subsidiary cords are attached AFTER the parent cord is knotted, because knotting a parent after attaching subsidiaries would require passing the subsidiary mass through each knot. Implied construction order: spin/ply → attach pendant → knot pendant → attach subsidiary → knot subsidiary.

**Consequence:** Subsidiary information is necessarily LATER than parent information. Hierarchy encodes a weak temporal ordering (before/after) without grammatical tense.

**Why it matters:** The project hypothesized khipu are tenseless (no verbs, no tense morphology). Conklin offers a non-grammatical temporal mechanism: constructional chronology. If it holds, khipu have built-in "original vs. addition" structure.

**Database:** `okr-khipu.db`. 593 non-funerary khipu. Values from the type-aware decoder (`decoder.py` logic, batch-cached: 50,203 cords decoded, 41,006 high-confidence).

---

## Test 1: Construction-order violations in anomalous khipu

**Method:** Examine physical evidence in NOTES fields for four anomalous khipu against the predicted sequence.

### 1000178 — pendant slipped through a knot on its own subsidiary
> "At 27.0 cm. there is a knot on this subsidiary. Pendant 6 is slipped through the knot."

**Analysis:** For the pendant to pass through a knot on the subsidiary, the subsidiary's knot must have existed first. This reverses Conklin's sequence: the subsidiary was knotted BEFORE the pendant was threaded through. Under strict Conklin, the pendant should have been fully knotted before the subsidiary was even attached.

**Possible rescue:** The threading was a later modification (re-threading after original construction). But the Aschers labeled this a "Construction note," not a repair — weakening (not eliminating) the modification reading.

**Verdict: CONTRADICTS the strict sequence** as a claim about original construction.

### 1000344 — finishing knot on P10 tied around P11
> "The finishing knot on P10 is knotted around P11. Thus, the end of P10 is tied to P11 at 5.5 cm. from the bottom of P11."

**Analysis:** This is a lateral pendant-to-pendant link made at the finishing stage (end knots are tied last). It does not directly test the parent→subsidiary sequence. However, the same entry notes missing pendants ("darkened color of the main cord... a pendant was present but is now missing"), confirming post-construction removal.

**Verdict: NEUTRAL on Conklin's sequence; SUPPORTS "khipu as living document"** (cords added, tied, and removed after initial construction).

### 1000239 — six subsidiaries through a pendant's doubled end
> "Pendant 21 has its 6 subsidiaries attached through the doubled end."

**Analysis:** A doubled end is a finishing treatment. Subsidiaries attached through it depend on the doubling pre-existing — the parent was complete (finished) before subsidiaries were attached. This is exactly Conklin's predicted order.

**Verdict: WEAKLY SUPPORTS Conklin.**

### 1000201 — pendant replaced upside down
> "Pendant 70 is mended at 5.5 cm. It appears to have been replaced upside down so the knot order is reversed."

**Analysis:** Explicit repair — a pendant removed and reattached inverted during the khipu's use-life. Does not test original construction sequence, but confirms khipu were physically modified after manufacture.

**Verdict: SUPPORTS "living document"; NEUTRAL on Conklin per se.**

### Test 1 overall: MIXED
One direct contradiction (1000178), one weak support (1000239), two confirming post-construction modification without testing the sequence. The strict physical claim — subsidiary ALWAYS attached after parent knotted — does not survive 1000178 unless the threading is a later alteration.

**Important distinction:** The *informational* sequence (parent content precedes subsidiary content) can hold even if the *physical* sequence is occasionally violated. A re-threaded pendant does not change the fact that the subsidiary's information was recorded later.

---

## Test 2: Value independence as temporal independence

**Method:** If subsidiaries are later independent entries (not contemporaneous subdivisions), their values should be statistically related-but-not-determined by parent values. Decode parent-subsidiary pairs corpus-wide (high-confidence, nonzero values only).

**Result:**
- n = 3,917 parent-subsidiary pairs
- Log-value Pearson r = 0.496 (p = 2.1e-244)
- Spearman r = 0.445 (p = 2.7e-190)
- Median parent value = 12; median subsidiary = 3

**Interpretation:** Moderate correlation — far from the r≈0.9+ expected if subsidiaries were arithmetic subdivisions, far from r≈0 expected if fully independent. This is the signature of *related but separately entered* values: the subsidiary belongs to the same account (hence correlation) but was recorded as its own entry (hence independence). Exactly what "later addition to a related account" predicts.

**Inkawasi note:** Only 12 high-confidence pairs recoverable (most Inkawasi long knots lack NUM_TURNS); these give r=0.974 but are a biased tiny subset (values cluster at 1 and 11). The earlier rider-test r=0.143 (n=65, including medium-confidence) remains the more honest Inkawasi estimate. The corpus-wide r=0.496 is the robust number.

**Roundness sub-test: INVALID.** Attempted to test whether subsidiary values cluster at round numbers (multiples of 10/100, suggesting new deposits). Found zero multiples of 10 among 23,685 high-confidence values — but this is a **decoder artifact**, not a real pattern: when a cord has S-knots but no units cluster, the decoder treats the first cluster as units-position, flags S-in-units as low-confidence, and the value is excluded from high-confidence results. Multiples of 10 are systematically invisible to the high-confidence filter. (Notable: 2,152 odd multiples of 5 — 5, 15, 25 — do decode, confirming the blind spot is specific to even multiples of 10.) The roundness hypothesis cannot be tested with the current decoder.

**Verdict: SUPPORTS the weak version.** Subsidiaries are related-but-independent entries, consistent with later additions. The strong version (fully independent, r≈0) is rejected; the subdivision model (r≈0.9, summation) was already rejected.

---

## Test 3: Depth as time

**Method:** If hierarchy = chronology, deeper levels are later additions. Test whether depth correlates with (a) color-marking, (b) value size.

**Results:**

| Level | n (values) | Median value | White fraction |
|-------|----------:|------------:|---------------:|
| L1 | 14,062 | 8 | 31.9% |
| L2 | 5,519 | 3 | 20.3% |
| L3 | 617 | 3 | 18.4% |
| L4 | 105 | 3 | 14.9% |

**Color:** White (unmarked) fraction drops monotonically with depth. Under Conklin + the evidentiality finding: L1 = original entries, directly witnessed (unmarked); L2+ = later additions, reported/secondary knowledge (marked). The existing evidentiality gradient (p=1.5e-213) **reads naturally as a chronological gradient** — this is the same data, reinterpreted temporally, and the two readings reinforce rather than compete.

**Value size:** Median drops from 8 (L1) to 3 (L2+). Later additions are smaller — consistent with incremental deposits, corrections, or updates rather than initial bulk entries.

**Verdict: SUPPORTS.** Both the marking gradient and the value-size gradient are what "deeper = later" predicts. The evidentiality finding and Conklin's chronology are mutually consistent: later knowledge is more reported, earlier knowledge more direct.

---

## Test 4: Repairs and additions

**Method:** Find khipu with mended/repaired cords (khipu-level + cord-level NOTES). If deep hierarchies reflect long use-life with additions, repaired khipu should have deeper hierarchies and more subsidiaries.

**Result:** n=16 repaired khipu (6 khipu-level notes, 12 cord-level, union 16).
- Max depth: repaired 1.81 vs. 1.95 overall (Mann-Whitney p=0.52) — **no difference**
- Subsidiary presence: 56% repaired vs. 64% overall (Fisher p=0.60) — **no difference**

**Verdict: CONTRADICTS the prediction, or the test is misaimed.** "Repaired" in the notes overwhelmingly means physical damage (broken pendants, mended main cords), not use-life additions. This test measures damage, not chronology. **Inconclusive as a test of Conklin** — but the null result is informative: visible damage does not correlate with structural depth, suggesting depth is a design feature, not an accident of preservation.

---

## Overall assessment

### Does Conklin's strict construction sequence hold?
**No, not as an absolute physical law.** 1000178 is a direct counterexample unless the pendant-through-subsidiary-knot is a later modification. The Aschers' "Construction note" (not "repair") labeling makes the modification rescue uncomfortable but not impossible.

### Does the broader chronological interpretation hold?
**Yes, on three independent lines of evidence:**
1. **Values:** Subsidiaries are related-but-independent (r=0.50) — the statistical signature of later entries to the same account, not subdivisions and not unrelated records.
2. **Marking:** The depth gradient (white 32%→15%) reads as "original = witnessed, addition = reported" — Conklin's chronology and the evidentiality finding are the same phenomenon viewed two ways.
3. **Modification:** Physical evidence of post-construction alteration is widespread (repairs, reattachments, missing pendants, lateral ties). Khipu were living documents.

### Does it rescue temporal structure for tenseless khipu?
**Partially — it gives before/after, not tense.** Hierarchy encodes a two-state temporal system: original entry vs. subsequent addition. That is enough for "this is the account, and these are later entries" — which is all an administrative record requires. It does not give past/present/future, habitual, or any other tense distinction. For a record-keeping system, before/after may be the only temporal distinction that matters.

### How a khipu reads as a temporal sequence
1. **Primary cord + L1 pendants:** The founding entries. Direct knowledge (unmarked), larger values (bulk deposits, initial census). The "original document."
2. **L2 subsidiaries:** First-generation additions. More marked (reported/secondary source), smaller values (incremental). Appended when new information arrived — a new deposit, a correction, a sub-account opened later.
3. **L3/L4:** Further additions, increasingly marked, increasingly small. The margins of the ledger filling up.
4. **Repairs, re-threadings, lateral ties (1000178, 1000344, 1000201):** The document's edit history — visible revisions, like cross-outs and marginalia in a paper ledger.

The khipu is not a snapshot; it is an **accrual**. Reading it top-to-bottom through the hierarchy is reading it oldest-to-newest.

---

## Caveats
- Construction order is a physical claim; we have database records, not the objects. "Consistent with" is not "proves."
- The roundness test is blocked by a decoder blind spot for multiples of 10. Do not cite the zero-multiples-of-10 as a finding.
- Inkawasi values are largely unrecoverable (missing NUM_TURNS); Inkawasi-specific claims rest on thin data.
- n=16 for the repair test is small; the null result may reflect low power, though the effect direction (repaired slightly *shallower*) argues against a missed large effect.
- 1000178 remains the strongest evidence against strict Conklin. Physical re-examination of that pendant/subsidiary junction would settle whether the threading is original or a later alteration.
