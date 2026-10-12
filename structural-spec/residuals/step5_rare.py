"""Step 5: rare feature census across the residual set."""
import pickle, sqlite3, csv
from collections import Counter, defaultdict

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
OUT = '/home/hatch/workspace/quipu-analysis/residuals/'

def main():
    with open(OUT + 'residual_feats.pkl', 'rb') as fh:
        res = pickle.load(fh)
    kids = [r['khipu_id'] for r in res]
    kset = set(kids)
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    rows = []  # (khipu_id, feature, detail, count)

    # 1. rare knot types per khipu
    c.execute('''SELECT co.KHIPU_ID, k.TYPE_CODE, COUNT(*)
                 FROM knot k JOIN cord co ON k.CORD_ID=co.CORD_ID
                 WHERE k.TYPE_CODE IN ('SP','TF','LL','BL','EE')
                 GROUP BY co.KHIPU_ID, k.TYPE_CODE''')
    for khipu_id, tcode, n in c.fetchall():
        if str(khipu_id) in kset:
            rows.append((khipu_id, f'rare-knot-{tcode}', f'{n} knots', n))

    # 2. twist direction anomalies: khipu-level direction mix
    c.execute('''SELECT co.KHIPU_ID, k.DIRECTION, COUNT(*)
                 FROM knot k JOIN cord co ON k.CORD_ID=co.CORD_ID
                 WHERE k.DIRECTION IN ('S','U','Z')
                 GROUP BY co.KHIPU_ID, k.DIRECTION''')
    dirmix = defaultdict(Counter)
    for khipu_id, d, n in c.fetchall():
        dirmix[str(khipu_id)][d] += n
    for kid in kids:
        m = dirmix.get(kid, Counter())
        tot = sum(m.values())
        if tot == 0: continue
        # unusual: >80% U, or >50% S (non-funerary set), or mixed S+U without Z
        if m['U']/tot > 0.8:
            rows.append((kid, 'twist-U-dominant', f"U={m['U']/tot:.0%}", m['U']))
        elif m['S']/tot > 0.5:
            rows.append((kid, 'twist-S-dominant', f"S={m['S']/tot:.0%}", m['S']))
        elif m['S'] > 0 and m['U'] > 0 and m['Z'] == 0:
            rows.append((kid, 'twist-SU-noZ', f"S={m['S']},U={m['U']}", m['S']+m['U']))

    # 3. cord-level twist field anomalies (cord.TWIST unusual values)
    c.execute('''SELECT KHIPU_ID, TWIST, COUNT(*) FROM cord
                 WHERE TWIST IS NOT NULL AND TWIST != ''
                 GROUP BY KHIPU_ID, TWIST''')
    twistvals = Counter()
    for khipu_id, t, n in c.fetchall():
        twistvals[t] += 1
    # rare twist values = appearing in <=3 khipu corpus-wide
    rare_twists = set(t for t, n in twistvals.items() if n <= 3)
    c.execute('''SELECT KHIPU_ID, TWIST, COUNT(*) FROM cord
                 WHERE TWIST IS NOT NULL AND TWIST != ''
                 GROUP BY KHIPU_ID, TWIST''')
    for khipu_id, t, n in c.fetchall():
        if str(khipu_id) in kset and t in rare_twists:
            rows.append((khipu_id, 'rare-cord-twist', t, n))

    # 4. fiber anomalies
    c.execute('''SELECT KHIPU_ID, FIBER, COUNT(*) FROM cord
                 WHERE FIBER IS NOT NULL AND FIBER != ''
                 GROUP BY KHIPU_ID, FIBER''')
    fibvals = Counter()
    allfib = []
    for khipu_id, fb, n in c.fetchall():
        fibvals[fb] += 1; allfib.append((khipu_id, fb, n))
    rare_fib = set(f for f, n in fibvals.items() if n <= 3)
    for khipu_id, fb, n in allfib:
        if str(khipu_id) in kset and fb in rare_fib:
            rows.append((khipu_id, 'rare-fiber', fb, n))

    # 5. long knots with >9 turns (non-standard)
    c.execute('''SELECT co.KHIPU_ID, COUNT(*) FROM knot k JOIN cord co ON k.CORD_ID=co.CORD_ID
                 WHERE k.TYPE_CODE='L' AND k.NUM_TURNS > 9
                 GROUP BY co.KHIPU_ID''')
    for khipu_id, n in c.fetchall():
        if str(khipu_id) in kset:
            rows.append((khipu_id, 'long-knot->9-turns', f'{n} knots', n))

    # 6. empty-color cords (no color recorded)
    c.execute('''SELECT co.KHIPU_ID, COUNT(*) FROM cord co
                 LEFT JOIN ascher_cord_color cc ON co.CORD_ID=cc.CORD_ID
                 WHERE cc.COLOR_CD_1 IS NULL
                 GROUP BY co.KHIPU_ID''')
    for khipu_id, n in c.fetchall():
        if str(khipu_id) in kset and n >= 5:
            rows.append((khipu_id, 'many-uncolored-cords', f'{n} cords', n))

    # 7. deep hierarchy (>=5 levels)
    for r in res:
        if r['max_level'] and r['max_level'] >= 5:
            rows.append((r['khipu_id'], 'deep-hierarchy', f"level {r['max_level']}", r['max_level']))

    # 8. single-cord khipu / tiny khipu
    for r in res:
        if r['n_cords'] is not None and r['n_cords'] <= 3:
            rows.append((r['khipu_id'], 'tiny-khipu', f"{r['n_cords']} cords", r['n_cords']))

    with open(OUT + 'rare_features.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['khipu_id','feature','detail','count'])
        for row in sorted(rows, key=lambda x: (x[1], x[0])):
            w.writerow(row)

    # summary: do rare features cluster?
    fk = defaultdict(set)
    for kid, feat, detail, n in rows:
        fk[feat].add(kid)
    lines = ['# Rare Feature Census (residual set only)', '']
    lines.append('| Feature | N khipu affected | khipu_ids |')
    lines.append('|---|---|---|')
    for feat in sorted(fk):
        members = sorted((str(m) for m in fk[feat]), key=int)
        lines.append(f'| {feat} | {len(members)} | {", ".join(members[:10])}{"..." if len(members)>10 else ""} |')
    lines.append('')
    # khipu with multiple rare features
    km = Counter(kid for kid, feat, d, n in rows)
    lines.append('## Khipu with 3+ rare features')
    lines.append('')
    for kid, n in km.most_common():
        if n >= 3:
            feats = sorted(set(feat for k, feat, d, nn in rows if k == kid))
            lines.append(f'- {kid}: {n} features — {", ".join(feats)}')
    with open(OUT + 'rare_features.md', 'w') as f:
        f.write('\n'.join(lines) + '\n')
    print(f'wrote rare_features.csv ({len(rows)} rows), rare_features.md', flush=True)

if __name__ == '__main__':
    main()
