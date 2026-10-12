"""Step 1: Identify anomalous khipu from NOTES fields."""
import sqlite3, csv, re
from collections import defaultdict

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

KEYWORDS = ['unusual', 'strange', 'weird', 'anomal', 'unclear', 'mystery',
            'odd', 'peculiar', 'bizarre', 'exception', 'irregular',
            'cannot read', "can't read", 'illegible', 'confusing',
            'not attached', 'unattached', 'loose', 'broken', 'repaired',
            'modern thread', 'reinforced', 'joined', 'two khipus',
            'doubled', 'spiral', 'turfted', 'belted', 'double figure',
            'mottling', 'senales', 'signal', 'marker thread']

anomalies = {}  # khipu_id -> list of reasons

# 1. khipu_main NOTES
c.execute("SELECT KHIPU_ID, NOTES FROM khipu_main WHERE NOTES IS NOT NULL AND NOTES != ''")
for kh, notes in c.fetchall():
    nl = notes.lower()
    hits = [k for k in KEYWORDS if k in nl]
    if hits:
        snippet = notes[:160].replace('\n', ' ')
        anomalies.setdefault(kh, []).append(f"MAIN NOTE [{', '.join(hits)}]: {snippet}")

# 2. cord CORD_NOTES - aggregate unusual ones
c.execute("""SELECT KHIPU_ID, COUNT(*) as n FROM cord
             WHERE CORD_NOTES IS NOT NULL AND CORD_NOTES != ''
             GROUP BY KHIPU_ID ORDER BY n DESC LIMIT 40""")
cord_note_counts = c.fetchall()

for kh, n in cord_note_counts:
    c.execute("SELECT CORD_NOTES FROM cord WHERE KHIPU_ID=? AND CORD_NOTES IS NOT NULL AND CORD_NOTES != '' LIMIT 3", (kh,))
    samples = [r[0][:120].replace('\n', ' ') for r in c.fetchall()]
    # check for anomaly keywords in samples
    for s in samples:
        sl = s.lower()
        hits = [k for k in KEYWORDS if k in sl]
        if hits:
            anomalies.setdefault(kh, []).append(f"CORD NOTE [{', '.join(hits)}]: {s}")
            break

# 3. Cross-ref with clusters - deep_sparse_mixed members
clusters = {}
with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
    for line in f:
        if line.startswith('#') or line.startswith('KHIPU_ID'):
            continue
        p = line.strip().split(',')
        clusters[int(p[0])] = p[2]

# 4. reclassification unclassified with strange flags
reclass = {}
try:
    with open('/home/hatch/workspace/quipu-analysis/reclassification-2026-10-10.csv') as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            reclass[int(row['KHIPU_ID'])] = (row['DOCUMENT_TYPE'], row.get('EVIDENCE_NOTES', '')[:100])
except FileNotFoundError:
    pass

print(f"Total khipu with anomaly-flagged notes: {len(anomalies)}")
print()
for kh in sorted(anomalies):
    cl = clusters.get(kh, '?')
    rc = reclass.get(kh, ('?', ''))[0]
    print(f"=== {kh} | cluster={cl} | reclass={rc}")
    for reason in anomalies[kh][:2]:
        print(f"    {reason}")
    print()
