"""1000588 final reconstruction: 15 blocks, 2 known missing MBs, emendation applied."""
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
seen[162], seen[163] = seen[163], seen[162]  # emendation

# Block boundaries (observed ordinals).
# Missing MBs: after 51 (block 4 divider), after 63 (block 5 divider).
# From 52 onward, ordinals compressed by 1; from 64 onward, by 2.
blocks = [
    (1, 13, 0, 'complete'),
    (14, 26, 0, 'complete'),
    (27, 39, 0, 'complete'),
    (40, 51, 1, 'divider missing final MB'),
    (52, 63, 1, 'divider missing final MB'),
    (64, 76, 0, 'complete (realigned)'),
    (77, 89, 0, 'complete?'),
    (90, 101, 0, 'complete?'),
    (102, 114, 0, ''),
    (115, 127, 0, ''),
    (128, 140, 0, ''),
    (141, 149, 0, ''),
    (150, 162, 0, ''),
    (163, 175, 0, ''),
    (176, 189, 0, ''),
]

def box(o, cid, col):
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(10 + v * 1.5, 50) if v else 6
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:9px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:1px solid #555;"></div>')

def missing_box():
    return ('<div title="MISSING MB (divider-final)" '
            'style="width:9px;height:20px;background:#3a0000;'
            'display:inline-block;margin:1px;vertical-align:bottom;'
            'border:2px dashed #ff4444;"></div>')

row_html = []
for n, (s, e, n_missing, note) in enumerate(blocks, 1):
    cords = []
    for o in range(s, e+1):
        if o in seen:
            cid, col = seen[o]
            cords.append(box(o, cid, col))
    # append missing markers
    for _ in range(n_missing):
        cords.append(missing_box())
    tag = f'Block {n}: ords {s}-{e} ({len(cords)} with missing)'
    if note:
        tag += f' <span style="color:#fa0;">[{note}]</span>'
    row_html.append(
        f'<div style="margin:6px 0;padding:6px;background:#1a1a1a;border-radius:4px;line-height:0;">'
        f'<span style="color:#888;font-size:11px;line-height:1.5;">{tag}</span><br>{"".join(cords)}</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000588 Final Reconstruction</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000588 — Final Reconstruction</h1>
<p class="note">15 blocks. Red dashed = missing divider-final MB (blocks 4, 5).
Emendation 162/163 applied. Block 6 realigned after accounting for upstream losses.</p>
{''.join(row_html)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000588-final.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
