"""Color/value strip for khipu 1000344 (rectangular table, Paris)."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'AB': '#4A6FA5', 'MB': '#1B3A5C', 'BG': '#8B4513',
    'PK': '#DDA0DD', 'SY': '#FFD700', 'RL': '#CC0000', 'RB': '#8B0000',
    'KB': '#000000', 'CB': '#8B7355', 'YB': '#DAA520', 'GG': '#808080',
    'BY': '#F0E68C', 'BL': '#000080',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, c.CORD_LEVEL, cc.COLOR_CD_1, cc.COLOR_CD_2
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000344
    ORDER BY c.CORD_ORDINAL, cc.COLOR_CD_1
""")
seen = {}
for cid, o, lvl, c1, c2 in c.fetchall():
    if o not in seen:
        seen[o] = (cid, lvl, (c1 or '?').strip(), (c2 or '').strip())
ords = sorted(seen.keys())

boxes = []
vals = []
for o in ords:
    cid, lvl, c1, c2 = seen[o]
    try:
        v = decode_cord(conn, cid)['value'] or 0
    except:
        v = 0
    vals.append(v)
    label = f'{c1}' + (f'+{c2}' if c2 else '') + f' L{lvl}={v}'
    hexcol = COLORS.get(c1, '#CCCCCC')
    border = 'border:1px solid #555;'
    # Height by value, width by level (deeper = narrower, offset)
    h = min(15 + v * 2, 90) if v else 12
    indent = (lvl - 1) * 4 if lvl and lvl > 1 else 0
    boxes.append(
        f'<div title="Cord {o}: {label}" '
        f'style="width:14px;height:{h}px;background:{hexcol};{border}'
        f'display:inline-block;margin:1px;margin-left:{1+indent}px;'
        f'vertical-align:bottom;"></div>'
    )

from collections import Counter
ccount = Counter(seen[o][2] for o in ords)
lvlcount = Counter(seen[o][1] for o in ords)
n = len(ords)
nz = sum(1 for v in vals if v != 0)

legend_items = []
for code in sorted(ccount.keys()):
    hexcol = COLORS.get(code, '#CCCCCC')
    legend_items.append(
        f'<span style="display:inline-block;width:14px;height:14px;'
        f'background:{hexcol};border:1px solid #999;vertical-align:middle;"></span> '
        f'{code}({ccount[code]})'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000344 Rectangular Table</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #1a1a1a; color: #eee; }}
h1 {{ font-size: 1.4em; }}
.strip {{ line-height: 0; margin: 20px 0; border-bottom: 2px solid #444; padding-bottom: 4px; }}
.legend {{ margin: 14px 0; font-size: 0.8em; line-height: 2; }}
.legend span {{ margin-right: 10px; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000344 — "Rectangular Table" (Musée Quai Branly, Paris)</h1>
<p class="note">71.1930.19.470. {n} cords, {nz} nonzero ({100*nz//n}%).
Levels: {dict(lvlcount)}. Value range 0–{max(vals) if vals else 0}.
Bar height = value. Deeper-level cords offset right.
Ascher notes: P10's finishing knot tied around P11; small spaces between some pendants.</p>
<div class="legend">{' '.join(legend_items)}</div>
<div class="strip">{''.join(boxes)}</div>
<div class="note">Cord 1 &rarr; Cord {n}, left to right.</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000344-strip.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}: {n} boxes")
print(f"Colors: {dict(ccount.most_common(10))}")
print(f"Levels: {dict(lvlcount)}")
print(f"Value stats: min={min(vals)} max={max(vals)} nonzero={nz}/{n}")
