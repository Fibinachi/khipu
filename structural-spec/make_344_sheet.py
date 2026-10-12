"""Render 1000344 as a true spreadsheet: rows x color-columns."""
import sqlite3
from decoder import decode_cord

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000344
    ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, (col or '?').strip())
ords = sorted(seen.keys())

# The column cycle: BL -> BY -> MB -> W (from bigram analysis)
# Parse sequence into rows: each row = one pass through the column order
COLS = ['BL', 'BY', 'MB', 'W']

rows = []
current = {}
for o in ords:
    cid, col = seen[o]
    if col not in COLS:
        continue
    try:
        v = decode_cord(conn, cid)['value'] or 0
    except:
        v = 0
    # If this color already in current row, start new row
    if col in current:
        rows.append(current)
        current = {}
    current[col] = v
if current:
    rows.append(current)

# Build HTML table
header = ''.join(f'<th style="padding:8px 16px;background:#2a2a2a;">{col}</th>' for col in COLS)
body_rows = []
for i, r in enumerate(rows):
    cells = []
    for col in COLS:
        v = r.get(col, '')
        bg = '#1e3a1e' if v != '' and v != 0 else '#1a1a1a'
        cells.append(f'<td style="padding:6px 16px;text-align:right;background:{bg};">{v}</td>')
    body_rows.append(f'<tr><td style="padding:6px 8px;color:#666;">{i+1}</td>{"".join(cells)}</tr>')

# Column totals
totals = []
for col in COLS:
    t = sum(r.get(col, 0) for r in rows if isinstance(r.get(col), int))
    totals.append(f'<td style="padding:8px 16px;text-align:right;background:#2a2a2a;font-weight:bold;">{t}</td>')

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000344 as Spreadsheet</title>
<style>
body {{ font-family: monospace; max-width: 800px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
table {{ border-collapse: collapse; margin: 20px 0; }}
th, td {{ border: 1px solid #444; }}
h1 {{ font-size: 1.3em; font-family: sans-serif; }}
.note {{ font-size: 0.9em; color: #aaa; font-family: sans-serif; max-width: 700px; }}
</style></head><body>
<h1>Khipu 1000344 as Spreadsheet</h1>
<p class="note">Musée Quai Branly. {len(rows)} rows × 4 color columns.
Reconstructed from the BL→BY→MB→W column rotation.
Green cells = nonzero values.</p>
<table>
<tr><th></th>{header}</tr>
{''.join(body_rows)}
<tr><td style="padding:8px;color:#666;">Total</td>{''.join(totals)}</tr>
</table>
<p class="note">If this is a table, the columns are the variables and the rows are the records.
What the columns <i>mean</i> is the field-label problem — but the structure is spreadsheet.</p>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000344-spreadsheet.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}: {len(rows)} rows")
for col in COLS:
    t = sum(r.get(col, 0) for r in rows if isinstance(r.get(col), int))
    print(f"  {col}: total={t}")
