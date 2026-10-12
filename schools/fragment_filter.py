"""Fragment-joining filter: match 4-color sequences weighted by distinctiveness."""
import sqlite3, csv, math
from collections import Counter, defaultdict

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

flat_ids = []
with open('/home/hatch/workspace/quipu-analysis/spreadsheets/spreadsheet_index.csv') as f:
    r = csv.DictReader(f)
    for row in r:
        if row['format'] == '.flat':
            flat_ids.append(row['khipu_id'])

# Group .flat by provenance (3+ members)
prov_groups = defaultdict(list)
for kid in flat_ids:
    c.execute('SELECT PROVENANCE, REGION FROM khipu_main WHERE KHIPU_ID=?', (kid,))
    row = c.fetchone()
    if row:
        key = (row[0] or '').strip() or (row[1] or '').strip() or 'unknown'
        prov_groups[key].append(kid)

# Color sequences per khipu (cache)
seq_cache = {}
def get_seq(kid):
    if kid not in seq_cache:
        c.execute('''
            SELECT co.CORD_ORDINAL, cc.COLOR_CD_1 FROM cord co
            LEFT JOIN ascher_cord_color cc ON co.CORD_ID = cc.CORD_ID
            WHERE co.KHIPU_ID=? ORDER BY co.CORD_ORDINAL
        ''', (kid,))
        seen = {}
        for o, col in c.fetchall():
            if o not in seen: seen[o] = (col or '?').strip()
        seq_cache[kid] = [seen[o] for o in sorted(seen.keys())]
    return seq_cache[kid]

# Global bigram frequencies for distinctiveness weighting
print("Building global bigram model...", flush=True)
bigram_counts = Counter()
total_bigrams = 0
for kid in flat_ids[:400]:
    seq = get_seq(kid)
    for i in range(len(seq) - 1):
        bigram_counts[(seq[i], seq[i+1])] += 1
        total_bigrams += 1

def bigram_surprisal(a, b):
    """Higher = more distinctive = stronger join evidence."""
    p = bigram_counts.get((a, b), 0.5) / total_bigrams
    return -math.log(p)

# Per site: find joins on 4-color overlap
print("\nScanning sites for 4-color joins...", flush=True)
all_joins = []
for prov, members in sorted(prov_groups.items(), key=lambda x: -len(x[1])):
    if len(members) < 3 or prov == 'unknown':
        continue
    # index all 4-grams by their tuple
    fourgram_index = defaultdict(list)
    for kid in members:
        seq = get_seq(kid)
        for i in range(len(seq) - 3):
            fourgram_index[tuple(seq[i:i+4])].append((kid, i, len(seq)))
    # a join: A's trailing 4-gram == B's leading 4-gram (positional)
    # EXCLUDE monochromatic 4-grams (single repeated color = run, not syntax)
    for kid in members:
        seq = get_seq(kid)
        if len(seq) < 4: continue
        tail = tuple(seq[-4:])
        if len(set(tail)) < 2: continue
        for (okid, pos, slen) in fourgram_index.get(tail, []):
            if okid == kid: continue
            if pos > 2: continue  # must be near B's start
            # score by surprisal of the 3 bigrams in the 4-gram
            score = sum(bigram_surprisal(tail[i], tail[i+1]) for i in range(3))
            all_joins.append((score, kid, okid, tail, prov))

all_joins.sort(reverse=True)
# dedupe identical (from, to, 4gram) pairs
seen_pairs = set()
deduped = []
for score, a, b, tail, prov in all_joins:
    key = (a, b, tail)
    if key not in seen_pairs:
        seen_pairs.add(key)
        deduped.append((score, a, b, tail, prov))
all_joins = deduped
print(f"\n{len(all_joins)} candidate joins found (deduped)", flush=True)
print("\nTop 20 by distinctiveness:", flush=True)
for score, a, b, tail, prov in all_joins[:20]:
    print(f"  {score:.1f}: {a} -> {b} via {tail} [{prov[:30]}]", flush=True)

# Save
with open('/home/hatch/workspace/quipu-analysis/schools/fragment_joins.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['score', 'from_khipu', 'to_khipu', 'match_4gram', 'provenance'])
    for score, a, b, tail, prov in all_joins:
        w.writerow([round(score, 2), a, b, '>'.join(tail), prov])
print("\nWrote schools/fragment_joins.csv", flush=True)
