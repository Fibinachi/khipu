"""Visual decoded view of a khipu with grammatical annotations."""
import sqlite3
import sys
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from decoder import decode_cord

KHIPU_ID = int(sys.argv[1]) if len(sys.argv) > 1 else 1000270
LIMIT = int(sys.argv[2]) if len(sys.argv) > 2 else 25

conn = sqlite3.connect('/home/hatch/workspace/quipu-analysis/okr-khipu.db')
c = conn.cursor()

# Khipu info
c.execute("SELECT PROVENANCE FROM khipu_main WHERE KHIPU_ID=?", (KHIPU_ID,))
prov = c.fetchone()
print(f"\n{'='*70}")
print(f"KHIPU {KHIPU_ID}  |  {prov[0] if prov else 'unknown'}")
print(f"{'='*70}")

# Grammatical tier colors
GRAMMATICAL = {'W', 'AB', 'MB', 'KB'}

c.execute("""
    SELECT c.CORD_ID, c.CORD_ORDINAL, c.CORD_LEVEL, cc.COLOR_CD_1, cc.COLOR_CD_2
    FROM cord c
    LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
    WHERE c.KHIPU_ID = ?
    ORDER BY c.CORD_ORDINAL
    LIMIT ?
""", (KHIPU_ID, LIMIT))

print(f"\n{'Ord':<5} {'Lvl':<4} {'Color':<10} {'Value':<8} {'Grammar':<40}")
print(f"{'-'*70}")

for cord_id, ordinal, level, col1, col2 in c.fetchall():
    color = col1 or '?'
    if col2:
        color = f"{col1}:{col2}"

    result = decode_cord(conn, cord_id)
    val = result['value']
    conf = result['confidence'][0].upper()  # H/M/L

    # Grammatical annotations
    notes = []
    base_color = col1 or ''
    if base_color in GRAMMATICAL:
        notes.append("GRAM")
        if base_color == 'W':
            notes.append("unmarked/nom")
        elif base_color == 'AB':
            notes.append("topic/head")
        elif base_color == 'KB':
            notes.append("relational")
    else:
        notes.append("IDENT")

    if level and level >= 2:
        notes.append(f"L{level}=later/addition")
    if level == 1:
        notes.append("founding")

    # Twist direction
    c2 = conn.cursor()
    c2.execute("SELECT DISTINCT DIRECTION FROM knot WHERE CORD_ID=?", (cord_id,))
    dirs = [r[0] for r in c2.fetchall() if r[0]]
    if dirs:
        twist = '/'.join(set(dirs))
        notes.append(f"twist:{twist}")

    grammar = ' '.join(notes)
    val_str = str(val) if val is not None else '?'
    print(f"{ordinal:<5} {level or '?':<4} {color:<10} {val_str:<8} {grammar:<40} [{conf}]")

print(f"\n{'='*70}")
print("GRAM=grammatical-tier color (case role)  IDENT=identity-tier color")
print("L1=founding entry  L2+=later addition (accrual chronology)")
print("twist:Z/S/U = document register  [H]igh/[M]ed/[L]ow decode confidence")
print(f"{'='*70}\n")
