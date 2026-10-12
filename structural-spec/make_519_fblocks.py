"""1000519: color blocks, section-divided."""
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

def box(o, cid, col, w=14, h_base=10):
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = min(h_base + v*1.2, 44) if v else 6
    label = str(v) if v else ''
    tc = '#000' if col in ('W','G0') else '#fff'
    border = '2px solid #0f0' if v else '1px solid #555'
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:{w}px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:1px;vertical-align:bottom;'
            f'border:{border};border-radius:2px;text-align:center;'
            f'color:{tc};font-size:8px;line-height:{h}px;">{label}</div>')

def green_box():
    return ('<div title="restored" style="width:14px;height:18px;background:#00AA00;'
            'display:inline-block;margin:1px;vertical-align:bottom;border:2px solid #ffd700;border-radius:2px;"></div>')

sections = []

# A: Head
parts = []
for o in range(1, 5):
    if o == 2: parts.append(green_box())
    parts.append(box(o, *seen[o]))
sections.append(("A: Head", "AB [G] W MB AB", ''.join(parts)))

# B: 8 blocks of 5
bparts = []
for b in range(8):
    s = 5 + b*5
    blk = ''.join(box(o, *seen[o]) for o in range(s, s+5))
    bparts.append(f'<span style="display:inline-block;margin:0 10px 10px 0;padding:4px;background:#222;border-radius:4px;">{blk}<br><span style="font-size:9px;color:#888;">{s}-{s+4}</span></span>')
sections.append(("B: Eight 5-Blocks", "[cat][cat] W MB AB chained", ''.join(bparts)))

# C: 45-90
cparts = ''.join(box(o, *seen[o]) for o in range(45, 91) if o in seen)
sections.append(("C: HB/KB/MB/PR Zone (45-90)", "Unresolved", cparts))

# D: 86-115 units (overlap with C, show separately)
dparts = []
for (s, e) in [(86,90),(91,95),(96,100),(101,105),(106,110),(111,115)]:
    blk = ''.join(box(o, *seen[o]) for o in range(s, e+1))
    dparts.append(f'<span style="display:inline-block;margin:0 10px 10px 0;padding:4px;background:#222;border-radius:4px;">{blk}<br><span style="font-size:9px;color:#888;">{s}-{e}</span></span>')
sections.append(("D: W/X Data Table (86-115)", "[CAT] W [PR|MB|HB] AB AB", ''.join(dparts)))

# E: 116-148
eparts = ''.join(box(o, *seen[o]) for o in range(116, 149) if o in seen)
sections.append(("E: Remainder (116-148)", "Unanalyzed", eparts))

sec_html = []
for title, pattern, content in sections:
    sec_html.append(
        f'<div style="margin:16px 0;padding:14px;background:#1a1a1a;border-radius:8px;border-left:4px solid #ffd700;">'
        f'<div style="font-size:14px;font-weight:bold;color:#ffd700;margin-bottom:4px;">{title}</div>'
        f'<div style="font-size:11px;color:#888;margin-bottom:10px;">{pattern}</div>'
        f'<div style="line-height:1;">{content}</div>'
        f'</div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000519 Formatted Blocks</title>
<style>
body {{ font-family: sans-serif; max-width: 1500px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.3em; }}
</style></head><body>
<h1>Khipu 1000519 — Color Blocks by Section</h1>
{''.join(sec_html)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000519-formatted-blocks.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
