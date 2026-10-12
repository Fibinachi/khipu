"""Step 2: normalize features, hierarchical + k-means clustering, silhouette scores,
cluster characterization. Loads /tmp/cluster_feats.pkl from step 1."""
import pickle, csv, math
import numpy as np
from collections import Counter, defaultdict
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.cluster.vq import kmeans2
from scipy.spatial.distance import pdist, squareform

LOG_FEATS = {'n_cords', 'n_top', 'n_subsidiary', 'n_colors', 'n_knots', 'val_median', 'val_max'}

FEATS = ['n_cords', 'n_top', 'max_level', 'n_subsidiary', 'sub_parent_rate',
         'color_fill', 'n_colors', 'compound_pct', 'red_pct', 'white_pct',
         'color_group_size', 'color_group_cons',
         's_pct', 'l_pct', 'e_pct', 'n_knots', 'knots_per_cord',
         'decode_rate', 'val_median', 'val_max', 'zero_pct', 'small_pct', 'unique_pct']

def silhouette(X, labels):
    """Mean silhouette score (manual, fine for n=593)."""
    D = squareform(pdist(X, 'euclidean'))
    lab = np.array(labels)
    sils = []
    for i in range(len(X)):
        same = (lab == lab[i])
        same[i] = False
        a = D[i][same].mean() if same.sum() else 0.0
        b = min((D[i][lab == l].mean() for l in set(lab) if l != lab[i]), default=0.0)
        sils.append((b - a) / max(a, b) if max(a, b) > 0 else 0.0)
    return float(np.mean(sils)), sils

def main():
    with open('/tmp/cluster_feats.pkl', 'rb') as fh:
        rows = pickle.load(fh)
    ids = [r['khipu_id'] for r in rows]
    print(f'n={len(rows)}')

    # Build matrix; log-transform skewed, then z-score
    X = np.zeros((len(rows), len(FEATS)))
    for i, r in enumerate(rows):
        for j, f in enumerate(FEATS):
            v = r.get(f)
            v = 0.0 if v is None else float(v)
            if f in LOG_FEATS:
                v = math.log1p(v)
            X[i, j] = v
    mu = X.mean(axis=0); sd = X.std(axis=0); sd[sd == 0] = 1.0
    Z = (X - mu) / sd

    # Hierarchical (Ward)
    L = linkage(Z, method='ward')
    print('\n--- hierarchical (Ward) ---')
    hier = {}
    for k in [2, 3, 4, 5, 6, 8, 10, 12, 15]:
        lab = fcluster(L, k, criterion='maxclust')
        s, _ = silhouette(Z, lab)
        hier[k] = lab
        print(f'k={k:2d}  silhouette={s:.3f}  sizes={sorted(Counter(lab).values(), reverse=True)}')

    # k-means several k
    print('\n--- k-means ---')
    km = {}
    for k in [2, 3, 4, 5, 6, 8, 10, 12, 15]:
        best, best_s = None, -1
        for seed in range(5):
            np.random.seed(seed)
            cent, lab = kmeans2(Z, k, minit='points', iter=50)
            s, _ = silhouette(Z, lab)
            if s > best_s:
                best, best_s = (lab, s), s
        km[k] = best[0]
        print(f'k={k:2d}  silhouette={best_s:.3f}  sizes={sorted(Counter(best[0]).values(), reverse=True)}')

    # Save both at chosen resolution; pick k by elbow of silhouette
    np.save('/tmp/cluster_Z.npy', Z)
    with open('/tmp/cluster_ids.txt', 'w') as fh:
        fh.write('\n'.join(map(str, ids)))
    with open('/tmp/cluster_labels.pkl', 'wb') as fh:
        pickle.dump({'hier': hier, 'kmeans': km, 'feats': FEATS}, fh)
    print('\nsaved labels')

if __name__ == '__main__':
    main()
