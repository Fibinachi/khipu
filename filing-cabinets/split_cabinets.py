"""Split deep_sparse_mixed khipu into documents (filing cabinet model).

Boundary signals between consecutive L1 cords (ordinal order):
  - twist shift (dominant knot direction changes)        weight 3
  - color palette shift (Jaccard distance, windows ±3)   weight 2
  - depth reset (deep run -> flat run)                   weight 2
  - empty run separator (>=2 consecutive empty cords)   weight 2
  - magnitude regime shift (log knot-count median)       weight 1
Boundary if total score >= 4. Min segment = 4 L1 cords.
"""
import sqlite3, csv, math, sys
from collections import Counter, defaultdict

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
OUT = '/home/hatch/workspace/quipu-analysis/filing-cabinets'

def load_ids():
    ids = []
    with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
        for line in f:
            if line.startswith('#') or line.startswith('KHIPU'):
                continue
            p = line.strip().split(',')
            if len(p) >= 3 and p[2] == 'deep_sparse_mixed':
                ids.append(p[0])
    return ids

def load_cord_features(conn, khipu_ids):
    """Bulk-load per-cord features. Returns {khipu_id: [cord dicts in ordinal order]}."""
    ph = ','.join('?' * len(khipu_ids))
    c = conn.cursor()
    c.execute(f"""
        SELECT c.KHIPU_ID, c.CORD_ID, c.CORD_ORDINAL, c.CORD_LEVEL,
               cc.COLOR_CD_1, cc.COLOR_CD_2
        FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
        WHERE c.KHIPU_ID IN ({ph})
        ORDER BY c.KHIPU_ID, c.CORD_ORDINAL
    """, khipu_ids)
    cords = c.fetchall()
    # bulk knot stats per cord
    c.execute(f"""
        SELECT k.CORD_ID, k.DIRECTION, COUNT(*) FROM knot k
        WHERE k.CORD_ID IN (SELECT CORD_ID FROM cord WHERE KHIPU_ID IN ({ph}))
        GROUP BY k.CORD_ID, k.DIRECTION
    """, khipu_ids)
    knotdir = defaultdict(Counter)
    for cid, d, n in c.fetchall():
        knotdir[cid][d or '?'] += n
    c.execute(f"""
        SELECT CORD_ID, COUNT(*) FROM knot
        WHERE CORD_ID IN (SELECT CORD_ID FROM cord WHERE KHIPU_ID IN ({ph}))
        GROUP BY CORD_ID
    """, khipu_ids)
    knotcount = dict(c.fetchall())

    out = defaultdict(list)
    for khipu_id, cord_id, ordinal, level, col1, col2 in cords:
        dirs = knotdir.get(cord_id, Counter())
        dom = dirs.most_common(1)[0][0] if dirs else '?'
        nk = knotcount.get(cord_id, 0)
        out[str(khipu_id)].append(dict(
            cord_id=cord_id, ordinal=ordinal or 0, level=level or 0,
            color=col1 or '?', compound=bool(col2),
            twist=dom, nknots=nk, empty=(nk == 0),
        ))
    return out

def dominant_twist_run(seq):
    return [s['twist'] for s in seq]

def find_boundaries(l1, depth_by_ord):
    """l1: list of L1 cord dicts in ordinal order. depth_by_ord: {ordinal: max level}.
    Returns list of (index, score, evidence)."""
    n = len(l1)
    if n < 8:
        return []
    bounds = []
    for i in range(4, n - 3):
        score = 0
        evidence = []
        # 1. twist shift: dominant twist in prev 3 vs next 3
        prev_t = Counter(s['twist'] for s in l1[max(0,i-3):i]).most_common(1)[0][0]
        next_t = Counter(s['twist'] for s in l1[i:i+3]).most_common(1)[0][0]
        if prev_t != '?' and next_t != '?' and prev_t != next_t:
            # require the shift to persist (not a single-cord blip)
            score += 3; evidence.append(f'twist {prev_t}->{next_t}')
        # 2. color palette shift (Jaccard on windows of 4)
        pc = set(s['color'] for s in l1[max(0,i-4):i]) - {'?'}
        nc = set(s['color'] for s in l1[i:i+4]) - {'?'}
        if pc and nc:
            jac = 1 - len(pc & nc) / len(pc | nc)
            if jac >= 0.75:
                score += 2; evidence.append(f'palette shift J={jac:.2f}')
        # 3. depth reset: deep run -> flat run
        pd = max((depth_by_ord.get(s['ordinal'], 1) for s in l1[max(0,i-3):i]), default=1)
        nd = max((depth_by_ord.get(s['ordinal'], 1) for s in l1[i:i+3]), default=1)
        if pd >= 3 and nd == 1:
            score += 2; evidence.append(f'depth reset {pd}->1')
        # 4. empty run separator: >=2 consecutive empty right before i
        if i >= 2 and l1[i-1]['empty'] and l1[i-2]['empty'] and not l1[i]['empty']:
            score += 2; evidence.append('empty-run separator')
        # 5. magnitude regime shift
        def medmag(seq):
            ms = sorted(s['nknots'] for s in seq)
            return ms[len(ms)//2] if ms else 0
        pm = medmag(l1[max(0,i-4):i]); nm = medmag(l1[i:i+4])
        if pm > 0 and nm > 0 and abs(math.log10(pm+1) - math.log10(nm+1)) > 0.7:
            score += 1; evidence.append(f'magnitude {pm}->{nm}')
        if score >= 4:
            bounds.append((i, score, '; '.join(evidence)))
    # enforce min segment length 4 by dropping weakest conflicting boundaries
    bounds.sort(key=lambda b: -b[1])
    kept = []
    for i, score, ev in bounds:
        if all(abs(i - k[0]) >= 4 for k in kept):
            kept.append((i, score, ev))
    kept.sort()
    return kept

def main():
    conn = sqlite3.connect(DB)
    ids = load_ids()
    print(f"{len(ids)} deep_sparse_mixed khipu", flush=True)
    feats = load_cord_features(conn, ids)
    # depth info per khipu: max level per L1 ordinal run -> attach subsidiaries to parent ordinal
    results = []
    for khipu_id in ids:
        seq = feats[khipu_id]
        depth_by_ord = {}
        for s in seq:
            o = s['ordinal']
            depth_by_ord[o] = max(depth_by_ord.get(o, 1), s['level'] or 1)
        l1 = [s for s in seq if s['level'] == 1]
        if not l1:
            # no L1? treat whole as one segment
            results.append(dict(khipu_id=khipu_id, segments=[(0, len(seq), 'no-L1', 0, 'no level-1 cords')]))
            continue
        bounds = find_boundaries(l1, depth_by_ord)
        # map L1 ordinal index -> cut points in full seq
        # segment k covers l1[start:end]; include subsidiaries: assign each non-L1 cord
        # to nearest preceding L1 by ordinal (PENDANT_FROM would be better but unreliable)
        cuts = [0] + [b[0] for b in bounds] + [len(l1)]
        segs = []
        for si in range(len(cuts) - 1):
            s0, s1 = cuts[si], cuts[si+1]
            ev = bounds[si-1][2] if si > 0 else 'start'
            sc = bounds[si-1][1] if si > 0 else 0
            ord0 = l1[s0]['ordinal']; ord1 = l1[s1-1]['ordinal']
            segs.append((ord0, ord1, s1 - s0, sc, ev))
        results.append(dict(khipu_id=khipu_id, segments=segs, n_l1=len(l1)))
    # summary
    n_multi = sum(1 for r in results if len(r['segments']) > 1)
    n_seg = sum(len(r['segments']) for r in results)
    print(f"khipu with >1 document: {n_multi}/{len(results)}; total segments: {n_seg}", flush=True)
    import json
    with open(f'{OUT}/segments_raw.json', 'w') as f:
        json.dump(results, f)
    print("wrote segments_raw.json", flush=True)

if __name__ == '__main__':
    main()
