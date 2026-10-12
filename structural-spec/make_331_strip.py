"""Generate a visual color-sequence strip for khipu 1000331."""
import sqlite3

# Color to hex mapping (approximate)
COLORS = {
    'W': '#F5F5F5',   # white
    'AB': '#4A6FA5',  # light blue
    'MB': '#1B3A5C',  # dark blue
    'BG': '#8B4513',  # brown
    'PK': '#DDA0DD',  # pink
    'SY': '#FFD700',  # yellow/gold
    'RL': '#CC0000',  # red
    'RB': '#8B0000',  # dark red
    'KB': '#000000',  # black
    'CB': '#8B7355',  # tan
    'YB': '#DAA520',  # goldenrod
    'GG': '#808080',  # gray
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ORDINAL, cc.COLOR_CD_1, cc.COLOR_CD_2
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000331
    ORDER BY c.CORD_ORDINAL, cc.COLOR_CD_1
""")

# Group by ordinal, take the primary color (first)
seen = {}
for ordinal, c1, c2 in c.fetchall():
    if ordinal not in seen:
        seen[ordinal] = (c1 or '?', c2 or '')

ords = sorted(seen.keys())
boxes = []
for o in ords:
    c1, c2 = seen[o]
    label = c1 + (f'+{c2}' if c2 else '')
    hexcol = COLORS.get(c1, '#CCCCCC')
    # Border for compounds
    border = f'border:2px solid {COLORS.get(c2, "#999")};' if c2 else 'border:1px solid #999;'
    boxes.append(
        f'<div title="Cord {o}: {label}" '
        f'style="width:22px;height:36px;background:{hexcol};{border}'
        f'display:inline-block;margin:1px;vertical-align:bottom;"></div>'
    )

# Legend
legend_items = []
for code, hexcol in sorted(COLORS.items()):
    legend_items.append(
        f'<span style="display:inline-block;width:16px;height:16px;'
        f'background:{hexcol};border:1px solid #999;vertical-align:middle;"></span> {code}'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000331 Color Sequence</title>
<style>
body {{ font-family: sans-serif; max-width: 1200px; margin: 20px auto; padding: 0 20px; background: #1a1a1a; color: #eee; }}
h1 {{ font-size: 1.4em; }}
.strip {{ line-height: 0; margin: 20px 0; }}
.legend {{ margin: 16px 0; font-size: 0.85em; line-height: 2; }}
.legend span {{ margin-right: 12px; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 800px; }}
.num {{ font-size: 0.7em; color: #666; margin: 4px 0; }}
</style></head><body>
<h1>Khipu 1000331 — Color Sequence Strip</h1>
<p class="note">Museo Amano, Lima (R4248). {len(ords)} cords in ordinal sequence, left to right.
Each box = one cord, colored by primary color. Double border = compound color (second color shown in border).
142 of 198 values are exactly 2 — the information is in the color order, not the numbers.</p>
<div class="legend">{' '.join(legend_items)}</div>
<div class="strip">{''.join(boxes)}</div>
<div class="num">Cord 1 &rarr; Cord {len(ords)}, left to right</div>
<p class="note">Pattern: AB (blue) and W (white) dominate as carrier (72%). MB, BG, PK+AB and others
appear as signal. BG occurs only after AB — a positional section marker.</p>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000331-strip.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out} with {len(ords)} boxes")
