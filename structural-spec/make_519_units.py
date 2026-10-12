"""1000519: G0-labeled W-X-AB-AB units (ords 86-115)."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'MB': '#1B3A5C', 'AB': '#4A6FA5',
    'BG': '#2E8B57', 'GG': '#808080', 'PB': '#8B008B',
    'G0': '#FFD700', 'HB': '#8B4513', 'KB': '#00008B',
    'PR': '#800080', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1
    FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000519 AND c.CORD_ORDINAL BETWEEN 86 AND 115
    ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, (col or '?').strip())

# Units start at each G0 or PB category
units = [(86, 90), (91, 95), (96, 100), (101, 105), (106, 110), (111, 115)]

def box(o, cid, col):
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = 48
    label = str(v) if v else col
    tc = '#000' if col in ('W', 'G0') else '#fff'
    # G0 = gold border (category), W/PR/HB/MB with values = green, AB AB = red
    if col == 'G0' or (o in (96, 106, 111) and col == 'PB'):
        border = '3px solid #ffd700'
    elif col in ('AB',):
        border = '2px solid #ff4444'
    elif v:
        border = '2px solid #0f0'
    else:
        border = '1px solid #555'
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:44px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:3px;vertical-align:bottom;'
            f'border:{border};border-radius:5px;text-align:center;'
            f'color:{tc};font-size:13px;line-height:{h}px;font-weight:bold;">{label}</div>')

row_html = []
for n, (s, e) in enumerate(units, 1):
    cords = ''.join(box(o, *seen[o]) for o in range(s, e+1) if o in seen)
    # describe the X slot
    x_col = seen[s+2][1] if s+2 in seen else '?'
    try: xv = decode_cord(conn, seen[s+2][0])['value'] or 0
    except: xv = 0
    wv = 0
    try: wv = decode_cord(conn, seen[s+1][0])['value'] or 0
    except: pass
    cat = seen[s][1]
    row_html.append(
        f'<div style="margin:10px 0;padding:10px;background:#1a1a1a;border-radius:6px;line-height:1;">'
        f'<span style="color:#888;font-size:13px;">Unit {n}: {cat} → W={wv}, {x_col}={xv}, AB AB</span><br><br>{cords}</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000519 Units</title>
<style>
body {{ font-family: sans-serif; max-width: 1200px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.3em; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000519 — G0/PB-Labeled Units (ords 86-115)</h1>
<p class="note">Gold = category. Green = values. Red = AB AB divider.
Pattern: [CAT] W [PR|MB|HB] AB AB.</p>
{''.join(row_html)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000519-units.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
