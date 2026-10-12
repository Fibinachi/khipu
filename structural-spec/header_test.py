import sqlite3
import statistics
conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

c.execute('SELECT KHIPU_ID, PCORD_LENGTH FROM primary_cord WHERE PCORD_LENGTH IS NOT NULL')
rows = c.fetchall()
print('Primary cords with length:', len(rows))

data = []
for kh, plen in rows:
    c.execute('SELECT COUNT(*) FROM cord WHERE KHIPU_ID=? AND CORD_LEVEL=1', (kh,))
    n = c.fetchone()[0]
    if n > 0:
        data.append((plen, n))

print('Quipu with both:', len(data))
pls = [d[0] for d in data]
ns = [d[1] for d in data]
mp = statistics.mean(pls)
mn = statistics.mean(ns)
num = sum((a - mp) * (v - mn) for a, v in zip(pls, ns))
den = (sum((a - mp) ** 2 for a in pls) * sum((v - mn) ** 2 for v in ns)) ** 0.5
print('Correlation(primary length, pendant count): %.3f' % (num / den if den else 0))
