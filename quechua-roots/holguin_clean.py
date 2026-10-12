import json, re, sys

with open('lexicon_holguin_only.json') as f:
    data = json.load(f)

cleaned = []
for d in data:
    root = d['root'].strip()
    # Strict filters
    if ' ' in root:  # single word only
        continue
    if len(root) < 4 or len(root) > 20:
        continue
    # Must be mostly alphabetic
    if len(re.sub(r'[a-záéíóúñü\']', '', root.lower())) > 2:
        continue
    # Must have Quechua vowel pattern (at least one vowel)
    if not re.search(r'[aeiouáéíóú]', root.lower()):
        continue
    # Gloss must look like Spanish definition (3+ words)
    gloss_words = d['gloss'].split()
    if len(gloss_words) < 3:
        continue
    # Skip if gloss is clearly OCR garbage (too many special chars)
    if len(re.sub(r'[a-záéíóúñ ]', '', d['gloss'].lower())) > len(d['gloss']) * 0.3:
        continue
    cleaned.append(d)

print(f"Cleaned Holguín-only: {len(cleaned)}", file=sys.stderr)
for c in cleaned[:15]:
    print(f"  {c['root']} | {c['gloss'][:60]}", file=sys.stderr)

with open('lexicon_holguin_clean.json','w') as f:
    json.dump(cleaned, f, ensure_ascii=False)
