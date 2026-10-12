"""1000396 with form analysis: sections, 3a/3b split, blue blocks."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'AB': '#4A6FA5', 'MB': '#1B3A5C', 'BG': '#8B4513',
    'GG': '#808080', 'YB': '#DDD700', 'KB': '#1a1a1a', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1
    FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000396 ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen: seen[o] = (cid, (col or '?').strip())

def cord_box(o):
    cid, col = seen[o]
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(14 + v * 2, 60) if v else 10
    # Highlight blue blocks
    if col in ('AB', 'MB'):
        border = 'border:2px solid #00FF00;'
    else:
        border = 'border:1px solid #555;'
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:12px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;{border}"></div>')

sections = [
    ("Section 1 — AB form", 5, 16, "#1a2a1a",
     "AB=6 run. Single blue block."),
    ("Section 2 — MB form", 20, 31, "#1a2a1a",
     "MB=6 run. Single blue block."),
    ("Section 3a — INTRUDER", 35, 57, "#2a1a1a",
     "23 cords, mixed. Does not fit the form. Spliced material."),
    ("Section 3b — MB form", 58, 76, "#1a2a1a",
     "MB=6 run (ords 66-71). Real section 3."),
    ("Section 4 — DOUBLE form", 80, 106, "#1a1a2a",
     "AB run (81-87) + MB=6 run (96-101). Both slots filled."),
    ("Section 5", 110, 168, "#1a1a1a",
     "AB-dominant. Longest section."),
]

html_parts = []
for name, s, e, bg, desc in sections:
    boxes = "".join(cord_box(o) for o in range(s, e+1) if o in seen)
    html_parts.append(
        f'<div style="margin:14px 0;padding:10px;background:{bg};'
        f'border-radius:6px;">'
        f'<div style="font-weight:bold;margin-bottom:4px;">{name} '
        f'<span style="color:#888;font-weight:normal;">(ords {s}–{e})</span></div>'
        f'<div style="font-size:0.8em;color:#aaa;margin-bottom:6px;">{desc}</div>'
        f'<div style="line-height:0;">{boxes}</div></div>'
    )
    if "INTRUDER" not in name:
        html_parts.append(
            '<div style="text-align:center;color:#666;margin:2px 0;'
            'font-size:0.8em;letter-spacing:3px;">— 3 white —</div>'
        )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000396 Form Analysis</title>
<style>
body {{ font-family: sans-serif; max-width: 1200px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000396 — Form Analysis</h1>
<p class="note"><span style="color:#00FF00;">Green borders</span> = blue blocks (AB/MB).
Each section is a form instance with AB and/or MB slots.
Section 3a (red tint) is intruder material. Section 4 fills both slots.</p>
{''.join(html_parts)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000396-form.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
