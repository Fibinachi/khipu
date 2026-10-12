"""Compute type centroids from known-type khipu for segment classification."""
import sqlite3, csv, json, math, statistics
from collections import Counter, defaultdict

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
OUT = '/home/hatch/workspace/quipu-analysis/filing-cabinets'

# type_code -> (cluster_name or explicit id list, label)
SOUTH_FUNERARY = ['1000565','1000007','1000648','1000293','1000280','1000329',
                  '1000279','1000323','1000376','1000495','1000344','1000012',
                  '1000238','1000010','1000292']
UNKNOWN_OFFICE = ['1000029','1000034','1000345','1000361','1000368']
TYPE_DEFS = {
    0x01: ('census_format_paired', 'census'),
    0x02: ('deep_hierarchical_grouped', 'warehouse'),
    0x03: ('large_value_flat', 'bulk_tally'),
    0x05: (SOUTH_FUNERARY, 'south_funerary'),
    0x06: (UNKNOWN_OFFICE, 'unknown_office'),
}
GRAMMATICAL = {'W', 'AB', 'MB', 'KB'}

def cluster_ids(name):
    ids = []
    with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
        for line in f:
            if line.startswith('#') or line.startswith('KHIPU'):
                continue
            p = line.strip().split(',')
            if len(p) >= 3 and p[2] == name:
                ids.append(p[0])
    return ids

def khipu_features(conn, khipu_id):
    """Feature vector for a whole khipu (or segment cord set)."""
    c = conn.cursor()
    c.execute("""
        SELECT c.CORD_ID, c.CORD_LEVEL, cc.COLOR_CD_1, cc.COLOR_CD_2
        FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
        WHERE c.KHIPU_ID = ?
    """, (khipu_id,))
    rows = c.fetchall()
    if not rows:
        return None
    cids = [r[0] for r in rows]
    ph = ','.join('?' * len(cids))
    c.execute(f"SELECT CORD_ID, DIRECTION, COUNT(*) FROM knot WHERE CORD_ID IN ({ph}) GROUP BY CORD_ID, DIRECTION", cids)
    tdir = defaultdict(Counter)
    for cid, d, n in c.fetchall():
        tdir[cid][d or '?'] += n
    c.execute(f"SELECT CORD_ID, COUNT(*) FROM knot WHERE CORD_ID IN ({ph}) GROUP BY CORD_ID", cids)
    nk = dict(c.fetchall())
    n = len(rows)
    levels = [r[1] or 0 for r in rows]
    colors = [r[2] for r in rows if r[2]]
    ncolors = len(set(colors))
    white = sum(1 for col in colors if col == 'W') / max(len(colors), 1)
    comp = sum(1 for r in rows if r[3]) / n
    # dominant twist per cord
    twists = []
    for cid in cids:
        d = tdir.get(cid, Counter())
        twists.append(d.most_common(1)[0][0] if d else '?')
    tc = Counter(twists)
    tot = max(sum(tc.values()), 1)
    zpct = tc.get('Z', 0) / tot; spct = tc.get('S', 0) / tot; upct = tc.get('U', 0) / tot
    sub_rate = sum(1 for l in levels if l >= 2) / n
    mags = sorted(nk.get(cid, 0) for cid in cids)
    medmag = mags[len(mags)//2]
    return {
        'n_cords': n, 'max_level': max(levels), 'n_colors': ncolors,
        'white_pct': white, 'compound_pct': comp,
        'z_pct': zpct, 's_pct': spct, 'u_pct': upct,
        'subsidiary_rate': sub_rate, 'med_knotcount': medmag,
    }

FEAT_KEYS = ['max_level','n_colors','white_pct','compound_pct',
             'z_pct','s_pct','u_pct','subsidiary_rate','med_knotcount']
# NOTE: n_cords excluded — segments are fragments, so absolute size is not
# comparable to whole-khipu centroids. All features above are scale-invariant
# (rates, proportions, per-cord medians).

def main():
    conn = sqlite3.connect(DB)
    centroids = {}
    for tcode, (src, label) in TYPE_DEFS.items():
        ids = src if isinstance(src, list) else cluster_ids(src)
        # cap census at 60 random-ish (even stride) for speed
        if len(ids) > 60:
            ids = ids[::len(ids)//60][:60]
        vecs = []
        for kid in ids:
            fv = khipu_features(conn, kid)
            if fv:
                vecs.append(fv)
        cent = {k: statistics.median(v[k] for v in vecs) for k in FEAT_KEYS}
        centroids[tcode] = {'label': label, 'n': len(vecs), 'centroid': cent}
        print(f"{label}: n={len(vecs)}", flush=True)
    # corpus stats for z-scoring: use all typed khipu
    allv = defaultdict(list)
    for tcode, (src, label) in TYPE_DEFS.items():
        ids = src if isinstance(src, list) else cluster_ids(src)
        if len(ids) > 60:
            ids = ids[::len(ids)//60][:60]
        for kid in ids:
            fv = khipu_features(conn, kid)
            if fv:
                for k in FEAT_KEYS:
                    allv[k].append(fv[k])
    stats = {k: (statistics.mean(v), statistics.pstdev(v) or 1) for k, v in allv.items()}
    with open(f'{OUT}/centroids.json', 'w') as f:
        json.dump({'centroids': {str(k): v for k, v in centroids.items()},
                   'stats': stats, 'feat_keys': FEAT_KEYS}, f)
    print("wrote centroids.json", flush=True)

if __name__ == '__main__':
    main()
