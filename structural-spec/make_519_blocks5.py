"""1000519: blocks of 5."""
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
    h = min(10 + v*1.5, 50) if v else 6
    label = str(v) if v else ''
    tc = '#000' if col == 'W' else '#fff'
    border = '2px solid #0f0' if v else '1px solid #555'
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:20px;height:32px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:{border};border-radius:3px;text-align:center;'
            f'color:{tc};font-size:9px;line-height:32px;font-weight:bold;">{label}</div>')

row_html = []
# Head: ords 1-4
head = ''.join(box(o, *seen[o]) for o in range(1, 5))
row_html.append(
    f'<div style="margin:6px 0;padding:6px;background:#1a1a1a;border-radius:4px;line-height:1;">'
    f'<span style="color:#888;font-size:11px;">Head (1-4, fragmented)</span><br>{head}</div>'
)
# Blocks of 5 from ord 5
nblocks = (n - 4) // 5
for b in range(nblocks):
    s = 5 + b*5
    e = s + 4
    cords = ''.join(box(o, *seen[o]) for o in range(s, e+1) if o in seen)
    # check if it matches X,Y,W,MB,AB pattern
    seq = [seen[o][1] for o in range(s, e+1) if o in seen]
    match = len(seq) == 5 and seq[2] == 'W' and seq[3] == 'MB' and seq[4] == 'AB'
    tag = f'Block {b+1} ({s}-{e})'
    if not match:
        tag += ' <span style="color:#f44;">[breaks pattern]</span>'
    row_html.append(
        f'<div style="margin:6px 0;padding:6px;background:#1a1a1a;border-radius:4px;line-height:1;">'
        f'<span style="color:#888;font-size:11px;">{tag}</span><br>{cords}</div>'
    )
# Remainder
rem_start = 5 + nblocks*5
if rem_start <= n:
    rem = ''.join(box(o, *seen[o]) for o in range(rem_start, n+1) if o in seen)
    row_html.append(
        f'<div style="margin:6px 0;padding:6px;background:#1a1a1a;border-radius:4px;line-height:1;">'
        f'<span style="color:#888;font-size:11px;">Remainder ({rem_start}-{n})</span><br>{rem}</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000519 Blocks of 5</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000519 — Blocks of 5</h1>
<p class="note">Green-bordered cords have knot values (labeled). Pattern: [X],[Y],W,MB,AB with chained AB.</p>
{''.join(row_html)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000519-blocks5.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
