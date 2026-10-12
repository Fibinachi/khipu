"""Compare symbol distributions: inventory/census khipu vs all others.

'Letters' = knot types (S/L/E) and color usage. Question: do the
non-inventory/non-census khipu use a different symbolic palette?
"""
import sqlite3
import csv
from collections import Counter, defaultdict

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

# Load classifications
inv_census = set()
other = set()
with open('/home/hatch/workspace/quipu-analysis/reclassification-2026-10-10.csv') as f:
    for row in csv.DictReader(f):
        kid = int(row['KHIPU_ID'])
        dt = row['DOCUMENT_TYPE'].lower()
        if 'census' in dt or 'warehouse' in dt:
            inv_census.add(kid)
        else:
            other.add(kid)

print('Inventory/census: %d quipu' % len(inv_census))
print('Other (unclassified): %d quipu' % len(other))

def knot_dist(kids):
    counter = Counter()
    total = 0
    for kh in kids:
        c.execute('''SELECT k.TYPE_CODE, COUNT(*)
                     FROM knot k JOIN cord co ON k.CORD_ID = co.CORD_ID
                     WHERE co.KHIPU_ID = ?
                     GROUP BY k.TYPE_CODE''', (kh,))
        for tcode, n in c.fetchall():
            counter[tcode or '?'] += n
            total += n
    return counter, total

kc, kt = knot_dist(inv_census)
oc, ot = knot_dist(other)

print()
print('KNOT TYPES — inventory/census vs other:')
all_types = sorted(set(kc) | set(oc))
for t in all_types:
    kp = 100 * kc[t] / kt if kt else 0
    op = 100 * oc[t] / ot if ot else 0
    print('  %s: inv/cen %.1f%% vs other %.1f%% (diff %+.1f)' % (t, kp, op, op - kp))
print('  total knots: %d vs %d' % (kt, ot))

def color_dist(kids):
    counter = Counter()
    total = 0
    for kh in kids:
        c.execute('''SELECT FULL_COLOR, COUNT(*)
                     FROM ascher_cord_color WHERE KHIPU_ID = ?
                     GROUP BY FULL_COLOR''', (kh,))
        for fc, n in c.fetchall():
            # Simplify to base color (first component)
            base = (fc or '?').split(':')[0].split('-')[0]
            counter[base] += n
            total += n
    return counter, total

kc2, kt2 = color_dist(inv_census)
oc2, ot2 = color_dist(other)

print()
print('COLORS (base) — inventory/census vs other:')
all_c = sorted(set(kc2) | set(oc2), key=lambda x: -(kc2[x] + oc2[x]))
for col in all_c[:15]:
    kp = 100 * kc2[col] / kt2 if kt2 else 0
    op = 100 * oc2[col] / ot2 if ot2 else 0
    print('  %s: inv/cen %.1f%% vs other %.1f%% (diff %+.1f)' % (col, kp, op, op - kp))
