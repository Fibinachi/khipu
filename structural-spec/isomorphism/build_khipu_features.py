#!/usr/bin/env python3
"""Build khipu-side feature co-occurrence database for distributional isomorphism.

Input:  ~/workspace/quipu-analysis/anomalous-transcriptions.csv
Output: ~/workspace/quipu-analysis/isomorphism/
        khipu_features.csv, feature_ids.csv, within_cord_pmi.csv,
        sequential_bigrams.csv, hierarchical_pairs.csv, README.md,
        sanity_report.md

Feature = atomic observable on a cord (color, knot type, direction, level,
turn count, structural flag). Each gets a stable integer ID.
"""
import csv, re, math, os
from collections import Counter, defaultdict

BASE = os.path.expanduser("~/workspace/quipu-analysis")
IN_CSV = os.path.join(BASE, "anomalous-transcriptions.csv")
OUT = os.path.join(BASE, "isomorphism")
os.makedirs(OUT, exist_ok=True)

# ---------- transcription parsing ----------
CLUSTER_RE = re.compile(
    r"^(EE|LL|BL|SP|TF|S|L|E|X)"    # knot type (X = unknown/'' placeholder)
    r"(\{[^}]*\})?"                  # optional axis {..}
    r"(\d*)"                        # optional turns/count
    r"([zsu]?)$"                     # optional direction
)
FLAG_RE = re.compile(r"\[([^\]]+)\]")

def parse_line(trans):
    """Return dict of features for one cord transcription."""
    f = {"colors": [], "compound": None, "knots": [], "dirs": [],
         "turns": [], "axis": [], "empty": False, "missing": False,
         "broken": False, "flags": [], "level": "L1", "parent": None,
         "ordinal": None, "is_header": False}
    t = trans.strip()
    # level
    if t.startswith("H:"):
        f["is_header"] = True
        f["level"] = "H"
        rest = t[2:]
    else:
        m = re.match(r"^(\^+)", t)
        if m:
            n = len(m.group(1))
            f["level"] = {1: "L2", 2: "L3", 3: "L4"}.get(n, "L4+")
            rest = t[n:]
        else:
            rest = t
    # ordinal + optional (Pn)
    m = re.match(r"^([^:]+):(.*)$", rest, re.S)
    if not m:
        return f
    ordpart, rest2 = m.group(1), m.group(2)
    pm = re.search(r"\(P(\d+)\)", ordpart)
    if pm:
        f["parent"] = int(pm.group(1))
    om = re.match(r"(\d+)", ordpart)
    if om:
        f["ordinal"] = int(om.group(1))
    # split color vs knotseq on LAST colon that precedes knot-like content.
    # color field may itself contain ':' (compound AB:W). Strategy: split rest2
    # on ':'; the knotseq is the final segment if it looks like knots/empty,
    # else the whole thing is color-only with empty knotseq.
    parts = rest2.split(":")
    knotseq = parts[-1]
    colorfield = ":".join(parts[:-1])
    # normalize '' (unknown/illegible knot placeholder) to X before parsing
    knotseq = knotseq.replace("''", "X")
    # knotseq sanity: should match clusters / empty / missing
    if not re.fullmatch(r"((EE|LL|BL|SP|TF|S|L|E|X)\{?[^}]*\}?[0-9]*[zsu]?-?)*|∅|\?|~", knotseq):
        # not knot-like: treat whole rest2 as color, knotseq empty
        colorfield, knotseq = rest2, "∅"
    # flags
    for fm in FLAG_RE.finditer(knotseq):
        f["flags"].append(fm.group(1))
    knotseq = FLAG_RE.sub("", knotseq)
    # special states
    if knotseq == "∅" or knotseq == "":
        f["empty"] = True
    elif knotseq == "?":
        f["missing"] = True
    elif "~" in knotseq:
        f["broken"] = True
        knotseq = knotseq.replace("~", "")
    # knot clusters: split on '-' AND on new knot-type letters (transcriber
    # sometimes concatenates, e.g. SP{U}S3). findall handles both.
    if knotseq and knotseq not in ("∅", "?"):
        for cm in re.finditer(
                r"(EE|LL|BL|SP|TF|S|L|E|X)(\{[^}]*\})?(\d*)([zsu]?)",
                knotseq):
            kt, ax, num, dr = cm.groups()
            f["knots"].append(kt)
            if ax:
                f["axis"].append(ax.strip("{}"))
            if num:
                f["turns"].append((kt, int(num)))
            if dr:
                f["dirs"].append((kt, dr))
    # colors: split compound on : - /
    if colorfield and colorfield != "?":
        segs = re.split(r"[:\-/]", colorfield)
        f["colors"] = [s for s in segs if s]
        if len(segs) > 1:
            f["compound"] = colorfield
    elif colorfield == "?":
        f["colors"] = ["?"]
    return f

def features_of(f):
    """Flatten parsed dict into atomic feature strings."""
    out = []
    out.append("level:" + f["level"])
    if f["is_header"]:
        out.append("struct:header")
    if f["parent"] is not None:
        out.append("struct:subsidiary")
    else:
        if not f["is_header"]:
            out.append("struct:pendant")
    for c in f["colors"]:
        out.append("color:" + c)
    if f["compound"]:
        out.append("compound:" + f["compound"])
    for k in f["knots"]:
        out.append("knot:" + k)
    for kt, dr in f["dirs"]:
        out.append("dir:" + dr)
        out.append("dir:" + kt + dr)   # type-specific, e.g. dir:Eu
    for kt, n in f["turns"]:
        out.append("turns:" + kt + str(n))
    for ax in f["axis"]:
        out.append("axis:" + ax)
    if f["empty"]:
        out.append("struct:empty")
    if f["missing"]:
        out.append("struct:missing")
    if f["broken"]:
        out.append("struct:broken")
    for fl in f["flags"]:
        out.append("flag:" + fl.split(":")[0])
    return sorted(set(out))

# ---------- load ----------
cords = []   # (khipu, ordinal_raw, fdict, featlist)
with open(IN_CSV, encoding="utf-8") as fh:
    rdr = csv.DictReader(fh)
    for row in rdr:
        fd = parse_line(row["TRANSCRIPTION"])
        feats = features_of(fd)
        cords.append({"khipu": row["KHIPU_ID"], "cord_ord": row["CORD_ORDINAL"],
                      "fd": fd, "feats": feats})

# ---------- feature IDs (stable, deterministic) ----------
all_feats = sorted({ft for c in cords for ft in c["feats"]},
                   key=lambda s: (s.split(":")[0], s))
fid = {f: i + 1 for i, f in enumerate(all_feats)}

def ftype(f):
    return f.split(":")[0]

DESCR = {
    "color": "cord color code (Ascher notation)",
    "compound": "multi-color cord, operator preserved",
    "knot": "knot type present on cord",
    "dir": "anomalous twist direction (s/u; z omitted as default)",
    "turns": "turn/count number on L/SP/BL/S knot",
    "axis": "axis orientation on spiral knot",
    "level": "hierarchy level (H=primary cord)",
    "struct": "structural state (empty/missing/broken/subsidiary/pendant/header)",
    "flag": "physical flag (rev/loop/mended/thr/sig/...)",
}
with open(os.path.join(OUT, "feature_ids.csv"), "w", newline="",
          encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["id", "feature_type", "feature_value", "description"])
    for f in all_feats:
        t, v = f.split(":", 1)
        w.writerow([fid[f], t, v, DESCR.get(t, "")])

# ---------- khipu_features.csv ----------
with open(os.path.join(OUT, "khipu_features.csv"), "w", newline="",
          encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["khipu_id", "cord_ord", "level", "parent_ord",
                "feature_ids", "feature_names"])
    for c in cords:
        ids = sorted(fid[x] for x in c["feats"])
        w.writerow([c["khipu"], c["cord_ord"], c["fd"]["level"],
                    c["fd"]["parent"] if c["fd"]["parent"] is not None else "",
                    ";".join(map(str, ids)), ";".join(c["feats"])])

# ---------- within-cord co-occurrence + PMI ----------
N = len(cords)
fc = Counter()
pair = Counter()
for c in cords:
    fs = c["feats"]
    for x in fs:
        fc[x] += 1
    for i in range(len(fs)):
        for j in range(i + 1, len(fs)):
            a, b = sorted([fs[i], fs[j]])
            pair[(a, b)] += 1

def pmi(c_xy, c_x, c_y, n):
    return math.log2((c_xy / n) / ((c_x / n) * (c_y / n)))

rows = []
for (a, b), cxy in pair.items():
    if cxy < 3:      # singletons/doubletons inflate PMI; require >=3
        continue
    v = pmi(cxy, fc[a], fc[b], N)
    rows.append((v, cxy, a, b, fc[a], fc[b]))
rows.sort(reverse=True)
with open(os.path.join(OUT, "within_cord_pmi.csv"), "w", newline="",
          encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["pmi", "cooccur", "feat_a", "id_a", "feat_b", "id_b",
                "count_a", "count_b"])
    for v, cxy, a, b, ca, cb in rows[:200]:
        w.writerow([round(v, 3), cxy, a, fid[a], b, fid[b], ca, cb])

# ---------- sequential bigrams ----------
# sequence A: L1 cords in physical ordinal order (headers first)
# sequence B: depth-first (each L1 cord followed by its subsidiaries)
def build_sequences():
    by_khipu = defaultdict(list)
    for c in cords:
        by_khipu[c["khipu"]].append(c)
    seqs = {}
    for k, cs in by_khipu.items():
        l1 = sorted([c for c in cs if c["fd"]["level"] == "L1"
                     and c["fd"]["ordinal"] is not None],
                    key=lambda c: c["fd"]["ordinal"])
        hdr = [c for c in cs if c["fd"]["is_header"]]
        subs = defaultdict(list)
        for c in cs:
            if c["fd"]["parent"] is not None:
                subs[c["fd"]["parent"]].append(c)
        for v in subs.values():
            v.sort(key=lambda c: (c["cord_ord"]))
        seq_a = hdr + l1
        seq_b = []
        for c in hdr + l1:
            seq_b.append(c)
            if c["fd"]["ordinal"] in subs:
                seq_b.extend(subs[c["fd"]["ordinal"]])
        seqs[k] = {"L1": seq_a, "depthfirst": seq_b}
    return seqs

seqs = build_sequences()
bigram = Counter()   # (fa, fb) ordered, feature-level across adjacent cords
for k, s in seqs.items():
    for seq in (s["L1"], s["depthfirst"]):
        for i in range(len(seq) - 1):
            for fa in seq[i]["feats"]:
                for fb in seq[i + 1]["feats"]:
                    bigram[(fa, fb)] += 1

tot_bi = sum(bigram.values())
brows = []
for (a, b), cxy in bigram.items():
    v = pmi(cxy, fc[a], fc[b], tot_bi)
    brows.append((cxy, v, a, b))
brows.sort(key=lambda r: (-r[0], -r[1]))
with open(os.path.join(OUT, "sequential_bigrams.csv"), "w", newline="",
          encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["count", "pmi", "feat_from", "id_from", "feat_to", "id_to"])
    for cxy, v, a, b in brows[:200]:
        w.writerow([cxy, round(v, 3), a, fid[a], b, fid[b]])

# ---------- hierarchical pairs (parent -> subsidiary, feature level) ----------
hier = Counter()
for c in cords:
    p = c["fd"]["parent"]
    if p is None:
        continue
    # find parent cord: same khipu, L1, ordinal == p
    for pc in cords:
        if (pc["khipu"] == c["khipu"] and pc["fd"]["level"] == "L1"
                and pc["fd"]["ordinal"] == p):
            for fa in pc["feats"]:
                for fb in c["feats"]:
                    hier[(fa, fb)] += 1
            break

tot_h = sum(hier.values()) or 1
hrows = []
for (a, b), cxy in hier.items():
    v = pmi(cxy, fc[a], fc[b], tot_h)
    hrows.append((cxy, v, a, b))
hrows.sort(key=lambda r: (-r[0], -r[1]))
with open(os.path.join(OUT, "hierarchical_pairs.csv"), "w", newline="",
          encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["count", "pmi", "parent_feat", "parent_id",
                "subsidiary_feat", "subsidiary_id"])
    for cxy, v, a, b in hrows[:200]:
        w.writerow([cxy, round(v, 3), a, fid[a], b, fid[b]])

# ---------- sanity: promiscuity, restriction, complementary distribution ----------
partners = defaultdict(set)
for (a, b) in pair:
    partners[a].add(b)
    partners[b].add(a)
prom = sorted(((f, len(partners[f]), fc[f]) for f in all_feats),
              key=lambda r: -r[1])

# complementary distribution: pairs that never co-occur but each is common
# (check within same feature type)
by_type = defaultdict(list)
for f in all_feats:
    by_type[ftype(f)].append(f)
complement = []
pairset = set(pair)
for t, fs in by_type.items():
    for i in range(len(fs)):
        for j in range(i + 1, len(fs)):
            a, b = sorted([fs[i], fs[j]])
            if (a, b) not in pairset and fc[a] >= 10 and fc[b] >= 10:
                complement.append((fc[a] + fc[b], a, b, fc[a], fc[b]))
complement.sort(reverse=True)

with open(os.path.join(OUT, "sanity_report.md"), "w",
          encoding="utf-8") as fh:
    fh.write("# Khipu Feature Database — Sanity Report\n\n")
    fh.write(f"Cords parsed: {N}\n\n")
    fh.write(f"Feature vocabulary size: {len(all_feats)}\n\n")
    fh.write("## Most promiscuous features (combine with many others)\n\n")
    fh.write("| feature | id | distinct partners | cord count |\n|---|---|---|---|\n")
    for f, np_, c_ in prom[:20]:
        fh.write(f"| {f} | {fid[f]} | {np_} | {c_} |\n")
    fh.write("\n## Most restricted features (>=5 cords, few partners)\n\n")
    fh.write("| feature | id | distinct partners | cord count |\n|---|---|---|---|\n")
    restr = sorted([r for r in prom if r[2] >= 5], key=lambda r: r[1])[:20]
    for f, np_, c_ in restr:
        fh.write(f"| {f} | {fid[f]} | {np_} | {c_} |\n")
    fh.write("\n## Complementary distribution candidates (never co-occur, each >=10 cords)\n\n")
    fh.write("| feature a | feature b | count a | count b |\n|---|---|---|---|\n")
    for tot, a, b, ca, cb in complement[:30]:
        fh.write(f"| {a} | {b} | {ca} | {cb} |\n")
    if not complement:
        fh.write("(none)\n")

print(f"cords={N} features={len(all_feats)} "
      f"pairs={len(pair)} bigrams={len(bigram)} hier={len(hier)}")
print("top promiscuous:", [(f, n) for f, n, _ in prom[:5]])
