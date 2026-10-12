"""Build full cord-signature profiles for every khipu and score overlap with 1000331.
Signature = (color1, color2, dominant_knot_type, dominant_twist).
Runs in background; writes CSVs to ~/workspace/quipu-analysis/tag-search/.
"""
import sqlite3, csv, json
from collections import Counter, defaultdict
import os

OUT = os.path.expanduser('~/workspace/quipu-analysis/tag-search')
os.makedirs(OUT, exist_ok=True)
DB = os.path.expanduser('~/workspace/quipu-analysis/okr-khipu.db')

conn = sqlite3.connect(DB)
conn.execute('PRAGMA journal_mode=OFF')
c = conn.cursor()

print('Loading cords...', flush=True)
# cord_id -> (khipu_id, ordinal, color1, color2)
c.execute('''
    SELECT cord.CORD_ID, cord.KHIPU_ID, cord.CORD_ORDINAL,
           cc.COLOR_CD_1, cc.COLOR_CD_2
    FROM cord LEFT JOIN ascher_cord_color cc ON cord.CORD_ID = cc.CORD_ID
''')
cords = {}
for cid, kid, ordinal, c1, c2 in c.fetchall():
    # keep first color row per cord (primary)
    if cid not in cords:
        cords[cid] = (kid, ordinal, c1 or '?', c2 or '')

print(f'{len(cords)} cords', flush=True)
print('Loading knots...', flush=True)
# dominant knot type/direction per cord
c.execute('''
    SELECT CORD_ID, TYPE_CODE, DIRECTION, COUNT(*) as n
    FROM knot GROUP BY CORD_ID, TYPE_CODE, DIRECTION
''')
best = {}
for cid, t, d, n in c.fetchall():
    t = t or '?'; d = d or '?'
    if cid not in best or n > best[cid][2]:
        best[cid] = (t, d, n)

print('Building signatures...', flush=True)
# khipu -> Counter of signatures; khipu -> ordered list of (ordinal, sig)
khipu_sigs = defaultdict(Counter)
khipu_seq = defaultdict(list)
for cid, (kid, ordinal, c1, c2) in cords.items():
    kt, tw = best.get(cid, ('?', '?'))[:2]
    sig = (c1, c2, kt, tw)
    khipu_sigs[kid][sig] += 1
    khipu_seq[kid].append((ordinal if ordinal is not None else 0, sig))

for kid in khipu_seq:
    khipu_seq[kid].sort()

# 1000331 reference
REF = 1000331
ref_counter = khipu_sigs[REF]
ref_set = set(ref_counter)
print(f'1000331: {len(ref_set)} distinct signatures, {sum(ref_counter.values())} cords', flush=True)
with open(f'{OUT}/ref_1000331_signatures.json', 'w') as f:
    json.dump([[list(k), v] for k, v in ref_counter.most_common()], f)

# Overlap scoring
rows = []
for kid, counter in khipu_sigs.items():
    s = set(counter)
    inter = s & ref_set
    union = s | ref_set
    jaccard = len(inter) / len(union) if union else 0
    # weighted: sum of ref frequencies for shared sigs, normalized by ref total
    ref_total = sum(ref_counter.values())
    weighted = sum(ref_counter[sig] for sig in inter) / ref_total if ref_total else 0
    rows.append({
        'khipu_id': kid,
        'n_cords': sum(counter.values()),
        'n_signatures': len(s),
        'n_shared': len(inter),
        'jaccard': round(jaccard, 4),
        'weighted_overlap': round(weighted, 4),
    })

rows.sort(key=lambda r: -(r['weighted_overlap'] + r['jaccard']))

# Check AB+BG compound and WWW triplet in sequences
def has_ab_bg(seq):
    cols = [sg[0] for _, sg in seq]
    return any(cols[i] == 'AB' and cols[i+1] == 'BG' for i in range(len(cols)-1))

def has_www(seq):
    cols = [sg[0] for _, sg in seq]
    return any(cols[i] == 'W' and cols[i+1] == 'W' and cols[i+2] == 'W'
               for i in range(len(cols)-2))

# BG two-type split: both (BG,'','L','S') and (BG,'','E','Z') present
def has_bg_split(s):
    return ('BG','','L','S') in s and ('BG','','E','Z') in s

# provenance
c.execute('SELECT KHIPU_ID, PROVENANCE, REGION, MUSEUM_NAME FROM khipu_main')
prov = {r[0]: (r[1] or '', r[2] or '', r[3] or '') for r in c.fetchall()}

for r in rows:
    kid = r['khipu_id']
    seq = khipu_seq[kid]
    s = set(khipu_sigs[kid])
    r['has_AB_BG'] = int(has_ab_bg(seq))
    r['has_WWW'] = int(has_www(seq))
    r['has_BG_split'] = int(has_bg_split(s))
    p, rg, mu = prov.get(kid, ('', '', ''))
    r['provenance'] = p; r['region'] = rg; r['museum'] = mu
    # combined score
    r['combined'] = round(r['weighted_overlap'] + r['jaccard']
                          + 0.3*r['has_AB_BG'] + 0.2*r['has_WWW']
                          + 0.2*r['has_BG_split'], 4)

rows.sort(key=lambda r: -r['combined'])

with open(f'{OUT}/overlap_scores.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['khipu_id','n_cords','n_signatures','n_shared',
        'jaccard','weighted_overlap','has_AB_BG','has_WWW','has_BG_split',
        'combined','provenance','region','museum'])
    w.writeheader(); w.writerows(rows)

# signature profiles
with open(f'{OUT}/signature_profiles.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['khipu_id','n_cords','n_signatures','top_5_signatures'])
    for kid, counter in sorted(khipu_sigs.items()):
        top5 = '; '.join(f"{'/'.join(k)}:{v}" for k, v in counter.most_common(5))
        w.writerow([kid, sum(counter.values()), len(counter), top5])

print(f'Done. {len(rows)} khipu scored. Top 15:', flush=True)
for r in rows[:15]:
    print(f"  {r['khipu_id']}: combined={r['combined']} jacc={r['jaccard']} "
          f"w={r['weighted_overlap']} ABBG={r['has_AB_BG']} WWW={r['has_WWW']} "
          f"BGS={r['has_BG_split']} n_sig={r['n_signatures']} {r['provenance']}", flush=True)
conn.close()
