"""Fixed neighbor indexing + trigram/fixed-expression test for markers."""
import pickle, csv, os
from collections import Counter, defaultdict

BASE = os.path.expanduser('~/workspace/quipu-analysis')
OUT = os.path.join(BASE, 'marker-words')
MARKERS = {22, 23, 32, 33, 34}

with open(os.path.join(BASE, 'templates/cache.pkl'), 'rb') as f:
    cache = pickle.load(f)

# Rebuild occurrences with CORRECT neighbor indexing
# neigh list = [n-3, n-2, n-1, SELF(None), n+1, n+2, n+3] -> idx 0..6, self at 3
occurrences = []
for kid, cords in cache.items():
    sc = sorted(cords, key=lambda t: t[0])
    n = len(sc)
    colors = [(t[2] or '?').strip() for t in sc]
    for i, t in enumerate(sc):
        ordinal, level, color1, color2, value = t
        if value in MARKERS:
            own = (color1 or '?').strip()
            def cn(j):
                return colors[j] if 0 <= j < n else None
            occurrences.append({
                'khipu_id': kid, 'value': value, 'own_color': own,
                'prev3': cn(i-3), 'prev2': cn(i-2), 'prev1': cn(i-1),
                'next1': cn(i+1), 'next2': cn(i+2), 'next3': cn(i+3),
            })

print(f"Total: {len(occurrences)} occurrences")

# ---- Trigram test: (prev1_color, marker_value, next1_color) ----
# If markers are fixed expressions, specific trigrams should dominate
for mv in sorted(MARKERS):
    occ = [o for o in occurrences if o['value'] == mv]
    # own+next bigram: what follows (own_color=mv)?
    own_next = Counter((o['own_color'], o['next1']) for o in occ if o['next1'])
    # prev+own bigram: what precedes?
    prev_own = Counter((o['prev1'], o['own_color']) for o in occ if o['prev1'])
    # full trigram
    tri = Counter((o['prev1'], o['own_color'], o['next1']) for o in occ
                    if o['prev1'] and o['next1'])
    n = len(occ)
    print(f"\n=== Marker {mv} ({n} occ) ===")
    print(f"  top (own->next): {own_next.most_common(5)}")
    print(f"  top (prev->own): {prev_own.most_common(5)}")
    top_tri, top_tri_n = tri.most_common(1)[0] if tri else (('-','-','-'), 0)
    print(f"  top trigram: {top_tri} = {top_tri_n}/{n} ({100*top_tri_n/n:.1f}%)")
    # concentration: what fraction in top 3 trigrams?
    top3 = sum(c for _, c in tri.most_common(3))
    print(f"  top-3 trigram coverage: {top3}/{n} ({100*top3/n:.1f}%)")
    # distinct trigrams
    print(f"  distinct trigrams: {len(tri)}")

# ---- Cross-khipu consistency: for marker 22, do the SAME trigrams recur across khipu? ----
print("\n\n=== Cross-khipu trigram recurrence (marker 22) ===")
occ22 = [o for o in occurrences if o['value'] == 22]
tri_by_khipu = defaultdict(Counter)
for o in occ22:
    if o['prev1'] and o['next1']:
        tri_by_khipu[o['khipu_id']][(o['prev1'], o['own_color'], o['next1'])] += 1
# Find trigrams appearing in multiple khipu
tri_khipu_count = Counter()
for kid, tc in tri_by_khipu.items():
    for tri in tc:
        tri_khipu_count[tri] += 1
print(f"Trigrams found in >1 khipu: {sum(1 for c in tri_khipu_count.values() if c > 1)}")
print("Most shared trigrams:")
for tri, nk in tri_khipu_count.most_common(10):
    total = sum(tc[tri] for tc in tri_by_khipu.values())
    print(f"  {tri}: in {nk} khipu, {total} total occ")

# ---- Same for 33 ----
print("\n=== Cross-khipu trigram recurrence (marker 33) ===")
occ33 = [o for o in occurrences if o['value'] == 33]
tri_by_khipu33 = defaultdict(Counter)
for o in occ33:
    if o['prev1'] and o['next1']:
        tri_by_khipu33[o['khipu_id']][(o['prev1'], o['own_color'], o['next1'])] += 1
tri_khipu_count33 = Counter()
for kid, tc in tri_by_khipu33.items():
    for tri in tc:
        tri_khipu_count33[tri] += 1
print(f"Trigrams found in >1 khipu: {sum(1 for c in tri_khipu_count33.values() if c > 1)}")
for tri, nk in tri_khipu_count33.most_common(10):
    total = sum(tc[tri] for tc in tri_by_khipu33.values())
    print(f"  {tri}: in {nk} khipu, {total} total occ")
