# Ascher Databook Notation System (reverse-engineered)

Based on OCR of sample entries (AS44, AS50, AS71, AS207, AS212).
Source: Ascher & Ascher, Code of the Quipu: Databook (1978) and Databook II (1988).

## Entry structure

Each khipu entry has three sections:
1. **Header page**: catalog ID, museum/owner identification, main cord color, cord placement map
2. **Data tables**: cord-by-cord measurements
3. **Observations**: numbered structural/arithmetic findings

## Catalog numbers

- Format: `AS` + number (AS10 through AS215)
- Databook I (1978): AS10–AS200 (191 entries)
- Databook II (1988): AS201–AS215 (15 entries)
- Suffix variants exist in OKR cross-references (e.g. AS207A) but the databook PDF is AS207

## Cord identifiers

| Code | Meaning |
|------|---------|
| `1`, `2`, `3`... | Pendant cord number (in attachment order) |
| `2s1`, `2s2` | Subsidiary cords: `NsM` = Mth subsidiary of pendant N |
| `T1`, `T2` | Top cords (cords tied around groups, not pendants) |
| `T1s1` | Subsidiary of a top cord |

## Knot notation

In the "Knots (no., type, position)" column:

| Code | Meaning |
|------|---------|
| `s` | Single (overhand) knot |
| `L` | Long knot (multiple turns) |
| `E` | Figure-eight knot |

Format: `{count}{type}({position_cm})`, multiple groups separated by `;`

Examples:
- `1s(15.5)` = 1 single knot at 15.5 cm from top
- `8s(15.0); 3L(24.5)` = 8 singles at 15.0 cm, 3 longs at 24.5 cm
- `1E(5.5)` = 1 figure-eight at 5.5 cm
- `--` = no knots
- `?` = unreadable/uncertain

Note: The Aschers do NOT record number of turns on long knots in the knot column
(the turn count must be inferred from their computed Value).

## Length column

- Format: `{number}{unit}`
- `¢` (cents symbol) = pendant cord (hangs from main cord)
- `b` = broken cord (incomplete, length is partial)
- No suffix = main cord or top cord measurement
- `?` = unmeasurable

## Color codes

Colors are abbreviated and combined with `:` for multicolor cords.

Observed codes (partial list):
| Code | Likely meaning |
|------|----------------|
| `W` | White |
| `B` | Brown |
| `LB` | Light brown |
| `BL` | Black |
| `DB` | Dark brown (?) |

Compound: `B:BL:W` = brown, black, and white plies twisted together.
`LB:W` = light brown and white.

Note: The Aschers' color abbreviations do NOT directly match OKR color codes.
A mapping table is needed for cross-referencing.

## Value column

The Aschers' computed decimal interpretation of the knots on each cord.

- Integer = their reading (e.g. `10`, `83`, `36`)
- `?` = no value (broken, no knots, or unreadable)
- `(3+)??` = uncertain, minimum 3
- `27(?)` = probably 27 but uncertain
- `0` = explicitly zero (e.g. top cord with no knots: T6 = 0)

Their decoding follows the standard: long knots = units (by turns), singles = tens/hundreds, figure-eight = 1.

## Subsidiaries column

Format: `{count}:{position}` or `{count}:{range}`, multiple separated by `,`

Examples:
- `1:9.0` = 1 subsidiary at 9.0 cm
- `1:9.0, 5:20.0-20.5` = subsidiary 1 at 9.0 cm, subsidiary 5 spanning 20.0-20.5 cm
- `2:16.5-17.0` = 2 subsidiaries between 16.5 and 17.0 cm

## Header: cord placement map

Page 1 gives physical layout along the main cord:
- `$ 3.0 cm: group of 6 pendant cords (1-6), tied with top cord (T1), then space of 0.5 cm.`
- `$` = start of main cord (sometimes `¢$`)
- Positions in cm from the start
- Groups, spaces, and top-cord bindings noted
- `*` marks mend points or anomalies
- `end ¢` = end of main cord

## Observations

Numbered findings about structural regularities. Two formats:
- Roman numerals: `(ii)`, `(iii)`, `(iv)` — older entries
- Arabic numerals: `1.`, `2.`, `5.` — later entries

These include:
- Color-pattern regularities
- Arithmetic relationships (top cord = sum of pendants)
- Positional regularities (which positions lack subsidiaries)
- Cross-group value correspondences
- Provenance/acquisition notes (excavation history, collector info)

## Cross-reference to OKR

OKR's `INVESTIGATOR_NUM` field contains the Ascher number (e.g. `AS207A`, `AS044`).
Note: OKR pads with zeros (AS044) and may add suffixes (AS207A) not in the databook.
