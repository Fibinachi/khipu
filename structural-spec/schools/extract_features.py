"""Extract per-khipu features for school clustering. Fast: counts from DB, no full decode."""
import sqlite3, csv, json
from collections import Counter, defaultdict

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

c.execute("SELECT KHIPU_ID, PROVENANCE, REGION FROM khipu_main")
khipus = [(r[0], (r[1] or '').strip(), (r[2] or '').strip()) for r in c.fetchall()]
print(f"{len(khipus)} khipu")

features = {}
for idx, (kid, prov, reg) in enumerate(khipus):
    if idx % 100 == 0:
        print(f"  {idx}/{len(khipus)}")

    # Cord count, max level, distinct ordinals
    c.execute("SELECT COUNT(*), MAX(CORD_LEVEL), COUNT(DISTINCT CORD_ORDINAL) FROM cord WHERE KHIPU_ID=?", (kid,))
    n_cords, max_lvl, n_ord = c.fetchone()

    # Palette: top 5 colors with fractions
    c.execute("""
        SELECT cc.COLOR_CD_1, COUNT(*) FROM cord co
        JOIN ascher_cord_color cc ON co.CORD_ID = cc.CORD_ID
        WHERE co.KHIPU_ID=? GROUP BY cc.COLOR_CD_1 ORDER BY COUNT(*) DESC LIMIT 5
    """, (kid,))
    pal = [((col or '?').strip(), n) for col, n in c.fetchall()]
    pal_total = sum(n for _, n in pal) or 1
    pal_frac = {col: round(n / pal_total, 3) for col, n in pal}
    white_frac = pal_frac.get('W', 0)

    # Knot types
    c.execute("""
        SELECT k.TYPE_CODE, COUNT(*) FROM knot k
        JOIN cord co ON k.CORD_ID = co.CORD_ID
        WHERE co.KHIPU_ID=? GROUP BY k.TYPE_CODE
    """, (kid,))
    knots = { (t or '?').strip(): n for t, n in c.fetchall() }
    knot_total = sum(knots.values()) or 1
    knot_frac = {t: round(n / knot_total, 3) for t, n in knots.items()}

    # Twist direction
    c.execute("""
        SELECT k.DIRECTION, COUNT(*) FROM knot k
        JOIN cord co ON k.CORD_ID = co.CORD_ID
        WHERE co.KHIPU_ID=? GROUP BY k.DIRECTION
    """, (kid,))
    twist = { (d or '?').strip(): n for d, n in c.fetchall() }
    twist_total = sum(twist.values()) or 1
    twist_frac = {d: round(n / twist_total, 3) for d, n in twist.items()}

    # Self-transition rate (log vs tabular signal) from ordinal color sequence
    c.execute("""
        SELECT co.CORD_ORDINAL, cc.COLOR_CD_1 FROM cord co
        LEFT JOIN ascher_cord_color cc ON co.CORD_ID = cc.CORD_ID
        WHERE co.KHIPU_ID=? ORDER BY co.CORD_ORDINAL
    """, (kid,))
    seen = {}
    for o, col in c.fetchall():
        if o not in seen:
            seen[o] = (col or '?').strip()
    seq = [seen[o] for o in sorted(seen.keys())]
    self_t = sum(1 for i in range(len(seq) - 1) if seq[i] == seq[i + 1])
    self_rate = round(self_t / (len(seq) - 1), 3) if len(seq) > 1 else 0

    features[kid] = {
        'n_cords': n_cords, 'n_ord': n_ord, 'max_level': max_lvl or 1,
        'palette': pal_frac, 'white_frac': white_frac,
        'knots': knot_frac, 'twist': twist_frac,
        'self_rate': self_rate,
        'provenance': prov, 'region': reg,
    }

out = '/home/hatch/workspace/quipu-analysis/schools/khipu_features.json'
import os
os.makedirs(os.path.dirname(out), exist_ok=True)
with open(out, 'w') as f:
    json.dump(features, f)
print(f"Wrote {out} ({len(features)} khipu)")
