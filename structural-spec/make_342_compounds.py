"""1000342 strip with MB+B compounds boxed as units."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'YB': '#C9A227', 'MB': '#1B3A5C', 'B': '#0000CC',
    'BS': '#8B5A2B', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1
    FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000342 ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, (col or '?').strip())
ords = sorted(seen.keys())

# Build elements: group MB+B into compounds
elements = []
i = 0
while i < len(ords):
    o = ords[i]
    cid, col = seen[o]
    if col == 'MB' and i + 1 < len(ords) and seen[ords[i+1]][1] == 'B':
        # compound
        cid2, _ = seen[ords[i+1]]
        elements.append(('compound', [(o, cid, 'MB'), (ords[i+1], cid2, 'B')]))
        i += 2
    else:
        elements.append(('single', [(o, cid, col)]))
        i += 1

n_compounds = sum(1 for t, _ in elements if t == 'compound')
print(f"{len(elements)} elements, {n_compounds} MB+B compounds")

def box(o, cid, col):
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(10 + v * 1.5, 60) if v else 6
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:8px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;"></div>')

parts = []
for typ, cords in elements:
    if typ == 'compound':
        inner = ''.join(box(o, cid, col) for o, cid, col in cords)
        o0 = cords[0][0]
        parts.append(
            f'<span title="Compound MB+B at ord {o0}" '
            f'style="display:inline-block;border:2px solid #ff4444;'
            f'border-radius:3px;padding:1px;margin:1px;vertical-align:bottom;'
            f'line-height:0;">{inner}</span>'
        )
    else:
        o, cid, col = cords[0]
        parts.append(box(o, cid, col))

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000342 Compounds</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
.strip {{ line-height: 0; word-wrap: break-word; margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 6px; }}
</style></head><body>
<h1>Khipu 1000342 — MB+B Compounds Boxed</h1>
<p class="note">{len(ords)} cords → {len(elements)} elements. {n_compounds} MB+B compounds outlined in red.
Red boxes = compound fields (MB always followed by B, directional).</p>
<div class="strip">{''.join(parts)}</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000342-compounds.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
