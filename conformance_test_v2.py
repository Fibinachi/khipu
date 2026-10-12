#!/usr/bin/env python3
"""
Khipu Structural Conformance Test v0.2
Tests the corpus against the developed specification.
Incorporates all corrections from conformance review:
- R1 uses DISTINCT (duplicate rows in primary_cord are data dirt, not violations)
- R2 checks PENDANT_FROM = KHIPU_ID (true pendants), allowing level 1 or negative (top)
- R6 validates top cord attachment properly
"""

import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), "okr-khipu.db")

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
    print(f"Testing {len(khipu_ids)} khipu against {len(RULES)} rules\n")

    results = {r: {"pass": 0, "fail": 0, "fail_ids": []} for r in RULES}

    for kid in khipu_ids:
        # R1: exactly one DISTINCT primary cord
        cur.execute("SELECT COUNT(DISTINCT PCORD_ID) FROM primary_cord WHERE KHIPU_ID = ?", (kid,))
        n_primary = cur.fetchone()[0]
        if n_primary == 1:
            results["R1"]["pass"] += 1
        else:
            results["R1"]["fail"] += 1
            results["R1"]["fail_ids"].append((kid, n_primary))

        # R2: true pendants (PENDANT_FROM = KHIPU_ID) at level 1 or negative
        cur.execute("""SELECT CORD_ID, CORD_LEVEL FROM cord
                       WHERE KHIPU_ID = ? AND PENDANT_FROM = KHIPU_ID""", (kid,))
        pendants = cur.fetchall()
        if pendants:
            bad = [p for p in pendants if not (p[1] == 1 or (p[1] is not None and p[1] < 0))]
            if not bad:
                results["R2"]["pass"] += 1
            else:
                results["R2"]["fail"] += 1
                results["R2"]["fail_ids"].append((kid, bad[:5]))

        # R3: subsidiaries (level >= 2) must not attach directly to primary
        cur.execute("SELECT DISTINCT PCORD_ID FROM primary_cord WHERE KHIPU_ID = ?", (kid,))
        pcords = {r[0] for r in cur.fetchall()}
        cur.execute("""SELECT CORD_ID, ATTACHED_TO FROM cord
                       WHERE KHIPU_ID = ? AND CORD_LEVEL >= 2""", (kid,))
        subs = cur.fetchall()
        if subs:
            bad = [s for s in subs if s[1] in pcords]
            if not bad:
                results["R3"]["pass"] += 1
            else:
                results["R3"]["fail"] += 1
                results["R3"]["fail_ids"].append((kid, bad[:5]))

        # R4: every cord has a color
        cur.execute("""SELECT COUNT(*) FROM cord c
                       LEFT JOIN ascher_cord_color cc ON c.CORD_ID = cc.CORD_ID
                       WHERE c.KHIPU_ID = ? AND cc.CORD_ID IS NULL""", (kid,))
        n_nocolor = cur.fetchone()[0]
        if n_nocolor == 0:
            results["R4"]["pass"] += 1
        else:
            results["R4"]["fail"] += 1
            results["R4"]["fail_ids"].append((kid, n_nocolor))

        # R5: at least one knotted cord
        cur.execute("""SELECT COUNT(DISTINCT k.CORD_ID) FROM knot k
                       JOIN cord c ON k.CORD_ID = c.CORD_ID
                       WHERE c.KHIPU_ID = ?""", (kid,))
        n_knotted = cur.fetchone()[0]
        if n_knotted > 0:
            results["R5"]["pass"] += 1
        else:
            results["R5"]["fail"] += 1
            results["R5"]["fail_ids"].append(kid)

        # R6: top cords form valid tree (each top cord's parent is primary or another top cord)
        cur.execute("""SELECT CORD_ID, PENDANT_FROM FROM cord
                       WHERE KHIPU_ID = ? AND CORD_LEVEL < 0""", (kid,))
        tops = cur.fetchall()
        if tops:
            top_ids = {t[0] for t in tops}
            bad = []
            for coid, pfrom in tops:
                # Attached to primary (PENDANT_FROM = khipu_id) or to another top cord
                if pfrom == kid or pfrom in top_ids:
                    continue
                # Also check ATTACHED_TO
                cur.execute("SELECT ATTACHED_TO FROM cord WHERE CORD_ID = ?", (coid,))
                atto = cur.fetchone()[0]
                if atto in pcords or atto in top_ids:
                    continue
                bad.append(coid)
            if not bad:
                results["R6"]["pass"] += 1
            else:
                results["R6"]["fail"] += 1
                results["R6"]["fail_ids"].append((kid, bad[:5]))

    print("=" * 70)
    print("CONFORMANCE RESULTS v0.2")
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
