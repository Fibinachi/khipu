"""1000588: 15-block reconstruction with missing cords marked."""
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

# 15 blocks of 13. Certain dividers at ends of blocks 1,2,3,7,15.
# Reconstructed boundaries for damaged sections.
# Missing 6 cords distributed: assume gaps where blocks are short.
blocks = [
    (1, 13), (14, 26), (27, 39),           # certain
    (40, 52), (53, 65), (66, 76),           # block 6 short (11, missing 2)
    (77, 89), (90, 101),                    # block 8 short (12, missing 1)
    (102, 114), (115, 127), (128, 140),
    (141, 153), (154, 166), (167, 176),     # block 14 short (10, missing 3)
    (177, 189),                             # certain
]

def box(o, cid, col, missing=False):
    if missing:
        return ('<div title="MISSING cord" '
                'style="width:10px;height:20px;background:#3a0000;'
                'display:inline-block;margin:1px;vertical-align:bottom;'
                'border:1px dashed #ff4444;"></div>')
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(10 + v * 1.5, 50) if v else 6
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:10px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:1px solid #555;"></div>')

row_html = []
for n, (s, e) in enumerate(blocks, 1):
    cords = []
    for o in range(s, e+1):
        if o in seen:
            cid, col = seen[o]
            cords.append(box(o, cid, col))
        else:
            cords.append(box(o, None, None, missing=True))
    # pad to 13 with missing markers
    while len(cords) < 13:
        cords.append(box(None, None, None, missing=True))
    n_missing = 13 - (e - s + 1)
    tag = f'Block {n}: ords {s}-{e}' + (f' <span style="color:#f44;">({n_missing} missing)</span>' if n_missing else ' (complete)')
    row_html.append(
        f'<div style="margin:6px 0;padding:6px;background:#1a1a1a;border-radius:4px;line-height:0;">'
        f'<span style="color:#888;font-size:11px;line-height:1.5;">{tag}</span><br>{"".join(cords)}</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000588 Reconstruction</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000588 — 15-Block Reconstruction</h1>
<p class="note">15 blocks × 13 cords = 195 original. 189 present, 6 missing (red dashed).
Emendation 162/163 applied. Internal boundaries in damaged sections are conjectural.</p>
{''.join(row_html)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000588-reconstruction.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
