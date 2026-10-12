import json, urllib.request, urllib.parse, time, sys

def api(params):
    params['format'] = 'json'
    url = 'https://en.wiktionary.org/w/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': 'QuechuaLexiconResearch/1.0 (research use)'})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)

# Get all Quechua lemmas
lemmas = []
cmcontinue = None
while True:
    p = {'action':'query','list':'categorymembers','cmtitle':'Category:Quechua_lemmas',
         'cmlimit':500, 'cmtype':'page'}
    if cmcontinue: p['cmcontinue'] = cmcontinue
    d = api(p)
    lemmas.extend([x['title'] for x in d['query']['categorymembers']])
    if 'continue' in d:
        cmcontinue = d['continue']['cmcontinue']
    else:
        break
    time.sleep(0.3)

print(f"Total lemmas: {len(lemmas)}", file=sys.stderr)
with open('wikt_lemmas.json','w') as f:
    json.dump(lemmas, f)
print("saved", file=sys.stderr)
