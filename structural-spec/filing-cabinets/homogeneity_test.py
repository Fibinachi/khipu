"""Test: are segments more homogeneous than wholes?
If splitting is meaningful, segments should have lower internal entropy
(twist, palette) than the unsplit khipu. This tests the cabinet model
without relying on the weak type classifier."""
import sqlite3, json, math, sys
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis/filing-cabinets')
from split_cabinets import load_cord_features
from collections import Counter

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'

def entropy(counter):
    tot = sum(counter.values())
    if tot == 0:
        return 0.0
    return -sum((n/tot) * math.log2(n/tot) for n in counter.values() if n > 0)

conn = sqlite3.connect(DB)
with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
    ids = [l.strip().split(',')[0] for l in f
           if not l.startswith('#') and not l.startswith('KHIPU')
           and len(l.strip().split(',')) >= 3 and l.strip().split(',')[2] == 'deep_sparse_mixed']
feats = load_cord_features(conn, ids)
segs = {e['khipu_id']: e['segments'] for e in json.load(
    open('/home/hatch/workspace/quipu-analysis/filing-cabinets/segments_raw.json'))}

improved_twist = improved_pal = 0
n_multi = 0
for kid in ids:
    seq = feats.get(kid, [])
    l1 = [s for s in seq if s['level'] == 1]
    if not l1:
        continue
    whole_twist = entropy(Counter(s['twist'] for s in l1))
    whole_pal = entropy(Counter(s['color'] for s in l1))
    sgs = segs.get(kid, [])
    if len(sgs) <= 1:
        continue
    n_multi += 1
    # weighted avg segment entropy; map segment ordinal ranges to l1 indices
    tot_l1 = 0
    w_twist = w_pal = 0.0
    # rebuild cuts
    bounds_idx = []
    # segments_raw stores (ord0, ord1, nL1, score, ev); find l1 index ranges by ordinal
    ords = [s['ordinal'] for s in l1]
    for s in sgs:
        ord0, ord1 = s[0], s[1]
        sub = [x for x in l1 if ord0 <= x['ordinal'] <= ord1]
        if not sub:
            continue
        w = len(sub)
        tot_l1 += w
        w_twist += w * entropy(Counter(x['twist'] for x in sub))
        w_pal += w * entropy(Counter(x['color'] for x in sub))
    if tot_l1:
        w_twist /= tot_l1
        w_pal /= tot_l1
        if w_twist < whole_twist - 0.1:
            improved_twist += 1
        if w_pal < whole_pal - 0.1:
            improved_pal += 1

print(f"multi-document khipu: {n_multi}")
print(f"twist entropy improved by splitting: {improved_twist}/{n_multi} ({100*improved_twist/max(n_multi,1):.0f}%)")
print(f"palette entropy improved by splitting: {improved_pal}/{n_multi} ({100*improved_pal/max(n_multi,1):.0f}%)")
