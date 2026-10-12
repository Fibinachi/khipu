"""Contents of the three five-groups in 1000396 section 5."""
import sqlite3
from decoder import decode_cord

COLORS = {'AB': '#4A6FA5', 'MB': '#1B3A5C'}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

groups = [
    ('Five-Pack 1', 141, 145, [(141,'AB',8),(142,'MB',8),(143,'AB',12),(144,'AB',0),(145,'AB',49)]),
    ('Five-Pack 2', 147, 151, [(147,'AB',2),(148,'MB',7),(149,'MB',17),(150,'AB',0),(151,'MB',33)]),
    ('Five-Pack 3', 159, 163, [(159,'MB',11),(160,'MB',13),(161,'MB',27),(162,'AB',0),(163,'AB',17)]),
]

html_groups = []
for name, s, e, cords in groups:
    cells = []
    total = sum(v for _,_,v in cords)
    for o, col, v in cords:
        hexcol = COLORS[col]
        h = min(20 + v * 3, 180) if v else 12
        # Highlight the large value and zero
        if v == 0:
            border = 'border:3px dashed #FF0000;'
            label = 'ZERO'
        elif v == max(vv for _,_,vv in cords):
            border = 'border:3px solid #FFD700;'
            label = f'MAX={v}'
        else:
            border = 'border:1px solid #555;'
            label = f'{v}'
        cells.append(
            f'<div title="Ord {o}: {col}={v}" '
            f'style="width:60px;height:{h}px;background:{hexcol};{border}'
            f'display:inline-block;margin:3px;vertical-align:bottom;'
            f'text-align:center;color:#fff;font-weight:bold;font-size:14px;'
            f'line-height:{h}px;">{v}</div>'
        )
    html_groups.append(
        f'<div style="margin:16px 0;padding:14px;background:#1a1a1a;border-radius:8px;">'
        f'<div style="font-weight:bold;font-size:1.1em;margin-bottom:4px;">{name} '
        f'<span style="color:#888;">(ords {s}–{e})</span></div>'
        f'<div style="font-size:0.85em;color:#aaa;margin-bottom:8px;">'
        f'Total: {total} &nbsp;|&nbsp; '
        f'<span style="color:#FF0000;">dashed</span>=zero &nbsp;'
        f'<span style="color:#FFD700;">gold</span>=max</div>'
        f'<div>{"".join(cells)}</div></div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Five-Packs</title>
<style>
body {{ font-family: sans-serif; max-width: 800px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 700px; }}
</style></head><body>
<h1>1000396 Section 5 — Five-Pack Contents</h1>
<p class="note">Each pack: 5 blues, one zero, one large value, rest small.
Same internal shape, different totals (77, 59, 68).</p>
{''.join(html_groups)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000396-fivepacks.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
