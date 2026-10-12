"""Probe deep_sparse_mixed (n=172) for subdivisions. Check: value profiles,
zero rates, color counts, provenance, and whether it splits cleanly."""
import sqlite3
import sys
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from decoder import decode_cord
from collections import Counter, defaultdict
import statistics

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

members = []
with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split(',')
        if parts[2] == 'deep_sparse_mixed':
            members.append(int(parts[0]))
print('n =', len(members))

def get_val(cid):
    try:
        r = decode_cord(conn, cid)
        return r.get('value') if isinstance(r, dict) else None
    except:
        return None

def full_color(kh, cid):
    c.execute('SELECT FULL_COLOR FROM ascher_cord_color WHERE KHIPU_ID=? AND CORD_ID=?',
              (kh, cid))
    r = c.fetchone()
    return r[0] if r else None

rows = []
for kh in members:
    c.execute('SELECT CORD_ID, CORD_LEVEL FROM cord WHERE KHIPU_ID=?', (kh,))
    cords = c.fetchall()
    n1 = sum(1 for _, l in cords if l == 1)
    nsub = sum(1 for _, l in cords if l and l > 1)
    vals = [get_val(cid) for cid, _ in cords]
    vals = [v for v in vals if v is not None]
    zr = sum(1 for v in vals if v == 0) / len(vals) if vals else 1
    nz = [v for v in vals if v > 0]
    med = statistics.median(nz) if nz else 0
    mx = max(nz) if nz else 0
    colors = set(full_color(kh, cid) for cid, _ in cords if full_color(kh, cid))
    c.execute('SELECT PROVENANCE, REGION FROM khipu_main WHERE KHIPU_ID=?', (kh,))
    prov, reg = c.fetchone() or ('', '')
    rows.append(dict(kh=kh, n1=n1, nsub=nsub, zr=zr, med=med, mx=mx,
                     ncol=len(colors), prov=prov or '', reg=reg or ''))

# Split candidates
hi_zero = [r for r in rows if r['zr'] >= 0.7]
lo_zero = [r for r in rows if r['zr'] < 0.4]
mid_zero = [r for r in rows if 0.4 <= r['zr'] < 0.7]
print('zero-rate >=70%%: %d | 40-70%%: %d | <40%%: %d' % (len(hi_zero), len(mid_zero), len(lo_zero)))

big = [r for r in rows if r['mx'] >= 500]
small = [r for r in rows if r['mx'] < 100]
print('max>=500: %d | max<100: %d' % (len(big), len(small)))

# provenance of high-zero group
print('hi-zero provenance:', dict(Counter(r['prov'][:40] for r in hi_zero).most_common(6)))
print('lo-zero provenance:', dict(Counter(r['prov'][:40] for r in lo_zero).most_common(6)))

# deep ones (>=3 levels) vs shallow within this cluster
c2 = [r for r in rows if r['nsub'] > 0]
c.execute('SELECT COUNT(*) FROM cord WHERE KHIPU_ID=? AND CORD_LEVEL>=3')
deep = []
for r in rows:
    c.execute('SELECT MAX(CORD_LEVEL) FROM cord WHERE KHIPU_ID=?', (r['kh'],))
    ml = c.fetchone()[0] or 0
    r['maxlvl'] = ml
d3 = [r for r in rows if r['maxlvl'] >= 3]
d2 = [r for r in rows if r['maxlvl'] == 2]
d1 = [r for r in rows if r['maxlvl'] <= 1]
print('maxlevel>=3: %d | =2: %d | <=1: %d' % (len(d3), len(d2), len(d1)))
print('d3 zero-rate med: %.2f | d2 zero-rate med: %.2f' % (
    statistics.median([r['zr'] for r in d3]) if d3 else 0,
    statistics.median([r['zr'] for r in d2]) if d2 else 0))
