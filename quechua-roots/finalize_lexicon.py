import json, re, sys, csv
from collections import Counter

with open('lexicon_wikt.json') as f:
    wikt_lex = json.load(f)
with open('lexicon_holguin_clean.json') as f:
    holg_lex = json.load(f)

# Improved domain classification with more keywords
DOMAIN_PATTERNS = [
    ('kinship', r'madre|padre|hijo|hija|herman[oa]|t[ií]o|t[ií]a|abuel[oa]|niet[oa]|espos[oa]|marido|mujer|familia|pariente|mother|father|son|daughter|brother|sister|uncle|aunt|wife|husband|family|kin|child'),
    ('body', r'cabeza|ojo|ojos|mano|pie|brazo|pierna|boca|nariz|oreja|diente|cabello|sangre|coraz[oó]n|cuerpo|dedo|uña|lengua|head|eye|hand|foot|arm|leg|mouth|nose|ear|tooth|hair|blood|heart|body|finger'),
    ('natural_world', r'\bsol\b|luna|estrella|cielo|tierra|agua|r[ií]o|mar|monta[ñn]a|piedra|[aá]rbol|flor|cerro|quebrada|laguna|sun|moon|star|sky|earth|water|river|sea|mountain|stone|tree|flower'),
    ('agriculture', r'ma[ií]z|papa|quinua|oca|sembrar|cosech|chacra|chakra|arar|semilla|plantar|maize|potato|quinoa|sow|harvest|field|plow|seed|agricult|crop|tuber'),
    ('numbers', r'uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|cien|mil|n[uú]mero|contar|one|two|three|four|five|six|seven|eight|nine|ten|hundred|thousand|number|count'),
    ('colors', r'blanco|negro|rojo|amarillo|verde|azul|color|white|black|red|yellow|green|blue|colou?r'),
    ('social_organization', r'pueblo|ayllu|jefe|cacique|comunidad|curaca|rey|se[ñn]or|village|chief|community|king|lord|tributo|mita|mitayo'),
    ('administration', r'tributo|guardar|dep[oó]sito|almac[eé]n|cuenta|registro|escribano|quipu|khipu|tribute|store|warehouse|deposit|register|account|record'),
    ('actions', r'hacer|decir|ir\b|venir|comer|beber|dar\b|tomar|caminar|correr|dormir|despertar|hablar|callar|llorar|re[íi]r|do\b|make|say|go\b|come|eat|drink|give|take|walk|run|sleep|speak|laugh|cry'),
    ('animals', r'llama|alpaca|vicu[ñn]a|perro|ave|p[aá]jaro|pez|serpiente|c[óo]ndor|puma|animal|dog|bird|fish|snake|camelid'),
    ('food', r'comida|carne|chicha|comer|beber|aliment|food|meat|eat|drink|maize beer'),
    ('time', r'd[ií]a|noche|a[ñn]o|mes|tiempo|ma[ñn]ana|ayer|day|night|year|month|time|morning|yesterday'),
    ('space_direction', r'arriba|abajo|aqu[ií]|all[ií]|cerca|lejos|dentro|fuera|encima|debajo|up\b|down|here|there|near|far|inside|outside|above|below'),
    ('religion', r'dios|esp[ií]ritu|santo|rezar|oraci[óo]n|huaca|wak\'?a|god|spirit|saint|pray|shrine'),
    ('materials', r'oro|plata|cobre|hierro|madera|piedra|lana|algod[óo]n|barro|gold|silver|copper|iron|wood|wool|cotton|clay|metal'),
    ('textiles', r'tejer|hilar|tela|vestido|poncho|manta|weave|spin|cloth|clothe|garment|textile'),
    ('warfare', r'guerra|pelear|arma|arco|flecha|honda|war|fight|weapon|bow|arrow|sling'),
]

def classify(gloss):
    g = ' ' + gloss.lower() + ' '
    for domain, pattern in DOMAIN_PATTERNS:
        if re.search(pattern, g):
            return domain
    return 'other'

# Combine
all_entries = []
for e in wikt_lex:
    e['semantic_domain'] = classify(e['gloss'])
    all_entries.append(e)
for e in holg_lex:
    e['semantic_domain'] = classify(e['gloss'])
    # POS unknown for Holguín-only; guess from gloss
    g = e['gloss'].lower()
    if re.search(r'\b(el|la|los|las)\b.*\b(es|son)\b', g[:30]):
        e['pos'] = 'Noun?'
    elif re.search(r'hacer|action|verb', g[:50]):
        e['pos'] = 'Verb?'
    all_entries.append(e)

print(f"Total lexicon: {len(all_entries)}", file=sys.stderr)
print(f"  Wiktionary native: {len(wikt_lex)}", file=sys.stderr)
print(f"  Holguín-only: {len(holg_lex)}", file=sys.stderr)

# Stats
att = Counter(e['earliest_attestation'] for e in all_entries)
print(f"Attestation: {dict(att)}", file=sys.stderr)
dom = Counter(e['semantic_domain'] for e in all_entries)
print("Domains:", file=sys.stderr)
for d, c in dom.most_common(20):
    print(f"  {d}: {c}", file=sys.stderr)

# Write CSV
with open('quechua_native_roots.csv','w',newline='',encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=['root','gloss','pos','semantic_domain','earliest_attestation','attested_1560','attested_1608','source','confidence','dialect_notes'])
    w.writeheader()
    for e in sorted(all_entries, key=lambda x: (str(x['earliest_attestation']), x['root'])):
        w.writerow({k: e.get(k,'') for k in ['root','gloss','pos','semantic_domain','earliest_attestation','attested_1560','attested_1608','source','confidence','dialect_notes']})

print("CSV written", file=sys.stderr)
