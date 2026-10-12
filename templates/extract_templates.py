"""Corpus-wide form template extraction.

Stage 1: bulk decode all cords -> templates/cache.pkl
Stage 2: row segmentation per khipu -> templates/row_segmentation.csv
Stage 3: template extraction -> templates/template_signatures.csv
Stage 4: template clustering (exact + fuzzy) -> templates/template_catalog.csv
Stage 5: report -> templates/template_report.md
"""
import sqlite3, pickle, csv, os, sys, time
from collections import Counter, defaultdict

sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from decoder import decode_cord

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
OUT = '/home/hatch/workspace/quipu-analysis/templates'
os.makedirs(OUT, exist_ok=True)
CACHE = os.path.join(OUT, 'cache.pkl')

def load_khipu_ids():
    ids = []
    with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
        for line in f:
            if line.startswith('#') or line.startswith('KHIPU'):
                continue
            ids.append(line.split(',')[0].strip())
    return ids

def stage1_decode():
    if os.path.exists(CACHE):
        print('cache exists, loading', flush=True)
        with open(CACHE, 'rb') as f:
            return pickle.load(f)
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    data = {}  # kid -> list of (ordinal, level, c1, c2, value)
    c.execute('SELECT DISTINCT KHIPU_ID FROM cord')
    kids = [r[0] for r in c.fetchall()]
    kids = [str(k) for k in kids]
    t0 = time.time()
    n = 0
    for ki, kid in enumerate(kids):
        c2 = conn.cursor()
        c2.execute('''SELECT cord.CORD_ID, cord.CORD_ORDINAL, cord.CORD_LEVEL,
                      cc.COLOR_CD_1, cc.COLOR_CD_2
                      FROM cord LEFT JOIN ascher_cord_color cc ON cord.CORD_ID=cc.CORD_ID
                      WHERE cord.KHIPU_ID=? ORDER BY cord.CORD_ORDINAL''', (kid,))
        seen = {}
        for cid, o, lvl, c1, c2c in c2.fetchall():
            if o not in seen:
                seen[o] = (cid, lvl or 1, (c1 or '?').strip(), (c2c or '').strip())
        rows = []
        for o in sorted(seen.keys()):
            cid, lvl, c1, c2c = seen[o]
            try:
                v = decode_cord(conn, cid)['value']
            except Exception:
                v = None
            rows.append((o, lvl, c1, c2c, v))
            n += 1
        data[kid] = rows
        if (ki+1) % 50 == 0:
            print(f'  decoded {ki+1}/{len(kids)} khipu, {n} cords, {time.time()-t0:.0f}s', flush=True)
    conn.close()
    with open(CACHE, 'wb') as f:
        pickle.dump(data, f)
    print(f'stage1 done: {n} cords in {time.time()-t0:.0f}s', flush=True)
    return data

def detect_cycle(seq):
    """Find dominant color cycle. Returns (cycle_list, coverage) or (None, 0)."""
    if len(seq) < 8:
        return None, 0
    bigram = Counter()
    for i in range(len(seq)-1):
        bigram[(seq[i], seq[i+1])] += 1
    total = sum(bigram.values())
    # build deterministic chain from most common bigram
    if not bigram:
        return None, 0
    (a, b), _ = bigram.most_common(1)[0]
    # next map: for each color, most common follower
    nxt = defaultdict(Counter)
    for (x, y), n in bigram.items():
        nxt[x][y] += n
    chain = [a]
    seen_c = {a}
    cur = a
    for _ in range(8):
        if cur not in nxt or not nxt[cur]:
            break
        nb = nxt[cur].most_common(1)[0][0]
        if nb == a and len(chain) >= 2:
            chain.append(nb)
            break
        if nb in seen_c:
            break
        chain.append(nb)
        seen_c.add(nb)
        cur = nb
    # chain must be a cycle: last == first, length>=3
    if len(chain) >= 3 and chain[-1] == chain[0]:
        cyc = chain[:-1]
        # coverage: fraction of bigrams consistent with cycle
        cyc_bigrams = set((cyc[i], cyc[(i+1) % len(cyc)]) for i in range(len(cyc)))
        cov = sum(n for (x, y), n in bigram.items() if (x, y) in cyc_bigrams) / total
        if cov > 0.60 and len(cyc) <= 8:
            return cyc, cov
    return None, 0

def detect_value_marker(rows):
    """Find (color, value) repeating at regular ordinal intervals. Returns (color, value, median_gap)."""
    # rows: list of (ordinal, level, c1, c2, value)
    pos = defaultdict(list)
    for (o, lvl, c1, c2, v) in rows:
        if v is not None and v != 0:
            pos[(c1, v)].append(o)
    best = None
    for (c1, v), occ in pos.items():
        if len(occ) >= 3:
            gaps = [occ[i+1]-occ[i] for i in range(len(occ)-1)]
            gaps.sort()
            med = gaps[len(gaps)//2]
            # regularity: most gaps within 30% of median
            reg = sum(1 for g in gaps if abs(g-med) <= max(2, 0.3*med)) / len(gaps)
            if reg >= 0.6 and med >= 4:
                score = len(occ) * reg
                if best is None or score > best[0]:
                    best = (score, c1, v, med)
    if best:
        return best[1], best[2], best[3]
    return None

def segment_rows(kid, rows):
    """Returns (method, row_list, info). row_list = list of lists of (ordinal, level, c1, c2, value)."""
    seq = [r[2] for r in rows]  # colors
    cyc, cov = detect_cycle(seq)
    if cyc:
        # pivot: new row at each cycle[0] that follows cycle[-1]; fallback every cycle[0]
        c0 = cyc[0]
        clast = cyc[-1]
        row_list, cur = [], []
        for r in rows:
            col = r[2]
            if col == c0 and cur:
                # check previous color was clast (proper completion) or just split
                prev_col = cur[-1][2]
                row_list.append(cur)
                cur = []
            cur.append(r)
        if cur:
            row_list.append(cur)
        # drop tiny leading fragment (< half cycle) if more than 2 rows
        if len(row_list) > 2 and len(row_list[0]) < len(cyc)//2:
            row_list = row_list[1:]
        if len(row_list) >= 3:
            return 'color_cycle', row_list, {'cycle': '>'.join(cyc), 'coverage': round(cov, 3)}
    vm = detect_value_marker(rows)
    if vm:
        c1m, vmv, med = vm
        marks = [r[0] for r in rows if r[2] == c1m and r[4] == vmv]
        row_list, cur = [], []
        markset = set(marks)
        for r in rows:
            if r[0] in markset and cur:
                row_list.append(cur)
                cur = []
            cur.append(r)
        if cur:
            row_list.append(cur)
        if len(row_list) >= 3:
            return 'value_marker', row_list, {'marker': f'{c1m}={vmv}', 'median_gap': med}
    # journal-style: white runs >=3 as dividers
    row_list, cur = [], []
    i = 0
    ords = rows
    while i < len(ords):
        run = 0
        j = i
        while j < len(ords) and ords[j][2] == 'W':
            run += 1
            j += 1
        if run >= 3:
            if cur:
                row_list.append(cur)
                cur = []
            i = j
        else:
            cur.append(ords[i])
            i += 1
    if cur:
        row_list.append(cur)
    if len(row_list) >= 3 and sum(len(r) for r in row_list) / len(row_list) >= 5:
        return 'white_dividers', row_list, {}
    return 'none', [], {}

def extract_template(row_list):
    """row_list: list of rows, each row list of (ordinal, level, c1, c2, value).
    Returns signature tuple of (pos, color, kind, const_value)."""
    maxlen = max(len(r) for r in row_list)
    n = len(row_list)
    sig = []
    for p in range(maxlen):
        cells = []
        for r in row_list:
            if p < len(r):
                cells.append((r[p][2], r[p][4]))
        if not cells:
            continue
        colors = Counter(c for c, v in cells)
        vals = Counter(v for c, v in cells if v is not None)
        dom_c, nc = colors.most_common(1)[0]
        frac_c = nc / len(cells)
        if vals:
            dom_v, nv = vals.most_common(1)[0]
            frac_v = nv / len([1 for c, v in cells if v is not None])
        else:
            dom_v, frac_v = None, 0
        if p == 0:
            kind = 'MARKER'
        elif frac_c >= 0.8 and frac_v >= 0.8 and dom_v is not None:
            kind = 'CONST'
        elif frac_c >= 0.8:
            kind = 'VAR'
        else:
            kind = 'MIXED'
        sig.append((p, dom_c, kind, dom_v if kind == 'CONST' else None))
    return tuple(sig)

def fuzzy_key(sig):
    """Same structure ignoring constant values: (len, tuple((pos,color,kind)))."""
    return (len(sig), tuple((p, c, k) for p, c, k, v in sig))

def main():
    data = stage1_decode()
    ids = load_khipu_ids()
    conn = sqlite3.connect(DB)

    # cluster + provenance lookup
    clus = {}
    with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
        for line in f:
            if line.startswith('#') or line.startswith('KHIPU'):
                continue
            p = line.strip().split(',')
            clus[p[0]] = p[2]
    prov = {}
    c0 = conn.cursor()
    for kid in ids:
        c0.execute('SELECT PROVENANCE, REGION, MUSEUM_NAME FROM khipu_main WHERE KHIPU_ID=?', (kid,))
        r = c0.fetchone()
        prov[kid] = r if r else ('', '', '')

    # Stage 2+3
    seg_rows = []
    sigs = {}
    for kid in ids:
        rows = data.get(kid, [])
        if len(rows) < 12:
            seg_rows.append((kid, 'none', 0, 'too_few_cords', ''))
            continue
        method, row_list, info = segment_rows(kid, rows)
        seg_rows.append((kid, method, len(row_list), str(info.get('cycle', info.get('marker', ''))), str(info)))
        if method != 'none' and len(row_list) >= 3:
            sigs[kid] = extract_template(row_list)

    with open(os.path.join(OUT, 'row_segmentation.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['khipu_id', 'method', 'n_rows', 'cycle_or_marker', 'info'])
        w.writerows(seg_rows)

    # Stage 4: cluster
    exact_groups = defaultdict(list)
    fuzzy_groups = defaultdict(list)
    for kid, sig in sigs.items():
        exact_groups[sig].append(kid)
        fuzzy_groups[fuzzy_key(sig)].append(kid)

    # assign template ids
    exact_id, fuzzy_id = {}, {}
    for i, (sig, members) in enumerate(sorted(exact_groups.items(), key=lambda x: -len(x[1]))):
        tid = f'T{i+1:03d}'
        for m in members:
            exact_id[m] = tid
    for i, (fk, members) in enumerate(sorted(fuzzy_groups.items(), key=lambda x: -len(x[1]))):
        tid = f'F{i+1:03d}'
        for m in members:
            fuzzy_id[m] = tid

    with open(os.path.join(OUT, 'template_signatures.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['khipu_id', 'n_rows', 'method', 'template_exact', 'template_fuzzy',
                    'n_const', 'n_var', 'n_marker', 'sig_len', 'cluster', 'provenance', 'region'])
        for kid, sig in sigs.items():
            kinds = Counter(k for p, c, k, v in sig)
            p0, p1, p2 = prov.get(kid, ('', '', ''))
            w.writerow([kid, next((r[2] for r in seg_rows if r[0] == kid), 0),
                        next((r[1] for r in seg_rows if r[0] == kid), ''),
                        exact_id.get(kid, ''), fuzzy_id.get(kid, ''),
                        kinds.get('CONST', 0), kinds.get('VAR', 0),
                        kinds.get('MARKER', 0), len(sig),
                        clus.get(kid, ''), p0 or '', p1 or ''])

    # catalog
    with open(os.path.join(OUT, 'template_catalog.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['template_id', 'kind', 'n_khipu', 'example_khipu', 'signature',
                    'n_const', 'n_var', 'clusters', 'top_provenances'])
        # exact templates
        for i, (sig, members) in enumerate(sorted(exact_groups.items(), key=lambda x: -len(x[1]))):
            tid = f'T{i+1:03d}'
            kinds = Counter(k for p, c, k, v in sig)
            cl = Counter(clus.get(m, '') for m in members)
            pv = Counter((prov.get(m, ('', '', ''))[0] or 'unknown') for m in members)
            sigstr = ';'.join(f'{p}:{c}:{k}' + (f'={v}' if v is not None else '') for p, c, k, v in sig)
            w.writerow([tid, 'exact', len(members), members[0], sigstr,
                        kinds.get('CONST', 0), kinds.get('VAR', 0),
                        '|'.join(f'{k}={v}' for k, v in cl.most_common(3)),
                        '|'.join(f'{k}={v}' for k, v in pv.most_common(3))])
        for i, (fk, members) in enumerate(sorted(fuzzy_groups.items(), key=lambda x: -len(x[1]))):
            tid = f'F{i+1:03d}'
            ln, parts = fk
            cl = Counter(clus.get(m, '') for m in members)
            pv = Counter((prov.get(m, ('', '', ''))[0] or 'unknown') for m in members)
            sigstr = ';'.join(f'{p}:{c}:{k}' for p, c, k in parts)
            nconst = sum(1 for p, c, k in parts if k == 'CONST')
            nvar = sum(1 for p, c, k in parts if k == 'VAR')
            w.writerow([tid, 'fuzzy', len(members), members[0], sigstr, nconst, nvar,
                        '|'.join(f'{k}={v}' for k, v in cl.most_common(3)),
                        '|'.join(f'{k}={v}' for k, v in pv.most_common(3))])

    # Stage 5: report
    n_seg = sum(1 for r in seg_rows if r[1] != 'none')
    methods = Counter(r[1] for r in seg_rows)
    report = []
    report.append('# Corpus-wide Form Template Extraction\n')
    report.append(f'Khipu analyzed: {len(ids)}; with row structure: {n_seg}; templates extracted: {len(sigs)}\n')
    report.append('## Segmentation methods\n')
    for m, n in methods.most_common():
        report.append(f'- {m}: {n}')
    report.append(f'\n## Distinct templates\n- Exact (identical signature): {len(exact_groups)}\n- Fuzzy (same structure, constants may differ): {len(fuzzy_groups)}\n')
    report.append('\n## Top 15 exact templates\n')
    report.append('| ID | n_khipu | example | n_const | n_var | clusters |')
    report.append('|---|---|---|---|---|---|')
    for i, (sig, members) in enumerate(sorted(exact_groups.items(), key=lambda x: -len(x[1]))[:15]):
        kinds = Counter(k for p, c, k, v in sig)
        cl = Counter(clus.get(m, '') for m in members)
        report.append(f'| T{i+1:03d} | {len(members)} | {members[0]} | {kinds.get("CONST",0)} | {kinds.get("VAR",0)} | {", ".join(f"{k}={v}" for k,v in cl.most_common(2))} |')
    report.append('\n## Top 15 fuzzy templates\n')
    report.append('| ID | n_khipu | example | structure_len | n_const_pos | clusters |')
    report.append('|---|---|---|---|---|---|')
    for i, (fk, members) in enumerate(sorted(fuzzy_groups.items(), key=lambda x: -len(x[1]))[:15]):
        ln, parts = fk
        nconst = sum(1 for p, c, k in parts if k == 'CONST')
        cl = Counter(clus.get(m, '') for m in members)
        report.append(f'| F{i+1:03d} | {len(members)} | {members[0]} | {ln} | {nconst} | {", ".join(f"{k}={v}" for k,v in cl.most_common(2))} |')
    # singletons
    n_single_exact = sum(1 for sig, m in exact_groups.items() if len(m) == 1)
    n_single_fuzzy = sum(1 for fk, m in fuzzy_groups.items() if len(m) == 1)
    report.append(f'\n## Singletons\n- Exact singletons (unique forms): {n_single_exact}\n- Fuzzy singletons: {n_single_fuzzy}\n')
    with open(os.path.join(OUT, 'template_report.md'), 'w') as f:
        f.write('\n'.join(report))
    print('\n'.join(report[:40]), flush=True)
    conn.close()

if __name__ == '__main__':
    main()
