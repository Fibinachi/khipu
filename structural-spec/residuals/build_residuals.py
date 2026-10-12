"""Residual analysis: structure of the unclassified khipu.

Builds the residual set, extracts features, profiles vs classified,
byte n-grams + Zipf, subset clustering, rare feature census.
"""
import sqlite3, sys, csv, math, pickle
from collections import Counter, defaultdict
import numpy as np

sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from cluster_step1_features import extract, FEATS
from khipu_hex import serialize_khipu

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
OUT = '/home/hatch/workspace/quipu-analysis/residuals/'

def build_residual_set():
    sup = {}
    with open('/home/hatch/workspace/quipu-analysis/reclassification-2026-10-10.csv') as f:
        for r in csv.DictReader(f):
            sup[r['KHIPU_ID']] = r['DOCUMENT_TYPE']
    clus = {}
    with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
        for line in f:
            if line.startswith('#') or line.startswith('KHIPU'): continue
            p = line.strip().split(',')
            clus[p[0]] = p[2]
    cab = {}
    with open('/home/hatch/workspace/quipu-analysis/filing-cabinets/cabinet_summary.csv') as f:
        for r in csv.DictReader(f):
            cab[r['khipu_id']] = (r['n_documents'], r['types_present'])
    core = set(k for k,v in sup.items() if v=='unclassified' and clus.get(k)=='deep_sparse_mixed')
    cabinet_resid = set(k for k,(n,t) in cab.items() if n=='1' and t=='unclassified')
    rare_knot = {'1000096','1000279','1000317','1000382','1000504','1000514','1000522',
                 '1000526','1000528','1000533','1000554','1000598','1000605','1000608',
                 '1000613','1000624','1000635'}
    anomalous = {'1000004','1000005','1000008','1000009','1000018','1000027','1000144',
                 '1000176','1000178','1000183','1000197','1000198','1000201','1000239',
                 '1000249','1000344','1000454','1000504','1000567','1000583'}
    ee_heavy = {'1000159','1000279','1000060'}
    all_u = {'1000029','1000034','1000345','1000361','1000368'}

    reasons = defaultdict(list)
    for k in core: reasons[k].append('sup-unclassified+deep_sparse_mixed')
    for k in cabinet_resid: reasons[k].append('cabinet-no-split-unclassified')
    for k in rare_knot: reasons[k].append('rare-knot-type')
    for k in anomalous: reasons[k].append('anomalous-transcription')
    for k in ee_heavy: reasons[k].append('EE-heavy')
    for k in all_u: reasons[k].append('all-U-twist')
    return reasons, sup, clus

def main():
    reasons, sup, clus = build_residual_set()
    kids = sorted(reasons.keys(), key=int)
    print(f'residual set: {len(kids)} khipu', flush=True)

    conn = sqlite3.connect(DB)
    feats = []
    for i, kid in enumerate(kids):
        try:
            f = extract(conn, kid)
            f['reasons'] = ';'.join(reasons[kid])
            f['sup_label'] = sup.get(kid, '?')
            f['cluster'] = clus.get(kid, '?')
            feats.append(f)
        except Exception as e:
            print(f'ERR {kid}: {e}', file=sys.stderr)
        if (i+1) % 30 == 0:
            print(f'  {i+1}/{len(kids)}', flush=True)

    with open(OUT + 'residual_feats.pkl', 'wb') as fh:
        pickle.dump(feats, fh)
    print(f'saved {len(feats)} feature rows', flush=True)

    # unclassified_set.csv
    with open(OUT + 'unclassified_set.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['khipu_id','why_unclassified','n_cords','n_colors','max_level',
                    'sup_label','cluster','provenance','region'])
        for r in feats:
            w.writerow([r['khipu_id'], r['reasons'], r['n_cords'], r['n_colors'],
                        r['max_level'], r['sup_label'], r['cluster'],
                        r['provenance'], r['region']])
    print('wrote unclassified_set.csv', flush=True)

if __name__ == '__main__':
    main()
