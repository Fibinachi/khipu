# Symbolic Transcription Notation for Anomalous Khipu

Version 1.0 — 2026-10-11. Designed for transcribing anomalous khipu.
(Companion to knot-alphabet.md, which enumerates corpus knot symbols.)
Extends as needed; additions logged at bottom.

## Line format

```
ORD [LEVEL] : COLOR : KNOTSEQ [FLAGS]
```

Example: `3:W:L4-S2-E` — cord ordinal 3, white, long knot (4 turns), then a cluster of 2 single knots, then a figure-eight.

Example: `^12(P3):AB:W:S3-L2` — subsidiary (level 2), ordinal 12, attached to parent cord 3, compound color AB:W, cluster of 3 singles then cluster with long knot (2 turns).

## Cord ordinal (ORD)

Integer = CORD_ORDINAL (physical order along main cord, top to bottom).

## Level markers (LEVEL)

| Mark | Meaning |
|------|---------|
| (none) | Level 1 — pendant on main cord |
| `^` | Level 2 — subsidiary |
| `^^` | Level 3 |
| `^^^` | Level 4+ (extend as needed) |
| `H:` | Prefix for primary/header cord (replaces ORD) |

Subsidiary attachment shown as `(P<n>)` where n = parent CORD_ORDINAL.

## Colors (COLOR)

Ascher color codes used verbatim (64 codes). Common:

| Code | Description |
|------|-------------|
| W | white / natural cotton |
| B | moderate yellowish brown |
| AB | light brown |
| MB | moderate brown |
| BB | dark yellowish brown |
| KB | dark brown |
| DB | deep brown |
| NB | (dark brown variant) |
| G | grayish olive green |
| GG | grayish green |
| 0G | light grayish olive |
| YB | light grayish yellowish brown |
| R | red |
| RL | red (light/bright) |
| RM | red (medium) |
| FR | strong reddish brown |
| BL | pale blue |
| BG | grayish blue |

Compound colors preserve operator and order: `AB:W` (colon), `W-AB` (hyphen/barber-pole), `B/W` (slash). Operator kept verbatim from database.

Missing/unrecorded color: `?`

## Knot types

From knot_type_dc + observed TYPE_CODE values:

| Symbol | Database | Description | Standard value |
|--------|----------|-------------|----------------|
| S | S | single / overhand knot | digit count (tens+) |
| L | L | long knot | turns = units digit |
| E | E | figure-eight knot | 1 |
| EE | EE | double figure-eight | (anomalous) |
| LL | LL | double long (two axes) | 3 (per Aschers) |
| BL | BL | belted long knot | long + outer wrap |
| SP | SP | spiral knot | like long knot |
| TF | TF | tufted knot | 1 |
| (empty) | '' | no TYPE_CODE recorded | — |

## Knot modifiers

Appended directly to type letter:

- **Turns:** `L4` = long knot with 4 turns (from NUM_TURNS). `S` never takes turns. `SP3` = spiral with 3 turns.
- **Direction:** append `z`, `s`, or `u` only when anomalous or explicitly noted. Default (Z-twist) omitted. Example: `Ss` = single knot with S-direction twist (unusual).
- **Axis:** `SP{U}` = spiral knot with axis orientation U; `SP{AXU}` etc. Raw AXIS_ORIENTATION value in braces. (Per 1000504: spiral knots with and without axis.)
- **Count:** consecutive identical knots collapsed: `S3` = three single knots in one cluster. `S13` = thirteen — no ambiguity since turns only apply to L/SP/BL.

## Cluster separator

`-` separates knot clusters (place-value groups), ordered **top to bottom** = highest place to units, matching physical layout.

## Special cord states

| Symbol | Meaning |
|--------|---------|
| `∅` | no knots on cord (empty) |
| `?` | knot data missing/unrecorded |
| `~` | cord broken / fragmentary |
| `*` | cord repaired or replaced (note in comment) |

## Flags (end of line)

| Flag | Meaning |
|------|---------|
| `[rev]` | knot order reversed (e.g., replaced upside-down, cf. 1000201) |
| `[loop]` | cord end formed into loop |
| `[mended]` | cord mended |
| `[loose]` | attachment loose / movable |
| `[modern]` | modern repair thread present |
| `[sig:<color>@<cm>]` | signal/marker thread (señal) of color at cm from main cord |
| `[thr:<color>]` | short cord tied through knot (cf. 1000183) |
| `[tiedto:P<n>]` | cord end tied to another pendant |

## Comments

Lines starting with `#` are comments (anomaly notes, provenance).

## Worked example

```
# 1000201 — Pendant 70 replaced upside down (knot order reversed)
70:W:S6-L5-E[rev]
# 1000183 — Short YB:0G cord tied through the long knot
4:YB:S2-L3[thr:YB:0G]-S1
```

## Notation extensions log

- v1.0 (2026-10-11): initial scheme.
- v1.1 (2026-10-11): axis orientation for SP knots as `SP{value}` (raw AXIS_ORIENTATION); subsidiary ordinal format `3s1` (parent ordinal + s + sibling index) for CSV CORD_ORDINAL column.
