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

def blue_tile():
    return ('<div title="restored blue (MB)" style="display:inline-block;text-align:center;margin:2px;vertical-align:top;">'
            '<div style="width:30px;height:36px;background:#1B3A5C;'
            'border:2px solid #ffd700;border-radius:3px;"></div>'
            '<div style="font-size:9px;color:#888;margin-top:2px;">o? MB</div>'
            '</div>')

def red_tile():
    return ('<div title="restored red (RL)" style="display:inline-block;text-align:center;margin:2px;vertical-align:top;">'
            '<div style="width:30px;height:36px;background:#FF0000;'
            'border:2px solid #ffd700;border-radius:3px;"></div>'
            '<div style="font-size:9px;color:#888;margin-top:2px;">o? RL</div>'
            '</div>')

def blank_tile():
    return ('<div title="missing cord" style="display:inline-block;text-align:center;margin:2px;vertical-align:top;">'
            '<div style="width:30px;height:36px;background:#2a2a2a;'
            'border:2px dashed #888;border-radius:3px;"></div>'
            '<div style="font-size:9px;color:#888;margin-top:2px;">missing</div>'
            '</div>')

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
p3 = []
p4 = []
p5 = []
p6 = []
p7 = []
p7b = []
p8 = []
for i, o in enumerate(ords):
    b = box(i+1, o, *seen[o])
    n = i+1
    if n <= 6:
        p1.append(b)
    elif n <= 12:
        p2.append(b)
    elif n <= 16:
        p3.append(b)
        if n == 13:
            p3.append(red_tile())
            p3.append(blue_tile())
    elif n == 17:
        p4.append(b)
    elif n == 18:
        p4.append(b)
        p4.append(blue_tile())
    elif n <= 21:
        p4.append(b)
    elif n <= 26:
        p5.append(b)
        if n == 22:
            p5.append(red_tile())
    elif n <= 31:
        p6.append(b)
        if n == 27:
            p6.append(red_tile())
    elif n <= 36:
        p7.append(b)
        if n == 32:
            p7.append(red_tile())
    elif n <= 41:
        p7b.append(b)
    else:
        p8.append(b)
part1 = ''.join(p1)
part2 = ''.join(p2)
part3 = ''.join(p3)
part4 = ''.join(p4)
part5 = ''.join(p5)
part6 = ''.join(p6)
part7 = ''.join(p7)
part7b = ''.join(p7b)
part8 = ''.join(p8)

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
<div style="font-size:13px;font-weight:bold;color:#ffd700;margin-bottom:8px;">Part 2: #7-12 (ords 51-56)</div>
<div style="line-height:1;">{part2}</div>
</div>
<div style="margin:12px 0;padding:14px;background:#1a1a1a;border-radius:8px;border-left:4px solid #ffd700;">
<div style="font-size:13px;font-weight:bold;color:#ffd700;margin-bottom:8px;">Part 3: #13 + red + blue + #14-16 (ords 57-60)</div>
<div style="line-height:1;">{part3}</div>
</div>
<div style="margin:12px 0;padding:14px;background:#1a1a1a;border-radius:8px;border-left:4px solid #ffd700;">
<div style="font-size:13px;font-weight:bold;color:#ffd700;margin-bottom:8px;">Part 4: #17-18 + blue + #19-21 (ords 61-65)</div>
<div style="line-height:1;">{part4}</div>
</div>
<div style="margin:12px 0;padding:14px;background:#1a1a1a;border-radius:8px;border-left:4px solid #ffd700;">
<div style="font-size:13px;font-weight:bold;color:#ffd700;margin-bottom:8px;">Part 5: #22-26 (ords 66-70)</div>
<div style="line-height:1;">{part5}</div>
</div>
<div style="margin:12px 0;padding:14px;background:#1a1a1a;border-radius:8px;border-left:4px solid #ffd700;">
<div style="font-size:13px;font-weight:bold;color:#ffd700;margin-bottom:8px;">Part 6: #27-31 (ords 71-75)</div>
<div style="line-height:1;">{part6}</div>
</div>
<div style="margin:12px 0;padding:14px;background:#1a1a1a;border-radius:8px;border-left:4px solid #ffd700;">
<div style="font-size:13px;font-weight:bold;color:#ffd700;margin-bottom:8px;">Part 7: #32-36 (ords 76-80)</div>
<div style="line-height:1;">{part7}</div>
</div>
<div style="margin:12px 0;padding:14px;background:#1a1a1a;border-radius:8px;border-left:4px solid #ffd700;">
<div style="font-size:13px;font-weight:bold;color:#ffd700;margin-bottom:8px;">Part 7b: #37-41 (ords 81-85)</div>
<div style="line-height:1;">{part7b}</div>
</div>
<div style="margin:12px 0;padding:14px;background:#1a1a1a;border-radius:8px;border-left:4px solid #ffd700;">
<div style="font-size:13px;font-weight:bold;color:#ffd700;margin-bottom:8px;">Part 8: #42-46 (ords 86-90)</div>
<div style="line-height:1;">{part8}</div>
</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000519-secc-blocks18.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
