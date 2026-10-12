# Distribution Orders: Corpus-Wide Search

## The Pattern

A value V followed by same-color values summing to V. Like 1000029 Ord 21:
YG=112 followed by YG values 13, 79, 9, 11 (sum=112).

**Interpretation:** Allocation, not subtotal. "Distribute 112 units as 13/79/9/11."
Total comes FIRST (prospective), not after (retrospective).

## Method

Scanned all 612 khipu in `templates/cache.pkl` (pre-decoded values).

For each cord with value V >= 20:
- Collected following same-color nonzero values within 20-ordinal window
- Flagged if 2+ components sum exactly to V
- Excluded if V also equals sum of PRECEDING values (ambiguous direction)

## Results

**14 candidates** across 14 khipu (2.3% of corpus).

After manual verification of each against actual cord sequences:

### Strong (4) — Likely real distribution orders

| Khipu | Ord | Color | Total | Components | Notes |
|-------|-----|-------|-------|------------|-------|
| 1000029 | 21 | YG | 112 | 13, 79, 9, 11 | Reference case. Clean YG block. |
| 1000127 | 70 | YG | 369 | 114, 81, 92, 82 | 4 large varied. Clean block. Ica. |
| 1000338 | 6 | FB | 102 | 13, 13, 18, 25, 33 | 5 components. Clean block. Radicati. |
| 1000009 | 17 | BL | 41 | 23, 11, 7 | 3 components, contiguous. Leymebamba. |

All four share the same structure:
- Total at the START of a clean same-color block
- 3-5 varied components (not "large + tiny")
- Exact sums, no ambiguity
- Components are contiguous or near-contiguous

### Medium (4) — Possible

| Khipu | Ord | Color | Total | Components | Notes |
|-------|-----|-------|-------|------------|-------|
| 1000081 | 16 | DB | 50 | 10, 40 | Round total. Zeros interspersed. |
| 1000091 | 15 | W | 20 | 10, 10 | Even split. Small numbers. |
| 1000147 | 169 | YB | 34 | 16, 18 | Natural split. Scattered. Pachacamac. |
| 1000139 | 4 | W | 91 | 52, 25, 14 | At khipu start. Interleaved. Pachacamac. |

### Weak (6) — Likely false positives

| Khipu | Reason |
|-------|--------|
| 1000007 | 459 = 458+1. "Large + tiny" pattern. Components 13 ordinals apart. |
| 1000012 | 54 = 52+2. "Large + tiny" pattern. Scattered singletons. |
| 1000113 | Even split but components far apart in mixed sequence. |
| 1000292 | Components in separate block after color interruption. |
| 1000344 | Wide span (14 ordinals). Only 2 components. Different context. |
| 1000506 | Window artifact. 8 tiny values. Extending window breaks sum. |

## Is This a Document Type?

**No.** 4 strong cases out of 612 khipu (0.65%) is too rare for a document type.

**What it is:** An occasional scribal technique. When a scribe needs to record a distribution plan
("divide X among recipients"), they write the total first, then the allocations. Most khipu don't
need this — they're recording transactions, not planning distributions.

**Geographic spread:** The strong cases come from Ica (south coast), Leymebamba/Chachapoyas
(northern highlands), Radicati (unknown), and Buffalo (unknown). No regional clustering.
This is a general technique, not a local convention.

**Document context:**
- 1000029: deep_sparse_mixed, data regime 2 (small counts). Transaction log with one allocation.
- 1000127: No template classification. Large values (369).
- 1000338: No template classification.
- 1000009: No template classification. Chachapoyas.

The allocations appear in different document contexts, supporting the "technique, not type" reading.

## The "Large + Tiny" False Positive Pattern

Two candidates (1000007, 1000012) showed V = (V-1) + 1 or V = (V-2) + 2.
This is almost certainly coincidence: in a corpus with thousands of values, some large value
will happen to equal another large value plus a tiny one. The components are far apart
and don't form a clean block. Excluded from strong classification.

## Files

- `allocation_candidates.csv` — all 14 candidates with strength assessments
- `scan_allocations.py` — reproducible scan script

## Answer

**1000029 is not unique, but distribution orders are rare.** 4 strong cases corpus-wide.
It's a scribal technique for recording allocation plans, used occasionally across different
regions and document types. Not a document type in itself.
