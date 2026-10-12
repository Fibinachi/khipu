"""1000029 laid out with subtotal hierarchy."""
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
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, (col or '?').strip())
ords = sorted(seen.keys())

# Known subtotal: Ord 21 (YG=112) = sum of 23,24,25,27
# Structure: show it hierarchically, rest flat
subtotal_detail = {21: [23, 24, 25, 26, 27]}  # ord -> detail ords
detail_ords = set()
for details in subtotal_detail.values():
    detail_ords.update(details)

html_rows = []
for o in ords:
    if o in detail_ords:
        continue  # will be shown under parent
    cid, col = seen[o]
    hexcol = COLORS.get(col, '#CCCCCC')
    fg = '#fff' if col in ('MB','KB','DB','BB') else '#000'
    try: v = decode_cord(conn, cid)['value'] or 0
    except: v = 0

    is_subtotal = o in subtotal_detail
    row_bg = '#2a2a00' if is_subtotal else '#1a1a1a'
    label = 'SUBTOTAL' if is_subtotal else ''

    html_rows.append(
        f'<tr style="background:{row_bg};">'
        f'<td style="padding:6px 12px;color:#666;">{o}</td>'
        f'<td style="padding:6px 12px;background:{hexcol};color:{fg};font-weight:bold;">{col}</td>'
        f'<td style="padding:6px 12px;text-align:right;font-weight:bold;">{v}</td>'
        f'<td style="padding:6px 12px;color:#FFD700;">{label}</td>'
        f'</tr>'
    )

    # Detail rows indented
    if is_subtotal:
        for do in subtotal_detail[o]:
            if do not in seen: continue
            dcid, dcol = seen[do]
            dhex = COLORS.get(dcol, '#CCCCCC')
            dfg = '#fff' if dcol in ('MB','KB','DB','BB') else '#000'
            try: dv = decode_cord(conn, dcid)['value'] or 0
            except: dv = 0
            html_rows.append(
                f'<tr>'
                f'<td style="padding:4px 12px 4px 32px;color:#555;">└ {do}</td>'
                f'<td style="padding:4px 12px;background:{dhex};color:{dfg};">{dcol}</td>'
                f'<td style="padding:4px 12px;text-align:right;">{dv}</td>'
                f'<td></td>'
                f'</tr>'
            )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000029 Hierarchical</title>
<style>
body {{ font-family: monospace; max-width: 600px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
table {{ border-collapse: collapse; width: 100%; }}
td {{ border: 1px solid #333; }}
h1 {{ font-size: 1.2em; font-family: sans-serif; }}
.note {{ font-size: 0.85em; color: #aaa; font-family: sans-serif; }}
</style></head><body>
<h1>Khipu 1000029 — Hierarchical Layout</h1>
<p class="note">Subtotals (gold) with detail lines indented beneath.
Only one clear subtotal found: Ord 21 (YG=112).</p>
<table>
<tr><th>Ord</th><th>Color</th><th>Value</th><th></th></tr>
{''.join(html_rows)}
</table>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000029-hier.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
