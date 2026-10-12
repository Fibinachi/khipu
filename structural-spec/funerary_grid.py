#!/usr/bin/env python3
"""Side-by-side strip visualization of all 26 funerary khipu."""
import sqlite3
import os

DB = os.path.expanduser("~/workspace/quipu-analysis/okr-khipu.db")
OUT = os.path.expanduser("~/workspace/quipu-analysis/funerary-side-by-side.html")

FUNERARY = [1000000,1000001,1000002,1000003,1000004,1000005,1000006,1000007,
            1000008,1000009,1000010,1000011,1000012,1000018,1000019,1000020,
            1000021,1000022,1000023,1000024,1000025,1000045,1000235,1000366,
            1000367,1000648]

# Ascher color -> hex (approximations from ascher_color_dc RGB)
COLOR_HEX = {
    'W': '#f5f5f0', 'AB': '#a86540', 'MB': '#673923', 'B': '#7d522d',
    'BB': '#3f2512', 'KB': '#38170c', 'DB': '#4d2214', 'HB': '#5a3d30',
    'BS': '#753300', 'LB': '#593300', 'EB': '#786141', 'BY': '#b48764',
    'CB': '#32221a', 'GA': '#503d33', 'GB': '#966a57',
    'BL': '#919191', 'BG': '#4a545c', 'GL': '#30626b', 'LA': '#7d7470',
    'LC': '#2c3336', 'LD': '#464544', 'LG': '#baaf96',
    'G': '#48432d', 'GG': '#575e4e', 'GR': '#49423d', 'DG': '#232c16',
    'G0': '#52452c', '0G': '#8b7350', 'GY': '#4d4234', '0D': '#27261a',
    '0L': '#2b2517', '0K': '#121a10', 'KG': '#45453b',
    'Y': '#c37629', '0Y': '#b8480a', '0R': '#c34d0a', 'N': '#c34d0a',
    'FR': '#7f1810', 'FB': '#140e0b', 'Z': '#140e0b', 'LK': '#131313',
    'SP': '#d4a017', 'RL': '#a52a2a', 'RB': '#8b0000', 'PG': '#9370db',
    'SY': '#ffff00', 'TF': '#d2b48c', 'EE': '#800080', 'LL': '#228b22',
}

conn = sqlite3.connect(DB)
c = conn.cursor()

khipu_data = []
for kid in FUNERARY:
    c.execute("""SELECT c.CORD_ORDINAL, cc.COLOR_CD_1
                 FROM cord c JOIN ascher_cord_color cc
                   ON cc.CORD_ID=c.CORD_ID AND cc.KHIPU_ID=c.KHIPU_ID
                 WHERE c.KHIPU_ID=? AND cc.COLOR_CD_1 IS NOT NULL AND cc.COLOR_CD_1!=''
                 ORDER BY c.CORD_ORDINAL""", (kid,))
    cords = c.fetchall()
    c.execute("SELECT PROVENANCE, NOTES FROM khipu_main WHERE KHIPU_ID=?", (kid,))
    prov, notes = c.fetchone() or ("?", "")
    khipu_data.append({"id": kid, "cords": cords, "prov": prov or "?"})

conn.close()

# Build HTML
cells = []
for k in khipu_data:
    strips = []
    for ord_, col in k["cords"]:
        hx = COLOR_HEX.get(col, '#888888')
        border = 'border:1px solid #999;' if col == 'W' else ''
        strips.append(
            f'<div title="{ord_}: {col}" style="width:14px;height:34px;background:{hx};{border}display:inline-block;margin:0;"></div>')
    cells.append(f"""
    <div style="margin:8px;padding:8px;border:1px solid #ccc;display:inline-block;vertical-align:top;background:#fafafa;">
      <div style="font-family:monospace;font-size:12px;font-weight:bold;margin-bottom:4px;">{k["id"]}</div>
      <div style="font-family:monospace;font-size:10px;color:#666;margin-bottom:4px;">{k["prov"]} · {len(k["cords"])} cords</div>
      <div style="line-height:0;">{''.join(strips)}</div>
    </div>""")

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Funerary Khipu — Side by Side</title></head>
<body style="font-family:sans-serif;padding:16px;background:#fff;">
<h2>Funerary Khipu — All 26 Side by Side</h2>
<p style="color:#555;max-width:800px;">Each strip shows cord colors in ordinal order (left to right = first to last pendant).
Leymebamba cluster dominates (22 of 26). Colors approximate Ascher codes.</p>
<div>{''.join(cells)}</div>
<p style="color:#888;font-size:12px;margin-top:16px;">Generated {__import__('datetime').date.today()} from okr-khipu.db</p>
</body></html>"""

with open(OUT, "w") as f:
    f.write(html)
print(f"Wrote {OUT} with {len(khipu_data)} khipu")
