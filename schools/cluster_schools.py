"""Cluster khipu into schools using habit features. No semantics, just attribution."""
import json, math
from collections import Counter, defaultdict

with open('/home/hatch/workspace/quipu-analysis/schools/khipu_features.json') as f:
    feats = json.load(f)

# Build fixed feature vocabulary
ALL_COLORS = ['W','B','AB','MB','LB','KB','FB','DB','BB','YB','BY','BL','BR','BG','BS',
              'G','GY','GR','GG','G0','SR','RL','RB','HB','CB','SY','LK','PR','RG','LG','0G','?']
ALL_KNOTS = ['S','L','E','TF','LL','SP','?']
ALL_TWIST = ['S','U','Z','?']

kids = sorted(feats.keys())

def vec(kid):
    f = feats[kid]
    v = []
    # palette fractions over fixed vocab
    pal = f['palette']
    v += [pal.get(c, 0) for c in ALL_COLORS]
    # knot fractions
    kn = f['knots']
    v += [kn.get(t, 0) for t in ALL_KNOTS]
    # twist fractions
    tw = f['twist']
    v += [tw.get(d, 0) for d in ALL_TWIST]
    # structural scalars (standardized roughly)
    v += [
        min(f['n_cords'] / 500.0, 2.0),          # size
        f['max_level'] / 6.0,                     # depth
        f['white_frac'],                          # white share
        f['self_rate'],                           # log-vs-tabular signal
        min(f['n_ord'] / 500.0, 2.0),
    ]
    return v

V = {k: vec(k) for k in kids}

def dist(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(V[a], V[b])))

# Agglomerative clustering with average linkage, target ~12 clusters
clusters = [{k} for k in kids]
def avg_dist(c1, c2):
    tot, n = 0.0, 0
    for a in c1:
        for b in c2:
            tot += dist(a, b); n += 1
    return tot / n if n else 0

while len(clusters) > 12:
    best, bi, bj = 1e18, -1, -1
    for i in range(len(clusters)):
        for j in range(i + 1, len(clusters)):
            d = avg_dist(clusters[i], clusters[j])
            if d < best:
                best, bi, bj = d, i, j
    clusters[bi] = clusters[bi] | clusters[bj]
    del clusters[bj]
    if len(clusters) % 10 == 0:
        print(f"  {len(clusters)} clusters")

print(f"\nFinal: {len(clusters)} clusters")
out = {}
for i, cl in enumerate(sorted(clusters, key=len, reverse=True)):
    name = f"SCH{i+1:02d}"
    out[name] = sorted(cl)
    # summarize
    n = len(cl)
    dom_color = Counter()
    regions = Counter()
    self_rates = []
    sizes = []
    for k in cl:
        f = feats[k]
        if f['palette']:
            dom_color[max(f['palette'], key=f['palette'].get)] += 1
        reg = f['region'] or f['provenance'] or 'unknown'
        regions[reg] += 1
        self_rates.append(f['self_rate'])
        sizes.append(f['n_cords'])
    print(f"{name}: n={n} dom_palette={dom_color.most_common(3)} "
          f"top_region={regions.most_common(3)} "
          f"self_rate_med={sorted(self_rates)[n//2]:.2f} size_med={sorted(sizes)[n//2]}")

with open('/home/hatch/workspace/quipu-analysis/schools/school_clusters.json', 'w') as f:
    json.dump(out, f, indent=1)
print("Wrote school_clusters.json")
