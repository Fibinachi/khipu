"""Phonotactic constraint test: does khipu 1000331's color sequence obey
language-like constraints matching Quechua phonotactics?

Part 1: Quechua phonotactic constraints from phonetic-hex encoded lexicon.
Part 2: 1000331 "colorotactics" from FULL_COLOR sequence.
Part 3: Compare constraint geometries.
"""
import csv, math, os, sqlite3
from collections import Counter, defaultdict

BASE = os.path.expanduser('~/workspace/quipu-analysis')
OUT = os.path.join(BASE, 'phonotactics')
DB = os.path.join(BASE, 'okr-khipu.db')
os.makedirs(OUT, exist_ok=True)

VOWELS = {'01', '02', '03'}  # a, i, u

# ---------------------------------------------------------------- Part 1
def load_quechua_phoneme_bigrams():
    """Extract phoneme bigrams from all hex-encoded Quechua forms."""
    seqs = []
    for fn in ['phonetic-hex/quechua_phonetic_hex.csv',
               'phonetic-hex/roots_phonetic_hex.csv']:
        with open(os.path.join(BASE, fn)) as f:
            for row in csv.DictReader(f):
                hx = (row.get('phonetic_hex') or '').strip()
                if len(hx) >= 4 and len(hx) % 2 == 0:
                    phonemes = [hx[i:i+2] for i in range(0, len(hx), 2)]
                    seqs.append(phonemes)
    return seqs

def bigram_stats(seqs):
    bigram_counts = Counter()
    unigram_counts = Counter()
    phonemes = set()
    for s in seqs:
        for p in s:
            phonemes.add(p)
            unigram_counts[p] += 1
        for a, b in zip(s, s[1:]):
            bigram_counts[(a, b)] += 1
    return phonemes, unigram_counts, bigram_counts

def analyze_constraints(phonemes, unigram_counts, bigram_counts, label):
    n = len(phonemes)
    possible = n * n
    observed = len(bigram_counts)
    forbidden = possible - observed
    total_bigrams = sum(bigram_counts.values())

    # class of each phoneme
    def pclass(p):
        return 'V' if p in VOWELS else 'C'

    # class-transition matrix
    class_counts = Counter()
    for (a, b), cnt in bigram_counts.items():
        class_counts[(pclass(a), pclass(b))] += cnt

    # repeat bigrams (AA)
    repeat_obs = sum(1 for (a, b) in bigram_counts if a == b)
    repeat_possible = n  # one per phoneme

    # flexibility per phoneme: distinct followers / distinct predecessors
    followers = defaultdict(set)
    predecessors = defaultdict(set)
    for (a, b) in bigram_counts:
        followers[a].add(b)
        predecessors[b].add(a)

    flex = {}
    for p in phonemes:
        flex[p] = (len(followers[p]), len(predecessors[p]))

    # expected forbidden under independence (for calibration)
    # P(bigram unseen) approx exp(-E[count]); use simple coverage estimate
    return {
        'label': label, 'n_symbols': n, 'possible_bigrams': possible,
        'observed_bigrams': observed, 'forbidden_bigrams': forbidden,
        'forbidden_rate': forbidden / possible,
        'total_bigram_tokens': total_bigrams,
        'class_counts': dict(class_counts),
        'repeat_bigrams_observed': repeat_obs,
        'repeat_bigrams_possible': repeat_possible,
        'flexibility': flex,
        'bigram_counts': bigram_counts,
        'unigram_counts': unigram_counts,
        'phonemes': sorted(phonemes),
    }

def write_quechua_outputs(st):
    with open(os.path.join(OUT, 'quechua_phonotactics.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['bigram', 'class_pattern', 'observed_count', 'is_legal'])
        for (a, b), cnt in sorted(st['bigram_counts'].items()):
            cp = ('V' if a in VOWELS else 'C') + ('V' if b in VOWELS else 'C')
            w.writerow([f'{a}-{b}', cp, cnt, 1])
        # note: forbidden bigrams not enumerated (361-observed rows); summarized in profile

    with open(os.path.join(OUT, 'quechua_constraint_profile.md'), 'w') as f:
        f.write('# Quechua Phonotactic Constraint Profile\n\n')
        f.write(f"Source: {len(st['phonemes'])} phonemes from hex-encoded lexicon "
                f"(roots + grammatical morphemes).\n\n")
        f.write(f"- Phoneme inventory: {st['n_symbols']} "
                f"({len(VOWELS)} vowels, {st['n_symbols']-len(VOWELS)} consonants)\n")
        f.write(f"- Possible bigrams: {st['possible_bigrams']}\n")
        f.write(f"- Observed bigrams: {st['observed_bigrams']}\n")
        f.write(f"- Forbidden bigrams: {st['forbidden_bigrams']} "
                f"({st['forbidden_rate']:.1%})\n")
        f.write(f"- Bigram tokens analyzed: {st['total_bigram_tokens']}\n\n")
        f.write('## Class transition counts (tokens)\n\n')
        tot = sum(st['class_counts'].values())
        for k in sorted(st['class_counts']):
            f.write(f"- {k[0]}->{k[1]}: {st['class_counts'][k]} ({st['class_counts'][k]/tot:.1%})\n")
        f.write(f"\n- Repeat bigrams (X->X): {st['repeat_bigrams_observed']}/"
                f"{st['repeat_bigrams_possible']} phonemes allow self-transition\n\n")
        f.write('## Flexibility (distinct followers, distinct predecessors)\n\n')
        f.write('| phoneme | class | followers | predecessors |\n|---|---|---|---|\n')
        for p in sorted(st['phonemes']):
            fl, pr = st['flexibility'][p]
            f.write(f"| {p} | {'V' if p in VOWELS else 'C'} | {fl} | {pr} |\n")

# ---------------------------------------------------------------- Part 2
def load_khipu331_sequence():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # one color per cord: take lowest color_id to dedupe
    c.execute("""
        SELECT c.CORD_ID, c.CORD_ORDINAL,
               (SELECT cc2.FULL_COLOR FROM ascher_cord_color cc2
                WHERE cc2.CORD_ID = c.CORD_ID ORDER BY cc2.color_id LIMIT 1) AS fc
        FROM cord c WHERE c.KHIPU_ID = 1000331
        ORDER BY c.CORD_ORDINAL, c.CORD_ID
    """)
    rows = c.fetchall()
    conn.close()
    seq = [(r[2] if r[2] else 'NONE') for r in rows]
    return seq

def analyze_khipu331(seq):
    symbols = sorted(set(seq))
    n = len(symbols)
    bigram_counts = Counter(zip(seq, seq[1:]))
    unigram_counts = Counter(seq)
    possible = n * n
    observed = len(bigram_counts)
    forbidden = possible - observed

    followers = defaultdict(set)
    predecessors = defaultdict(set)
    for (a, b) in bigram_counts:
        followers[a].add(b)
        predecessors[b].add(a)
    flex = {s: (len(followers[s]), len(predecessors[s])) for s in symbols}

    repeat_obs = sum(1 for (a, b) in bigram_counts if a == b)

    # trigram stats for "syllable" detection
    trigram_counts = Counter(zip(seq, seq[1:], seq[2:]))

    return {
        'n_symbols': n, 'symbols': symbols, 'seq_len': len(seq),
        'possible_bigrams': possible, 'observed_bigrams': observed,
        'forbidden_bigrams': forbidden, 'forbidden_rate': forbidden / possible,
        'total_bigram_tokens': sum(bigram_counts.values()),
        'repeat_bigrams_observed': repeat_obs, 'repeat_bigrams_possible': n,
        'flexibility': flex, 'bigram_counts': bigram_counts,
        'unigram_counts': unigram_counts, 'trigram_counts': trigram_counts,
        'seq': seq,
    }

def write_khipu331_outputs(st):
    with open(os.path.join(OUT, 'khipu331_colorotactics.csv'), 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['bigram', 'observed_count', 'is_legal'])
        for (a, b), cnt in sorted(st['bigram_counts'].items(),
                                  key=lambda x: -x[1]):
            w.writerow([f'{a} -> {b}', cnt, 1])

    with open(os.path.join(OUT, 'khipu331_constraint_profile.md'), 'w') as f:
        f.write('# Khipu 1000331 "Colorotactic" Constraint Profile\n\n')
        f.write(f"- Sequence length: {st['seq_len']} cords\n")
        f.write(f"- Symbol inventory: {st['n_symbols']} distinct FULL_COLOR values\n")
        f.write(f"- Possible bigrams: {st['possible_bigrams']}\n")
        f.write(f"- Observed bigrams: {st['observed_bigrams']}\n")
        f.write(f"- Forbidden bigrams: {st['forbidden_bigrams']} "
                f"({st['forbidden_rate']:.1%})\n")
        f.write(f"- Bigram tokens: {st['total_bigram_tokens']}\n")
        f.write(f"- Repeat bigrams (X->X): {st['repeat_bigrams_observed']}/"
                f"{st['repeat_bigrams_possible']}\n\n")
        f.write('## Symbol frequencies\n\n')
        f.write('| symbol | count | pct |\n|---|---|---|\n')
        for s, cnt in st['unigram_counts'].most_common():
            f.write(f"| {s} | {cnt} | {cnt/st['seq_len']:.1%} |\n")
        f.write('\n## Flexibility (distinct followers, distinct predecessors)\n\n')
        f.write('| symbol | followers | predecessors | total |\n|---|---|---|---|\n')
        for s in sorted(st['symbols'], key=lambda x: -(st['flexibility'][x][0] + st['flexibility'][x][1])):
            fl, pr = st['flexibility'][s]
            f.write(f"| {s} | {fl} | {pr} | {fl+pr} |\n")
        f.write('\n## Top 20 bigrams\n\n')
        for (a, b), cnt in st['bigram_counts'].most_common(20):
            f.write(f"- {a} -> {b}: {cnt}\n")
        f.write('\n## Top 15 trigrams (syllable candidates)\n\n')
        for (a, b, c), cnt in st['trigram_counts'].most_common(15):
            f.write(f"- {a} -> {b} -> {c}: {cnt}\n")

# ---------------------------------------------------------------- Part 3
def compare(q, k):
    lines = []
    lines.append('# Constraint Geometry Comparison: Quechua vs Khipu 1000331\n')
    lines.append('## Forbidden bigram rates\n')
    lines.append(f"| system | symbols | possible | observed | forbidden | rate |")
    lines.append(f"|---|---|---|---|---|---|")
    lines.append(f"| Quechua phonemes | {q['n_symbols']} | {q['possible_bigrams']} | "
                 f"{q['observed_bigrams']} | {q['forbidden_bigrams']} | {q['forbidden_rate']:.1%} |")
    lines.append(f"| 1000331 colors | {k['n_symbols']} | {k['possible_bigrams']} | "
                 f"{k['observed_bigrams']} | {k['forbidden_bigrams']} | {k['forbidden_rate']:.1%} |")
    lines.append('')
    # Null calibration: expected forbidden under random permutation of each sequence
    import random
    def null_forbidden_rate(seq, trials=200):
        syms = sorted(set(seq))
        n = len(syms)
        rates = []
        for _ in range(trials):
            sh = seq[:]
            random.shuffle(sh)
            obs = len(set(zip(sh, sh[1:])))
            rates.append(1 - obs / (n * n))
        return sum(rates) / len(rates)
    random.seed(42)
    k_null = null_forbidden_rate(k['seq'])
    lines.append(f"- 1000331 null (shuffled) forbidden rate: {k_null:.1%} "
                 f"(observed {k['forbidden_rate']:.1%})")
    # Quechua null: shuffle phonemes within each word-shape
    qseqs = load_quechua_phoneme_bigrams()
    flat = [p for s in qseqs for p in s]
    q_null_rates = []
    for _ in range(50):
        # shuffle bigrams by rewiring: preserve unigram counts, random pairing
        sh = flat[:]
        random.shuffle(sh)
        obs = len(set(zip(sh, sh[1:])))
        q_null_rates.append(1 - obs / (q['n_symbols'] ** 2))
    q_null = sum(q_null_rates) / len(q_null_rates)
    lines.append(f"- Quechua null (shuffled phonemes) forbidden rate: {q_null:.1%} "
                 f"(observed {q['forbidden_rate']:.1%})")
    lines.append('')
    lines.append('## Repeat (X->X) bigrams\n')
    lines.append(f"- Quechua: {q['repeat_bigrams_observed']}/{q['repeat_bigrams_possible']} "
                 f"phonemes allow self-transition")
    lines.append(f"- 1000331: {k['repeat_bigrams_observed']}/{k['repeat_bigrams_possible']} "
                 f"colors allow self-transition")
    lines.append('')
    lines.append('## Vowel/consonant-like split\n')
    # Quechua: vowels by definition
    q_vow_flex = [q['flexibility'][p][0] + q['flexibility'][p][1] for p in VOWELS if p in q['flexibility']]
    q_con_flex = [q['flexibility'][p][0] + q['flexibility'][p][1] for p in q['phonemes'] if p not in VOWELS]
    lines.append(f"- Quechua vowels (n={len(q_vow_flex)}): mean flexibility "
                 f"{sum(q_vow_flex)/len(q_vow_flex):.1f}")
    lines.append(f"- Quechua consonants (n={len(q_con_flex)}): mean flexibility "
                 f"{sum(q_con_flex)/len(q_con_flex):.1f}")
    # Khipu: split by median flexibility
    kflex = sorted(((s, fl + pr) for s, (fl, pr) in k['flexibility'].items()),
                   key=lambda x: -x[1])
    med = sorted([v for _, v in kflex])[len(kflex) // 2]
    khi = [x for x in kflex if x[1] >= med]
    klo = [x for x in kflex if x[1] < med]
    lines.append(f"- 1000331 flexible half ({len(khi)}): " +
                 ", ".join(f"{s}({v})" for s, v in khi))
    lines.append(f"- 1000331 restricted half ({len(klo)}): " +
                 ", ".join(f"{s}({v})" for s, v in klo))
    lines.append('')
    # class-transition comparison for Quechua
    lines.append('## Quechua class transitions (for reference)\n')
    tot = sum(q['class_counts'].values())
    for kk in sorted(q['class_counts']):
        lines.append(f"- {kk[0]}->{kk[1]}: {q['class_counts'][kk]/tot:.1%}")
    lines.append('')
    # Khipu: transitions between flexible (F) and restricted (R) classes
    fset = set(s for s, _ in khi)
    fr_counts = Counter()
    for (a, b), cnt in k['bigram_counts'].items():
        fr_counts[(('F' if a in fset else 'R'), ('F' if b in fset else 'R'))] += cnt
    lines.append('## 1000331 flexible/restricted transitions\n')
    ftot = sum(fr_counts.values())
    for kk in sorted(fr_counts):
        lines.append(f"- {kk[0]}->{kk[1]}: {fr_counts[kk]/ftot:.1%}")
    with open(os.path.join(OUT, 'constraint_comparison.md'), 'w') as f:
        f.write("\n".join(lines) + "\n")
    return k_null, q_null

def verdict(q, k, k_null, q_null):
    lines = ['# Phonotactic Verdict: Does 1000331 Obey Language-Like Constraints?\n']
    lines.append('## Numbers\n')
    lines.append(f"- Quechua forbidden-bigram rate: {q['forbidden_rate']:.1%} "
                 f"(null {q_null:.1%})")
    lines.append(f"- 1000331 forbidden-bigram rate: {k['forbidden_rate']:.1%} "
                 f"(null {k_null:.1%})")
    # effect sizes: observed - null (positive = more constrained than random)
    q_eff = (q['forbidden_rate'] - q_null)
    k_eff = (k['forbidden_rate'] - k_null)
    lines.append(f"- Quechua constraint effect (null - observed): {q_eff:.3f}")
    lines.append(f"- 1000331 constraint effect (null - observed): {k_eff:.3f}")
    lines.append('')
    # vowel/consonant geometry
    q_vow = sum(q['flexibility'][p][0] + q['flexibility'][p][1] for p in VOWELS if p in q['flexibility']) / 3
    q_con_vals = [q['flexibility'][p][0] + q['flexibility'][p][1] for p in q['phonemes'] if p not in VOWELS]
    q_con = sum(q_con_vals) / len(q_con_vals)
    lines.append(f"- Quechua vowel/consonant flexibility ratio: {q_vow/q_con:.2f}")
    kflex = sorted((fl + pr for fl, pr in k['flexibility'].values()), reverse=True)
    khi_mean = sum(kflex[:7]) / 7
    klo_mean = sum(kflex[7:]) / 7
    lines.append(f"- 1000331 top-7 / bottom-7 flexibility ratio: {khi_mean/klo_mean:.2f}")
    lines.append('')
    lines.append('## Interpretation\n')
    # decision logic
    lang_like = []
    if k_eff > 0.03:
        lang_like.append(f"1000331 shows excess sequential constraint beyond null "
                         f"(effect +{k_eff:.1%})")
    else:
        lang_like.append("1000331 shows NO excess constraint beyond shuffled null")
    # compare forbidden rates with inventory-size adjustment is hard; use effect sizes
    ratio = k_eff / q_eff if q_eff > 0 else 0
    lang_like.append(f"Constraint effect is {ratio:.0%} of Quechua's phonotactic effect")
    if khi_mean / klo_mean > 1.5:
        lang_like.append("Flexibility split present (vowel/consonant-like asymmetry)")
    else:
        lang_like.append("No strong flexibility asymmetry (unlike natural language)")
    for l in lang_like:
        lines.append(f"- {l}")
    lines.append('')
    if k_eff > 0.03 and ratio > 0.3 and khi_mean / klo_mean > 1.5:
        lines.append('**VERDICT: LANGUAGE-LIKE.** 1000331 obeys phonotactic-style '
                     'constraints with natural-language geometry.')
    elif k_eff > 0.03:
        lines.append('**VERDICT: CONSTRAINED BUT NOT LANGUAGE-LIKE.** 1000331 has '
                     'sequential structure, but its constraint geometry does not match '
                     'natural-language phonotactics. Consistent with a categorical code.')
    else:
        lines.append('**VERDICT: NOT LANGUAGE-LIKE.** 1000331 bigram constraints are '
                     'indistinguishable from shuffled null. No phonotactic fingerprint.')
    with open(os.path.join(OUT, 'phonotactic_verdict.md'), 'w') as f:
        f.write("\n".join(lines) + "\n")
    print("\n".join(lines))

def main():
    print("Part 1: Quechua phonotactics...")
    qseqs = load_quechua_phoneme_bigrams()
    print(f"  {len(qseqs)} forms")
    q = analyze_constraints(*bigram_stats(qseqs), 'quechua')
    write_quechua_outputs(q)
    print(f"  forbidden rate: {q['forbidden_rate']:.1%}")

    print("Part 2: 1000331 colorotactics...")
    seq = load_khipu331_sequence()
    print(f"  {len(seq)} cords, {len(set(seq))} symbols")
    k = analyze_khipu331(seq)
    write_khipu331_outputs(k)
    print(f"  forbidden rate: {k['forbidden_rate']:.1%}")

    print("Part 3: comparison...")
    k_null, q_null = compare(q, k)
    print("Part 4: verdict...")
    verdict(q, k, k_null, q_null)
    print("Done.")

if __name__ == '__main__':
    main()
