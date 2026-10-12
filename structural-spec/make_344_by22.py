"""Render 1000344 with rows defined by BY=22 markers."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'AB': '#4A6FA5', 'MB': '#1B3A5C', 'BG': '#8B4513',
    'BY': '#FFD700', 'BL': '#000080', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000344
    ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, (col or '?').strip())
ords = sorted(seen.keys())

# Find BY=22 marker positions
markers = []
for o in ords:
    cid, col = seen[o]
    if col == 'BY':
        try: v = decode_cord(conn, cid)['value'] or 0
        except: v = 0
        if v == 22:
            markers.append(o)

print(f"BY=22 markers at: {markers}")

# Build rows: each row starts at a marker, ends before next marker
# Also include leading segment (before first marker) and trailing
bounds = [0] + markers + [ords[-1] + 1]
rows = []
for i in range(len(bounds) - 1):
    start, end = bounds[i], bounds[i+1]
    row_ords = [o for o in ords if start <= o < end]
    if row_ords:
        rows.append(row_ords)

# Render each row as a horizontal strip with values
html_rows = []
for ri, row_ords in enumerate(rows):
    boxes = []
    for o in row_ords:
        cid, col = seen[o]
        try: v = decode_cord(conn, cid)['value'] or 0
        except: v = 0
        hexcol = COLORS.get(col, '#CCCCCC')
        h = min(14 + v * 1.5, 70) if v else 10
        is_marker = (col == 'BY' and v == 22)
        border = 'border:3px solid #FF0000;' if is_marker else 'border:1px solid #555;'
        boxes.append(
            f'<div title="Ord {o}: {col}={v}" style="width:13px;height:{h}px;'
            f'background:{hexcol};{border}display:inline-block;margin:1px;'
            f'vertical-align:bottom;"></div>'
        )
    label = f"Row {ri+1}"
    if row_ords and row_ords[0] in markers:
        label += f" ★ BY=22 marker at ord {row_ords[0]}"
    else:
        label += f" (ords {row_ords[0]}–{row_ords[-1]}, no marker)"
    n_nz = sum(1 for o in row_ords
               if (lambda cid: (lambda r: r['value'] or 0)(decode_cord(conn, cid)))(seen[o][0]))
    html_rows.append(
        f'<div style="margin:10px 0;padding:8px;background:#1e1e1e;border-radius:4px;">'
        f'<div style="font-size:0.8em;color:#aaa;margin-bottom:4px;">{label} — '
        f'{len(row_ords)} cords</div>'
        f'<div style="line-height:0;">{"".join(boxes)}</div></div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000344 by BY=22 Rows</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.3em; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000344 — Rows Defined by BY=22 Markers</h1>
<p class="note">Red-bordered boxes = BY=22 row markers. Bar height = value.
{len(rows)} rows. First 7 markers are metronomic (12-cord gaps); then irregular.</p>
{''.join(html_rows)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000344-by22rows.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}: {len(rows)} rows")
