"""1000029 as transaction log: Seq | Color | Value."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'MB': '#1B3A5C', 'KB': '#1a1a1a', 'W': '#F5F5F5', 'DB': '#0a0a3a',
    'YB': '#DDD700', 'YG': '#9ACD32', 'BB': '#2a2a5a', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1
    FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000029 ORDER BY c.CORD_ORDINAL
""")

rows = []
for cid, o, col in c.fetchall():
    col = (col or '?').strip()
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0
    rows.append((o, col, v))

# Build log table, grouping consecutive same-color as entries
html_rows = []
prev_col = None
for o, col, v in rows:
    hexcol = COLORS.get(col, '#CCCCCC')
    fg = '#fff' if col in ('MB','KB','DB','BB') else '#000'
    # Divider when color changes
    divider = ''
    if col != prev_col and prev_col is not None:
        divider = '<tr><td colspan="3" style="border:none;height:4px;background:#333;"></td></tr>'
    bg = '#1e3a1e' if v else '#1a1a1a'
    html_rows.append(
        f'{divider}<tr>'
        f'<td style="padding:4px 12px;color:#666;">{o}</td>'
        f'<td style="padding:4px 12px;background:{hexcol};color:{fg};font-weight:bold;">{col}</td>'
        f'<td style="padding:4px 12px;text-align:right;background:{bg};">{v if v else ""}</td>'
        f'</tr>'
    )
    prev_col = col

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000029 Log</title>
<style>
body {{ font-family: monospace; max-width: 500px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
table {{ border-collapse: collapse; width: 100%; }}
td {{ border: 1px solid #333; }}
h1 {{ font-size: 1.2em; font-family: sans-serif; }}
.note {{ font-size: 0.85em; color: #aaa; font-family: sans-serif; }}
</style></head><body>
<h1>Khipu 1000029 — Transaction Log</h1>
<p class="note">211 entries in sequence. Color = category, value = amount.
Dividers mark category changes. Green = nonzero.</p>
<table>
<tr><th style="padding:6px;">Seq</th><th style="padding:6px;">Category</th><th style="padding:6px;">Value</th></tr>
{''.join(html_rows)}
</table>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000029-log.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}: {len(rows)} entries")
