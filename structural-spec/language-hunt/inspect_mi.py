"""Detailed inspection of high-MI-ratio candidates: 1000183, 1000331, 1000083, 1000176, 1000382."""
import os, sqlite3, sys
sys.path.insert(0, os.path.expanduser('~/workspace/quipu-analysis'))
from decoder import decode_cord

BASE = os.path.expanduser('~/workspace/quipu-analysis')
DB = os.path.join(BASE, 'okr-khipu.db')

def get_cords(khipu_id, limit=60):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        SELECT c.CORD_ID, c.CORD_ORDINAL, c.CORD_LEVEL, cc.COLOR_CD_1, cc.COLOR_CD_2
        FROM cord c
        LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
        WHERE c.KHIPU_ID = ?
        ORDER BY c.CORD_ORDINAL LIMIT ?
    """, (khipu_id, limit))
    rows = c.fetchall()
    result = []
    for cid, ordinal, level, col1, col2 in rows:
        try:
            dec = decode_cord(conn, cid)
            val = dec['value']
        except Exception:
            val = None
        c2 = conn.cursor()
        c2.execute("SELECT TYPE_CODE, DIRECTION, COUNT(*) FROM knot WHERE CORD_ID=? GROUP BY TYPE_CODE, DIRECTION ORDER BY 3 DESC LIMIT 4", (cid,))
        knots = c2.fetchall()
        kstr = '/'.join(f"{k[0]}{k[1]}x{k[2]}" for k in knots) if knots else '(no knots)'
        color = f"{col1}" + (f"+{col2}" if col2 else "")
        result.append({'ordinal': ordinal, 'level': level, 'color': color, 'value': val, 'knots': kstr})
    # provenance
    c3 = conn.cursor()
    c3.execute("SELECT PROVENANCE, REGION FROM khipu_main WHERE KHIPU_ID=?", (khipu_id,))
    prov = c3.fetchone()
    conn.close()
    return result, prov

def main():
    for kid in [1000183, 1000331, 1000083, 1000176, 1000382]:
        cords, prov = get_cords(kid)
        print(f"\n{'='*75}")
        print(f"KHIPU {kid} | provenance: {prov}")
        print(f"{'='*75}")
        print(f"  {'ord':>4} {'lvl':>3} {'color':>14} {'value':>8}  knots")
        for co in cords:
            print(f"  {co['ordinal']:>4} {co['level']:>3} {co['color']:>14} {str(co['value']):>8}  {co['knots']}")
        vals = [co['value'] for co in cords if co['value'] is not None]
        if vals:
            nz = sum(1 for v in vals if v and v > 0)
            print(f"  [showing {len(cords)} cords; nonzero values: {nz}/{len(vals)}]")

if __name__ == '__main__':
    main()
