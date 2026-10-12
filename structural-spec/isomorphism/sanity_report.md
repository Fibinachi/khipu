# Khipu Feature Database — Sanity Report

Cords parsed: 3184

Feature vocabulary size: 170

## Most promiscuous features (combine with many others)

| feature | id | distinct partners | cord count |
|---|---|---|---|
| knot:L | 136 | 139 | 1349 |
| level:L1 | 141 | 134 | 2110 |
| struct:pendant | 148 | 134 | 2110 |
| knot:S | 137 | 129 | 979 |
| struct:subsidiary | 149 | 119 | 1054 |
| color:W | 30 | 113 | 1508 |
| level:L2 | 142 | 110 | 969 |
| turns:L3 | 155 | 92 | 232 |
| turns:S2 | 162 | 92 | 212 |
| dir:u | 129 | 89 | 579 |
| turns:L4 | 156 | 89 | 238 |
| dir:s | 128 | 86 | 713 |
| turns:L5 | 157 | 85 | 163 |
| turns:S3 | 163 | 85 | 124 |
| turns:L2 | 154 | 80 | 384 |
| knot:E | 134 | 79 | 500 |
| struct:empty | 145 | 79 | 1068 |
| dir:Su | 125 | 77 | 271 |
| turns:L6 | 158 | 75 | 157 |
| turns:S4 | 164 | 75 | 83 |

## Most restricted features (>=5 cords, few partners)

| feature | id | distinct partners | cord count |
|---|---|---|---|
| compound:YB-KB | 112 | 5 | 5 |
| struct:missing | 147 | 7 | 7 |
| compound:B:GG | 44 | 9 | 14 |
| level:H | 140 | 9 | 20 |
| struct:header | 146 | 9 | 20 |
| compound:KB:AB | 70 | 10 | 14 |
| compound:YB:PB: | 116 | 10 | 8 |
| compound:MB-W | 83 | 11 | 5 |
| color:0D | 3 | 12 | 9 |
| compound:GG:AB | 66 | 12 | 9 |
| compound:MB:BL: | 88 | 12 | 8 |
| color:PB | 23 | 13 | 12 |
| compound:BY:BL | 55 | 13 | 6 |
| compound:FB:B | 62 | 13 | 5 |
| color:G0 | 16 | 14 | 14 |
| compound:KB:B | 71 | 14 | 17 |
| compound:W:AB | 101 | 14 | 10 |
| compound:BL:MB | 50 | 15 | 5 |
| compound:BY-W | 54 | 16 | 49 |
| compound:LB-W | 77 | 16 | 6 |

## Complementary distribution candidates (never co-occur, each >=10 cords)

| feature a | feature b | count a | count b |
|---|---|---|---|
| struct:pendant | struct:subsidiary | 2110 | 1054 |
| level:L1 | level:L2 | 2110 | 969 |
| level:L1 | level:L3 | 2110 | 82 |
| struct:header | struct:pendant | 20 | 2110 |
| level:H | level:L1 | 20 | 2110 |
| color:? | color:W | 61 | 1508 |
| color:G0 | color:W | 14 | 1508 |
| color:PB | color:W | 12 | 1508 |
| color:AB | color:YB | 626 | 463 |
| struct:header | struct:subsidiary | 20 | 1054 |
| level:L2 | level:L3 | 969 | 82 |
| level:H | level:L2 | 20 | 969 |
| color:MB | color:YB | 386 | 463 |
| dir:Es | dir:u | 192 | 579 |
| dir:SPu | dir:s | 16 | 713 |
| color:AB | color:BY | 626 | 95 |
| color:B | color:YB | 233 | 463 |
| dir:Ls | dir:Lu | 396 | 296 |
| color:? | color:AB | 61 | 626 |
| color:AB | color:BB | 626 | 50 |
| color:AB | color:LB | 626 | 46 |
| color:AB | color:RM | 626 | 42 |
| color:AB | color:FB | 626 | 42 |
| color:AB | color:LC | 626 | 39 |
| color:AB | color:DB | 626 | 31 |
| color:0G | color:AB | 28 | 626 |
| color:AB | color:BS | 626 | 24 |
| color:AB | color:G0 | 626 | 14 |
| color:AB | color:PB | 626 | 12 |
| color:AB | color:VR | 626 | 11 |
