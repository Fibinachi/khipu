"""Test the Quechua evidentiality hypothesis on khipu color-marking.

Hypothesis: color-marking encodes information source (evidentiality).
- Main cords (level 1, house/witnessed) -> minimal marking (white/unmarked)
- Subsidiaries (level 2+, rider/reported) -> obligatory source-marking (colored)
- Gradient strongest in warehouse-like structures, weaker/absent elsewhere.
"""
import sqlite3
import csv
from collections import defaultdict
from math import sqrt

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

# Load cluster assignments
clusters = {}  # khipu_id -> cluster_name
with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split(',')
        if parts[0] == 'KHIPU_ID':
            continue
        clusters[int(parts[0])] = parts[2]

# Funerary exclusion (26)
c.execute("""SELECT KHIPU_ID FROM khipu_main WHERE PROVENANCE LIKE '%Leymebamba%'
             OR PROVENANCE LIKE '%Condores%' OR PROVENANCE LIKE '%C%ndores%'
             OR NOTES LIKE '%funerary%' OR NOTES LIKE '%mummy%' OR NOTES LIKE '%burial%'""")
funerary = set(r[0] for r in c.fetchall())
print('Funerary excluded: %d' % len(funerary))

INKAWASI = set(range(1000597, 1000615))

def is_white_only(fc):
    return fc is not None and fc.strip() == 'W'

def is_marked(fc):
    """Has a non-white color component. None/missing -> separate category."""
    if fc is None:
        return None  # missing
    fc = fc.strip()
    if fc == 'W':
        return False  # white-only = unmarked
    # compound: check if any component is non-white
    parts = fc.replace('-', ':').split(':')
    return any(p.strip() not in ('W', '') for p in parts)

# Cache colors
color_cache = {}
def get_color(kh, cid):
    key = (kh, cid)
    if key not in color_cache:
        c.execute('SELECT FULL_COLOR FROM ascher_cord_color WHERE KHIPU_ID=? AND CORD_ID=?',
                  (kh, cid))
        r = c.fetchone()
        color_cache[key] = r[0] if r else None
    return color_cache[key]

def get_cords(khipu_ids):
    """Return list of (khipu_id, cord_id, level, pendant_from, color, marked)."""
    out = []
    ph = ','.join('?' * len(khipu_ids))
    c.execute(f'''SELECT KHIPU_ID, CORD_ID, CORD_LEVEL, PENDANT_FROM FROM cord
                  WHERE KHIPU_ID IN ({ph})''', list(khipu_ids))
    for kh, cid, lvl, pf in c.fetchall():
        if kh in funerary:
            continue
        fc = get_color(kh, cid)
        out.append((kh, cid, lvl, pf, fc, is_marked(fc)))
    return out

def level_gradient(khipu_ids, label):
    cords = get_cords(khipu_ids)
    by_level = defaultdict(lambda: {'marked': 0, 'unmarked': 0, 'missing': 0, 'total': 0})
    for kh, cid, lvl, pf, fc, mk in cords:
        if lvl is None:
            continue
        lvl_key = lvl if lvl <= 4 else '4+'
        by_level[lvl_key]['total'] += 1
        if mk is None:
            by_level[lvl_key]['missing'] += 1
        elif mk:
            by_level[lvl_key]['marked'] += 1
        else:
            by_level[lvl_key]['unmarked'] += 1
    print('\n=== %s (n_quipu=%d) ===' % (label, len(khipu_ids)))
    for lvl in [1, 2, 3, 4, '4+']:
        d = by_level.get(lvl)
        if not d or d['total'] == 0:
            continue
        denom = d['marked'] + d['unmarked']  # exclude missing from %
        pct = 100 * d['marked'] / denom if denom else 0
        print('  Level %s: marked %d/%d (%.1f%%), unmarked %d, missing-color %d, n=%d' % (
            lvl, d['marked'], denom, pct, d['unmarked'], d['missing'], d['total']))
    return by_level

# Group definitions
deep_hier = [k for k, cl in clusters.items() if cl == 'deep_hierarchical_grouped' and k not in funerary]
census_fmt = [k for k, cl in clusters.items() if cl == 'census_format_paired' and k not in funerary]
large_flat = [k for k, cl in clusters.items() if cl == 'large_value_flat' and k not in funerary]
deep_sparse = [k for k, cl in clusters.items() if cl == 'deep_sparse_mixed' and k not in funerary]
blank = [k for k, cl in clusters.items() if cl == 'blank_empty_stubs']

print('deep_hierarchical_grouped: %d' % len(deep_hier))
print('census_format_paired: %d' % len(census_fmt))
print('large_value_flat: %d' % len(large_flat))
print('deep_sparse_mixed: %d' % len(deep_sparse))
print('blank_empty_stubs (excluded): %d' % len(blank))

# TEST 1: gradient on warehouse-adjacent
wh1 = level_gradient(deep_hier, 'TEST 1a: deep_hierarchical_grouped (warehouse-adjacent)')
wh2 = level_gradient(list(INKAWASI), 'TEST 1b: Inkawasi anchor (18)')

# TEST 2: comparison groups
level_gradient(census_fmt, 'TEST 2a: census_format_paired')
level_gradient(large_flat, 'TEST 2b: large_value_flat')
level_gradient(deep_sparse, 'TEST 2c: deep_sparse_mixed')
