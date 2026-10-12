"""Step 3: characterize clusters. For chosen resolutions, report per-cluster:
median feature values, geographic spread, overlap with old labels, representatives."""
import pickle, csv
import numpy as np
from collections import Counter, defaultdict

FEATS = ['n_cords', 'n_top', 'max_level', 'n_subsidiary', 'sub_parent_rate',
         'color_fill', 'n_colors', 'compound_pct', 'red_pct', 'white_pct',
         'color_group_size', 'color_group_cons',
         's_pct', 'l_pct', 'e_pct', 'n_knots', 'knots_per_cord',
         'decode_rate', 'val_median', 'val_max', 'zero_pct', 'small_pct', 'unique_pct']

def main():
    with open('/tmp/cluster_feats.pkl', 'rb') as fh:
        rows = pickle.load(fh)
    by_id = {r['khipu_id']: r for r in rows}
    with open('/tmp/cluster_labels.pkl', 'rb') as fh:
        L = pickle.load(fh)

    # old labels
    old = {}
    with open('/home/hatch/workspace/quipu-analysis/reclassification-2026-10-10.csv') as fh:
        for row in csv.DictReader(fh):
            old[int(row['KHIPU_ID'])] = row['DOCUMENT_TYPE']

    ids = [r['khipu_id'] for r in rows]

    def describe(name, lab):
        print(f'\n===== {name} =====')
        labs = sorted(set(lab))
        for l in labs:
            members = [ids[i] for i in range(len(ids)) if lab[i] == l]
            print(f'\n-- cluster {l}: n={len(members)}')
            print('   old labels:', dict(Counter(old.get(m, '?') for m in members)))
            regs = Counter((by_id[m]['region'] or '?') for m in members)
            print('   regions:', dict(regs.most_common(6)))
            provs = Counter((by_id[m]['provenance'] or '?')[:40] for m in members)
            print('   top provenance:', dict(provs.most_common(4)))
            med = {}
            for f in FEATS:
                vals = [by_id[m][f] for m in members if by_id[m][f] is not None]
                med[f] = float(np.median(vals)) if vals else None
            show = {f: (round(med[f], 3) if med[f] is not None else None)
                    for f in ['n_top', 'max_level', 'n_subsidiary', 'sub_parent_rate',
                              'n_colors', 'compound_pct', 'red_pct',
                              'color_group_size', 'color_group_cons',
                              'decode_rate', 'val_median', 'val_max', 'zero_pct', 'small_pct']}
            print('   medians:', show)
            # representatives: 3 closest to centroid in z-space
            Z = np.load('/tmp/cluster_Z.npy')
            idx = [i for i in range(len(ids)) if lab[i] == l]
            cent = Z[idx].mean(axis=0)
            dists = [((Z[i] - cent) ** 2).sum() for i in idx]
            reps = sorted(zip(dists, idx))[:3]
            print('   representatives:', [(ids[i], round(float(d), 2)) for d, i in reps])

    describe('hierarchical k=4', L['hier'][4])
    describe('hierarchical k=5', L['hier'][5])
    describe('kmeans k=2', L['kmeans'][2])
    describe('kmeans k=4', L['kmeans'][4])
    describe('kmeans k=5', L['kmeans'][5])

if __name__ == '__main__':
    main()
