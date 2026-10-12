"""Serialize all non-funerary khipu to hex files."""
import sys
sys.path.insert(0, '/home/hatch/workspace/quipu-analysis')
from khipu_hex import serialize_khipu
import os

OUTDIR = '/home/hatch/workspace/quipu-analysis/byte-patterns/hex-corpus'
os.makedirs(OUTDIR, exist_ok=True)

with open('/tmp/khipu_ids.txt') as f:
    ids = [line.strip() for line in f if line.strip()]

ok, fail = 0, 0
concat = b''
for i, kid in enumerate(ids):
    try:
        data = serialize_khipu(int(kid))
        with open(f'{OUTDIR}/{kid}.hex', 'w') as f:
            f.write(data.hex())
        concat += data
        ok += 1
    except Exception as e:
        print(f'FAIL {kid}: {e}', flush=True)
        fail += 1
    if (i + 1) % 50 == 0:
        print(f'{i+1}/{len(ids)} done ({ok} ok, {fail} fail)', flush=True)

with open(f'{OUTDIR}/_concatenated.hex', 'w') as f:
    f.write(concat.hex())

print(f'DONE: {ok} ok, {fail} fail, concatenated {len(concat)} bytes')
