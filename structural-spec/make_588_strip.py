"""Color strip for 1000588 (largest unstructured, near Lima)."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'AB': '#4A6FA5', 'MB': '#1B3A5C', 'BG': '#8B4513',
    'BY': '#FFD700', 'BL': '#000080', 'KB': '#1a1a1a', 'SR': '#CC4444',
    'B': '#0000CC', 'LB': '#C4A77D', 'FB': '#4169E1', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("SELECT MUSEUM_NAME, MUSEUM_NUM, PROVENANCE FROM khipu_main WHERE KHIPU_ID=1000588")
prov = c.fetchone()
print(f"Provenance: {prov}")

c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1
    FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000588 ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, (col or '?').strip())
ords = sorted(seen.keys())
print(f"{len(ords)} ordinals")

from collections import Counter
cc = Counter(seen[o][1] for o in ords)
print(f"Colors: {dict(cc.most_common(8))}")

boxes = []
for o in ords:
    cid, col = seen[o]
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(10 + v * 1.5, 60) if v else 6
    boxes.append(
        f'<div title="Ord {o}: {col}={v}" '
        f'style="width:8px;height:{h}px;background:{hexcol};'
        f'display:inline-block;margin:1px;vertical-align:bottom;'
        f'border:1px solid #555;"></div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000588 Strip</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
.strip {{ line-height: 0; word-wrap: break-word; margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 6px; }}
</style></head><body>
<h1>Khipu 1000588 — Unstructured (unknown prov.)</h1>
<p class="note">{len(ords)} ordinals. Bar height = value.
Provenance: {prov[0] if prov else '?'} / {prov[2] if prov and len(prov)>2 else '?'}.
No detected row structure. Flat, level 1.</p>
<div class="strip">{''.join(boxes)}</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000588-strip.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
