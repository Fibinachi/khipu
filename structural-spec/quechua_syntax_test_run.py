"""Test whether khipu cord sequences follow Quechua syntactic patterns.
5 tests: NP order, clause chaining, postpositional order, SOV document level, negative test.
"""
import sqlite3, csv, sys
from collections import defaultdict, Counter
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from decoder import decode_cord

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Load cluster assignments
clusters = {}
with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
    for row in csv.DictReader(filter(lambda r: not r.startswith('#'), f)):
        clusters[int(row['KHIPU_ID'])] = (int(row['CLUSTER_ID']), row['CLUSTER_NAME'])

CENSUS = [k for k,v in clusters.items() if v[0]==2]      # 250 paired
TALLY  = [k for k,v in clusters.items() if v[0]==3]      # 78 flat large-value
WAREH  = [k for k,v in clusters.items() if v[0]==4]       # 76 deep hierarchical
SPARSE = [k for k,v in clusters.items() if v[0]==5]       # 172 deep/sparse

def get_cords(khipu_id, level=None):
    q = """SELECT c.CORD_ID, c.CORD_ORDINAL, c.CORD_LEVEL, c.PENDANT_FROM,
                  acc.COLOR_CD_1 as color
           FROM cord c LEFT JOIN ascher_cord_color acc ON c.CORD_ID=acc.CORD_ID
           WHERE c.KHIPU_ID=?"""
    params=[khipu_id]
    if level is not None:
        q += " AND c.CORD_LEVEL=?"
        params.append(level)
    q += " ORDER BY c.CORD_ORDINAL"
    return list(c.execute(q, params))

def decode_all(khipu_id):
    vals = {}
    for row in get_cords(khipu_id):
        try:
            d = decode_cord(conn, row['CORD_ID'])
            if d and d.get('value') is not None and d.get('confidence')=='high':
                vals[row['CORD_ID']] = d['value']
        except Exception:
            pass
    return vals

def norm_color(col):
    if not col: return 'BLANK'
    return col.strip()

print("="*70)
print("TEST 1: NP-internal order — value ordering within color groups")
print("="*70)
# In census khipu, find repeating color-pattern groups.
# Within each group instance, check if values follow consistent order
# (e.g., position 1 always >= position 2, etc.)
group_order_votes = Counter()  # 'asc','desc','mixed','equal' per position-pair
group_instances = 0
pos_patterns = Counter()
for kid in CENSUS[:250]:
    cords = get_cords(kid, level=1)
    if len(cords) < 8: continue
    colors = [norm_color(r['color']) for r in cords]
    # Find the repeating unit: try period 2..6, pick the one with best repetition
    best_period, best_score = None, 0
    for p in range(2,7):
        matches = sum(1 for i in range(len(colors)-p) if colors[i]==colors[i+p])
        score = matches/(len(colors)-p) if len(colors)>p else 0
        if score > best_score:
            best_score, best_period = score, p
    if best_score < 0.7 or not best_period: continue
    p = best_period
    pos_patterns[p]+=1
    vals = decode_all(kid)
    # For each group instance, record value order across positions
    for start in range(0, len(cords)-p+1, p):
        grp = cords[start:start+p]
        v = [vals.get(r['CORD_ID']) for r in grp]
        if any(x is None for x in v): continue
        group_instances += 1
        # pairwise ordering pattern
        for i in range(len(v)-1):
            if v[i] > v[i+1]: group_order_votes[(i,'desc')]+=1
            elif v[i] < v[i+1]: group_order_votes[(i,'asc')]+=1
            else: group_order_votes[(i,'eq')]+=1

print(f"Census khipu with detectable color period: {sum(pos_patterns.values())}")
print(f"Period distribution: {dict(pos_patterns)}")
print(f"Group instances with full high-conf values: {group_instances}")
print("Position-pair ordering votes (pos: desc=v[i]>v[i+1], asc, eq):")
for key in sorted(group_order_votes):
    print(f"  pos{key[0]}->{key[0]+1} {key[1]}: {group_order_votes[key]}")

print()
print("="*70)
print("TEST 2: Clause chaining — group boundary markers")
print("="*70)
# At color-group boundaries: is there a structural marker?
# Check: empty cord at boundary? top cord? Check if boundary positions
# are more likely to have (a) blank color, (b) no knots, (c) top cord nearby
boundary_blank = 0; boundary_total = 0
nonboundary_blank = 0; nonboundary_total = 0
for kid in CENSUS[:250]:
    cords = get_cords(kid, level=1)
    if len(cords) < 8: continue
    colors = [norm_color(r['color']) for r in cords]
    best_period, best_score = None, 0
    for p in range(2,7):
        matches = sum(1 for i in range(len(colors)-p) if colors[i]==colors[i+p])
        score = matches/(len(colors)-p) if len(colors)>p else 0
        if score > best_score:
            best_score, best_period = score, p
    if best_score < 0.7 or not best_period: continue
    p = best_period
    for i, r in enumerate(cords):
        is_boundary = (i % p == 0)
        is_blank = norm_color(r['color'])=='BLANK'
        if is_boundary:
            boundary_total+=1; boundary_blank+=is_blank
        else:
            nonboundary_total+=1; nonboundary_blank+=is_blank
print(f"Boundary positions: {boundary_blank}/{boundary_total} blank ({100*boundary_blank/max(1,boundary_total):.1f}%)")
print(f"Non-boundary: {nonboundary_blank}/{nonboundary_total} blank ({100*nonboundary_blank/max(1,nonboundary_total):.1f}%)")

# Same vs different color sequence across groups (SS vs DS analog)
# If consecutive groups have identical color patterns = "same subject",
# different = "different subject". Check if "DS" boundaries have more marking.
ss_marked = 0; ss_total=0; ds_marked=0; ds_total=0
for kid in CENSUS[:100]:
    cords = get_cords(kid, level=1)
    if len(cords) < 8: continue
    colors = [norm_color(r['color']) for r in cords]
    best_period, best_score = None, 0
    for p in range(2,7):
        matches = sum(1 for i in range(len(colors)-p) if colors[i]==colors[i+p])
        score = matches/(len(colors)-p) if len(colors)>p else 0
        if score > best_score:
            best_score, best_period = score, p
    if best_score < 0.9 or not best_period: continue  # strict: nearly identical groups
    # All groups same pattern by construction; check color VALUES across group pairs
    # Instead: compare group N color multiset vs group N+1
    p = best_period
    groups = [colors[i:i+p] for i in range(0, len(colors)-p+1, p)]
    for g1, g2 in zip(groups, groups[1:]):
        same = (g1==g2)
        # "marking" = does the boundary cord (first of g2) differ in color from last of g1?
        boundary_shift = (g1[-1] != g2[0])
        if same: ss_total+=1; ss_marked+=boundary_shift
        else: ds_total+=1; ds_marked+=boundary_shift
print(f"Same-pattern groups (SS analog): boundary shift {ss_marked}/{ss_total}")
print(f"Different-pattern groups (DS analog): boundary shift {ds_marked}/{ds_total}")

print()
print("="*70)
print("TEST 3: Postpositional order — subsidiary color contrast by depth")
print("="*70)
# For each subsidiary, compare its color to parent's color.
# Quechua postpositional prediction: deeper = more relational marking = higher contrast
for level in [2,3,4]:
    match=0; total=0
    for kid in list(clusters.keys()):
        # get parent-child pairs where child is at this level
        rows = c.execute("""SELECT ch.CORD_ID as ch_id, ch.PENDANT_FROM as par_cord,
                                   acc1.COLOR_CD_1 as ch_color, acc2.COLOR_CD_1 as par_color
                            FROM cord ch
                            JOIN cord par ON ch.PENDANT_FROM = par.CORD_ID
                            LEFT JOIN ascher_cord_color acc1 ON ch.CORD_ID=acc1.CORD_ID
                            LEFT JOIN ascher_cord_color acc2 ON par.CORD_ID=acc2.CORD_ID
                            WHERE ch.KHIPU_ID=? AND ch.CORD_LEVEL=?""",
                         (kid, level)).fetchall()
        for r in rows:
            cc = norm_color(r['ch_color']); pc = norm_color(r['par_color'])
            if cc=='BLANK' or pc=='BLANK': continue
            total+=1
            if cc!=pc: match+=1
    pct = 100*match/max(1,total)
    print(f"Level {level}: color contrast {match}/{total} = {pct:.1f}%")

print()
print("="*70)
print("TEST 4: SOV document level — structural arrangement by document type")
print("="*70)
# Compare: does warehouse (deep) put more in "object" vs census (flat)?
# Metrics: mean max_level, mean n_cords, subsidiary rate, color diversity
import statistics
for name, kids in [('census_paired',CENSUS),('tally_flat',TALLY),('warehouse_deep',WAREH),('sparse',SPARSE)]:
    levels=[]; ncords=[]; subrates=[]; ncolors=[]
    for kid in kids:
        cords = get_cords(kid)
        if not cords: continue
        ncords.append(len(cords))
        levels.append(max(r['CORD_LEVEL'] for r in cords if r['CORD_LEVEL'] is not None) or 0)
        l1 = sum(1 for r in cords if r['CORD_LEVEL']==1)
        sub = sum(1 for r in cords if (r['CORD_LEVEL'] or 0)>1)
        subrates.append(sub/max(1,len(cords)))
        ncolors.append(len(set(norm_color(r['color']) for r in cords)))
    print(f"{name} (n={len(kids)}): cords med={statistics.median(ncords) if ncords else 0:.0f}, "
          f"maxlevel med={statistics.median(levels) if levels else 0:.0f}, "
          f"sub_rate mean={statistics.mean(subrates) if subrates else 0:.2f}, "
          f"colors med={statistics.median(ncolors) if ncolors else 0:.0f}")

print()
print("="*70)
print("TEST 5: Negative test — contradictions with Quechua syntax")
print("="*70)
# 5a: Pre-nominal modification check. In Quechua NP: demonstrative-numeral-adjective-noun.
# On khipu, if a "modifier" cord (subsidiary) ever PRECEDES its head in ordinal order
# in a way that suggests modifier-before-head at the PHRASE level... 
# Actually the real test: does any cord's value+color arrangement violate
# numeral-before-noun? Since they're fused, check instead:
# Do subsidiaries (modifiers) ever appear at LOWER ordinal than their parent
# (i.e., before the head in reading order)?
violations=0; total_pairs=0
for kid in list(clusters.keys())[:593]:
    rows = c.execute("""SELECT ch.CORD_ORDINAL as ch_ord, par.CORD_ORDINAL as par_ord
                        FROM cord ch JOIN cord par ON ch.PENDANT_FROM=par.CORD_ID
                        WHERE ch.KHIPU_ID=? AND ch.CORD_ORDINAL IS NOT NULL
                        AND par.CORD_ORDINAL IS NOT NULL""", (kid,)).fetchall()
    for r in rows:
        total_pairs+=1
        if r['ch_ord'] < r['par_ord']:
            violations+=1
print(f"5a: Subsidiary ordinal < parent ordinal (modifier before head): {violations}/{total_pairs} = {100*violations/max(1,total_pairs):.2f}%")

# 5b: Check knot cluster order on cord: Quechua is head-final (postpositions, SOV).
# If khipu "words" are head-final, the most significant digit cluster should come FIRST
# (top of cord, nearest main cord), units last (free end). Check decoder assumption.
# The decoder already assumes units at free end. Verify: in high-conf decodes,
# is the E/L (units) cluster always the last (max START_POS)?
from decoder import decode_cord
checked=0; units_last=0
for kid in list(clusters.keys())[:100]:
    for row in get_cords(kid):
        try:
            d = decode_cord(conn, row['CORD_ID'])
        except Exception:
            continue
        if not d or d.get('confidence')!='high': continue
        cl = d.get('clusters', [])
        if len(cl) < 2: continue
        checked+=1
        # last cluster by START_POS should be units type
        last = max(cl, key=lambda x: x.get('START_POS',0) or 0)
        if last.get('unit_type') in ('L','E','EE','SP','LL','BL'):
            units_last+=1
print(f"5b: Units cluster at free end (head-final digit order): {units_last}/{checked} = {100*units_last/max(1,checked):.1f}%")

print()
print("ALL TESTS COMPLETE")
