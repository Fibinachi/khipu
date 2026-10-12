"""Color/value strip for 1000608 (Khipu del Aji, 2-color)."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'AB': '#4A6FA5', 'MB': '#1B3A5C', 'BG': '#8B4513',
    'BY': '#FFD700', 'BL': '#000080', 'R': '#CC0000', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

c.execute("""
    SELECT MUSEUM_NAME, MUSEUM_NUM, PROVENANCE, REGION, NICKNAME
    FROM khipu_main WHERE KHIPU_ID = 1000608
""")
prov = c.fetchone()
print(f"Provenance: {prov}")

c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, c.CORD_LEVEL, cc.COLOR_CD_1
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000608
    ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, lvl, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, lvl, (col or '?').strip())

ords = sorted(seen.keys())
print(f"{len(ords)} cords")

from collections import Counter
cc = Counter()
vals = []
for o in ords:
    cid, lvl, col = seen[o]
    cc[col] += 1
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    vals.append(v)
print(f"Colors: {dict(cc)}")
print(f"Nonzero: {sum(1 for v in vals if v)}/{len(vals)}")
print(f"Range: {min(vals)}-{max(vals)}")

boxes = []
for o in ords:
    cid, lvl, col = seen[o]
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(12 + v * 1.5, 70) if v else 8
    boxes.append(
        f'<div title="Ord {o}: {col}={v}" '
        f'style="width:13px;height:{h}px;background:{hexcol};'
        f'display:inline-block;margin:1px;vertical-align:bottom;'
        f'border:1px solid #555;"></div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000608 Strip</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
.strip {{ line-height: 0; word-wrap: break-word; margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 6px; }}
</style></head><body>
<h1>Khipu 1000608 — "Khipu del Aji"</h1>
<p class="note">{len(ords)} cords. Bar height = value.
Provenance: {prov[0] if prov else '?'} / {prov[2] if prov and len(prov)>2 else '?'}, {prov[3] if prov and len(prov)>3 else '?'}.
Two-color inventory candidate.</p>
<div class="strip">{''.join(boxes)}</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000608-strip.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
