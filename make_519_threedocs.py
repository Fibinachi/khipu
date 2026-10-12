"""1000519: three documents."""
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
    h = min(10 + v*1.5, 40) if v else 6
    label = str(v) if v else ''
    tc = '#000' if col == 'W' else '#fff'
    border = '2px solid #0f0' if v else '1px solid #555'
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:8px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:{border};"></div>')

def green_box():
    return ('<div title="INSERTED green" style="width:8px;height:20px;background:#00AA00;'
            'display:inline-block;margin:1px;vertical-align:bottom;'
            'border:2px solid #ffd700;"></div>')

sections = []

# Doc 1: Head (ords 1-4 + restored green)
head_parts = []
for o in range(1, 5):
    if o == 2:
        head_parts.append(green_box())
    head_parts.append(box(o, *seen[o]))
sections.append(('Document 1: Head (ords 1-4 + restored green) — 5-cord header',
                 ''.join(head_parts)))

# Doc 2: Blocks 1-8 (ords 5-44), 5-cord blocks
doc2_parts = []
for b in range(8):
    s = 5 + b*5
    block = ''.join(box(o, *seen[o]) for o in range(s, s+5) if o in seen)
    doc2_parts.append(f'<span style="display:inline-block;margin-right:8px;">{block}</span>')
sections.append(('Document 2: Eight 5-cord blocks (ords 5-44) — [cat],[cat],W,MB,AB chained',
                 ''.join(doc2_parts)))

# Doc 3: ords 45-148, PR-led 5-blocks
doc3_parts = []
remaining = [o for o in ords if o >= 45]
nblocks = len(remaining) // 5
for b in range(nblocks):
    chunk = remaining[b*5:(b+1)*5]
    block = ''.join(box(o, *seen[o]) for o in chunk)
    doc3_parts.append(f'<span style="display:inline-block;margin-right:8px;">{block}</span>')
sections.append((f'Document 3: PR-led blocks (ords 45-{remaining[-1]}) — {nblocks} x 5-cord',
                 ''.join(doc3_parts)))

sec_html = []
for title, content in sections:
    sec_html.append(
        f'<div style="margin:12px 0;padding:10px;background:#1a1a1a;border-radius:6px;line-height:0;">'
        f'<span style="color:#ffd700;font-size:13px;line-height:1.5;font-weight:bold;">{title}</span><br><br>{content}</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000519 Three Documents</title>
<style>
body {{ font-family: sans-serif; max-width: 1600px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.3em; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000519 — Three Documents</h1>
<p class="note">One cord, three distinct forms. Green-bordered = knot values.
Gold-bordered green = restored.</p>
{''.join(sec_html)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000519-three-docs.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
