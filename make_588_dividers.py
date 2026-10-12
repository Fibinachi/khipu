"""1000588 with double-blue dividers and 13-cord blocks marked."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'MB': '#1B3A5C', 'PG': '#FF69B4',
    'AB': '#4A6FA5', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
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
seq = [seen[o][1] for o in ords]

# find double-blue divider positions
dividers = set()
for i in range(len(seq)-1):
    if seq[i] == 'MB' and seq[i+1] == 'MB':
        dividers.add(ords[i])
        dividers.add(ords[i+1])

def box(o, cid, col, is_div):
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(10 + v * 1.5, 55) if v else 6
    border = '3px solid #ff4444' if is_div else '1px solid #555'
    return (f'<div title="Ord {o}: {col}={v}{" DIVIDER" if is_div else ""}" '
            f'style="width:8px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:{border};"></div>')

parts = []
for o in ords:
    cid, col = seen[o]
    parts.append(box(o, cid, col, o in dividers))

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000588 Dividers</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
.strip {{ line-height: 0; word-wrap: break-word; margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 6px; }}
</style></head><body>
<h1>Khipu 1000588 — Double-Blue Dividers</h1>
<p class="note">{len(ords)} cords. Red borders = MB+MB divider pairs.
7 dividers → 8 sections. Clean 13-cord blocks at 12–24, 25–37, 175–187.</p>
<div class="strip">{''.join(parts)}</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000588-dividers.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
