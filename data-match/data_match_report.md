# Same Data, Different Templates — Report

Khipu with templates: 200; fingerprinted: 200; clustered (n_var>=10): 165; data clusters (k=6): 6

## Data cluster profiles

| cluster | n | med_value | iqr | max | zero_frac | marker_frac | entropy |
|---|---|---|---|---|---|---|---|
| 1 | 7 | 1 | 0 | 1 | 0.89 | 0.00 | 0.00 |
| 2 | 78 | 3 | 4 | 33 | 0.31 | 0.00 | 0.95 |
| 3 | 12 | 344 | 544 | 8376 | 0.23 | 0.00 | 1.55 |
| 4 | 15 | 8 | 27 | 4657 | 0.37 | 0.01 | 1.52 |
| 5 | 3 | 33 | 44 | 232 | 0.53 | 0.41 | 0.97 |
| 6 | 50 | 20 | 32 | 202 | 0.30 | 0.05 | 1.19 |

## Data cluster vs document-type cluster

```
doc_cluster   census_format_paired  deep_hierarchical_grouped  deep_sparse_mixed  large_value_flat
data_cluster                                                                                      
1                                3                          0                  4                 0
2                               36                          6                 36                 0
3                                0                          6                  3                 3
4                                2                          5                  8                 0
5                                0                          1                  2                 0
6                               11                         19                 18                 2
```

## Data cluster vs template: do data clusters span templates?

- data cluster 1: 7 khipu across **7 distinct templates** (members: 1000065, 1000474, 1000571, 1000575, 1000649, 1000654, 1000659)
- data cluster 2: 78 khipu across **78 distinct templates** (members: 1000014, 1000029, 1000033, 1000034, 1000039, 1000042, 1000052, 1000085, 1000099, 1000103, 1000108, 1000121...)
- data cluster 3: 12 khipu across **12 distinct templates** (members: 1000032, 1000118, 1000124, 1000144, 1000231, 1000265, 1000280, 1000493, 1000499, 1000609, 1000611, 1000616)
- data cluster 4: 15 khipu across **15 distinct templates** (members: 1000096, 1000120, 1000262, 1000263, 1000310, 1000314, 1000320, 1000336, 1000494, 1000504, 1000508, 1000509...)
- data cluster 5: 3 khipu across **3 distinct templates** (members: 1000279, 1000344, 1000513)
- data cluster 6: 50 khipu across **50 distinct templates** (members: 1000040, 1000053, 1000057, 1000063, 1000089, 1000094, 1000097, 1000110, 1000115, 1000131, 1000137, 1000140...)

## Data cluster vs region/provenance

- cluster 1: Ica=2, unknown=2, Armatambo, Huaca San Pedro=2, Huaca San Pedro, Armatambo=1
- cluster 2: unknown=36, Pachacamac=4, Huaquerones/Puruchuco=4, Santa=4
- cluster 3: unknown=5, Incahuasi=3, Ica=1, Ocucaje=1
- cluster 4: Pachacamac/"Central Coast, Peru"=3, Pachacamac=2, Lluta Valley=1, unknown/Puruchuco=1
- cluster 5: Mollepampa/"Inka, Playa Miller"=1, unknown=1, Pachacamac/"Central Coast, Peru"=1
- cluster 6: unknown=15, Pachacamac=6, Nazca=4, Between Ica and Pisco=3

## 22/23/32/33/34 in variable positions

68/165 khipu have marker values (22/23/32/33/34) in variable positions.

| khipu | data_cluster | template | marker_frac | top5 | doc_cluster |
|---|---|---|---|---|---|
| 1000279 | 5 | T086 | 0.50 | 22:1;15:1 | deep_hierarchical_grouped |
| 1000344 | 5 | T107 | 0.41 | 22:22;33:18;12:16;42:12;32:11 | deep_sparse_mixed |
| 1000513 | 5 | T149 | 0.25 | 215:1;232:1;225:1;30:1;199:1 | deep_sparse_mixed |
| 1000510 | 6 | T148 | 0.22 | 8:8;33:7;6:7;4:6;22:6 | deep_sparse_mixed |
| 1000089 | 6 | T018 | 0.16 | 33:6;34:6;26:5;47:4;29:4 | deep_hierarchical_grouped |
| 1000539 | 6 | T160 | 0.15 | 11:8;13:5;34:4;9:4;14:3 | deep_sparse_mixed |
| 1000524 | 6 | T154 | 0.12 | 11:3;8:2;44:2;12:2;3:2 | deep_hierarchical_grouped |
| 1000140 | 6 | T036 | 0.12 | 7:6;5:3;11:3;2:3;12:3 | deep_hierarchical_grouped |
| 1000500 | 6 | T140 | 0.12 | 1:3;16:2;23:2;226:1;49:1 | census_format_paired |
| 1000094 | 6 | T020 | 0.12 | 12:8;11:5;36:5;24:5;27:5 | deep_hierarchical_grouped |
| 1000115 | 6 | T029 | 0.11 | 11:12;18:9;15:8;12:7;4:7 | census_format_paired |
| 1000543 | 6 | T161 | 0.11 | 26:2;24:2;77:2;12:2;10:1 | deep_sparse_mixed |
| 1000546 | 6 | T163 | 0.11 | 24:2;1:2;2:2;533:1;512:1 | deep_hierarchical_grouped |
| 1000528 | 6 | T156 | 0.10 | 12:4;6:3;22:2;5:2;7:2 | deep_hierarchical_grouped |
| 1000228 | 6 | T057 | 0.10 | 20:5;7:3;6:3;22:2;30:2 | census_format_paired |
| 1000501 | 2 | T141 | 0.09 | 1:53;5:36;2:30;3:17;33:14 | deep_hierarchical_grouped |
| 1000302 | 6 | T092 | 0.09 | 2:2;60:1;16:1;4:1;15:1 | deep_hierarchical_grouped |
| 1000063 | 6 | T015 | 0.09 | 4:9;1:7;2:6;12:6;5:5 | deep_hierarchical_grouped |
| 1000164 | 6 | T043 | 0.09 | 44:3;2:2;46:2;64:2;13:1 | large_value_flat |
| 1000099 | 2 | T024 | 0.09 | 2:4;3:3;4:3;5:3;1:2 | census_format_paired |

## Benford check (leading digits, values>=10, n>=20)

49 khipu had enough large values for a Benford test. Median chi2 (df=8, 5% crit=15.5): 16.5

## Do warehouse-type khipu share a data fingerprint?

Document clusters present: census_format_paired, deep_hierarchical_grouped, deep_sparse_mixed, large_value_flat

- census_format_paired (n=52): data clusters 2×36, 6×11, 1×3, 4×2
- deep_hierarchical_grouped (n=37): data clusters 6×19, 3×6, 2×6, 4×5, 5×1
- deep_sparse_mixed (n=71): data clusters 2×36, 6×18, 4×8, 1×4, 3×3, 5×2
- large_value_flat (n=5): data clusters 3×3, 6×2
## Synthesis: same data, different forms — confirmed

**Charles's hypothesis holds.** Stripping the form layout and clustering only the
variable-field values produces 6 clean data regimes, and every regime spans
completely distinct templates:

- Data cluster 2: **78 khipu, 78 distinct templates**, one signature (small counts, median ~3)
- Data cluster 6: **50 khipu, 50 distinct templates**, one signature (mid-range, median ~20)
- Data cluster 3: **12 khipu, 12 distinct templates**, one signature (bulk quantities, median ~344)

No two khipu in the same data cluster share a form. The standardization is in
*what is recorded*, not *how it is laid out*.

## What the six data regimes look like (bureaucrat's reading)

| Regime | n | Typical values | Likely recording |
|---|---|---|---|
| DC1 sparse/binary | 7 | 0/1, 89% zeros | presence/absence, checklists |
| DC2 small counts | 78 | median 3, max ~33 | census headcounts, small tallies |
| DC3 bulk quantities | 12 | median 344, max ~8,376 | warehouse/inventory volumes |
| DC4 mixed large | 15 | median 8, max ~4,657 | mixed admin, possibly multi-part |
| DC5 marker-saturated | 3 | 41% in {22,23,32,33,34} | form-batch markers as data (1000344 family) |
| DC6 mid-range | 50 | median 20, max ~202 | mid-scale admin counts |

## Document type vs data regime (the cross-cutting finding)

- **census_format_paired** (n=52) concentrates in DC2/DC6: census documents record
  small numbers (typical median ~4, max ~21) regardless of template layout.
- **large_value_flat** (n=5) concentrates in DC3: flat documents record bulk
  quantities (typical median ~165, max ~9,528).
- **deep_sparse_mixed** (n=71) and **deep_hierarchical_grouped** (n=37) spread
  across ALL data regimes: these are structural/layout styles, not data types.
  A hierarchical khipu can hold census counts or warehouse volumes.

The data signature cuts across the structural classification. Layout tells you the
office's habits; the value distribution tells you what was being recorded.

## The waterfall split (validation)

1000265-269 are physically tied, share a palette, and were read as one
multi-commodity inventory. Data fingerprinting puts them in THREE regimes:
1000265 -> DC3 (bulk), 1000266/267/268 -> DC6 (mid), 1000269 -> DC2 (small).
Same office, same form family, different commodities at different scales.
The magnitude stratification (W large / AB medium / RL-RB small) is visible
in the data clusters. Template-matching could not separate them; data-matching can.

## Marker values live in the data, not just the structure

68/165 khipu (41%) have 22/23/32/33/34 in *variable* positions. These are not
only row markers or template constants; they appear as recorded values across
the corpus. 1000344 is the extreme (41% of 220 variable values), but the
vocabulary is widespread. DC5 (1000344, 1000279, 1000513) is defined by it,
though two of its three members are small-n (10, 17 values) and provisional.

## Caveats

- 35/200 khipu excluded from clustering (fewer than 10 variable values or high
  decode-failure rate).
- DC5 rests on one strong member (1000344, n=220) plus two small-n members.
- MIXED positions (color varies across rows) were included as data; noisier than VAR.
- Benford test inconclusive (median chi2 16.5 vs 15.5 critical, n=49).
- Inkawasi long-knot values carry lower decode confidence.
