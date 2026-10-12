"""Build natural colonial Quechua corpus, v2.
Fixes: root-first segmentation, Spanish stopword filtering, stricter sentence selection.
"""
import re, csv, json, math
from collections import Counter
from pathlib import Path

BASE = Path('/home/hatch/workspace/quipu-analysis')
HUAR = BASE/'huarochiri'

# --- Load morphemes ---
suffixes = []  # (form, mtype, gloss) — grammatical suffixes/enclitics
with open(BASE/'isomorphism/quechua_morphemes.csv') as f:
    for row in csv.DictReader(f):
        m = row['morpheme'].lstrip('=-').lower()
        if m and len(m) >= 2:
            suffixes.append((m, row['mtype'], row['gloss']))
suffixes.sort(key=lambda x: -len(x[0]))

# Load roots (longest first)
roots = []
with open(BASE/'quechua-roots/quechua_native_roots.csv') as f:
    rdr = csv.DictReader(f)
    for row in rdr:
        r = (row.get('root') or '').strip().lower()
        if r and len(r) >= 3 and re.fullmatch(r'[a-zñ]+', r):
            roots.append(r)
roots = sorted(set(roots), key=len, reverse=True)
print(f"Loaded {len(suffixes)} suffixes, {len(roots)} roots")

# Common Quechua function words that are roots for our purposes
EXTRA_ROOTS = ['chay','kay','pay','ñuqa','ñoca','qam','paykuna','ñuqanchik',
    'ima','may','pi','hay','mana','ama','ñataq','ñispa','ñishpa','ñirqan',
    'rimay','yuyay','mikuy','waqay','tiyay','riy','hamuy','niy','kay',
    'pacha','runa','waka','yaku','urqu','llama','mama','tayta','wasi',
    'chacra','ayllu','apu','inka','qucha','inti','killa','sara','papa',
    'yupa','chunka','pichqa','iskay','kimsa','tawa','suqta','qanchis',
    'pusaq','isqun','hunu','waranka','punchaw','tuta','kunan','ñawpa']
roots = sorted(set(EXTRA_ROOTS) | set(roots), key=len, reverse=True)

SPANISH_STOP = {'de','la','el','los','las','y','en','que','por','con','para',
    'como','una','uno','del','al','se','no','si','es','son','esta','este',
    'estos','estas','mas','más','tambien','también','pero','pues','porque',
    'cuando','donde','muy','tan','así','asi','dice','dizque','añade','añadida',
    'aunque','propia','puede','poner','mis','dos','ojos','pies','siempre',
    'dativo','nominativo','plural','singular','pronombre','persona','verbo',
    'nombre','caso','modo','tiempo','dice','dizen','dezimos','como','está',
    'dicho','manera','suyo','suya','mismo','misma','otro','otra','cada'}

def segment_word(word):
    """Root-first: match longest root at start, then longest suffixes on remainder.
    Returns list of (piece, type, gloss) or [] if no root found."""
    w = word.lower().strip('.,;:!?()\"«»“”')
    if not w or len(w) < 3 or not re.fullmatch(r'[a-záéíóúñü]+', w):
        return []
    # normalize accents for matching
    wn = w.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ü','u')
    # Find root: longest root that is a prefix of wn, or that covers most of wn
    best_root = None
    for r in roots:
        if wn.startswith(r):
            best_root = r
            break
    if not best_root:
        return []
    pieces = [('ROOT:'+best_root, 'root', best_root)]
    rest = wn[len(best_root):]
    # Segment remainder into suffixes (longest match)
    i = 0
    while i < len(rest):
        matched = False
        for m, mt, gl in suffixes:
            if rest.startswith(m, i):
                pieces.append((m, mt, gl))
                i += len(m)
                matched = True
                break
        if not matched:
            # One unrecognized char: mark as unknown, advance
            pieces.append(('?'+rest[i], 'unknown', ''))
            i += 1
    return pieces

def is_spanish_heavy(text):
    words = re.findall(r'[a-záéíóúñü]+', text.lower())
    if not words:
        return True
    n_sp = sum(1 for w in words if w in SPANISH_STOP)
    return n_sp / len(words) > 0.15

def quechua_density(text):
    words = [w for w in re.findall(r'[a-záéíóúñü]+', text.lower()) if len(w) >= 3]
    words = [w for w in words if w not in SPANISH_STOP]
    if len(words) < 3:
        return 0
    ok = sum(1 for w in words if segment_word(w))
    return ok / len(words)

# --- 1. Huarochirí Ch.III (gold standard) ---
hq = (HUAR/'sources/huarochiri_ch3_quechua.txt').read_text()
huar_sents = [s.strip() for s in re.split(r'[.!?]', hq) if len(s.strip().split()) >= 3]

# --- 2. Holguín grammar: strict extraction ---
hg = open(BASE/'quechua-roots/holguin_gramatica.txt', encoding='utf-8', errors='ignore').read()
holguin_sents = []
for line in hg.split('\n'):
    line = line.strip()
    if len(line) < 15:
        continue
    for chunk in re.split(r'[.;:!?]', line):
        chunk = chunk.strip()
        nwords = len(chunk.split())
        if 3 <= nwords <= 20 and not is_spanish_heavy(chunk) and quechua_density(chunk) >= 0.6:
            holguin_sents.append(chunk)
# dedup
seen, uniq_hg = set(), []
for s in holguin_sents:
    k = s.lower()
    if k not in seen:
        seen.add(k); uniq_hg.append(s)

print(f"\nHuarochirí sents: {len(huar_sents)}, Holguín sents: {len(uniq_hg)}")
print("Sample Holguín:")
for s in uniq_hg[:8]:
    print("  ", s[:110])

# --- 3. Segment everything ---
all_sents = [('huarochiri', s) for s in huar_sents] + [('holguin', s) for s in uniq_hg]
tokens = []  # (piece, mtype, gloss, source)
for src, sent in all_sents:
    for w in re.findall(r'[a-záéíóúñü]+', sent.lower()):
        if w in SPANISH_STOP or len(w) < 3:
            continue
        for piece, mt, gl in segment_word(w):
            tokens.append((piece, mt, gl, src))

print(f"\nTotal tokens: {len(tokens)}, unique: {len(set(p for p,_,_,_ in tokens))}")

# Frequency (grammatical morphemes only — collapse ROOT:xxx into just roots for separate table)
gram = Counter()
rootc = Counter()
for p, mt, gl, src in tokens:
    if mt == 'root':
        rootc[p[5:]] += 1
    elif mt != 'unknown':
        gram[p] += 1

info = {}
for p, mt, gl, src in tokens:
    if p not in info:
        info[p] = (mt, gl)

def zipf(counter):
    counts = sorted(counter.values(), reverse=True)
    n = len(counts)
    if n < 5: return 0
    xs = [math.log(i+1) for i in range(n)]; ys = [math.log(c) for c in counts]
    mx, my = sum(xs)/n, sum(ys)/n
    return sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)

print("\nTop 30 GRAMMATICAL morphemes:")
rows = []
for rank, (m, c) in enumerate(gram.most_common(30), 1):
    mt, gl = info[m]
    print(f"  {rank:2d}. {m:12s} {c:5d}  [{mt}] {gl}")
    rows.append((rank, m, c, mt, gl))

with open(HUAR/'morpheme_frequencies.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['rank','morpheme','count','mtype','gloss','pct'])
    tot = sum(gram.values())
    for rank, (m, c) in enumerate(gram.most_common(), 1):
        mt, gl = info[m]
        w.writerow([rank, m, c, mt, gl, round(100*c/tot, 2)])

with open(HUAR/'root_frequencies.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['rank','root','count'])
    for rank, (r, c) in enumerate(rootc.most_common(50), 1):
        w.writerow([rank, r, c])

print("\nTop 20 ROOTS:")
for rank, (r, c) in enumerate(rootc.most_common(20), 1):
    print(f"  {rank:2d}. {r:15s} {c}")

# Bigrams of grammatical morphemes
seqs = []
for src, sent in all_sents:
    toks = []
    for w in re.findall(r'[a-záéíóúñü]+', sent.lower()):
        if w in SPANISH_STOP or len(w) < 3: continue
        toks.extend(p for p, mt, _ in segment_word(w) if mt != 'unknown')
    seqs.append(toks)
bigrams = Counter()
for toks in seqs:
    for a, b in zip(toks, toks[1:]):
        # normalize roots
        a2 = 'ROOT' if a.startswith('ROOT:') else a
        b2 = 'ROOT' if b.startswith('ROOT:') else b
        bigrams[(a2,b)] += 1

with open(HUAR/'morpheme_bigrams.csv','w',newline='') as f:
    w = csv.writer(f); w.writerow(['rank','bigram','count'])
    for rank, ((a,b), c) in enumerate(bigrams.most_common(50), 1):
        w.writerow([rank, f"{a}+{b}", c])

print("\nTop 15 bigrams:")
for (a,b), c in bigrams.most_common(15):
    print(f"   {a}+{b}: {c}")

zs = zipf(gram)
print(f"\nZipf slope (grammatical): {zs:.3f}")

stats = {
    'huarochiri_sentences': len(huar_sents),
    'holguin_sentences': len(uniq_hg),
    'grammatical_tokens': sum(gram.values()),
    'grammatical_types': len(gram),
    'root_tokens': sum(rootc.values()),
    'root_types': len(rootc),
    'zipf_slope_grammatical': round(zs, 3),
}
open(HUAR/'corpus_stats.json','w').write(json.dumps(stats, indent=2))
print(json.dumps(stats, indent=2))
