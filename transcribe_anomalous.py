"""Step 3: Transcribe anomalous khipu into symbolic letter-notation."""
import sqlite3
import csv

DB = '/home/hatch/workspace/quipu-analysis/okr-khipu.db'
conn = sqlite3.connect(DB)
c = conn.cursor()

# Anomalous khipu: (id, one-line reason)
TARGETS = [
    (1000004, "Red signal threads (senales rojos) woven INTO pendant fibers; loose pendant tied above a long knot on #156"),
    (1000005, "Two different khipus joined (main cords 0.3cm vs 0.5cm); red signal threads at measured distances on pendants"),
    (1000008, "Primary cord knot UNITES THREE khipus (257D/UR13 + 257C/UR12 + 257F/UR15)"),
    (1000009, "White signal threads at 26cm and 32cm; broken pendant repaired with matching thread from fragment bag"),
    (1000018, "Leymebamba funerary; check red-flag (RL-W x49) cord structure"),
    (1000027, "Main cord (A) connected to second cord (B); pendants 1-11 may all be subsidiaries of a single pendant"),
    (1000144, "6-pendant groups with 'non-existent' 6th/7th positions — phantom slots in fixed color pattern"),
    (1000176, "Pendant not attached in usual way; peculiar s-knot placement in group 1"),
    (1000178, "Pendant 6 slipped THROUGH a knot on its own subsidiary (recursive attachment)"),
    (1000183, "Short 2cm cords (YB:0G or W) tied THROUGH knots as markers/flags"),
    (1000197, "Joined to AS026B: main cords knotted together"),
    (1000198, "Joined to AS026A; 103/150 subsidiaries have exactly one knot (S or E both read as 1)"),
    (1000201, "Pendant 70 replaced UPSIDE DOWN (knot order reversed: 6s,5L,E instead of 1s,5L,6s); P43 end in loop"),
    (1000239, "Pendant 21 has 6 subsidiaries attached THROUGH its doubled end"),
    (1000249, "Z-spiral roll construction (rolls right-to-left, pendants facing away)"),
    (1000344, "P10 finishing knot tied AROUND P11 (pendant-to-pendant link); phantom missing pendants"),
    (1000454, "Tricolor mottling anomalous in Group 1"),
    (1000504, "Spiral knots (SP) with and without axis — unusual pair on UR193"),
    (1000567, "Cord 13 ambiguous: pendant or top cord?; P28 loose with modern repair"),
    (1000583, "All knots bunched near principal cord; place value unreadable; knot direction unclear"),
]

def get_color(kh, cid):
    c.execute("""SELECT COLOR_CD_1, OPERATOR_1, COLOR_CD_2, OPERATOR_2
                 FROM ascher_cord_color WHERE KHIPU_ID=? AND CORD_ID=?""", (kh, cid))
    r = c.fetchone()
    if not r or not r[0]:
        return "?"
    col = r[0].strip()
    if r[1] and r[2]:
        col += r[1].strip() + r[2].strip()
        if r[3]:
            col += r[3].strip()  # rare 3-color
    return col

def get_knotseq(cid):
    """Return knot sequence string, clusters top-to-bottom separated by -."""
    c.execute("""SELECT CLUSTER_ID, START_POS FROM knot_cluster
                 WHERE CORD_ID=? ORDER BY START_POS ASC""", (cid,))
    clusters = c.fetchall()
    if not clusters:
        # check if any knots exist at all
        c.execute("SELECT COUNT(*) FROM knot WHERE CORD_ID=?", (cid,))
        if c.fetchone()[0] == 0:
            return "\u2205"
        else:
            return "?"
    parts = []
    for cl_id, _ in clusters:
        c.execute("""SELECT TYPE_CODE, NUM_TURNS, DIRECTION, AXIS_ORIENTATION, COUNT(*) as n
                     FROM knot WHERE CLUSTER_ID=?
                     GROUP BY TYPE_CODE, NUM_TURNS, DIRECTION, AXIS_ORIENTATION
                     ORDER BY MIN(KNOT_ORDINAL)""", (cl_id,))
        knots = []
        for tcode, turns, direction, axis, n in c.fetchall():
            tc = (tcode or "").strip()
            if not tc:
                tc = "?"
            sym = tc
            # turns for L/SP/BL
            if tc in ("L", "SP", "BL") and turns:
                try:
                    sym += str(int(float(turns)))
                except:
                    pass
            # axis orientation for SP (cf. 1000504 with/without axis)
            if tc == "SP" and axis and axis.strip():
                sym += "{%s}" % axis.strip()
            # collapse multiples
            if n > 1 and tc in ("S", "E", "EE", "TF"):
                sym += str(n)
            elif n > 1:
                sym += "x%d" % n
            # anomalous direction
            if direction and direction.strip() not in ("Z", ""):
                sym += direction.strip().lower()
            knots.append(sym)
        parts.append("".join(knots) if knots else "?")
    return "-".join(parts)

def transcribe(kh):
    lines = []
    # body cords in physical order
    c.execute("""SELECT CORD_ID, CORD_ORDINAL, CORD_LEVEL, PENDANT_FROM, CORD_NOTES
                 FROM cord WHERE KHIPU_ID=?
                 ORDER BY COALESCE(CORD_ORDINAL, 999999), CORD_ID""", (kh,))
    # build ordinal -> cord map for parent references
    cords = c.fetchall()
    ord_map = {}
    for cid, cord_ord, lvl, pf, notes in cords:
        if cord_ord is not None:
            ord_map[cid] = cord_ord
    # parent CORD_ID -> parent ordinal; sibling index for subsidiaries
    from collections import defaultdict
    sib_count = defaultdict(int)
    result = []  # (sort_key, cord_ordinal_out, line)
    for cid, cord_ord, lvl, pf, notes in cords:
        co = cord_ord if cord_ord is not None else "?"
        lvl_mark = ""
        parent_ref = ""
        ord_out = co
        if lvl and lvl > 1:
            lvl_mark = "^" * (lvl - 1)
            # find parent ordinal
            if pf and pf in ord_map:
                parent_ref = f"(P{ord_map[pf]})"
            elif pf:
                parent_ref = f"(P?{pf})"
            # sibling index: nth subsidiary of this parent
            sib_count[pf] += 1
            co = f"{sib_count[pf]}"
            ord_out = f"{ord_map.get(pf, '?')}s{sib_count[pf]}"
        col = get_color(kh, cid)
        ks = get_knotseq(cid)
        flags = ""
        if notes:
            nl = notes.lower()
            if "upside down" in nl or "reversed" in nl:
                flags += "[rev]"
            if "loop" in nl:
                flags += "[loop]"
            if "mended" in nl or "repaired" in nl:
                flags += "[mended]"
            if "loose" in nl or "movable" in nl:
                flags += "[loose]"
            if "modern" in nl:
                flags += "[modern]"
        line = f"{lvl_mark}{co}{parent_ref}:{col}:{ks}{flags}"
        result.append((co if isinstance(co, int) else 999999, lvl or 0, ord_out, line))
    # sort already by ordinal; return lines
    return [(r[2], r[3]) for r in result]

# --- run ---
all_rows = []  # for CSV: (khipu_id, cord_ordinal, transcription)
md_parts = []
for kh, reason in TARGETS:
    c.execute("SELECT COUNT(*) FROM cord WHERE KHIPU_ID=?", (kh,))
    n_cords = c.fetchone()[0]
    md_parts.append(f"\n## {kh} — {n_cords} cords")
    md_parts.append(f"# ANOMALY: {reason}")
    # full khipu note as comment
    c.execute("SELECT substr(NOTES,1,300) FROM khipu_main WHERE KHIPU_ID=?", (kh,))
    r = c.fetchone()
    if r and r[0]:
        note = r[0].replace("\n", " ").strip()
        md_parts.append(f"# NOTE: {note}")
    # header line
    c.execute("""SELECT PCORD_ID FROM primary_cord WHERE KHIPU_ID=? LIMIT 1""", (kh,))
    r = c.fetchone()
    if r:
        pcol = get_color(kh, r[0])
        hline = f"H:{pcol}:{get_knotseq(r[0])}"
        md_parts.append(hline)
        all_rows.append((kh, "H", hline))
    for ord_out, line in transcribe(kh):
        md_parts.append(line)
        all_rows.append((kh, ord_out, line))

with open('/home/hatch/workspace/quipu-analysis/anomalous-transcriptions.md', 'w') as f:
    f.write("# Anomalous Khipu Transcriptions\n")
    f.write("Notation: see transcription-notation.md\n")
    f.write("\n".join(md_parts))

with open('/home/hatch/workspace/quipu-analysis/anomalous-transcriptions.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['KHIPU_ID', 'CORD_ORDINAL', 'TRANSCRIPTION'])
    w.writerows(all_rows)

print(f"Transcribed {len(TARGETS)} khipu, {len(all_rows)} cord lines")
