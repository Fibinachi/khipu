"""Re-screen .flat khipu with compound-aware and divider-aware segmentation."""
import sqlite3
from collections import Counter, defaultdict

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

# Get .flat khipu from spreadsheet index
# Get .flat khipu from spreadsheet index CSV
import csv
flat_ids = []
with open('/home/hatch/workspace/quipu-analysis/spreadsheets/spreadsheet_index.csv') as f:
    for row in csv.DictReader(f):
        if row['format'] == '.flat':
            flat_ids.append(int(row['khipu_id']))
print(f"{len(flat_ids)} .flat khipu to screen")

def get_seq(khipu_id):
    c.execute("""
        SELECT c.CORD_ORDINAL, cc.COLOR_CD_1 FROM cord c
        LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
        WHERE c.KHIPU_ID=? ORDER BY c.CORD_ORDINAL
    """, (khipu_id,))
    seen = {}
    for o, col in c.fetchall():
        if o not in seen:
            seen[o] = (col or '?').strip()
    return [seen[o] for o in sorted(seen.keys())]

def find_compounds(seq):
    """Find strongly directional color pairs (A->B common, B->A rare/absent)."""
    pairs = Counter()
    for i in range(len(seq)-1):
        pairs[(seq[i], seq[i+1])] += 1
    compounds = []
    for (a, b), n in pairs.items():
        if a == b or n < 3:
            continue
        rev = pairs.get((b, a), 0)
        # directional if forward >= 3x reverse and forward >= 5
        if n >= 5 and n >= 3 * max(rev, 1):
            compounds.append((a, b, n, rev))
    return sorted(compounds, key=lambda x: -x[2])

def find_dividers(seq, min_len=4, max_len=8):
    """Find repeated multi-cord signatures that could be dividers."""
    dividers = []
    for L in range(min_len, max_len+1):
        ngrams = Counter()
        for i in range(len(seq)-L+1):
            ngrams[tuple(seq[i:i+L])] += 1
        for ng, count in ngrams.items():
            if count >= 3 and len(set(ng)) > 1:  # repeated, not monochromatic
                dividers.append((ng, count, L))
    return sorted(dividers, key=lambda x: (-x[1], -x[2]))[:5]

results = []
for kid in flat_ids:
    seq = get_seq(kid)
    if len(seq) < 10:
        continue
    compounds = find_compounds(seq)
    dividers = find_dividers(seq)
    # Heuristic: if it has strong compounds OR clear dividers, flag for review
    score = len(compounds) * 2 + len([d for d in dividers if d[1] >= 4])
    if score > 0:
        results.append((kid, len(seq), compounds[:3], dividers[:2], score))

results.sort(key=lambda x: -x[4])
print(f"\n{len(results)} .flat khipu show compound/divider signals\n")
for kid, n, comps, divs, score in results[:30]:
    print(f"Khipu {kid} ({n} cords, score {score}):")
    for a, b, fwd, rev in comps:
        print(f"  compound: {a}->{b} ({fwd}x, reverse {rev}x)")
    for ng, cnt, L in divs:
        print(f"  divider: {' '.join(ng)} ({cnt}x, len {L})")
    print()

# Save full results
with open('/home/hatch/workspace/quipu-analysis/rescreen_flat.csv', 'w') as f:
    f.write("khipu_id,n_cords,score,n_compounds,n_dividers\n")
    for kid, n, comps, divs, score in results:
        f.write(f"{kid},{n},{score},{len(comps)},{len(divs)}\n")
print(f"Saved {len(results)} candidates to rescreen_flat.csv")
