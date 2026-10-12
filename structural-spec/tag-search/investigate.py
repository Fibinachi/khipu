"""Deep-investigate the 5 all-three-marker khipu: sectional structure, shared
signatures, contexts. Writes top_candidates.md sections and tag concordance."""
import sqlite3, csv, json
from collections import Counter, defaultdict
import os

OUT = os.path.expanduser('~/workspace/quipu-analysis/tag-search')
DB = os.path.expanduser('~/workspace/quipu-analysis/okr-khipu.db')
conn = sqlite3.connect(DB)
conn.execute('PRAGMA journal_mode=OFF')
c = conn.cursor()

CANDS = [1000331, 1000396, 1000507, 1000321, 1000659]

# Load per-khipu ordered sequences with full signatures
def load_seq(kid):
    c.execute('''
        SELECT cord.CORD_ID, cord.CORD_ORDINAL, cc.COLOR_CD_1, cc.COLOR_CD_2
        FROM cord LEFT JOIN ascher_cord_color cc ON cord.CORD_ID = cc.CORD_ID
        WHERE cord.KHIPU_ID = ? ORDER BY cord.CORD_ORDINAL
    ''', (kid,))
    seen = {}
    for cid, o, c1, c2 in c.fetchall():
        if cid not in seen:
            seen[cid] = (o if o is not None else 0, c1 or '?', c2 or '')
    items = sorted(seen.items(), key=lambda kv: kv[1][0])
    out = []
    for cid, (o, c1, c2) in items:
        c2c = conn.cursor()
        c2c.execute('''SELECT TYPE_CODE, DIRECTION, COUNT(*) FROM knot
                       WHERE CORD_ID=? GROUP BY TYPE_CODE, DIRECTION
                       ORDER BY COUNT(*) DESC LIMIT 1''', (cid,))
        kr = c2c.fetchone()
        kt, tw = (kr[0] or '?', kr[1] or '?') if kr else ('?', '?')
        out.append({'ordinal': o, 'sig': (c1, c2, kt, tw), 'color': c1})
    return out

ref_sigs = json.load(open(f'{OUT}/ref_1000331_signatures.json'))
ref_set = set(tuple(k) for k, v in ref_sigs)

report = []
concord = []  # (sig, khipu, n, contexts)

for kid in CANDS:
    seq = load_seq(kid)
    sigs = [x['sig'] for x in seq]
    shared = [s for s in sigs if s in ref_set]
    # sectional structure: split at AB->BG
    cols = [x['color'] for x in seq]
    n_abbg = sum(1 for i in range(len(cols)-1) if cols[i]=='AB' and cols[i+1]=='BG')
    n_www = sum(1 for i in range(len(cols)-2)
                if cols[i]=='W' and cols[i+1]=='W' and cols[i+2]=='W')
    # value profile via quick decode count
    n_total = len(seq)
    uniq_shared = sorted(set(shared), key=lambda s: -sum(1 for x in sigs if x==s))
    c.execute('SELECT PROVENANCE, REGION, MUSEUM_NAME, MUSEUM_NUM, NOTES FROM khipu_main WHERE KHIPU_ID=?', (kid,))
    prow = c.fetchone()
    report.append({
        'khipu_id': kid, 'n_cords': n_total,
        'n_signatures': len(set(sigs)),
        'n_shared_sigs': len(set(shared)),
        'shared_cord_frac': round(len(shared)/n_total, 3) if n_total else 0,
        'n_ABBG': n_abbg, 'n_WWW': n_www,
        'top_shared': ['/'.join(s) for s in uniq_shared[:8]],
        'provenance': (prow[0] or '') if prow else '',
        'region': (prow[1] or '') if prow else '',
        'museum': (prow[2] or '') if prow else '',
    })
    # concordance entries for shared sigs
    cnt = Counter(shared)
    for sig, n in cnt.most_common(12):
        # neighbors of first few occurrences
        idxs = [i for i, s in enumerate(sigs) if s == sig][:4]
        ctx = []
        for i in idxs:
            pre = '/'.join(sigs[i-1]) if i > 0 else 'START'
            nxt = '/'.join(sigs[i+1]) if i < len(sigs)-1 else 'END'
            ctx.append(f'{pre} [{"/".join(sig)}] {nxt}')
        concord.append({
            'signature': '/'.join(sig), 'khipu_id': kid, 'n': n,
            'contexts': ' | '.join(ctx),
        })

with open(f'{OUT}/candidate_profiles.json', 'w') as f:
    json.dump(report, f, indent=1)
with open(f'{OUT}/tag_concordance.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['signature','khipu_id','n','contexts'])
    w.writeheader(); w.writerows(concord)

for r in report:
    print(f"== {r['khipu_id']} ==")
    print(f"  cords={r['n_cords']} sigs={r['n_signatures']} shared_sigs={r['n_shared_sigs']} "
          f"shared_frac={r['shared_cord_frac']} ABBG={r['n_ABBG']} WWW={r['n_WWW']}")
    print(f"  top shared: {r['top_shared']}")
    print(f"  {r['provenance']} / {r['museum']}")
conn.close()
print('wrote candidate_profiles.json, tag_concordance.csv')
