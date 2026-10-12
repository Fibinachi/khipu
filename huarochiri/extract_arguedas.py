"""Extract Quechua from Arguedas 1966 bilingual edition, build frequency baseline.
Uses paragraph-level language classification, then morpheme segmentation.
"""
import re, csv, json, math
from collections import Counter
from pathlib import Path

BASE = Path('/home/hatch/workspace/quipu-analysis')
HUAR = BASE/'huarochiri'
SRC = HUAR/'sources/huarochiri_arguedas_full.txt'

# --- Language classification ---
# Arguedas 1966 Quechua orthography markers
Q_MARKERS = {'chay','cay','ñ','hc','chaysi','ñocca','ñoca','canan','ñaupa',
    'cunan','runacuna','tac','scca','pachac','caymi','chaymi','ñatac','natac',
    'rimay','yachay','micuy','waqay','hamuy','riy','niy','tupuy','carcan',
    'munarcan','yachaspas','mana','ama','ñispa','nispa','huc','yupay'}
Q_SUFFIX = re.compile(r'(cuna|sc|cam|tac|pas|mi|si|ri|chi|nacu|yoc|ntin)$')
SPANISH_STOP = {'de','la','el','los','las','que','y','en','por','con','para',
    'como','una','uno','del','al','se','no','es','son','esta','este','estos',
    'muy','tan','dice','cuando','donde','porque','pero','mas','tambien',
    'habia','había','fue','fueron','dijo','dios','hombre','hombres','tiempo',
    'entonces','despues','después','asi','así','hasta','entre','sobre','este',
    'esta','esto','ese','esa','eso','aquel','mi','su','sus','nuestro','nuestra'}

def classify_para(text):
    words = re.findall(r'[a-záéíóúñü]+', text.lower())
    if len(words) < 5:
        return 'short'
    n_q = sum(1 for w in words if w in Q_MARKERS or Q_SUFFIX.search(w) or 'ñ' in w)
    n_s = sum(1 for w in words if w in SPANISH_STOP)
    # ratio-based
    if n_q > n_s * 1.5 and n_q >= 3:
        return 'quechua'
    if n_s > n_q * 1.5 and n_s >= 3:
        return 'spanish'
    return 'mixed'

text = SRC.read_text(encoding='utf-8', errors='ignore')
# Split into paragraphs (blank-line separated)
paras = [p.strip() for p in re.split(r'\n\s*\n', text) if len(p.strip()) > 30]

q_paras, s_paras, m_paras = [], [], []
for p in paras:
    # collapse internal newlines
    p1 = ' '.join(p.split())
    c = classify_para(p1)
    if c == 'quechua': q_paras.append(p1)
    elif c == 'spanish': s_paras.append(p1)
    elif c == 'mixed': m_paras.append(p1)

print(f"Paragraphs: {len(paras)} total | Quechua: {len(q_paras)} | Spanish: {len(s_paras)} | Mixed: {len(m_paras)}")
q_words = sum(len(p.split()) for p in q_paras)
print(f"Quechua words: {q_words}")

# Save extracted Quechua
(HUAR/'sources/huarochiri_quechua_extracted.txt').write_text('\n\n'.join(q_paras))
# Spot check
print("\nSample Quechua paras:")
for p in q_paras[2:5]:
    print("  ", p[:150]); print()

# --- Morpheme segmentation (Arguedas orthography) ---
# Arguedas 1966 orthography -> normalized mapping for segmentation
# Arguedas uses: c/qu, hc (for q?), ñ, hu, y. Our morpheme list uses modern-ish forms.
# Key: normalize Arguedas spelling to match morpheme forms.

def normalize_arguedas(w):
    w = w.lower()
    # Arguedas: 'c' before a/o/u = /k/, 'qu' before e/i = /k/
    # 'hc' often = /q/ ? Actually in Arguedas, 'cc' or 'hc'...
    # Simplify: map to a canonical form
    w = w.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u')
    w = re.sub(r'qu([ei])', r'k\1', w)  # que->ke, qui->ki
    w = w.replace('hu', 'w')  # hua->wa
    w = w.replace('cc', 'q')  # ccar->qar? approximate
    w = w.replace('hc', 'q')
    # leading c before a/o/u -> k
    w = re.sub(r'^c([aou])', r'k\1', w)
    w = re.sub(r'c([aou])', r'k\1', w)
    return w

# Load suffixes
suffixes = []
with open(BASE/'isomorphism/quechua_morphemes.csv') as f:
    for row in csv.DictReader(f):
        m = row['morpheme'].lstrip('=-').lower()
        if m and len(m) >= 2:
            # normalize morpheme forms too
            mn = normalize_arguedas(m)
            suffixes.append((mn, m, row['mtype'], row['gloss']))
suffixes.sort(key=lambda x: -len(x[0]))

# Load roots, normalized
roots = set()
with open(BASE/'quechua-roots/quechua_native_roots.csv') as f:
    for row in csv.DictReader(f):
        r = (row.get('root') or '').strip().lower()
        if r and len(r) >= 3 and re.fullmatch(r'[a-zñ]+', r):
            roots.add(normalize_arguedas(r))
# Add common roots in Arguedas spelling (normalized)
EXTRA = ['chay','kay','pay','ñuqa','qam','ima','may','mana','ñataq','ñispa',
    'rimay','yuyay','mikuy','waqay','tiyay','riy','hamuy','niy','pacha',
    'runa','waka','yaku','urqu','llama','mama','wasi','chakra','ayllu',
    'apu','inka','qucha','inti','killa','sara','papa','yupay','chunka',
    'pichqa','iskay','kimsa','tawa','suqta','punchaw','tuta','kunan',
    'ñawpa','ancha','hina','pay','ñuqanchik','wamra','sara','aya','supay']
roots |= set(normalize_arguedas(r) for r in EXTRA)
roots = sorted(roots, key=len, reverse=True)
print(f"Roots: {len(roots)}, suffixes: {len(suffixes)}")

def segment(w):
    wn = normalize_arguedas(w)
    if len(wn) < 3: return []
    # root-first
    broot = None
    for r in roots:
        if wn.startswith(r):
            broot = r; break
    if not broot: return []
    pieces = [('R:'+broot, 'root', broot)]
    rest = wn[len(broot):]
    i = 0
    while i < len(rest):
        hit = False
        for mn, orig, mt, gl in suffixes:
            if rest.startswith(mn, i):
                pieces.append((orig, mt, gl)); i += len(mn); hit = True; break
        if not hit:
            pieces.append(('?'+rest[i], 'unknown', '')); i += 1
    return pieces

# Segment all Quechua
tokens = []
for p in q_paras:
    for w in re.findall(r'[a-záéíóúñü]+', p.lower()):
        if len(w) < 3: continue
        for piece, mt, gl in segment(w):
            tokens.append((piece, mt, gl))

print(f"\nTokens: {len(tokens)}")
gram = Counter(); rootc = Counter(); info = {}
for p, mt, gl in tokens:
    if p not in info: info[p] = (mt, gl)
    if mt == 'root': rootc[p[2:]] += 1
    elif mt != 'unknown': gram[p] += 1

print(f"Grammatical types: {len(gram)}, tokens: {sum(gram.values())}")
print(f"Root types: {len(rootc)}, tokens: {sum(rootc.values())}")
print(f"Unknown rate: {sum(1 for p,mt,_ in tokens if mt=='unknown')/max(len(tokens),1):.2%}")

print("\nTop 30 grammatical:")
for rank, (m, c) in enumerate(gram.most_common(30), 1):
    mt, gl = info[m]
    print(f"  {rank:2d}. {m:10s} {c:5d} [{mt}] {gl}")

print("\nTop 20 roots:")
for rank, (r, c) in enumerate(rootc.most_common(20), 1):
    print(f"  {rank:2d}. {r:12s} {c}")

# Save
with open(HUAR/'morpheme_frequencies.csv','w',newline='') as f:
    w = csv.writer(f); w.writerow(['rank','morpheme','count','mtype','gloss','pct'])
    tot = sum(gram.values())
    for rank,(m,c) in enumerate(gram.most_common(),1):
        mt,gl = info[m]; w.writerow([rank,m,c,mt,gl,round(100*c/tot,2)])
with open(HUAR/'root_frequencies.csv','w',newline='') as f:
    w = csv.writer(f); w.writerow(['rank','root','count'])
    for rank,(r,c) in enumerate(rootc.most_common(100),1):
        w.writerow([rank,r,c])

# Bigrams
seqs = []
for p in q_paras:
    toks = []
    for w in re.findall(r'[a-záéíóúñü]+', p.lower()):
        if len(w) < 3: continue
        toks.extend(pc for pc,mt,_ in segment(w) if mt != 'unknown')
    if toks: seqs.append(toks)
bigrams = Counter()
for toks in seqs:
    for a,b in zip(toks,toks[1:]):
        a2 = 'ROOT' if a.startswith('R:') else a
        b2 = 'ROOT' if b.startswith('R:') else b
        bigrams[(a2,b2)] += 1
with open(HUAR/'morpheme_bigrams.csv','w',newline='') as f:
    w = csv.writer(f); w.writerow(['rank','bigram','count'])
    for rank,((a,b),c) in enumerate(bigrams.most_common(60),1):
        w.writerow([rank,f"{a}+{b}",c])
print("\nTop 15 bigrams:")
for (a,b),c in bigrams.most_common(15):
    print(f"   {a}+{b}: {c}")

# Zipf
counts = sorted(gram.values(), reverse=True); n = len(counts)
xs=[math.log(i+1) for i in range(n)]; ys=[math.log(c) for c in counts]
mx,my=sum(xs)/n,sum(ys)/n
slope=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
print(f"\nZipf slope: {slope:.3f}")

stats = {'quechua_paragraphs': len(q_paras), 'quechua_words': q_words,
    'grammatical_tokens': sum(gram.values()), 'grammatical_types': len(gram),
    'root_tokens': sum(rootc.values()), 'root_types': len(rootc),
    'zipf_slope': round(slope,3)}
open(HUAR/'corpus_stats.json','w').write(json.dumps(stats,indent=2))
print(json.dumps(stats,indent=2))
