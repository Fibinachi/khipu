"""Reorganize 1000368 by white-run section dividers."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'AB': '#4A6FA5', 'MB': '#1B3A5C', 'BG': '#8B4513',
    'PK': '#DDA0DD', 'SY': '#FFD700', 'RL': '#CC0000', 'RB': '#8B0000',
    'KB': '#000000', 'CB': '#8B7355', 'YB': '#DAA520', 'GG': '#808080',
    'BS': '#6B7B8B', 'DB': '#2C3E50', 'HB': '#5D6D7E', 'B': '#0000FF',
    'GR': '#4A6741',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1, cc.COLOR_CD_2
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000368
    ORDER BY c.CORD_ORDINAL, cc.COLOR_CD_1
""")
seen = {}
for cid, o, c1, c2 in c.fetchall():
    if o not in seen:
        seen[o] = (cid, (c1 or '?').strip(), (c2 or '').strip())
ords = sorted(seen.keys())

# Find white runs of length >= 3 as section dividers
sections = []
current = []
i = 0
while i < len(ords):
    o = ords[i]
    cid, c1, c2 = seen[o]
    # Check if this starts a white run of >=3
    run_len = 0
    j = i
    while j < len(ords) and seen[ords[j]][1] == 'W':
        run_len += 1
        j += 1
    if run_len >= 3:
        # End current section, start new with this white run
        if current:
            sections.append(('content', current))
            current = []
        wrun = [(ords[k], seen[ords[k]]) for k in range(i, j)]
        sections.append(('divider', wrun))
        i = j
    else:
        current.append((o, seen[o]))
        i += 1
if current:
    sections.append(('content', current))

def box(o, cid, c1, c2):
    result = decode_cord(conn, cid)
    val = result['value'] or 0
    label = f'{c1}' + (f'+{c2}' if c2 else '') + f'={val}'
    hexcol = COLORS.get(c1, '#CCCCCC')
    border = 'border:1px solid #555;'
    h = min(20 + val * 4, 90)
    return (f'<div title="Cord {o}: {label}" style="width:16px;height:{h}px;'
            f'background:{hexcol};{border}display:inline-block;margin:1px;'
            f'vertical-align:bottom;"></div>')

html_parts = []
sec_num = 0
for stype, cords in sections:
    if stype == 'divider':
        boxes = ''.join(box(o, cid, c1, c2) for o, (cid, c1, c2) in cords)
        html_parts.append(
            f'<div style="margin:4px 0;padding:4px;background:#333;'
            f'border-radius:3px;opacity:0.7;">'
            f'<div style="line-height:0;">{boxes}</div></div>'
        )
    else:
        sec_num += 1
        boxes = ''.join(box(o, cid, c1, c2) for o, (cid, c1, c2) in cords)
        # Stats
        vals = [decode_cord(conn, cid)['value'] or 0 for o, (cid, c1, c2) in cords]
        nz = sum(1 for v in vals if v)
        o_first, o_last = cords[0][0], cords[-1][0]
        html_parts.append(
            f'<div style="margin:14px 0;padding:10px;background:#1e1e1e;'
            f'border-left:3px solid #F5F5F5;border-radius:4px;">'
            f'<div style="font-size:0.8em;color:#aaa;margin-bottom:6px;">'
            f'Entry block {sec_num} — {len(cords)} cords '
            f'(ordinals {o_first}–{o_last}), {nz} nonzero, '
            f'max value {max(vals) if vals else 0}</div>'
            f'<div style="line-height:0;">{boxes}</div></div>'
        )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000368 Sectioned by White Runs</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.3em; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 900px; }}
</style></head><body>
<h1>Khipu 1000368 — Reorganized by White-Run Dividers</h1>
<p class="note">Gray bars = white-cord dividers (runs of 3+). White-bar panels = entry blocks between dividers.
Bar height = decoded value. The journal structure: divider, entries, divider, entries...</p>
{''.join(html_parts)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/journal-hunt/1000368-sectioned.html'
with open(out, 'w') as f:
    f.write(html)
n_sec = sum(1 for s, _ in sections if s == 'content')
n_div = sum(1 for s, _ in sections if s == 'divider')
print(f"Wrote {out}: {n_sec} entry blocks, {n_div} dividers")
