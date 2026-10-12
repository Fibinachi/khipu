"""Test pre-cut blanks vs cut-after by looking for length clustering.

Pre-cut blanks: primary cord lengths should cluster at standard sizes
within each file type (cluster family).
Cut-after-finishing: lengths should vary continuously with pendant count,
no clustering beyond what pendant count predicts.
"""
import sqlite3
import statistics
from collections import defaultdict

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

# Load cluster assignments
clusters = {}
with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split(',')
        if parts[0] == 'KHIPU_ID':
            continue
        clusters[int(parts[0])] = parts[2]

# Get primary cord lengths by cluster
by_cluster = defaultdict(list)
c.execute('SELECT KHIPU_ID, PCORD_LENGTH FROM primary_cord WHERE PCORD_LENGTH IS NOT NULL')
for kh, plen in c.fetchall():
    cl = clusters.get(kh)
    if cl:
        by_cluster[cl].append(plen)

for cl in sorted(by_cluster):
    vals = sorted(by_cluster[cl])
    n = len(vals)
    if n < 10:
        continue
    # Simple modality check: compare stdev to range
    # If clustered at standard sizes, we'd see multimodal distribution
    # Quick proxy: coefficient of variation and quartile gaps
    q1 = vals[n // 4]
    med = vals[n // 2]
    q3 = vals[3 * n // 4]
    print('%s: n=%d range=%.0f-%.0f median=%.0f IQR=%.0f-%.0f' % (
        cl, n, vals[0], vals[-1], med, q1, q3))

    # Check for round-number clustering (standard sizes often round)
    round_n = sum(1 for v in vals if v % 50 < 1 or v % 50 > 49)
    print('  lengths near multiples of 50: %d/%d (%.0f%%)' % (
        round_n, n, 100 * round_n / n))
