import json, re, sys, unicodedata

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def normalize_q(word):
    """Normalize Quechua word for fuzzy matching across orthographies."""
    w = word.lower().strip()
    w = strip_accents(w)
    # Colonial variants -> simplified
    w = w.replace('cc', 'k').replace('qq', 'q').replace('cqu', 'k')
    w = w.replace('hu', 'w').replace('gu', 'w').replace('gua', 'wa')
    w = re.sub(r'[^a-z]', '', w)
    return w

# Load colonial texts
print("Loading colonial texts...", file=sys.stderr)
with open('vocabulariodelal01gonz.txt', encoding='utf-8', errors='replace') as f:
    holguin = f.read()
with open('lexiconovocabula00domi.txt', encoding='utf-8', errors='replace') as f:
    santo = f.read()

# Build normalized search indices (set of normalized tokens)
def tokenize(text):
    tokens = set()
    for tok in re.findall(r"[a-záéíóúñü']{3,}", text.lower()):
        n = normalize_q(tok)
        if len(n) >= 3:
            tokens.add(n)
    return tokens

print("Tokenizing Holguin...", file=sys.stderr)
holguin_tokens = tokenize(holguin)
print(f"Holguin tokens: {len(holguin_tokens)}", file=sys.stderr)
print("Tokenizing Santo Tomas...", file=sys.stderr)
santo_tokens = tokenize(santo)
print(f"Santo tokens: {len(santo_tokens)}", file=sys.stderr)

# Load Wiktionary details
with open('wikt_details.json') as f:
    wikt = json.load(f)

results = []
for lemma, info in wikt.items():
    n = normalize_q(lemma)
    in_holguin = n in holguin_tokens
    in_santo = n in santo_tokens
    if in_santo:
        earliest = 1560
    elif in_holguin:
        earliest = 1608
    else:
        earliest = None  # modern only
    results.append({
        'lemma': lemma,
        'normalized': n,
        'pos': info.get('pos',''),
        'gloss': info.get('gloss',''),
        'wikt_loan_flag': info.get('wikt_loan_flag', False),
        'attested_1560': in_santo,
        'attested_1608': in_holguin,
        'earliest': earliest,
    })

with open('attestation.json','w') as f:
    json.dump(results, f, ensure_ascii=False)

n1560 = sum(1 for r in results if r['earliest']==1560)
n1608 = sum(1 for r in results if r['earliest']==1608)
nmod = sum(1 for r in results if r['earliest'] is None)
print(f"1560: {n1560}, 1608: {n1608}, modern-only: {nmod}", file=sys.stderr)
