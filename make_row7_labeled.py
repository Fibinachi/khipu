"""Row 7 (157-176) with ordinal labels on each cord."""
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
    WHERE c.KHIPU_ID = 1000588 AND c.CORD_ORDINAL BETWEEN 157 AND 176
    ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, (col or '?').strip())
ords = sorted(seen.keys())

boxes = []
for idx, o in enumerate(ords, 1):
    cid, col = seen[o]
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    # dark text on light, light text on dark
    tc = '#000' if col in ('W',) else '#fff'
    boxes.append(
        f'<div title="Ord {o}: {col}={v}" '
        f'style="width:34px;height:44px;background:{hexcol};'
        f'display:inline-block;margin:2px;vertical-align:bottom;'
        f'border:1px solid #555;border-radius:3px;text-align:center;'
        f'color:{tc};font-size:10px;line-height:1.2;padding-top:4px;">'
        f'<b>#{idx}</b><br>{o}<br>{col}</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Row 7 Labeled</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
.strip {{ line-height: 1; margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 6px; }}
</style></head><body>
<h1>Row 7 (ords 157–176) — Labeled</h1>
<p class="note">#N = position in row, then ordinal, then color. Point at the numbers.</p>
<div class="strip">{''.join(boxes)}</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000588-row7-labeled.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
