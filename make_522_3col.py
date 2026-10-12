"""1000522 as three-column table: Sections A, B, C side by side."""
import sqlite3

COLORS = {
    'W': '#F5F5F5', 'KB': '#1a1a1a', 'MB': '#1B3A5C', 'GG': '#808080',
    'FR': '#CC4444', 'HB': '#8B6914', 'RB': '#AA2222', 'BG': '#8B4513',
    'AB': '#4A6FA5', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

sections = {
    'A': (8, 32),
    'B': (36, 65),
    'C': (67, 95),
}

data = {}
max_len = 0
for name, (s, e) in sections.items():
    c.execute('''
        SELECT c.CORD_ORDINAL, cc.COLOR_CD_1,
               (SELECT COUNT(*) FROM knot k WHERE k.CORD_ID = c.CORD_ID) as nk
        FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
        WHERE c.KHIPU_ID = 1000522 AND c.CORD_ORDINAL >= ? AND c.CORD_ORDINAL <= ?
        ORDER BY c.CORD_ORDINAL
    ''', (s, e))
    rows = [(o, (col or '?').strip(), nk) for o, col, nk in c.fetchall()]
    data[name] = rows
    max_len = max(max_len, len(rows))

# Build table rows
html_rows = []
for i in range(max_len):
    cells = []
    for name in ['A', 'B', 'C']:
        if i < len(data[name]):
            o, col, nk = data[name][i]
            hexcol = COLORS.get(col, '#CCCCCC')
            fg = '#fff' if col in ('KB', 'MB', 'BG', 'AB') else '#000'
            cells.append(
                f'<td style="background:{hexcol};color:{fg};padding:6px 12px;'
                f'text-align:center;border:1px solid #444;">'
                f'{col}<br><b>{nk}</b></td>'
            )
        else:
            cells.append('<td style="border:1px solid #333;"></td>')
    html_rows.append(f'<tr><td style="color:#666;padding:6px;">{i+1}</td>{"".join(cells)}</tr>')

# Totals
tot_cells = []
for name in ['A', 'B', 'C']:
    total = sum(nk for _, _, nk in data[name])
    tot_cells.append(
        f'<td style="padding:8px 12px;text-align:center;border:1px solid #444;'
        f'background:#2a2a2a;font-weight:bold;">{total} tufts</td>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000522 Three Columns</title>
<style>
body {{ font-family: sans-serif; max-width: 700px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
table {{ border-collapse: collapse; margin: 20px 0; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; }}
</style></head><body>
<h1>Khipu 1000522 — Three Sections as Columns</h1>
<p class="note">Sections A (ords 8–32), B (36–65), C (67–95) side by side.
Cell = color + tuft count. Row numbers are position within section, not ordinals.</p>
<table>
<tr><th></th><th style="padding:8px;">A</th><th style="padding:8px;">B</th><th style="padding:8px;">C</th></tr>
{''.join(html_rows)}
<tr><td></td>{''.join(tot_cells)}</tr>
</table>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000522-threecol.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
for name in ['A', 'B', 'C']:
    print(f"  Section {name}: {len(data[name])} cords, {sum(nk for _,_,nk in data[name])} tufts")
