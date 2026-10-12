"""1000588: restored original with missing MBs inserted as blue."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'MB': '#1B3A5C', 'PG': '#FF69B4',
    'AB': '#4A6FA5', '?': '#CCCCCC',
}
RESTORED = '#1B3A5C'  # MB blue, with gold border to mark restoration

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
seen[162], seen[163] = seen[163], seen[162]

# (start, end, restored_count)
blocks = [
    (1, 13, 0), (14, 26, 0), (27, 39, 0),
    (40, 51, 1), (52, 63, 1), (64, 76, 0),
    (77, 88, 1), (89, 101, 0), (102, 113, 1),
    (114, 125, 1), (126, 137, 0), (138, 149, 0),
    (150, 162, 0), (163, 176, 0), (177, 189, 0),
]

def box(o, cid, col, restored=False):
    hexcol = RESTORED if restored else COLORS.get(col, '#CCCCCC')
    border = '2px solid #ffd700' if restored else '1px solid #555'
    title = f"RESTORED MB (was missing)" if restored else f"Ord {o}: {col}"
    if not restored:
        try: v = decode_cord(conn, cid)['value'] or 0
        except: v = 0
        h = min(10 + v * 1.5, 50) if v else 6
        title += f"={v}"
    else:
        h = 20
    return (f'<div title="{title}" '
            f'style="width:9px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:{border};"></div>')

row_html = []
for n, (s, e, nr) in enumerate(blocks, 1):
    cords = [box(o, *seen[o]) for o in range(s, e+1) if o in seen]
    for _ in range(nr):
        cords.append(box(None, None, None, restored=True))
    n_rest = f' <span style="color:#ffd700;">(+{nr} restored)</span>' if nr else ''
    row_html.append(
        f'<div style="margin:6px 0;padding:6px;background:#1a1a1a;border-radius:4px;line-height:0;">'
        f'<span style="color:#888;font-size:11px;line-height:1.5;">Block {n}{n_rest}</span><br>{"".join(cords)}</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000588 Restored</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000588 — Restored Original</h1>
<p class="note">Gold-bordered blue cords are restored (5 missing divider-final MBs).
Emendation 162/163 applied. This is the khipu as tied.</p>
{''.join(row_html)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000588-restored4.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
