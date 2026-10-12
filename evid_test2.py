"""Evidentiality tests 3-5: chi-square, color contrast replication, white-parent prediction."""
import sqlite3
import csv
from collections import defaultdict
from math import sqrt, erf

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

clusters = {}
with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split(',')
        if parts[0] == 'KHIPU_ID':
            continue
        clusters[int(parts[0])] = parts[2]

c.execute("""SELECT KHIPU_ID FROM khipu_main WHERE PROVENANCE LIKE '%Leymebamba%'
             OR PROVENANCE LIKE '%Condores%' OR NOTES LIKE '%funerary%'
             OR NOTES LIKE '%mummy%' OR NOTES LIKE '%burial%'""")
funerary = set(r[0] for r in c.fetchall())

deep_hier = [k for k, cl in clusters.items()
             if cl == 'deep_hierarchical_grouped' and k not in funerary]

# Batch-load all colors for deep_hier quipu
ph = ','.join('?' * len(deep_hier))
c.execute(f'SELECT KHIPU_ID, CORD_ID, FULL_COLOR FROM ascher_cord_color WHERE KHIPU_ID IN ({ph})',
          deep_hier)
colors = {(r[0], r[1]): r[2] for r in c.fetchall()}
print('Colors loaded: %d' % len(colors))

c.execute(f'''SELECT KHIPU_ID, CORD_ID, CORD_LEVEL, PENDANT_FROM FROM cord
              WHERE KHIPU_ID IN ({ph})''', deep_hier)
cords = [(r[0], r[1], r[2], r[3]) for r in c.fetchall()
         if r[0] not in funerary]
print('Cords: %d' % len(cords))

def is_marked(fc):
    if fc is None:
        return None
    fc = fc.strip()
    if fc == 'W':
        return False
    parts = fc.replace('-', ':').split(':')
    return any(p.strip() not in ('W', '') for p in parts)

def is_white_only(fc):
    return fc is not None and fc.strip() == 'W'

# TEST 3: chi-square — subsidiary more likely marked than main?
main_marked = main_unmarked = sub_marked = sub_unmarked = 0
for kh, cid, lvl, pf in cords:
    if lvl is None:
        continue
    mk = is_marked(colors.get((kh, cid)))
    if mk is None:
        continue
    if lvl == 1:
        if mk:
            main_marked += 1
        else:
            main_unmarked += 1
    elif lvl > 1:
        if mk:
            sub_marked += 1
        else:
            sub_unmarked += 1

print('\n=== TEST 3: chi-square (warehouse-adjacent) ===')
print('Main: marked=%d unmarked=%d' % (main_marked, main_unmarked))
print('Sub:  marked=%d unmarked=%d' % (sub_marked, sub_unmarked))

# Chi-square 2x2
a, b, cc_, d = main_marked, main_unmarked, sub_marked, sub_unmarked
n = a + b + cc_ + d
exp_a = (a + b) * (a + cc_) / n
exp_b = (a + b) * (b + d) / n
exp_c = (cc_ + d) * (a + cc_) / n
exp_d = (cc_ + d) * (b + d) / n
chi2 = sum((o - e) ** 2 / e for o, e in [(a, exp_a), (b, exp_b), (cc_, exp_c), (d, exp_d)])
# p-value from chi-square(1): p = 1 - Phi(sqrt(chi2))... use survival
# For df=1, p = erfc(sqrt(chi2/2))
p = 1 - erf(sqrt(chi2 / 2)) if chi2 > 0 else 1.0
# erfc approximation
import math
p_val = math.erfc(sqrt(chi2 / 2))
print('Chi-square = %.1f, df=1, p = %.2e' % (chi2, p_val))
print('OR (sub marked vs main marked) = %.2f' % ((cc_ / d) / (a / b)))

# TEST 4: color contrast replication on warehouse-adjacent
# Build parent map
cord_map = {(kh, cid): (lvl, pf) for kh, cid, lvl, pf in cords}
contrast_n = contrast_diff = 0
for kh, cid, lvl, pf in cords:
    if lvl is None or lvl <= 1 or pf is None:
        continue
    parent_key = (kh, pf)
    if parent_key not in cord_map:
        continue
    child_fc = colors.get((kh, cid))
    parent_fc = colors.get(parent_key)
    if child_fc is None or parent_fc is None:
        continue
    # Normalize: compare base color sets
    def bases(fc):
        return set(p.strip() for p in fc.replace('-', ':').split(':') if p.strip())
    contrast_n += 1
    if bases(child_fc) != bases(parent_fc):
        contrast_diff += 1

print('\n=== TEST 4: color contrast (warehouse-adjacent, not just Inkawasi) ===')
print('Subsidiaries differing from parent: %d/%d (%.1f%%)' % (
    contrast_diff, contrast_n, 100 * contrast_diff / contrast_n))

# Null: reshuffle child colors within quipu, recompute
import random
random.seed(42)
null_diffs = []
for trial in range(200):
    # reshuffle colors among subsidiaries within each quipu
    by_kh = defaultdict(list)
    child_keys = []
    for kh, cid, lvl, pf in cords:
        if lvl is None or lvl <= 1 or pf is None:
            continue
        if (kh, pf) not in cord_map:
            continue
        if colors.get((kh, cid)) is None or colors.get((kh, pf)) is None:
            continue
        by_kh[kh].append((kh, cid, pf))
        child_keys.append((kh, cid))
    # shuffle colors within quipu
    shuffled = {}
    for kh, kids in by_kh.items():
        fcs = [colors[(kh, cid)] for kh, cid, pf in kids]
        random.shuffle(fcs)
        for (kh2, cid2, pf2), fc in zip(kids, fcs):
            shuffled[(kh2, cid2)] = fc
    nd = 0
    nn = 0
    for kh, cid, lvl, pf in cords:
        if lvl is None or lvl <= 1 or pf is None:
            continue
        if (kh, pf) not in cord_map:
            continue
        cfc = shuffled.get((kh, cid))
        pfc = colors.get((kh, pf))
        if cfc is None or pfc is None:
            continue
        def bases(fc):
            return set(p.strip() for p in fc.replace('-', ':').split(':') if p.strip())
        nn += 1
        if bases(cfc) != bases(pfc):
            nd += 1
    null_diffs.append(nd / nn if nn else 0)
null_mean = sum(null_diffs) / len(null_diffs)
obs = contrast_diff / contrast_n
exceed = sum(1 for x in null_diffs if x >= obs)
print('Null (reshuffled) mean: %.1f%%, observed %.1f%%, p < %.3f (%d/200 trials >= obs)' % (
    100 * null_mean, 100 * obs, (exceed + 1) / 201, exceed))

# TEST 5: subsidiaries of white parents MORE marked than of colored parents?
sub_white_parent_marked = sub_white_parent_unmarked = 0
sub_color_parent_marked = sub_color_parent_unmarked = 0
for kh, cid, lvl, pf in cords:
    if lvl is None or lvl <= 1 or pf is None:
        continue
    parent_key = (kh, pf)
    if parent_key not in cord_map:
        continue
    child_fc = colors.get((kh, cid))
    parent_fc = colors.get(parent_key)
    if child_fc is None or parent_fc is None:
        continue
    cmk = is_marked(child_fc)
    if cmk is None:
        continue
    if is_white_only(parent_fc):
        if cmk:
            sub_white_parent_marked += 1
        else:
            sub_white_parent_unmarked += 1
    else:
        # colored parent (has non-white component)
        pmk = is_marked(parent_fc)
        if pmk:  # only count definitively colored parents
            if cmk:
                sub_color_parent_marked += 1
            else:
                sub_color_parent_unmarked += 1

print('\n=== TEST 5: subsidiaries of white vs colored parents ===')
w_tot = sub_white_parent_marked + sub_white_parent_unmarked
cc_tot = sub_color_parent_marked + sub_color_parent_unmarked
print('White parent -> sub marked: %d/%d (%.1f%%)' % (
    sub_white_parent_marked, w_tot, 100 * sub_white_parent_marked / w_tot if w_tot else 0))
print('Colored parent -> sub marked: %d/%d (%.1f%%)' % (
    sub_color_parent_marked, cc_tot, 100 * sub_color_parent_marked / cc_tot if cc_tot else 0))
# chi-square
a, b, cc2, d = sub_white_parent_marked, sub_white_parent_unmarked, sub_color_parent_marked, sub_color_parent_unmarked
n = a + b + cc2 + d
if n > 0 and min(a, b, cc2, d) >= 0:
    exp_a = (a + b) * (a + cc2) / n
    exp_b = (a + b) * (b + d) / n
    exp_c = (cc2 + d) * (a + cc2) / n
    exp_d = (cc2 + d) * (b + d) / n
    chi2 = sum((o - e) ** 2 / e for o, e in [(a, exp_a), (b, exp_b), (cc2, exp_c), (d, exp_d)] if e > 0)
    p_val = math.erfc(sqrt(chi2 / 2)) if chi2 > 0 else 1.0
    print('Chi-square = %.1f, p = %.2e' % (chi2, p_val))
