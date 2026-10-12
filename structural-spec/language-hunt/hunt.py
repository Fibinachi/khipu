"""Find khipu that fail spreadsheet tests but show language-like sequential structure.

Step 1: Load residuals (147 unclassified khipu).
Step 2: Apply spreadsheet-NEGATIVE filter (remove stratified, zero-heavy, column-repetitive).
Step 3: Apply language-POSITIVE scoring (uniqueness, hapax, entropy).
Step 4: Rank and report top candidates.
"""
import csv, math, os
from collections import Counter

BASE = os.path.expanduser('~/workspace/quipu-analysis')
HEXCORPUS = os.path.join(BASE, 'byte-patterns/hex-corpus')

def load_hex(khipu_id):
    """Return list of 8-char cord tokens (header stripped)."""
    p = os.path.join(HEXCORPUS, f'{khipu_id}.hex')
    if not os.path.exists(p):
        return []
    s = open(p).read().strip()
    body = s[16:]  # strip 8-byte header
    return [body[i:i+8] for i in range(0, len(body), 8) if len(body[i:i+8]) == 8]

def cord_value(tok):
    """Last 4 hex chars = big-endian uint16 value."""
    return int(tok[4:8], 16)

def shannon_entropy(tokens):
    if not tokens:
        return 0.0
    c = Counter(tokens)
    n = len(tokens)
    return -sum((v/n) * math.log2(v/n) for v in c.values())

def max_run(tokens):
    """Longest run of identical adjacent tokens."""
    if not tokens:
        return 0
    best, cur = 1, 1
    for i in range(1, len(tokens)):
        if tokens[i] == tokens[i-1]:
            cur += 1
            best = max(best, cur)
        else:
            cur = 1
    return best

def ngram_uniqueness(tokens, n=2):
    """% of n-cord n-grams (as joined hex) that occur exactly once."""
    if len(tokens) < n:
        return 1.0
    grams = [''.join(tokens[i:i+n]) for i in range(len(tokens)-n+1)]
    c = Counter(grams)
    hapax = sum(1 for v in c.values() if v == 1)
    return hapax / len(grams) if grams else 1.0

def hapax_rate(tokens):
    """% of cord tokens occurring exactly once in this khipu."""
    if not tokens:
        return 0.0
    c = Counter(tokens)
    return sum(1 for v in c.values() if v == 1) / len(c)

def zero_pct(tokens):
    if not tokens:
        return 0.0
    return sum(1 for t in tokens if cord_value(t) == 0) / len(tokens)

def main():
    # Load residuals
    residuals = {}
    with open(os.path.join(BASE, 'residuals/unclassified_set.csv')) as f:
        for row in csv.DictReader(f):
            residuals[row['khipu_id']] = row

    # Load stratification scores
    strat = {}
    with open(os.path.join(BASE, 'stratification/stratification_scores.csv')) as f:
        for row in csv.DictReader(f):
            try:
                strat[row['khipu_id']] = float(row['strat_score']) if row['strat_score'] not in ('nan','') else None
            except ValueError:
                strat[row['khipu_id']] = None

    results = []
    for kid, rinfo in residuals.items():
        toks = load_hex(kid)
        if len(toks) < 10:
            continue  # too small to assess
        s = strat.get(kid)
        zp = zero_pct(toks)
        ent = shannon_entropy(toks)
        uniq2 = ngram_uniqueness(toks, 2)
        uniq3 = ngram_uniqueness(toks, 3)
        hap = hapax_rate(toks)
        mr = max_run(toks)
        ndistinct = len(set(toks))

        # Spreadsheet-negative flags
        is_stratified = (s is not None and s > 0.7)
        is_zero_heavy = zp > 0.70
        is_column_rep = mr >= 8  # long runs = column formatting

        spreadsheet_positive = is_stratified or is_zero_heavy or is_column_rep

        # Language-positive composite score (higher = more language-like)
        # Normalize components to 0-1 and combine
        # entropy: typical range 1-8 bits; scale /8
        # uniqueness: already 0-1
        # hapax: already 0-1
        lang_score = (min(ent/8,1)*0.4 + uniq2*0.3 + hap*0.3)

        results.append({
            'khipu_id': kid,
            'n_cords': len(toks),
            'n_distinct': ndistinct,
            'strat_score': s,
            'zero_pct': round(zp,3),
            'entropy': round(ent,3),
            'uniq2': round(uniq2,3),
            'uniq3': round(uniq3,3),
            'hapax': round(hap,3),
            'max_run': mr,
            'is_stratified': is_stratified,
            'is_zero_heavy': is_zero_heavy,
            'is_column_rep': is_column_rep,
            'spreadsheet_positive': spreadsheet_positive,
            'lang_score': round(lang_score,3),
            'why_unclassified': rinfo['why_unclassified'],
            'provenance': rinfo['provenance'],
            'region': rinfo['region'],
            'n_colors': rinfo['n_colors'],
            'max_level': rinfo['max_level'],
        })

    # Split into spreadsheet-positive (exclude) and candidates
    excluded = [r for r in results if r['spreadsheet_positive']]
    candidates = [r for r in results if not r['spreadsheet_positive']]
    candidates.sort(key=lambda r: -r['lang_score'])

    os.makedirs(os.path.join(BASE, 'language-hunt'), exist_ok=True)

    # Write spreadsheet_negative.csv (the ones that FAIL spreadsheet = our candidates)
    with open(os.path.join(BASE, 'language-hunt/spreadsheet_negative.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=candidates[0].keys())
        w.writeheader(); w.writerows(candidates)

    # Write excluded for reference
    with open(os.path.join(BASE, 'language-hunt/spreadsheet_positive_excluded.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=excluded[0].keys() if excluded else [])
        if excluded:
            w.writeheader(); w.writerows(excluded)

    # Write language_positive.csv (ranked)
    with open(os.path.join(BASE, 'language-hunt/language_positive.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=candidates[0].keys())
        w.writeheader(); w.writerows(candidates)

    print(f"Residuals with >=10 cords: {len(results)}")
    print(f"Spreadsheet-positive (excluded): {len(excluded)}")
    print(f"Spreadsheet-negative candidates: {len(candidates)}")
    print()
    print("Top 20 by language score:")
    print(f"{'khipu':>10} {'n':>5} {'ent':>6} {'uniq2':>6} {'hapax':>6} {'zero%':>6} {'mrun':>5} {'score':>6}  prov")
    for r in candidates[:20]:
        print(f"{r['khipu_id']:>10} {r['n_cords']:>5} {r['entropy']:>6} {r['uniq2']:>6} {r['hapax']:>6} {r['zero_pct']:>6} {r['max_run']:>5} {r['lang_score']:>6}  {r['provenance']}")

if __name__ == '__main__':
    main()
