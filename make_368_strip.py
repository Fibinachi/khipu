"""Color-sequence strip for khipu 1000368 (all-U journal)."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'AB': '#4A6FA5', 'MB': '#1B3A5C', 'BG': '#8B4513',
    'PK': '#DDA0DD', 'SY': '#FFD700', 'RL': '#CC0000', 'RB': '#8B0000',
    'KB': '#000000', 'CB': '#8B7355', 'YB': '#DAA520', 'GG': '#808080',
    'LB': '#ADD8E6', 'BB': '#00008B',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1, cc.COLOR_CD_2
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000368
    ORDER BY c.CORD_ORDINAL, cc.COLOR_CD_1
""")
seen = {}
for cid, o, c1, c2 in c.fetchall():
    if o not in seen:
        seen[o] = (cid, c1 or '?', c2 or '')
ords = sorted(seen.keys())

boxes = []
for o in ords:
    cid, c1, c2 = seen[o]
    result = decode_cord(conn, cid)
    val = result['value']
    label = f'{c1}' + (f'+{c2}' if c2 else '') + f'={val}'
    hexcol = COLORS.get(c1, '#CCCCCC')
    border = f'border:2px solid {COLORS.get(c2, "#999")};' if c2 else 'border:1px solid #555;'
    # Height scaled by value (journal: values matter)
    h = min(20 + (val or 0) * 3, 80)
    boxes.append(
        f'<div title="Cord {o}: {label}" '
        f'style="width:18px;height:{h}px;background:{hexcol};{border}'
        f'display:inline-block;margin:1px;vertical-align:bottom;"></div>'
    )

# Value sparkline data
vals = []
for o in ords:
    cid = seen[o][0]
    vals.append(decode_cord(conn, cid)['value'] or 0)

# Stats
from collections import Counter
ccount = Counter(seen[o][1] for o in ords)
n = len(ords)
nz = sum(1 for v in vals if v != 0)

legend_items = []
for code, hexcol in sorted(COLORS.items()):
    if code in ccount:
        legend_items.append(
            f'<span style="display:inline-block;width:14px;height:14px;'
            f'background:{hexcol};border:1px solid #999;vertical-align:middle;"></span> '
            f'{code}({ccount[code]})'
        )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000368 Color/Value Strip</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #1a1a1a; color: #eee; }}
h1 {{ font-size: 1.4em; }}
.strip {{ line-height: 0; margin: 20px 0; border-bottom: 2px solid #444; padding-bottom: 4px; }}
.legend {{ margin: 14px 0; font-size: 0.8em; line-height: 2; }}
.legend span {{ margin-right: 10px; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000368 — Color/Value Sequence Strip</h1>
<p class="note">Percy Dauelsberg collection, Arica, Chile. {n} cords, MI ratio 2.26 (highest in corpus).
One of five all-U-twist unknown-office pieces. Bar height = decoded knot value.
{nz}/{n} nonzero ({100*nz//n}%). Ascher notes: marker M1 (KB wrapped with SY) divides khipu into 2 parts;
pendant cords threaded with contrasting colors.</p>
<div class="legend">{' '.join(legend_items)}</div>
<div class="strip">{''.join(boxes)}</div>
<div class="note">Cord 1 &rarr; Cord {n}, left to right. Taller bars = larger values.
This is a sequential journal — values vary meaningfully along the sequence (unlike 1000331's constant 2s).</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/journal-hunt/1000368-strip.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}: {n} boxes, {nz} nonzero")
print(f"Value range: {min(vals)}-{max(vals)}, colors: {dict(ccount.most_common(8))}")
