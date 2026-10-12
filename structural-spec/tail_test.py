"""Distinguish pre-cut vs cut-after-finishing for khipu main cords.

If makers cut the cord AFTER finishing: tail beyond last pendant should be
small and consistent (you cut near where you stopped).
If makers PRE-CUT to expected size: tail should vary, sometimes long
(unused allocation = file still open or over-provisioned).
"""
import sqlite3
import statistics

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

# For each quipu: max ATTACH_POS of level-1 pendants vs primary cord length
c.execute('''SELECT KHIPU_ID, PCORD_LENGTH FROM primary_cord WHERE PCORD_LENGTH IS NOT NULL''')
tails = []
for kh, plen in c.fetchall():
    c.execute('''SELECT MAX(ATTACH_POS) FROM cord
                 WHERE KHIPU_ID=? AND CORD_LEVEL=1 AND ATTACH_POS IS NOT NULL''', (kh,))
    r = c.fetchone()
    if r and r[0] is not None and plen > 0:
        tail = plen - r[0]
        tails.append((kh, plen, r[0], tail))

print('Quipu with both measures: %d' % len(tails))
tail_vals = [t[3] for t in tails]
print('Tail (cord end beyond last pendant):')
print('  median: %.1f' % statistics.median(tail_vals))
print('  mean: %.1f' % statistics.mean(tail_vals))
print('  stdev: %.1f' % statistics.stdev(tail_vals))
print('  min: %.1f, max: %.1f' % (min(tail_vals), max(tail_vals)))

# What fraction have substantial unused tail (>10% of cord)?
big_tail = sum(1 for t in tails if t[3] > 0.1 * t[1])
print('Quipu with tail >10%% of cord length: %d (%.1f%%)' % (big_tail, 100 * big_tail / len(tails)))

# Negative tails (last pendant beyond recorded length = data issue)
neg = sum(1 for t in tails if t[3] < 0)
print('Negative tails (data issue): %d' % neg)

# Show some examples of long tails
tails_sorted = sorted(tails, key=lambda x: x[3], reverse=True)
print()
print('Longest tails (quipu, cord_len, last_pendant_pos, tail):')
for kh, plen, lastpos, tail in tails_sorted[:8]:
    print('  %d: len=%.0f last=%.0f tail=%.0f (%.0f%% unused)' % (kh, plen, lastpos, tail, 100 * tail / plen))
