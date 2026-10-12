"""Triangulation: for each shared signature, compare structural role across the
5 all-three-marker khipu. Also verify AB+BG in 1000321 and check sectional
structure of 1000396 (closest match)."""
import sqlite3, json
from collections import Counter
import os

OUT = os.path.expanduser('~/workspace/quipu-analysis/tag-search')
DB = os.path.expanduser('~/workspace/quipu-analysis/okr-khipu.db')
conn = sqlite3.connect(DB)
c = conn.cursor()

def load_seq(kid):
    c.execute('''
        SELECT cord.CORD_ID, cord.CORD_ORDINAL, cc.COLOR_CD_1, cc.COLOR_CD_2
        FROM cord LEFT JOIN ascher_cord_color cc ON cord.CORD_ID = cc.CORD_ID
        WHERE cord.KHIPU_ID = ? ORDER BY cord.CORD_ORDINAL, cc.COLOR_CD_1
    ''', (kid,))
    seen = {}
    for cid, o, c1, c2 in c.fetchall():
        if cid not in seen:
            seen[cid] = (o if o is not None else 0, c1 or '?', c2 or '')
    items = sorted(seen.items(), key=lambda kv: kv[1][0])
    out = []
    for cid, (o, c1, c2) in items:
        cc2 = conn.cursor()
        cc2.execute('''SELECT TYPE_CODE, DIRECTION FROM knot WHERE CORD_ID=?
                       GROUP BY TYPE_CODE, DIRECTION ORDER BY COUNT(*) DESC LIMIT 1''', (cid,))
        kr = cc2.fetchone()
        kt, tw = (kr[0] or '?', kr[1] or '?') if kr else ('?', '?')
        out.append({'ordinal': o, 'sig': (c1, c2, kt, tw), 'color': c1})
    return out

CANDS = [1000331, 1000396, 1000507, 1000321, 1000659]
seqs = {k: load_seq(k) for k in CANDS}

print("=== 1. AB+BG verification in 1000321 (color1, deterministic order) ===")
cols = [x['color'] for x in seqs[1000321]]
hits = [i for i in range(len(cols)-1) if cols[i]=='AB' and cols[i+1]=='BG']
print(f"AB->BG adjacencies: {len(hits)} at idx {hits[:10]}")
# also check color2 for BG compounds
c.execute('''SELECT cord.CORD_ORDINAL, cc.COLOR_CD_1, cc.COLOR_CD_2 FROM cord
             JOIN ascher_cord_color cc ON cord.CORD_ID=cc.CORD_ID
             WHERE cord.KHIPU_ID=1000321 AND (cc.COLOR_CD_1='BG' OR cc.COLOR_CD_2='BG')
             ORDER BY cord.CORD_ORDINAL LIMIT 20''')
print("BG-involved cords in 1000321:", c.fetchall()[:20])

print()
print("=== 2. Role of shared tags per khipu: position of MB/* near AB+BG ===")
for kid in CANDS:
    seq = seqs[kid]
    cols = [x['color'] for x in seq]
    # find AB+BG positions
    abbg_idx = [i+1 for i in range(len(cols)-1) if cols[i]=='AB' and cols[i+1]=='BG']
    # for each MB cord, distance to nearest ABBG
    mb_dists = []
    for i, x in enumerate(seq):
        if x['color'] == 'MB':
            d = min([abs(i-j) for j in abbg_idx], default=None)
            if d is not None: mb_dists.append(d)
    if mb_dists:
        print(f"{kid}: n_MB={[x['color'] for x in seq].count('MB')}, "
              f"median dist MB->ABBG = {sorted(mb_dists)[len(mb_dists)//2]}, "
              f"frac within 4 = {sum(1 for d in mb_dists if d<=4)/len(mb_dists):.2f}")
    else:
        print(f"{kid}: no MB cords")

print()
print("=== 3. BG two-type split detail per khipu ===")
for kid in CANDS:
    seq = seqs[kid]
    e_z = [(x['ordinal']) for x in seq if x['sig'][0]=='BG' and x['sig'][2]=='E' and x['sig'][3]=='Z']
    l_s = [(x['ordinal']) for x in seq if x['sig'][0]=='BG' and x['sig'][2]=='L' and x['sig'][3]=='S']
    other = [(x['ordinal'], x['sig']) for x in seq if x['sig'][0]=='BG' and not (
        (x['sig'][2]=='E' and x['sig'][3]=='Z') or (x['sig'][2]=='L' and x['sig'][3]=='S'))]
    print(f"{kid}: BG E/Z at {e_z[:8]} | BG L/S at {l_s[:8]} | other BG: {other[:6]}")

print()
print("=== 4. 1000396 sectional structure (split at AB+BG) ===")
seq = seqs[1000396]
cols = [x['color'] for x in seq]
sections, cur = [], []
for x in seq:
    cur.append(x)
    if len(cur) >= 2 and cur[-2]['color']=='AB' and cur[-1]['color']=='BG':
        sections.append(cur); cur = []
if cur: sections.append(cur)
print(f"{len(sections)} sections")
for i, s in enumerate(sections):
    cc = Counter(x['color'] for x in s)
    print(f"  sec{i+1}: {len(s)} cords, ord {s[0]['ordinal']}-{s[-1]['ordinal']}, top colors {cc.most_common(4)}")

print()
print("=== 5. Shared-signature role comparison: is AB//L/S the carrier everywhere? ===")
for kid in CANDS:
    seq = seqs[kid]
    tot = len(seq)
    for sigstr in ['AB//L/S', 'W//L/S', 'MB//L/S']:
        parts = sigstr.split('/')
        n = sum(1 for x in seq if x['sig'][0]==parts[0] and x['sig'][2]==parts[2] and x['sig'][3]==parts[3])
        print(f"  {kid} {sigstr}: {n}/{tot} ({100*n/tot:.1f}%)")
conn.close()
