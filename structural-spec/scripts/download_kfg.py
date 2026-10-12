#!/usr/bin/env python3
"""
Download KFG Excel files for khipu NOT in our OKR database.
URL pattern: https://www.khipufieldguide.com/databook/excel_khipus/KHnnnn.xlsx
Polite: 1.5s delay between requests. Resume-capable.
"""
import os
import time
import urllib.request
import urllib.error

RAW_DIR = os.path.expanduser("~/workspace/quipu-analysis/kfg_raw")
os.makedirs(RAW_DIR, exist_ok=True)

# Load our existing KH numbers
our_nums = set()
with open("/tmp/our_kh_nums.txt") as f:
    for line in f:
        our_nums.add(line.strip())

BASE = "https://www.khipufieldguide.com/databook/excel_khipus/{}.xlsx"
DELAY = 1.5
MAX_KH = 702  # KH0702 is highest known per OKR repo (Dec 2025)

def fetch(kh):
    url = BASE.format(kh)
    req = urllib.request.Request(url, headers={
        "User-Agent": "Khipu-Research/0.1 (academic research; polite bulk download)"
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return -1, None

def main():
    downloaded, skipped_have, skipped_404, errors = 0, 0, 0, 0
    # Resume: skip already-downloaded
    existing = {f.replace(".xlsx", "") for f in os.listdir(RAW_DIR) if f.endswith(".xlsx")}

    for n in range(1, MAX_KH + 1):
        kh = f"KH{n:04d}"
        if kh in our_nums:
            skipped_have += 1
            continue
        if kh in existing:
            continue
        status, data = fetch(kh)
        if status == 200 and data:
            path = os.path.join(RAW_DIR, f"{kh}.xlsx")
            with open(path, "wb") as f:
                f.write(data)
            downloaded += 1
            print(f"  GOT {kh} ({len(data)} bytes)", flush=True)
        elif status == 404:
            skipped_404 += 1
        else:
            errors += 1
            print(f"  ERR {kh}: status {status}", flush=True)
        time.sleep(DELAY)

    print(f"\nDone. Downloaded: {downloaded}, already-have: {skipped_have}, 404: {skipped_404}, errors: {errors}")

if __name__ == "__main__":
    main()
