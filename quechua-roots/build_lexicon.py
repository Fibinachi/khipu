import json, re, sys, csv

with open('attestation.json') as f:
    data = json.load(f)

def is_likely_loan(lemma, wikt_loan_flag):
    """Phonological + flag-based loanword detection."""
    if wikt_loan_flag:
        return True, "wiktionary_flag"
    w = lemma.lower()
    # Spanish phonology markers not native to Quechua
    # f is never native
    if 'f' in w:
        return True, "contains_f"
    # Word-initial b/d/g/r are Spanish (native Quechua doesn't have these initially)
    if re.match(r'^[bdg]', w):
        return True, "initial_voiced_stop"
    if w.startswith('r'):
        return True, "initial_r"
    # Consonant clusters (except n+consonant, q+consonant which occur)
    # Spanish-style clusters: br, cr, dr, gr, pr, tr, bl, cl, gl, pl, etc.
    if re.search(r'[bcdfgprt]r|[bcdgfp]l', w):
        return True, "consonant_cluster"
    # Double consonants that aren't native geminates
    if re.search(r'bb|dd|gg|ff|vv|zz|jj|ss(?!$)', w):
        return True, "double_consonant"
    return False, ""

# Semantic domain keywords (Spanish and English glosses)
DOMAIN_KEYWORDS = {
    'kinship': ['madre','padre','hijo','hija','hermano','hermana','tío','tía','abuelo','abuela','nieto','esposo','esposa','familia','pariente','mother','father','son','daughter','brother','sister','uncle','aunt','wife','husband','family','kin'],
    'body': ['cabeza','ojo','mano','pie','brazo','pierna','boca','nariz','oreja','diente','cabello','sangre','corazón','cuerpo','head','eye','hand','foot','arm','leg','mouth','nose','ear','tooth','hair','blood','heart','body'],
    'natural_world': ['sol','luna','estrella','cielo','tierra','agua','río','mar','montaña','piedra','árbol','flor','sun','moon','star','sky','earth','water','river','sea','mountain','stone','tree','flower','nature'],
    'agriculture': ['maíz','papa','quinua','sembrar','cosecha','chacra','arar','semilla','maize','potato','quinoa','sow','harvest','field','plow','seed','agricult','crop'],
    'numbers': ['uno','dos','tres','cuatro','cinco','número','contar','one','two','three','four','five','number','count','numeral'],
    'colors': ['blanco','negro','rojo','color','white','black','red','color','colour'],
    'social_organization': ['pueblo','ayllu','jefe','cacique','comunidad','inca','rey','señor','village','chief','community','king','lord','social','tribute','mita'],
    'administration': ['tributo','contar','guardar','depósito','almacén','quenta','registro','tribute','count','store','warehouse','deposit','register','account','khipu','quipu'],
    'actions': ['hacer','decir','ir','venir','comer','beber','dar','tomar','do','make','say','go','come','eat','drink','give','take','verb'],
    'animals': ['llama','alpaca','perro','ave','pájaro','pez','serpiente','animal','dog','bird','fish','snake'],
    'food': ['comida','carne','pan','chicha','comer','food','meat','bread','eat','drink'],
    'time': ['día','noche','año','mes','tiempo','day','night','year','month','time'],
    'space_direction': ['arriba','abajo','aquí','allí','cerca','lejos','up','down','here','there','near','far'],
    'religion': ['dios','espíritu','santo','rezar','oración','god','spirit','saint','pray'],
    'materials': ['oro','plata','cobre','hierro','madera','piedra','lana','algodón','gold','silver','copper','iron','wood','wool','cotton'],
}

def classify_domain(gloss):
    g = gloss.lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in g:
                return domain
    return 'other'

lexicon = []
loans_removed = []
for r in data:
    lemma = r['lemma']
    is_loan, reason = is_likely_loan(lemma, r['wikt_loan_flag'])
    if is_loan:
        loans_removed.append({'lemma': lemma, 'reason': reason, 'gloss': r['gloss']})
        continue
    
    # Confidence based on attestation
    earliest = r['earliest']
    if earliest == 1560:
        confidence = 'certain_native'
    elif earliest == 1608:
        confidence = 'certain_native'
    else:
        # Modern only: probably native if passes phonology, but lower confidence
        confidence = 'probably_native'
    
    domain = classify_domain(r['gloss'])
    
    lexicon.append({
        'root': lemma,
        'gloss': r['gloss'],
        'pos': r['pos'],
        'semantic_domain': domain,
        'earliest_attestation': earliest if earliest else 'modern',
        'attested_1560': r['attested_1560'],
        'attested_1608': r['attested_1608'],
        'source': 'wiktionary',
        'confidence': confidence,
        'dialect_notes': '',
    })

print(f"Native roots: {len(lexicon)}", file=sys.stderr)
print(f"Loans removed: {len(loans_removed)}", file=sys.stderr)

# Domain distribution
from collections import Counter
domains = Counter(l['semantic_domain'] for l in lexicon)
for d, c in domains.most_common():
    print(f"  {d}: {c}", file=sys.stderr)

with open('lexicon_wikt.json','w') as f:
    json.dump(lexicon, f, ensure_ascii=False)
with open('loans_removed.json','w') as f:
    json.dump(loans_removed, f, ensure_ascii=False)
