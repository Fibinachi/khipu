#!/usr/bin/env python3
"""
Build the Quechua morpheme co-occurrence database for distributional isomorphism
matching against the khipu feature database.

Mirrors build_khipu_features.py: same PMI formula (log2), same min-count (>=3),
same output formats. See isomorphism/README.md for the join spec.

Quechua "phrases" here are WORD-FORMS (morpheme sequences in surface order).
Each row = one word decomposed into morpheme-feature IDs.

Data sources (marked per-row in quechua_phrases.csv `origin` field):
  - attested: segmented from glossed examples in quechua-reference-grammar.md
             and colonial_grammar_notes.md
  - template: generated from documented morphological templates
             (ROOT-derivational-inflectional=enclitics; Faller SALT 2002)

The template-generated majority means Quechua co-occurrence here reflects the
GRAMMAR DESCRIPTION's structure, not natural-text frequencies. The isomorphism
therefore tests whether khipu patterns match Quechua's grammatical TYPOLOGY.
This is stated explicitly in isomorphism_results.md.
"""

import csv, math, os, itertools
from collections import Counter, defaultdict

OUT = os.path.expanduser("~/workspace/quipu-analysis/isomorphism")

# ----------------------------------------------------------------------------
# 1b. Administrative roots from quechua_native_roots.csv (researcher constraint:
#     khipu encode STATE vocabulary; weight administrative register heaviest)
# ----------------------------------------------------------------------------
import re as _re

def load_admin_roots():
    admin_domains = {'numbers', 'agriculture', 'animals', 'social_organization',
                     'colors', 'materials', 'administration'}
    out = []
    with open(os.path.expanduser("~/workspace/quipu-analysis/quechua-roots/quechua_native_roots.csv")) as f:
        for r in csv.DictReader(f):
            if r['earliest_attestation'] not in ('1560', '1608'):
                continue
            if r['semantic_domain'] not in admin_domains:
                continue
            root = r['root'].strip()
            # cleanliness filter: plausible Quechua orthography, has gloss
            if not _re.match(r"^[a-záéíóúñü' -]+$", root):
                continue
            if len(root) > 25 or len(root) < 2:
                continue
            if not r['gloss'] or len(r['gloss'].strip()) < 2:
                continue
            # skip entries that are clearly OCR garbage (excessive punctuation)
            if _re.search(r"[*_©\[\]0-9/]{2,}", r['gloss']):
                continue
            # 1608 OCR is noisy: require 1560 attestation OR phonotactic plausibility.
            # Quechua phonotactics: no word-initial tt/pp/kk/cc clusters, no 'cnk',
            # no hyphen except medial, max 2 consecutive vowels.
            if r['earliest_attestation'] == '1608':
                if _re.match(r"^(tt|pp|kk|cc|chh)", root):
                    continue
                if _re.search(r"cnk|ncn|qcc|ycc", root):
                    continue
                if root.startswith('-') or root.endswith('-'):
                    continue
                if _re.search(r"[aeiouáéíóú]{3,}", root):
                    continue
                # reject roots with no vowel (likely OCR fragments)
                if not _re.search(r"[aeiouáéíóú]", root):
                    continue
            pos = r['pos'] if r['pos'] in ('Noun', 'Verb', 'Adjective', 'Numeral',
                                           'Adverb', 'Pronoun') else 'Noun'
            out.append((root, r['gloss'][:60], pos, r['semantic_domain']))
    # dedupe by root
    seen, deduped = set(), []
    for e in out:
        if e[0] not in seen:
            seen.add(e[0])
            deduped.append(e)
    return deduped

ADMIN_ROOTS = load_admin_roots()
print(f"administrative roots loaded: {len(ADMIN_ROOTS)}")

# ----------------------------------------------------------------------------
# 1c. Military roots (researcher: military = state vocabulary; some khipu may
#     be military documents). Oldest attested FORM used as primary label
#     (researcher oldest-variant rule: 1560 > 1608 > modern).
#     Format: (oldest_form, modern_form, gloss, pos, source)
# ----------------------------------------------------------------------------
MILITARY = [
    ("auca",     "awqa",    "enemy, adversary",          "Noun", "1560 ST"),
    ("aucacona", "awqakuna","warriors, people of war",   "Noun", "1560 ST"),
    ("atiy",     "atiy",    "to defeat, to conquer",     "Verb", "1560 ST/1608 H"),
    ("fuyuchak", "fuyuchak","captain, war leader",       "Noun", "1560 ST"),
    ("checni",   "checni",  "public enemy",              "Noun", "1560 ST"),
    ("wach'i",   "wach'i",  "arrow, spear",              "Noun", "1560 ST"),
    ("champi",   "champi",  "war club, mace",            "Noun", "1608 H"),
    ("auccay",   "awqay",   "to fight, to combat",       "Verb", "1608 H"),
    ("pukara",   "pukara",  "fortress",                  "Noun", "modern"),
    ("llalliy",  "llalliy", "to defeat, to conquer",     "Verb", "modern"),
    ("awqaq",    "awqaq",   "warrior, fighter",          "Noun", "modern"),
    ("suyuchakuy", "suyuchakuy", "to muster troops, parade", "Verb", "1560 ST"),
    ("guallpa",  "huallpa", "armed man",                 "Noun", "1560 ST"),
]

# ----------------------------------------------------------------------------
# 1. Morpheme inventory
# ----------------------------------------------------------------------------
# mtype: root | suffix | enclitic | particle
# domain: grammatical subsystem, or semantic domain for roots
# admin flag: 1 if in the state-administrative vocabulary (researcher constraint)

GRAMMATICAL = [
    # --- Evidentials (enclitics; mutually exclusive per clause) ---
    ("enclitic", "=mi",  "EVD.Direct/BestGrounds", "Faller2002", "evidentiality"),
    ("enclitic", "=si",  "EVD.Reportative",        "Faller2002", "evidentiality"),
    ("enclitic", "=cha", "EVD.Conjectural",        "Faller2002", "evidentiality"),
    ("enclitic", "=chusina", "EVD.PercInferential","Faller2002", "evidentiality"),
    # --- Case markers (suffixes; attach to nouns) ---
    ("suffix", "-ta",    "ACC",  "Cusihuaman", "case"),
    ("suffix", "-man",   "ALL",  "Cusihuaman", "case"),
    ("suffix", "-pi",    "LOC",  "Cusihuaman", "case"),
    ("suffix", "-manta", "ABL",  "Cusihuaman", "case"),
    ("suffix", "-pa",    "GEN",  "Cusihuaman", "case"),
    ("suffix", "-q",     "GEN.alt", "Cusihuaman", "case"),
    ("suffix", "-wan",   "COM/INST", "Cusihuaman", "case"),
    ("suffix", "-paq",   "BEN",  "Cusihuaman", "case"),
    ("suffix", "-kama",  "LIM",  "Cusihuaman", "case"),
    # --- Tense/aspect (verbal suffixes) ---
    ("suffix", "-rqa",   "PST.Witnessed", "Mannheim1998", "tense"),
    ("suffix", "-sqa",   "PST.Narrative", "Mannheim1998", "tense"),
    ("suffix", "-shaq",  "FUT.1/2",       "Cusihuaman",   "tense"),
    ("suffix", "-nqa",   "FUT.3",         "Cusihuaman",   "tense"),
    ("suffix", "-chka",  "PROG",          "Cusihuaman",   "tense"),
    ("suffix", "-qka",   "HAB.PST",       "Cusihuaman",   "tense"),
    # --- Nominalizers ---
    ("suffix", "-na",    "NOMLZ.oblig",   "Rios2013", "nominalization"),
    ("suffix", "-y",     "INF",           "Rios2013", "nominalization"),
    ("suffix", "-q",     "AGENTIVE",      "Rios2013", "nominalization"),
    # note: -sqa doubles as nominalizer; listed once under tense
    # --- Switch-reference ---
    ("suffix", "-spa",   "SS",            "Cusihuaman", "switchref"),
    ("suffix", "-qti",   "DS",            "Cusihuaman", "switchref"),
    # --- Topic/focus ---
    ("suffix", "-qa",    "TOP",           "Sanchez2010", "topicfocus"),
    ("suffix", "-taq",   "CTOP",          "Sanchez2010", "topicfocus"),
    ("enclitic", "=lla", "EXCL.only",     "Sanchez2010", "topicfocus"),
    ("enclitic", "=pas", "ADD.too",       "Sanchez2010", "topicfocus"),
    # --- Negation ---
    ("particle", "mana", "NEG",           "Faller2002", "negation"),
    ("suffix", "-chu",   "NEG/INT",       "Faller2002", "negation"),
    # --- Possessives (nominal) ---
    ("suffix", "-y",       "POSS.1SG",  "Cusihuaman", "possession"),
    ("suffix", "-yki",     "POSS.2SG",  "Cusihuaman", "possession"),
    ("suffix", "-n_poss",  "POSS.3",    "Cusihuaman", "possession"),
    ("suffix", "-nchis",   "POSS.1INCL","Cusihuaman", "possession"),
    ("suffix", "-yku",     "POSS.1EXCL","Cusihuaman", "possession"),
    ("suffix", "-nku",     "POSS.3PL",  "Cusihuaman", "possession"),
    # --- Verbal person agreement ---
    ("suffix", "-ni",      "1SG.S",     "Cusihuaman", "agreement"),
    ("suffix", "-nki",     "2SG.S",     "Cusihuaman", "agreement"),
    ("suffix", "-n_agr",   "3.S",       "Cusihuaman", "agreement"),
    ("suffix", "-nchis_agr","1INCL.S",  "Cusihuaman", "agreement"),
    ("suffix", "-yku_agr", "1EXCL.S",   "Cusihuaman", "agreement"),
    ("suffix", "-nku_agr", "3PL.S",     "Cusihuaman", "agreement"),
    ("suffix", "-wa-",     "1SG.O",     "SantoTomas1560", "agreement"),
    ("suffix", "-su-",     "2SG.O",     "SantoTomas1560", "agreement"),
    # --- Plural ---
    ("suffix", "-kuna",  "PL",          "Cusihuaman", "number"),
    # --- Derivational (common, template-relevant) ---
    ("suffix", "-chi",   "CAUS",        "Cusihuaman", "derivation"),
    ("suffix", "-ku",    "REFL/MID",    "Cusihuaman", "derivation"),
    ("suffix", "-mu",    "CISL",        "Cusihuaman", "derivation"),
    ("suffix", "-pu",    "BEN",         "Cusihuaman", "derivation"),
    ("suffix", "-ri",    "INCH",        "Cusihuaman", "derivation"),
]

# Lexical roots: curated from quechua_native_roots.csv
# Priority: 1560-attested administrative/agricultural/social + clean glosses.
# Format: (root, gloss, pos, domain)
LEXICAL = [
    # --- 1560-attested, administrative/agricultural core ---
    ("papa", "potato", "Noun", "agriculture"),
    ("sara", "maize", "Noun", "agriculture"),
    ("uqa", "oca tuber", "Noun", "agriculture"),
    ("yupana", "counting device", "Noun", "administration"),
    ("tawa", "four", "Numeral", "numbers"),
    ("llama", "llama", "Noun", "animals"),
    ("wasi", "house", "Noun", "social_organization"),
    ("ayllu", "kin group/community", "Noun", "social_organization"),
    ("inka", "inka/ruler", "Noun", "social_organization"),
    ("kuraka", "local lord", "Noun", "social_organization"),
    ("mita", "labor turn", "Noun", "administration"),
    ("chunka", "ten", "Numeral", "numbers"),
    ("pachak", "hundred", "Numeral", "numbers"),
    ("waranqa", "thousand", "Numeral", "numbers"),
    ("huk", "one", "Numeral", "numbers"),
    ("iskay", "two", "Numeral", "numbers"),
    ("kimsa", "three", "Numeral", "numbers"),
    ("tayta", "father", "Noun", "kinship"),
    ("mama", "mother", "Noun", "kinship"),
    ("wawa", "child", "Noun", "kinship"),
    ("chakra", "field", "Noun", "agriculture"),
    ("yaku", "water", "Noun", "natural_world"),
    ("allpa", "earth/land", "Noun", "natural_world"),
    ("kuka", "coca", "Noun", "agriculture"),
    ("kinwa", "quinoa", "Noun", "agriculture"),
    ("chuqllu", "fresh maize", "Noun", "agriculture"),
    ("muru", "seed", "Noun", "agriculture"),
    # --- 1560-attested actions ---
    ("riy", "to go", "Verb", "actions"),
    ("hamuy", "to come", "Verb", "actions"),
    ("quy", "to give", "Verb", "actions"),
    ("chaskiy", "to receive", "Verb", "actions"),
    ("yachay", "to know/learn", "Verb", "actions"),
    ("rimay", "to speak", "Verb", "actions"),
    ("ruway", "to do/make", "Verb", "actions"),
    ("mikuy", "to eat", "Verb", "actions"),
    ("upiy", "to drink", "Verb", "actions"),
    ("puriy", "to walk", "Verb", "actions"),
    ("haykuy", "to enter", "Verb", "actions"),
    ("lluqshiy", "to exit", "Verb", "actions"),
    ("apay", "to carry", "Verb", "actions"),
    ("churay", "to place/put", "Verb", "actions"),
    ("kipuy", "to knot (quipu)", "Verb", "actions"),
    ("yupay", "to count", "Verb", "administration"),
    ("qillqay", "to write/mark", "Verb", "administration"),
    ("waqaychay", "to guard/store", "Verb", "administration"),
    ("taqiy", "to distribute", "Verb", "administration"),
    ("rantiy", "to buy/barter", "Verb", "administration"),
    # --- 1608/colonial administrative ---
    ("qullqa", "storehouse", "Noun", "administration"),
    ("tampu", "waystation", "Noun", "administration"),
    ("suyu", "region/quarter", "Noun", "administration"),
    ("wamani", "province", "Noun", "administration"),
    ("tokrikuq", "overseer", "Noun", "administration"),
    ("khipukamayuq", "khipu keeper", "Noun", "administration"),
    ("chaski", "messenger", "Noun", "administration"),
    # --- colors (khipu-relevant) ---
    ("yana", "black", "Adjective", "colors"),
    ("yuraq", "white", "Adjective", "colors"),
    ("puka", "red", "Adjective", "colors"),
    ("qillu", "yellow", "Adjective", "colors"),
    ("anqas", "blue", "Adjective", "colors"),
    ("chumpi", "brown", "Adjective", "colors"),
    ("warmi", "woman", "Noun", "kinship"),
    ("qari", "man", "Noun", "kinship"),
    ("punchaw", "day", "Noun", "time"),
    ("killa", "moon/month", "Noun", "time"),
    ("wata", "year", "Noun", "time"),
    ("tutamanta", "morning", "Noun", "time"),
]

# ----------------------------------------------------------------------------
# 2. Attested examples (segmented from grammar docs)
# Each: (surface, [morpheme sequence], source)
# ----------------------------------------------------------------------------
ATTESTED = [
    ("Parashan=mi", ["para", "-sha", "-n_agr", "=mi"], "Faller2002"),
    ("Parashan=si", ["para", "-sha", "-n_agr", "=si"], "Faller2002"),
    ("Parashan=chá", ["para", "-sha", "-n_agr", "=cha"], "Faller2002"),
    ("Mana rinichu", ["mana", "riy", "-ni", "-chu"], "Faller2002"),
    ("Mana taytaytaqa rimarichisqakupaschu",
     ["mana", "tayta", "-y", "-ta", "-qa", "rimay", "-ri", "-chi", "-sqa", "-ku", "=pas", "-chu"],
     "Faller2002"),
    ("Rinayta munani", ["riy", "-na", "-y", "-ta", "munay", "-ni"], "Rios2013"),
    ("Yachasqaykita ama qunqankichu",
     ["yachay", "-sqa", "-yki", "-ta", "ama", "qunqay", "-nki", "-chu"], "Rios2013"),
    ("Utavaluman chayashpa, ñuka mamata rikurkani",
     ["utavalu", "-man", "chayay", "-spa", "ñuka", "mama", "-ta", "riy", "-ku", "-rqa", "-ni"],
     "Cole1983"),
    ("Juzi Utavaluman chayajpi, paypaj wasiman rirkani",
     ["juzi", "utavalu", "-man", "chayay", "-qti", "pay", "-pa", "-q", "wasi", "-man", "riy", "-rqa", "-ni"],
     "Cole1983"),
    ("Mamayqa qheswata rin",
     ["mama", "-y", "-qa", "qheswa", "-ta", "riy", "-n_agr"], "Sanchez2010"),
    ("Taytaytaq chakrata",
     ["tayta", "-y", "-taq", "chakra", "-ta"], "Sanchez2010"),
    ("Domingolla", ["domingo", "=lla"], "Sanchez2010"),
    ("Inkapas", ["inka", "=pas"], "Sanchez2010"),
    ("Allquqa kawalluta kanin",
     ["allqu", "-qa", "kawallu", "-ta", "kaniy", "-n_agr"], "Cusihuaman"),
    ("wasiyki", ["wasi", "-yki"], "Cusihuaman"),
    ("taytay", ["tayta", "-y"], "Cusihuaman"),
    ("Phuturiq wawan", ["phuturi", "-q", "wawa", "-n_poss"], "Cusihuaman"),
    ("Munascca casccaymi", ["munay", "-sqa", "kay", "=mi"], "Holguin1607"),
    ("Manascca casccavmicarca", ["mana", "-sqa", "kay", "=mi", "-rqa"], "Holguin1607"),
    ("Cachcarcani", ["kachkay", "-rqa", "-ni"], "Holguin1607"),
    ("kuchana", ["kuchuy", "-na"], "Rios2013"),
    ("Pukllaq", ["pukllay", "-q"], "Rios2013"),
    ("Rimay", ["rimay", "-y"], "Rios2013"),
]

# Some roots used in ATTESTED but not in LEXICAL — add as needed
EXTRA_ROOTS = [
    ("para", "to rain", "Verb", "natural_world"),
    ("-sha", "3SG.PROG?", "suffix", "tense"),  # placeholder gloss; actually -sha- is 3sg progressive-ish
    ("munay", "to want/love", "Verb", "actions"),
    ("ama", "NEG.IMP", "particle", "negation"),
    ("qunqay", "to forget", "Verb", "actions"),
    ("utavalu", "Otavalo (place)", "Proper noun", "space_direction"),
    ("chayay", "to arrive", "Verb", "actions"),
    ("ñuka", "I (Ecuador)", "Pronoun", "pronouns"),
    ("juzi", "José", "Proper noun", "names"),
    ("pay", "he/she", "Pronoun", "pronouns"),
    ("qheswa", "valley", "Noun", "natural_world"),
    ("domingo", "Sunday (loan, structural example only)", "Noun", "time"),
    ("allqu", "dog", "Noun", "animals"),
    ("kawallu", "horse (loan, structural example only)", "Noun", "animals"),
    ("kaniy", "to bite", "Verb", "actions"),
    ("phuturi", "Phuturi (name)", "Proper noun", "names"),
    ("kay", "to be", "Verb", "actions"),
    ("kachkay", "to be (stative)", "Verb", "actions"),
    ("kuchuy", "to cut", "Verb", "actions"),
    ("pukllay", "to play", "Verb", "actions"),
]

# ----------------------------------------------------------------------------
# 3. Template generation
# ----------------------------------------------------------------------------
def generate_templates(noun_roots, verb_roots, gm):
    """Generate word-forms from documented morphological templates.
    NOUN: ROOT-(POSS)-(PL)-CASE(=ENCLITIC)
    VERB: ROOT-(ASP)-TENSE-PERSON(=ENCLITIC)
    Returns list of (surface, [morphs], 'template').
    """
    out = []
    cases = ["-ta", "-man", "-pi", "-manta", "-pa", "-wan", "-paq"]
    poss = [None, "-y", "-yki", "-n_poss", "-nchis", "-yku", "-nku"]
    evid = [None, "=mi", "=si", "=cha"]
    topic = [None, "-qa", "-taq", "=lla", "=pas"]
    tenses = ["-rqa", "-sqa", "-shaq", "-nqa", "-chka"]
    persons = ["-ni", "-nki", "-n_agr", "-nchis_agr", "-yku_agr", "-nku_agr"]

    # Noun forms: denser cross-product for affix co-occurrence statistics.
    # Each root gets multiple case/possessive/evidential combinations so that
    # AFFIX-AFFIX pairs (the diagnostic shapes) clear the min-count filter.
    for i, r in enumerate(noun_roots):
        for j in range(4):
            c = cases[(i + j * 2) % len(cases)]
            p = poss[(i + j) % len(poss)] if j % 2 == 0 else None
            e = evid[(i + j) % len(evid)]
            t = topic[(i + j * 3) % len(topic)] if j % 3 == 0 else None
            morphs = [r]
            if p: morphs.append(p)
            if j == 1: morphs.append("-kuna")
            morphs.append(c)
            if t: morphs.append(t)
            if e: morphs.append(e)
            out.append((r + "".join(morphs[1:]), morphs, "template"))

    # Verb forms: denser
    for i, r in enumerate(verb_roots):
        for j in range(3):
            tn = tenses[(i + j) % len(tenses)]
            ps = persons[(i + j * 2) % len(persons)]
            e = evid[(i + j) % len(evid)]
            morphs = [r, tn, ps] + ([e] if e else [])
            out.append((r + "".join(morphs[1:]), morphs, "template"))
        # SS/DS chained form
        sr = "-spa" if i % 2 == 0 else "-qti"
        morphs2 = [r, sr]
        out.append((r + sr, morphs2, "template"))
        # negated form (subset)
        if i % 2 == 0:
            ps = persons[i % len(persons)]
            morphs3 = ["mana", r, ps, "-chu"]
            out.append(("mana " + r + ps + "-chu", morphs3, "template"))

    # Nominalized forms
    for i, r in enumerate(verb_roots[:20]):
        nom = ["-na", "-sqa", "-y", "-q"][i % 4]
        morphs = [r, nom]
        if i % 2 == 0:
            morphs += ["-y", "-ta"]  # possessed + accusative, e.g. rinayta
        out.append((r + "".join(morphs[1:]), morphs, "template"))

    return out

# ----------------------------------------------------------------------------
# 4. Build
# ----------------------------------------------------------------------------
def main():
    os.makedirs(OUT, exist_ok=True)

    # --- morpheme table ---
    # (id, mtype, morpheme, gloss, source, domain, admin, oldest_form, form_src)
    # Researcher oldest-variant rule: morpheme label = oldest attested FORM
    # (1560 Santo Tomas > 1608 Holguin > modern). Where only modern is
    # available, oldest_form = morpheme, flagged lower confidence.
    morphemes = []  # (id, mtype, morpheme, gloss, source, domain, admin, oldest_form, form_src)
    name_to_id = {}
    admin_ids = set()
    qm = 1
    for mtype, morph, gloss, source, domain in GRAMMATICAL:
        morphemes.append((qm, mtype, morph, gloss, source, domain, 0, morph,
                          "grammatical (form stable)"))
        name_to_id[morph] = qm
        qm += 1
    # Military roots (oldest forms as labels, admin=1, domain=military)
    for oldest, modern, gloss, pos, src in MILITARY:
        form_note = src + ("; modern: " + modern if oldest != modern else "")
        morphemes.append((qm, "root", oldest, gloss, src, "military", 1,
                          oldest, form_note))
        name_to_id[oldest] = qm
        admin_ids.add(qm)
        qm += 1
    for root, gloss, pos, domain in LEXICAL:
        is_admin = 1 if domain in ('administration', 'numbers', 'agriculture',
                                   'animals', 'social_organization', 'colors',
                                   'materials') else 0
        if root in name_to_id:
            # upgrade existing to admin if applicable
            for i, m in enumerate(morphemes):
                if m[2] == root and is_admin:
                    morphemes[i] = (m[0], m[1], m[2], m[3], m[4], m[5], 1, m[7], m[8])
                    admin_ids.add(m[0])
            continue
        morphemes.append((qm, "root", root, gloss, "roots.csv", domain, is_admin,
                          root, "modern (lower confidence)"))
        name_to_id[root] = qm
        if is_admin:
            admin_ids.add(qm)
        qm += 1
    # administrative roots from CSV (skip ones already added)
    for root, gloss, pos, domain in ADMIN_ROOTS:
        if root in name_to_id:
            # upgrade existing entry to admin
            for i, m in enumerate(morphemes):
                if m[2] == root:
                    morphemes[i] = (m[0], m[1], m[2], m[3], m[4], m[5], 1, m[7], m[8])
                    admin_ids.add(m[0])
            continue
        morphemes.append((qm, "root", root, gloss, "roots.csv/admin", domain, 1,
                          root, "modern (lower confidence)"))
        name_to_id[root] = qm
        admin_ids.add(qm)
        qm += 1
    for root, gloss, pos, domain in EXTRA_ROOTS:
        if root not in name_to_id:
            morphemes.append((qm, "root" if pos != "suffix" else "suffix",
                              root, gloss, "attested-context", domain, 0,
                              root, "modern (lower confidence)"))
            name_to_id[root] = qm
            qm += 1

    with open(os.path.join(OUT, "quechua_morphemes.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "mtype", "morpheme", "gloss", "source", "domain", "admin",
                    "oldest_form", "form_src"])
        w.writerows(morphemes)
    print(f"morphemes: {len(morphemes)} ({len(admin_ids)} administrative)")

    # --- phrases ---
    # Administrative roots get 3x template weight (researcher constraint:
    # khipu encode state vocabulary; administrative register is the target).
    noun_roots = [r for r, g, p, d in LEXICAL if p in ("Noun", "Proper noun", "Numeral", "Adjective", "Pronoun")]
    verb_roots = [r for r, g, p, d in LEXICAL if p == "Verb"]
    admin_noun = [r for r, g, p, d in ADMIN_ROOTS if p in ("Noun", "Numeral", "Adjective")]
    admin_verb = [r for r, g, p, d in ADMIN_ROOTS if p == "Verb"]
    # military roots (oldest forms as labels)
    mil_noun = [o for o, m, g, p, s in MILITARY if p == "Noun"]
    mil_verb = [o for o, m, g, p, s in MILITARY if p == "Verb"]
    # merge: admin/military roots not already present get added; all weighted 3x
    for r in admin_noun + mil_noun:
        if r not in noun_roots:
            noun_roots.append(r)
    for r in admin_verb + mil_verb:
        if r not in verb_roots:
            verb_roots.append(r)
    admin_set = set([r for r, _, _, _ in ADMIN_ROOTS]) | set(mil_noun) | set(mil_verb)
    noun_roots_w = noun_roots + [r for r in noun_roots if r in admin_set] * 2
    verb_roots_w = verb_roots + [r for r in verb_roots if r in admin_set] * 2
    print(f"template roots: {len(noun_roots_w)} noun ({len(admin_set & set(noun_roots_w))} admin/mil), "
          f"{len(verb_roots_w)} verb")
    phrases = []
    for surface, morphs, src in ATTESTED:
        ids = [name_to_id[m] for m in morphs if m in name_to_id]
        missing = [m for m in morphs if m not in name_to_id]
        if missing:
            print("WARN missing morpheme:", missing, "in", surface)
        phrases.append((surface, ids, [m for m in morphs if m in name_to_id], "attested"))
    for surface, morphs, origin in generate_templates(noun_roots_w, verb_roots_w, None):
        ids = [name_to_id[m] for m in morphs]
        phrases.append((surface, ids, morphs, origin))

    with open(os.path.join(OUT, "quechua_phrases.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["source_id", "phrase_ord", "feature_ids", "feature_names", "origin"])
        for i, (surface, ids, morphs, origin) in enumerate(phrases):
            w.writerow([surface, i, ";".join(map(str, ids)), ";".join(morphs), origin])
    print(f"phrases: {len(phrases)} "
          f"({sum(1 for p in phrases if p[3]=='attested')} attested)")

    # --- frequency tables over morpheme occurrences ---
    # N = total morpheme tokens; fc = per-morpheme counts
    all_ids = [i for _, ids, _, _ in phrases for i in ids]
    N = len(all_ids)
    fc = Counter(all_ids)

    def pmi(c_xy, c_x, c_y, n):
        return math.log2((c_xy / n) / ((c_x / n) * (c_y / n)))

    id_to_name = {m[0]: m[2] for m in morphemes}

    # within-word PMI (unordered pairs in same word)
    pair_c = Counter()
    for _, ids, _, _ in phrases:
        for a, b in itertools.combinations(sorted(set(ids)), 2):
            pair_c[(a, b)] += 1
    rows = []
    for (a, b), cxy in pair_c.items():
        if cxy < 3:
            continue
        v = pmi(cxy, fc[a], fc[b], N)
        rows.append((v, cxy, id_to_name[a], a, id_to_name[b], b, fc[a], fc[b]))
    rows.sort(reverse=True)
    with open(os.path.join(OUT, "within_word_pmi.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["pmi", "cooccur", "feat_a", "id_a", "feat_b", "id_b",
                    "count_a", "count_b"])
        w.writerows(rows[:200])
    print("within-word pairs:", len(rows))

    # sequential bigrams (ordered, adjacent morphemes within word)
    bi_c = Counter()
    for _, ids, _, _ in phrases:
        for a, b in zip(ids, ids[1:]):
            bi_c[(a, b)] += 1
    tot_bi = sum(bi_c.values())
    rows = []
    for (a, b), cxy in bi_c.items():
        if cxy < 3:
            continue
        v = pmi(cxy, fc[a], fc[b], tot_bi)
        rows.append((cxy, v, id_to_name[a], a, id_to_name[b], b))
    rows.sort(reverse=True)
    with open(os.path.join(OUT, "quechua_sequential_bigrams.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["count", "pmi", "feat_from", "id_from", "feat_to", "id_to"])
        w.writerows(rows[:200])
    print("sequential bigrams:", len(rows))

    # hierarchical: head -> dependent. For Quechua words: ROOT -> each affix.
    h_c = Counter()
    for _, ids, morphs, _ in phrases:
        # head = first root in the word
        head = None
        for i, m in zip(ids, morphs):
            # root = mtype root (look up)
            pass
        # simpler: head = first morpheme that is a lexical root
    # rebuild with mtype lookup
    id_to_mtype = {m[0]: m[1] for m in morphemes}
    for _, ids, morphs, _ in phrases:
        head = next((i for i in ids if id_to_mtype[i] == "root"), None)
        if head is None:
            continue
        for i in ids:
            if i != head:
                h_c[(head, i)] += 1
    tot_h = sum(h_c.values())
    rows = []
    for (a, b), cxy in h_c.items():
        if cxy < 3:
            continue
        v = pmi(cxy, fc[a], fc[b], tot_h)
        rows.append((cxy, v, id_to_name[a], a, id_to_name[b], b))
    rows.sort(reverse=True)
    with open(os.path.join(OUT, "quechua_hierarchical_pairs.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["count", "pmi", "head_feat", "head_id", "dep_feat", "dep_id"])
        w.writerows(rows[:200])
    print("hierarchical pairs:", len(rows))

    # --- sanity report ---
    # promiscuity: distinct partners in within-word pairs
    partners = defaultdict(set)
    for (a, b), c in pair_c.items():
        partners[a].add(b); partners[b].add(a)
    prom = sorted(((id_to_name[i], i, len(p), fc[i]) for i, p in partners.items()),
                  key=lambda r: -r[2])
    # complementary: never co-occur, each >=5 words
    in_word = defaultdict(set)
    for wi, (_, ids, _, _) in enumerate(phrases):
        for i in set(ids):
            in_word[i].add(wi)
    comp = []
    ids_list = list(fc.keys())
    for x in range(len(ids_list)):
        for y in range(x + 1, len(ids_list)):
            a, b = ids_list[x], ids_list[y]
            if fc[a] >= 5 and fc[b] >= 5 and not (in_word[a] & in_word[b]):
                comp.append((id_to_name[a], id_to_name[b], fc[a], fc[b]))
    comp.sort(key=lambda r: -(r[2] + r[3]))

    with open(os.path.join(OUT, "quechua_sanity_report.md"), "w") as f:
        f.write("# Quechua Morpheme Database — Sanity Report\n\n")
        f.write(f"Word-forms: {len(phrases)} "
                f"({sum(1 for p in phrases if p[3]=='attested')} attested, "
                f"rest rule-generated templates)\n\n")
        f.write(f"Morpheme vocabulary size: {len(morphemes)}\n\n")
        f.write("**IMPORTANT CAVEAT:** the template-generated majority means "
                "co-occurrence here reflects the GRAMMAR DESCRIPTION's structure, "
                "not natural-text frequencies. Isomorphism results test whether "
                "khipu patterns match Quechua's grammatical TYPOLOGY.\n\n")
        f.write("## Most promiscuous morphemes\n\n")
        f.write("| morpheme | id | distinct partners | word count |\n|---|---|---|---|\n")
        for name, i, np, c in prom[:20]:
            f.write(f"| {name} | {i} | {np} | {c} |\n")
        f.write("\n## Most restricted morphemes (>=3 words)\n\n")
        f.write("| morpheme | id | distinct partners | word count |\n|---|---|---|---|\n")
        for name, i, np, c in [r for r in prom if r[3] >= 3][-20:]:
            f.write(f"| {name} | {i} | {np} | {c} |\n")
        f.write("\n## Complementary distribution (>=5 words each, never co-occur)\n\n")
        f.write("| morpheme a | morpheme b | count a | count b |\n|---|---|---|---|\n")
        for a, b, ca, cb in comp[:30]:
            f.write(f"| {a} | {b} | {ca} | {cb} |\n")
    print("done.")

if __name__ == "__main__":
    main()
