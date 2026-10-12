"""Find the same DATA expressed through different TEMPLATES.

Stage 1: for each khipu with an extracted template, re-segment rows, re-extract
         template, pull values from VAR/MIXED positions only (strip the form).
Stage 2: fingerprint each khipu's variable data (distribution stats, Benford,
         marker-value presence, sparsity, etc).
Stage 3: cluster fingerprints (Ward hierarchical, silhouette-picked k).
Stage 4: cross-tab data clusters vs template IDs vs doc-type clusters vs region.
"""
import sys, os, csv, pickle, math
from collections import Counter, defaultdict

import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist

sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from templates.extract_templates import segment_rows, extract_template

TDIR = '/home/hatch/workspace/quipu-analysis/templates'
OUT = '/home/hatch/workspace/quipu-analysis/data-match'
os.makedirs(OUT, exist_ok=True)

MARKER_VALS = {22, 23, 32, 33, 34}
BENFORD = np.array([math.log10(1 + 1/d) for d in range(1, 10)])

def load():
    with open(os.path.join(TDIR, 'cache.pkl'), 'rb') as f:
        data = pickle.load(f)
    sigs = pd.read_csv(os.path.join(TDIR, 'template_signatures.csv'), dtype={'khipu_id': str})
    clus = {}
    with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
        for line in f:
            if line.startswith('#') or line.startswith('KHIPU'):
                continue
            p = line.strip().split(',')
            if len(p) >= 3:
                clus[p[0].strip()] = p[2].strip()
    return data, sigs, clus

def variable_values(kid, rows):
    """Segment rows, extract template, return (var_values, var_positions_info)."""
    method, row_list, info = segment_rows(kid, rows)
    if method == 'none' or len(row_list) < 3:
        return None, method, []
    sig = extract_template(row_list)
    var_pos = {p for (p, c, k, v) in sig if k in ('VAR', 'MIXED')}
    vals = []
    pos_detail = []  # (pos, color, value)
    for r in row_list:
        for (p, c, k, v) in sig:
            if p in var_pos and p < len(r):
                vals.append(r[p][4])  # decoded value (may be None)
                pos_detail.append((p, r[p][2], r[p][4]))
    return vals, method, pos_detail

def fingerprint(vals):
    """vals: list of values (may contain None/0). Returns dict of features."""
    n = len(vals)
    v = np.array([x if x is not None else 0 for x in vals], dtype=float)
    fail_frac = sum(1 for x in vals if x is None) / n if n else 0
    zero_frac = np.mean(v == 0) if n else 0
    nz = v[v > 0]
    feat = {'n_var': n, 'fail_frac': fail_frac, 'zero_frac': zero_frac}
    if len(nz) == 0:
        feat.update({k: 0 for k in
                     ['log_med', 'log_iqr', 'log_max', 'log_mean', 'cv',
                      'small_frac', 'med_frac', 'large_frac', 'mode_frac',
                      'marker_frac', 'benford_chi2', 'entropy']})
        feat['top5'] = ''
        return feat
    feat['log_med'] = math.log10(np.median(nz) + 1)
    q75, q25 = np.percentile(nz, [75, 25])
    feat['log_iqr'] = math.log10((q75 - q25) + 1)
    feat['log_max'] = math.log10(nz.max() + 1)
    feat['log_mean'] = math.log10(nz.mean() + 1)
    feat['cv'] = float(np.std(nz) / np.mean(nz)) if np.mean(nz) > 0 else 0
    feat['small_frac'] = float(np.mean(nz < 10))
    feat['med_frac'] = float(np.mean((nz >= 10) & (nz < 100)))
    feat['large_frac'] = float(np.mean(nz >= 100))
    mc = Counter(nz.tolist()).most_common(5)
    feat['top5'] = ';'.join(f'{int(k)}:{c}' for k, c in mc)
    feat['mode_frac'] = mc[0][1] / len(nz)
    feat['marker_frac'] = float(np.mean(np.isin(nz, list(MARKER_VALS))))
    # Benford on leading digit of values >= 10
    big = nz[nz >= 10]
    if len(big) >= 20:
        lead = np.array([int(str(int(x))[0]) for x in big])
        obs = np.array([np.mean(lead == d) for d in range(1, 10)])
        exp = BENFORD
        feat['benford_chi2'] = float(np.sum((obs - exp) ** 2 / exp) * len(big))
    else:
        feat['benford_chi2'] = -1  # insufficient data flag
    # entropy of log10-binned histogram
    lb = np.log10(nz + 1)
    hist, _ = np.histogram(lb, bins=10, range=(0, 5))
    p = hist / hist.sum()
    p = p[p > 0]
    feat['entropy'] = float(-np.sum(p * np.log(p)))
    return feat

def main():
    data, sigs, clus = load()
    print(f'{len(sigs)} khipu with templates', flush=True)

    records = []   # variable_data rows
    feats = {}
    for _, row in sigs.iterrows():
        kid = str(row['khipu_id'])
        rows = data.get(kid, [])
        if not rows:
            continue
        vals, method, pos_detail = variable_values(kid, rows)
        if vals is None:
            records.append({'khipu_id': kid, 'template_exact': row['template_exact'],
                            'method': method, 'n_var_values': 0,
                            'n_var_positions': 0, 'value_summary': 'no_rows'})
            continue
        # value summary: min/median/max of nonzero + count
        nz = [x for x in vals if x]
        summ = (f'n={len(vals)} nz={len(nz)} ' +
                (f'min={min(nz)} med={sorted(nz)[len(nz)//2]} max={max(nz)}' if nz else 'all_zero'))
        n_var_pos = len({p for p, _, _ in pos_detail})
        records.append({'khipu_id': kid, 'template_exact': row['template_exact'],
                        'method': method, 'n_var_values': len(vals),
                        'n_var_positions': n_var_pos, 'value_summary': summ})
        feats[kid] = fingerprint(vals)

    var_df = pd.DataFrame(records)
    var_df.to_csv(os.path.join(OUT, 'variable_data.csv'), index=False)
    print(f'variable_data.csv: {len(var_df)} rows', flush=True)

    # fingerprints
    fp_rows = []
    for kid, f in feats.items():
        r = {'khipu_id': kid}
        r.update(f)
        fp_rows.append(r)
    fp = pd.DataFrame(fp_rows)
    fp.to_csv(os.path.join(OUT, 'data_fingerprints.csv'), index=False)
    print(f'data_fingerprints.csv: {len(fp)} rows', flush=True)

    # cluster: only khipu with enough variable data
    good = fp[(fp['n_var'] >= 10) & (fp['fail_frac'] < 0.5)].copy()
    print(f'{len(good)} khipu with >=10 variable values for clustering', flush=True)
    feat_cols = ['log_med', 'log_iqr', 'log_max', 'log_mean', 'cv',
                 'small_frac', 'med_frac', 'large_frac', 'mode_frac',
                 'marker_frac', 'entropy', 'zero_frac']
    X = good[feat_cols].to_numpy(dtype=float)
    # z-score
    mu, sd = X.mean(0), X.std(0)
    sd[sd == 0] = 1
    Z = (X - mu) / sd
    D = pdist(Z, metric='euclidean')
    L = linkage(D, method='ward')

    # silhouette pick k in 2..10
    def silhouette(Z, labels):
        from scipy.spatial.distance import cdist
        labs = np.unique(labels)
        if len(labs) < 2:
            return -1
        sil = []
        for i in range(len(Z)):
            same = Z[labels == labels[i]]
            a = np.mean(cdist([Z[i]], same)[0][1:]) if len(same) > 1 else 0
            b = min(np.mean(cdist([Z[i]], Z[labels == l])[0])
                    for l in labs if l != labels[i])
            sil.append((b - a) / max(a, b) if max(a, b) > 0 else 0)
        return float(np.mean(sil))
    best_k, best_s = 2, -1
    for k in range(2, 11):
        lab = fcluster(L, k, criterion='maxclust')
        s = silhouette(Z, lab)
        print(f'  k={k} silhouette={s:.3f}', flush=True)
        if s > best_s:
            best_k, best_s = k, s
    print(f'picked k={best_k} (sil={best_s:.3f})', flush=True)
    good['data_cluster'] = fcluster(L, best_k, criterion='maxclust')

    # attach metadata
    meta = sigs.set_index('khipu_id')[['template_exact', 'template_fuzzy',
                                       'n_rows', 'method', 'cluster',
                                       'provenance', 'region']].copy()
    meta.index = meta.index.astype(str)
    good = good.join(meta, on='khipu_id')
    good['doc_cluster'] = good['khipu_id'].map(clus)
    good.to_csv(os.path.join(OUT, 'data_clusters.csv'), index=False)

    # also write cluster assignment for ALL fingerprinted khipu (low-data get cluster 0)
    allc = fp[['khipu_id']].copy()
    allc = allc.join(meta, on='khipu_id')
    allc['doc_cluster'] = allc['khipu_id'].map(clus)
    cmap = dict(zip(good['khipu_id'], good['data_cluster']))
    allc['data_cluster'] = allc['khipu_id'].map(cmap).fillna(0).astype(int)
    allc.to_csv(os.path.join(OUT, 'data_clusters.csv'), index=False)
    print('data_clusters.csv written', flush=True)

    # ---- analysis ----
    rep = []
    rep.append('# Same Data, Different Templates — Report\n')
    rep.append(f'Khipu with templates: {len(sigs)}; fingerprinted: {len(fp)}; '
               f'clustered (n_var>=10): {len(good)}; data clusters (k={best_k}): {best_k}\n')

    rep.append('## Data cluster profiles\n')
    rep.append('| cluster | n | med_value | iqr | max | zero_frac | marker_frac | entropy |')
    rep.append('|---|---|---|---|---|---|---|---|')
    for dc in sorted(good['data_cluster'].unique()):
        g = good[good['data_cluster'] == dc]
        rep.append(f'| {dc} | {len(g)} | {10**g["log_med"].median()-1:.0f} | '
                   f'{10**g["log_iqr"].median()-1:.0f} | {10**g["log_max"].median()-1:.0f} | '
                   f'{g["zero_frac"].median():.2f} | {g["marker_frac"].median():.2f} | '
                   f'{g["entropy"].median():.2f} |')
    rep.append('')

    rep.append('## Data cluster vs document-type cluster\n')
    ct = pd.crosstab(good['data_cluster'], good['doc_cluster'])
    rep.append('```\n' + ct.to_string() + '\n```\n')

    rep.append('## Data cluster vs template: do data clusters span templates?\n')
    for dc in sorted(good['data_cluster'].unique()):
        g = good[good['data_cluster'] == dc]
        n_t = g['template_exact'].nunique()
        rep.append(f'- data cluster {dc}: {len(g)} khipu across **{n_t} distinct templates** '
                   f'(members: {", ".join(g["khipu_id"].tolist()[:12])}'
                   f'{"..." if len(g) > 12 else ""})')
    rep.append('')

    rep.append('## Data cluster vs region/provenance\n')
    for dc in sorted(good['data_cluster'].unique()):
        g = good[good['data_cluster'] == dc]
        pr = Counter((g['provenance'].fillna('unknown') + '/' + g['region'].fillna('')).str.strip('/'))
        rep.append(f'- cluster {dc}: ' + ', '.join(f'{k}={v}' for k, v in pr.most_common(4)))
    rep.append('')

    # marker values in variable positions
    rep.append('## 22/23/32/33/34 in variable positions\n')
    mk = good[good['marker_frac'] > 0].sort_values('marker_frac', ascending=False)
    rep.append(f'{len(mk)}/{len(good)} khipu have marker values (22/23/32/33/34) in variable positions.\n')
    if len(mk):
        rep.append('| khipu | data_cluster | template | marker_frac | top5 | doc_cluster |')
        rep.append('|---|---|---|---|---|---|')
        for _, r in mk.head(20).iterrows():
            t5 = fp.set_index('khipu_id').loc[r['khipu_id'], 'top5']
            rep.append(f'| {r["khipu_id"]} | {r["data_cluster"]} | {r["template_exact"]} | '
                       f'{r["marker_frac"]:.2f} | {t5} | {r["doc_cluster"]} |')
    rep.append('')

    # Benford
    rep.append('## Benford check (leading digits, values>=10, n>=20)\n')
    bf = good[fp.set_index('khipu_id').loc[good['khipu_id'], 'benford_chi2'].to_numpy() >= 0]
    rep.append(f'{len(bf)} khipu had enough large values for a Benford test. '
               f'Median chi2 (df=8, 5% crit=15.5): '
               f'{fp.set_index("khipu_id").loc[bf["khipu_id"], "benford_chi2"].median():.1f}\n')

    # warehouse question
    rep.append('## Do warehouse-type khipu share a data fingerprint?\n')
    # doc clusters containing 'warehouse' or similar
    docvals = sorted(str(x) for x in good['doc_cluster'].dropna().unique())
    rep.append('Document clusters present: ' + ', '.join(docvals) + '\n')
    for dv in docvals:
        g = good[good['doc_cluster'] == dv]
        if len(g) >= 3:
            dc = Counter(g['data_cluster'])
            rep.append(f'- {dv} (n={len(g)}): data clusters ' +
                       ', '.join(f'{k}×{v}' for k, v in dc.most_common()))

    with open(os.path.join(OUT, 'data_match_report.md'), 'w') as f:
        f.write('\n'.join(rep))
    print('\n'.join(rep[:60]), flush=True)

if __name__ == '__main__':
    main()
