import re, json, sys

with open('vocabulariodelal01gonz.txt', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# Libro Primero: lines 436 to 46078 (0-indexed: 435 to 46077)
start, end = 435, 46077
section = lines[start:end]

# Join into text, entries are separated by blank lines
text = ''.join(section)

# Split on blank lines (2+ newlines)
raw_entries = re.split(r'\n\s*\n', text)

entries = []
for raw in raw_entries:
    raw = raw.strip()
    if len(raw) < 10:
        continue
    # Skip headers/page artifacts
    if re.match(r'^(EL\s+)?LIBRO', raw, re.IGNORECASE):
        continue
    # Collapse internal newlines/spacing
    entry = re.sub(r'\s+', ' ', raw).strip()
    if len(entry) < 8:
        continue
    entries.append(entry)

print(f"Raw entries: {len(entries)}", file=sys.stderr)
# Show samples
for e in entries[5:15]:
    print("ENTRY:", e[:150], file=sys.stderr)

with open('holguin_libro1_raw.json','w') as f:
    json.dump(entries, f, ensure_ascii=False)
