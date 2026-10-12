"""Corpus-wide compound-color overlap with 1000368's legend vocabulary."""
import sqlite3, csv, json

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')

# Legend compounds: the defined (color1, color2) pairs, excluding plain singles
LEGEND = {
    ('W','DB'),('W','VB'),('W','0G'),('W','KB'),('W','SR'),('W','SY'),
    ('BS','DB'),('BS','VB'),('BS','0G'),('BS','KB'),('BS','SR'),('BS','SY'),
    ('DB','VB'),('DB','0G'),('DB','KB'),('DB','SR'),('DB','SY'),
}
LEGEND_SINGLES = {('DB',''),('W',''),('BS','')}
ALL_LEGEND = LEGEND | LEGEND_SINGLES

c = conn.cursor()
c.execute("SELECT DISTINCT KHIPU_ID FROM cord")
kids = [r[0] for r in c.fetchall()]
print(f"{len(kids)} khipu")

# Provenance map
c.execute("SELECT KHIPU_ID, PROVENANCE, REGION, MUSEUM_NAME FROM khipu_main")
prov = {r[0]: (r[1] or '', r[2] or '', r[3] or '') for r in c.fetchall()}

rows = []
for ki, kid in enumerate(kids):
    c2 = conn.cursor()
    c2.execute("""
        SELECT cc.COLOR_CD_1, cc.COLOR_CD_2
        FROM cord c LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
        WHERE c.KHIPU_ID = ?
    """, (kid,))
    seen_pairs = {}
    for r1, r2 in c2.fetchall():
        p = ((r1 or '?').strip(), (r2 or '').strip())
        seen_pairs[p] = seen_pairs.get(p, 0) + 1
    compounds = {p: n for p, n in seen_pairs.items() if p[1]}  # has second color
    legend_hits = {p: n for p, n in compounds.items() if p in LEGEND}
    n_legend = sum(legend_hits.values())
    n_comp = sum(compounds.values())
    pct = (n_legend / n_comp * 100) if n_comp else 0
    pr, rg, mu = prov.get(kid, ('','',''))
    rows.append({
        'khipu_id': kid,
        'n_cords': sum(seen_pairs.values()),
        'n_compound_cords': n_comp,
        'n_distinct_compounds': len(compounds),
        'n_legend_compounds': n_legend,
        'n_distinct_legend': len(legend_hits),
        'pct_compounds_in_legend': round(pct, 1),
        'legend_list': ';'.join(f"{a}+{b}x{n}" for (a,b), n in sorted(legend_hits.items())),
        'provenance': pr, 'region': rg, 'museum': mu,
    })
    if ki % 100 == 0:
        print(f"  {ki}/{len(kids)}")

rows.sort(key=lambda r: (-r['n_legend_compounds'], -r['pct_compounds_in_legend']))
with open('/home/hatch/workspace/quipu-analysis/legend-apply/compound_overlap.csv','w',newline='') as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader(); w.writerows(rows)

print("\nTop 25 by legend compound count:")
for r in rows[:25]:
    print(f"  {r['khipu_id']}: {r['n_legend_compounds']} legend cords "
          f"({r['n_distinct_legend']} distinct, {r['pct_compounds_in_legend']}%) "
          f"[{r['provenance'] or '?'} / {r['museum'][:40]}]")
# Save top list
with open('/home/hatch/workspace/quipu-analysis/legend-apply/_top25.json','w') as f:
    json.dump(rows[:25], f, indent=1)
