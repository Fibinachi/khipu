"""Compressed strip for 1000096 (Lluta monster, 1831 cords)."""
import sqlite3

COLORS = {
    'W': '#F5F5F5', 'FB': '#4169E1', 'KB': '#1a1a1a', 'BS': '#8B5A2B',
    'SR': '#CC4444', 'HB': '#8B6914', '?': '#CCCCCC',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ORDINAL, cc.COLOR_CD_1, c.CORD_LEVEL
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000096
    ORDER BY c.CORD_ORDINAL
""")
seen = {}
for o, col, lvl in c.fetchall():
    if o not in seen:
        seen[o] = ((col or '?').strip(), lvl)
ords = sorted(seen.keys())
print(f"{len(ords)} ordinals")

# Compressed: 3px per cord
boxes = []
for o in ords:
    col, lvl = seen[o]
    hexcol = COLORS.get(col, '#CCCCCC')
    # Height by level
    h = 30 if lvl == 1 else (20 if lvl == 2 else 12)
    boxes.append(
        f'<div title="Ord {o} L{lvl}: {col}" '
        f'style="width:3px;height:{h}px;background:{hexcol};'
        f'display:inline-block;margin:0;vertical-align:bottom;"></div>'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000096 Strip</title>
<style>
body {{ font-family: sans-serif; max-width: 1400px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.2em; }}
.note {{ font-size: 0.85em; color: #aaa; max-width: 900px; }}
.strip {{ line-height: 0; word-wrap: break-word; margin: 20px 0; padding: 15px; background: #1a1a1a; border-radius: 6px; }}
</style></head><body>
<h1>Khipu 1000096 — Lluta Monster (compressed)</h1>
<p class="note">{len(ords)} ordinals, 1,831 cords. 3px per cord. Height = level (taller = L1).
Provenance: Percy Dauelsberg, Arica. Lluta Valley.
White dominates. FB/KB/BS are the color accents.</p>
<div class="strip">{''.join(boxes)}</div>
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000096-strip.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
