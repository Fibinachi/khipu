#!/usr/bin/env python3
"""Diagram of the meta-khipu: a khipu cataloging all 619 khipu in the OKR database."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches

fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis("off")

# Colors
PENDANT_COLORS = {"khipu_id": "#f5f5f0", "n_cords": "#7d522d",
                  "n_knotted": "#a52a2a", "n_colors": "#4a7c59"}
EDGE = "#333333"

# Primary cord (horizontal, top)
ax.add_patch(patches.Rectangle((1, 8.6), 14, 0.28, facecolor="#e8e0d0",
                               edgecolor=EDGE, linewidth=1.5, zorder=2))
ax.text(8, 8.98, "PRIMARY  ·  khipu catalog  ·  619 khipu", ha="center", va="center",
        fontsize=11, fontweight="bold", family="monospace")

pendants = [
    ("khipu_id", "619 khipu IDs", None),
    ("n_cords", "54,403 total cords", "54,403"),
    ("n_knotted", "37,082 knotted cords", "37,082"),
    ("n_colors", "3,103 color entries", "3,103"),
]

x_positions = [3.0, 6.3, 9.6, 12.9]

for i, (key, label, total) in enumerate(pendants):
    x = x_positions[i]
    col = PENDANT_COLORS[key]
    # Pendant cord (vertical)
    ax.add_patch(patches.Rectangle((x - 0.14, 2.2), 0.28, 6.4,
                                   facecolor=col, edgecolor=EDGE, linewidth=1.2, zorder=2))
    # Label
    ax.text(x, 1.85, key, ha="center", va="top", fontsize=10,
            fontweight="bold", family="monospace")
    ax.text(x, 1.45, label, ha="center", va="top", fontsize=8,
            family="monospace", color="#555")
    # Knot cluster on pendant (summary value) — stacked rectangles
    if total:
        digits = total.replace(",", "")
        ky = 7.6
        for d in digits:
            n = int(d)
            # draw n small knot ticks
            for t in range(n):
                ax.add_patch(patches.Rectangle((x - 0.22, ky), 0.44, 0.09,
                                               facecolor=EDGE, zorder=3))
                ky -= 0.14
            ky -= 0.12  # gap between digit positions

    # Subsidiaries: show first 12 as thin lines fanning out, then ellipsis
    n_show = 12
    for s in range(n_show):
        sx = x - 0.55 + s * 0.1
        ax.plot([x, sx], [2.2, 0.55], color=col, linewidth=0.8,
                alpha=0.7, zorder=1)
        ax.add_patch(patches.Circle((sx, 0.5), 0.045, facecolor=col,
                                    edgecolor=EDGE, linewidth=0.5, zorder=2))
    ax.text(x, 0.18, "619 subsidiaries\n(one per khipu)", ha="center", va="top",
            fontsize=7, family="monospace", color="#777", style="italic")

# Title and annotations
ax.text(8, 9.6, "META-KHIPU — a khipu cataloging 619 khipu", ha="center",
        fontsize=14, fontweight="bold")
ax.text(8, 9.28, "Each pendant summarizes one database field; each subsidiary encodes one khipu's value  ·  R1–R3 conformant",
        ha="center", fontsize=9, color="#555", style="italic")

# Legend
ax.text(0.3, 0.3, "Generated 2026-10-12  ·  spreadsheet_to_khipu.py  ·  khipu_catalog_khipu.json",
        fontsize=7, color="#999", family="monospace")

plt.tight_layout()
out = "/home/hatch/workspace/quipu-analysis/meta_khipu_diagram.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Wrote {out}")
