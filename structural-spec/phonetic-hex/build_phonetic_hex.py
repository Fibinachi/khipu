"""Build hex-encoded phonetic Quechua corpus and compare against khipu byte patterns.

Pipeline:
  1. Define phoneme -> hex byte encoding (ordered by articulation so similar
     sounds get adjacent values).
  2. Encode the 216-morpheme inventory + 2,827 native roots to phonetic hex.
  3. Build morpheme-sequence corpus from attested phrases + template phrases
     (templates flagged; valid for phonotactics, caveat for frequency).
  4. Extract additional Quechua sentences from Holguin grammar via
     morpheme-coverage filter.
  5. Compute phonetic-hex n-grams, Zipf slopes, positional stats.
  6. Compare against khipu byte n-grams.
"""
import csv, json, re, math, os
from collections import Counter

BASE = '/home/hatch/workspace/quipu-analysis'
OUT  = os.path.join(BASE, 'phonetic-hex')
SRC  = os.path.join(OUT, 'sources')
os.makedirs(SRC, exist_ok=True)

# ---------------------------------------------------------------- phoneme map
# Vowels by height; consonants by place of articulation so that phonetically
# similar segments receive numerically adjacent byte values.
VOWELS = {'a': 0x01, 'i': 0x02, 'u': 0x03}
CONSONANTS = {
    # labial
    'p': 0x10, 'm': 0x11, 'w': 0x12, 'v': 0x13,
    # dental / alveolar
    't': 0x14, 'n': 0x15, 's': 0x16, 'l': 0x17, 'r': 0x18, 'z': 0x19,
    # palatal
    'ch': 0x1A, 'ñ': 0x1B, 'll': 0x1C, 'y': 0x1D, 'sh': 0x1E, 'j': 0x1F,
    # velar
    'k': 0x20, 'c': 0x20, 'qu': 0x20, 'g': 0x21, 'x': 0x22,
    # uvular / glottal
    'q': 0x23, 'h': 0x24,
}
# digraphs must be matched before single chars
DIGRAPHS = ['ch', 'll', 'sh', 'ñ', 'qu']
PHONEME_RE = re.compile(r'ch|ll|sh|qu|ñ|[aeiou]|[^aeiou\s\W\d_]')

def tokenize_phonemes(s):
    """Lowercase-normalize a Quechua string into a phoneme list."""
    s = s.lower().strip()
    # strip morpheme boundary markers
    s = s.replace('=', '').replace('-', '').replace('_agr', '').replace('_poss', '')
    s = s.replace('_', '')
    out = []
    for m in PHONEME_RE.finditer(s):
        ph = m.group(0)
        if ph in VOWELS:
            out.append(('V', ph, VOWELS[ph]))
        elif ph in CONSONANTS:
            out.append(('C', ph, CONSONANTS[ph]))
        # skip anything unmapped (punctuation etc. already excluded by regex)
    return out

def phonemes_to_hex(phlist):
    return ''.join(f'{b:02x}' for _, _, b in phlist)

def syllable_skeleton(phlist):
    return ''.join(kind for kind, _, _ in phlist)

# ---------------------------------------------------------------- load morphemes
morphs = []  # (morpheme, mtype, gloss)
with open(os.path.join(BASE, 'isomorphism', 'quechua_morphemes.csv')) as f:
    for row in csv.DictReader(f):
        morphs.append((row['morpheme'], row['mtype'], row['gloss']))
print(f'loaded {len(morphs)} morphemes')

morph_hex = {}
for m, t, g in morphs:
    ph = tokenize_phonemes(m)
    morph_hex[m] = (phonemes_to_hex(ph), syllable_skeleton(ph), len(ph))

# ---------------------------------------------------------------- load roots
roots = []
with open(os.path.join(BASE, 'quechua-roots', 'quechua_native_roots.csv')) as f:
    for row in csv.DictReader(f):
        r = row['root'].strip()
        if r:
            roots.append(r)
print(f'loaded {len(roots)} native roots')

root_hex = {}
for r in roots:
    ph = tokenize_phonemes(r)
    if ph:
        root_hex[r] = (phonemes_to_hex(ph), syllable_skeleton(ph), len(ph))

# ---------------------------------------------------------------- phrases
attested_seqs, template_seqs = [], []
with open(os.path.join(BASE, 'isomorphism', 'quechua_phrases.csv')) as f:
    for row in csv.DictReader(f):
        feats = row['feature_names'].split(';')
        if row['origin'] == 'attested':
            attested_seqs.append(feats)
        else:
            template_seqs.append(feats)
print(f'attested phrase morpheme-seqs: {len(attested_seqs)}, template: {len(template_seqs)}')

# ---------------------------------------------------------------- Holguin extraction
# Strategy: scan holguin_gramatica.txt for tokens that segment cleanly into
# known morphemes/roots (>=80% char coverage, >=2 morphemes). Those are
# near-certainly Quechua example words/phrases, not Spanish prose.

# Build a segmentation lexicon: roots + morpheme stems, longest first
seg_lex = set()
for r in roots:
    rr = re.sub(r'^[-=]', '', r).lower()
    if len(rr) >= 2:
        seg_lex.add(rr)
for m, t, g in morphs:
    mm = re.sub(r'^[-=]', '', m).lower().replace('_agr', 'n').replace('_poss', 'n')
    if len(mm) >= 1:
        seg_lex.add(mm)
seg_sorted = sorted(seg_lex, key=len, reverse=True)

def segment(word, _memo=None):
    """Greedy longest-match segmentation; returns list of pieces or None."""
    w = word.lower()
    pieces, i = [], 0
    while i < len(w):
        hit = None
        for cand in seg_sorted:
            if w.startswith(cand, i):
                hit = cand
                break
        if hit is None:
            return None
        pieces.append(hit)
        i += len(hit)
    return pieces

def is_quechua_word(tok):
    if len(tok) < 3 or not re.fullmatch(r'[a-zñáéíóúü]+', tok):
        return False
    # Spanish function words are common; require Quechua phonotactic plausibility:
    # must contain q, or ñ, or end in a known Quechua suffix shape
    t = tok.lower()
    pieces = segment(t)
    return pieces is not None and len(pieces) >= 2

holguin_quechua = []
seen = set()
with open(os.path.join(BASE, 'quechua-roots', 'holguin_gramatica.txt'), errors='replace') as f:
    for line in f:
        for tok in re.findall(r'[A-Za-zñÑáéíóúü]{3,}', line):
            tl = tok.lower()
            if tl in seen:
                continue
            seen.add(tl)
            if is_quechua_word(tl):
                pieces = segment(tl)
                holguin_quechua.append((tl, pieces))
print(f'Holguin Quechua-like tokens: {len(holguin_quechua)}')

# Save a sample of extracted tokens as a source record (not the full text)
with open(os.path.join(SRC, 'holguin_extracted_quechua_tokens.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['token', 'segmentation'])
    for tok, pieces in holguin_quechua[:5000]:
        w.writerow([tok, ';'.join(pieces)])

# ---------------------------------------------------------------- phonetic corpus
# Corpus A (high-trust): attested phrase morpheme sequences, phonetically encoded
# Corpus B (phonotactic): native roots (type-level phonotactics)
# Corpus C (supplemental): Holguin-extracted tokens, segmented
# Corpus D (flagged): template phrase sequences (valid phonotactics, artificial freq)

def encode_seq(feats):
    """Encode a morpheme feature sequence to a list of phonetic-hex tokens."""
    toks = []
    for feat in feats:
        key = feat.strip()
        if key in morph_hex:
            toks.append(morph_hex[key][0])
        else:
            ph = tokenize_phonemes(key)
            if ph:
                toks.append(phonemes_to_hex(ph))
    return toks

corpusA = [encode_seq(s) for s in attested_seqs]
corpusA = [s for s in corpusA if s]
corpusC = []
for tok, pieces in holguin_quechua:
    hx = phonemes_to_hex(tokenize_phonemes(tok))
    if hx:
        corpusC.append([hx])
corpusD = [encode_seq(s) for s in template_seqs]
corpusD = [s for s in corpusD if s]

nA = sum(len(s) for s in corpusA)
nC = len(corpusC)
nD = sum(len(s) for s in corpusD)
print(f'Corpus A (attested seqs): {len(corpusA)} seqs, {nA} morpheme tokens')
print(f'Corpus C (Holguin tokens): {nC} tokens')
print(f'Corpus D (template seqs, flagged): {len(corpusD)} seqs, {nD} tokens')
print(f'Corpus B (roots, type-level): {len(root_hex)} items')

# ---------------------------------------------------------------- n-gram + Zipf
def ngrams(tokens, n):
    return [tuple(tokens[i:i+n]) for i in range(len(tokens)-n+1)]

def zipf_slope(counter):
    freqs = sorted(counter.values(), reverse=True)
    if len(freqs) < 10:
        return None
    xs = [math.log(i+1) for i in range(len(freqs))]
    ys = [math.log(f) for f in freqs]
    mx, my = sum(xs)/len(xs), sum(ys)/len(ys)
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    den = sum((x-mx)**2 for x in xs)
    return num/den if den else None

results = {}
# Flatten corpora to token streams for n-gram analysis
streamA = [t for s in corpusA for t in s]
streamD = [t for s in corpusD for t in s]
streamC = [t for s in corpusC for t in s]
# Roots as individual phonetic tokens (type-level)
streamB = [v[0] for v in root_hex.values()]

for name, stream in [('A_attested', streamA), ('C_holguin', streamC),
                     ('D_template_flagged', streamD), ('B_roots_typelevel', streamB)]:
    r = {}
    for n in (1, 2, 3):
        ng = ngrams(stream, n)
        c = Counter(''.join(g) for g in ng)
        r[n] = {'types': len(c), 'tokens': len(ng),
                'zipf': zipf_slope(c),
                'top': c.most_common(10)}
    results[name] = r
    print(f"{name}: tokens={len(stream)} " +
          ' '.join(f"n={n}:types={r[n]['types']},zipf={r[n]['zipf']:.3f}" if r[n]['zipf'] else f"n={n}:types={r[n]['types']},zipf=NA" for n in (1,2,3)))

with open(os.path.join(OUT, 'zipf_results.json'), 'w') as f:
    json.dump({k: {str(n): {'types': v[n]['types'], 'tokens': v[n]['tokens'],
                            'zipf': v[n]['zipf'],
                            'top': [(t, c) for t, c in v[n]['top']]}
                 for n in (1,2,3)} for k, v in results.items()}, f, indent=1)

# ---------------------------------------------------------------- morpheme hex table
with open(os.path.join(OUT, 'quechua_phonetic_hex.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['morpheme', 'mtype', 'gloss', 'phonetic_hex', 'syllable_skeleton',
                'n_phonemes', 'hex_bytes'])
    for m, t, g in morphs:
        hx, skel, nph = morph_hex[m]
        w.writerow([m, t, g, hx, skel, nph, nph])

with open(os.path.join(OUT, 'roots_phonetic_hex.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['root', 'phonetic_hex', 'syllable_skeleton', 'n_phonemes'])
    for r, (hx, skel, nph) in root_hex.items():
        w.writerow([r, hx, skel, nph])

print('wrote quechua_phonetic_hex.csv, roots_phonetic_hex.csv, zipf_results.json')
