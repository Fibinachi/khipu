"""Direction test, CORRECTED SCOPE: unclassified/other khipu only.

Excludes: funerary (26), warehouse/custodial (18 Inkawasi + 14 warehouse-like
+ deep_hierarchical_grouped cluster), census (6 + 205 census-like +
census_format_paired cluster).

Rationale: well-understood administrative types are numerical; seek the
linguistic/direction channel where document function is still unknown.
"""
import sqlite3
import csv
from collections import Counter
import math

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
FUNERARY = {1000000,1000001,1000002,1000003,1000004,1000005,1000006,1000007,
            1000008,1000009,1000010,1000011,1000012,1000018,1000019,1000020,
            1000021,1000022,1000023,1000024,1000025,1000045,1000235,1000366,
            1000367,1000648}

# Load reclassification labels
reclass = {}
with open('/home/hatch/workspace/quipu-analysis/reclassification-2026-10-10.csv') as f:
    for row in csv.DictReader(f):
        reclass[int(row['KHIPU_ID'])] = row['DOCUMENT_TYPE'].strip().lower()

# Load cluster labels
clusters = {}
with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
    for line in f:
        if line.startswith('#'):
            continue
        parts = line.strip().split(',')
        if parts[0] == 'KHIPU_ID' or not parts[0].isdigit():
            continue
        clusters[int(parts[0])] = parts[2].strip()

EXCL_TYPES = {'warehouse', 'warehouse-like', 'census', 'census-like'}
EXCL_CLUSTERS = {'deep_hierarchical_grouped', 'census_format_paired'}

# All khipu in DB
conn = sqlite3.connect(DB)
c = conn.cursor()
c.execute('SELECT DISTINCT KHIPU_ID FROM cord')
all_khipu = set(r[0] for r in c.fetchall())

included = set()
excluded_detail = Counter()
for kh in all_khipu:
    if kh in FUNERARY:
        excluded_detail['funerary'] += 1
        continue
    dt = reclass.get(kh, 'unclassified')
    cl = clusters.get(kh, 'nocluster')
    if dt in EXCL_TYPES:
        excluded_detail[f'type:{dt}'] += 1
        continue
    if cl in EXCL_CLUSTERS:
        excluded_detail[f'cluster:{cl}'] += 1
        continue
    included.add(kh)
    excluded_detail['INCLUDED'] += 1

print(f"Total khipu with cords: {len(all_khipu)}")
print(f"Excluded: {dict(excluded_detail)}")
print(f"INCLUDED (unclassified/other): {len(included)}")

# Cluster composition of included set
inc_clusters = Counter(clusters.get(kh, 'nocluster') for kh in included)
print(f"Included cluster mix: {dict(inc_clusters)}")
inc_types = Counter(reclass.get(kh, 'unclassified') for kh in included)
print(f"Included type mix: {dict(inc_types)}")

def is_marked(fc):
    if fc is None:
        return None
    parts = fc.replace('-', ':').split(':')
    return any(p and p != 'W' for p in parts)

color_cache = {}
def get_color(kh, cid):
    key = (kh, cid)
    if key not in color_cache:
        c.execute('SELECT FULL_COLOR FROM ascher_cord_color WHERE KHIPU_ID=? AND CORD_ID=?',
                  (kh, cid))
        r = c.fetchone()
        color_cache[key] = r[0] if r else None
    return color_cache[key]

# Pull knots for included khipu only
ph = ','.join('?' * len(included))
c.execute(f'''SELECT k.DIRECTION, co.KHIPU_ID, co.CORD_ID, co.CORD_LEVEL
              FROM knot k JOIN cord co ON k.CORD_ID = co.CORD_ID
              WHERE co.KHIPU_ID IN ({ph})''', tuple(included))
rows = [(d, kh, cid, lvl) for d, kh, cid, lvl in c.fetchall()
        if d in ('S', 'U', 'Z')]
print(f"\n{len(rows)} knots (S/U/Z) on included khipu")

inv = Counter(d for d, _, _, _ in rows)
print(f"Direction inventory: S={inv['S']}, U={inv['U']}, Z={inv['Z']}")

# Cord-level aggregation
cord_data = {}
for d, kh, cid, lvl in rows:
    key = (kh, cid)
    if key not in cord_data:
        cord_data[key] = {'U': False, 'nonZ': False, 'level': lvl,
                          'color': get_color(kh, cid)}
    if d == 'U':
        cord_data[key]['U'] = True
    if d != 'Z':
        cord_data[key]['nonZ'] = True

def chi2(a, b, cc, dd):
    n = a + b + cc + dd
    if n == 0:
        return 0, 1.0
    ea = (a + b) * (a + cc) / n
    eb = (a + b) * (b + dd) / n
    ec = (cc + dd) * (a + cc) / n
    ed = (cc + dd) * (b + dd) / n
    x2 = sum((o - e) ** 2 / e for o, e in
             [(a, ea), (b, eb), (cc, ec), (dd, ed)] if e > 0)
    p = math.erfc(math.sqrt(x2) / math.sqrt(2))
    return x2, p

print("\n=== TEST 1: U-direction vs color-marking (unclassified only) ===")
for label, key in [('U-direction', 'U'), ('non-Z direction', 'nonZ')]:
    a = b = cc = dd = 0
    for v in cord_data.values():
        m = is_marked(v['color'])
        if m is None:
            continue
        has = v[key]
        if m and has: a += 1
        elif m and not has: b += 1
        elif not m and has: cc += 1
        else: dd += 1
    x2, p = chi2(a, b, cc, dd)
    rm = 100 * a / (a + b) if (a + b) else 0
    ru = 100 * cc / (cc + dd) if (cc + dd) else 0
    print(f"  {label}: marked {rm:.1f}% (n={a+b}) vs unmarked {ru:.1f}% (n={cc+dd}), chi2={x2:.1f} p={p:.2e}")

print("\n=== TEST 3: within-level control ===")
for lvl in sorted(set(v['level'] for v in cord_data.values() if v['level'] is not None))[:6]:
    a = b = cc = dd = 0
    for v in cord_data.values():
        if v['level'] != lvl:
            continue
        m = is_marked(v['color'])
        if m is None:
            continue
        if m and v['U']: a += 1
        elif m and not v['U']: b += 1
        elif not m and v['U']: cc += 1
        else: dd += 1
    if (a + b + cc + dd) < 30:
        print(f"  Level {lvl}: n too small ({a+b+cc+dd}), skipping")
        continue
    x2, p = chi2(a, b, cc, dd)
    rm = 100 * a / (a + b) if (a + b) else 0
    ru = 100 * cc / (cc + dd) if (cc + dd) else 0
    print(f"  Level {lvl}: marked+U {rm:.1f}% vs unmarked+U {ru:.1f}%, chi2={x2:.1f} p={p:.2e}")

print("\n=== TEST 5: U-rate and marking-rate by level ===")
for lvl in sorted(set(v['level'] for v in cord_data.values() if v['level'] is not None))[:6]:
    vs = [v for v in cord_data.values() if v['level'] == lvl]
    nu = sum(1 for v in vs if v['U'])
    mk = sum(1 for v in vs if is_marked(v['color']) is True)
    tk = sum(1 for v in vs if is_marked(v['color']) is not None)
    print(f"  Level {lvl}: U {100*nu/max(len(vs),1):.1f}% (n={len(vs)}), marked {100*mk/max(tk,1):.1f}%")

print("\n=== TEST 4: anomaly overlap ===")
import re
anom_ids = set()
try:
    with open('/home/hatch/workspace/quipu-analysis/anomalous-transcriptions.md') as f:
        text = f.read()
    # section headers like "## 1000008" or "### ID 1000008"
    for m in re.finditer(r'^#{1,4}\s*[^\d\n]*(\d{7})', text, re.M):
        anom_ids.add(int(m.group(1)))
    print(f"  Anomalous IDs parsed: {len(anom_ids)}")
except FileNotFoundError:
    print("  transcription file not found")
u_quipu = set(kh for (kh, cid), v in cord_data.items() if v['U'])
print(f"  Included quipu with U: {len(u_quipu)}")
ov = u_quipu & anom_ids
print(f"  Overlap with anomalous: {len(ov)} {sorted(ov) if ov else ''}")
only_anom = anom_ids - u_quipu
print(f"  Anomalous without U (in included set or not): {sorted(only_anom) if only_anom else 'none'}")
# which anomalous are in included set at all?
in_inc = anom_ids & included
print(f"  Anomalous IDs in included set: {len(in_inc)} {sorted(in_inc) if in_inc else ''}")

# U-direction quipu list (for reference, top by U count)
uc = Counter(kh for (kh, cid), v in cord_data.items() if v['U'])
print(f"\nTop U-direction quipu in included set:")
for kh, n in uc.most_common(10):
    print(f"  {kh}: {n} U-cords (cluster={clusters.get(kh)}, type={reclass.get(kh)})")

conn.close()
print("\nDone.")
