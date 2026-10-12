"""Step 2: profile residuals vs classified population; byte n-grams + Zipf on residuals."""
import pickle, csv, math
from collections import Counter, defaultdict
import numpy as np

OUT = '/home/hatch/workspace/quipu-analysis/residuals/'
FEATS = ['n_cords','n_top','max_level','n_subsidiary','sub_parent_rate','color_fill',
         'n_colors','compound_pct','red_pct','white_pct','color_group_size','color_group_cons',
         's_pct','l_pct','e_pct','n_knots','knots_per_cord','decode_rate','val_median',
         'val_max','zero_pct','small_pct','unique_pct']

def load_all_feats():
    """Load full-corpus features if available, else return None."""
    import os
    p = '/tmp/cluster_feats.pkl'
    if os.path.exists(p):
        with open(p, 'rb') as fh:
            return pickle.load(fh)
    return None

def main():
    with open(OUT + 'residual_feats.pkl', 'rb') as fh:
        res = pickle.load(fh)
    rids = set(r['khipu_id'] for r in res)
    print(f'residuals: {len(res)}')

    full = load_all_feats()
    if full:
        clf = [r for r in full if r['khipu_id'] not in rids]
        print(f'classified (rest of corpus): {len(clf)}')

    # --- Profile comparison ---
    lines = ['# Residual Profile: unclassified vs classified populations', '']
    lines.append('| Feature | Residual median | Classified median | Residual mean | Classified mean |')
    lines.append('|---|---|---|---|---|')
    for f in FEATS:
        rv = [r[f] for r in res if r.get(f) is not None]
        row = f'| {f} | '
        if rv:
            row += f'{np.median(rv):.3f} | '
        else:
            row += '— | '
        if full:
            cv = [r[f] for r in clf if r.get(f) is not None]
            row += f'{np.median(cv):.3f} | ' if cv else '— | '
            row += f'{np.mean(rv):.3f} | ' if rv else '— | '
            row += f'{np.mean(cv):.3f} |' if cv else '— |'
        else:
            row += '— | — | — |'
        lines.append(row)

    # reason breakdown
    rc = Counter()
    for r in res:
        for reason in r['reasons'].split(';'):
            rc[reason] += 1
    lines += ['', '## Residual set composition (reasons)', '']
    for reason, n in rc.most_common():
        lines.append(f'- {reason}: {n}')

    # sup label breakdown
    sc = Counter(r['sup_label'] for r in res)
    lines += ['', '## Supervised labels within residual set', '']
    for lab, n in sc.most_common():
        lines.append(f'- {lab}: {n}')

    # provenance
    prov = Counter(r['provenance'] for r in res if r['provenance'])
    lines += ['', '## Top provenances in residual set', '']
    for p, n in prov.most_common(15):
        lines.append(f'- {p}: {n}')
    noprove = sum(1 for r in res if not r['provenance'])
    lines.append(f'- (no provenance): {noprove}')

    with open(OUT + 'residual_profile.md', 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print('wrote residual_profile.md')

if __name__ == '__main__':
    main()
