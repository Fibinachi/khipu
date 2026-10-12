# Tree test report: hierarchical marking hypothesis

## Question
The ordinal-letter analysis killed the linear-sequential hypothesis (letters
repeat rather than chain). New hypothesis: letter cords (W:0, AB:0, MB:0, KB:0)
mark content cords through parent-subsidiary attachment, like Quechua suffixes
on nouns.

## Data
- 8,754 letter cords identified (90% of 9,688 occurrences; 934 unmapped due to
  duplicate CORD_ORDINAL values in source hex files)
- 416 khipu, 42,184 cords, all values decoded in Python (batched)

## Test 1: Attachment census
| Letter | n | Subsidiary of content | Top-level (primary) | Has subsidiaries | Levels |
|---|---|---|---|---|---|
| W (-ta?) | 4,227 | 9 (0.2%) | 4,060 (96%) | 669 (16%) | L1: 4,192 |
| A (-mi?) | 1,927 | 6 (0.3%) | 1,914 (99%) | 369 (19%) | L1: 1,916 |
| M (-kuna?) | 1,682 | 8 (0.5%) | 1,636 (97%) | 211 (13%) | L1: 1,665 |
| K (TBD) | 918 | 9 (1.0%) | 906 (99%) | 127 (14%) | L1: 904 |

Letter cords are overwhelmingly level-1 pendants hanging directly from the
primary cord. They are siblings of content cords, not suffixes on them.

## Test 2: Hierarchy test (permutation null)
- Observed P(letter subsidiary of content cord): 0.0037
- Null (200 within-khipu parent-link shuffles): mean 0.5033, sd 0.0417
- One-sided p (obs >= null): 1.0000
- VERDICT: NOT SUPPORTED. Letters attach to content cords far BELOW chance.
  They actively avoid subsidiary position; top-level placement is deliberate.

## Test 3: Marking test
- Forward (letter marks content as subsidiary): 20/18,406 content cords (0.1%). Negligible.
- Reverse (letter heads content group): 1,372 letter cords head 2,301 subsidiaries,
  41-50% nonzero. But control comparison shows letter-headed groups are
  indistinguishable from ordinary L1 groups (1.67 vs 1.82 subsidiaries;
  homogeneity 0.307 vs 0.245). Not a distinctive grammatical function.

## Test 4: Stacking
- Only single-letter attachments found (20 instances, depth exactly 1).
- No M+W, W+A, or M+W+A stacking. Quechua suffix-order test not applicable.
- VERDICT: no stacking. KILLED.

## Overall verdict: the tree hypothesis FAILS

All four tests fail or are non-distinctive:
1. Letters are not suffixes on content parents (0.37% vs 50% null).
2. Letters do not mark content cords (0.1% coverage).
3. No stacking occurs.
4. Letter-headed groups are ordinary hierarchy, not grammatical marking.

## Interpretation
The Hangman frequency alignment (W:0 = most frequent khipu pattern;
-ta = most frequent Quechua morpheme) was a Zipfian coincidence, not a
decipherment key. Both systems have few high-frequency function items, but
khipu letters operate as DOCUMENT-LEVEL structural elements (spreadsheet
column formats, section markers, categorical flags segregated by document),
not as morpheme-like units attaching to content words at any level.

The spreadsheet model is strengthened: letters are formatting, headers, and
section structure. They tell you what KIND of data follows, not grammatical
relationships between adjacent or attached cords.

## What remains open
- The moiety finding (S=upper/Z=lower from khipu boards) operates on knot
  DIRECTION, not letter cords; it is unaffected by this result.
- Color-tier separation (grammatical vs identity) stands on byte-level and
  distributional evidence independent of the Hangman anchors.
- The specific grammatical roles of W/AB/MB/KB (case? evidentiality?
  plurality?) are UNRESOLVED. Frequency suggested candidates; structure
  rejects the morpheme analogy. New hypotheses needed for what these
  high-frequency zero-value cords DO.
