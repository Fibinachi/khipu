"""Classify filing-cabinet segments against type centroids; merge adjacent same-type."""
import sqlite3, json, csv, math, statistics
from collections import Counter, defaultdict

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
OUT = '/home/hatch/workspace/quipu-analysis/filing-cabinets'
TYPE_NAMES = {0x01: 'census', 0x02: 'warehouse', 0x03: 'bulk_tally',
              0x05: 'south_funerary', 0x06: 'unknown_office', 0x00: 'unclassified'}

def seg_features(conn, khipu_id, ord0, ord1):
    c = conn.cursor()
    c.execute("""
        SELECT c.CORD_ID, c.CORD_LEVEL, cc.COLOR_CD_1, cc.COLOR_CD_2
        FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
        WHERE c.KHIPU_ID = ? AND c.CORD_ORDINAL >= ? AND c.CORD_ORDINAL <= ?
    """, (khipu_id, ord0, ord1))
    rows = c.fetchall()
    if not rows:
        return None
    cids = [r[0] for r in rows]
    ph = ','.join('?' * len(cids))
    c.execute(f"SELECT CORD_ID, DIRECTION, COUNT(*) FROM knot WHERE CORD_ID IN ({ph}) GROUP BY CORD_ID, DIRECTION", cids)
    tdir = defaultdict(Counter)
    for cid, d, n in c.fetchall():
        tdir[cid][d or '?'] += n
    c.execute(f"SELECT CORD_ID, COUNT(*) FROM knot WHERE CORD_ID IN ({ph}) GROUP BY CORD_ID", cids)
    nk = dict(c.fetchall())
    n = len(rows)
    levels = [r[1] or 0 for r in rows]
    colors = [r[2] for r in rows if r[2]]
    ncolors = len(set(colors))
    white = sum(1 for col in colors if col == 'W') / max(len(colors), 1)
    comp = sum(1 for r in rows if r[3]) / n
    twists = []
    for cid in cids:
        d = tdir.get(cid, Counter())
        twists.append(d.most_common(1)[0][0] if d else '?')
    tc = Counter(twists)
    tot = max(sum(tc.values()), 1)
    sub_rate = sum(1 for l in levels if l >= 2) / n
    mags = sorted(nk.get(cid, 0) for cid in cids)
    return {
        'n_cords': n, 'max_level': max(levels), 'n_colors': ncolors,
        'white_pct': white, 'compound_pct': comp,
        'z_pct': tc.get('Z', 0) / tot, 's_pct': tc.get('S', 0) / tot,
        'u_pct': tc.get('U', 0) / tot,
        'subsidiary_rate': sub_rate, 'med_knotcount': mags[len(mags)//2],
    }

def classify(fv, centroids, stats, keys):
    if fv is None:
        return 0x00, 0.0
    zv = {k: (fv[k] - stats[k][0]) / stats[k][1] for k in keys}
    dists = {}
    for tcode, cinfo in centroids.items():
        d2 = sum((zv[k] - (cinfo['centroid'][k] - stats[k][0]) / stats[k][1]) ** 2 for k in keys)
        dists[int(tcode)] = math.sqrt(d2)
    best = min(dists, key=dists.get)
    srt = sorted(dists.values())
    conf = 1 - srt[0] / max(srt[1], 1e-9) if len(srt) > 1 else 1.0
    # distance gate: too far from everything -> unclassified
    if srt[0] > 3.0:
        return 0x00, 0.0
    return best, round(conf, 2)

def main():
    conn = sqlite3.connect(DB)
    pack = json.load(open(f'{OUT}/centroids.json'))
    centroids, stats, keys = pack['centroids'], pack['stats'], pack['feat_keys']
    segs = json.load(open(f'{OUT}/segments_raw.json'))

    classified = []  # (khipu_id, seg_idx, ord0, ord1, nL1, score, evidence, type, conf, n_cords)
    for entry in segs:
        kid = entry['khipu_id']
        for si, s in enumerate(entry['segments']):
            if len(s) == 5:
                ord0, ord1, nL1, score, ev = s
            else:
                ord0, ord1, ev, score, _ = s[0], s[1], s[4], s[3], None
                nL1 = s[2]
            fv = seg_features(conn, kid, ord0, ord1)
            tcode, conf = classify(fv, centroids, stats, keys)
            n_cords = fv['n_cords'] if fv else 0
            classified.append([kid, si, ord0, ord1, nL1, n_cords, tcode, conf, score, ev])

    # merge adjacent same-type segments within each khipu
    merged = []
    for kid in sorted(set(c[0] for c in classified), key=int):
        ks = sorted([c for c in classified if c[0] == kid], key=lambda c: c[1])
        cur = None
        for c in ks:
            if cur and cur[6] == c[6] and c[6] != 0x00:
                # merge: extend ord1, sum cords, min conf
                cur[3] = c[3]
                cur[5] += c[5]
                cur[7] = round(min(cur[7], c[7]), 2)
                cur[9] = cur[9] + ' + ' + c[9]
            else:
                if cur:
                    merged.append(cur)
                cur = list(c)
        if cur:
            merged.append(cur)

    with open(f'{OUT}/segments.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['khipu_id','segment_num','cord_start','cord_end','n_l1','n_cords',
                    'assigned_type','type_code','confidence','boundary_score','boundary_evidence'])
        for m in merged:
            kid, si, ord0, ord1, nL1, nc, tcode, conf, score, ev = m
            w.writerow([kid, si, ord0, ord1, nL1, nc, TYPE_NAMES[tcode],
                        hex(tcode), conf, score, ev])

    # cabinet summary
    with open(f'{OUT}/cabinet_summary.csv', 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['khipu_id','n_documents','types_present','n_unclassified_segments','n_cords_total'])
        for kid in sorted(set(m[0] for m in merged), key=int):
            ks = [m for m in merged if m[0] == kid]
            types = sorted(set(TYPE_NAMES[m[6]] for m in ks))
            n_un = sum(1 for m in ks if m[6] == 0x00)
            w.writerow([kid, len(ks), ';'.join(types), n_un, sum(m[5] for m in ks)])

    # stats
    tc = Counter(TYPE_NAMES[m[6]] for m in merged)
    print("segment type distribution (after merge):")
    for t, n in tc.most_common():
        print(f"  {t}: {n}")
    print(f"total documents: {len(merged)} from 172 khipu")
    n_single = sum(1 for kid in set(m[0] for m in merged)
                   if len([m for m in merged if m[0]==kid]) == 1)
    print(f"khipu that are single documents: {n_single}/172")

if __name__ == '__main__':
    main()
