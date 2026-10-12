import re, json, sys

with open('holguin_libro1_raw.json') as f:
    entries = json.load(f)

def normalize_colonial(word):
    """Light normalization of Holguín's orthography toward modern Quechua."""
    w = word.strip()
    # Remove OCR artifacts but keep the word
    w = re.sub(r'[^\wñáéíóúüç\'\- ]', '', w, flags=re.UNICODE)
    w = w.strip()
    return w

def split_headword_gloss(entry):
    """
    Entry format: Quechua headword(s) + Spanish gloss.
    Headword typically ends at first period followed by space+lowercase,
    or is 1-3 tokens at start.
    """
    # Try: headword ends at first ". " where what follows looks like Spanish
    # Quechua headwords often contain q, hua, cc, etc.
    # Strategy: take up to first period as headword candidate, rest as gloss
    m = re.match(r'^(.{2,60}?)\.\s+([A-ZÁÉÍÓÚa-záéíóú].*)$', entry, re.DOTALL)
    if m:
        hw, gloss = m.group(1).strip(), m.group(2).strip()
        # Headword shouldn't be too long or contain too many words
        hw_words = hw.split()
        if len(hw_words) <= 4 and len(hw) <= 40:
            return hw, gloss
    # Fallback: first 1-2 tokens as headword
    tokens = entry.split()
    if len(tokens) >= 2:
        return ' '.join(tokens[:2]), ' '.join(tokens[2:])
    return entry, ''

parsed = []
for e in entries:
    hw, gloss = split_headword_gloss(e)
    hw = normalize_colonial(hw)
    if len(hw) < 2 or len(gloss) < 3:
        continue
    parsed.append({'quechua_1608': hw, 'gloss_es': gloss[:300], 'raw': e[:200]})

print(f"Parsed: {len(parsed)}", file=sys.stderr)
for p in parsed[10:15]:
    print(f"HW: {p['quechua_1608']} | GLOSS: {p['gloss_es'][:80]}", file=sys.stderr)

with open('holguin_roots_raw.json','w') as f:
    json.dump(parsed, f, ensure_ascii=False)
