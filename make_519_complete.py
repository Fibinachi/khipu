"""1000519: complete annotated view."""
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
n = len(ords)

def box(o, cid, col):
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(6 + v*1.0, 32) if v else 5
    border = '1px solid #0f0' if v else '1px solid #333'
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:6px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:{border};"></div>')

def green_box():
    return ('<div title="restored green" style="width:6px;height:14px;background:#00AA00;'
            'display:inline-block;margin:1px;vertical-align:bottom;border:1px solid #ffd700;"></div>')

# Build full strip with section markers
parts = []
# Head (1-4 + green)
for o in range(1, 5):
    if o == 2:
        parts.append(green_box())
    parts.append(box(o, *seen[o]))
parts.append('<span style="color:#ffd700;font-size:10px;margin:0 6px;">|HEAD|</span>')
# Doc B (5-44)
for o in range(5, 45):
    parts.append(box(o, *seen[o]))
parts.append('<span style="color:#ffd700;font-size:10px;margin:0 6px;">|8x5|</span>')
# Doc C (45-90)
for o in range(45, 91):
    if o in seen:
        parts.append(box(o, *seen[o]))
parts.append('<span style="color:#ffd700;font-size:10px;margin:0 6px;">|HB/PR|</span>')
# Doc D (91-115)
for o in range(91, 116):
    parts.append(box(o, *seen[o]))
parts.append('<span style="color:#ffd700;font-size:10px;margin:0 6px;">|W/PR TABLE|</span>')
# Remainder (116-148)
for o in range(116, n+1):
    if o in seen:
        parts.append(box(o, *seen[o]))

# Value summary by section
def section_values(s, e):
    vals = []
    for o in range(s, e+1):
        if o in seen:
            cid, col = seen[o]
            try: v = decode_cord(conn, cid)['value'] or 0
            except: v = 0
            if v: vals.append(f'{o}:{col}={v}')
    return vals

summaries = [
    ("A: Head (1-4)", 1, 4),
    ("B: Eight 5-blocks (5-44)", 5, 44),
    ("C: HB/KB/MB/PR zone (45-90)", 45, 90),
    ("D: W/PR table (91-115)", 91, 115),
    ("E: Remainder (116-148)", 116, 148),
]
sum_html = []
for name, s, e in summaries:
    vals = section_values(s, e)
    vstr = ', '.join(vals) if vals else '(all zero)'
    sum_html.append(f'<div style="margin:4px 0;font-size:12px;"><b style="color:#ffd700;">{name}:</b> <span style="color:#aaa;">{vstr}</span></div>')

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000519 Complete</title>
<style>
body {{ font-family: sans-serif; max-width: 1700px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.3em; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 1000px; }}
.strip {{ line-height: 1; padding: 16px; background: #1a1a1a; border-radius: 8px; margin: 16px 0; }}
</style></head><body>
<h1>Khipu 1000519 — Complete ({n} cords)</h1>
<p class="note">Full cord strip with section markers. Green-bordered = non-zero knot values.</p>
<div class="strip">{''.join(parts)}</div>
<h2 style="font-size:1.1em;">Values by section</h2>
{''.join(sum_html)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000519-complete.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
