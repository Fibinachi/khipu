"""Visualize 1000331 with two-level hierarchy: BG = major sections, WWW = sub-sections."""
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
seq = [(o, seen[o][0], seen[o][1]) for o in ords]

# Find WWW triplet start positions
www_starts = set()
for i in range(len(seq)-2):
    if seq[i][1]=='W' and seq[i+1][1]=='W' and seq[i+2][1]=='W':
        # Only mark the first of overlapping
        if not www_starts or i > max(www_starts)+2:
            www_starts.add(i)

def box(o, c1, c2):
    label = c1 + (f'+{c2}' if c2 else '')
    hexcol = COLORS.get(c1, '#CCCCCC')
    border = f'border:2px solid {COLORS.get(c2, "#999")};' if c2 else 'border:1px solid #555;'
    extra = ''
    if c1 == 'BG':
        border = 'border:3px solid #FFD700;'
    if c1 == 'W':
        extra = 'box-shadow: inset 0 0 0 1px #999;'
    return (f'<div title="Cord {o}: {label}" style="width:20px;height:34px;'
            f'background:{hexcol};{border}{extra}display:inline-block;margin:1px;'
            f'vertical-align:bottom;"></div>')

# Build: major sections split at BG, sub-sections split at WWW
html_parts = []
major_num = 0
i = 0
while i < len(seq):
    major_num += 1
    # Collect until BG (inclusive)
    major = []
    while i < len(seq):
        major.append(seq[i])
        is_bg = seq[i][1] == 'BG'
        i += 1
        if is_bg:
            break
    # Within major, split at WWW starts
    sub_html = []
    sub_num = 0
    j = 0
    # Find www indices relative to major
    rel_www = sorted([w - (len(seq) - len(major) - (len(seq)-i)) for w in www_starts])
    # Simpler: track absolute
    abs_start = seq.index(major[0])
    k = 0
    sub = []
    sub_num = 0
    for m_idx, (o, c1, c2) in enumerate(major):
        abs_idx = abs_start + m_idx
        if abs_idx in www_starts and sub:
            # End current sub, start new
            sub_num += 1
            boxes = ''.join(box(oo, cc1, cc2) for oo, cc1, cc2 in sub)
            sub_html.append(
                f'<div style="margin:6px 0;padding:6px;background:#2a2a2a;'
                f'border-left:3px solid #F5F5F5;border-radius:3px;">'
                f'<div style="font-size:0.75em;color:#999;margin-bottom:4px;">'
                f'§{major_num}.{sub_num} — {len(sub)} cords</div>'
                f'<div style="line-height:0;">{boxes}</div></div>'
            )
            sub = []
        sub.append((o, c1, c2))
    if sub:
        sub_num += 1
        boxes = ''.join(box(oo, cc1, cc2) for oo, cc1, cc2 in sub)
        sub_html.append(
            f'<div style="margin:6px 0;padding:6px;background:#2a2a2a;'
            f'border-left:3px solid #F5F5F5;border-radius:3px;">'
            f'<div style="font-size:0.75em;color:#999;margin-bottom:4px;">'
            f'§{major_num}.{sub_num} — {len(sub)} cords</div>'
            f'<div style="line-height:0;">{boxes}</div></div>'
        )

    o_first, o_last = major[0][0], major[-1][0]
    colors = sorted(set(c1 for _, c1, _ in major))
    html_parts.append(
        f'<div style="margin:20px 0;padding:14px;background:#1e1e1e;'
        f'border:2px solid #8B4513;border-radius:8px;">'
        f'<div style="font-size:0.95em;color:#DAA520;margin-bottom:10px;font-weight:bold;">'
        f'Section {major_num} — {len(major)} cords (ordinals {o_first}–{o_last})<br>'
        f'<span style="font-weight:normal;font-size:0.85em;color:#aaa;">'
        f'colors: {", ".join(colors)}</span></div>'
        f'{"".join(sub_html)}</div>'
    )

legend_items = []
for code, hexcol in sorted(COLORS.items()):
    legend_items.append(
        f'<span style="display:inline-block;width:14px;height:14px;'
        f'background:{hexcol};border:1px solid #999;vertical-align:middle;"></span> {code}'
    )

html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>1000331 Two-Level Structure</title>
<style>
body {{ font-family: sans-serif; max-width: 1200px; margin: 20px auto; padding: 0 20px; background: #111; color: #eee; }}
h1 {{ font-size: 1.4em; }}
.legend {{ margin: 14px 0; font-size: 0.8em; line-height: 2; }}
.legend span {{ margin-right: 10px; }}
.note {{ font-size: 0.9em; color: #aaa; max-width: 850px; }}
</style></head><body>
<h1>Khipu 1000331 — Two-Level Sectional Structure</h1>
<p class="note"><b style="color:#DAA520;">Brown-bordered panels</b> = major sections (split at BG markers, 13 total).
<b style="color:#F5F5F5;">White-bar sub-panels</b> = sub-sections (split at WWW triplets, 5 total).
BG terminates a major section. WWW (triple white) opens a sub-section, typically followed by AB&nbsp;AB&nbsp;AB.</p>
<div class="legend">{' '.join(legend_items)}</div>
{''.join(html_parts)}
</body></html>"""

out = '/home/hatch/workspace/quipu-analysis/language-hunt/1000331-hierarchy.html'
with open(out, 'w') as f:
    f.write(html)
print(f"Wrote {out}")
