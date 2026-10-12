"""1000029 as grouped spreadsheet (color blocks, not cycles)."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'MB': '#1B3A5C', 'KB': '#1a1a1a', 'W': '#F5F5F5', 'DB': '#0a0a3a',
    'YB': '#DDD700', 'YG': '#9ACD32', 'BB': '#2a2a5a', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1
    FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000029 ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen: seen[o] = (cid, (col or '?').strip())
ords = sorted(seen.keys())

# Find color blocks (runs)
blocks = []
i = 0
while i < len(ords):
    o = ords[i]
    col = seen[o][1]
    j = i
    while j < len(ords) and seen[ords[j]][1] == col:
        j += 1
    blocks.append((col, ords[i:j]))
    i = j

print(f"{len(blocks)} color blocks")
for col, block_ords in blocks:
    print(f"  {col}: {len(block_ords)} cords (ords {block_ords[0]}-{block_ords[-1]})")

# Build HTML: each block as a column
max_len = max(len(b[1]) for b in blocks)
html_cols = []
for col, block_ords in blocks:
    hexcol = COLORS.get(col, '#CCCCCC')
    fg = '#fff' if col in ('MB','KB','DB','BB') else '#000'
    cells = []
    for o in block_ords:
        cid, _ = seen[o]
        try: v = decode_cord(conn, cid)['value'] or 0
        except: v = 0
        bg = '#1e3a1e' if v else '#1a1a1a'
        cells.append(
            f'<div style="padding:4px 8px;text-align:right;background:{bg};'
            f'border-bottom:1px solid #333;">{v if v else ""}</div>'
        )
    # Pad to max_len
    while len(cells) < max_len:
        cells.append('<div style="padding:4px 8px;border-bottom:1px solid #222;"></div>')
    total = 0
    for o in block_ords:
        cid, _ = seen[o]
        try: v = decode_cord(conn, cid)['value'] or 0
        except: v = 0
        total += v
    html_cols.append(
        f'<div style="display:inline-block;vertical-align:top;margin:0 4px;min-width:70px;">'
        f'<div style="padding:8px;background:{hexcol};color:{fg};font-weight:bold;'
        f'text-align:center;">{col}<br><span style="font-size:0.8em;">'
        f'{len(block_ords)}c / {total}</span></div>'
        f'{"".join(cells)}</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000029 Spreadsheet</title>
<style>
body {{ font-family: monospace; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; font-family: sans-serif; }}
.note {{ font-size: 0.85em; color: #aaa; font-family: sans-serif; max-width: 800px; }}
</style></head><body>
<h1>Khipu 1000029 as Spreadsheet</h1>
<p class="note">{len(blocks)} color blocks as columns. No rotation cycle —
colors come in runs. Each column = one color run. Header shows cord count and total.
Green cells = nonzero.</p>
<div style="overflow-x:auto;white-space:nowrap;">{''.join(html_cols)}</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000029-spreadsheet.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
