"""Tree test: do grammatical-tier letter cords mark content cords via hierarchy?

Tests whether W:0 / AB:0 / MB:0 / KB:0 (zero-value grammatical cords) operate
as hierarchical markers (subsidiaries = suffixes on content parents) rather
than linear sequences.
"""
import sqlite3, csv, os, random
from collections import defaultdict, Counter

OUT = os.path.expanduser('~/workspace/quipu-analysis/tree-test')
os.makedirs(OUT, exist_ok=True)
DB = os.path.expanduser('~/workspace/quipu-analysis/okr-khipu.db')
LETTER_CSV = os.path.expanduser('~/workspace/quipu-analysis/ordinal-letters/letter_occurrences.csv')

LETTER_HEX = {'f8040000': 'W', '20040000': 'AB', 'a4040000': 'MB', '84040000': 'KB'}
LETTER_CORDS = {}   # cord_id -> letter

print("Loading letter occurrences...")
with open(LETTER_CSV) as f:
    rdr = csv.DictReader(f)
    khipu_ids = set()
    pending = []  # (khipu_id, token_index, letter)
    for r in rdr:
        khipu_ids.add(int(r['khipu_id']))
        if r['cord_id'].strip():
            LETTER_CORDS[int(r['cord_id'])] = r['letter']
        else:
            pending.append((int(r['khipu_id']), int(r['token_index']), r['letter']))
khipu_ids = sorted(khipu_ids)
print(f"  {len(LETTER_CORDS)} letter cords with IDs, {len(pending)} need ordinal mapping, {len(khipu_ids)} khipu")

conn = sqlite3.connect(DB)
c = conn.cursor()
ph = ','.join('?' * len(khipu_ids))

print("Loading cords...")
c.execute(f"""SELECT CORD_ID, KHIPU_ID, CORD_LEVEL, PENDANT_FROM, CORD_ORDINAL
              FROM cord WHERE KHIPU_ID IN ({ph})""", tuple(khipu_ids))
cords = {}
children = defaultdict(list)   # parent_cord_id -> [child cord_ids]
primary_of = {}                # khipu_id -> primary cord_id (PENDANT_FROM target at level 1)
for cid, kid, lvl, pf, co in c.fetchall():
    cords[cid] = {'khipu': kid, 'level': lvl, 'parent': pf, 'ordinal': co}
    if pf:
        children[pf].append(cid)
print(f"  {len(cords)} cords")

# resolve pending letter cords via (khipu_id, token_index) -> nth cord by CORD_ORDINAL
by_khipu_ord = defaultdict(list)
for cid, d in cords.items():
    by_khipu_ord[d['khipu']].append((d['ordinal'] if d['ordinal'] is not None else 0, cid))
for kid in by_khipu_ord:
    by_khipu_ord[kid].sort()
resolved = 0
for kid, tidx, letter in pending:
    ordered = by_khipu_ord.get(kid, [])
    if 0 <= tidx < len(ordered):
        LETTER_CORDS[ordered[tidx][1]] = letter
        resolved += 1
print(f"  resolved {resolved}/{len(pending)} ordinal-mapped letter cords")
print(f"  total letter cords: {len(LETTER_CORDS)}")

# primary cord ids: the PENDANT_FROM value shared by level-1 cords
primaries = set()
for cid, d in cords.items():
    if d['level'] == 1 and d['parent']:
        primaries.add(d['parent'])

print("Loading colors...")
c.execute(f"""SELECT CORD_ID, COLOR_CD_1 FROM ascher_cord_color
              WHERE CORD_ID IN (SELECT CORD_ID FROM cord WHERE KHIPU_ID IN ({ph}))""", tuple(khipu_ids))
colors = {cid: col for cid, col in c.fetchall()}

print("Loading knot clusters...")
c.execute(f"""SELECT kc.CLUSTER_ID, kc.CORD_ID, kc.ORDINAL, kc.START_POS
              FROM knot_cluster kc JOIN cord co ON kc.CORD_ID = co.CORD_ID
              WHERE co.KHIPU_ID IN ({ph})""", tuple(khipu_ids))
clusters = defaultdict(list)  # cord_id -> [(cl_id, ordinal, start_pos)]
for cl_id, cid, ordinal, sp in c.fetchall():
    clusters[cid].append((cl_id, ordinal, sp if sp is not None else 0))

print("Loading knots...")
c.execute(f"""SELECT k.CLUSTER_ID, k.TYPE_CODE, k.NUM_TURNS
              FROM knot k JOIN knot_cluster kc ON k.CLUSTER_ID = kc.CLUSTER_ID
              JOIN cord co ON kc.CORD_ID = co.CORD_ID
              WHERE co.KHIPU_ID IN ({ph})""", tuple(khipu_ids))
knot_groups = defaultdict(Counter)  # cluster_id -> Counter[(type, turns)]
for cl_id, tcode, turns in c.fetchall():
    knot_groups[cl_id][(tcode, turns)] += 1
print(f"  {len(clusters)} cords with clusters, {len(knot_groups)} knot groups")

def decode_value(cid):
    """Replicate decoder.py logic using preloaded dicts. Returns (value, confidence)."""
    cls = clusters.get(cid)
    if not cls:
        return 0, 'high'  # empty cord = 0
    # units cluster nearest free end = largest START_POS
    cls = sorted(cls, key=lambda x: -x[2])
    value = 0
    confidence = 'high'
    for place, (cl_id, ordinal, sp) in enumerate(cls):
        knots = knot_groups.get(cl_id, Counter())
        digit = 0
        if place == 0:
            total = sum(knots.values())
            if total == 0:
                digit = 0
            elif len(knots) == 1:
                (tcode, turns), n = next(iter(knots.items()))
                if tcode in ('L', 'SP', 'LL', 'BL') and n == 1:
                    if turns is None or turns == 0 or turns > 9 or turns < 1:
                        return None, 'low'
                    digit = int(turns)
                    if digit < 2:
                        confidence = 'medium'
                elif tcode in ('E', 'EE') and n == 1:
                    digit = 1
                elif tcode == 'S':
                    confidence = 'low'; digit = 0
                elif tcode == 'TF':
                    confidence = 'medium'; digit = 0
                else:
                    confidence = 'low'; digit = 0
            else:
                return None, 'low'
        else:
            for (tcode, turns), n in knots.items():
                if tcode == 'S':
                    digit += n
                elif tcode == 'TF':
                    digit += n
                    if confidence == 'high':
                        confidence = 'medium'
                else:
                    confidence = 'low'
        value += digit * (10 ** place)
    return value, confidence

print("Decoding all cord values...")
values = {}
for cid in cords:
    v, conf = decode_value(cid)
    values[cid] = (v, conf)
n_val = sum(1 for v, _ in values.values() if v)
print(f"  decoded, {n_val} nonzero")

# ---------- TEST 1: attachment census ----------
print("\nTEST 1: attachment census")
rows = []
for cid, letter in LETTER_CORDS.items():
    d = cords.get(cid)
    if not d:
        continue
    lvl = d['level']
    pid = d['parent']
    is_primary_target = pid in primaries
    # parent info
    pinfo = cords.get(pid) if pid else None
    parent_is_content = False
    parent_hex = ''
    parent_val = ''
    parent_color = ''
    if pinfo and pid not in primaries:
        pv, _ = values.get(pid, (None, None))
        parent_val = pv
        parent_color = colors.get(pid, '')
        parent_hex = f"{parent_color}:{pv}"
        # content = nonzero value OR has knots but not a letter cord
        parent_is_content = (pv not in (None, 0)) or (pid in clusters and pid not in LETTER_CORDS)
    subs = children.get(cid, [])
    sub_hexes = []
    for s in subs:
        sv, _ = values.get(s, (None, None))
        sub_hexes.append(f"{colors.get(s,'')}:{sv}")
    rows.append({
        'letter': letter, 'cord_id': cid, 'khipu_id': d['khipu'],
        'level': lvl, 'parent_id': pid,
        'parent_is_primary': is_primary_target,
        'parent_is_content': parent_is_content,
        'parent_color': parent_color, 'parent_value': parent_val,
        'n_subsidiaries': len(subs),
        'subsidiary_hexes': ';'.join(sub_hexes[:10]),
    })

with open(f'{OUT}/attachment_census.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)
print(f"  wrote {len(rows)} rows")

# summary by letter
for L in 'WAMB':
    lr = [r for r in rows if r['letter'] == ('K' if L == 'K' else L)]
for L in ['W', 'A', 'M', 'K']:
    lr = [r for r in rows if r['letter'] == L]
    n = len(lr)
    n_sub_of_content = sum(1 for r in lr if r['parent_is_content'])
    n_top = sum(1 for r in lr if r['parent_is_primary'])
    n_with_subs = sum(1 for r in lr if r['n_subsidiaries'] > 0)
    lvlc = Counter(r['level'] for r in lr)
    print(f"  {L}: n={n} subsidiary_of_content={n_sub_of_content} ({n_sub_of_content/max(n,1)*100:.1f}%) "
          f"top_level={n_top} has_subs={n_with_subs} levels={dict(lvlc)}")

# ---------- TEST 3: hierarchy test with permutation null ----------
print("\nTEST 3: hierarchy test (Quechua suffix prediction)")
# observed: fraction of letter cords that are subsidiaries of content cords
obs = sum(1 for r in rows if r['parent_is_content']) / max(len(rows), 1)
print(f"  observed P(letter is subsidiary of content) = {obs:.4f}")

# null: within each khipu, shuffle parent links among non-primary cords, recompute
random.seed(42)
khipu_cords = defaultdict(list)
for cid, d in cords.items():
    if d['parent'] not in primaries and d['parent']:  # has a real parent
        khipu_cords[d['khipu']].append(cid)

null_vals = []
N_PERM = 200
letter_set = set(LETTER_CORDS)
for it in range(N_PERM):
    hits = 0; tot = 0
    for kid, cids in khipu_cords.items():
        parents = [cords[x]['parent'] for x in cids]
        random.shuffle(parents)
        for x, p in zip(cids, parents):
            if x in letter_set:
                tot += 1
                pv, _ = values.get(p, (None, None))
                if pv not in (None, 0) or (p in clusters and p not in letter_set):
                    hits += 1
    null_vals.append(hits / max(tot, 1))
    if it % 50 == 0:
        print(f"  perm {it}: {null_vals[-1]:.4f}")
import statistics
mn, sd = statistics.mean(null_vals), statistics.stdev(null_vals)
p_val = sum(1 for v in null_vals if v >= obs) / N_PERM
print(f"  null mean={mn:.4f} sd={sd:.4f}; p(one-sided, obs>=null)={p_val:.4f}")

with open(f'{OUT}/hierarchy_test.md', 'w') as f:
    f.write("# Hierarchy test: are letter cords suffixes on content parents?\n\n")
    f.write("Quechua prediction: case/evidential/plural are suffixes ON the noun.\n")
    f.write("Khipu analogue: letter cord should be subsidiary of a content cord.\n\n")
    f.write(f"- Observed P(letter subsidiary of content cord): **{obs:.4f}**\n")
    f.write(f"- Null (shuffled parent links within khipu, {N_PERM} perms): mean={mn:.4f}, sd={sd:.4f}\n")
    f.write(f"- One-sided p-value: {p_val:.4f}\n\n")
    if p_val < 0.01 and obs > mn:
        f.write("VERDICT: SUPPORTED. Letter cords attach to content cords above chance.\n")
    elif p_val < 0.05 and obs > mn:
        f.write("VERDICT: WEAKLY SUPPORTED.\n")
    else:
        f.write("VERDICT: NOT SUPPORTED. Letter cords do not preferentially attach to content cords.\n")

# ---------- TEST 2: marking test ----------
print("\nTEST 2: marking test (marked vs unmarked content cords)")
# content cords = nonzero value, not letter cords
marked = defaultdict(list)    # letter -> [content cord ids with that letter as subsidiary]
unmarked = []
for cid, d in cords.items():
    if cid in LETTER_CORDS:
        continue
    v, conf = values.get(cid, (None, None))
    if v in (None, 0):
        continue
    subs = children.get(cid, [])
    letter_subs = [s for s in subs if s in LETTER_CORDS]
    if letter_subs:
        for s in letter_subs:
            marked[LETTER_CORDS[s]].append(cid)
    else:
        unmarked.append(cid)

print(f"  unmarked content cords: {len(unmarked)}")
for L in ['W', 'A', 'M', 'K']:
    print(f"  marked by {L}: {len(set(marked[L]))}")

def stats(cids):
    vals = [values[x][0] for x in cids if values[x][0] is not None]
    lvls = [cords[x]['level'] for x in cids]
    cols = Counter(colors.get(x, '?') for x in cids)
    if not vals:
        return None
    sv = sorted(vals)
    return {'n': len(vals), 'median': sv[len(sv)//2],
            'mean': sum(vals)/len(vals),
            'mean_level': sum(lvls)/len(lvls),
            'n_colors': len(cols), 'top_colors': cols.most_common(3)}

with open(f'{OUT}/marking_test.md', 'w') as f:
    f.write("# Marking test: do letter-marked content cords differ from unmarked?\n\n")
    us = stats(unmarked)
    f.write(f"## Unmarked content cords (n={us['n'] if us else 0})\n")
    if us:
        f.write(f"- median value: {us['median']}, mean value: {us['mean']:.1f}\n")
        f.write(f"- mean level: {us['mean_level']:.2f}, distinct colors: {us['n_colors']}\n")
        f.write(f"- top colors: {us['top_colors']}\n\n")
    for L, gloss in [('W','-ta/ACC'), ('A','-mi/EVD'), ('M','-kuna/PL'), ('K','TBD')]:
        ms = stats(list(set(marked[L])))
        f.write(f"## Marked by {L} ({gloss}), n={ms['n'] if ms else 0}\n")
        if ms and us:
            f.write(f"- median value: {ms['median']} (unmarked: {us['median']})\n")
            f.write(f"- mean value: {ms['mean']:.1f} (unmarked: {us['mean']:.1f})\n")
            f.write(f"- mean level: {ms['mean_level']:.2f} (unmarked: {us['mean_level']:.2f})\n")
            f.write(f"- distinct colors: {ms['n_colors']} (unmarked: {us['n_colors']})\n")
            f.write(f"- top colors: {ms['top_colors']}\n\n")
    f.write("Interpretation: systematic differences suggest the letter marks a distinct\n")
    f.write("grammatical role; no differences suggest letters are not content-markers.\n")

# ---------- TEST 4: stacking ----------
print("\nTEST 4: stacking analysis")
stack_counts = Counter()   # n letter-subs -> n content cords
stack_combos = Counter()   # frozenset of letters -> count
stack_orders = Counter()   # tuple of letters by ordinal -> count
for cid, d in cords.items():
    if cid in LETTER_CORDS:
        continue
    v, _ = values.get(cid, (None, None))
    if v in (None, 0):
        continue
    subs = children.get(cid, [])
    ls = [(LETTER_CORDS[s], cords[s]['ordinal']) for s in subs if s in LETTER_CORDS]
    if not ls:
        continue
    stack_counts[len(ls)] += 1
    stack_combos[tuple(sorted(l for l, _ in ls))] += 1
    by_ord = tuple(l for l, _ in sorted(ls, key=lambda x: x[1]))
    stack_orders[by_ord] += 1

print(f"  stack depth distribution: {dict(stack_counts)}")
print(f"  top combos: {stack_combos.most_common(10)}")
print(f"  top orders: {stack_orders.most_common(10)}")

with open(f'{OUT}/stacking_analysis.md', 'w') as f:
    f.write("# Stacking analysis: multiple letter subsidiaries on one content cord\n\n")
    f.write("Quechua prediction: noun + PL + CASE + EVD stacking -> up to 3 letter subsidiaries\n")
    f.write("with inner-to-outer order M < W < A (plural inner, case middle, evidential outer).\n\n")
    f.write(f"## Depth distribution: {dict(stack_counts)}\n\n")
    f.write("## Most common letter combinations:\n")
    for combo, n in stack_combos.most_common(15):
        f.write(f"- {'+'.join(combo)}: {n}\n")
    f.write("\n## Most common ordinal orders (by cord position):\n")
    for order, n in stack_orders.most_common(15):
        f.write(f"- {' -> '.join(order)}: {n}\n")
    f.write("\n## Verdict\n")
    multi = sum(n for d, n in stack_counts.items() if d >= 2)
    tot = sum(stack_counts.values())
    f.write(f"Content cords with 2+ letter subsidiaries: {multi}/{tot} ({multi/max(tot,1)*100:.1f}%)\n")
    # check M<W<A order among 3-stacks
    f.write("Quechua suffix order M<W<A test: see orders above.\n")

# ---------- final report ----------
with open(f'{OUT}/tree_report.md', 'w') as f:
    f.write("# Tree test report: hierarchical marking hypothesis\n\n")
    f.write("Follow-up to the killed linear-sequential hypothesis.\n")
    f.write("Question: do letter cords mark content cords via parent-subsidiary attachment?\n\n")
    f.write(f"## Attachment census ({len(rows)} letter cords)\n\n")
    for L in ['W', 'A', 'M', 'K']:
        lr = [r for r in rows if r['letter'] == L]
        n = len(lr)
        ns = sum(1 for r in lr if r['parent_is_content'])
        nt = sum(1 for r in lr if r['parent_is_primary'])
        nh = sum(1 for r in lr if r['n_subsidiaries'] > 0)
        f.write(f"- {L}: n={n}, subsidiary_of_content={ns} ({ns/max(n,1)*100:.1f}%), "
                f"top_level={nt}, has_subsidiaries={nh}\n")
    f.write(f"\n## Hierarchy test\n- observed={obs:.4f}, null mean={mn:.4f} (sd {sd:.4f}), p={p_val:.4f}\n")
    f.write("\n## Stacking\n")
    f.write(f"- depth distribution: {dict(stack_counts)}\n")
    f.write("\nSee marking_test.md, hierarchy_test.md, stacking_analysis.md for detail.\n")

print(f"\nDone. Outputs in {OUT}")
conn.close()
