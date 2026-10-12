import json, urllib.request, urllib.parse, time, sys, re

def api(params):
    params['format'] = 'json'
    url = 'https://en.wiktionary.org/w/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': 'QuechuaLexiconResearch/1.0 (research use)'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.load(r)

with open('wikt_lemmas.json') as f:
    lemmas = json.load(f)

results = {}
BATCH = 50
for i in range(0, len(lemmas), BATCH):
    batch = lemmas[i:i+BATCH]
    d = api({'action':'query','prop':'revisions','rvprop':'content','rvslots':'main',
             'titles':'|'.join(batch),'formatversion':2})
    for pg in d['query'].get('pages', []):
        title = pg.get('title','')
        try:
            text = pg['revisions'][0]['slots']['main']['content']
        except (KeyError, IndexError):
            continue
        # Extract Quechua section
        # Find ==Quechua== section
        m = re.search(r'==Quechua==(.*?)(?=\n==[^=]|\Z)', text, re.DOTALL)
        if not m:
            continue
        qsec = m.group(1)
        # Etymology
        etym = ''
        em = re.search(r'===Etymology.*?\n(.*?)(?=\n===|\n====|\Z)', qsec, re.DOTALL)
        if em: etym = em.group(1).strip()[:500]
        # POS and gloss: find first ===Noun=== etc with # definition
        pos = ''
        gloss = ''
        for p in ['Noun','Verb','Adjective','Adverb','Numeral','Pronoun','Particle','Interjection','Proper noun']:
            pm = re.search(r'==='+p+r'===(.*?)(?=\n===|\Z)', qsec, re.DOTALL)
            if pm:
                pos = p
                gm = re.search(r'^#\s*(.*?)$', pm.group(1), re.MULTILINE)
                if gm:
                    gloss = re.sub(r'\[\[|\]\]|\{\{.*?\}\}', '', gm.group(1)).strip()[:200]
                break
        # Check for Spanish borrowing markers
        is_loan = bool(re.search(r'[Bb]orrowed from Spanish|from Spanish|Spanish \w+|[Dd]erived from Spanish', text[:2000], re.IGNORECASE))
        results[title] = {'pos': pos, 'gloss': gloss, 'etymology': etym[:200], 'wikt_loan_flag': is_loan}
    print(f"{i+len(batch)}/{len(lemmas)}", file=sys.stderr)
    time.sleep(0.5)

with open('wikt_details.json','w') as f:
    json.dump(results, f, ensure_ascii=False)
print(f"Details for {len(results)}", file=sys.stderr)
