"""Extract morpheme n-grams from Quechua phrases."""
import csv
from collections import Counter, defaultdict
import os

OUTDIR = '/home/hatch/workspace/quipu-analysis/byte-patterns'
PHRASES = '/home/hatch/workspace/quipu-analysis/isomorphism/quechua_phrases.csv'

phrases = []  # list of (source_id, [morpheme_ids], [morpheme_names], origin)
with open(PHRASES) as f:
    r = csv.DictReader(f)
    for row in r:
        ids = row['feature_ids'].split(';')
        names = row['feature_names'].split(';')
        phrases.append((row['source_id'], ids, names, row['origin']))

print(f'Loaded {len(phrases)} phrases')

# Bigrams and trigrams of morpheme IDs
bigram_counts = Counter()
trigram_counts = Counter()
# Track which phrases (documents) each n-gram appears in
bigram_docs = defaultdict(set)
trigram_docs = defaultdict(set)
# Positional: index of n-gram within phrase (normalized 0-1)
bigram_pos = defaultdict(list)
trigram_pos = defaultdict(list)

for pid, (sid, ids, names, origin) in enumerate(phrases):
    n = len(ids)
    for i in range(n - 1):
        bg = (ids[i], ids[i+1])
        bigram_counts[bg] += 1
        bigram_docs[bg].add(pid)
        bigram_pos[bg].append(i / max(n - 1, 1))
    for i in range(n - 2):
        tg = (ids[i], ids[i+1], ids[i+2])
        trigram_counts[tg] += 1
        trigram_docs[tg].add(pid)
        trigram_pos[tg].append(i / max(n - 2, 1))

# Write bigrams
with open(f'{OUTDIR}/quechua_morpheme_ngrams.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['ngram_ids', 'n_morphemes', 'count', 'n_phrases', 'mean_norm_pos'])
    for bg, cnt in bigram_counts.most_common():
        ndoc = len(bigram_docs[bg])
        mpos = sum(bigram_pos[bg]) / len(bigram_pos[bg])
        w.writerow([';'.join(bg), 2, cnt, ndoc, f'{mpos:.3f}'])
    for tg, cnt in trigram_counts.most_common():
        ndoc = len(trigram_docs[tg])
        mpos = sum(trigram_pos[tg]) / len(trigram_pos[tg])
        w.writerow([';'.join(tg), 3, cnt, ndoc, f'{mpos:.3f}'])

print(f'Bigrams: {len(bigram_counts)}, Trigrams: {len(trigram_counts)}')
print('Top 10 bigrams:')
for bg, cnt in bigram_counts.most_common(10):
    print(f'  {bg}: {cnt}')
print('Top 10 trigrams:')
for tg, cnt in trigram_counts.most_common(10):
    print(f'  {tg}: {cnt}')

# Save raw counters for geometry comparison
import pickle
with open(f'{OUTDIR}/quechua_ngram_data.pkl', 'wb') as f:
    pickle.dump({
        'bigram_counts': bigram_counts,
        'trigram_counts': trigram_counts,
        'bigram_docs': dict(bigram_docs),
        'trigram_docs': dict(trigram_docs),
        'bigram_pos': dict(bigram_pos),
        'trigram_pos': dict(trigram_pos),
        'n_phrases': len(phrases),
    }, f)
print('Saved.')
