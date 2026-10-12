"""Cross-tabulate khipu grammatical structure against archaeological site/provenance."""
import sqlite3
import sys
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from decoder import decode_cord
from collections import Counter, defaultdict
import statistics

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
GRAMMATICAL = {'W', 'AB', 'MB', 'KB'}

conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row
c = conn.cursor()

# Load cluster assignments
unclass = {}  # khipu_id -> cluster_name
with open('/home/hatch/workspace/quipu-analysis/khipu-clusters-2026-10-11.csv') as f:
    for line in f:
        if line.startswith('#') or line.startswith('KHIPU'):
            continue
        parts = line.strip().split(',')
        if len(parts) >= 3 and parts[2] in ('deep_sparse_mixed', 'large_value_flat'):
            unclass[int(parts[0])] = parts[2]

print(f"Unclassified khipu: {len(unclass)}", file=sys.stderr)

# Get provenance + all cord data in bulk
ids = list(unclass.keys())
placeholders = ','.join('?' * len(ids))
c.execute(f"SELECT KHIPU_ID, PROVENANCE, REGION FROM khipu_main WHERE KHIPU_ID IN ({placeholders})", ids)
prov_map = {r['KHIPU_ID']: (r['PROVENANCE'] or 'unknown', r['REGION'] or '') for r in c.fetchall()}

# Bulk cord data
c.execute(f"""
    SELECT co.KHIPU_ID, co.CORD_ID, co.CORD_LEVEL, cc.COLOR_CD_1, cc.COLOR_CD_2
    FROM cord co
    LEFT JOIN ascher_cord_color cc ON co.CORD_ID = cc.CORD_ID
    WHERE co.KHIPU_ID IN ({placeholders})
""", ids)
cords_by_khipu = defaultdict(list)
for r in c.fetchall():
    color = r['COLOR_CD_1'] or '?'
    if r['COLOR_CD_2']:
        color = f"{r['COLOR_CD_1']}:{r['COLOR_CD_2']}"
    cords_by_khipu[r['KHIPU_ID']].append({
        'cord_id': r['CORD_ID'],
        'level': r['CORD_LEVEL'] or 1,
        'color': color,
        'base_color': r['COLOR_CD_1'] or '?',
    })

# Bulk twist data
c.execute(f"""
    SELECT k.CORD_ID, k.DIRECTION
    FROM knot k
    JOIN cord co ON k.CORD_ID = co.CORD_ID
    WHERE co.KHIPU_ID IN ({placeholders}) AND k.DIRECTION IS NOT NULL AND k.DIRECTION != ''
""", ids)
twist_by_cord = defaultdict(Counter)
for r in c.fetchall():
    twist_by_cord[r['CORD_ID']][r['DIRECTION']] += 1

# Decode all cords (cache)
import json, os
cache_path = '/tmp/decode_cache.json'
decode_cache = {}
if os.path.exists(cache_path):
    decode_cache = {int(k): v for k, v in json.load(open(cache_path)).items()}

def get_value(cord_id):
    if cord_id not in decode_cache:
        try:
            r = decode_cord(conn, cord_id)
            decode_cache[cord_id] = r['value']
        except Exception:
            decode_cache[cord_id] = None
    return decode_cache[cord_id]

# Per-khipu profiles
profiles = {}
for khipu_id, cords in cords_by_khipu.items():
    values = []
    for cd in cords:
        v = get_value(cd['cord_id'])
        cd['value'] = v
        if v is not None:
            values.append(v)
    
    n = len(cords)
    n_decoded = len(values)
    
    if values:
        med = statistics.median(values)
        mx = max(values)
        pct_zero = sum(1 for v in values if v == 0) / len(values) * 100
        pct_cat = sum(1 for v in values if 0 <= v <= 3) / len(values) * 100  # categorical range
        pct_quant = sum(1 for v in values if v >= 4) / len(values) * 100
    else:
        med = mx = pct_zero = pct_cat = pct_quant = None
    
    # Color tiers
    n_gram = sum(1 for cd in cords if cd['base_color'] in GRAMMATICAL)
    n_dist = sum(1 for cd in cords if cd['base_color'] not in GRAMMATICAL and cd['base_color'] != '?')
    n_colored = n_gram + n_dist
    pct_gram = n_gram / n_colored * 100 if n_colored else None
    n_distinct_colors = len(set(cd['base_color'] for cd in cords if cd['base_color'] != '?'))
    
    # Depth
    levels = [cd['level'] for cd in cords]
    max_level = max(levels) if levels else None
    mean_level = statistics.mean(levels) if levels else None
    
    # Twist
    twist_counts = Counter()
    for cd in cords:
        tc = twist_by_cord.get(cd['cord_id'], Counter())
        if tc:
            dominant = tc.most_common(1)[0][0]
            twist_counts[dominant] += 1
    n_twist = sum(twist_counts.values())
    twist_pct = {d: twist_counts[d] / n_twist * 100 for d in twist_counts} if n_twist else {}
    
    profiles[khipu_id] = {
        'cluster': unclass[khipu_id],
        'provenance': prov_map.get(khipu_id, ('unknown', ''))[0],
        'n_cords': n,
        'n_decoded': n_decoded,
        'median_val': med,
        'max_val': mx,
        'pct_zero': pct_zero,
        'pct_categorical': pct_cat,
        'pct_quantitative': pct_quant,
        'pct_grammatical': pct_gram,
        'n_distinct_colors': n_distinct_colors,
        'max_level': max_level,
        'mean_level': mean_level,
        'twist_z': twist_pct.get('Z', 0),
        'twist_s': twist_pct.get('S', 0),
        'twist_u': twist_pct.get('U', 0),
    }

# Save decode cache
json.dump({str(k): v for k, v in decode_cache.items()}, open(cache_path, 'w'))

# Save profiles
json.dump({str(k): v for k, v in profiles.items()}, open('/tmp/site_profiles.json', 'w'), indent=1)
print(f"Profiles computed: {len(profiles)}", file=sys.stderr)

# --- ANALYSIS 1: Value profile by site ---
print("\n" + "="*70)
print("ANALYSIS 1: VALUE PROFILE BY SITE")
print("="*70)
site_profiles = defaultdict(list)
for kid, p in profiles.items():
    if p['pct_categorical'] is not None:
        site_profiles[p['provenance']].append(p)

print(f"\n{'Site':<45} {'n':>4} {'med_cat%':>9} {'med_zero%':>10} {'med_max':>8}")
print("-"*80)
site_cat = []
for site, plist in sorted(site_profiles.items(), key=lambda x: -len(x[1])):
    cats = [p['pct_categorical'] for p in plist]
    zeros = [p['pct_zero'] for p in plist]
    maxes = [p['max_val'] for p in plist if p['max_val'] is not None]
    mc = statistics.median(cats)
    mz = statistics.median(zeros)
    mm = statistics.median(maxes) if maxes else 0
    site_cat.append((site, len(plist), mc, mz, mm))
    flag = " *" if len(plist) < 5 else ""
    print(f"{site[:43]:<45} {len(plist):>4} {mc:>8.1f}% {mz:>9.1f}% {mm:>8.0f}{flag}")

# --- ANALYSIS 2: Channel weighting by site ---
print("\n" + "="*70)
print("ANALYSIS 2: CHANNEL WEIGHTING BY SITE (sites with 5+ khipu)")
print("="*70)
print(f"\n{'Site':<40} {'n':>3} {'gram%':>6} {'colors':>7} {'maxlvl':>7} {'Z%':>5} {'S%':>5} {'U%':>5}")
print("-"*80)
for site, plist in sorted(site_profiles.items(), key=lambda x: -len(x[1])):
    if len(plist) < 5:
        continue
    grams = [p['pct_grammatical'] for p in plist if p['pct_grammatical'] is not None]
    ncols = [p['n_distinct_colors'] for p in plist]
    mlvls = [p['max_level'] for p in plist if p['max_level']]
    tzs = [p['twist_z'] for p in plist]
    tss = [p['twist_s'] for p in plist]
    tus = [p['twist_u'] for p in plist]
    mg = statistics.median(grams) if grams else 0
    mc = statistics.median(ncols) if ncols else 0
    ml = statistics.median(mlvls) if mlvls else 0
    mz_ = statistics.median(tzs)
    ms_ = statistics.median(tss)
    mu_ = statistics.median(tus)
    print(f"{site[:38]:<40} {len(plist):>3} {mg:>5.1f}% {mc:>7.0f} {ml:>7.1f} {mz_:>4.0f}% {ms_:>4.0f}% {mu_:>4.0f}%")

# --- ANALYSIS 3: Cluster x Site ---
print("\n" + "="*70)
print("ANALYSIS 3: CLUSTER x SITE MATRIX")
print("="*70)
clusters = sorted(set(unclass.values()))
sites_top = [s for s, pl in sorted(site_profiles.items(), key=lambda x: -len(x[1]))[:10]]
print(f"\n{'Site':<40}" + "".join(f"{cl[:18]:>20}" for cl in clusters))
print("-"*80)
for site in sites_top:
    plist = site_profiles[site]
    counts = Counter(p['cluster'] for p in plist)
    row = f"{site[:38]:<40}"
    for cl in clusters:
        row += f"{counts.get(cl, 0):>20}"
    print(row)

# --- ANALYSIS 4: Checklist-like ---
print("\n" + "="*70)
print("ANALYSIS 4: CHECKLIST-LIKE KHIPU")
print("Definition: >50% cords values 0-3 AND >30% zero AND <5 distinct colors")
print("="*70)
checklist = []
for kid, p in profiles.items():
    if (p['pct_categorical'] is not None and p['pct_categorical'] > 50
        and p['pct_zero'] is not None and p['pct_zero'] > 30
        and p['n_distinct_colors'] is not None and p['n_distinct_colors'] < 5
        and p['n_decoded'] >= 5):
        checklist.append((kid, p))

print(f"\nChecklist-like khipu: {len(checklist)} / {len(profiles)}")
if checklist:
    print(f"\n{'ID':<10} {'Site':<35} {'cat%':>6} {'zero%':>6} {'colors':>7} {'n_cords':>8}")
    print("-"*75)
    site_dist = Counter()
    for kid, p in sorted(checklist, key=lambda x: -x[1]['pct_categorical']):
        print(f"{kid:<10} {p['provenance'][:33]:<35} {p['pct_categorical']:>5.0f}% {p['pct_zero']:>5.0f}% {p['n_distinct_colors']:>7} {p['n_cords']:>8}")
        site_dist[p['provenance']] += 1
    print(f"\nSite distribution of checklist-like:")
    for site, n in site_dist.most_common():
        print(f"  {site}: {n}")

# --- ANALYSIS 5: Site fingerprints ---
print("\n" + "="*70)
print("ANALYSIS 5: SITE FINGERPRINTS (major sites vs corpus average)")
print("="*70)
# Corpus averages
all_p = [p for p in profiles.values() if p['pct_categorical'] is not None]
corpus_cat = statistics.median([p['pct_categorical'] for p in all_p])
corpus_zero = statistics.median([p['pct_zero'] for p in all_p])
corpus_gram = statistics.median([p['pct_grammatical'] for p in all_p if p['pct_grammatical'] is not None])
corpus_max = statistics.median([p['max_val'] for p in all_p if p['max_val'] is not None])
corpus_lvl = statistics.median([p['max_level'] for p in all_p if p['max_level']])
corpus_ncol = statistics.median([p['n_distinct_colors'] for p in all_p])
print(f"\nCorpus medians: cat%={corpus_cat:.0f} zero%={corpus_zero:.0f} gram%={corpus_gram:.0f} max={corpus_max:.0f} maxlvl={corpus_lvl:.0f} ncolors={corpus_ncol:.0f}")

for site in ['Pachacamac', 'Incahuasi', 'Ica', 'Nazca']:
    plist = site_profiles.get(site, [])
    if len(plist) < 4:
        print(f"\n{site}: n={len(plist)} — too few for fingerprint")
        continue
    sc = statistics.median([p['pct_categorical'] for p in plist])
    sz = statistics.median([p['pct_zero'] for p in plist])
    sg = statistics.median([p['pct_grammatical'] for p in plist if p['pct_grammatical'] is not None])
    sm = statistics.median([p['max_val'] for p in plist if p['max_val'] is not None])
    sl = statistics.median([p['max_level'] for p in plist if p['max_level']])
    sn = statistics.median([p['n_distinct_colors'] for p in plist])
    # Distinctive colors at this site
    print(f"\n{site} (n={len(plist)}):")
    print(f"  cat%={sc:.0f} (corpus {corpus_cat:.0f})  zero%={sz:.0f} (corpus {corpus_zero:.0f})")
    print(f"  gram%={sg:.0f} (corpus {corpus_gram:.0f})  max={sm:.0f} (corpus {corpus_max:.0f})")
    print(f"  maxlvl={sl:.0f} (corpus {corpus_lvl:.0f})  ncolors={sn:.0f} (corpus {corpus_ncol:.0f})")

print("\nDone.", file=sys.stderr)
