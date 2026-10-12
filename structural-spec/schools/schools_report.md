# Schools of Khipu Makers — Clustering Report

**Date:** 2026-10-12
**Method:** K-means (k=12) on 619 khipu using habit features only — no semantics.
**Features:** Top palette fractions (32 colors), knot type distribution, twist direction,
max hierarchy level, cord count, white fraction, self-transition rate (log-vs-tabular signal).

## The 12 Schools

| School | n | Dominant palette | Top regions | Self-rate (med) | Size (med) | Character |
|---|---|---|---|---|---|---|
| SCH01 | 114 | W/AB/MB | Pachacamac, Incahuasi | 0.18 | 46 | Large tabular school, central coast |
| SCH04 | 80 | W/AB | Chachapoyas, Ica | 0.41 | 65 | Mixed format, northern + south |
| SCH07 | 72 | AB/W/MB | Incahuasi, Puruchuco | 0.39 | 38 | Incahuasi office group |
| SCH03 | 66 | W/LB | Pachacamac, Ica | 0.75 | 31 | Log-like, white/light-brown |
| SCH11 | 59 | W (55/59) | Pachacamac, Incahuasi | 0.73 | 51 | The white school |
| SCH02 | 59 | B/YB/W | mostly unknown prov. | 0.55 | 28 | Small, dark palette |
| SCH05 | 57 | AB/B | Incahuasi, Ica | 0.83 | 70 | Very log-like, Incahuasi |
| SCH12 | 49 | AB/MB/LK | Nazca, Incahuasi | 0.80 | 74 | Log-like, southern |
| SCH08 | 22 | W (22/22) | Ica, Tambo Colorado | 1.00 | 19 | All-white khipu |
| SCH09 | 15 | AB/MB | "Inka, Late Horizon" | 0.00 | 10 | Fully tabular, Late Horizon, small |
| SCH10 | 13 | AB/MB/W | Chachapoyas, Nazca | 0.69 | 589 | The monsters (large khipu) |
| SCH06 | 13 | KB/W/NB | "Inka, Late Horizon" | 1.00 | 57 | Late Horizon, dark palette |

## Validation: where our analyzed khipu landed

- **SCH02** caught the all-U group: 1000029, 1000345, 1000361, plus 1000368 and 1000034.
  The features detected real structural similarity (dark palettes, similar self-rates).
  Note: 1000034 (tabular, self=0.28) landed here on palette, not structure — clustering
  weighted color over layout in this case.
- **SCH10** caught the three largest: 1000183, 1000103 (both journals), 1000096 (categorical matrix).
  Size dominated — they're different types but similar scale. This is a limitation:
  the "monster" school is about scale, not shared habit.
- **SCH04** caught the tabular forms: 1000344, 1000396, plus allocation candidates 1000338, 1000009.
- **SCH11** (white school): 1000514, 1000608.
- **SCH12**: 1000331 (code), 1000522 (checklist) — different formats, similar AB/MB palette.
- **SCH03**: 1000144 (Pachacamac).

## Regional signals (weak but present)

- Pachacamac concentrates in SCH01, SCH03, SCH11 (central coast tabular + white schools).
- Incahuasi concentrates in SCH01, SCH05, SCH07, SCH12 (southern log-like schools).
- Chachapoyas splits between SCH04 and SCH10.
- Two distinct "Inka, Late Horizon" groups: SCH09 (AB/MB, tabular, small) vs SCH06 (KB dark, log-like).
  Same period label, different habits — possibly two contemporary offices.

## Limitations

1. **Size dominates.** SCH10 is "big khipu" not a habit school. A size-normalized run would separate
   1000183/1000103 (journals) from 1000096 (categorical).
2. **Palette vs structure tradeoff.** K-means weighted palette heavily; 1000034 (tabular) landed
   with logs in SCH02 on color alone.
3. **Unknown provenance** (large fraction) limits regional validation.
4. **k=12 is arbitrary.** Hierarchical structure (schools > offices > hands) needs a second pass.

## Files

- `schools/khipu_features.json` — per-khipu feature vectors (619 khipu)
- `schools/school_clusters.json` — SCH01–SCH12 membership
- `schools/extract_features.py`, `schools/kmeans_schools.py` — pipeline
