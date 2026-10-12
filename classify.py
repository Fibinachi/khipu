"""Document classification for 593 non-funerary khipu.

Governing principle: Context dictates structure.
- Anchors: Santa (census, 1000270-1000275), Inkawasi (warehouse, 1000597-1000614)
- Extract structural + numerical features per quipu
- Classify by anchor similarity, but flag non-matching as unclassified
- Do NOT force into categories
"""

import sqlite3
import sys
from collections import Counter, defaultdict

sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from decoder import decode_cord

SANTA_IDS = {1000270, 1000271, 1000272, 1000273, 1000274, 1000275}
INKAWASI_IDS = set(range(1000597, 1000615))  # 1000597-1000614

def get_features(conn, khipu_id):
    c = conn.cursor()
    f = {'khipu_id': khipu_id}
    
    # Basic structure
    c.execute('SELECT CORD_LEVEL, COUNT(*) FROM cord WHERE KHIPU_ID = ? GROUP BY CORD_LEVEL', (khipu_id,))
    levels = dict(c.fetchall())
    f['levels'] = levels
    f['max_level'] = max(levels.keys()) if levels else 0
    f['n_cords'] = sum(levels.values())
    f['n_top'] = levels.get(1, 0)
    
    # Provenance
    c.execute('SELECT PROVENANCE, REGION, NOTES FROM khipu_main WHERE KHIPU_ID = ?', (khipu_id,))
    row = c.fetchone()
    f['provenance'] = row[0] if row else None
    f['region'] = row[1] if row else None
    
    # Decode top-level cords (cap at 300 for speed)
    c.execute('SELECT CORD_ID FROM cord WHERE KHIPU_ID = ? AND CORD_LEVEL = 1 ORDER BY CORD_ORDINAL LIMIT 300', (khipu_id,))
    cords = [r[0] for r in c.fetchall()]
    
    vals = []
    high_conf = 0
    undetermined = 0
    for cid in cords:
        r = decode_cord(conn, cid)
        if r['value'] is None:
            undetermined += 1
        else:
            vals.append(r['value'])
            if r['confidence'] == 'high':
                high_conf += 1
    
    f['n_decoded'] = len(vals)
    f['n_undetermined'] = undetermined
    f['decode_rate'] = len(vals) / len(cords) if cords else 0
    f['high_conf_rate'] = high_conf / len(cords) if cords else 0
    
    if vals:
        vs = sorted(vals)
        f['val_min'] = vs[0]
        f['val_max'] = vs[-1]
        f['val_median'] = vs[len(vs)//2]
        f['zero_pct'] = vs.count(0) / len(vs)
        f['unique_pct'] = len(set(vs)) / len(vs)
        # Small-value concentration (census-like: most values < 20)
        f['small_pct'] = sum(1 for v in vs if v < 20) / len(vs)
        # Large values (warehouse-like: some values > 1000)
        f['has_large'] = any(v > 1000 for v in vs)
    else:
        f['val_min'] = f['val_max'] = f['val_median'] = None
        f['zero_pct'] = f['unique_pct'] = f['small_pct'] = 0
        f['has_large'] = False
    
    # Subsidiary rate
    c.execute('''SELECT COUNT(DISTINCT PENDANT_FROM) FROM cord 
                 WHERE KHIPU_ID = ? AND CORD_LEVEL > 1 AND PENDANT_FROM IS NOT NULL''', (khipu_id,))
    n_parents = c.fetchone()[0] or 0
    f['subsidiary_parent_rate'] = n_parents / f['n_top'] if f['n_top'] else 0
    
    # Color group regularity: check if top cords form fixed-size same-color runs
    # Build compound color string from COLOR_CD_1, OPERATOR_1, COLOR_CD_2
    c.execute('''SELECT 
                   COALESCE(cc.COLOR_CD_1,'') || COALESCE(cc.OPERATOR_1,'') || COALESCE(cc.COLOR_CD_2,'')
                 FROM cord co
                 LEFT JOIN ascher_cord_color cc ON co.CORD_ID = cc.CORD_ID
                 WHERE co.KHIPU_ID = ? AND co.CORD_LEVEL = 1
                 ORDER BY co.CORD_ORDINAL LIMIT 300''', (khipu_id,))
    colors = [r[0] for r in c.fetchall()]
    f['color_regularity'] = _color_regularity(colors)
    f['n_colors'] = len(set(c for c in colors if c))
    
    return f

def _color_regularity(colors):
    """Detect fixed-size color runs. Returns (group_size, consistency) or (0, 0)."""
    if len(colors) < 6:
        return (0, 0.0)
    # Try group sizes 2-12
    best = (0, 0.0)
    for gs in range(2, 13):
        matches = 0
        total = 0
        for i in range(0, len(colors) - gs + 1, gs):
            group = colors[i:i+gs]
            if len(group) == gs and len(set(group)) == 1 and group[0]:
                matches += 1
            total += 1
        if total > 0:
            consistency = matches / total
            if consistency > best[1] and consistency > 0.5:
                best = (gs, consistency)
    return best

def classify(f):
    """Classify based on features. Returns (type, confidence, notes)."""
    kid = f['khipu_id']
    notes = []
    
    # No data
    if f['n_cords'] == 0:
        return ('unclassified', 'high', 'no cord records')
    if f['n_decoded'] == 0 and f['n_top'] > 0:
        # Check if it's non-numerical vs data-missing
        if f['decode_rate'] == 0 and f['n_undetermined'] > 0:
            return ('unclassified', 'medium', 'cords present but no decodable values (missing turn data or non-numerical)')
        return ('unclassified', 'medium', 'no decodable values')
    
    # Anchor checks
    is_santa = kid in SANTA_IDS
    is_inkawasi = kid in INKAWASI_IDS
    
    # Census signals (Santa-like)
    census_signals = []
    if f['color_regularity'][0] > 0 and f['color_regularity'][1] > 0.7:
        census_signals.append(f"fixed {f['color_regularity'][0]}-cord color groups ({f['color_regularity'][1]:.0%})")
    if f['small_pct'] > 0.7 and f['n_decoded'] > 5:
        census_signals.append(f"{f['small_pct']:.0%} values < 20")
    if f['max_level'] <= 2:
        census_signals.append(f"shallow (max level {f['max_level']})")
    if f['zero_pct'] > 0.15 and f['zero_pct'] < 0.6 and f['n_decoded'] > 5:
        census_signals.append(f"{f['zero_pct']:.0%} zeros (sparse fields)")
    
    # Warehouse signals (Inkawasi-like)
    warehouse_signals = []
    if f['max_level'] >= 3:
        warehouse_signals.append(f"deep hierarchy (max level {f['max_level']})")
    if f['has_large']:
        warehouse_signals.append(f"large values (max {f['val_max']})")
    if f['subsidiary_parent_rate'] > 0.2:
        warehouse_signals.append(f"{f['subsidiary_parent_rate']:.0%} cords have subsidiaries")
    if f['provenance'] and 'Inkawasi' in str(f['provenance']):
        warehouse_signals.append("Inkawasi provenance")
    
    # Decision
    if is_santa:
        return ('census', 'high', f'Santa anchor; {"; ".join(census_signals)}' if census_signals else 'Santa anchor')
    if is_inkawasi:
        return ('warehouse', 'high', f'Inkawasi anchor; {"; ".join(warehouse_signals)}' if warehouse_signals else 'Inkawasi anchor')
    
    n_census = len(census_signals)
    n_warehouse = len(warehouse_signals)
    
    if n_census >= 3 and n_warehouse <= 1:
        return ('census-like', 'medium', '; '.join(census_signals))
    if n_warehouse >= 3 and n_census <= 1:
        return ('warehouse-like', 'medium', '; '.join(warehouse_signals))
    if n_census >= 2 and n_warehouse >= 2:
        cs = "; ".join(census_signals)
        ws = "; ".join(warehouse_signals)
        return ('unclassified', 'medium', f'mixed signals: census=[{cs}] warehouse=[{ws}]')
    
    # Weak signals
    all_signals = census_signals + warehouse_signals
    if all_signals:
        return ('unclassified', 'low', f'weak signals: {"; ".join(all_signals)}')
    return ('unclassified', 'low', 'no diagnostic structural signals')

def main():
    conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
    c = conn.cursor()
    c.execute('''SELECT KHIPU_ID FROM khipu_main WHERE NOT (
        COALESCE(PROVENANCE,'') LIKE '%Leymebamba%' OR COALESCE(PROVENANCE,'') LIKE '%Condores%' 
        OR COALESCE(PROVENANCE,'') LIKE '%Cóndores%' OR COALESCE(NOTES,'') LIKE '%funerary%' 
        OR COALESCE(NOTES,'') LIKE '%mummy%' OR COALESCE(NOTES,'') LIKE '%burial%'
    )''')
    ids = [r[0] for r in c.fetchall()]
    print(f'Classifying {len(ids)} non-funerary khipu...', file=sys.stderr)
    
    import csv
    # Resume: skip already-classified IDs
    done_ids = set()
    try:
        with open('/home/hatch/workspace/quipu-analysis/reclassification-2026-10-10.csv') as f:
            r = csv.DictReader(f)
            for row in r:
                done_ids.add(int(row['KHIPU_ID']))
    except FileNotFoundError:
        pass
    ids = [k for k in ids if k not in done_ids]
    print(f'Classifying {len(ids)} remaining khipu ({len(done_ids)} already done)...', file=sys.stderr)
    
    with open('/home/hatch/workspace/quipu-analysis/reclassification-2026-10-10.csv', 'a', newline='') as out:
        w = csv.writer(out)
        if not done_ids:
            w.writerow(['KHIPU_ID', 'DOCUMENT_TYPE', 'CONFIDENCE', 'EVIDENCE_NOTES'])
        for i, kid in enumerate(ids):
            try:
                f = get_features(conn, kid)
                dtype, conf, notes = classify(f)
                # Truncate notes
                notes = notes[:500]
                w.writerow([kid, dtype, conf, notes])
            except Exception as e:
                w.writerow([kid, 'unclassified', 'low', f'error: {str(e)[:200]}'])
            if (i+1) % 50 == 0:
                print(f'  {i+1}/{len(ids)}', file=sys.stderr)
    
    print('Done.', file=sys.stderr)

if __name__ == '__main__':
    main()
