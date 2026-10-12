"""Visualize 1000331 split into sections at BG markers."""
import sqlite3

COLORS = {
    'W': '#F5F5F5', 'AB': '#4A6FA5', 'MB': '#1B3A5C', 'BG': '#8B4513',
    'PK': '#DDA0DD', 'SY': '#FFD700', 'RL': '#CC0000', 'RB': '#8B0000',
    'KB': '#000000', 'CB': '#8B7355', 'YB': '#DAA520', 'GG': '#808080',
}

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()
c.execute("""
    SELECT c.CORD_ORDINAL, cc.COLOR_CD_1, cc.COLOR_CD_2
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = 1000331
    ORDER BY c.CORD_ORDINAL, cc.COLOR_CD_1
""")

seen = {}
for ordinal, c1, c2 in c.fetchall():
    if ordinal not in seen:
        seen[ordinal] = (c1 or '?', c2 or '')
ords = sorted(seen.keys())

# Split into sections at BG
sections = []
current = []
for o in ords:
    c1, c2 = seen[o]
    current.append((o, c1, c2))
    if c1 == 'BG':
        sections.append(current)
        current = []
if current:
    sections.append(current)

def box(o, c1, c2, highlight=False):
    label = c1 + (f'+{c2}' if c2 else '')
    hexcol = COLORS.get(c1, '#CCCCCC')
    border = f'border:2px solid {COLORS.get(c2, "#999")};' if c2 else 'border:1px solid #999;'
    if c1 == 'BG':
        border = 'border:3px solid #FFD700;'
    return (f'<div title="Cord {o}: {label}" style="width:22px;height:36px;'
            f'background:{hexcol};{border}display:inline-block;margin:1px;'
            f'vertical-align:bottom;"></div>')

html_sections = []
for i, sec in enumerate(sections):
    boxes = ''.join(box(o, c1, c2) for o, c1, c2 in sec)
    # Section stats
    colors = [c1 for _, c1, _ in sec]
    uniq = sorted(set(colors))
    html_sections.append(
        f'<div style="margin:18px 0;padding:12px;background:#222;border-radius:6px;">'
        f'<div style="font-size:0.85em;color:#aaa;margin-bottom:8px;">'
        f'Section {i+1} — {len(sec)} cords (ordinals {sec[0][0]}–{sec[-1][0]}) — '
        f'colors: {", ".join(uniq)}</div>'
        f'<div style="line-height:0;">{boxes}</div></div>'
    )

legend_items = []
for code, hexcol in sorted(COLORS.items()):
    legend_items.append(
        f'<span style="display:inline-block;width:16px;height:16px;'
        f'background:{hexcol};border:1px solid #999;vertical-align:middle;"></span> {code}'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000331 by Section (BG markers)</title>
<style>
body {{ font-family: sans-serif; max-width: 1200px; margin: 20px auto; padding: 0 20px; background: #1a1a1a; color: #eee; }}
h1 {{ font-size: 1.4em; }}
.legend {{ margin: 16px 0; font-size: 0.85em; line-height: 2; }}
.legend span {{ margin-right: 12px; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 800px; }}
</style></head><body>
<h1>Khipu 1000331 — Sections Split at BG Markers</h1>
<p class="note">BG (brown, gold-bordered) occurs only after AB — 13/13 times. Treating each BG as a
section terminator yields {len(sections)} sections. Each section is a color-sequence unit.</p>
<div class="legend">{' '.join(legend_items)}</div>
{''.join(html_sections)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000331-sections.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}: {len(sections)} sections")
for i, sec in enumerate(sections):
    print(f"  Section {i+1}: {len(sec)} cords, ordinals {sec[0][0]}-{sec[-1][0]}")
