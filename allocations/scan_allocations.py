"""Scan corpus for distribution orders: value V followed by same-color values summing to V."""
import pickle, csv, os
from collections import defaultdict

CACHE = '/home/hatch/workspace/quipu-analysis/templates/cache.pkl'
OUTDIR = '/home/hatch/workspace/quipu-analysis/allocations'
os.makedirs(OUTDIR, exist_ok=True)

with open(CACHE, 'rb') as f:
    data = pickle.load(f)

print(f"Scanning {len(data)} khipu...")

candidates = []

for khipu_id, cords in data.items():
    # cords: list of (ordinal, level, color1, color2, value), assume ordinal order
    # sort by ordinal to be safe
    cords = sorted(cords, key=lambda x: x[0])
    n = len(cords)
    for i, (ord_i, lvl_i, col_i, col2_i, v_i) in enumerate(cords):
        if not v_i or v_i < 20:
            continue
        if not col_i or col_i == '?':
            continue
        # Collect following same-color nonzero values within 20-ordinal window
        comps = []  # (ordinal, value)
        for j in range(i+1, n):
            ord_j, lvl_j, col_j, col2_j, v_j = cords[j]
            if ord_j - ord_i > 20:
                break
            if col_j == col_i and v_j and v_j > 0:
                comps.append((ord_j, v_j))
        if len(comps) < 2:
            continue
        s = sum(v for _, v in comps)
        if s != v_i:
            continue
        # Exclude ambiguous: V also equals sum of PRECEDING same-color values
        prev_comps = []
        for j in range(i-1, -1, -1):
            ord_j, lvl_j, col_j, col2_j, v_j = cords[j]
            if ord_i - ord_j > 20:
                break
            if col_j == col_i and v_j and v_j > 0:
                prev_comps.append((ord_j, v_j))
        if len(prev_comps) >= 2 and sum(v for _, v in prev_comps) == v_i:
            continue  # ambiguous direction, skip
        # Position in block: is this the first cord of its color run?
        # Find start of current color run
        run_start = i
        while run_start > 0 and cords[run_start-1][2] == col_i:
            run_start -= 1
        position_in_block = 'start' if run_start == i else f'offset_{i - run_start}'
        # Span of components
        span = comps[-1][0] - comps[0][0] if comps else 0
        candidates.append({
            'khipu_id': khipu_id,
            'ordinal': ord_i,
            'color': col_i,
            'total': v_i,
            'n_components': len(comps),
            'component_ordinals': ';'.join(str(o) for o, _ in comps),
            'component_values': ';'.join(str(v) for _, v in comps),
            'position_in_block': position_in_block,
            'component_span': span,
            'has_preceding_match': len(prev_comps) >= 2 and sum(v for _, v in prev_comps) == v_i,
        })

print(f"Found {len(candidates)} candidates")

# Write CSV
with open(f'{OUTDIR}/allocation_candidates.csv', 'w', newline='') as f:
    fieldnames = ['khipu_id','ordinal','color','total','n_components',
                  'component_ordinals','component_values','position_in_block',
                  'component_span','has_preceding_match']
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    for c in sorted(candidates, key=lambda x: (x['khipu_id'], x['ordinal'])):
        w.writerow(c)

# Summary by khipu
by_khipu = defaultdict(list)
for c in candidates:
    by_khipu[c['khipu_id']].append(c)
print(f"\nKhipu with candidates: {len(by_khipu)}")
for kid in sorted(by_khipu.keys(), key=lambda x: -len(by_khipu[x]))[:20]:
    print(f"  {kid}: {len(by_khipu[kid])} candidates")
