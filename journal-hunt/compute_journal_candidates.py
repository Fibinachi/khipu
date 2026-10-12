"""Find khipu like 1000183 (sequential journal/log documents).

Computes MI ratio for full corpus, then filters:
  - MI ratio > 1.3 (sequential order matters)
  - Stratification score < 0.7 (not spreadsheet)
  - Value variance > 0 (numeric info present, not constant like 1000331)
  - Zero-value % < 70% (journals record events)
Ranks by similarity to 1000183.
"""
import csv, math, os, random, sqlite3, sys
from collections import Counter

BASE = os.path.expanduser('~/workspace/quipu-analysis')
HEXCORPUS = os.path.join(BASE, 'byte-patterns/hex-corpus')
OUTDIR = os.path.join(BASE, 'journal-hunt')
os.makedirs(OUTDIR, exist_ok=True)
sys.path.insert(0, BASE)
from decoder import decode_cord

def load_hex(khipu_id):
    p = os.path.join(HEXCORPUS, f'{khipu_id}.hex')
    if not os.path.exists(p):
        return []
    s = open(p).read().strip()
    body = s[16:]
    return [body[i:i+8] for i in range(0, len(body), 8) if len(body[i:i+8]) == 8]

def adj_mutual_info(tokens):
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
        if p_x > 0 and p_y > 0 and p_xy > 0:
            mi += p_xy * math.log2(p_xy / (p_x * p_y))
    return mi

def shuffled_mi(tokens, trials=3):
    if len(tokens) < 10:
        return 0.0
    total = 0.0
    for t in range(trials):
        sh = tokens[:]
        rnd = random.Random(42 + t)
        rnd.shuffle(sh)
        total += adj_mutual_info(sh)
    return total / trials

def main():
    # All khipu with hex files
    kids = sorted(f[:-4] for f in os.listdir(HEXCORPUS) if f.endswith('.hex'))
    print(f"Computing MI for {len(kids)} khipu...", flush=True)

    # Stratification scores
    strat = {}
    with open(os.path.join(BASE, 'stratification/stratification_scores.csv')) as f:
        for r in csv.DictReader(f):
            try:
                strat[r['khipu_id']] = float(r['strat_score'])
            except (ValueError, TypeError):
                strat[r['khipu_id']] = None

    conn = sqlite3.connect(os.path.join(BASE, 'okr-khipu.db'))
    c = conn.cursor()

    results = []
    for i, kid in enumerate(kids):
        toks = load_hex(kid)
        if len(toks) < 20:
            continue
        mi_obs = adj_mutual_info(toks)
        mi_shuf = shuffled_mi(toks)
        ratio = mi_obs / mi_shuf if mi_shuf > 0.001 else 0.0

        # Value stats from DB
        c.execute("SELECT CORD_ID FROM cord WHERE KHIPU_ID = ?", (kid,))
        cord_ids = [r[0] for r in c.fetchall()]
        vals = []
        for cid in cord_ids:
            try:
                res = decode_cord(conn, cid)
                v = res.get('value')
                if v is not None:
                    vals.append(v)
            except Exception:
                pass
        n_vals = len(vals)
        zero_pct = sum(1 for v in vals if v == 0) / n_vals if n_vals else 1.0
        val_var = 0.0
        val_min, val_max = None, None
        if n_vals > 1:
            mean = sum(vals) / n_vals
            val_var = sum((v - mean) ** 2 for v in vals) / n_vals
            val_min, val_max = min(vals), max(vals)

        # Provenance
        c.execute("SELECT PROVENANCE, REGION, MUSEUM_NAME FROM khipu_main WHERE KHIPU_ID = ?",
                  (kid,))
        prow = c.fetchone()
        prov = prow[0] if prow and prow[0] else ''
        region = prow[1] if prow and prow[1] else ''
        museum = prow[2] if prow and prow[2] else ''

        # N colors
        c.execute("""SELECT COUNT(DISTINCT COLOR_CD_1) FROM ascher_cord_color cc
                     JOIN cord co ON cc.CORD_ID = co.CORD_ID
                     WHERE co.KHIPU_ID = ?""", (kid,))
        n_colors = c.fetchone()[0] or 0

        results.append({
            'khipu_id': kid, 'n_cords': len(toks),
            'mi_obs': round(mi_obs, 4), 'mi_shuf': round(mi_shuf, 4),
            'mi_ratio': round(ratio, 4),
            'strat_score': strat.get(kid),
            'n_vals': n_vals, 'zero_pct': round(zero_pct, 4),
            'val_var': round(val_var, 2),
            'val_min': val_min, 'val_max': val_max,
            'n_colors': n_colors,
            'provenance': prov, 'region': region, 'museum': museum,
        })
        if (i + 1) % 100 == 0:
            print(f"  {i+1}/{len(kids)} done", flush=True)

    conn.close()

    # Save full MI results
    with open(os.path.join(OUTDIR, 'mi_full_corpus.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=results[0].keys())
        w.writeheader(); w.writerows(results)

    # Filter: journal candidates
    def ok(r):
        ss = r['strat_score']
        return (r['mi_ratio'] > 1.3
                and (ss is None or ss < 0.7)
                and r['val_var'] > 0
                and r['zero_pct'] < 0.70)

    cands = [r for r in results if ok(r)]
    cands.sort(key=lambda r: -r['mi_ratio'])
    print(f"\nJournal candidates (MI>1.3, strat<0.7, var>0, zero<70%): {len(cands)}")
    for r in cands:
        print(f"  {r['khipu_id']}: MI={r['mi_ratio']:.3f} strat={r['strat_score']} "
              f"n={r['n_cords']} vals[{r['val_min']}-{r['val_max']}] zero={r['zero_pct']:.2f} "
              f"colors={r['n_colors']} {r['museum'][:30]}")

    # Similarity to 1000183
    ref = next((r for r in results if r['khipu_id'] == '1000183'), None)
    if ref:
        for r in cands:
            # normalized similarity components
            mi_sim = 1 - min(abs(r['mi_ratio'] - ref['mi_ratio']) / ref['mi_ratio'], 1)
            n_sim = 1 - min(abs(r['n_cords'] - ref['n_cords']) / ref['n_cords'], 1)
            rng = (r['val_max'] or 0) - (r['val_min'] or 0)
            ref_rng = (ref['val_max'] or 0) - (ref['val_min'] or 0)
            rng_sim = 1 - min(abs(rng - ref_rng) / max(ref_rng, 1), 1)
            col_sim = 1 - min(abs(r['n_colors'] - ref['n_colors']) / max(ref['n_colors'], 1), 1)
            r['similarity_to_1000183'] = round(
                0.35 * mi_sim + 0.25 * n_sim + 0.2 * rng_sim + 0.2 * col_sim, 4)
        cands.sort(key=lambda r: -r['similarity_to_1000183'])

    with open(os.path.join(OUTDIR, 'journal_candidates.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cands[0].keys() if cands else [])
        w.writeheader(); w.writerows(cands)

    print(f"\nWrote {os.path.join(OUTDIR, 'journal_candidates.csv')}")

if __name__ == '__main__':
    main()
