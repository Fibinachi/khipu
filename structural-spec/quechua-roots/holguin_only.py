import json, re, sys, unicodedata

def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

def normalize_q(word):
    w = word.lower().strip()
    w = strip_accents(w)
    w = w.replace('cc', 'k').replace('qq', 'q').replace('cqu', 'k')
    w = w.replace('hu', 'w').replace('gu', 'w').replace('gua', 'wa')
    w = re.sub(r'[^a-z]', '', w)
    return w

# Load Wiktionary normalized forms
with open('attestation.json') as f:
    wikt_data = json.load(f)
wikt_norms = set(r['normalized'] for r in wikt_data)

# Load Holguín parsed entries
with open('holguin_roots_raw.json') as f:
    holguin = json.load(f)

# Extract clean Quechua headwords
# Pattern: headword is Quechua-like (contains q/k/hua/y), 3+ chars, at entry start
holguin_only = []
seen = set()
for entry in holguin:
    hw = entry['quechua_1608']
    # Split variants on , o /
    variants = re.split(r',\s*o\s+|,\s*|\s+o\s+', hw)
    for v in variants:
        v = v.strip()
        # Must look like Quechua: 3+ chars, has q/k/w/y
        if len(v) < 3 or len(v) > 25:
            continue
        if not re.search(r'[qkwhy]', v.lower()):
            continue
        # Skip if obviously Spanish
        if re.search(r'[fbdgjz]', v.lower()):
            continue
        n = normalize_q(v)
        if len(n) < 3:
            continue
        if n in wikt_norms or n in seen:
            continue
        seen.add(n)
        holguin_only.append({
            'root': v,
            'normalized': n,
            'gloss': entry['gloss_es'][:200],
            'pos': '',
            'semantic_domain': '',
            'earliest_attestation': 1608,
            'attested_1560': False,
            'attested_1608': True,
            'source': 'holguin_1608',
            'confidence': 'certain_native',
            'dialect_notes': 'Cuzco cortesano (Holguín)',
        })

print(f"Holguín-only roots: {len(holguin_only)}", file=sys.stderr)
for h in holguin_only[:10]:
    print(f"  {h['root']} | {h['gloss'][:60]}", file=sys.stderr)

with open('lexicon_holguin_only.json','w') as f:
    json.dump(holguin_only, f, ensure_ascii=False)
