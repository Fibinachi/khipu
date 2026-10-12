"""Build Hangman table, admin register, and reports."""
import csv, json
from pathlib import Path

BASE = Path('/home/hatch/workspace/quipu-analysis')
HUAR = BASE/'huarochiri'

# --- Load Quechua frequencies ---
qfreq = []
with open(HUAR/'morpheme_frequencies.csv') as f:
    for row in csv.DictReader(f):
        qfreq.append(row)

# --- Load khipu byte n-grams ---
kfreq = []
with open(BASE/'byte-patterns/khipu_byte_ngrams.csv') as f:
    for row in csv.DictReader(f):
        if row['n_bytes'] == '4':  # single-cord patterns only
            kfreq.append(row)
kfreq.sort(key=lambda r: -int(r['count']))

# Khipu pattern decodings (from byte-patterns analysis + khipu_hex.py)
# byte0 = (color_id << 2) | knot_high; byte1 = (knot_low<<7)|(dir<<5)|(level<<2)
DECODE = {
    'f8040000': 'W single-knot Z L1 val=0',
    '20040000': 'AB single-knot Z L1 val=0',
    'a4040000': 'MB single-knot Z L1 val=0',
    'f8080000': 'W single-knot Z L2 val=0',
    '84040000': 'KB single-knot Z L1 val=0',
}

# --- Hangman table ---
with open(HUAR/'hangman_table.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['rank','q_morpheme','q_count','q_pct','q_type','q_gloss',
                'k_hex','k_count','k_khipu','k_decode','alignment_note'])
    n = min(len(qfreq), len(kfreq), 30)
    for i in range(n):
        q = qfreq[i]; k = kfreq[i]
        hx = k['ngram_hex']
        note = ''
        # Suggest alignments based on rank + type
        if i == 0:
            note = 'Rank-1 both: most frequent function unit. Q=-ta(ACC). K=W:0. Hypothesis: W marks accusative/case role.'
        elif i == 1:
            note = 'Q=-si(REPORTATIVE, narrative genre). K=AB:0. Genre mismatch: admin khipu may rank -mi higher. AB may mark evidentiality.'
        elif i == 2:
            note = 'Q=-kuna(PL). K=MB:0. Hypothesis: MB marks plurality/collectivity.'
        elif i == 3:
            note = 'Q=-pas(ADD). K=W:0@L2. Level shift: L2 grammatical marking.'
        elif q['mtype'] == 'enclitic' and 'evid' in q['gloss'].lower():
            note = 'Evidential enclitic. Compare to khipu marking gradient (L1->L3).'
        elif 'case' in q['gloss'].lower() or q['mtype'] == 'suffix' and any(x in q['gloss'] for x in ['ACC','GEN','LOC','ALL','ABL','COM','BEN','LIM']):
            note = 'Case suffix. Candidate for color-tier mapping.'
        w.writerow([i+1, q['morpheme'], q['count'], q['pct'], q['mtype'], q['gloss'],
                    hx, k['count'], k['n_khipu'], DECODE.get(hx,''),
                    note])

print(f"Hangman table: {n} rows")

# --- Admin register ---
# Domains relevant to Inca bureaucracy
ADMIN_DOMAINS = {'administration','numbers','social_organization','warfare','textiles',
                 'agriculture','food','materials','time','space_direction'}
# Administrative verbs to pull from 'actions'
ADMIN_VERBS = {'give','take','bring','carry','count','store','keep','guard',
    'deliver','receive','send','collect','gather','distribute','divide',
    'measure','weigh','write','record','order','command','serve','work',
    'pay','owe','lend','borrow','buy','sell','exchange','tribute'}

admin_words = []
with open(BASE/'quechua-roots/quechua_native_roots.csv') as f:
    for row in csv.DictReader(f):
        dom = row['semantic_domain']
        gloss = (row['gloss'] or '').lower()
        root = row['root']
        if dom in ADMIN_DOMAINS:
            admin_words.append(row)
        elif dom == 'actions' and any(v in gloss for v in ADMIN_VERBS):
            admin_words.append(row)

# Add grammatical morphemes that are administrative (case, evidentiality)
with open(BASE/'isomorphism/quechua_morphemes.csv') as f:
    for row in csv.DictReader(f):
        if row['domain'] in ('case','evidentiality'):
            admin_words.append({
                'root': row['morpheme'], 'gloss': row['gloss'], 'pos': row['mtype'],
                'semantic_domain': 'grammar_'+row['domain'],
                'earliest_attestation': row['oldest_form'],
                'attested_1560': '', 'attested_1608': '',
                'source': row['source'], 'confidence': '', 'dialect_notes': ''
            })

with open(HUAR/'admin_register.csv','w',newline='') as f:
    w = csv.writer(f)
    w.writerow(['word','gloss','pos','semantic_domain','earliest','holguin_1608','santo_tomas_1560','source'])
    for r in sorted(admin_words, key=lambda x: (x['semantic_domain'], x['root'])):
        w.writerow([r['root'], r['gloss'], r['pos'], r['semantic_domain'],
                    r['earliest_attestation'],
                    r.get('attested_1608',''), r.get('attested_1560',''),
                    r['source']])

print(f"Admin register: {len(admin_words)} entries")
from collections import Counter
print(Counter(r['semantic_domain'] for r in admin_words))

print("\nDone.")
