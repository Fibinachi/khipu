"""Synthetic khipu generator from induced primitives + composition rules.

Primitives:
  COLORS: 10 families x 5 intensities (weighted by corpus frequency)
  KNOTS: S (decade), L(n) ones 2-9, E ones=1, TF unary
  POSITION: sequence (ordinal), hierarchy (level), cluster (decimal place)

Composition rules generate four document types from the SAME primitives:
  tabular, journal, checklist, code
"""
import random
from collections import Counter

# --- PRIMITIVES ---

# Color families with corpus weights (from family distribution)
FAMILIES = {
    'B': 0.62,  # brown
    'A': 0.28,  # white
    'G': 0.037, # green
    'H': 0.026, # blue
    'Z': 0.016, # black
    'M': 0.016, # gray
    'L': 0.010, # olive
    'R': 0.006, # red
    'N': 0.004, # orange
    'Y': 0.001, # yellow
}

# Representative color per family (most common code)
FAMILY_COLOR = {
    'B': 'MB', 'A': 'W', 'G': 'GG', 'H': 'BG', 'Z': 'KB',
    'M': 'MG', 'L': 'G0', 'R': 'SR', 'N': 'SB', 'Y': 'SY',
}

def pick_family(rng):
    r = rng.random()
    cum = 0
    for fam, w in FAMILIES.items():
        cum += w
        if r < cum:
            return fam
    return 'B'

def pick_color(rng, family=None):
    fam = family or pick_family(rng)
    return FAMILY_COLOR[fam], fam

# Knot primitives
def make_decimal_value(rng, max_val=9999):
    """Generate a decimal value using S/L/E primitives."""
    if max_val <= 0:
        return []
    # Choose number of digits — weight heavily toward 1-2 digits (ones-only cords common)
    ndigits = rng.choices([1, 2, 3, 4, 5], weights=[0.45, 0.30, 0.15, 0.08, 0.02])[0]
    knots = []
    for d in range(ndigits - 1, -1, -1):
        if d == 0:
            # Ones: E (=1) or L(n) (2-9), or empty (=0)
            # Weight toward non-zero to produce more knots
            v = rng.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                           weights=[0.15, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.08, 0.07])[0]
            if v == 1:
                knots.append(('E', 0))
            elif v > 1:
                knots.append(('L', v))
        else:
            # Tens+: S cluster, weighted toward non-zero
            v = rng.choices([0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
                           weights=[0.2, 0.12, 0.12, 0.12, 0.12, 0.1, 0.08, 0.06, 0.05, 0.03])[0]
            if v > 0:
                # S knots: one entry per single knot (not clustered count)
                for _ in range(v):
                    knots.append(('S', 0))
    return knots

def make_tuft_value(rng, max_tufts=4):
    """Unary tally using TF primitive."""
    n = rng.randint(0, max_tufts)
    return [('TF', 1)] * n

# --- COMPOSITION RULES ---

class SyntheticKhipu:
    def __init__(self, kid, doc_type):
        self.kid = kid
        self.doc_type = doc_type
        self.cords = []  # (ordinal, level, color, family, knots)

    def add_cord(self, ordinal, level, color, family, knots):
        self.cords.append((ordinal, level, color, family, knots))

    def stats(self):
        colors = Counter(c for _, _, c, _, _ in self.cords)
        fams = Counter(f for _, _, _, f, _ in self.cords)
        ktypes = Counter()
        for _, _, _, _, knots in self.cords:
            for t, _ in knots:
                ktypes[t] += 1
        levels = Counter(l for _, l, _, _, _ in self.cords)
        return {
            'n_cords': len(self.cords),
            'n_colors': len(colors),
            'families': dict(fams),
            'knot_types': dict(ktypes),
            'levels': dict(levels),
        }

def add_subsidiaries(kh, rng, parent_ordinal, parent_color, parent_fam, depth=2, max_depth=3):
    """Add subsidiary cords (levels 2+) to a parent. Real corpus: 25% L2, 3% L3."""
    if depth > max_depth or rng.random() > 0.35:
        return parent_ordinal
    ordinal = parent_ordinal
    n_subs = rng.randint(1, 4)
    for _ in range(n_subs):
        # Subsidiary often same color family or white
        if rng.random() < 0.5:
            color, fam = parent_color, parent_fam
        else:
            color, fam = pick_color(rng)
        kh.add_cord(ordinal, depth, color, fam, make_decimal_value(rng, 500))
        ordinal += 1
        # Recurse
        ordinal = add_subsidiaries(kh, rng, ordinal, color, fam, depth + 1, max_depth)
    return ordinal

def gen_tabular(rng, kid, n_rows=None, n_cols=None):
    """Tabular: color cycle x row repetition. Like 1000344."""
    kh = SyntheticKhipu(kid, 'tabular')
    # Long tail: occasionally very large
    if rng.random() < 0.05:
        n_rows = rng.randint(100, 400)
    else:
        n_rows = n_rows or rng.randint(5, 30)
    n_cols = n_cols or rng.randint(2, 5)
    # Pick column colors (the cycle)
    col_colors = [pick_color(rng) for _ in range(n_cols)]
    # Template constants: fixed values for some columns
    constants = {}
    for i in range(n_cols):
        if rng.random() < 0.5:
            constants[i] = rng.randint(1, 100)

    ordinal = 1
    # Header: white cords
    for _ in range(rng.randint(1, 4)):
        kh.add_cord(ordinal, 1, 'W', 'A', make_decimal_value(rng, 100))
        ordinal += 1

    for r in range(n_rows):
        for ci in range(n_cols):
            color, fam = col_colors[ci]
            if ci in constants and rng.random() < 0.8:
                # Template constant
                v = constants[ci]
                knots = []
                s = str(v)
                for d_idx, digit in enumerate(reversed(s)):
                    dv = int(digit)
                    if d_idx == 0:
                        if dv == 1: knots.append(('E', 0))
                        elif dv > 1: knots.append(('L', dv))
                    elif dv > 0:
                        for _ in range(dv):
                            knots.append(('S', 0))
            else:
                knots = make_decimal_value(rng, 2000)
            kh.add_cord(ordinal, 1, color, fam, knots)
            ordinal += 1
            # Subsidiaries
            if rng.random() < 0.2:
                ordinal = add_subsidiaries(kh, rng, ordinal, color, fam)
    return kh

def gen_journal(rng, kid, n_entries=None):
    """Journal: delimiter -> entries -> delimiter. Like 1000368."""
    kh = SyntheticKhipu(kid, 'journal')
    n_entries = n_entries or rng.randint(10, 50)
    ordinal = 1

    def add_delimiter(n=3):
        nonlocal ordinal
        for _ in range(n):
            kh.add_cord(ordinal, 1, 'W', 'A', [])
            ordinal += 1

    add_delimiter()
    for _ in range(n_entries):
        # Entry: 1-5 cords, small values
        for _ in range(rng.randint(1, 5)):
            color, fam = pick_color(rng)
            kh.add_cord(ordinal, 1, color, fam, make_decimal_value(rng, 50))
            ordinal += 1
        if rng.random() < 0.3:
            add_delimiter(rng.randint(2, 4))
    add_delimiter()
    return kh

def gen_checklist(rng, kid, n_sections=None):
    """Checklist: white-separated sections, graded marks. Like 1000522."""
    kh = SyntheticKhipu(kid, 'checklist')
    n_sections = n_sections or rng.randint(2, 4)
    ordinal = 1

    # Header: white cords with tuft-like values
    for _ in range(rng.randint(3, 7)):
        kh.add_cord(ordinal, 1, 'W', 'A', make_tuft_value(rng, 4))
        ordinal += 1

    for s in range(n_sections):
        # Section palette
        n_cats = rng.randint(3, 6)
        palette = [pick_color(rng) for _ in range(n_cats)]
        for color, fam in palette:
            for _ in range(rng.randint(3, 8)):
                kh.add_cord(ordinal, 1, color, fam, make_tuft_value(rng, 4))
                ordinal += 1
        # White separator
        for _ in range(rng.randint(1, 3)):
            kh.add_cord(ordinal, 1, 'W', 'A', [])
            ordinal += 1
    return kh

def gen_code(rng, kid, n_symbols=None):
    """Code: symbol sequence with punctuation. Like 1000331."""
    kh = SyntheticKhipu(kid, 'code')
    n_symbols = n_symbols or rng.randint(50, 200)
    ordinal = 1
    # Small vocabulary
    vocab = [pick_color(rng) for _ in range(rng.randint(5, 12))]
    punct = [('AB', 'B'), ('BG', 'H')]  # punctuation colors

    for _ in range(n_symbols):
        if rng.random() < 0.15:
            color, fam = rng.choice(punct)
        else:
            color, fam = rng.choice(vocab)
        # Codes use categorical knots, not decimal values
        knots = [('S', rng.randint(0, 3))] if rng.random() < 0.5 else []
        kh.add_cord(ordinal, 1, color, fam, knots)
        ordinal += 1
    return kh

def generate(n=100, seed=42):
    rng = random.Random(seed)
    khipus = []
    types = ['tabular', 'journal', 'checklist', 'code']
    weights = [0.40, 0.30, 0.05, 0.25]  # checklist rare (only 1000522 uses TF)
    for i in range(n):
        dt = rng.choices(types, weights=weights)[0]
        if dt == 'tabular':
            kh = gen_tabular(rng, 9000000 + i)
        elif dt == 'journal':
            kh = gen_journal(rng, 9000000 + i)
        elif dt == 'checklist':
            kh = gen_checklist(rng, 9000000 + i)
        else:
            kh = gen_code(rng, 9000000 + i)
        khipus.append(kh)
    return khipus

if __name__ == '__main__':
    khipus = generate(100)
    print(f"Generated {len(khipus)} synthetic khipu")
    for kh in khipus[:5]:
        s = kh.stats()
        print(f"  {kh.kid} ({kh.doc_type}): {s['n_cords']} cords, "
              f"{s['n_colors']} colors, knots={s['knot_types']}")
