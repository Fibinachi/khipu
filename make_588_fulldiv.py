"""1000588 with full 6-cord divider signatures boxed."""
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
ords = sorted(seen.keys())
seq = [seen[o][1] for o in ords]

# find full 6-cord dividers: W W [MB|PG] W MB MB
divider_spans = []  # (start_idx, end_idx)
for i in range(len(seq)-5):
    if (seq[i] == 'W' and seq[i+1] == 'W' and seq[i+2] in ('MB','PG')
        and seq[i+3] == 'W' and seq[i+4] == 'MB' and seq[i+5] == 'MB'):
        divider_spans.append((i, i+5))

print(f"{len(divider_spans)} full dividers")

in_div = set()
for s, e in divider_spans:
    for i in range(s, e+1):
        in_div.add(ords[i])

def box(o, cid, col, is_div):
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(10 + v * 1.5, 55) if v else 6
    if is_div:
        return (f'<div title="Ord {o}: {col}={v} DIVIDER" '
                f'style="width:8px;height:{h}px;background:{hexcol};'
                f'display:inline-block;margin:0;vertical-align:bottom;'
                f'border-top:3px solid #ff4444;border-bottom:3px solid #ff4444;"></div>')
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:8px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:1px solid #555;"></div>')

parts = []
for o in ords:
    cid, col = seen[o]
    parts.append(box(o, cid, col, o in in_div))

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000588 Full Dividers</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
.strip {{ line-height: 0; word-wrap: break-word; margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 6px; }}
</style></head><body>
<h1>Khipu 1000588 — Full Divider Signatures</h1>
<p class="note">{len(ords)} cords. Red-banded = full 6-cord divider (W W [MB|PG] W + MB MB).
{len(divider_spans)} dividers found.</p>
<div class="strip">{''.join(parts)}</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000588-fulldiv.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
