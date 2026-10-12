"""Generation test: compare synthetic khipu statistics to real corpus."""
import sqlite3
import sys
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis/abcs')
from generator import generate
from collections import Counter
import csv

# Real corpus stats
conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

print("=== REAL CORPUS ===")
c.execute('SELECT KHIPU_ID, COUNT(*) FROM cord GROUP BY KHIPU_ID')
real_cords = [r[1] for r in c.fetchall()]
print(f"Khipu: {len(real_cords)}")
print(f"Cords/khipu: mean={sum(real_cords)/len(real_cords):.1f}, "
      f"median={sorted(real_cords)[len(real_cords)//2]}, max={max(real_cords)}")

c.execute('''
    SELECT d.COLOR, COUNT(*)
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    LEFT JOIN ascher_color_dc d ON TRIM(cc.COLOR_CD_1) = d.AS_COLOR_CD
    GROUP BY d.COLOR
''')
real_fam = {r[0] or '?': r[1] for r in c.fetchall()}
total = sum(real_fam.values())
print(f"Family distribution: " +
      ", ".join(f"{k}={v/total:.2f}" for k, v in sorted(real_fam.items(), key=lambda x: -x[1])[:6]))

c.execute('SELECT TYPE_CODE, COUNT(*) FROM knot GROUP BY TYPE_CODE')
real_kt = {r[0] or '?': r[1] for r in c.fetchall()}
kt_total = sum(real_kt.values())
print(f"Knot types: " +
      ", ".join(f"{k}={v/kt_total:.2f}" for k, v in sorted(real_kt.items(), key=lambda x: -x[1])[:5]))

c.execute('SELECT CORD_LEVEL, COUNT(*) FROM cord GROUP BY CORD_LEVEL')
real_lv = {r[0]: r[1] for r in c.fetchall()}
lv_total = sum(real_lv.values())
print(f"Levels: " +
      ", ".join(f"L{k}={v/lv_total:.2f}" for k, v in sorted(real_lv.items()) if k and k > 0))

print()
print("=== SYNTHETIC (n=100) ===")
khipus = generate(100, seed=123)
syn_cords = [len(kh.cords) for kh in khipus]
print(f"Cords/khipu: mean={sum(syn_cords)/len(syn_cords):.1f}, "
      f"median={sorted(syn_cords)[len(syn_cords)//2]}, max={max(syn_cords)}")

syn_fam = Counter()
syn_kt = Counter()
syn_lv = Counter()
for kh in khipus:
    s = kh.stats()
    for f, n in s['families'].items():
        syn_fam[f] += n
    for t, n in s['knot_types'].items():
        syn_kt[t] += n
    for l, n in s['levels'].items():
        syn_lv[l] += n

st = sum(syn_fam.values())
print(f"Family distribution: " +
      ", ".join(f"{k}={v/st:.2f}" for k, v in syn_fam.most_common(6)))
kt = sum(syn_kt.values())
print(f"Knot types: " +
      ", ".join(f"{k}={v/kt:.2f}" for k, v in syn_kt.most_common(5)))
lv = sum(syn_lv.values())
print(f"Levels: " +
      ", ".join(f"L{k}={v/lv:.2f}" for k, v in sorted(syn_lv.items())))

print()
print("=== COMPARISON ===")
print(f"{'Metric':<25} {'Real':<20} {'Synthetic':<20} {'Match?'}")
print(f"{'Mean cords/khipu':<25} {sum(real_cords)/len(real_cords):<20.1f} {sum(syn_cords)/len(syn_cords):<20.1f} "
      f"{'~' if abs(sum(real_cords)/len(real_cords) - sum(syn_cords)/len(syn_cords)) < 20 else 'NO'}")
for fam in ['B', 'A', 'G']:
    r = real_fam.get(fam, 0) / total
    s = syn_fam.get(fam, 0) / st
    print(f"{'Family '+fam:<25} {r:<20.2f} {s:<20.2f} {'YES' if abs(r-s) < 0.1 else 'NO'}")
for kt_name in ['S', 'L', 'E']:
    r = real_kt.get(kt_name, 0) / kt_total
    s = syn_kt.get(kt_name, 0) / kt
    print(f"{'Knot '+kt_name:<25} {r:<20.2f} {s:<20.2f} {'YES' if abs(r-s) < 0.1 else 'NO'}")
