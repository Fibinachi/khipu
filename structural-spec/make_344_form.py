"""Render 1000344 rows 2-7 as form template: constants vs variable field."""
import sqlite3
from decoder import decode_cord

COLORS = {
    'W': '#F5F5F5', 'MB': '#1B3A5C', 'BY': '#FFD700', 'BL': '#000080',
    '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, cc.COLOR_CD_1
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000344 ORDER BY c.CORD_ORDINAL
""")
seen = {}
for cid, o, col in c.fetchall():
    if o not in seen:
        seen[o] = (cid, (col or '?').strip())
ords = sorted(seen.keys())

markers = [44, 57, 69, 81, 93, 105, 117, 120, 128, 139, 192, 225, 310]
bounds = [0] + markers + [ords[-1]+1]
rows = []
for i in range(len(bounds)-1):
    rows.append([o for o in ords if bounds[i] <= o < bounds[i+1]])

# Template positions (0-indexed within row) for rows 2-7 (index 1-6)
# From analysis: pos0=BY22(marker), pos1=BY32/33, pos2=BL66, pos3=BY32, pos4=MB33,
#                pos5=W42/43, pos6=W variable, pos7=BY12, pos8+=trailing
TEMPLATE_CONSTANTS = {2: 66, 3: 32, 4: 33}  # pos: expected value (BL66, BY32, MB33)
VARIABLE_POS = 6  # the W variable field

html_rows = []
for ri in range(1, 7):  # rows 2-7 (index 1-6)
    row_ords = rows[ri]
    cells = []
    for pi, o in enumerate(row_ords):
        cid, col = seen[o]
        try: v = decode_cord(conn, cid)['value'] or 0
        except: v = 0
        hexcol = COLORS.get(col, '#CCCCCC')

        # Classify: marker, template constant, variable, other
        if pi == 0 and col == 'BY' and v == 22:
            role = 'marker'
            bg_style = 'outline:3px solid #FF0000;'
            label = f'ROW MARKER'
        elif pi in TEMPLATE_CONSTANTS and v == TEMPLATE_CONSTANTS[pi]:
            role = 'template'
            bg_style = 'outline:2px solid #00FF00;'
            label = f'TEMPLATE (constant {v})'
        elif pi == VARIABLE_POS:
            role = 'variable'
            bg_style = 'outline:3px solid #FFD700;background:#3a3a00;'
            label = f'VARIABLE FIELD = {v}'
        else:
            role = 'other'
            bg_style = 'border:1px solid #555;'
            label = f'{col}={v}'

        h = min(20 + v * 0.8, 80) if v else 12
        cells.append(
            f'<div title="Ord {o} pos{pi}: {label}" '
            f'style="width:28px;height:{h}px;background:{hexcol};{bg_style}'
            f'display:inline-block;margin:2px;vertical-align:bottom;'
            f'text-align:center;font-size:9px;color:#000;font-weight:bold;'
            f'line-height:{h}px;">{v}</div>'
        )

    html_rows.append(
        f'<div style="margin:16px 0;padding:12px;background:#1a1a1a;'
        f'border-radius:6px;border:1px solid #333;">'
        f'<div style="font-size:0.9em;color:#fff;margin-bottom:8px;font-weight:bold;">'
        f'Form instance {ri} — ordinals {row_ords[0]}–{row_ords[-1]}</div>'
        f'<div style="line-height:1;">{"".join(cells)}</div>'
        f'<div style="font-size:0.75em;color:#888;margin-top:6px;">'
        f'<span style="color:#FF0000;">■</span> row marker &nbsp;'
        f'<span style="color:#00FF00;">■</span> template constant &nbsp;'
        f'<span style="color:#FFD700;">■</span> variable field'
        f'</div></div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000344 Form Template</title>
<style>
body {{ font-family: sans-serif; max-width: 1200px; margin: 20px auto; padding: 0 20px; background: #0a0a0a; color: #eee; }}
h1 {{ font-size: 1.3em; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 850px; }}
</style></head><body>
<h1>Khipu 1000344 — Form Template (Rows 2–7)</h1>
<p class="note">Six instances of the same form. <span style="color:#FF0000;">Red</span> = row marker (BY=22).
<span style="color:#00FF00;">Green</span> = template constants (BL=66, BY=32, MB=33 — identical every row).
<span style="color:#FFD700;">Gold</span> = the variable field (W value: 177, 178, 1179, 189, 178, 187).
The scribe fills one field; the rest is the form.</p>
{''.join(html_rows)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000344-form.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
