"""1000519: W PR AB AB data table (ords 91-115)."""
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
    WHERE c.KHIPU_ID = 1000519 AND c.CORD_ORDINAL BETWEEN 91 AND 116
    ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, (col or '?').strip())

# Records: [CAT], W, PR, AB, AB
records = [
    (91, 95), (96, 100), (101, 105), (106, 110), (111, 115),
]

def box(o, cid, col, is_div=False, is_cat=False):
    hexcol = COLORS.get(col, '#CCCCCC')
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    h = 44
    label = str(v) if v else ''
    tc = '#000' if col in ('W', 'G0') else '#fff'
    if is_div:
        border = '2px solid #ff4444'
    elif is_cat:
        border = '2px solid #ffd700'
    elif v:
        border = '2px solid #0f0'
    else:
        border = '1px solid #555'
    return (f'<div title="Ord {o}: {col}={v}" '
            f'style="width:34px;height:{h}px;background:{hexcol};'
            f'display:inline-block;margin:2px;vertical-align:bottom;'
            f'border:{border};border-radius:4px;text-align:center;'
            f'color:{tc};font-size:12px;line-height:{h}px;font-weight:bold;">{label}</div>')

row_html = []
table_rows = []
for n, (s, e) in enumerate(records, 1):
    cords = []
    vals = {}
    for o in range(s, e+1):
        cid, col = seen[o]
        try: v = decode_cord(conn, cid)['value'] or 0
        except: v = 0
        vals[col] = v
        # first cord is category, last two are divider
        is_cat = (o == s)
        is_div = (o >= e-1)
        cords.append(box(o, cid, col, is_div, is_cat))
    cat = seen[s][1]
    wv = vals.get('W', 0)
    prv = vals.get('PR', vals.get('HB', 0))
    table_rows.append(f'<tr><td>{n}</td><td>{cat}</td><td>{wv}</td><td>{prv}</td></tr>')
    row_html.append(
        f'<div style="margin:8px 0;padding:8px;background:#1a1a1a;border-radius:6px;line-height:1;">'
        f'<span style="color:#888;font-size:12px;">Record {n} (ords {s}-{e})</span><br>{"".join(cords)}</div>'
    )

table = f"""
<table border="1" cellpadding="8" style="border-collapse:collapse;margin:20px 0;font-size:14px;">
<tr style="background:#333;"><th>Record</th><th>Category</th><th>W value</th><th>PR value</th></tr>
{''.join(table_rows)}
</table>"""

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000519 Data Table</title>
<style>
body {{ font-family: sans-serif; max-width: 1200px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.3em; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 900px; }}
table {{ color: #eee; }} td, th {{ border: 1px solid #555; }}
</style></head><body>
<h1>Khipu 1000519 — W/PR Data Table (ords 91-115)</h1>
<p class="note">Gold = category. Green-bordered = values. Red = AB AB divider.</p>
{table}
{''.join(row_html)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000519-datatable.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
