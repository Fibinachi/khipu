"""Test the rider hypothesis on 18 Inkawasi warehouse quipu (1000597-1000614).

Hypothesis: main-cord (level 1) structure = house inventory;
subsidiary (level 2+) "rider" cords = separate inventory from another source,
co-located for administrative convenience. Subsidiaries are NOT detail of parent.
"""
import sqlite3, random, sys
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from decoder import decode_cord
from collections import Counter, defaultdict
import math

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
INKA = list(range(1000597, 1000615))
COMMODITY = {1000597:'chili(inf)', 1000598:'chili(inf)', 1000607:'peanut',
             1000608:'chili', 1000609:'chili', 1000610:'peanut', 1000611:'peanut',
             1000612:'peanut', 1000613:'beans', 1000614:'peanut'}

conn = sqlite3.connect(DB)
c = conn.cursor()

def full_color(khipu_id, cord_id):
    c.execute("SELECT FULL_COLOR FROM ascher_cord_color WHERE KHIPU_ID=? AND CORD_ID=?",
              (khipu_id, cord_id))
    r = c.fetchone()
    return r[0] if r else None

def is_compound(fc):
    return fc is not None and (':' in fc or '-' in fc)

def has_white(fc):
    return fc is not None and 'W' in fc.split(':') or (fc is not None and fc=='W')

# Build parent->children map via PENDANT_FROM->CORD_ID, levels via CORD_LEVEL
# parents = level-1 cords that have level-2+ children
cords = {}  # (khipu,cord) -> dict
for kh in INKA:
    c.execute("SELECT CORD_ID, CORD_LEVEL, CORD_ORDINAL, PENDANT_FROM FROM cord WHERE KHIPU_ID=?", (kh,))
    for cid, lvl, cord_ord, pf in c.fetchall():
        cords[(kh, cid)] = {'level': lvl, 'cord_ord': cord_ord, 'pf': pf,
                            'color': full_color(kh, cid), 'khipu': kh, 'cid': cid}

# parent map: child -> parent cord id
children_of = defaultdict(list)
for (kh, cid), d in cords.items():
    if d['level'] > 1 and d['pf'] in [cc for (kk, cc) in cords if kk == kh]:
        children_of[(kh, d['pf'])].append((kh, cid))

parents_with_kids = {p: kids for p, kids in children_of.items() if kids}
print(f"Parents with subsidiaries: {len(parents_with_kids)}")
print(f"Total subsidiary cords: {sum(len(v) for v in children_of.values())}")

# Decode values (tens and up; units unreliable for Inkawasi)
values = {}
null_count = 0
total_dec = 0
for (kh, cid), d in cords.items():
    total_dec += 1
    try:
        res = decode_cord(conn, cid)
        values[(kh, cid)] = res['value']
        if res['value'] is None:
            null_count += 1
    except Exception as e:
        values[(kh, cid)] = None
        null_count += 1
print(f"Decoded: {total_dec}, NULL: {null_count} ({100*null_count/total_dec:.1f}%)")

print("\n" + "="*70)
print("TEST 1: COLOR CONTRAST — subsidiary color vs parent color")
print("="*70)
diff = 0; same = 0; missing = 0
pairs = []  # (parent_color, child_color)
for p, kids in parents_with_kids.items():
    pc = cords[p]['color']
    for k in kids:
        kc = cords[k]['color']
        if pc is None or kc is None:
            missing += 1
            continue
        pairs.append((pc, kc))
        if kc == pc: same += 1
        else: diff += 1
n = diff + same
print(f"Subsidiary color == parent: {same} ({100*same/n:.1f}%)")
print(f"Subsidiary color != parent: {diff} ({100*diff/n:.1f}%)")
print(f"Missing color data: {missing}")

# Null: reshuffle child colors within each quipu
random.seed(42)
null_diffs = []
for _ in range(1000):
    nd = 0; ns = 0
    for p, kids in parents_with_kids.items():
        kh = p[0]
        # pool of colors in this quipu
        pool = [cords[(kk, cc)]['color'] for (kk, cc) in cords if kk == kh
                and cords[(kk, cc)]['color'] is not None]
        pc = cords[p]['color']
        if pc is None: continue
        for k in kids:
            kc = cords[k]['color']
            if kc is None: continue
            rc = random.choice(pool)
            if rc == pc: ns += 1
            else: nd += 1
    null_diffs.append(nd / (nd + ns) if (nd+ns) else 0)
obs = diff / n
print(f"Observed diff rate: {obs:.3f}")
print(f"Null mean diff rate: {sum(null_diffs)/len(null_diffs):.3f} (sd {math.sqrt(sum((x-sum(null_diffs)/len(null_diffs))**2 for x in null_diffs)/len(null_diffs)):.3f})")
print(f"P(observed >= null): {sum(1 for x in null_diffs if x >= obs)/len(null_diffs):.3f}")

print("\n" + "="*70)
print("TEST 2: VALUE INDEPENDENCE — parent vs summed subsidiaries")
print("="*70)
pv, sv = [], []
for p, kids in parents_with_kids.items():
    pval = values.get(p)
    if pval is None: continue
    stot = 0; ok = True
    for k in kids:
        kv = values.get(k)
        if kv is None: ok = False; break
        stot += kv
    if not ok: continue
    pv.append(pval); sv.append(stot)
print(f"Parent-child pairs with full values: {len(pv)}")
if len(pv) > 2:
    mp, ms = sum(pv)/len(pv), sum(sv)/len(sv)
    cov = sum((a-mp)*(b-ms) for a, b in zip(pv, sv))/len(pv)
    vp = sum((a-mp)**2 for a in pv)/len(pv)
    vs = sum((b-ms)**2 for b in sv)/len(sv)
    corr = cov/math.sqrt(vp*vs) if vp*vs > 0 else 0
    print(f"Correlation(parent, sum_of_subs): {corr:.3f}")
    # exact-sum check
    exact = sum(1 for a, b in zip(pv, sv) if a == b and a != 0)
    print(f"Exact nonzero matches: {exact}/{len(pv)}")
    # ratio check
    ratios = Counter()
    for a, b in zip(pv, sv):
        if b != 0 and a != 0:
            r = a/b
            if abs(r - round(r)) < 0.01 and round(r) <= 10:
                ratios[round(r)] += 1
    print(f"Integer ratios (parent/subs, top): {ratios.most_common(5)}")

print("\n" + "="*70)
print("TEST 3: SUBSIDIARY INTERNAL PATTERNS — repeating values")
print("="*70)
l1_vals = Counter(v for (kh, cid), v in values.items()
                 if cords[(kh, cid)]['level'] == 1 and v is not None and v != 0)
sub_vals = Counter(v for (kh, cid), v in values.items()
                  if cords[(kh, cid)]['level'] > 1 and v is not None and v != 0)
print(f"L1 top values: {l1_vals.most_common(8)}")
print(f"Sub top values: {sub_vals.most_common(8)}")
# Urton & Chu repeating values: 15/10/47/208 — check level distribution
for target in [15, 10, 47, 208, 150, 100, 470, 2080]:
    l1c = l1_vals.get(target, 0); sc = sub_vals.get(target, 0)
    if l1c + sc > 0:
        print(f"  Value {target}: L1={l1c}, Sub={sc}")

print("\n" + "="*70)
print("TEST 4: COMPOUND ENRICHMENT — subsidiary compounds vs parent color")
print("="*70)
# For subsidiaries with compound colors: does the compound contain the parent's color?
# Rider model: compound marks external origin -> should differ from parent
cont = 0; differ = 0; examples = []
for p, kids in parents_with_kids.items():
    pc = cords[p]['color']
    if pc is None: continue
    pparts = set(pc.replace('-', ':').split(':'))
    for k in kids:
        kc = cords[k]['color']
        if kc is None or not is_compound(kc): continue
        kparts = set(kc.replace('-', ':').split(':'))
        if pparts & kparts: cont += 1
        else:
            differ += 1
            if len(examples) < 8: examples.append((p, pc, k, kc))
t = cont + differ
print(f"Subsidiary compounds sharing >=1 color with parent: {cont} ({100*cont/t:.1f}%)" if t else "none")
print(f"Subsidiary compounds sharing NO color with parent: {differ} ({100*differ/t:.1f}%)" if t else "")
for p, pc, k, kc in examples:
    print(f"  parent {p[1]} ({pc}) <- sub {k[1]} ({kc})")

print("\n" + "="*70)
print("TEST 5: COMMODITY SPLIT")
print("="*70)
for kh in INKA:
    com = COMMODITY.get(kh, 'unknown')
    n_l1 = sum(1 for (kk, cc), d in cords.items() if kk == kh and d['level'] == 1)
    n_sub = sum(1 for (kk, cc), d in cords.items() if kk == kh and d['level'] > 1)
    n_par = sum(1 for p in parents_with_kids if p[0] == kh)
    # color contrast for this khipu
    d2 = s2 = 0
    for p, kids in parents_with_kids.items():
        if p[0] != kh: continue
        pc = cords[p]['color']
        for k in kids:
            kc = cords[k]['color']
            if pc is None or kc is None: continue
            if kc == pc: s2 += 1
            else: d2 += 1
    nn = d2 + s2
    print(f"  {kh} [{com}]: L1={n_l1} sub={n_sub} parents={n_par} " +
          (f"contrast={100*d2/nn:.0f}%" if nn else "no color pairs"))

print("\n" + "="*70)
print("TEST 6: WHITE GRADIENT — white on subsidiaries?")
print("="*70)
for lvl in [1, 2, 3, 4, 5]:
    tot = sum(1 for d in cords.values() if d['level'] == lvl and d['color'] is not None)
    wh = sum(1 for d in cords.values() if d['level'] == lvl and d['color'] is not None
             and 'W' in d['color'].replace('-', ':').split(':'))
    print(f"  Level {lvl}: {wh}/{tot} white-involved ({100*wh/tot:.1f}%)" if tot else f"  Level {lvl}: none")
# Are white subsidiaries attached to white or non-white parents?
wsub_wpar = 0; wsub_cpar = 0
for p, kids in parents_with_kids.items():
    pc = cords[p]['color']
    if pc is None: continue
    pwhite = 'W' in pc.replace('-', ':').split(':')
    for k in kids:
        kc = cords[k]['color']
        if kc is None: continue
        kwhite = 'W' in kc.replace('-', ':').split(':')
        if kwhite and pwhite: wsub_wpar += 1
        elif kwhite and not pwhite: wsub_cpar += 1
print(f"White subsidiaries under white parents: {wsub_wpar}")
print(f"White subsidiaries under colored parents: {wsub_cpar}")
print("\nDone.")
