"""1000519: full section map."""
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

def box(o, cid, col, highlight=False):
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(8 + v*1.2, 36) if v else 5
    border = '2px solid #0f0' if highlight and v else '1px solid #444'
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:7px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:{border};"></div>')

def green_box():
    return ('<div title="restored green" style="width:7px;height:16px;background:#00AA00;'
            'display:inline-block;margin:1px;vertical-align:bottom;border:2px solid #ffd700;"></div>')

# Sections: (name, start, end, description, highlight_values)
sections = [
    ("A: Head", 1, 4, "5-cord header (AB, green*, W, MB, AB) — *restored", True),
    ("B: Eight 5-blocks", 5, 44, "[cat],[cat],W,MB,AB chained — values at head", True),
    ("C: HB/KB/MB/PR zone", 45, 90, "Unresolved — repeating HB KB MB PR with values", True),
    ("D: W/PR data table", 91, 115, "5 records x [cat],W,PR,AB,AB — clean 2-column table", True),
    ("E: Remainder", 116, 148, "Unanalyzed", False),
]

sec_html = []
for name, s, e, desc, hl in sections:
    parts = []
    for o in range(s, e+1):
        if o not in seen:
            continue
        if s == 1 and o == 2:
            parts.append(green_box())
        cid, col = seen[o]
        parts.append(box(o, cid, col, hl))
    # count non-zero
    nz = 0
    for o in range(s, e+1):
        if o in seen:
            cid, col = seen[o]
            try: v = decode_cord(conn, cid)['value'] or 0
            except: v = 0
            if v: nz += 1
    sec_html.append(
        f'<div style="margin:10px 0;padding:10px;background:#1a1a1a;border-radius:6px;line-height:0;">'
        f'<span style="color:#ffd700;font-size:13px;line-height:1.6;font-weight:bold;">{name} (ords {s}-{e})</span><br>'
        f'<span style="color:#888;font-size:11px;line-height:1.6;">{desc} — {nz} non-zero values</span><br><br>'
        f'{"".join(parts)}</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000519 Section Map</title>
<style>
body {{ font-family: sans-serif; max-width: 1600px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.3em; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000519 — Section Map</h1>
<p class="note">Five sections, at least three document types. Green-bordered = values.</p>
{''.join(sec_html)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000519-sections.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
