"""1000396 segmented by white separators - visual sections."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'AB': '#4A6FA5', 'MB': '#1B3A5C', 'BG': '#8B4513',
    'GG': '#808080', 'YB': '#DDD700', 'KB': '#1a1a1a', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1
    FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000396 ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen: seen[o] = (cid, (col or '?').strip())
ords = sorted(seen.keys())

# White separator runs: 2-4, 17-19, 32-34, 77-79, 107-109
seps = [(2,4), (17,19), (32,34), (77,79), (107,109)]
sep_ords = set()
for s, e in seps:
    for o in range(s, e+1):
        sep_ords.add(o)

# Sections: between separators
sections = [
    ("Section 1", 5, 16),
    ("Section 2", 20, 31),
    ("Section 3", 35, 76),
    ("Section 4", 80, 106),
    ("Section 5", 110, 168),
]

html_secs = []
for name, s, e in sections:
    boxes = []
    for o in range(s, e+1):
        if o not in seen: continue
        cid, col = seen[o]
        hexcol = COLORS.get(col, '#CCCCCC')
        try: v = decode_cord(conn, cid)['value'] or 0
        except: v = 0
        h = min(14 + v * 2, 60) if v else 10
        boxes.append(
            f'<div title="Ord {o}: {col}={v}" '
            f'style="width:12px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:1px solid #555;"></div>'
        )
    from collections import Counter
    cc = Counter(seen[o][1] for o in range(s, e+1) if o in seen)
    top = ", ".join(f"{k}={v}" for k, v in cc.most_common(3))
    html_secs.append(
        f'<div style="margin:14px 0;padding:10px;background:#1a1a1a;'
        f'border-radius:6px;border-left:4px solid #4A6FA5;">'
        f'<div style="font-weight:bold;margin-bottom:6px;">{name} '
        f'<span style="color:#888;font-weight:normal;">(ords {s}–{e}, '
        f'{e-s+1} cords: {top})</span></div>'
        f'<div style="line-height:0;">{"".join(boxes)}</div></div>'
    )
    # Separator bar
    html_secs.append(
        f'<div style="text-align:center;color:#666;margin:4px 0;'
        f'font-size:0.8em;letter-spacing:3px;">— 3 white —</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000396 Sectioned</title>
<style>
body {{ font-family: sans-serif; max-width: 1200px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; }}
</style></head><body>
<h1>Khipu 1000396 — Five Sections</h1>
<p class="note">Segmented by 3-white separators. Bar height = value.</p>
{''.join(html_secs)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000396-sectioned.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
