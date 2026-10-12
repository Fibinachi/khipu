"""Step 3: byte n-grams + Zipf on residuals only; compare to full-corpus slope."""
import pickle, sys, math
from collections import Counter
import numpy as np

sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from khipu_hex import serialize_khipu

OUT = '/home/hatch/workspace/quipu-analysis/residuals/'

def zipf_slope(counts):
    """Fit log(rank) vs log(freq). Returns slope."""
    freqs = sorted(counts.values(), reverse=True)
    # use ranks 10..1000 to avoid head/tail noise
    xs, ys = [], []
    for i, f in enumerate(freqs):
        if 10 <= i < min(1000, len(freqs)) and f > 0:
            xs.append(math.log(i+1)); ys.append(math.log(f))
    if len(xs) < 10:
        return None
    X = np.array(xs); Y = np.array(ys)
    slope = np.polyfit(X, Y, 1)[0]
    return slope

def main():
    with open(OUT + 'residual_feats.pkl', 'rb') as fh:
        res = pickle.load(fh)
    kids = [r['khipu_id'] for r in res]
    print(f'serializing {len(kids)} khipu...', flush=True)

    ngrams = {4: Counter(), 8: Counter(), 12: Counter()}
    n_cords_total = 0
    ok = 0
    for i, kid in enumerate(kids):
        try:
            data = serialize_khipu(int(kid))
            body = data[8:]  # strip header
            n_cords_total += len(body) // 4
            ok += 1
            for nbytes in (4, 8, 12):
                step = 4
                for j in range(0, len(body) - nbytes + 1, step):
                    ngrams[nbytes][body[j:j+nbytes].hex()] += 1
        except Exception as e:
            print(f'ERR {kid}: {e}', file=sys.stderr)
        if (i+1) % 30 == 0:
            print(f'  {i+1}/{len(kids)}', flush=True)
    print(f'serialized {ok}, {n_cords_total} cord-tokens', flush=True)

    lines = ['# Residual Byte N-grams', '',
             f'Serialized {ok} khipu, {n_cords_total} cord-tokens (headers stripped).', '']
    for nbytes in (4, 8, 12):
        c = ngrams[nbytes]
        slope = zipf_slope(c)
        lines.append(f'## {nbytes}-byte n-grams: {len(c)} distinct, Zipf slope {slope:.3f}' if slope else f'## {nbytes}-byte: slope n/a')
        lines.append('')
        lines.append('| Rank | Hex | Count |')
        lines.append('|---|---|---|')
        for i, (h, n) in enumerate(c.most_common(20)):
            lines.append(f'| {i+1} | `{h}` | {n} |')
        lines.append('')
    lines.append('Full-corpus reference slopes: 4-byte -0.930, 8-byte -0.935, 12-byte -0.899.')
    lines.append('Natural language range: approx -1.0.')

    with open(OUT + 'residual_ngrams.md', 'w') as f:
        f.write('\n'.join(lines) + '\n')
    # save ngrams for reuse
    with open(OUT + 'residual_ngrams.pkl', 'wb') as f:
        pickle.dump({k: dict(v) for k, v in ngrams.items()}, f)
    print('wrote residual_ngrams.md', flush=True)

if __name__ == '__main__':
    main()
