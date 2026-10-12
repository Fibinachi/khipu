"""Detailed inspection of top journal candidates."""
import csv, os, sqlite3, sys
from collections import Counter

BASE = os.path.expanduser('~/workspace/quipu-analysis')
sys.path.insert(0, BASE)
from decoder import decode_cord

TOP = ['1000103', '1000368', '1000063', '1000501', '1000085',
       '1000586', '1000198', '1000565', '1000612', '1000148']

def main():
    conn = sqlite3.connect(os.path.join(BASE, 'okr-khipu.db'))
    c = conn.cursor()
    out = []
    for kid in TOP:
        c.execute("""SELECT CORD_ID, CORD_ORDINAL, CORD_LEVEL FROM cord
                     WHERE KHIPU_ID = ? ORDER BY CORD_ORDINAL""", (kid,))
        cords = c.fetchall()
        vals, colors, levels = [], [], []
        for cid, ordinal, level in cords:
            try:
                res = decode_cord(conn, cid)
                v = res.get('value')
                vals.append(v if v is not None else -1)
            except Exception:
                vals.append(-1)
            c2 = conn.cursor()
            c2.execute("SELECT COLOR_CD_1 FROM ascher_cord_color WHERE CORD_ID = ?", (cid,))
            cr = c2.fetchone()
            colors.append(cr[0] if cr and cr[0] else '?')
            levels.append(level)

        # Value-over-position sparkline (first 80 L1 cords)
        l1_idx = [i for i, l in enumerate(levels) if l == 1][:80]
        l1_vals = [vals[i] for i in l1_idx if vals[i] >= 0]
        mx = max(l1_vals) if l1_vals else 1
        blocks = ' .:-=+*#%@'
        spark = ''.join(blocks[min(int(v / max(mx, 1) * 9), 9)] for v in l1_vals[:80])

        col_counts = Counter(colors)
        lvl_counts = Counter(levels)
        # Section markers: look for color runs / W separators
        # Count color transitions
        transitions = sum(1 for i in range(1, len(colors)) if colors[i] != colors[i-1])

        # Provenance
        c.execute("SELECT PROVENANCE, REGION, MUSEUM_NAME, NICKNAME, NOTES FROM khipu_main WHERE KHIPU_ID = ?",
                  (kid,))
        prow = c.fetchone()

        # Nonzero value stats
        nz = [v for v in vals if v > 0]
        out.append({
            'khipu_id': kid,
            'n_cords': len(cords),
            'levels': dict(lvl_counts),
            'top_colors': col_counts.most_common(6),
            'n_transitions': transitions,
            'val_min': min(vals) if vals else None,
            'val_max': max(vals) if vals else None,
            'n_nonzero': len(nz),
            'sparkline_L1': spark,
            'provenance': (prow[0] or '') if prow else '',
            'region': (prow[1] or '') if prow else '',
            'museum': (prow[2] or '') if prow else '',
            'nickname': (prow[3] or '') if prow else '',
            'notes': ((prow[4] or '')[:300]) if prow else '',
        })

    conn.close()

    with open(os.path.join(BASE, 'journal-hunt/top_journals.md'), 'w') as f:
        f.write("# Top Journal Candidates: Detailed Profiles\n\n")
        for o in out:
            f.write(f"## {o['khipu_id']}\n\n")
            f.write(f"- **Cords:** {o['n_cords']}, levels: {o['levels']}\n")
            f.write(f"- **Colors:** {', '.join(f'{k}({v})' for k, v in o['top_colors'])}\n")
            f.write(f"- **Color transitions:** {o['n_transitions']}\n")
            f.write(f"- **Values:** range [{o['val_min']}, {o['val_max']}], {o['n_nonzero']} nonzero\n")
            f.write(f"- **Value sparkline (first 80 L1):**\n  `{o['sparkline_L1']}`\n")
            f.write(f"- **Provenance:** {o['provenance']}\n")
            f.write(f"- **Region:** {o['region']}\n")
            f.write(f"- **Museum:** {o['museum']}\n")
            f.write(f"- **Nickname:** {o['nickname']}\n")
            f.write(f"- **Notes:** {o['notes']}\n\n")

    # Also print to stdout
    for o in out:
        print(f"=== {o['khipu_id']} ===")
        print(f"  cords={o['n_cords']} levels={o['levels']}")
        print(f"  colors: {', '.join(f'{k}({v})' for k, v in o['top_colors'])}")
        print(f"  transitions={o['n_transitions']} vals=[{o['val_min']},{o['val_max']}] nonzero={o['n_nonzero']}")
        print(f"  spark: {o['sparkline_L1'][:80]}")
        print(f"  prov={o['provenance'][:50]} museum={o['museum'][:40]}")
        print()

if __name__ == '__main__':
    main()
