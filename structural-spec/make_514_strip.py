"""Color/value strip for 1000514 (most anomalous khipu)."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'AB': '#4A6FA5', 'MB': '#1B3A5C', 'BG': '#8B4513',
    'BY': '#FFD700', 'BL': '#000080', 'SP': '#FF6B6B', 'EE': '#90EE90',
    'LL': '#DDA0DD', 'TF': '#FFA500', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

# Provenance
c.execute("""
    SELECT MUSEUM_NAME, MUSEUM_NUM, PROVENANCE, REGION
    FROM khipu_main WHERE KHIPU_ID = 1000514
""")
prov = c.fetchone()
print(f"Provenance: {prov}")
print()

c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, c.CORD_LEVEL, cc.COLOR_CD_1
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000514
    ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, lvl, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, lvl, (col or '?').strip())

ords = sorted(seen.keys())
print(f"\n{len(ords)} cords")

boxes = []
vals = []
for o in ords:
    cid, lvl, col = seen[o]
    hexcol = COLORS.get(col, '#CCCCCC')
    try:
        v = decode_cord(conn, cid)['value']
    except:
        v = 0
    vals.append((o, col, v))
    h = min(12 + (v or 0) * 2, 70) if v else 8
    w = 14 if lvl == 1 else 10
    opacity = '1.0' if lvl == 1 else '0.6'
    boxes.append(
        f'<div title="Ord {o} L{lvl}: {col}={v}" '
        f'style="width:{w}px;height:{h}px;background:{hexcol};opacity:{opacity};'
        f'display:inline-block;margin:1px;vertical-align:bottom;'
        f'border:1px solid #555;"></div>'
    )

nz = [(o, col, v) for o, col, v in vals if v]
print(f"Nonzero: {len(nz)}/{len(vals)}")
print(f"Value range: {min(v for _,_,v in nz) if nz else 0} to {max(v for _,_,v in nz) if nz else 0}")
print(f"Top 15 values: {sorted([(v,o,col) for o,col,v in nz], reverse=True)[:15]}")

from collections import Counter
cc = Counter(col for _, col, _ in vals)
print(f"Colors: {dict(cc)}")

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000514 Strip</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
.strip {{ line-height: 0; word-wrap: break-word; margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 6px; }}
</style></head><body>
<h1>Khipu 1000514 — Color/Value Strip</h1>
<p class="note">{len(ords)} cords. {len(nz)} nonzero. Bar height = value.
Provenance: {prov[0] if prov else 'unknown'} / {prov[2] if prov and len(prov)>2 else 'unknown'}.
SP = red-pink, EE = light green. These are the anomaly-dense colors.</p>
<div class="strip">{''.join(boxes)}</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000514-strip.html'
with open(out, 'w') as f:
    f.write(html)
print(f"\nWrote {out}")
