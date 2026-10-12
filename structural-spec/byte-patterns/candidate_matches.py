"""Find direct pattern-level alignments between khipu bytes and Quechua morphemes.

Looks for structural rhymes:
1. Function-word analogues: high-frequency, widely-shared, positionally-fixed patterns
   on each side. Do khipu have byte patterns that behave like Quechua evidentials/case?
2. The most frequent khipu 8-byte pattern vs most frequent Quechua trigram:
   positional and distributional comparison.
3. Decode top khipu n-grams back to features and describe what they "say."
"""
import pickle
import csv

OUTDIR = '/home/hatch/workspace/quipu-analysis/byte-patterns'

with open(f'{OUTDIR}/khipu_ngram_data.pkl', 'rb') as f:
    kd = pickle.load(f)
with open(f'{OUTDIR}/quechua_ngram_data.pkl', 'rb') as f:
    qd = pickle.load(f)

# Load morpheme ID -> name mapping
morphpheme_names = {}
with open('/home/hatch/workspace/quipu-analysis/isomorphism/quechua_morphemes.csv') as f:
    r = csv.DictReader(f)
    for row in r:
        morphpheme_names[row['id']] = (row['morpheme'], row['gloss'], row['mtype'])

def decode_khipu_ngram(hexstr):
    """Decode a byte n-gram back to cord features."""
    data = bytes.fromhex(hexstr)
    cords = []
    for i in range(0, len(data), 4):
        b0, b1 = data[i], data[i+1]
        val = int.from_bytes(data[i+2:i+4], 'big')
        color_id = (b0 >> 2) & 0x3F
        knot = ((b0 & 0x03) << 1) | ((b1 >> 7) & 0x01)
        direction = (b1 >> 5) & 0x03
        level = (b1 >> 2) & 0x07
        knot_names = {0:'S',1:'L',2:'E',3:'EE',4:'SP',5:'TF',6:'LL',7:'BL'}
        dir_names = {0:'Z',1:'S',2:'U'}
        cords.append(f"col{color_id}:{knot_names.get(knot,'?')}:{dir_names.get(direction,'?')}:L{level}={val}")
    return ' | '.join(cords)

def function_word_score(counts, docs, positions, n_docs_total, top_n=100):
    """Score n-grams by function-word-likeness: high freq + wide sharing + fixed position."""
    # Positional fixity: low variance in normalized position
    scores = []
    for ng, cnt in counts.most_common(top_n):
        ndoc = len(docs.get(ng, set()))
        share = ndoc / n_docs_total
        posns = positions.get(ng, [])
        if len(posns) < 3:
            continue
        mean_p = sum(posns) / len(posns)
        var_p = sum((p - mean_p) ** 2 for p in posns) / len(posns)
        # Function words: high share, low positional variance
        score = share * (1 / (1 + var_p * 10))
        scores.append((ng, cnt, ndoc, mean_p, var_p, score))
    scores.sort(key=lambda x: x[5], reverse=True)
    return scores

report = []
report.append("# Candidate Pattern Matches")
report.append("")
report.append("Structural rhymes between khipu byte patterns and Quechua morpheme patterns.")
report.append("")

# --- Khipu function-word analogues ---
report.append("## Khipu byte patterns behaving like function words")
report.append("(High frequency + wide sharing + fixed position)")
report.append("")
for size, label in [(4, 'single cords'), (8, 'cord pairs')]:
    fw = function_word_score(kd['counts'][size], kd['docs'][size],
                             kd['positions'][size], kd['n_khipu'])
    report.append(f"### {label} — top 10 function-word-like")
    for ng, cnt, ndoc, mp, vp, score in fw[:10]:
        decoded = decode_khipu_ngram(ng)
        report.append(f"- `{ng}` ({cnt}x, {ndoc} khipu, pos={mp:.2f}): {decoded}")
    report.append("")

# --- Quechua function morphemes ---
report.append("## Quechua morpheme patterns (for comparison)")
report.append("Top bigrams by raw frequency:")
for bg, cnt in qd['bigram_counts'].most_common(10):
    names = [morphpheme_names.get(i, ('?', '?', '?')) for i in bg]
    gloss = '+'.join(n[0] for n in names)
    report.append(f"- `{';'.join(bg)}` ({gloss}): {cnt}x in {len(qd['bigram_docs'][bg])} phrases")
report.append("")

# --- Direct comparison: most frequent patterns ---
report.append("## Head-to-head: most frequent patterns")
k_top8 = kd['counts'][8].most_common(1)[0]
q_top3 = qd['trigram_counts'].most_common(1)[0]
report.append(f"Khipu top 8-byte: `{k_top8[0]}` ({k_top8[1]}x)")
report.append(f"  Decoded: {decode_khipu_ngram(k_top8[0])}")
q_names = [morphpheme_names.get(i, ('?', '?', '?'))[0] for i in q_top3[0]]
report.append(f"Quechua top trigram: `{';'.join(q_top3[0])}` ({' + '.join(q_names)}): {q_top3[1]}x")
report.append("")
report.append("Note: Quechua side is 98% template-generated; top patterns reflect")
report.append("template structure, not natural usage. Treat as baseline, not evidence.")
report.append("")

with open(f'{OUTDIR}/candidate_matches.md', 'w') as f:
    f.write('\n'.join(report))
print('\n'.join(report))
