#!/usr/bin/env python3
"""Diagram of the first khipu produced by the spreadsheet-to-khipu encoder (demo grain ledger)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(14, 9))
ax.set_xlim(0, 14)
ax.set_ylim(0, 9)
ax.axis("off")

EDGE = "#333333"

# Primary cord
ax.add_patch(patches.Rectangle((1, 7.6), 12, 0.28, facecolor="#e8e0d0",
                               edgecolor=EDGE, linewidth=1.5, zorder=2))
ax.text(7, 7.98, "PRIMARY  ·  grain ledger", ha="center", va="center",
        fontsize=11, fontweight="bold", family="monospace")

# Pendants: (key, color, total, subsidiaries)
pendants = [
    ("barley", "#f5f5f0", "24,000", [6000, 3000, 15000]),
    ("wheat", "#7d522d", "4,400", [1200, 800, 2400]),
    ("laborers", "#a52a2a", "40", [12, 8, 20]),
]
x_positions = [3.5, 7.0, 10.5]

for i, (key, col, total, subs) in enumerate(pendants):
    x = x_positions[i]
    # Pendant cord
    ax.add_patch(patches.Rectangle((x - 0.16, 2.6), 0.32, 5.0,
                                   facecolor=col, edgecolor=EDGE, linewidth=1.2, zorder=2))
    ax.text(x, 2.25, key, ha="center", va="top", fontsize=11,
            fontweight="bold", family="monospace")
    ax.text(x, 1.85, total, ha="center", va="top", fontsize=10,
            family="monospace", color="#333")

    # Knot clusters on pendant (decimal digits of total)
    digits = total.replace(",", "")
    ky = 7.0
    for d in digits:
        n = int(d)
        for t in range(n):
            ax.add_patch(patches.Rectangle((x - 0.26, ky), 0.52, 0.1,
                                           facecolor=EDGE, zorder=3))
            ky -= 0.15
        ky -= 0.14

    # Subsidiaries (one per row)
    for s, val in enumerate(subs):
        sx = x - 0.5 + s * 0.5
        ax.plot([x, sx], [2.6, 1.0], color=col, linewidth=1.0, alpha=0.8, zorder=1)
        # knot ticks for the value
        dstr = str(val)
        vy = 0.95
        for d in dstr:
            n = int(d)
            for t in range(min(n, 9)):
                ax.add_patch(patches.Rectangle((sx - 0.09, vy), 0.18, 0.045,
                                               facecolor=EDGE, zorder=3))
                vy -= 0.07
            vy -= 0.06
        ax.add_patch(patches.Circle((sx, 0.35), 0.06, facecolor=col,
                                    edgecolor=EDGE, linewidth=0.6, zorder=2))
        ax.text(sx, 0.12, str(val), ha="center", va="top", fontsize=7,
                family="monospace", color="#555")

ax.text(7, 8.6, "THE FIRST NEW KHIPU", ha="center", fontsize=15, fontweight="bold")
ax.text(7, 8.28, "Encoded from a spreadsheet by the khipu compiler  ·  2026-10-12  ·  R1–R3 conformant",
        ha="center", fontsize=9, color="#555", style="italic")

ax.text(0.3, 0.2, "spreadsheet_to_khipu.py  ·  github.com/Fibinachi/khipu",
        fontsize=7, color="#999", family="monospace")

plt.tight_layout()
out = "/home/hatch/workspace/quipu-analysis/structural-spec/first_new_khipu.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Wrote {out}")
