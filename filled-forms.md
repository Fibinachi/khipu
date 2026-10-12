# Filled Forms: How Quipu Were Completed

**Date:** 2026-10-10
**Question:** Now that we know the blank form types, what do recurring filled entries look like?

## 1. The Standard Unit: 10

The single most striking finding in the entire dataset:

| Knot value | Count |
|------------|-------|
| **10** | **47,637** |
| 100 | 12,820 |
| 1 | 7,486 |
| 2 | 5,233 |
| 3 | 3,739 |

The value 10 appears nearly **4x more often** than any other value. This is not a natural distribution — it is a bureaucratic standard. The Inca counted in tens the way modern systems count in dozens or hundreds. Ten is the base unit of the administrative system.

At the cord level (summing all knots on a cord), the distribution shifts:

| Cord total | Count |
|------------|-------|
| 1 | 5,107 |
| 2 | 3,018 |
| 3 | 1,953 |
| 4 | 1,748 |
| 10 | 1,641 |

Individual cords most commonly record small numbers (1-4). Combined with the knot-level dominance of 10, this reveals the **census pattern**: many cords each recording small counts, with 10 as the standard cluster value. One cord per person/household, values 1-4.

## 2. The Most Formulaic Line Items

The most common (color + value) combinations — the boilerplate entries:

| Line item | Count |
|-----------|-------|
| White cord = 1 | 288 |
| White cord = 2 | 228 |
| Brown cord = 1 | 183 |
| White cord = 4 | 168 |
| White cord = 3 | 164 |
| Light brown cord = 1 | 156 |

**White cords recording 1, 2, 3, or 4** are the most formulaic entries in the entire corpus. If white = undyed natural cotton (the default), and small numbers = individuals, these are census entries. The quipucamayoc's most common task was counting people.

The value 10 appears on **every major color** (W: 15,040; AB: 8,047; MB: 5,952; B: 2,971; KB: 2,145; GG: 1,513). Ten is color-blind — it is the universal counting unit regardless of commodity.

## 3. Color Batching: Commodities in Blocks

Colors do not alternate randomly. They run in contiguous blocks:

| Bigram | Count |
|--------|-------|
| W → W | 1,964 |
| B → B | 1,177 |
| MB → MB | 894 |
| AB → AB | 631 |

| Trigram | Count |
|---------|-------|
| W → W → W | 1,495 |
| B → B → B | 995 |
| MB → MB → MB | 694 |

Each commodity gets a **contiguous block of cords**. The quipu reads like a spreadsheet with color-coded column groups: all the white cords together, then all the brown cords, then the next color. Cross-color transitions (W→MB: 263; MB→W: 246) are the boundaries between commodity sections.

This is exactly how a modern inventory form works — group by category, not interleave.

## 4. Red Dividers in Context

48 quipu contain red (R/SR/RS) cords. Red appears as singletons 100% of the time — never in multi-cord runs. When red appears between two non-red cords:

| Context | Count |
|---------|-------|
| W → RED → W | 8 |
| AB → RED → GG | 4 |
| LC → RED → MB | 4 |
| W → RED → FB | 3 |

Red separates **different** colors in the majority of informative cases (AB|RED|GG, LC|RED|MB). It is a section divider, not a commodity code. The W→RED→W cases (8) may represent subdivisions within the white/census section — possibly separating different groups (e.g., taxpayers vs. exempt).

## 5. E-E-E Labels: What Follows

33 cords have 3+ figure-eight (E) knots. In the 7 cases where the next cord could be identified, the following values were: 33, 7, 160, 430, 215, 10. No single pattern — the label does not predict a specific value range.

This is consistent with E-E-E as a **name/category label** rather than a value prefix. It says "this section is about X" without constraining what the numbers will be. Like a column header in a spreadsheet.

## 6. Representative Filled Examples

### Example A: Tribute Ledger (Quipu 1000055, Pachacamac, Berlin VA42605 B)

**Form type:** Grouped account (D)

| Cord | Color | Knots | Total |
|------|-------|-------|-------|
| 1 | Light brown | L:5, S:10×7, S:100×6, L:5, S:10×7, S:100×6 | 1,350 |
| 2 | Dark brown | S:10 ×10 | 100 |
| 3 | Dark brown | S:10 ×2 | 20 |
| 4 | Dark brown | S:10 ×8 | 80 |
| 5 | Dark brown | S:10 ×2 | 20 |
| 6 | Dark brown | S:10, S:100, S:10, S:100 | 220 |
| 7 | Dark brown | S:10 ×8 | 80 |
| 8 | Dark brown | S:10 ×10 | 100 |

One summary cord (1,350, light brown) followed by detail cords (dark brown, values 20-220). The summary does not equal the sum of details (820) — it is not a simple total. Possibly a quota/target vs. actual contributions, or the summary covers a larger group than the surviving detail cords.

**Reading:** A tribute account. Light brown = the assessment or target. Dark brown = individual contributions toward it.

### Example B: Census (Quipu 1000163, AMNH 41.2/5786)

**Form type:** Simple list (C)

19 white cords, all values ≤ 10:

| Value | Cords |
|-------|-------|
| 4 | 14 |
| 2 | 3 |
| 5 | 1 |
| 3 | 1 |

**Total: 70 across 19 cords.**

Fourteen entries of "4 white." This is the most formulaic quipu in the dataset — 74% of cords record the identical value. Fourteen households of 4, fourteen tribute payers each owing 4 units, or fourteen work groups of 4 laborers.

**Reading:** A census or labor roster. White = people. The dominance of "4" suggests a standard household/work-unit size.

### Example C: The Blank-to-Filled Pipeline

Combining all findings, here is how a quipucamayoc filled out a form:

1. **Choose the form type** based on task (census → simple list; tribute → grouped account; imperial summary → deep hierarchy)
2. **Hang pendant cords** in color batches — one block per commodity (white for people, browns for goods, blue/green for highland products)
3. **Insert red singleton dividers** between major sections (possibly marking the state's share)
4. **Add E-E-E labels** where a section needs a name/category marker
5. **Tie knots** — predominantly in tens (the standard unit), with small numbers (1-4) for individual counts
6. **Add subsidiaries** selectively — not as subtotals, but as annotations (corrections, subdivisions, cross-references)

## 7. What This Proves

The filled forms confirm the four-device model:

- **Knots** record quantities in a decimal system dominated by the standard unit 10
- **Colors** batch by commodity in contiguous blocks (not interleaved)
- **Red** divides sections as singleton markers between different colors
- **E-E-E** labels sections without predicting values (like column headers)

The most common "sentence" in the quipu corpus is: **white cord, value 1-4**. The Inca bureaucracy's bread and butter was counting people in small groups.

The second most common pattern is: **any color, value 10**. Ten is the universal accounting unit — the Inca equivalent of "per dozen" or "per hundred."

## Limitations

- Cord ordinal data is unreliable in the 2012 KDB (multiple cords share ordinal 1). Positional analysis used CORD_ID ordering as proxy.
- Only 7 EEE-to-next-cord transitions could be traced. Larger sample needed.
- The "white = people" interpretation is inferential, based on the census-like distribution, not proven.
- 219 quipu in the 2012 KDB had cord data vs. 619 in OKR. Coverage is partial.
- Knot value decoding (KNOT_VALUE_DECIMAL) was pre-computed by the database creators; independent verification of Ascher decoding was not performed.

## Files

- This report: `~/workspace/quipu-analysis/filled-forms.md`
- Data: `khipudb_2012.db` (KNOT.KNOT_VALUE_DECIMAL), `okr-khipu.db` (cord/khipu metadata)
