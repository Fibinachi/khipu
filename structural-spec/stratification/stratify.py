"""Color-magnitude stratification analysis.

For each khipu: decode cord values, group by color, compute per-color stats.
Then test whether colors occupy distinct magnitude bands (stratification).
"""
import sqlite3, csv, sys, json
import numpy as np
from scipy import stats as spstats
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from decoder import decode_cord

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
OUT = '/home/hatch/workspace/quipu-analysis/stratification'

def load_clusters():
    m = {}
    with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
        for line in f:
            if line.startswith('#') or line.startswith('KHIPU'):
                continue
            p = line.strip().split(',')
            m[int(p[0])] = p[2]
    return m

def main():
    conn = sqlite3.connect(DB)
    clusters = load_clusters()
    khipu_ids = sorted(clusters.keys())
    print(f"{len(khipu_ids)} khipu", flush=True)

    # Preload colors: cord_id -> color_cd_1
    c = conn.cursor()
    c.execute("SELECT CORD_ID, COLOR_CD_1 FROM ascher_cord_color")
    color_of = {r[0]: r[1] for r in c.fetchall()}
    print(f"{len(color_of)} colored cords", flush=True)

    # Preload cord -> khipu
    c.execute("SELECT CORD_ID, KHIPU_ID FROM cord")
    khipu_of = {r[0]: r[1] for r in c.fetchall()}

    color_rows = []   # khipu_id, color, n, median, q25, q75, min, max
    strat_rows = []   # khipu_id, n_colors, score, kw_p, is_stratified, cluster

    for i, kid in enumerate(khipu_ids):
        if i % 100 == 0:
            print(f"  {i}/{len(khipu_ids)}", flush=True)
        c.execute("SELECT CORD_ID FROM cord WHERE KHIPU_ID=?", (kid,))
        cord_ids = [r[0] for r in c.fetchall()]
        by_color = {}
        for cid in cord_ids:
            col = color_of.get(cid)
            if not col:
                continue
            r = decode_cord(conn, cid)
            v = r['value']
            if v is None:
                continue
            by_color.setdefault(col, []).append(v)
        # per-color stats
        qualified = {}  # color -> array (n>=5)
        for col, vals in by_color.items():
            a = np.array(vals, dtype=float)
            color_rows.append([kid, col, len(a),
                               float(np.median(a)),
                               float(np.percentile(a, 25)),
                               float(np.percentile(a, 75)),
                               float(a.min()), float(a.max())])
            if len(a) >= 5:
                qualified[col] = a
        # stratification test
        if len(qualified) >= 3:
            cols = sorted(qualified.keys(), key=lambda c2: np.median(qualified[c2]))
            iqr = {c2: (np.percentile(qualified[c2], 25), np.percentile(qualified[c2], 75))
                   for c2 in cols}
            lo = min(v[0] for v in iqr.values())
            hi = max(v[1] for v in iqr.values())
            total_range = hi - lo
            overlap = 0.0
            for a_, b_ in zip(cols[:-1], cols[1:]):
                o = min(iqr[a_][1], iqr[b_][1]) - max(iqr[a_][0], iqr[b_][0])
                if o > 0:
                    overlap += o
            score = 1.0 - (overlap / total_range) if total_range > 0 else 0.0
            score = max(0.0, min(1.0, score))
            try:
                kw_p = float(spstats.kruskal(*[qualified[c2] for c2 in cols]).pvalue)
            except Exception:
                kw_p = float('nan')
            strat_rows.append([kid, len(cols), round(score, 4), kw_p,
                               1 if score > 0.7 else 0, clusters[kid]])
        else:
            strat_rows.append([kid, len(qualified), float('nan'), float('nan'), 0, clusters[kid]])

    conn.close()
    with open(f'{OUT}/color_magnitudes.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['khipu_id','color','n_cords','median','q25','q75','min','max'])
        w.writerows(color_rows)
    with open(f'{OUT}/stratification_scores.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['khipu_id','n_colors_tested','strat_score','kruskal_p','is_stratified','cluster'])
        w.writerows(strat_rows)
    print(f"done: {len(color_rows)} color rows, {len(strat_rows)} khipu scored", flush=True)

if __name__ == '__main__':
    main()
