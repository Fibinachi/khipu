"""Section 5 of 1000396 divided into five-groups."""
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
    WHERE c.KHIPU_ID = 1000396 AND c.CORD_ORDINAL BETWEEN 110 AND 168
    ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen: seen[o] = (cid, (col or '?').strip())

def box(o, highlight=False):
    cid, col = seen[o]
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(14 + v * 2, 60) if v else 10
    border = 'border:3px solid #FFD700;' if highlight else 'border:1px solid #555;'
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:14px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;{border}"></div>')

# Divide section 5
parts = [
    ("5a — scattered", 110, 140, False,
     "Scattered 1s and 3s. No grouping."),
    ("5b — FIVE GROUP 1", 141, 145, True,
     "AB, MB, AB, AB, AB"),
    ("5c — FIVE GROUP 2", 147, 151, True,
     "AB, MB, MB, AB, MB"),
    ("5d — transition", 153, 157, False,
     "3 MB + 1 AB. Between groups."),
    ("5e — FIVE GROUP 3", 159, 163, True,
     "MB, MB, MB, AB, AB"),
    ("5f — tail", 165, 168, False,
     "3 AB + close."),
]

html_parts = []
for name, s, e, hl, desc in parts:
    boxes = "".join(box(o, highlight=hl) for o in range(s, e+1) if o in seen)
    bg = "#2a2a00" if hl else "#1a1a1a"
    html_parts.append(
        f'<div style="margin:12px 0;padding:10px;background:{bg};border-radius:6px;">'
        f'<div style="font-weight:bold;margin-bottom:4px;">{name} '
        f'<span style="color:#888;font-weight:normal;">(ords {s}–{e})</span></div>'
        f'<div style="font-size:0.8em;color:#aaa;margin-bottom:6px;">{desc}</div>'
        f'<div style="line-height:0;">{boxes}</div></div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000396 Section 5 Divided</title>
<style>
body {{ font-family: sans-serif; max-width: 1000px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; }}
</style></head><body>
<h1>Khipu 1000396 — Section 5 Divided</h1>
<p class="note"><span style="color:#FFD700;">Gold borders</span> = the three five-groups.
Each is exactly 5 blues; AB/MB mix varies.</p>
{''.join(html_parts)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000396-sec5.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
