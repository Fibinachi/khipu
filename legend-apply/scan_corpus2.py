"""Corpus-wide compound-color overlap with 1000368's legend vocabulary (fast version)."""
import sqlite3, csv, json
from collections import Counter, defaultdict

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')

LEGEND = {
    ('W','DB'),('W','VB'),('W','0G'),('W','KB'),('W','SR'),('W','SY'),
    ('BS','DB'),('BS','VB'),('BS','0G'),('BS','KB'),('BS','SR'),('BS','SY'),
    ('DB','VB'),('DB','0G'),('DB','KB'),('DB','SR'),('DB','SY'),
}

c = conn.cursor()
print("Running single grouped query...")
c.execute("""
    SELECT c.KHIPU_ID,
           TRIM(COALESCE(cc.COLOR_CD_1,'')),
           TRIM(COALESCE(cc.COLOR_CD_2,''))
    FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
""")
per_khipu = defaultdict(Counter)
for kid, c1, c2 in c.fetchall():
    p = (c1 if c1 else '?', c2)
    per_khipu[kid][p] += 1
print(f"{len(per_khipu)} khipu aggregated")

c.execute("SELECT KHIPU_ID, PROVENANCE, REGION, MUSEUM_NAME FROM khipu_main")
prov = {r[0]: (r[1] or '', r[2] or '', (r[3] or '')[:50]) for r in c.fetchall()}

rows = []
for kid, counter in per_khipu.items():
    compounds = {p: n for p, n in counter.items() if p[1]}
    legend_hits = {p: n for p, n in compounds.items() if p in LEGEND}
    n_legend = sum(legend_hits.values())
    n_comp = sum(compounds.values())
    pct = (n_legend / n_comp * 100) if n_comp else 0
    pr, rg, mu = prov.get(kid, ('','',''))
    rows.append({
        'khipu_id': kid,
        'n_cords': sum(counter.values()),
        'n_compound_cords': n_comp,
        'n_distinct_compounds': len(compounds),
        'n_legend_compounds': n_legend,
        'n_distinct_legend': len(legend_hits),
        'pct_compounds_in_legend': round(pct, 1),
        'legend_list': ';'.join(f"{a}+{b}x{n}" for (a,b), n in sorted(legend_hits.items())),
        'provenance': pr, 'region': rg, 'museum': mu,
    })

rows.sort(key=lambda r: (-r['n_legend_compounds'], -r['pct_compounds_in_legend']))
with open('/home/hatch/workspace/quipu-analysis/legend-apply/compound_overlap.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)

print("\nTop 25 by legend compound count (excluding 1000368 itself):")
shown = 0
for r in rows:
    if r['khipu_id'] == 1000368: continue
    print(f"  {r['khipu_id']}: {r['n_legend_compounds']} legend cords "
          f"({r['n_distinct_legend']} distinct, {r['pct_compounds_in_legend']}%) "
          f"[{r['provenance'] or '?'}]")
    shown += 1
    if shown >= 25: break
with open('/home/hatch/workspace/quipu-analysis/legend-apply/_top25.json','w') as f:
    json.dump([r for r in rows if r['khipu_id'] != 1000368][:25], f, indent=1)
print("DONE")
