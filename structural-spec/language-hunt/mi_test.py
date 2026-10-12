"""Refined language-likeness: sequential dependency test.

Key discriminator: in LANGUAGE, adjacent units are statistically dependent
(grammar constrains what follows what). In SPREADSHEETS, rows are independent.

Measure: mutual information between adjacent cord tokens vs shuffled baseline.
High MI = sequential structure (language-like). Low MI = independent rows (table-like).

Also: non-numeric content. Language-encoding khipu might use knots/colors
as SYMBOLS, not numbers. Flag khipu with high % of non-decodable or
non-numeric knot patterns.
"""
import csv, math, os, random
from collections import Counter

BASE = os.path.expanduser('~/workspace/quipu-analysis')
HEXCORPUS = os.path.join(BASE, 'byte-patterns/hex-corpus')

def load_hex(khipu_id):
    p = os.path.join(HEXCORPUS, f'{khipu_id}.hex')
    if not os.path.exists(p):
        return []
    s = open(p).read().strip()
    body = s[16:]
    return [body[i:i+8] for i in range(0, len(body), 8) if len(body[i:i+8]) == 8]

def adj_mutual_info(tokens):
    """Mutual information between adjacent tokens (in bits)."""
    if len(tokens) < 10:
        return 0.0
    pairs = [(tokens[i], tokens[i+1]) for i in range(len(tokens)-1)]
    n = len(pairs)
    px = Counter(t for t, _ in pairs)
    py = Counter(t for _, t in pairs)
    pxy = Counter(pairs)
    mi = 0.0
    for (x, y), c in pxy.items():
        p_xy = c / n
        p_x = px[x] / n
        p_y = py[y] / n
        mi += p_xy * math.log2(p_xy / (p_x * p_y))
    return mi

def shuffled_mi(tokens, trials=5):
    """MI after shuffling (baseline for independence)."""
    if len(tokens) < 10:
        return 0.0
    total = 0.0
    for _ in range(trials):
        sh = tokens[:]
        random.seed(42)
        random.shuffle(sh)
        total += adj_mutual_info(sh)
    return total / trials

def main():
    cands = []
    with open(os.path.join(BASE, 'language-hunt/language_positive.csv')) as f:
        for row in csv.DictReader(f):
            cands.append(row)

    print(f"{'khipu':>10} {'n':>5} {'MI_obs':>8} {'MI_shuf':>8} {'MI_ratio':>8}  prov")
    results = []
    for cand in cands:
        kid = cand['khipu_id']
        toks = load_hex(kid)
        if len(toks) < 20:
            continue
        mi_obs = adj_mutual_info(toks)
        mi_shuf = shuffled_mi(toks)
        ratio = mi_obs / mi_shuf if mi_shuf > 0.001 else 0
        results.append({
            **cand,
            'mi_obs': round(mi_obs, 3),
            'mi_shuf': round(mi_shuf, 3),
            'mi_ratio': round(ratio, 3),
        })
        print(f"{kid:>10} {len(toks):>5} {mi_obs:>8.3f} {mi_shuf:>8.3f} {ratio:>8.2f}  {cand['provenance'][:40]}")

    results.sort(key=lambda r: -r['mi_ratio'])
    print("\n--- Top 15 by MI ratio (sequential dependency) ---")
    for r in results[:15]:
        print(f"{r['khipu_id']:>10} ratio={r['mi_ratio']:.2f} MI={r['mi_obs']:.3f} n={r['n_cords']} ent={r['entropy']} prov={r['provenance'][:40]}")

    with open(os.path.join(BASE, 'language-hunt/mi_analysis.csv'), 'w', newline='') as f:
        if results:
            w = csv.DictWriter(f, fieldnames=results[0].keys())
            w.writeheader(); w.writerows(results)

if __name__ == '__main__':
    main()
