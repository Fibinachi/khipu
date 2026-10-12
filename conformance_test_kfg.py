#!/usr/bin/env python3
"""
Khipu Structural Conformance Test — KFG edition.
Runs R1-R6 against kfg-khipu.db (66 khipu from Khipu Field Guide).
Schema adaptations from okr-khipu.db version:
- primary_cord has one row per KHIPU_ID (no PCORD_ID)
- cord has no ATTACHED_TO; R3 checks PENDANT_FROM != KHIPU_ID for level>=2
- color table is cord_color (COLOR_CD_1)
"""

import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), "kfg-khipu.db")

RULES = {
    "R1": "Every khipu SHALL have exactly one primary cord",
    "R2": "True pendant cords (attached directly to primary) SHALL be at level 1 or negative (top)",
    "R3": "Subsidiary cords (LEVEL >= 2) SHALL NOT attach directly to the primary cord",
    "R4": "Every cord SHALL have a recorded color",
    "R5": "Every khipu SHALL have at least one knotted cord",
    "R6": "Top cords (level < 0) SHALL form a valid tree above the primary cord",
}

def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("SELECT DISTINCT KHIPU_ID FROM cord WHERE KHIPU_ID IS NOT NULL")
    khipu_ids = [r[0] for r in cur.fetchall()]
    print(f"Testing {len(khipu_ids)} KFG khipu against {len(RULES)} rules\n")

    results = {r: {"pass": 0, "fail": 0, "fail_ids": []} for r in RULES}

    for kid in khipu_ids:
        # R1: exactly one primary_cord row
        cur.execute("SELECT COUNT(*) FROM primary_cord WHERE KHIPU_ID = ?", (kid,))
        n_primary = cur.fetchone()[0]
        if n_primary == 1:
            results["R1"]["pass"] += 1
        else:
            results["R1"]["fail"] += 1
            results["R1"]["fail_ids"].append((kid, n_primary))

        # R2: true pendants (PENDANT_FROM = KHIPU_ID*100000, i.e. attached to
        # primary) SHALL be at level 1. KFG uses synthetic primary CORD_ID.
        primary_ref = kid * 100000
        cur.execute("""SELECT CORD_ID, CORD_LEVEL FROM cord
                       WHERE KHIPU_ID = ? AND PENDANT_FROM = ?""",
                    (kid, primary_ref))
        pendants = cur.fetchall()
        if pendants:
            bad = [p for p in pendants if p[1] != 1]
            if not bad:
                results["R2"]["pass"] += 1
            else:
                results["R2"]["fail"] += 1
                results["R2"]["fail_ids"].append((kid, bad[:5]))
        else:
            # No pendants found with this convention; record as untestable
            results["R2"]["fail"] += 1
            results["R2"]["fail_ids"].append((kid, "no PENDANT_FROM=kid*100000"))

        # R3: subsidiaries (level >= 2) must not attach directly to primary,
        # i.e. PENDANT_FROM != KHIPU_ID*100000
        cur.execute("""SELECT CORD_ID, PENDANT_FROM FROM cord
                       WHERE KHIPU_ID = ? AND CORD_LEVEL >= 2""", (kid,))
        subs = cur.fetchall()
        if subs:
            bad = [s for s in subs if s[1] == primary_ref]
            if not bad:
                results["R3"]["pass"] += 1
            else:
                results["R3"]["fail"] += 1
                results["R3"]["fail_ids"].append((kid, bad[:5]))

        # R4: every cord has a color
        cur.execute("""SELECT COUNT(*) FROM cord c
                       LEFT JOIN cord_color cc ON c.CORD_ID = cc.CORD_ID AND c.KHIPU_ID = cc.KHIPU_ID
                       WHERE c.KHIPU_ID = ? AND cc.CORD_ID IS NULL""", (kid,))
        n_nocolor = cur.fetchone()[0]
        if n_nocolor == 0:
            results["R4"]["pass"] += 1
        else:
            results["R4"]["fail"] += 1
            results["R4"]["fail_ids"].append((kid, n_nocolor))

        # R5: at least one knotted cord
        cur.execute("""SELECT COUNT(DISTINCT k.CORD_ID) FROM knot k
                       WHERE k.KHIPU_ID = ?""", (kid,))
        n_knotted = cur.fetchone()[0]
        if n_knotted > 0:
            results["R5"]["pass"] += 1
        else:
            results["R5"]["fail"] += 1
            results["R5"]["fail_ids"].append(kid)

        # R6: top cords (level < 0). KFG has no negative levels in this
        # dataset; record as not-applicable rather than fail.
        cur.execute("""SELECT CORD_ID, PENDANT_FROM FROM cord
                       WHERE KHIPU_ID = ? AND CORD_LEVEL < 0""", (kid,))
        tops = cur.fetchall()
        if tops:
            top_ids = {t[0] for t in tops}
            bad = [coid for coid, pfrom in tops
                   if not (pfrom == primary_ref or pfrom in top_ids)]
            if not bad:
                results["R6"]["pass"] += 1
            else:
                results["R6"]["fail"] += 1
                results["R6"]["fail_ids"].append((kid, bad[:5]))
        # else: no top cords -> skip (neither pass nor fail)

    print("=" * 70)
    print("CONFORMANCE RESULTS — KFG DATASET (66 khipu)")
    print("=" * 70)
    for rid, rule in RULES.items():
        r = results[rid]
        total = r["pass"] + r["fail"]
        pct = 100 * r["pass"] / total if total else 0
        status = "PASS" if pct >= 95 else ("MARGINAL" if pct >= 80 else "FAIL")
        print(f"\n{rid}: {rule}")
        print(f"  {r['pass']}/{total} conform ({pct:.1f}%) [{status}]")
        if r["fail_ids"]:
            shown = r["fail_ids"][:8]
            print(f"  Non-conformant: {shown}")
            if len(r["fail_ids"]) > 8:
                print(f"  ... and {len(r['fail_ids']) - 8} more")

    con.close()

if __name__ == "__main__":
    main()
