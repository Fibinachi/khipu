"""1000519 section C: numbered cords for edit reference."""
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
    WHERE c.KHIPU_ID = 1000519 AND c.CORD_ORDINAL BETWEEN 45 AND 90
    ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, (col or '?').strip())
ords = sorted(seen.keys())

def box(idx, o, cid, col):
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = 36
    tc = '#000' if col in ('W','G0') else '#fff'
    vlo = str(v) if v else ''
    return (f'<div style="display:inline-block;text-align:center;margin:2px;vertical-align:top;">'
            f'<div title="Ord {o}: {col}={v}" '
            f'style="width:30px;height:{h}px;background:{hexcol};'
            f'border:1px solid #555;border-radius:3px;'
            f'color:{tc};font-size:11px;line-height:{h}px;font-weight:bold;">{vlo}</div>'
            f'<div style="font-size:9px;color:#888;margin-top:2px;">#{idx}<br>o{o}</div>'
            f'</div>')

p1 = []
p2 = []
for i, o in enumerate(ords):
    b = box(i+1, o, *seen[o])
    if i+1 <= 6:
        p1.append(b)
    else:
        p2.append(b)
part1 = ''.join(p1)
part2 = ''.join(p2)

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000519 Section C Numbered</title>
<style>
body {{ font-family: sans-serif; max-width: 1600px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 900px; }}
.strip {{ line-height: 1; padding: 16px; background: #1a1a1a; border-radius: 8px; }}
</style></head><body>
<h1>Section C (ords 45-90) — Numbered</h1>
<p class="note">#N = position in section, oN = ordinal. Say "insert after #12" or "divide after o57".</p>
<div style="margin:12px 0;padding:14px;background:#1a1a1a;border-radius:8px;border-left:4px solid #ffd700;">
<div style="font-size:13px;font-weight:bold;color:#ffd700;margin-bottom:8px;">Part 1: #1-6 (ords 45-50)</div>
<div style="line-height:1;">{part1}</div>
</div>
<div style="margin:12px 0;padding:14px;background:#1a1a1a;border-radius:8px;border-left:4px solid #ffd700;">
<div style="font-size:13px;font-weight:bold;color:#ffd700;margin-bottom:8px;">Part 2: #7-46 (ords 51-90)</div>
<div style="line-height:1;">{part2}</div>
</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000519-secc-blocks.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
