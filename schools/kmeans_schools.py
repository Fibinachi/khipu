"""K-means clustering of khipu into schools. Pure Python, fast."""
import json, math, random
from collections import Counter

with open('/home/hatch/workspace/quipu-analysis/schools/khipu_features.json') as f:
    feats = json.load(f)

ALL_COLORS = ['W','B','AB','MB','LB','KB','FB','DB','BB','YB','BY','BL','BR','BG','BS',
              'G','GY','GR','GG','G0','SR','RL','RB','HB','CB','SY','LK','PR','RG','LG','0G','?']
ALL_KNOTS = ['S','L','E','TF','LL','SP','?']
ALL_TWIST = ['S','U','Z','?']

kids = sorted(feats.keys())

def vec(kid):
    f = feats[kid]
    v = []
    pal = f['palette']
    v += [pal.get(c, 0) for c in ALL_COLORS]
    kn = f['knots']
    v += [kn.get(t, 0) for t in ALL_KNOTS]
    tw = f['twist']
    v += [tw.get(d, 0) for d in ALL_TWIST]
    v += [min(f['n_cords'] / 500.0, 2.0), f['max_level'] / 6.0,
          f['white_frac'], f['self_rate'], min(f['n_ord'] / 500.0, 2.0)]
    return v

V = [vec(k) for k in kids]
D = len(V[0])
K = 12

random.seed(42)
# k-means++ init
centroids = [V[random.randrange(len(V))]]
while len(centroids) < K:
    d2 = []
    for p in V:
        d2.append(min(sum((a - b) ** 2 for a, b in zip(p, c)) for c in centroids))
    tot = sum(d2)
    r = random.random() * tot
    for i, w in enumerate(d2):
        r -= w
        if r <= 0:
            centroids.append(V[i]); break

def nearest(p):
    best, bi = 1e18, 0
    for i, c in enumerate(centroids):
        d = sum((a - b) ** 2 for a, b in zip(p, c))
        if d < best: best, bi = d, i
    return bi

assign = [0] * len(V)
for it in range(60):
    changed = 0
    for i, p in enumerate(V):
        a = nearest(p)
        if a != assign[i]: changed += 1; assign[i] = a
    # recompute centroids
    sums = [[0.0] * D for _ in range(K)]
    counts = [0] * K
    for i, p in enumerate(V):
        a = assign[i]; counts[a] += 1
        for d in range(D): sums[a][d] += p[d]
    for k in range(K):
        if counts[k]: centroids[k] = [s / counts[k] for s in sums[k]]
    print(f"  iter {it}: changed={changed}", flush=True)
    if changed == 0: break

clusters = {}
for i, k in enumerate(kids):
    clusters.setdefault(f"SCH{assign[i]+1:02d}", []).append(k)

# summarize sorted by size
out = {}
for name in sorted(clusters, key=lambda n: -len(clusters[n])):
    cl = clusters[name]
    n = len(cl)
    dom_color = Counter(); regions = Counter(); self_rates = []; sizes = []
    for k in cl:
        f = feats[k]
        if f['palette']: dom_color[max(f['palette'], key=f['palette'].get)] += 1
        regions[f['region'] or f['provenance'] or 'unknown'] += 1
        self_rates.append(f['self_rate']); sizes.append(f['n_cords'])
    out[name] = sorted(cl)
    print(f"{name}: n={n} palette={dom_color.most_common(3)} "
          f"region={regions.most_common(3)} "
          f"self_med={sorted(self_rates)[n//2]:.2f} size_med={sorted(sizes)[n//2]}")

with open('/home/hatch/workspace/quipu-analysis/schools/school_clusters.json', 'w') as f:
    json.dump(out, f, indent=1)
print("Wrote school_clusters.json")
