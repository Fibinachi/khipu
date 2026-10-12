"""Compare repetition geometries: khipu byte n-grams vs Quechua morpheme n-grams.

For each side, compute:
1. Zipf distribution (rank vs frequency) — fit power-law slope
2. Positional distribution (where do top n-grams occur? beginning/middle/end?)
3. Cross-document spread (how many documents share each n-gram?)
4. Type-token ratio and vocabulary richness

Then compare: do the geometries rhyme?
"""
import pickle
import math
from collections import Counter

OUTDIR = '/home/hatch/workspace/quipu-analysis/byte-patterns'

with open(f'{OUTDIR}/khipu_ngram_data.pkl', 'rb') as f:
    kd = pickle.load(f)
with open(f'{OUTDIR}/quechua_ngram_data.pkl', 'rb') as f:
    qd = pickle.load(f)

def zipf_slope(counts):
    """Fit log(rank) vs log(freq) slope via least squares on top 100."""
    freqs = sorted(counts.values(), reverse=True)[:100]
    n = len(freqs)
    if n < 10:
        return None
    xs = [math.log(i+1) for i in range(n)]
    ys = [math.log(f) for f in freqs]
    mx, my = sum(xs)/n, sum(ys)/n
    num = sum((x-mx)*(y-my) for x, y in zip(xs, ys))
    den = sum((x-mx)**2 for x in xs)
    return num/den if den else None

def positional_profile(pos_dict, counts, top_n=50):
    """Mean normalized position of top-N n-grams. <0.33=front, >0.67=back."""
    top = [ng for ng, _ in counts.most_common(top_n)]
    posns = []
    for ng in top:
        if ng in pos_dict:
            posns.extend(pos_dict[ng])
    if not posns:
        return None
    # Bin into thirds
    front = sum(1 for p in posns if p < 0.33) / len(posns)
    mid = sum(1 for p in posns if 0.33 <= p < 0.67) / len(posns)
    back = sum(1 for p in posns if p >= 0.67) / len(posns)
    return {'front': front, 'mid': mid, 'back': back, 'n': len(posns)}

def sharing_profile(docs_dict, counts, n_docs_total, top_n=100):
    """How widely shared are top n-grams? Mean docs per n-gram."""
    top = [ng for ng, _ in counts.most_common(top_n)]
    shares = []
    for ng in top:
        if ng in docs_dict:
            shares.append(len(docs_dict[ng]) / n_docs_total)
    if not shares:
        return None
    return {
        'mean_share': sum(shares)/len(shares),
        'max_share': max(shares),
        'n_single_doc': sum(1 for s in shares if s < 2/n_docs_total),
    }

report = []
report.append("# Repetition Geometry Comparison")
report.append("")
report.append("Comparing khipu byte n-grams vs Quechua morpheme n-grams.")
report.append("")

# --- Khipu side ---
report.append("## Khipu byte n-grams")
for size in [4, 8, 12]:
    c = kd['counts'][size]
    total_tokens = sum(c.values())
    report.append(f"### {size}-byte ({size//4} cords)")
    report.append(f"- Types: {len(c)}, Tokens: {total_tokens}")
    report.append(f"- Khipu: {kd['n_khipu']}")
    slope = zipf_slope(c)
    report.append(f"- Zipf slope: {slope:.3f}" if slope else "- Zipf slope: N/A")
    pp = positional_profile(kd['positions'][size], c)
    if pp:
        report.append(f"- Position (top 50): front={pp['front']:.2f} mid={pp['mid']:.2f} back={pp['back']:.2f}")
    sp = sharing_profile(kd['docs'][size], c, kd['n_khipu'])
    if sp:
        report.append(f"- Sharing (top 100): mean={sp['mean_share']:.3f} max={sp['max_share']:.3f} single-doc={sp['n_single_doc']}")
    # Top 5
    report.append("- Top 5:")
    for ng, cnt in c.most_common(5):
        ndoc = len(kd['docs'][size].get(ng, set()))
        report.append(f"  - `{ng}`: {cnt}x in {ndoc} khipu")
    report.append("")

# --- Quechua side ---
report.append("## Quechua morpheme n-grams")
report.append(f"- Phrases: {qd['n_phrases']}")
report.append("- NOTE: 98% rule-generated templates; bigram frequencies are artificially uniform.")
report.append("")
for name, c, pos_d, doc_d in [
    ('bigrams', qd['bigram_counts'], qd['bigram_pos'], qd['bigram_docs']),
    ('trigrams', qd['trigram_counts'], qd['trigram_pos'], qd['trigram_docs']),
]:
    total_tokens = sum(c.values())
    report.append(f"### {name}")
    report.append(f"- Types: {len(c)}, Tokens: {total_tokens}")
    slope = zipf_slope(c)
    report.append(f"- Zipf slope: {slope:.3f}" if slope else "- Zipf slope: N/A")
    pp = positional_profile(pos_d, c)
    if pp:
        report.append(f"- Position (top 50): front={pp['front']:.2f} mid={pp['mid']:.2f} back={pp['back']:.2f}")
    sp = sharing_profile(doc_d, c, qd['n_phrases'])
    if sp:
        report.append(f"- Sharing (top 100): mean={sp['mean_share']:.3f} max={sp['max_share']:.3f}")
    report.append("")

# --- Comparison ---
report.append("## Geometry comparison")
report.append("")
report.append("Do the repetition structures rhyme?")
report.append("")

k4_slope = zipf_slope(kd['counts'][4])
k8_slope = zipf_slope(kd['counts'][8])
qb_slope = zipf_slope(qd['bigram_counts'])
qt_slope = zipf_slope(qd['trigram_counts'])

report.append(f"- Khipu 4-byte Zipf: {k4_slope:.3f} | Quechua bigram Zipf: {qb_slope:.3f}")
report.append(f"- Khipu 8-byte Zipf: {k8_slope:.3f} | Quechua trigram Zipf: {qt_slope:.3f}")
report.append("")
report.append("Natural language typically shows Zipf slope ≈ -1.0.")
report.append("Template-generated text shows flatter slopes (uniform frequencies).")
report.append("")

with open(f'{OUTDIR}/geometry_comparison.md', 'w') as f:
    f.write('\n'.join(report))
print('\n'.join(report))
