"""Unsupervised clustering of 593 non-funerary khipu by structural document likeness.

Features per quipu: structure (cord counts, depth, subsidiary rate), color
(palette, compound %, red-family %, color-run regularity), knots (type mix),
values (log-median, log-max, zero %, small %, uniqueness, decode rate).

No forcing into census/warehouse buckets. Report what emerges.
"""
import sqlite3, sys, csv, math
import numpy as np
from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.cluster.vq import kmeans2

sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from decoder import decode_cord

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
RED_FAM = ('RL', 'RM', 'RD', 'RS')

def compound_str(c1, op, c2):
    return f"{c1 or ''}{op or ''}{c2 or ''}"

def color_regularity(colors):
    """Best fixed-size same-color run detection. Returns (group_size, consistency)."""
    if len(colors) < 6:
        return (0, 0.0)
    best = (0, 0.0)
    for gs in range(2, 13):
        matches = 0; total = 0
        for i in range(0, len(colors) - gs + 1, gs):
            group = colors[i:i+gs]
            if len(group) == gs and group[0] and len(set(group)) == 1:
                matches += 1
            total += 1
        if total:
            cons = matches / total
            if cons > best[1] and cons > 0.5:
                best = (gs, cons)
    return best

def extract(conn, kid):
    c = conn.cursor()
    f = {'khipu_id': kid}
    c.execute('SELECT CORD_LEVEL, COUNT(*) FROM cord WHERE KHIPU_ID=? GROUP BY CORD_LEVEL', (kid,))
    levels = {r[0]: r[1] for r in c.fetchall()}
    f['n_cords'] = sum(v for k, v in levels.items() if k and k > 0)
    f['n_top'] = levels.get(1, 0)
    f['max_level'] = max([k for k in levels if k and k > 0], default=0)
    f['n_subsidiary'] = sum(v for k, v in levels.items() if k and k > 1)

    # Subsidiary parent rate: distinct parents / n_top
    c.execute('''SELECT COUNT(DISTINCT PENDANT_FROM) FROM cord WHERE KHIPU_ID=? AND CORD_LEVEL>1 AND PENDANT_FROM IS NOT NULL''', (kid,))
    np_ = c.fetchone()[0] or 0
    f['sub_parent_rate'] = np_ / f['n_top'] if f['n_top'] else 0.0

    # Colors on top cords
    c.execute('''SELECT cc.COLOR_CD_1, cc.OPERATOR_1, cc.COLOR_CD_2
                 FROM cord co LEFT JOIN ascher_cord_color cc ON co.CORD_ID=cc.CORD_ID
                 WHERE co.KHIPU_ID=? AND co.CORD_LEVEL=1
                 ORDER BY co.CORD_ORDINAL''', (kid,))
    rows = c.fetchall()
    comp = [compound_str(*r) for r in rows]
    nonempty = [x for x in comp if x]
    f['color_fill'] = len(nonempty) / len(comp) if comp else 0.0
    f['n_colors'] = len(set(nonempty))
    f['compound_pct'] = sum(1 for x in nonempty if ':' in x or '-' in x) / len(nonempty) if nonempty else 0.0
    def hasfam(x, fam):
        parts = x.replace(':', ' ').replace('-', ' ').split()
        return any(p in fam for p in parts)
    f['red_pct'] = sum(1 for x in nonempty if hasfam(x, RED_FAM)) / len(nonempty) if nonempty else 0.0
    f['white_pct'] = sum(1 for x in nonempty if 'W' in x.replace(':',' ').replace('-',' ').split()) / len(nonempty) if nonempty else 0.0
    gs, cons = color_regularity(comp)
    f['color_group_size'] = gs
    f['color_group_cons'] = cons

    # Knot type mix (all cords)
    c.execute('''SELECT k.TYPE_CODE, COUNT(*) FROM knot k
                 JOIN cord co ON k.CORD_ID=co.CORD_ID
                 WHERE co.KHIPU_ID=? GROUP BY k.TYPE_CODE''', (kid,))
    kt = Counter({r[0]: r[1] for r in c.fetchall()})
    tot = sum(kt.values()) or 1
    f['s_pct'] = kt.get('S', 0) / tot
    f['l_pct'] = (kt.get('L', 0) + kt.get('LL', 0) + kt.get('BL', 0) + kt.get('SP', 0)) / tot
    f['e_pct'] = (kt.get('E', 0) + kt.get('EE', 0)) / tot
    f['n_knots'] = tot
    f['knots_per_cord'] = tot / f['n_cords'] if f['n_cords'] else 0.0

    # Decoded values on top cords (cap 300)
    c.execute('SELECT CORD_ID FROM cord WHERE KHIPU_ID=? AND CORD_LEVEL=1 ORDER BY CORD_ORDINAL LIMIT 300', (kid,))
    cords = [r[0] for r in c.fetchall()]
    vals, high, und = [], 0, 0
    for cid in cords:
        r = decode_cord(conn, cid)
        if r['value'] is None: und += 1
        else:
            vals.append(r['value'])
            if r['confidence'] == 'high': high += 1
    f['decode_rate'] = len(vals) / len(cords) if cords else 0.0
    if vals:
        vs = sorted(vals)
        f['val_median'] = vs[len(vs)//2]
        f['val_max'] = vs[-1]
        f['zero_pct'] = vs.count(0) / len(vs)
        f['small_pct'] = sum(1 for v in vs if v < 20) / len(vs)
        f['unique_pct'] = len(set(vs)) / len(vs)
    else:
        f['val_median'] = f['val_max'] = None
        f['zero_pct'] = f['small_pct'] = f['unique_pct'] = 0.0

    c.execute('SELECT PROVENANCE, REGION FROM khipu_main WHERE KHIPU_ID=?', (kid,))
    r = c.fetchone()
    f['provenance'] = r[0] if r else None
    f['region'] = r[1] if r else None
    return f

FEATS = ['n_cords', 'n_top', 'max_level', 'n_subsidiary', 'sub_parent_rate',
         'color_fill', 'n_colors', 'compound_pct', 'red_pct', 'white_pct',
         'color_group_size', 'color_group_cons',
         's_pct', 'l_pct', 'e_pct', 'n_knots', 'knots_per_cord',
         'decode_rate', 'val_median', 'val_max', 'zero_pct', 'small_pct', 'unique_pct']

def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''SELECT KHIPU_ID FROM khipu_main WHERE NOT (
        COALESCE(PROVENANCE,'') LIKE '%Leymebamba%' OR COALESCE(PROVENANCE,'') LIKE '%Condores%'
        OR COALESCE(PROVENANCE,'') LIKE '%Cóndores%' OR COALESCE(NOTES,'') LIKE '%funerary%'
        OR COALESCE(NOTES,'') LIKE '%mummy%' OR COALESCE(NOTES,'') LIKE '%burial%'
    )''')
    ids = [r[0] for r in c.fetchall()]
    print(f'{len(ids)} non-funerary khipu', file=sys.stderr)

    rows = []
    for i, kid in enumerate(ids):
        try:
            rows.append(extract(conn, kid))
        except Exception as e:
            print(f'ERR {kid}: {e}', file=sys.stderr)
        if (i+1) % 60 == 0:
            print(f'  {i+1}/{len(ids)}', file=sys.stderr)

    import pickle
    with open('/tmp/cluster_feats.pkl', 'wb') as fh:
        pickle.dump(rows, fh)
    print(f'extracted {len(rows)} feature rows -> /tmp/cluster_feats.pkl', file=sys.stderr)

if __name__ == '__main__':
    main()
