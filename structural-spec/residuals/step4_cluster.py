"""Step 4: cluster residuals only. Do they form their own groups?"""
import pickle, math
from collections import Counter
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster

OUT = '/home/hatch/workspace/quipu-analysis/residuals/'
FEATS = ['n_cords','n_top','max_level','n_subsidiary','sub_parent_rate','color_fill',
         'n_colors','compound_pct','red_pct','white_pct','color_group_size','color_group_cons',
         's_pct','l_pct','e_pct','n_knots','knots_per_cord','decode_rate','val_median',
         'val_max','zero_pct','small_pct','unique_pct']
LOG_FEATS = {'n_cords','n_top','n_subsidiary','n_colors','n_knots','val_median','val_max'}

def main():
    with open(OUT + 'residual_feats.pkl', 'rb') as fh:
        res = pickle.load(fh)
    ids = [r['khipu_id'] for r in res]
    n = len(res)
    X = np.zeros((n, len(FEATS)))
    for i, r in enumerate(res):
        for j, f in enumerate(FEATS):
            v = r.get(f); v = 0.0 if v is None else float(v)
            if f in LOG_FEATS: v = math.log1p(v)
            X[i, j] = v
    mu = X.mean(axis=0); sd = X.std(axis=0); sd[sd == 0] = 1.0
    Z = (X - mu) / sd
    L = linkage(Z, method='ward')

    lines = ['# Residual Sub-clustering', '',
             f'n={n} unclassified khipu, {len(FEATS)} features, Ward linkage.', '']
    from scipy.spatial.distance import pdist, squareform
    for k in (2, 3, 4, 5, 6):
        lab = fcluster(L, k, criterion='maxclust')
        # silhouette (manual)
        D = squareform(pdist(Z, 'euclidean'))
        labarr = np.array(lab); sils = []
        for i in range(n):
            same = (labarr == labarr[i]); same[i] = False
            a = D[i][same].mean() if same.sum() else 0.0
            b = min((D[i][labarr == l].mean() for l in set(labarr) if l != labarr[i]), default=0.0)
            sils.append((b-a)/max(a,b) if max(a,b) > 0 else 0.0)
        sil = float(np.mean(sils))
        sizes = Counter(lab)
        lines.append(f'## k={k}: silhouette {sil:.3f}, sizes {dict(sorted(sizes.items()))}')
        lines.append('')
        # characterize each sub-cluster at k
        for cl in sorted(sizes):
            members = [ids[i] for i in range(n) if lab[i] == cl]
            sub = [res[i] for i in range(n) if lab[i] == cl]
            med_cords = np.median([r['n_cords'] for r in sub])
            med_colors = np.median([r['n_colors'] for r in sub])
            med_level = np.median([r['max_level'] for r in sub])
            med_zero = np.median([r['zero_pct'] for r in sub])
            med_decode = np.median([r['decode_rate'] for r in sub])
            reasons = Counter()
            for r in sub:
                for x in r['reasons'].split(';'): reasons[x] += 1
            prov = Counter(r['provenance'] for r in sub if r['provenance']).most_common(3)
            lines.append(f'### Sub-cluster {cl} (n={len(members)})')
            lines.append(f'- median cords {med_cords:.0f}, colors {med_colors:.0f}, max level {med_level:.0f}, zero% {med_zero:.2f}, decode {med_decode:.2f}')
            lines.append(f'- reasons: {dict(reasons.most_common(4))}')
            lines.append(f'- top provenance: {prov}')
            lines.append(f'- members: {", ".join(members[:12])}{"..." if len(members)>12 else ""}')
            lines.append('')
    with open(OUT + 'residual_clusters.md', 'w') as f:
        f.write('\n'.join(lines) + '\n')
    # save k=4 labels as canonical
    lab4 = fcluster(L, 4, criterion='maxclust')
    with open(OUT + 'residual_subclusters.pkl', 'wb') as f:
        pickle.dump({ids[i]: int(lab4[i]) for i in range(n)}, f)
    print('wrote residual_clusters.md', flush=True)

if __name__ == '__main__':
    main()
