"""Extract byte n-grams from khipu hex corpus.

Each cord = 4 bytes. We extract:
- 4-byte n-grams (single cords)
- 8-byte n-grams (cord pairs)
- 12-byte n-grams (cord triples)

Header (8 bytes) is skipped for n-gram extraction — we analyze the body only.
But we also record the doc-type byte from each header for stratification.
"""
import csv
import os
import pickle
from collections import Counter, defaultdict

HEXDIR = '/home/hatch/workspace/quipu-analysis/byte-patterns/hex-corpus'
OUTDIR = '/home/hatch/workspace/quipu-analysis/byte-patterns'

# n-gram sizes in bytes (must be multiples of 4 for cord alignment)
SIZES = [4, 8, 12]

counts = {s: Counter() for s in SIZES}
docs = {s: defaultdict(set) for s in SIZES}       # ngram -> set of khipu ids
positions = {s: defaultdict(list) for s in SIZES}  # ngram -> list of norm positions
doc_types = {}  # khipu_id -> doc type byte

files = [f for f in os.listdir(HEXDIR) if f.endswith('.hex') and not f.startswith('_')]
print(f'Processing {len(files)} hex files...')

for fi, fname in enumerate(files):
    khipu_id = fname.replace('.hex', '')
    with open(os.path.join(HEXDIR, fname)) as f:
        hexstr = f.read().strip()
    data = bytes.fromhex(hexstr)
    if len(data) < 8:
        continue
    # Header: bytes 0-3 magic, 4 version, 5 doc_type, 6-7 cord count
    doc_types[khipu_id] = data[5]
    body = data[8:]
    n_cords = len(body) // 4
    if n_cords == 0:
        continue
    for size in SIZES:
        n_units = size // 4
        for i in range(n_cords - n_units + 1):
            ng = body[i*4:(i+n_units)*4]
            key = ng.hex()
            counts[size][key] += 1
            docs[size][key].add(khipu_id)
            positions[size][key].append(i / max(n_cords - n_units, 1))

# Write CSV
with open(f'{OUTDIR}/khipu_byte_ngrams.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['ngram_hex', 'n_bytes', 'n_cords', 'count', 'n_khipu', 'mean_norm_pos'])
    for size in SIZES:
        for ng, cnt in counts[size].most_common():
            ndoc = len(docs[size][ng])
            mpos = sum(positions[size][ng]) / len(positions[size][ng])
            w.writerow([ng, size, size // 4, cnt, ndoc, f'{mpos:.3f}'])

print('Top 4-byte n-grams:')
for ng, cnt in counts[4].most_common(10):
    print(f'  {ng}: {cnt} (in {len(docs[4][ng])} khipu)')
print('Top 8-byte n-grams:')
for ng, cnt in counts[8].most_common(10):
    print(f'  {ng}: {cnt} (in {len(docs[8][ng])} khipu)')

with open(f'{OUTDIR}/khipu_ngram_data.pkl', 'wb') as f:
    pickle.dump({
        'counts': counts, 'docs': dict(docs), 'positions': dict(positions),
        'doc_types': doc_types, 'n_khipu': len(files),
    }, f)
print('Saved.')
