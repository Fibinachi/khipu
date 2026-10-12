"""Color strip for 1000029 (all-U direction piece)."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'AB': '#4A6FA5', 'MB': '#1B3A5C', 'BG': '#8B4513',
    'BY': '#FFD700', 'BL': '#000080', 'KB': '#1a1a1a', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

c.execute("""
    SELECT MUSEUM_NAME, MUSEUM_NUM, PROVENANCE, REGION
    FROM khipu_main WHERE KHIPU_ID = 1000029
""")
prov = c.fetchone()
print(f"Provenance: {prov}")

c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, c.CORD_LEVEL, cc.COLOR_CD_1
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000029
    ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, lvl, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, lvl, (col or '?').strip())

ords = sorted(seen.keys())
print(f"{len(ords)} cords")

from collections import Counter
cc = Counter(seen[o][2] for o in ords)
print(f"Colors: {dict(cc)}")

# Direction check
c.execute("""
    SELECT k.DIRECTION, COUNT(*)
    FROM knot k JOIN cord c ON k.CORD_ID = c.CORD_ID
    WHERE c.KHIPU_ID = 1000029 GROUP BY k.DIRECTION
""")
print("Directions:")
for row in c.fetchall():
    print(f"  {row[0]}: {row[1]}")

boxes = []
for o in ords:
    cid, lvl, col = seen[o]
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(12 + v * 1.5, 70) if v else 8
    boxes.append(
        f'<div title="Ord {o} L{lvl}: {col}={v}" '
        f'style="width:11px;height:{h}px;background:{hexcol};'
        f'display:inline-block;margin:1px;vertical-align:bottom;'
        f'border:1px solid #555;"></div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000029 Strip</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
.strip {{ line-height: 0; word-wrap: break-word; margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 6px; }}
</style></head><body>
<h1>Khipu 1000029 — All-U Direction</h1>
<p class="note">{len(ords)} cords. Bar height = value.
Provenance: {prov[0] if prov else '?'} / {prov[2] if prov and len(prov)>2 else '?'}, {prov[3] if prov and len(prov)>3 else '?'}.</p>
<div class="strip">{''.join(boxes)}</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000029-strip.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
