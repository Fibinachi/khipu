"""Per-cluster header (primary cord) and body specs for the file-type analysis."""
import sqlite3
from collections import Counter, defaultdict
import statistics

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

# Load cluster assignments
clusters = {}   # khipu_id -> (cluster_id, cluster_name)
with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split(',')
        if parts[0] == 'KHIPU_ID':
            continue
        clusters[int(parts[0])] = (parts[1], parts[2])

by_cl = defaultdict(list)
for kh, (cid, cname) in clusters.items():
    by_cl[cname].append(kh)

def full_color(kh, cid):
    c.execute('SELECT FULL_COLOR FROM ascher_cord_color WHERE KHIPU_ID=? AND CORD_ID=?',
              (kh, cid))
    r = c.fetchone()
    return r[0] if r else None

for cname in sorted(by_cl):
    khs = by_cl[cname]
    print('=' * 70)
    print('CLUSTER: %s  (n=%d)' % (cname, len(khs)))

    # ---- HEADER: primary cord ----
    lens, thicks, fibers, terms, begins = [], [], [], [], []
    pcolors = []
    for kh in khs:
        c.execute('''SELECT PCORD_ID, PCORD_LENGTH, THICKNESS, FIBER, TERMINATION, BEGINNING
                     FROM primary_cord WHERE KHIPU_ID=?''', (kh,))
        for pcid, plen, th, fib, term, beg in c.fetchall():
            if plen: lens.append(plen)
            if th: thicks.append(th)
            if fib: fibers.append(fib)
            if term: terms.append(term)
            if beg: begins.append(beg)
            fc = full_color(kh, pcid)
            if fc: pcolors.append(fc)
    print('--- HEADER (primary cord) ---')
    if lens:
        print('  length: n=%d med=%.0f IQR=%.0f-%.0f range=%.0f-%.0f' % (
            len(lens), statistics.median(lens),
            sorted(lens)[len(lens)//4], sorted(lens)[3*len(lens)//4],
            min(lens), max(lens)))
    if thicks:
        print('  thickness: n=%d med=%.2f' % (len(thicks), statistics.median(thicks)))
    if fibers:
        print('  fiber: %s' % dict(Counter(fibers).most_common(5)))
    if terms:
        print('  termination: %s' % dict(Counter(terms).most_common(5)))
    if begins:
        print('  beginning: %s' % dict(Counter(begins).most_common(5)))
    if pcolors:
        print('  primary color: %s' % dict(Counter(pcolors).most_common(8)))

    # ---- BODY ----
    n_top, n_sub, maxlvl, ncomp = [], [], [], []
    for kh in khs:
        c.execute('SELECT CORD_LEVEL, COUNT(*) FROM cord WHERE KHIPU_ID=? GROUP BY CORD_LEVEL', (kh,))
        lv = {r[0]: r[1] for r in c.fetchall()}
        n_top.append(lv.get(1, 0))
        n_sub.append(sum(v for k, v in lv.items() if k and k > 1))
        maxlvl.append(max([k for k in lv if k] or [0]))
    print('--- BODY ---')
    if n_top:
        print('  L1 cords: med=%d IQR=%d-%d' % (
            statistics.median(n_top),
            sorted(n_top)[len(n_top)//4], sorted(n_top)[3*len(n_top)//4]))
    if n_sub:
        print('  subsidiary cords: med=%d' % statistics.median(n_sub))
    if maxlvl:
        print('  max level: %s' % dict(Counter(maxlvl)))
    print()
