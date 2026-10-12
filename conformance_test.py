#!/usr/bin/env python3
"""
Khipu Structural Conformance Test v0.1
Tests the corpus against SHALL statements derived from the structural grammar.
Model: ISO-style conformance testing — each rule is PASS/FAIL per khipu.
"""

import sqlite3
import os

DB = os.path.join(os.path.dirname(__file__), "okr-khipu.db")

RULES = {
    "R1": "Every khipu SHALL have exactly one primary cord",
    "R2": "Pendant cords SHALL attach at CORD_LEVEL = 1 (top cords at negative levels excluded)",
    "R3": "Subsidiary cords (LEVEL >= 2) SHALL attach to a pendant, not directly to the primary cord",
    "R4": "Every cord SHALL have a recorded color",
    "R5": "Every khipu SHALL have at least one knotted cord (non-empty document)",
    "R6": "Top cords (CORD_LEVEL < 0) SHALL attach to the primary cord or to another top cord",
}

def main():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # Get all khipu IDs
    cur.execute("SELECT DISTINCT KHIPU_ID FROM cord WHERE KHIPU_ID IS NOT NULL")
    khipu_ids = [r[0] for r in cur.fetchall()]
    print(f"Testing {len(khipu_ids)} khipu against {len(RULES)} rules\n")

    results = {r: {"pass": 0, "fail": 0, "fail_ids": []} for r in RULES}

    for kid in khipu_ids:
        # R1: exactly one primary cord
        cur.execute("SELECT COUNT(*) FROM primary_cord WHERE KHIPU_ID = ?", (kid,))
        n_primary = cur.fetchone()[0]
        if n_primary == 1:
            results["R1"]["pass"] += 1
        else:
            results["R1"]["fail"] += 1
            results["R1"]["fail_ids"].append((kid, n_primary))

        # R2: pendants at level 1 (excluding top cords at negative levels)
        # A pendant is a cord with PENDANT_FROM set and CORD_LEVEL >= 1
        cur.execute("""SELECT COUNT(*) FROM cord
                       WHERE KHIPU_ID = ? AND PENDANT_FROM IS NOT NULL
                       AND CORD_LEVEL >= 1""", (kid,))
        n_pendants = cur.fetchone()[0]
        if n_pendants > 0:
            cur.execute("""SELECT COUNT(*) FROM cord
                           WHERE KHIPU_ID = ? AND PENDANT_FROM IS NOT NULL
                           AND CORD_LEVEL >= 1 AND CORD_LEVEL != 1""", (kid,))
            n_non_l1 = cur.fetchone()[0]
            if n_non_l1 == 0:
                results["R2"]["pass"] += 1
            else:
                results["R2"]["fail"] += 1
                results["R2"]["fail_ids"].append((kid, n_non_l1, n_pendants))

        # R3: subsidiaries attach to pendants
        cur.execute("""SELECT CORD_ID, ATTACHED_TO FROM cord
                       WHERE KHIPU_ID = ? AND CORD_LEVEL >= 2""", (kid,))
        subs = cur.fetchall()
        if subs:
            # Get primary cord ID
            cur.execute("SELECT PCORD_ID FROM primary_cord WHERE KHIPU_ID = ?", (kid,))
            prow = cur.fetchone()
            pcord_id = prow[0] if prow else None
            bad = [s for s in subs if s[1] == pcord_id]
            if not bad:
                results["R3"]["pass"] += 1
            else:
                results["R3"]["fail"] += 1
                results["R3"]["fail_ids"].append((kid, len(bad), len(subs)))

        # R4: every cord has a color
        # Check ascher_cord_color table
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

        # R6: top cords attach to primary or another top cord
        cur.execute("""SELECT CORD_ID, PENDANT_FROM, ATTACHED_TO FROM cord
                       WHERE KHIPU_ID = ? AND CORD_LEVEL < 0""", (kid,))
        tops = cur.fetchall()
        if tops:
            cur.execute("SELECT PCORD_ID FROM primary_cord WHERE KHIPU_ID = ?", (kid,))
            prow = cur.fetchone()
            pcord_id = prow[0] if prow else None
            # Top cord is conformant if PENDANT_FROM = khipu_id (attached to primary)
            # or attached to another top cord
            top_ids = {t[0] for t in tops}
            bad = []
            for coid, pfrom, atto in tops:
                # PENDANT_FROM = khipu_id means attached to primary cord
                if pfrom == kid:
                    continue
                # Attached to another top cord
                if pfrom in top_ids or atto in top_ids:
                    continue
                bad.append(coid)
            if not bad:
                results["R6"]["pass"] += 1
            else:
                results["R6"]["fail"] += 1
                results["R6"]["fail_ids"].append((kid, bad))

    # Report
    print("=" * 70)
    print("CONFORMANCE RESULTS")
    print("=" * 70)
    for rid, rule in RULES.items():
        r = results[rid]
        total = r["pass"] + r["fail"]
        pct = 100 * r["pass"] / total if total else 0
        status = "PASS" if pct >= 95 else ("MARGINAL" if pct >= 80 else "FAIL")
        print(f"\n{rid}: {rule}")
        print(f"  {r['pass']}/{total} conform ({pct:.1f}%) [{status}]")
        if r["fail_ids"] and len(r["fail_ids"]) <= 10:
            print(f"  Non-conformant: {r['fail_ids']}")
        elif r["fail_ids"]:
            print(f"  Non-conformant (first 10): {r['fail_ids'][:10]}")
            print(f"  ... and {len(r['fail_ids']) - 10} more")

    con.close()

if __name__ == "__main__":
    main()
