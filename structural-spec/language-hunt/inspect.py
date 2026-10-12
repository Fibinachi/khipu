"""Deep inspection of top language-like candidates.

For each candidate: show the full cord sequence (decoded), color/value patterns,
and assess whether it reads as sequential language vs dense tabular data.
"""
import csv, os, sqlite3, sys
sys.path.insert(0, os.path.expanduser('~/workspace/quipu-analysis'))
from decoder import decode_cord

BASE = os.path.expanduser('~/workspace/quipu-analysis')
DB = os.path.join(BASE, 'okr-khipu.db')

def get_cords(khipu_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT c.CORD_ID, c.CORD_ORDINAL, c.CORD_LEVEL, cc.COLOR_CD_1, cc.COLOR_CD_2
        FROM cord c
        LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
        WHERE c.KHIPU_ID = ?
        ORDER BY c.CORD_ORDINAL
    """, (khipu_id,))
    rows = c.fetchall()
    result = []
    for cid, ordinal, level, col1, col2 in rows:
        try:
            dec = decode_cord(conn, cid)
            val = dec['value']
        except Exception:
            val = None
        # knot info
        c2 = conn.cursor()
        c2.execute("SELECT TYPE_CODE, DIRECTION, COUNT(*) FROM knot WHERE CORD_ID=? GROUP BY TYPE_CODE, DIRECTION ORDER BY 3 DESC LIMIT 3", (cid,))
        knots = c2.fetchall()
        kstr = '/'.join(f"{k[0]}{k[1]}x{k[2]}" for k in knots) if knots else '-'
        color = f"{col1}" + (f"+{col2}" if col2 else "")
        result.append({'ordinal': ordinal, 'level': level, 'color': color, 'value': val, 'knots': kstr})
    conn.close()
    return result

def main():
    # Top 15 from language_positive.csv
    cands = []
    with open(os.path.join(BASE, 'language-hunt/language_positive.csv')) as f:
        for i, row in enumerate(csv.DictReader(f)):
            if i >= 15:
                break
            cands.append(row)

    out = []
    for cand in cands:
        kid = cand['khipu_id']
        out.append(f"\n{'='*70}")
        out.append(f"KHIPU {kid} | n={cand['n_cords']} cords, {cand['n_colors']} colors, L{cand['max_level']}")
        out.append(f"  entropy={cand['entropy']} uniq2={cand['uniq2']} hapax={cand['hapax']} zero%={cand['zero_pct']}")
        out.append(f"  why_unclassified: {cand['why_unclassified']}")
        out.append(f"  provenance: {cand['provenance']} | region: {cand['region']}")
        out.append(f"{'='*70}")
        cords = get_cords(int(kid))
        # Show first 40 cords
        out.append(f"  {'ord':>4} {'lvl':>3} {'color':>12} {'value':>7}  knots")
        for co in cords[:40]:
            out.append(f"  {co['ordinal']:>4} {co['level']:>3} {co['color']:>12} {str(co['value']):>7}  {co['knots']}")
        if len(cords) > 40:
            out.append(f"  ... ({len(cords)-40} more cords)")
        # Value summary
        vals = [co['value'] for co in cords if co['value'] is not None]
        if vals:
            out.append(f"  Value range: {min(vals)}-{max(vals)}, nonzero: {sum(1 for v in vals if v>0)}/{len(vals)}")

    report = '\n'.join(out)
    with open(os.path.join(BASE, 'language-hunt/candidate_sequences.txt'), 'w') as f:
        f.write(report)
    print(report[:6000])

if __name__ == '__main__':
    main()
