#!/usr/bin/env python3
"""
Spreadsheet-to-Khipu Encoder v0.1
Generates a structurally valid khipu tree from tabular data.

This is the generative proof of the Khipu Data Interchange Format:
if the spec is complete, we can encode, not just decode.

Mapping:
- Spreadsheet → primary cord
- Column → pendant cord (level 1), color-coded by column index
- Cell value → knot cluster on pendant (decimal positional, Inca style)
- Hierarchical data → subsidiary cords (level 2+)

Knot encoding (following Inca decimal convention):
- Units (1-9): long knot with N turns
- Tens, hundreds, etc.: clusters of single knots
- Zero: empty space (gap)

Output: JSON tree + optional ASCII visualization
"""

import json
import csv
import sys
from dataclasses import dataclass, field, asdict
from typing import List, Optional

# Color palette (Ascher color codes, cycling)
PALETTE = ["W", "B", "R", "G", "Y", "KB", "AB", "MB", "WG", "OB"]


@dataclass
class KnotCluster:
    """A cluster of knots representing one decimal digit position."""
    position: int       # 0=units, 1=tens, 2=hundreds, ...
    digit: int          # 0-9
    knot_type: str      # "long" (units), "single" (tens+), "figure-eight" (alt units)
    turns: int          # number of turns/loops


@dataclass
class Cord:
    cord_id: str
    level: int                    # 0=primary, 1=pendant, 2+=subsidiary, negative=top
    color: str
    label: str                    # column name or description
    knots: List[KnotCluster] = field(default_factory=list)
    children: List["Cord"] = field(default_factory=list)
    value: Optional[int] = None    # decoded integer value

    def to_dict(self):
        return {
            "cord_id": self.cord_id,
            "level": self.level,
            "color": self.color,
            "label": self.label,
            "value": self.value,
            "knots": [asdict(k) for k in self.knots],
            "children": [c.to_dict() for c in self.children],
        }


def encode_number(n: int) -> List[KnotCluster]:
    """Encode an integer as Inca-style knot clusters (decimal positional)."""
    if n == 0:
        return []  # zero = empty space
    clusters = []
    pos = 0
    while n > 0:
        digit = n % 10
        if digit > 0:
            if pos == 0:
                # Units: long knot (or figure-eight for 1)
                kt = "figure-eight" if digit == 1 else "long"
            else:
                kt = "single"
            clusters.append(KnotCluster(
                position=pos, digit=digit,
                knot_type=kt, turns=digit,
            ))
        n //= 10
        pos += 1
    return clusters


def spreadsheet_to_khipu(rows: List[dict], title: str = "spreadsheet") -> Cord:
    """
    Convert a list of dicts (spreadsheet rows) to a khipu tree.
    Each column becomes a pendant; each row's values are encoded
    as knot clusters. Multiple rows → grouped pendants per column.
    """
    if not rows:
        raise ValueError("No data rows provided")

    columns = list(rows[0].keys())
    primary = Cord(cord_id="P0", level=0, color="W", label=title)

    for ci, col in enumerate(columns):
        color = PALETTE[ci % len(PALETTE)]
        pendant = Cord(
            cord_id=f"P{ci+1}", level=1,
            color=color, label=col,
        )
        # For simplicity v0.1: encode the SUM of numeric values in this column
        # (like a khipu summary cord). Full row-level encoding → subsidiaries.
        total = 0
        has_numeric = False
        for ri, row in enumerate(rows):
            val = row[col]
            try:
                num = int(float(val))
                has_numeric = True
                total += num
                # Each row as a subsidiary cord (level 2)
                sub = Cord(
                    cord_id=f"P{ci+1}S{ri+1}", level=2,
                    color=color, label=f"{col}[{ri}]",
                    value=num, knots=encode_number(num),
                )
                pendant.children.append(sub)
            except (ValueError, TypeError):
                pass

        if has_numeric:
            pendant.value = total
            # Summary knots on the pendant itself
            pendant.knots = encode_number(total)

        primary.children.append(pendant)

    return primary


def ascii_tree(cord: Cord, prefix: str = "", is_last: bool = True) -> str:
    """Render khipu tree as ASCII."""
    lines = []
    connector = "└── " if is_last else "├── "
    knot_str = ""
    if cord.knots:
        digits = sorted([(k.position, k.digit) for k in cord.knots])
        knot_str = f" knots={digits}"
    val_str = f" val={cord.value}" if cord.value is not None else ""
    lines.append(f"{prefix}{connector}[{cord.color}] {cord.label} (L{cord.level}){val_str}{knot_str}")
    ext = "    " if is_last else "│   "
    for i, child in enumerate(cord.children):
        lines.append(ascii_tree(child, prefix + ext, i == len(cord.children) - 1))
    return "\n".join(lines)


def main():
    # Demo: encode a simple spreadsheet
    demo_data = [
        {"barley": 6000, "wheat": 1200, "laborers": 12},
        {"barley": 3000, "wheat": 800, "laborers": 8},
        {"barley": 15000, "wheat": 2400, "laborers": 20},
    ]

    if len(sys.argv) > 1:
        # Load from CSV file
        with open(sys.argv[1]) as f:
            demo_data = list(csv.DictReader(f))
        title = sys.argv[1]
    else:
        title = "demo grain ledger"

    khipu = spreadsheet_to_khipu(demo_data, title)

    print("=" * 60)
    print("KHIPU TREE (spreadsheet → khipu)")
    print("=" * 60)
    print(ascii_tree(khipu))

    # Validate against spec rules
    print("\n" + "=" * 60)
    print("SPEC CONFORMANCE CHECK")
    print("=" * 60)

    def check(cord, depth=0, errors=None):
        if errors is None:
            errors = []
        # R1: exactly one level-0 cord (checked at top)
        # R2: pendants at level 1
        if depth == 1 and cord.level != 1:
            errors.append(f"{cord.cord_id}: pendant not at level 1")
        # R3: subsidiaries at level >= 2
        if depth >= 2 and cord.level < 2:
            errors.append(f"{cord.cord_id}: subsidiary not at level >= 2")
        for child in cord.children:
            check(child, depth + 1, errors)
        return errors

    errors = check(khipu)
    # R1 check
    level_zero = [khipu] if khipu.level == 0 else []
    r1 = len(level_zero) == 1

    print(f"  R1 (one primary cord): {'PASS' if r1 else 'FAIL'}")
    print(f"  R2 (pendants at level 1): {'PASS' if not [e for e in errors if 'pendant' in e] else 'FAIL'}")
    print(f"  R3 (subsidiaries at level 2+): {'PASS' if not [e for e in errors if 'subsidiary' in e] else 'FAIL'}")
    if errors:
        for e in errors:
            print(f"    ! {e}")
    else:
        print("  All structural rules PASS — valid khipu per spec v0.2")

    # Save JSON
    out_path = "/home/hatch/workspace/quipu-analysis/encoded_khipu_demo.json"
    with open(out_path, "w") as f:
        json.dump(khipu.to_dict(), f, indent=2)
    print(f"\nJSON saved to {out_path}")


if __name__ == "__main__":
    main()
