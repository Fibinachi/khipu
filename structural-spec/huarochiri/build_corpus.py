"""Build natural colonial Quechua corpus from Huarochirí Ch.III + Holguín grammar examples.
Then run morpheme frequency analysis.
"""
import re, csv, json
from collections import Counter
from pathlib import Path

BASE = Path('/home/hatch/workspace/quipu-analysis')
HUAR = Path('/home/hatch/workspace/quipu-analysis/huarochiri')

# --- Load morpheme lexicon ---
morphs = []  # (morpheme_form, mtype, gloss)
with open(BASE/'isomorphism/quechua_morphemes.csv') as f:
    for row in csv.DictReader(f):
        m = row['morpheme'].lstrip('=-').lower()
        if m:
            morphs.append((m, row['mtype'], row['gloss']))
# Sort by length desc for longest-match
morphs.sort(key=lambda x: -len(x[0]))

# Load roots
roots = set()
with open(BASE/'quechua-roots/quechua_native_roots.csv') as f:
    for row in csv.DictReader(f):
        r = (row.get('root') or row.get('quechua') or '').strip().lower()
        if r and len(r) >= 2:
            roots.add(r)

def segment_word(word):
    """Longest-match segmentation. Returns list of (piece, type)."""
    w = word.lower().strip('.,;:!?()\"«»')
    if not w or len(w) < 2:
        return []
    pieces = []
    i = 0
    while i < len(w):
        best = None
        for m, mt, gl in morphs:
            if w.startswith(m, i) and (best is None or len(m) > len(best[0])):
                best = (m, mt, gl)
        if best and len(best[0]) >= 2:
            pieces.append(best)
            i += len(best[0])
        else:
            # try single char advance if we already have pieces (root residue)
            if pieces:
                i += 1
            else:
                return []  # can't start -> not Quechua
    return pieces

def quechua_score(sentence):
    """Fraction of words (len>=3) that segment into known morphemes."""
    words = [w for w in re.findall(r"[a-záéíóúñü]+", sentence.lower()) if len(w) >= 3]
    if len(words) < 3:
        return 0
    ok = sum(1 for w in words if segment_word(w))
    return ok / len(words)

# --- 1. Huarochirí Ch.III ---
hq = (HUAR/'sources/huarochiri_ch3_quechua.txt').read_text()
# Normalize Taylor orthography to be closer to segmentable form
# Taylor uses: sh, ch, q, ñ, k. Our morphemes use similar. Keep as-is.
huar_sentences = [s.strip() for s in re.split(r'[.!?]', hq) if s.strip()]

# --- 2. Holguín grammar examples ---
hg = open(BASE/'quechua-roots/holguin_gramatica.txt', encoding='utf-8', errors='ignore').read()
# Holguín examples: often after colons or in specific patterns. Extract candidate lines.
holguin_quechua_sents = []
for line in hg.split('\n'):
    line = line.strip()
    if len(line) < 20:
        continue
    # Split line into sentence-like chunks
    for chunk in re.split(r'[.;:!?]', line):
        chunk = chunk.strip()
        words = chunk.split()
        if 3 <= len(words) <= 25 and quechua_score(chunk) >= 0.5:
            # Exclude pure Spanish: must contain Quechua-specific chars or patterns
            if re.search(r'q[^u]|sh|ch|ñ|[^aeiou]y[^aeiou]|qq|chh', chunk.lower()):
                holguin_quechua_sents.append(chunk)

# Deduplicate
seen = set()
uniq_hg = []
for s in holguin_quechua_sents:
    k = s.lower()
    if k not in seen:
        seen.add(k)
        uniq_hg.append(s)

print(f"Huarochirí sentences: {len(huar_sentences)}")
print(f"Holguín Quechua sentences: {len(uniq_hg)}")
print("Sample Holguín:")
for s in uniq_hg[:5]:
    print("  ", s[:120])

# --- 3. Combine + tokenize ---
all_sents = [('huarochiri', s) for s in huar_sentences] + [('holguin', s) for s in uniq_hg]
morpheme_tokens = []  # (morpheme, mtype, gloss, source)
for src, sent in all_sents:
    for w in re.findall(r"[a-záéíóúñü]+", sent.lower()):
        segs = segment_word(w)
        for m, mt, gl in segs:
            morpheme_tokens.append((m, mt, gl, src))

print(f"\nTotal morpheme tokens: {len(morpheme_tokens)}")
print(f"Unique morphemes: {len(set(m for m,_,_,_ in morpheme_tokens))}")

# --- 4. Frequency ranking ---
freq = Counter(m for m,_,_,_ in morpheme_tokens)
# type/gloss lookup
info = {}
for m, mt, gl, src in morpheme_tokens:
    if m not in info:
        info[m] = (mt, gl)

# Save morpheme_frequencies.csv
with open(HUAR/'morpheme_frequencies.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['rank','morpheme','count','mtype','gloss','pct_of_tokens'])
    total = len(morpheme_tokens)
    for rank, (m, c) in enumerate(freq.most_common(), 1):
        mt, gl = info[m]
        w.writerow([rank, m, c, mt, gl, round(100*c/total,2)])

print("\nTop 30 morphemes:")
for rank, (m, c) in enumerate(freq.most_common(30), 1):
    mt, gl = info[m]
    print(f"  {rank:2d}. {m:12s} {c:5d}  [{mt}] {gl}")

# Save corpus stats
stats = {
    'huarochiri_sentences': len(huar_sentences),
    'huarochiri_words': len(re.findall(r'\w+', hq)),
    'holguin_sentences': len(uniq_hg),
    'total_morpheme_tokens': len(morpheme_tokens),
    'unique_morphemes': len(freq),
}
open(HUAR/'corpus_stats.json','w').write(json.dumps(stats, indent=2))

# Bigrams
bigrams = Counter()
for src, sent in all_sents:
    toks = []
    for w in re.findall(r"[a-záéíóúñü]+", sent.lower()):
        toks.extend(m for m,_,_ in segment_word(w))
    for a, b in zip(toks, toks[1:]):
        bigrams[(a,b)] += 1

with open(HUAR/'morpheme_bigrams.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['rank','bigram','count'])
    for rank, ((a,b), c) in enumerate(bigrams.most_common(50), 1):
        w.writerow([rank, f"{a}+{b}", c])

print("\nTop 15 bigrams:")
for (a,b), c in bigrams.most_common(15):
    print(f"   {a}+{b}: {c}")

# Zipf slope
import math
counts = sorted(freq.values(), reverse=True)
n = len(counts)
xs = [math.log(i+1) for i in range(n)]
ys = [math.log(c) for c in counts]
mx, my = sum(xs)/n, sum(ys)/n
slope = sum((x-mx)*(y-my) for x,y in zip(xs,ys)) / sum((x-mx)**2 for x in xs)
print(f"\nZipf slope: {slope:.3f} (n={n} morpheme types, {total} tokens)")
stats['zipf_slope'] = round(slope,3)
open(HUAR/'corpus_stats.json','w').write(json.dumps(stats, indent=2))
