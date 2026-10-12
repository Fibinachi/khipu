"""Value roundness check for large_value_flat: are values round (summaries/tallies)
or precise (transactions)? Compare across clusters."""
import sqlite3
import sys
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from decoder import decode_cord
from collections import defaultdict
import statistics

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

members = defaultdict(list)
with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
    for line in f:
        if line.startswith('#') or line.startswith('KHIPU_ID'):
            continue
        parts = line.strip().split(',')
        members[parts[2]].append(int(parts[0]))

def get_val(cid):
    try:
        r = decode_cord(conn, cid)
        return r.get('value') if isinstance(r, dict) else None
    except:
        return None

for cname in ['large_value_flat', 'census_format_paired', 'deep_hierarchical_grouped']:
    vals = []
    for kh in members[cname][:40]:  # sample 40 for speed
        c.execute('SELECT CORD_ID FROM cord WHERE KHIPU_ID=? AND CORD_LEVEL=1', (kh,))
        for (cid,) in c.fetchall():
            v = get_val(cid)
            if v and v > 0:
                vals.append(v)
    if not vals:
        continue
    round10 = sum(1 for v in vals if v % 10 == 0) / len(vals)
    round100 = sum(1 for v in vals if v % 100 == 0) / len(vals)
    print('%s: n=%d med=%d | %%10==0: %.1f%% | %%100==0: %.1f%%' % (
        cname, len(vals), statistics.median(vals), 100 * round10, 100 * round100))
