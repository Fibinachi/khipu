"""1000183 journal entries separated by single-white delimiters."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'YB': '#DDD700', 'W': '#F5F5F5', 'BB': '#2a2a5a', '0G': '#228B22',
    'FB': '#4169E1', 'DB': '#0a0a3a', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1
    FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000183 ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen: seen[o] = (cid, (col or '?').strip())
ords = sorted(seen.keys())

# Split on single W
entries = []
current = []
for o in ords:
    cid, col = seen[o]
    if col == 'W':
        if current:
            entries.append(current)
            current = []
    else:
        current.append(o)
if current:
    entries.append(current)

print(f"{len(entries)} journal entries")

html_entries = []
for ei, entry_ords in enumerate(entries[:40]):  # first 40
    boxes = []
    total = 0
    for o in entry_ords:
        cid, col = seen[o]
        hexcol = COLORS.get(col, '#CCCCCC')
        try: v = decode_cord(conn, cid)['value'] or 0
        except: v = 0
        total += v
        h = min(12 + v * 2, 50) if v else 8
        boxes.append(
            f'<div title="Ord {o}: {col}={v}" '
            f'style="width:10px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:1px solid #555;"></div>'
        )
    from collections import Counter
    cc = Counter(seen[o][1] for o in entry_ords)
    cols = ",".join(f"{k}{v}" for k, v in cc.most_common(3))
    html_entries.append(
        f'<div style="margin:8px 0;padding:8px;background:#1a1a1a;border-radius:4px;">'
        f'<div style="font-size:0.8em;color:#888;margin-bottom:4px;">'
        f'Entry {ei+1} <span style="color:#666;">(ords {entry_ords[0]}–{entry_ords[-1]}, '
        f'{len(entry_ords)} cords, {cols}, total={total})</span></div>'
        f'<div style="line-height:0;">{"".join(boxes)}</div></div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000183 Entries</title>
<style>
body {{ font-family: sans-serif; max-width: 1000px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; }}
</style></head><body>
<h1>Khipu 1000183 — Journal Entries</h1>
<p class="note">{len(entries)} entries separated by single white delimiters.
Showing first 40. Bar height = value.</p>
{''.join(html_entries)}
{f'<p class="note">... and {len(entries)-40} more entries.</p>' if len(entries) > 40 else ''}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000183-entries.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
