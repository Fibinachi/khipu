"""Ordinal-letter analysis: find anchored Hangman patterns as sequential items.
Letters: W=f8040000 (-ta ACC), A=20040000 (-mi EVD), M=a4040000 (-kuna PL), K=84040000 (TBD).
"""
import sqlite3, os, glob, csv, json, math, random
from collections import Counter, defaultdict

BASE = '/home/hatch/workspace/quipu-analysis'
OUT = os.path.join(BASE, 'ordinal-letters')
os.makedirs(OUT, exist_ok=True)

LETTERS = {
    'f8040000': 'W',   # -ta accusative
    '20040000': 'A',   # -mi evidential
    'a4040000': 'M',   # -kuna plural
    '84040000': 'K',   # TBD
}
GLOSS = {'W': '-ta/ACC', 'A': '-mi/EVD', 'M': '-kuna/PL', 'K': 'TBD'}

def decode(tok):
    b0 = int(tok[0:2], 16); b1 = int(tok[2:4], 16)
    return {
        'color_id': b0 >> 2,
        'knot': ((b0 & 3) << 1) | ((b1 >> 7) & 1),
        'dir': (b1 >> 5) & 3,
        'level': (b1 >> 2) & 7,
        'val': int(tok[4:8], 16),
    }

def load_hex_corpus():
    khipu = {}
    for f in sorted(glob.glob(os.path.join(BASE, 'byte-patterns/hex-corpus/*.hex'))):
        base = os.path.basename(f).replace('.hex', '')
        if not base.isdigit():
            continue
        kid = int(base)
        raw = open(f).read().strip()
        body = raw[16:]  # skip 8-byte header
        toks = [body[i:i+8] for i in range(0, len(body), 8) if len(body[i:i+8]) == 8]
        khipu[kid] = toks
    return khipu

def load_cord_ids():
    """khipu_id -> list of (cord_id, cord_ordinal) in serializer order."""
    conn = sqlite3.connect(os.path.join(BASE, 'okr-khipu.db'))
    c = conn.cursor()
    c.execute("SELECT KHIPU_ID, CORD_ID, CORD_ORDINAL FROM cord ORDER BY KHIPU_ID, CORD_ORDINAL")
    out = defaultdict(list)
    for kid, cid, cord_ord in c.fetchall():
        out[kid].append((cid, cord_ord))
    conn.close()
    return out

def main():
    random.seed(42)
    khipu = load_hex_corpus()
    cord_ids = load_cord_ids()
    print(f"loaded {len(khipu)} khipu")

    # ---- 1. letter occurrences ----
    occ_rows = []
    seqs = {}          # kid -> list of letters or None per position
    all_toks = {}      # kid -> toks
    for kid, toks in khipu.items():
        ids = cord_ids.get(kid, [])
        letters = []
        for i, tok in enumerate(toks):
            L = LETTERS.get(tok)
            letters.append(L)
            if L:
                cid = ids[i][0] if i < len(ids) else ''
                dec = decode(tok)
                neigh = []
                for j in range(i-3, i+4):
                    if j == i:
                        continue
                    neigh.append(toks[j] if 0 <= j < len(toks) else '.')
                occ_rows.append({
                    'pattern': tok, 'letter': L, 'gloss': GLOSS[L],
                    'khipu_id': kid, 'cord_id': cid,
                    'token_index': i, 'n_tokens': len(toks),
                    'level': dec['level'],
                    'neighbors_hex': ';'.join(neigh),
                })
        seqs[kid] = letters
        all_toks[kid] = toks

    with open(os.path.join(OUT, 'letter_occurrences.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['pattern','letter','gloss','khipu_id','cord_id','token_index','n_tokens','level','neighbors_hex'])
        w.writeheader(); w.writerows(occ_rows)
    print(f"occurrences: {len(occ_rows)}")
    print("per-letter:", Counter(r['letter'] for r in occ_rows))

    # ---- 2. letter words: maximal runs of consecutive letters ----
    word_counter = Counter()
    word_khipu = defaultdict(set)
    for kid, letters in seqs.items():
        run = []
        for L in letters + [None]:
            if L:
                run.append(L)
            else:
                if run:
                    s = ''.join(run)
                    word_counter[s] += 1
                    word_khipu[s].add(kid)
                    run = []
    with open(os.path.join(OUT, 'letter_words.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['sequence','length','count','n_khipu','example_khipu'])
        for s, cnt in word_counter.most_common():
            ex = sorted(word_khipu[s])[:5]
            w.writerow([s, len(s), cnt, len(word_khipu[s]), ';'.join(map(str, ex))])
    print(f"distinct words: {len(word_counter)}, total runs: {sum(word_counter.values())}")

    # bigram transitions within alphabet (consecutive letters only)
    bi = Counter(); bi_from = Counter()
    for kid, letters in seqs.items():
        prev = None
        for L in letters:
            if L and prev:
                bi[(prev, L)] += 1
                bi_from[prev] += 1
            prev = L if L else None
    print("top letter bigrams:", bi.most_common(10))

    # ---- 3. positional grammar ----
    pos = {L: [] for L in 'WAMK'}
    third = {L: Counter() for L in 'WAMK'}
    for r in occ_rows:
        L = r['letter']
        p = r['token_index'] / max(r['n_tokens'] - 1, 1)
        pos[L].append(p)
        third[L]['begin' if p < 1/3 else ('mid' if p < 2/3 else 'end')] += 1
    with open(os.path.join(OUT, 'positional_grammar.md'), 'w') as f:
        f.write("# Positional grammar of the 4-letter alphabet\n\n")
        f.write("Letters: W=f8040000 (-ta/ACC), A=20040000 (-mi/EVD), M=a4040000 (-kuna/PL), K=84040000 (TBD).\n\n")
        f.write("## Normalized position in khipu (0=start, 1=end)\n\n")
        f.write("| letter | gloss | n | mean pos | median pos | begin | mid | end |\n|---|---|---|---|---|---|---|---|\n")
        for L in 'WAMK':
            ps = sorted(pos[L])
            mean = sum(ps)/len(ps) if ps else 0
            med = ps[len(ps)//2] if ps else 0
            t = third[L]
            f.write(f"| {L} | {GLOSS[L]} | {len(ps)} | {mean:.3f} | {med:.3f} | {t['begin']} | {t['mid']} | {t['end']} |\n")
        f.write("\n## Letter bigram transitions (consecutive letters)\n\n")
        f.write("| from -> to | count | P(to|from) |\n|---|---|---|\n")
        for (a, b), cnt in bi.most_common(16):
            f.write(f"| {a}->{b} | {cnt} | {cnt/bi_from[a]:.3f} |\n")
        f.write("\n## Word-length distribution of letter runs\n\n")
        wl = Counter(len(s) for s in word_counter for _ in range(word_counter[s]))
        # simpler: distribution over runs
        wl2 = Counter()
        for s, cnt in word_counter.items():
            wl2[len(s)] += cnt
        f.write("| run length | n runs |\n|---|---|\n")
        for l in sorted(wl2):
            f.write(f"| {l} | {wl2[l]} |\n")

    # ---- 4. Quechua ordering test: ROOT-PL-CASE-EVD -> content,M,W,A ----
    # Count adjacent M->W, W->A bigrams and M->W->A trigrams among ALL adjacent token pairs
    def count_patterns(seqs):
        bMW = bWA = 0
        tMWA = 0
        n_pairs = n_tri = 0
        marg = Counter()
        for kid, letters in seqs.items():
            n = len(letters)
            for L in letters:
                if L: marg[L] += 1
            for i in range(n-1):
                a, b = letters[i], letters[i+1]
                if a and b:
                    n_pairs += 1
                    if (a, b) == ('M', 'W'): bMW += 1
                    if (a, b) == ('W', 'A'): bWA += 1
            for i in range(n-2):
                a, b, cc = letters[i], letters[i+1], letters[i+2]
                if a and b and cc:
                    n_tri += 1
                    if (a, b, cc) == ('M', 'W', 'A'): tMWA += 1
        return {'bMW': bMW, 'bWA': bWA, 'tMWA': tMWA, 'n_pairs': n_pairs,
                'n_tri': n_tri, 'marg': dict(marg)}

    obs = count_patterns(seqs)
    # permutation null: shuffle letters WITHIN each khipu (keep positions of non-letters fixed)
    NPERM = 500
    null_bMW, null_bWA, null_tMWA = [], [], []
    kids = list(seqs.keys())
    for _ in range(NPERM):
        pseq = {}
        for kid in kids:
            letters = seqs[kid]
            idx = [i for i, L in enumerate(letters) if L]
            vals = [letters[i] for i in idx]
            random.shuffle(vals)
            new = list(letters)
            for i, v in zip(idx, vals):
                new[i] = v
            pseq[kid] = new
        r = count_patterns(pseq)
        null_bMW.append(r['bMW']); null_bWA.append(r['bWA']); null_tMWA.append(r['tMWA'])

    def pval(obs_v, nulls, greater=True):
        ge = sum(1 for x in nulls if x >= obs_v)
        return (ge + 1) / (len(nulls) + 1)

    # analytic expectation under independence using global letter rates among letter tokens
    tot_letters = sum(obs['marg'].values())
    p = {L: obs['marg'].get(L, 0)/tot_letters for L in 'WAMK'}
    exp_bMW = obs['n_pairs'] * p['M'] * p['W']
    exp_bWA = obs['n_pairs'] * p['W'] * p['A']
    exp_tMWA = obs['n_tri'] * p['M'] * p['W'] * p['A']

    # also: content-precedes check: for M->W->A trigrams, is previous token a content cord?
    prec_content = prec_total = 0
    for kid, letters in seqs.items():
        for i in range(len(letters)-2):
            if (letters[i], letters[i+1], letters[i+2]) == ('M', 'W', 'A'):
                prec_total += 1
                if i > 0 and letters[i-1] is None:
                    prec_content += 1
    # baseline: fraction of letter tokens preceded by content
    base_prec = base_tot = 0
    for kid, letters in seqs.items():
        for i, L in enumerate(letters):
            if L and i > 0:
                base_tot += 1
                if letters[i-1] is None:
                    base_prec += 1

    with open(os.path.join(OUT, 'ordering_test.md'), 'w') as f:
        f.write("# Quechua ordering hypothesis test\n\n")
        f.write("Quechua morpheme order: ROOT-PL-CASE-EVD. Predicted khipu order: [content] -> M(-kuna) -> W(-ta) -> A(-mi).\n\n")
        f.write(f"Letter-token marginals: {obs['marg']} (total {tot_letters})\n\n")
        f.write("## Bigram/trigram counts vs null\n\n")
        f.write("| pattern | observed | expected (independence) | perm-mean | perm p (one-sided, greater) |\n")
        f.write("|---|---|---|---|\n")
        import statistics
        for name, key, exp in [('M->W', 'bMW', exp_bMW), ('W->A', 'bWA', exp_bWA), ('M->W->A', 'tMWA', exp_tMWA)]:
            nulls = {'bMW': null_bMW, 'bWA': null_bWA, 'tMWA': null_tMWA}[key]
            f.write(f"| {name} | {obs[key]} | {exp:.1f} | {statistics.mean(nulls):.1f} | {pval(obs[key], nulls):.4f} |\n")
        f.write(f"\nAdjacent letter pairs total: {obs['n_pairs']}; adjacent letter triples total: {obs['n_tri']}.\n")
        f.write("\n## Content-precedes check (ROOT before PL-CASE-EVD)\n\n")
        f.write(f"M->W->A trigrams preceded by content cord: {prec_content}/{prec_total}")
        if prec_total:
            f.write(f" = {prec_content/prec_total:.3f}\n")
        f.write(f"Baseline (any letter token preceded by content): {base_prec}/{base_tot}")
        if base_tot:
            f.write(f" = {base_prec/base_tot:.3f}\n")

    # summary report
    with open(os.path.join(OUT, 'ordinal_report.md'), 'w') as f:
        f.write("# Ordinal-letter analysis: summary\n\n")
        f.write("## Alphabet\n\nW=f8040000 (-ta/ACC), A=20040000 (-mi/EVD), M=a4040000 (-kuna/PL), K=84040000 (TBD).\n\n")
        f.write(f"## Occurrences\n\n{len(occ_rows)} total letter-tokens across {len(khipu)} khipu.\nPer letter: {dict(Counter(r['letter'] for r in occ_rows))}\n\n")
        f.write(f"## Words\n\n{len(word_counter)} distinct letter-runs, {sum(word_counter.values())} total runs.\n")
        f.write("Top 15 words:\n\n| seq | count | n_khipu |\n|---|---|---|\n")
        for s, cnt in word_counter.most_common(15):
            f.write(f"| {s} | {cnt} | {len(word_khipu[s])} |\n")
        f.write("\n## Ordering test (Quechua ROOT-PL-CASE-EVD)\n\n")
        f.write(f"M->W: obs {obs['bMW']} vs exp {exp_bMW:.1f}, p={pval(obs['bMW'], null_bMW):.4f}\n\n")
        f.write(f"W->A: obs {obs['bWA']} vs exp {exp_bWA:.1f}, p={pval(obs['bWA'], null_bWA):.4f}\n\n")
        f.write(f"M->W->A: obs {obs['tMWA']} vs exp {exp_tMWA:.1f}, p={pval(obs['tMWA'], null_tMWA):.4f}\n\n")
    print("done. p-values:", pval(obs['bMW'], null_bMW), pval(obs['bWA'], null_bWA), pval(obs['tMWA'], null_tMWA))

if __name__ == '__main__':
    main()
