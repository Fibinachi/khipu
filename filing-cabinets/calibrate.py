"""Calibrate boundary scores: what do the signal components look like?"""
import sqlite3, math, sys
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis/filing-cabinets')
from split_cabinets import load_ids, load_cord_features
from collections import Counter

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'

def signal_profile(l1, depth_by_ord):
    n = len(l1)
    if n < 8:
        return None
    # check each signal independently: what fraction of candidate positions fire?
    twist_hits = pal_hits = depth_hits = empty_hits = mag_hits = 0
    total = 0
    for i in range(4, n - 3):
        total += 1
        prev_t = Counter(s['twist'] for s in l1[max(0,i-3):i]).most_common(1)[0][0]
        next_t = Counter(s['twist'] for s in l1[i:i+3]).most_common(1)[0][0]
        if prev_t != '?' and next_t != '?' and prev_t != next_t:
            twist_hits += 1
        pc = set(s['color'] for s in l1[max(0,i-4):i]) - {'?'}
        nc = set(s['color'] for s in l1[i:i+4]) - {'?'}
        if pc and nc and (1 - len(pc & nc) / len(pc | nc)) >= 0.75:
            pal_hits += 1
        pd = max((depth_by_ord.get(s['ordinal'], 1) for s in l1[max(0,i-3):i]), default=1)
        nd = max((depth_by_ord.get(s['ordinal'], 1) for s in l1[i:i+3]), default=1)
        if pd >= 3 and nd == 1:
            depth_hits += 1
        if i >= 2 and l1[i-1]['empty'] and l1[i-2]['empty'] and not l1[i]['empty']:
            empty_hits += 1
        def medmag(seq):
            ms = sorted(s['nknots'] for s in seq)
            return ms[len(ms)//2] if ms else 0
        pm = medmag(l1[max(0,i-4):i]); nm = medmag(l1[i:i+4])
        if pm > 0 and nm > 0 and abs(math.log10(pm+1) - math.log10(nm+1)) > 0.7:
            mag_hits += 1
    return dict(n=n, total=total, twist=twist_hits, pal=pal_hits,
                depth=depth_hits, empty=empty_hits, mag=mag_hits)

conn = sqlite3.connect(DB)
ids = load_ids()
feats = load_cord_features(conn, ids)
agg = Counter(); n_khipu = 0; n_toolong = 0
for khipu_id in ids:
    seq = feats[khipu_id]
    depth_by_ord = {}
    for s in seq:
        o = s['ordinal']
        depth_by_ord[o] = max(depth_by_ord.get(o, 1), s['level'] or 1)
    l1 = [s for s in seq if s['level'] == 1]
    if len(l1) < 8:
        n_toolong += 1
        continue
    p = signal_profile(l1, depth_by_ord)
    n_khipu += 1
    for k in ('twist','pal','depth','empty','mag'):
        agg[k] += p[k]
    agg['total'] += p['total']
print(f"khipu with >=8 L1: {n_khipu}, with <8 L1: {n_toolong}")
for k in ('twist','pal','depth','empty','mag'):
    print(f"  {k}: {agg[k]}/{agg['total']} positions ({100*agg[k]/max(agg['total'],1):.1f}%)")
