"""1000519: category-labeled dividers W MB AB AB."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'MB': '#1B3A5C', 'AB': '#4A6FA5',
    'BG': '#2E8B57', 'GG': '#808080', 'PB': '#8B008B',
    'G0': '#FFD700', 'HB': '#8B4513', 'KB': '#00008B',
    'PR': '#800080', 'RB': '#8B0000', 'RL': '#FF0000',
    'FR': '#FF6347', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1
    FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000519 ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, (col or '?').strip())
ords = sorted(seen.keys())
seq = [seen[o][1] for o in ords]

# Find dividers: [CAT] W MB AB AB — category + W MB AB AB
# Mark divider cords (W MB AB AB) and category cords
div_cords = set()
cat_cords = set()
for i in range(len(seq)-4):
    if seq[i+1] == 'W' and seq[i+2] == 'MB' and seq[i+3] == 'AB' and seq[i+4] == 'AB':
        cat_cords.add(ords[i])
        for j in range(1, 5):
            div_cords.add(ords[i+j])

def box(o, cid, col):
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(10 + v*1.5, 50) if v else 6
    if o in div_cords:
        border = '2px solid #ff4444'
    elif o in cat_cords:
        border = '2px solid #ffd700'
    else:
        border = '1px solid #555'
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:10px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:{border};"></div>')

# Segment by dividers: break after each AB AB
breaks = set()
for i in range(len(seq)-3):
    if seq[i] == 'W' and seq[i+1] == 'MB' and seq[i+2] == 'AB' and seq[i+3] == 'AB':
        breaks.add(ords[i+3])

rows = []
cur = []
for o in ords:
    cid, col = seen[o]
    cur.append(box(o, cid, col))
    if o in breaks:
        rows.append(cur)
        cur = []
if cur:
    rows.append(cur)

row_html = []
for n, r in enumerate(rows, 1):
    row_html.append(
        f'<div style="margin:6px 0;padding:6px;background:#1a1a1a;border-radius:4px;line-height:0;">'
        f'<span style="color:#888;font-size:11px;line-height:1.5;">Record {n} ({len(r)} cords)</span><br>{"".join(r)}</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000519</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000519 — Category-Labeled Records</h1>
<p class="note">Gold border = category label. Red border = divider (W MB AB AB).
{len(rows)} records.</p>
{''.join(row_html)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000519-records.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out} ({len(rows)} records)")
