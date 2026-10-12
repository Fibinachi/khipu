"""Test whether knot twist direction patterns with color-marking (evidentiality).

Hypothesis: knot direction is a semantic channel. Non-standard direction
should appear disproportionately on color-marked (evidentially distant) cords.
"""
import sqlite3
from collections import Counter, defaultdict
from math import sqrt

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
FUNERARY = {1000000,1000001,1000002,1000003,1000004,1000005,1000006,1000007,
            1000008,1000009,1000010,1000011,1000012,1000018,1000019,1000020,
            1000021,1000022,1000023,1000024,1000025,1000045,1000235,1000366,
            1000367,1000648}

conn = sqlite3.connect(DB)
c = conn.cursor()

def is_marked(fc):
    """Marked = has a non-white color component."""
    if fc is None:
        return None  # missing, not unmarked
    parts = fc.replace('-', ':').split(':')
    nonwhite = [p for p in parts if p and p != 'W']
    return len(nonwhite) > 0

def get_color(kh, cid, cache):
    key = (kh, cid)
    if key not in cache:
        c.execute('SELECT FULL_COLOR FROM ascher_cord_color WHERE KHIPU_ID=? AND CORD_ID=?',
                  (kh, cid))
        r = c.fetchone()
        cache[key] = r[0] if r else None
    return cache[key]

# Pull all knots with direction, cord level, khipu — excluding funerary
print("Loading knot data (excluding 26 funerary)...")
c.execute('''SELECT k.DIRECTION, co.KHIPU_ID, co.CORD_ID, co.CORD_LEVEL
             FROM knot k JOIN cord co ON k.CORD_ID = co.CORD_ID''')
rows = [(d, kh, cid, lvl) for d, kh, cid, lvl in c.fetchall()
        if kh not in FUNERARY and d in ('S', 'U', 'Z')]
print(f"  {len(rows)} knots with S/U/Z direction, non-funerary")

# Direction inventory
inv = Counter(d for d, _, _, _ in rows)
print(f"\nDirection inventory: S={inv['S']}, U={inv['U']}, Z={inv['Z']}")
print(f"  Modal = Z ({100*inv['Z']/len(rows):.1f}%)")

color_cache = {}

# ---- TEST 1: Basic association ----
# U (rarest, flagged anomalous) vs color-marking, at cord level
print("\n=== TEST 1: U-direction vs color-marking (cord level) ===")
cord_data = {}  # (kh,cid) -> (has_U, marked, level)
for d, kh, cid, lvl in rows:
    key = (kh, cid)
    if key not in cord_data:
        cord_data[key] = {'U': False, 'nonZ': False, 'level': lvl,
                          'color': get_color(kh, cid, color_cache)}
    if d == 'U':
        cord_data[key]['U'] = True
    if d != 'Z':
        cord_data[key]['nonZ'] = True

# Contingency: U vs marked (excluding missing color)
def chi2(a, b, cc, dd):
    # [[a,b],[c,d]]
    n = a + b + cc + dd
    if n == 0:
        return 0, 1.0
    exp_a = (a + b) * (a + cc) / n
    exp_b = (a + b) * (b + dd) / n
    exp_c = (cc + dd) * (a + cc) / n
    exp_d = (cc + dd) * (b + dd) / n
    x2 = sum((o - e) ** 2 / e for o, e in
             [(a, exp_a), (b, exp_b), (cc, exp_c), (dd, exp_d)] if e > 0)
    # p-value approx for 1df: use survival function approximation
    # For large x2, p ~ tiny. Report x2 and use normal approx for z = sqrt(x2)
    import math
    z = math.sqrt(x2)
    # two-tailed p from z (rough)
    p = math.erfc(z / math.sqrt(2))
    return x2, p

for label, key in [('U-direction', 'U'), ('non-Z direction', 'nonZ')]:
    # marked+dir, marked+nodir, unmarked+dir, unmarked+nodir
    a = b = cc = dd = 0
    for k, v in cord_data.items():
        m = is_marked(v['color'])
        if m is None:
            continue
        has = v[key]
        if m and has:
            a += 1
        elif m and not has:
            b += 1
        elif not m and has:
            cc += 1
        else:
            dd += 1
    x2, p = chi2(a, b, cc, dd)
    rate_marked = 100 * a / (a + b) if (a + b) else 0
    rate_unmarked = 100 * cc / (cc + dd) if (cc + dd) else 0
    print(f"  {label}:")
    print(f"    marked cords with {label}: {a}/{a+b} ({rate_marked:.1f}%)")
    print(f"    unmarked cords with {label}: {cc}/{cc+dd} ({rate_unmarked:.1f}%)")
    print(f"    chi2={x2:.1f}, p={p:.2e}")

# ---- TEST 3: Level control ----
print("\n=== TEST 3: U-direction vs marking within each CORD_LEVEL ===")
for lvl in sorted(set(v['level'] for v in cord_data.values() if v['level'] is not None))[:6]:
    a = b = cc = dd = 0
    for k, v in cord_data.items():
        if v['level'] != lvl:
            continue
        m = is_marked(v['color'])
        if m is None:
            continue
        has = v['U']
        if m and has:
            a += 1
        elif m and not has:
            b += 1
        elif not m and has:
            cc += 1
        else:
            dd += 1
    if (a + b + cc + dd) < 50:
        continue
    x2, p = chi2(a, b, cc, dd)
    rm = 100 * a / (a + b) if (a + b) else 0
    ru = 100 * cc / (cc + dd) if (cc + dd) else 0
    print(f"  Level {lvl}: marked+U {rm:.1f}% (n={a+b}), unmarked+U {ru:.1f}% (n={cc+dd}), chi2={x2:.1f} p={p:.2e}")

# ---- TEST 5: Does U-direction increase with depth? ----
print("\n=== TEST 5: U-direction rate by CORD_LEVEL (evidentiality parallel?) ===")
for lvl in sorted(set(v['level'] for v in cord_data.values() if v['level'] is not None))[:6]:
    n_u = sum(1 for v in cord_data.values() if v['level'] == lvl and v['U'])
    n_t = sum(1 for v in cord_data.values() if v['level'] == lvl)
    print(f"  Level {lvl}: U-cords {n_u}/{n_t} ({100*n_u/max(n_t,1):.1f}%)")

# Also: marking rate by level for reference
print("\n  (Reference: marking rate by level)")
for lvl in sorted(set(v['level'] for v in cord_data.values() if v['level'] is not None))[:6]:
    mk = sum(1 for v in cord_data.values()
             if v['level'] == lvl and is_marked(v['color']) is True)
    tot = sum(1 for v in cord_data.values()
              if v['level'] == lvl and is_marked(v['color']) is not None)
    print(f"  Level {lvl}: marked {mk}/{tot} ({100*mk/max(tot,1):.1f}%)")

# ---- TEST 4: Anomaly overlap ----
print("\n=== TEST 4: U-direction quipu vs 20 anomalous transcriptions ===")
anom_ids = set()
try:
    with open('/home/hatch/workspace/quipu-analysis/anomalous-transcriptions.md') as f:
        import re
        for line in f:
            m = re.search(r'100\d{4}', line)
            if m and ('##' in line or 'ID' in line or 'quipu' in line.lower() or '100' in line[:20]):
                anom_ids.add(int(m.group()))
except FileNotFoundError:
    print("  anomalous-transcriptions.md not found")

u_quipu = set(kh for (kh, cid), v in cord_data.items() if v['U'])
print(f"  Quipu with any U-direction knot: {len(u_quipu)}")
print(f"  Anomalous transcribed quipu found: {len(anom_ids)}")
overlap = u_quipu & anom_ids
print(f"  Overlap: {len(overlap)}")
if overlap:
    print(f"  Overlapping IDs: {sorted(overlap)}")
if anom_ids - u_quipu:
    print(f"  Anomalous WITHOUT U: {sorted(anom_ids - u_quipu)}")

conn.close()
print("\nDone.")
