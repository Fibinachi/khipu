"""Marker-word test: do values 22/23/32/33/34 keep consistent company?

For each occurrence of a marker value, capture:
  - own color
  - colors of +-3 neighbors
  - doc_cluster, data_cluster, provenance, region
  - tertile position in khipu
Then test companion consistency per marker value.
"""
import pickle, csv, os
from collections import Counter, defaultdict
from math import log

BASE = os.path.expanduser('~/workspace/quipu-analysis')
OUT = os.path.join(BASE, 'marker-words')
os.makedirs(OUT, exist_ok=True)

MARKERS = {22, 23, 32, 33, 34}

# Load decoded cache
with open(os.path.join(BASE, 'templates/cache.pkl'), 'rb') as f:
    cache = pickle.load(f)

# Load cluster metadata
meta = {}
with open(os.path.join(BASE, 'data-match/data_clusters.csv')) as f:
    for r in csv.DictReader(f):
        meta[str(r['khipu_id'])] = r

# ---- 1. Collect all marker occurrences with context ----
occurrences = []  # (khipu_id, ordinal, value, own_color, neighbors, doc, regime, prov, region, tertile)
for kid, cords in cache.items():
    # cords: list of (ordinal, level, color1, color2, value)
    # sort by ordinal for neighbor lookup
    sc = sorted(cords, key=lambda t: t[0])
    n = len(sc)
    colors = [(t[2] or '?').strip() for t in sc]
    for i, t in enumerate(sc):
        ordinal, level, color1, color2, value = t
        if value in MARKERS:
            own = (color1 or '?').strip()
            neigh = []
            for j in range(i-3, i+4):
                if j == i or j < 0 or j >= n:
                    neigh.append(None)
                else:
                    neigh.append(colors[j])
            m = meta.get(str(kid), {})
            doc = m.get('doc_cluster', '') or 'unknown'
            regime = m.get('data_cluster', '') or 'unknown'
            prov = m.get('provenance', '') or ''
            region = m.get('region', '') or ''
            tert = 'begin' if i < n/3 else ('end' if i >= 2*n/3 else 'mid')
            occurrences.append({
                'khipu_id': kid, 'ordinal': ordinal, 'value': value,
                'own_color': own, 'neighbors': neigh,
                'doc_cluster': doc, 'data_cluster': regime,
                'provenance': prov, 'region': region, 'tertile': tert,
                'level': level,
            })

print(f"Total marker occurrences: {len(occurrences)}")
print(f"Khipu with markers: {len(set(o['khipu_id'] for o in occurrences))}")

# Write marker_contexts.csv
with open(os.path.join(OUT, 'marker_contexts.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['khipu_id','ordinal','value','own_color','level',
                'n-3','n-2','n-1','n+1','n+2','n+3',
                'doc_cluster','data_cluster','provenance','region','tertile'])
    for o in occurrences:
        w.writerow([o['khipu_id'], o['ordinal'], o['value'], o['own_color'], o['level'],
                    *[x or '' for x in o['neighbors']],
                    o['doc_cluster'], o['data_cluster'], o['provenance'],
                    o['region'], o['tertile']])

# ---- 2. Background rates: overall color distribution (for chi-square expectation) ----
bg_color = Counter()
bg_total = 0
for kid, cords in cache.items():
    for t in cords:
        bg_color[(t[2] or '?').strip()] += 1
        bg_total += 1

# ---- 3. Companion analysis per marker value ----
def chi_square(observed, expected):
    chi2 = 0.0
    for k, obs in observed.items():
        exp = expected.get(k, 0)
        if exp > 0:
            chi2 += (obs - exp) ** 2 / exp
    dof = len([k for k in observed if expected.get(k, 0) > 0]) - 1
    return chi2, dof

rows = []
for mv in sorted(MARKERS):
    occ = [o for o in occurrences if o['value'] == mv]
    n_occ = len(occ)
    n_khipu = len(set(o['khipu_id'] for o in occ))
    if n_occ == 0:
        rows.append({'value': mv, 'n_occ': 0, 'n_khipu': 0})
        continue

    own_dist = Counter(o['own_color'] for o in occ)
    # neighbors (all 6 positions pooled, excluding None)
    neigh_all = Counter()
    for o in occ:
        for x in o['neighbors']:
            if x:
                neigh_all[x] += 1
    # immediate neighbors only (n-1, n+1)
    neigh_imm = Counter()
    for o in occ:
        for x in (o['neighbors'][2], o['neighbors'][3]):
            if x:
                neigh_imm[x] += 1
    # next cord (n+1) — "what follows the marker"
    next_dist = Counter(o['neighbors'][3] for o in occ if o['neighbors'][3])
    prev_dist = Counter(o['neighbors'][2] for o in occ if o['neighbors'][2])
    doc_dist = Counter(o['doc_cluster'] for o in occ)
    reg_dist = Counter(o['data_cluster'] for o in occ)
    region_dist = Counter(o['region'] or '(blank)' for o in occ)
    tert_dist = Counter(o['tertile'] for o in occ)

    # top own color concentration
    top_own, top_own_n = own_dist.most_common(1)[0]
    own_conc = top_own_n / n_occ
    # top next-color concentration
    top_next, top_next_n = next_dist.most_common(1)[0] if next_dist else ('-', 0)
    next_conc = top_next_n / n_occ if n_occ else 0

    # chi-square: own-color vs background
    exp_own = {c: n_occ * bg_color[c] / bg_total for c in own_dist}
    chi2_own, dof_own = chi_square(own_dist, exp_own)

    # chi-square: neighbor colors vs background
    n_neigh = sum(neigh_all.values())
    exp_neigh = {c: n_neigh * bg_color[c] / bg_total for c in neigh_all}
    chi2_neigh, dof_neigh = chi_square(neigh_all, exp_neigh)

    # positional concentration: is it always at row starts? use tertile
    tert_conc = max(tert_dist.values()) / n_occ

    rows.append({
        'value': mv, 'n_occ': n_occ, 'n_khipu': n_khipu,
        'own_top': top_own, 'own_top_n': top_own_n, 'own_conc': round(own_conc, 3),
        'own_dist': dict(own_dist.most_common(8)),
        'next_top': top_next, 'next_conc': round(next_conc, 3),
        'next_dist': dict(next_dist.most_common(8)),
        'prev_dist': dict(prev_dist.most_common(8)),
        'neigh_top5': dict(neigh_all.most_common(5)),
        'doc_dist': dict(doc_dist),
        'regime_dist': dict(reg_dist),
        'region_top5': dict(region_dist.most_common(5)),
        'n_regions': len(region_dist),
        'tertile_dist': dict(tert_dist),
        'tert_conc': round(tert_conc, 3),
        'chi2_own': round(chi2_own, 1), 'dof_own': dof_own,
        'chi2_neigh': round(chi2_neigh, 1), 'dof_neigh': dof_neigh,
    })
    print(f"\n=== Marker {mv}: {n_occ} occ in {n_khipu} khipu ===")
    print(f"  own color: top={top_own} ({top_own_n}/{n_occ}={own_conc:.2f}) dist={dict(own_dist.most_common(6))}")
    print(f"  next: top={top_next} conc={next_conc:.2f} dist={dict(next_dist.most_common(6))}")
    print(f"  prev: dist={dict(prev_dist.most_common(6))}")
    print(f"  doc: {dict(doc_dist)}")
    print(f"  regime: {dict(reg_dist)}")
    print(f"  regions ({len(region_dist)}): {dict(region_dist.most_common(6))}")
    print(f"  tertile: {dict(tert_dist)} conc={tert_conc:.2f}")
    print(f"  chi2 own vs bg: {chi2_own:.1f} (dof {dof_own})")

# Write companion_analysis.csv (flattened)
with open(os.path.join(OUT, 'companion_analysis.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['value','n_occ','n_khipu','own_top','own_top_n','own_conc',
                'own_dist','next_top','next_conc','next_dist','prev_dist',
                'neigh_top5','doc_dist','regime_dist','region_top5','n_regions',
                'tertile_dist','tert_conc','chi2_own','dof_own','chi2_neigh','dof_neigh'])
    for r in rows:
        w.writerow([r.get('value'), r.get('n_occ'), r.get('n_khipu'),
                    r.get('own_top',''), r.get('own_top_n',''), r.get('own_conc',''),
                    r.get('own_dist',''), r.get('next_top',''), r.get('next_conc',''),
                    r.get('next_dist',''), r.get('prev_dist',''), r.get('neigh_top5',''),
                    r.get('doc_dist',''), r.get('regime_dist',''), r.get('region_top5',''),
                    r.get('n_regions',''), r.get('tertile_dist',''), r.get('tert_conc',''),
                    r.get('chi2_own',''), r.get('dof_own',''),
                    r.get('chi2_neigh',''), r.get('dof_neigh','')])

# ---- 4. Khipu-level clustering: do some khipu use markers heavily, others never? ----
khipu_marker_counts = Counter(o['khipu_id'] for o in occurrences)
heavy = khipu_marker_counts.most_common(15)
print("\nTop 15 khipu by marker count:")
for kid, n in heavy:
    m = meta.get(str(kid), {})
    print(f"  {kid}: {n} markers, doc={m.get('doc_cluster')}, regime={m.get('data_cluster')}, region={m.get('region')}")
with open(os.path.join(OUT, 'heavy_users.txt'), 'w') as f:
    for kid, n in khipu_marker_counts.most_common(50):
        m = meta.get(str(kid), {})
        f.write(f"{kid}\t{n}\t{m.get('doc_cluster')}\t{m.get('data_cluster')}\t{m.get('region')}\t{m.get('provenance')}\n")

print("\nDone. Outputs in", OUT)
