"""Validate the split+classify pipeline on known-type khipu.
If a census khipu splits into segments that classify as census, the method works."""
import sqlite3, json, sys
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis/filing-cabinets')
from split_cabinets import load_cord_features, find_boundaries
from classify_segments import seg_features, classify
from collections import Counter

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'

def get_ids(cluster_name, n=10):
    ids = []
    with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
        for line in f:
            if line.startswith('#') or line.startswith('KHIPU'):
                continue
            p = line.strip().split(',')
            if len(p) >= 3 and p[2] == cluster_name:
                ids.append(p[0])
    return ids[:n]

conn = sqlite3.connect(DB)
pack = json.load(open('/home/hatch/workspace/quipu-analysis/filing-cabinets/centroids.json'))
centroids, stats, keys = pack['centroids'], pack['stats'], pack['feat_keys']
TYPE_NAMES = {1: 'census', 2: 'warehouse', 3: 'bulk_tally', 5: 'south_funerary', 6: 'unknown_office', 0: 'unclassified'}

for cluster, tcode in [('census_format_paired', 1), ('deep_hierarchical_grouped', 2), ('large_value_flat', 3)]:
    ids = get_ids(cluster, 12)
    feats = load_cord_features(conn, ids)
    results = []
    for kid in ids:
        seq = feats.get(kid, [])
        if not seq:
            continue
        depth_by_ord = {}
        for s in seq:
            o = s['ordinal']
            depth_by_ord[o] = max(depth_by_ord.get(o, 1), s['level'] or 1)
        l1 = [s for s in seq if s['level'] == 1]
        bounds = find_boundaries(l1, depth_by_ord)
        cuts = [0] + [b[0] for b in bounds] + [len(l1)]
        for si in range(len(cuts) - 1):
            ord0 = l1[cuts[si]]['ordinal']
            ord1 = l1[cuts[si+1]-1]['ordinal']
            fv = seg_features(conn, kid, ord0, ord1)
            pred, conf = classify(fv, centroids, stats, keys)
            results.append((pred == tcode, conf))
    n = len(results)
    correct = sum(1 for c, _ in results if c)
    hi = sum(1 for c, cf in results if c and cf >= 0.2)
    print(f"{cluster}: {n} segments from {len(ids)} khipu; "
          f"correct type: {correct}/{n} ({100*correct/max(n,1):.0f}%), "
          f"correct+conf>=0.2: {hi}/{n}", flush=True)
