"""1000519: formatted as documents."""
import sqlite3
from decoder import decode_cord

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

def val(o):
    if o not in seen: return 0
    cid, col = seen[o]
    try: return decode_cord(conn, cid)['value'] or 0
    except: return 0

def col(o):
    return seen[o][1] if o in seen else '?'

# Doc A: Head
head_html = """
<h2>Document A: Head</h2>
<table border="1" cellpadding="6" style="border-collapse:collapse;">
<tr style="background:#333;"><th>Ord</th><th>Color</th><th>Value</th><th>Role</th></tr>
<tr><td>1</td><td>AB</td><td>0</td><td>Category</td></tr>
<tr><td style="color:#0f0;">(restored)</td><td style="color:#0f0;">Green</td><td>—</td><td>Category</td></tr>
<tr><td>2</td><td>W</td><td>40</td><td>Data</td></tr>
<tr><td>3</td><td>MB</td><td>236</td><td>Data</td></tr>
<tr><td>4</td><td>AB</td><td>50</td><td>Divider</td></tr>
</table>"""

# Doc B: 8 blocks
b_rows = []
for b in range(8):
    s = 5 + b*5
    cells = ' | '.join(f'{col(o)}={val(o)}' for o in range(s, s+5))
    b_rows.append(f'<tr><td>{b+1}</td><td>{s}-{s+4}</td><td>{cells}</td></tr>')
docb_html = f"""
<h2>Document B: Eight 5-Cord Blocks</h2>
<table border="1" cellpadding="6" style="border-collapse:collapse;">
<tr style="background:#333;"><th>Block</th><th>Ords</th><th>Colors = Values</th></tr>
{''.join(b_rows)}
</table>"""

# Doc D: W/PR table
d_rows = []
for n, (s, label) in enumerate([(86,'G0'), (91,'G0'), (96,'PB'), (101,'G0'), (106,'PB'), (111,'PB')], 1):
    wv = val(s+1)
    # X slot varies: PR, MB, HB
    xv = val(s+2)
    xc = col(s+2)
    d_rows.append(f'<tr><td>{n}</td><td>{label}</td><td>{wv}</td><td>{xc}={xv}</td></tr>')
docd_html = f"""
<h2>Document D: W/X Data Table (ords 86-115)</h2>
<table border="1" cellpadding="6" style="border-collapse:collapse;">
<tr style="background:#333;"><th>Record</th><th>Category</th><th>W</th><th>X</th></tr>
{''.join(d_rows)}
</table>"""

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000519 Formatted</title>
<style>
body {{ font-family: sans-serif; max-width: 1000px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.3em; }} h2 {{ font-size: 1.1em; color: #ffd700; margin-top: 30px; }}
table {{ color: #eee; margin: 10px 0; }} td, th {{ border: 1px solid #555; }}
.note {{ color: #aaa; font-size: 0.9em; }}
</style></head><body>
<h1>Khipu 1000519 — Formatted Documents</h1>
<p class="note">Sections C (45-90) and E (116-148) pending analysis.</p>
{head_html}
{docb_html}
{docd_html}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000519-formatted.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
