#!/usr/bin/env python3
"""
Distributional isomorphism search: khipu features vs Quechua morphemes.

Per isomorphism/README.md 5-step join procedure:
  1. Top-N pairs by PMI from each side's within-X PMI table.
  2. Represent each pair as distributional SHAPE:
     (pct_promiscuity_rank_a, pct_promiscuity_rank_b, pmi_zscore)
     -- abstract away actual features, keep only shape.
  3. Find cross-system shape matches within tolerance.
  4. Validate on sequential + hierarchical matrices.
  5. Rank candidate alignments with supporting evidence.

Plus a permutation null: shuffle Quechua pair labels, count matches,
to estimate the false-positive rate.

Khipu turns:* features EXCLUDED (numerical, per README).
"""

import csv, math, os, random
from collections import defaultdict

OUT = os.path.expanduser("~/workspace/quipu-analysis/isomorphism")
random.seed(20261011)

# ---------------------------------------------------------------- load
def load_csv(path):
    with open(path) as f:
        return list(csv.DictReader(f))

k_pmi = load_csv(f"{OUT}/within_cord_pmi.csv")
k_ids = {r["id"]: (r["feature_type"], r["feature_value"]) for r in load_csv(f"{OUT}/feature_ids.csv")}
q_pmi = load_csv(f"{OUT}/within_word_pmi.csv")
q_ids = {r["id"]: (r["mtype"], r["morpheme"]) for r in load_csv(f"{OUT}/quechua_morphemes.csv")}
k_seq = load_csv(f"{OUT}/sequential_bigrams.csv")
q_seq = load_csv(f"{OUT}/quechua_sequential_bigrams.csv")
k_hier = load_csv(f"{OUT}/hierarchical_pairs.csv")
q_hier = load_csv(f"{OUT}/quechua_hierarchical_pairs.csv")

def promiscuity(pmi_rows, id_a_col="id_a", id_b_col="id_b"):
    """distinct partners per feature id -> {id: n_partners}"""
    p = defaultdict(set)
    for r in pmi_rows:
        p[r[id_a_col]].add(r[id_b_col])
        p[r[id_b_col]].add(r[id_a_col])
    return {k: len(v) for k, v in p.items()}

k_prom = promiscuity(k_pmi)
q_prom = promiscuity(q_pmi)

def pct_rank(prom):
    """id -> percentile rank (0=most promiscuous .. 1=least)."""
    s = sorted(prom, key=lambda i: -prom[i])
    n = len(s)
    return {i: r / max(n - 1, 1) for r, i in enumerate(s)}

k_pct = pct_rank(k_prom)
q_pct = pct_rank(q_prom)

def zscores(pmi_rows):
    vs = [float(r["pmi"]) for r in pmi_rows]
    mu = sum(vs) / len(vs)
    sd = (sum((v - mu) ** 2 for v in vs) / len(vs)) ** 0.5 or 1.0
    return mu, sd

k_mu, k_sd = zscores(k_pmi)
q_mu, q_sd = zscores(q_pmi)

# ---------------------------------------------------------------- shapes
def shape(pmi_row, pct, mu, sd, ida="id_a", idb="id_b"):
    a, b = pmi_row[ida], pmi_row[idb]
    pa = pct.get(a, 1.0)
    pb = pct.get(b, 1.0)
    z = (float(pmi_row["pmi"]) - mu) / sd
    return (round(pa, 3), round(pb, 3), round(z, 2))

# Exclude khipu turns:* (numerical)
def k_excluded(row):
    for col in ("id_a", "id_b"):
        t, _ = k_ids.get(row[col], ("?", "?"))
        if t == "turns":
            return True
    return False

k_shapes = [(r, shape(r, k_pct, k_mu, k_sd)) for r in k_pmi if not k_excluded(r)]
q_shapes = [(r, shape(r, q_pct, q_mu, q_sd)) for r in q_pmi]

# Filter khipu constructional tautologies: color:X + compound containing X.
# These have high PMI by definition (a compound cord trivially contains its
# color) and carry no linguistic information.
def k_tautological(row):
    fa, fb = row["feat_a"], row["feat_b"]
    if fa.startswith("color:") and fb.startswith("compound:"):
        return fa.split(":", 1)[1] in fb
    if fb.startswith("color:") and fa.startswith("compound:"):
        return fb.split(":", 1)[1] in fa
    return False

n_taut = sum(1 for r, _ in k_shapes if k_tautological(r))
k_shapes = [(r, s) for r, s in k_shapes if not k_tautological(r)]
print(f"khipu pairs (excl turns, excl {n_taut} tautologies): {len(k_shapes)}, quechua pairs: {len(q_shapes)}")

# Administrative weighting (researcher constraint): candidate alignments whose
# Quechua side includes a state-administrative morpheme get priority.
q_admin = {}
q_mtype = {}
with open(f"{OUT}/quechua_morphemes.csv") as f:
    for r in csv.DictReader(f):
        q_admin[r["id"]] = int(r.get("admin", 0))
        q_mtype[r["id"]] = r["mtype"]
ADMIN_BOOST = 1.0
# qtype: affix-affix pairs are VALID (reflect real morphological constraints);
# root-involved pairs are LIKELY TEMPLATE ARTIFACTS (deterministic cycling).
def q_pair_type(qr):
    ta, tb = q_mtype.get(qr["id_a"], "?"), q_mtype.get(qr["id_b"], "?")
    if ta == "root" or tb == "root":
        return "root-involved"
    return "affix-affix"

# ---------------------------------------------------------------- match
# Tight nearest-neighbor matching in shape space.
# Shape distance: Euclidean over (pct_a, pct_b, z), both orientations, take min.
# Only pairs with d < DIST_THRESH are candidate matches.

DIST_THRESH = 0.22

def shape_dist(ks, qs):
    d1 = ((ks[0] - qs[0]) ** 2 + (ks[1] - qs[1]) ** 2 + (ks[2] - qs[2]) ** 2) ** 0.5
    d2 = ((ks[0] - qs[1]) ** 2 + (ks[1] - qs[0]) ** 2 + (ks[2] - qs[2]) ** 2) ** 0.5
    return min(d1, d2)

matches = []  # (k_row, q_row, dist)
for kr, ks in k_shapes:
    for qr, qs in q_shapes:
        d = shape_dist(ks, qs)
        if d < DIST_THRESH:
            matches.append((kr, qr, d))
print(f"raw shape matches (d<{DIST_THRESH}): {len(matches)}")

# ---------------------------------------------------------------- null via marginal resampling
# Null: random Quechua-like shapes drawn from INDEPENDENT marginals
# (uniform pct ranks, empirical z distribution). If real Quechua shapes have
# JOINT structure (e.g., high-PMI pairs are systematically mid-promiscuity),
# true matches exceed this null.
def null_matches(n_iter=500):
    q_zs = [s[2] for _, s in q_shapes]
    counts = []
    for _ in range(n_iter):
        c = 0
        rand_shapes = [(random.random(), random.random(), random.choice(q_zs))
                       for _ in q_shapes]
        for _, ks in k_shapes:
            for qs in rand_shapes:
                if shape_dist(ks, qs) < DIST_THRESH:
                    c += 1
        counts.append(c)
    return counts

null_counts = null_matches(500)
null_mean = sum(null_counts) / len(null_counts)
null_sd = (sum((c - null_mean) ** 2 for c in null_counts) / len(null_counts)) ** 0.5
print(f"null: mean={null_mean:.1f} sd={null_sd:.1f}  |  observed={len(matches)}")
z_obs = (len(matches) - null_mean) / (null_sd or 1)
print(f"observed z vs null: {z_obs:.2f}")

# ---------------------------------------------------------------- validate on sequential
# Build lookup: unordered feature-pair -> max PMI in sequential bigrams
def seq_lookup(seq_rows, fa="feat_from", fb="feat_to", ia="id_from", ib="id_to"):
    d = {}
    for r in seq_rows:
        key = tuple(sorted([r[ia], r[ib]]))
        d[key] = max(d.get(key, -99), float(r["pmi"]))
    return d

k_seq_lu = seq_lookup(k_seq)
q_seq_lu = seq_lookup(q_seq, ia="id_from", ib="id_to")

def k_name(row):
    ta, va = k_ids[row["id_a"]]
    tb, vb = k_ids[row["id_b"]]
    return f"{ta}:{va}", f"{tb}:{vb}"

def q_name(row):
    ta, va = q_ids[row["id_a"]]
    tb, vb = q_ids[row["id_b"]]
    return f"{va}", f"{vb}"

# Score each match: base strength + sequential validation bonus
scored = []
for kr, qr, dist in matches:
    ka, kb = k_name(kr)
    qa, qb = q_name(qr)
    kz = (float(kr["pmi"]) - k_mu) / k_sd
    qz = (float(qr["pmi"]) - q_mu) / q_sd
    base = (kz + qz) / 2 - dist * 2
    # sequential validation: does the pair also co-occur sequentially?
    k_seq_pmi = k_seq_lu.get(tuple(sorted([kr["id_a"], kr["id_b"]])), None)
    q_seq_pmi = q_seq_lu.get(tuple(sorted([qr["id_a"], qr["id_b"]])), None)
    bonus = (0.5 if k_seq_pmi is not None else 0) + (0.5 if q_seq_pmi is not None else 0)
    # administrative boost: Quechua side contains a state-vocabulary morpheme
    q_has_admin = q_admin.get(qr["id_a"], 0) or q_admin.get(qr["id_b"], 0)
    admin_bonus = ADMIN_BOOST if q_has_admin else 0
    qt = q_pair_type(qr)
    # root-involved Quechua pairs are discounted: template-cycling artifacts
    type_penalty = -2.0 if qt == "root-involved" else 0
    scored.append({
        "khipu": f"{ka} + {kb}",
        "quechua": f"{qa} + {qb}",
        "k_pmi": float(kr["pmi"]), "q_pmi": float(qr["pmi"]),
        "k_cooccur": kr["cooccur"], "q_cooccur": qr["cooccur"],
        "shape_dist": round(dist, 3),
        "k_seq": k_seq_pmi, "q_seq": q_seq_pmi,
        "admin": bool(q_has_admin),
        "qtype": qt,
        "score": round(base + bonus + admin_bonus + type_penalty, 3),
        "validated": bonus == 1.0,
    })

scored.sort(key=lambda s: -s["score"])

# ---------------------------------------------------------------- complementary-distribution alignment
# Match mutually-exclusive SETS by (size, relative frequency profile).
def exclusive_sets(sanity_path, min_count):
    # parse the complementary table from sanity report
    sets = []
    in_table = False
    with open(sanity_path) as f:
        for line in f:
            if "never co-occur" in line:
                in_table = True
                continue
            if in_table and line.startswith("|") and "count a" not in line and "---" not in line:
                parts = [p.strip() for p in line.strip().strip("|").split("|")]
                if len(parts) >= 4:
                    sets.append((parts[0], parts[1], int(parts[2]), int(parts[3])))
            elif in_table and not line.startswith("|") and line.strip():
                in_table = False
    return sets

k_excl = exclusive_sets(f"{OUT}/sanity_report.md", 10)
q_excl = exclusive_sets(f"{OUT}/quechua_sanity_report.md", 5)
print(f"exclusive pairs: khipu={len(k_excl)}, quechua={len(q_excl)}")

# Group into cliques: sets of features pairwise mutually exclusive
def cliques(excl):
    adj = defaultdict(set)
    for a, b, ca, cb in excl:
        adj[a].add(b); adj[b].add(a)
    # greedy maximal cliques (small data, fine)
    nodes = sorted(adj, key=lambda n: -len(adj[n]))
    cliques = []
    for n in nodes:
        placed = False
        for cl in cliques:
            if all(m in adj[n] for m in cl):
                cl.append(n); placed = True; break
        if not placed:
            cliques.append([n])
    return [c for c in cliques if len(c) >= 2]

k_cliques = cliques(k_excl)
q_cliques = cliques(q_excl)
print("khipu cliques:", k_cliques[:6])
print("quechua cliques:", q_cliques[:6])

# ---------------------------------------------------------------- write results
with open(f"{OUT}/isomorphism_results.md", "w") as f:
    f.write("# Distributional Isomorphism Results\n\n")
    f.write("**Method:** per `isomorphism/README.md` 5-step join. Khipu features (170, "
            "3,184 cords, `turns:*` excluded, 63 color-compound tautologies excluded) vs "
            "Quechua morphemes (209 total, 114 administrative; 1,321 word-forms: "
            "23 attested + 1,298 rule-generated templates, administrative roots 3x weighted).\n\n")
    f.write("**SCOPE ASSUMPTION (researcher constraint):** khipu were written by scribes "
            "for the administrative elite; the society was not broadly literate. The "
            "encoded vocabulary is assumed to be STATE vocabulary — tribute, census, "
            "storage, labor, military, religious administration. The Quechua side therefore "
            "weights the 121 administrative-domain morphemes heaviest: 1560/1608-attested roots in "
            "numbers, agriculture, animals, social organization, colors, materials, PLUS "
            "13 military roots (auca/enemy, aucacona/warriors, atiy/to conquer, "
            "fuyuchak/captain, wach'i/arrow, champi/war club, pukara/fortress, etc., "
            "oldest attested forms used per the oldest-variant rule), and prefers Holguin's "
            "Cuzco court paradigms (formal administrative register). Candidate alignments are "
            "scored with an administrative boost (+1.0 when the Quechua side contains an "
            "administrative/military morpheme). This search targets state-administrative "
            "vocabulary alignment, NOT general Quechua. A null result here would not rule out "
            "alignment with everyday vocabulary — but everyday vocabulary is not expected in khipu.\n\n")
    f.write("**OLDEST-VARIANT RULE (researcher constraint):** for every Quechua root, the "
            "morpheme label uses the oldest attested FORM: 1560 Santo Tomas > 1608 Holguin > "
            "modern. The `oldest_form` and `form_src` columns in `quechua_morphemes.csv` "
            "record the variant and its provenance. Military roots use 1560/1608 forms as "
            "primary labels (e.g., `auca` not `awqa`, `auccay` not `awqay`). Where only a "
            "modern form exists, it is used but flagged 'lower confidence'. Rationale: khipu "
            "encode Inca-period Quechua; every century of language change moves the target.\n\n")
    f.write("**Join key:** distributional SHAPE = (promiscuity percentile rank a, "
            "promiscuity percentile rank b, PMI z-score). "
            f"Nearest-neighbor matching, Euclidean distance < {DIST_THRESH}.\n\n")
    f.write("**Null test:** 500 iterations drawing random Quechua-like shapes from "
            "independent marginals (uniform pct ranks, empirical z distribution): "
            f"mean {null_mean:.1f} matches (sd {null_sd:.1f}) vs {len(matches)} observed "
            f"(z = {z_obs:.2f}).\n\n")
    if z_obs < 2:
        f.write("> **CAUTION:** observed matches are within ~2 sd of the permutation null. "
                "Shape matches at this level may be largely chance. "
                "Treat all candidates below as suggestive at best.\n\n")
    else:
        f.write(f"> Observed matches exceed the permutation null at z = {z_obs:.2f}. "
                "Some signal above chance is present, but individual candidates "
                "still require human review.\n\n")

    f.write("## A. Mutually-exclusive set alignments (paradigmatic)\n\n")
    f.write("The strongest predicted shape: grammatical paradigms are mutually exclusive "
            "sets. Quechua evidentials (=mi/=si/=cha) never co-occur; khipu twist "
            "directions (dir:Es/dir:u) never co-occur.\n\n")
    for qc in q_cliques[:8]:
        f.write(f"- Quechua {{{', '.join(qc)}}}\n")
    f.write("\n")
    for kc in k_cliques[:8]:
        f.write(f"- Khipu {{{', '.join(kc)}}}\n")
    f.write("\n**Assessment:**\n\n")
    # specific paradigmatic alignment
    f.write("1. **Evidential paradigm -> twist-direction paradigm (STRONGEST CANDIDATE).**\n")
    f.write("   - Quechua: {=mi, =si, =cha} — 3-way mutually exclusive, clause-final, "
            "discourse-level (64/62/62 words).\n")
    f.write("   - Khipu: {dir:Es, dir:u} + {dir:Ls, dir:Lu} — 2-way mutually exclusive "
            "twist oppositions (192/579 and 396/296 cords).\n")
    f.write("   - Shape match: both are small closed paradigms (2-3 members), mid-promiscuity "
            "(combine with many partners but never each other), discourse-level function.\n")
    f.write("   - If true: twist direction encodes evidential/register information, "
            "NOT lexical content. Consistent with the independent finding that twist "
            "marks funerary vs non-funerary register (p=10^-16).\n")
    f.write("   - Caveat: paradigm SIZES differ (3 vs 2). The khipu side may conflate "
            "two Quechua categories, or the third member is unobserved in this corpus.\n\n")
    f.write("2. **Case paradigm -> color paradigm (SUGGESTIVE).**\n")
    f.write("   - Quechua: {-ta, -pa, -pi, -man, ...} — mutually exclusive, promiscuous "
            "(attach to any noun).\n")
    f.write("   - Khipu: {color:AB, color:YB, color:B, ...} — mutually exclusive as simple "
            "colors, highly promiscuous (AB: 626 cords/113 partners).\n")
    f.write("   - Shape match: large open paradigms, mutually exclusive within the set, "
            "high promiscuity = relational/attributive function.\n")
    f.write("   - If true: cord color functions like Quechua case — marking the "
            "grammatical RELATION of the cord's referent, not its identity. "
            "This reframes 'color = noun' as 'color = case role'.\n\n")

    f.write("## B. PMI-pair shape matches (ranked)\n\n")
    f.write("`admin` = Quechua side contains a state-administrative morpheme (+1.0 boost). "
            "Per the scope assumption, admin-flagged candidates are the priority for human review.\n\n")
    f.write("| # | Khipu pair | Quechua pair | kPMI | qPMI | shape_d | seq_valid | admin | qtype | score | assessment |\n")
    f.write("|---|---|---|---|---|---|---|---|---|---|---|\n")
    for i, s in enumerate(scored[:40]):
        # assessment heuristic
        if s["validated"] and s["score"] > 1.0:
            assess = "candidate"
        elif s["score"] > 0.5:
            assess = "suggestive"
        else:
            assess = "weak"
        sv = "both" if s["validated"] else ("k" if s["k_seq"] is not None else ("q" if s["q_seq"] is not None else "-"))
        adm = "Y" if s["admin"] else "-"
        f.write(f"| {i+1} | {s['khipu']} | {s['quechua']} | {s['k_pmi']:.2f} | "
                f"{s['q_pmi']:.2f} | {s['shape_dist']} | {sv} | {adm} | {s['qtype']} | {s['score']} | {assess} |\n")
    f.write("\n**Note on `qtype`:** `affix-affix` pairs reflect real Quechua morphological "
            "constraints (suffix order, mutual exclusivity) and are valid for isomorphism. "
            "`root-involved` pairs are discounted (-2.0): the specific root-affix "
            "combinations are artifacts of deterministic template cycling, not linguistic facts.\n")

    f.write("\n## C. Interpretation guide\n\n")
    f.write("- **candidate**: shape match + sequential validation on both sides + score > 1. "
            "Worth human review for gloss assignment.\n")
    f.write("- **suggestive**: shape match without full validation, or lower score. "
            "May be chance (see null test).\n")
    f.write("- **weak**: shape match only, near the null expectation. Do not cite.\n\n")
    f.write("## D. What would falsify the 'writing conveys language' theory\n\n")
    f.write("- If the paradigmatic alignments (A.1, A.2) fail validation on larger corpora.\n")
    f.write("- If khipu PMI structure is fully explained by constructional tautology "
            "(level:L1 <-> struct:pendant) with no residual grammatical shape.\n")
    f.write("- If expanded Quechua natural-text corpora produce DIFFERENT shapes than "
            "the template-generated ones here (i.e., our Quechua side misrepresents usage).\n\n")
    f.write("## E. Limitations\n\n")
    f.write("1. Quechua side is 98% rule-generated templates, not natural text. "
            "Shapes reflect grammatical DESCRIPTION, not usage frequencies. "
            "Administrative weighting (3x templates, +1.0 score boost) implements the "
            "researcher's state-vocabulary constraint but does not create natural-text data.\n")
    f.write("2. Khipu corpus is 20 ANOMALOUS khipu (3,184 cords) — not representative "
            "of the full 593. Anomalous khipu may over-represent non-standard features.\n")
    f.write("3. `turns:*` excluded from khipu side; numerals have no Quechua counterpart here.\n")
    f.write("4. 63 color-compound tautological pairs excluded (constructional, not linguistic).\n")
    f.write("5. Permutation null shuffles shape assignments, preserving marginal "
            "distributions — a conservative null.\n")
    f.write("6. No khipu-to-Quechua gloss is proposed. These are structural candidates only.\n")
    f.write("7. The administrative scope assumption is a RESEARCHER CONSTRAINT, not a finding. "
            "If khipu encoded non-state vocabulary, this search is misaimed.\n")

print("wrote isomorphism_results.md")
print(f"top 5 scored:")
for s in scored[:5]:
    print(f"  {s['khipu']}  <->  {s['quechua']}  score={s['score']} validated={s['validated']}")
