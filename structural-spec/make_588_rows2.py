"""1000588 broken into rows at each divider."""
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

# divider end positions (ordinal of last MB in the pair)
divider_ends = set()
for i in range(len(seq)-5):
    if (seq[i] == 'W' and seq[i+1] == 'W' and seq[i+2] in ('MB','PG')
        and seq[i+3] == 'W' and seq[i+4] == 'MB' and seq[i+5] == 'MB'):
        divider_ends.add(ords[i+5])
# manual split: row 6 tail becomes new row 7
manual_breaks = {156}

# divider start positions (for red banding)
divider_starts = set()
for i in range(len(seq)-5):
    if (seq[i] == 'W' and seq[i+1] == 'W' and seq[i+2] in ('MB','PG')
        and seq[i+3] == 'W' and seq[i+4] == 'MB' and seq[i+5] == 'MB'):
        for j in range(6):
            divider_starts.add(ords[i+j])

def box(o, cid, col, is_div):
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(10 + v * 1.5, 50) if v else 6
    border = '2px solid #ff4444' if is_div else '1px solid #555'
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:10px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:{border};"></div>')

rows = []
current = []
row_n = 0
for o in ords:
    cid, col = seen[o]
    current.append(box(o, cid, col, o in divider_starts))
    if o in divider_ends or o == 156:
        row_n += 1
        rows.append((row_n, len(current), ''.join(current)))
        current = []
if current:
    row_n += 1
    rows.append((row_n, len(current), ''.join(current)))

row_html = []
for n, length, content in rows:
    row_html.append(
        f'<div style="margin:8px 0;padding:6px;background:#1a1a1a;border-radius:4px;line-height:0;">'
        f'<span style="color:#888;font-size:11px;line-height:1.5;">Row {n} ({length} cords): </span><br>{content}</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000588 Rows</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000588 — Divided Into Rows</h1>
<p class="note">New row starts after each 6-cord divider. Red borders = divider cords.</p>
{''.join(row_html)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000588-rows.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out} ({len(rows)} rows)")
