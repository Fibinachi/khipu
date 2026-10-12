"""Convert every khipu in the OKR database to a CSV spreadsheet.

.tab  : khipu with row structure -> rows x color-coded columns
.flat : no row structure -> flat cord list (ordinal, level, color, value, knots)
.log  : journals -> flat list with ENTRY/DELIMITER roles
.chk  : checklists -> flat list with section info
.cod  : code khipu -> flat list

Output: ~/workspace/quipu-analysis/spreadsheets/by_khipu/{id}.csv
        + spreadsheet_index.csv + conversion_report.md
"""
import sqlite3, pickle, csv, os, sys
from collections import Counter, defaultdict

QA = '/home/hatch/workspace/quipu-analysis'
sys.path.insert(0, QA)
sys.path.insert(0, QA + '/templates')
from extract_templates import segment_rows

DB = QA + '/okr-khipu.db'
OUT = QA + '/spreadsheets'
BYKHIPU = OUT + '/by_khipu'
os.makedirs(BYKHIPU, exist_ok=True)

print('loading cache...', flush=True)
with open(QA + '/templates/cache.pkl', 'rb') as f:
    CACHE = pickle.load(f)  # kid -> [(ordinal, level, c1, c2, value)]

conn = sqlite3.connect(DB)

# ---- metadata ----
META = {}
for r in conn.execute(
        'SELECT KHIPU_ID, PROVENANCE, REGION, MUSEUM_NAME, MUSEUM_NUM, NICKNAME FROM khipu_main'):
    META[str(r[0])] = {
        'provenance': (r[1] or '').strip(),
        'region': (r[2] or '').strip(),
        'museum': (r[3] or '').strip(),
        'museum_num': (r[4] or '').strip(),
        'nickname': (r[5] or '').strip(),
    }

# ---- data regimes ----
REGIME, DOCCLUSTER = {}, {}
for r in csv.DictReader(open(QA + '/data-match/data_clusters.csv')):
    dc = r['data_cluster']
    REGIME[r['khipu_id']] = 'unclustered' if dc == '0' else 'DC' + str(dc)
    DOCCLUSTER[r['khipu_id']] = r['cluster']

# ---- template signatures ----
SIG = {}
for r in csv.DictReader(open(QA + '/templates/template_signatures.csv')):
    SIG[r['khipu_id']] = r

# ---- segmentation methods ----
SEG = {}
for r in csv.DictReader(open(QA + '/templates/row_segmentation.csv')):
    SEG[r['khipu_id']] = r

# ---- knot summaries per (khipu_id, ordinal), aggregated over all CORD_IDs sharing the ordinal ----
print('building knot summaries...', flush=True)
cid_by_ko = defaultdict(list)
for khipu_id, ordinal, cid in conn.execute(
        'SELECT KHIPU_ID, CORD_ORDINAL, CORD_ID FROM cord'):
    cid_by_ko[(str(khipu_id), ordinal)].append(cid)
knot_counts = defaultdict(Counter)
for cid, tcode in conn.execute('SELECT CORD_ID, TYPE_CODE FROM knot'):
    knot_counts[cid][(tcode or '?').strip()] += 1
KNOTSUM = {}
for (kid, o), cids in cid_by_ko.items():
    kc = Counter()
    for cid in cids:
        kc.update(knot_counts.get(cid, {}))
    KNOTSUM[(kid, o)] = ','.join(f'{t}:{n}' for t, n in sorted(kc.items())) if kc else ''

# ---- TF unary override: pure-tuft cords get tuft count as value (decoder mangles TF as decimal) ----
TF_OVERRIDE = set()
for kid, rows in CACHE.items():
    for idx, (o, lvl, c1, c2, v) in enumerate(rows):
        ks = KNOTSUM.get((kid, o), '')
        parts = ks.split(',') if ks else []
        if parts and all(p.startswith('TF:') for p in parts):
            tf_count = sum(int(p.split(':')[1]) for p in parts)
            if v != tf_count:
                rows[idx] = (o, lvl, c1, c2, tf_count)
                TF_OVERRIDE.add(kid)
print(f'TF override applied to {len(TF_OVERRIDE)} khipu', flush=True)

# ---- format overrides ----
LOGS = {'1000103', '1000368', '1000183', '1000501', '1000063'}
CODS = {'1000331', '1000396', '1000507', '1000321', '1000659'}
CHKS = {'1000522'}

def file_format(kid, method):
    if kid in LOGS:
        return '.log'
    if kid in CODS:
        return '.cod'
    if kid in CHKS:
        return '.chk'
    if method != 'none':
        return '.tab'
    return '.flat'

def meta_block(kid, fmt, method, template_id, n_rows, n_cols, extra=''):
    m = META.get(kid, {})
    lines = [
        f'# khipu_id: {kid}',
        f'# provenance: {m.get("provenance", "")}',
        f'# region: {m.get("region", "")}',
        f'# museum: {m.get("museum", "")} {m.get("museum_num", "")}'.rstrip(),
        f'# nickname: {m.get("nickname", "")}',
        f'# file_format: {fmt}',
        f'# data_regime: {REGIME.get(kid, "")}',
        f'# doc_cluster: {DOCCLUSTER.get(kid, "")}',
        f'# template_id: {template_id}',
        f'# segmentation: {method}',
        f'# n_rows: {n_rows}',
        f'# n_cols: {n_cols}',
    ]
    if extra:
        lines.append(f'# note: {extra}')
    if kid in TF_OVERRIDE:
        lines.append('# note: TF unary override - pure-tuft cord values are tuft counts, not decimal decodes')
    return lines

def white_sections(rows):
    """Map ordinal -> section id, splitting on 3+ white runs."""
    sec, cur_sec = {}, 1
    i = 0
    cur = []
    while i < len(rows):
        run = 0
        j = i
        while j < len(rows) and rows[j][2] == 'W':
            run += 1
            j += 1
        if run >= 3:
            for r in cur:
                sec[r[0]] = cur_sec
            cur_sec += 1
            cur = []
            i = j
        else:
            cur.append(rows[i])
            i += 1
    for r in cur:
        sec[r[0]] = cur_sec
    return sec

def write_tab(kid, rows, method, info):
    method_name, row_list, _ = segment_rows(kid, rows)
    # segment_rows re-detects; use its output (should match stored method)
    if not row_list:
        return None  # fall back to flat
    # value_marker: split overlong rows (e.g. leading header fragment) into
    # median-sized chunks so the positional pivot stays meaningful
    if method_name == 'value_marker' and len(row_list) > 2:
        lens = sorted(len(r) for r in row_list[1:])
        med = lens[len(lens) // 2]
        if med >= 4:
            chunked = []
            for r in row_list:
                if len(r) > 2 * med:
                    for k in range(0, len(r), med):
                        chunked.append(r[k:k + med])
                else:
                    chunked.append(r)
            row_list = chunked
    n = len(row_list)
    maxlen = max(len(r) for r in row_list)
    # per-position analysis
    col_color, col_kind = [], []
    for p in range(maxlen):
        cells = [(r[p][2], r[p][4]) for r in row_list if p < len(r)]
        colors = Counter(c for c, v in cells)
        dom_c = colors.most_common(1)[0][0]
        vals = [v for c, v in cells if v is not None]
        if p == 0 and method_name == 'value_marker':
            kind = 'MARKER'
        elif vals and len(set(vals)) == 1:
            kind = 'CONSTANT'
        elif vals:
            top_v, top_n = Counter(vals).most_common(1)[0]
            kind = 'CONSTANT' if top_n / len(vals) >= 0.8 else 'VARIABLE'
        else:
            kind = 'VARIABLE'
        col_color.append(dom_c)
        col_kind.append(kind)
    # disambiguate headers
    seen_h = Counter()
    headers = []
    for cc in col_color:
        seen_h[cc] += 1
        headers.append(cc if seen_h[cc] == 1 else f'{cc}_{seen_h[cc]}')
    # sections
    secmap = white_sections(rows)
    # marker info for value_marker
    marker_sig = info.get('marker', '')
    mcolor, mval = None, None
    if marker_sig and '=' in marker_sig:
        mcolor, mval = marker_sig.split('=', 1)
        try:
            mval = int(mval)
        except ValueError:
            pass
    out_lines = meta_block(kid, '.tab', method_name,
                           SIG.get(kid, {}).get('template_exact', ''),
                           n, len(headers))
    fh = open(f'{BYKHIPU}/{kid}.csv', 'w', newline='')
    for L in out_lines:
        fh.write(L + '\n')
    cw = csv.writer(fh)
    cw.writerow(['ROW_ID', 'IS_MARKER_ROW', 'SECTION'] + headers)
    cw.writerow(['', '', ''] + col_kind)
    for ri, r in enumerate(row_list):
        first = r[0] if r else None
        if method_name == 'value_marker' and first is not None:
            starts_with_marker = (first[2] == mcolor and first[4] == mval)
            is_marker_row = (ri == 0 and not starts_with_marker)
        else:
            is_marker_row = False
        sec = secmap.get(r[0][0], '') if r else ''
        vals = []
        for p in range(maxlen):
            if p < len(r):
                v = r[p][4]
                vals.append('' if v is None or v == 0 else v)
            else:
                vals.append('')
        cw.writerow([ri + 1, 'TRUE' if is_marker_row else 'FALSE', sec] + vals)
    fh.close()
    return {'n_rows': n, 'n_cols': len(headers), 'method': method_name}

def write_flat(kid, rows, fmt, method):
    """Flat cord list. fmt in .flat/.log/.chk/.cod"""
    fh = open(f'{BYKHIPU}/{kid}.csv', 'w', newline='')
    n = len(rows)
    out_lines = meta_block(kid, fmt, method,
                           SIG.get(kid, {}).get('template_exact', ''),
                           n, 0)
    for L in out_lines:
        fh.write(L + '\n')
    cw = csv.writer(fh)
    if fmt == '.log':
        cw.writerow(['ORDINAL', 'LEVEL', 'COLOR1', 'COLOR2', 'VALUE', 'ROLE', 'KNOTS'])
        # delimiter = white runs >= 3
        is_delim = set()
        i = 0
        while i < len(rows):
            run = []
            j = i
            while j < len(rows) and rows[j][2] == 'W':
                run.append(rows[j][0])
                j += 1
            if len(run) >= 3:
                is_delim.update(run)
            i = j if run else i + 1
        for (o, lvl, c1, c2, v) in rows:
            role = 'DELIMITER' if o in is_delim else 'ENTRY'
            cw.writerow([o, lvl, c1, c2, '' if v is None or v == 0 else v,
                         role, KNOTSUM.get((kid, o), '')])
    elif fmt in ('.chk', '.cod'):
        cw.writerow(['ORDINAL', 'LEVEL', 'COLOR1', 'COLOR2', 'VALUE', 'KNOTS'])
        for (o, lvl, c1, c2, v) in rows:
            cw.writerow([o, lvl, c1, c2, '' if v is None or v == 0 else v,
                         KNOTSUM.get((kid, o), '')])
    else:  # .flat
        cw.writerow(['ORDINAL', 'LEVEL', 'COLOR1', 'COLOR2', 'VALUE', 'KNOTS'])
        for (o, lvl, c1, c2, v) in rows:
            cw.writerow([o, lvl, c1, c2, '' if v is None or v == 0 else v,
                         KNOTSUM.get((kid, o), '')])
    fh.close()
    ncols = 7 if fmt == '.log' else 6
    return {'n_rows': n, 'n_cols': ncols, 'method': method}

# ---- main loop over ALL khipu in khipu_main (619) ----
all_kids = [str(r[0]) for r in conn.execute('SELECT KHIPU_ID FROM khipu_main ORDER BY KHIPU_ID')]
print(f'{len(all_kids)} khipu total', flush=True)

index_rows = []
counts = Counter()
for ki, kid in enumerate(all_kids):
    rows = CACHE.get(kid, [])
    seg = SEG.get(kid, {})
    method = seg.get('method', 'none')
    fmt = file_format(kid, method)
    m = META.get(kid, {})
    if not rows:
        # no cords: metadata-only file
        fh = open(f'{BYKHIPU}/{kid}.csv', 'w', newline='')
        for L in meta_block(kid, fmt, method, '', 0, 0, 'NO CORDS IN DATABASE'):
            fh.write(L + '\n')
        fh.close()
        index_rows.append([kid, False, 0, 0, fmt, '', '', m.get('provenance', ''),
                           m.get('region', ''), f'by_khipu/{kid}.csv', 'no_cords'])
        counts['no_cords'] += 1
        continue
    info = {}
    try:
        import ast
        info = ast.literal_eval(seg.get('info', '{}') or '{}')
    except Exception:
        info = {}
    if fmt == '.tab':
        res = write_tab(kid, rows, method, info)
        if res is None:
            res = write_flat(kid, rows, '.flat', method)
            fmt = '.flat'
    else:
        res = write_flat(kid, rows, fmt, method)
    counts[fmt] += 1
    index_rows.append([kid, True, res['n_rows'], res['n_cols'], fmt,
                       REGIME.get(kid, ''), SIG.get(kid, {}).get('template_exact', ''),
                       m.get('provenance', ''), m.get('region', ''),
                       f'by_khipu/{kid}.csv', res['method']])
    if (ki + 1) % 100 == 0:
        print(f'  {ki+1}/{len(all_kids)}', flush=True)

with open(OUT + '/spreadsheet_index.csv', 'w', newline='') as f:
    cw = csv.writer(f)
    cw.writerow(['khipu_id', 'has_spreadsheet', 'n_rows', 'n_cols', 'format',
                 'data_regime', 'template_id', 'provenance', 'region',
                 'file_path', 'segmentation'])
    cw.writerows(index_rows)

print('counts:', dict(counts))
print('done', flush=True)
