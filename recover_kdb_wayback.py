"""
Recover the Harvard Khipu Database (KDB) DataTables archive from the Wayback Machine,
and generate a provenance manifest.

The original site (khipukamayuq.fas.harvard.edu) is offline; its per-khipu Excel
sheets, codebook, catalogs, and a 2012 SQL dump survive only as web.archive.org
captures. This script:

  1. enumerates every archived file under DataTables/ via the Wayback CDX API,
  2. downloads the LATEST capture of each (original bytes via the `id_` URL modifier),
     verifying magic bytes so an HTML error page can never masquerade as a spreadsheet,
  3. writes data/raw_data/kdb_sheets/MANIFEST.csv: one row per recovered file with
     original URL, snapshot timestamp, size, and SHA256.

Usage (from the repository root; the output path resolves relative to this
file's parent's parent — adjust OUT if running the script standalone):
    python recover_kdb_wayback.py                    # download missing + manifest
    python recover_kdb_wayback.py --manifest-only

Re-running is idempotent: files already present with valid magic bytes are skipped.
Provenance notes: data/raw_data/README.md. First run: 2026-07-17/18.
"""
import argparse
import csv
import hashlib
import subprocess
import time
import urllib.parse
import urllib.request
from pathlib import Path

CDX = ('http://web.archive.org/cdx/search/cdx'
       '?url=khipukamayuq.fas.harvard.edu/DataTables/*'
       '&output=text&fl=original,timestamp,statuscode&filter=statuscode:200'
       '&limit=50000')
OUT = Path(__file__).resolve().parent.parent / 'data/raw_data/kdb_sheets'
EXTS = ('xls', 'xlsx', 'doc', 'docx', 'zip')
MAGIC = (b'\xd0\xcf\x11\xe0', b'PK\x03\x04')   # OLE2 (.xls/.doc), zip (.xlsx/.docx/.zip)


def cdx_latest() -> dict:
    """{original_url: latest_timestamp} for every 200-status DataTables capture."""
    with urllib.request.urlopen(CDX, timeout=120) as r:
        text = r.read().decode()
    latest = {}
    for line in text.splitlines():
        parts = line.split()
        if len(parts) >= 2 and parts[0].rsplit('.', 1)[-1].lower() in EXTS:
            orig, ts = parts[0].replace(':80/', '/', 1), parts[1]
            if orig not in latest or ts > latest[orig]:
                latest[orig] = ts
    return latest


def magic_valid(path: Path) -> bool:
    return (path.exists() and path.stat().st_size >= 1000
            and path.open('rb').read(4) in MAGIC)


def dest_for(orig: str) -> Path:
    name = urllib.parse.unquote(orig.split('/')[-1]).replace(' ', '_')
    up = name.upper()
    if up.startswith('UR') and up.endswith(('.XLS', '.XLSX')):
        sub = 'UR'
    elif up.startswith('HP'):
        sub = 'HP'
    elif up.startswith('JC'):
        sub = 'JC'
    else:
        sub = 'misc'
    return OUT / sub / name


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest-only', action='store_true',
                    help='skip downloads; just (re)write MANIFEST.csv')
    args = ap.parse_args()

    latest = cdx_latest()
    print(f'{len(latest)} archived files enumerated via CDX')

    ok = skip = fail = 0
    if not args.manifest_only:
        for orig, ts in sorted(latest.items()):
            dest = dest_for(orig)
            if magic_valid(dest):
                skip += 1
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            wb = f'https://web.archive.org/web/{ts}id_/{orig.replace(":80/", "/", 1)}'
            for attempt in range(3):
                r = subprocess.run(['curl', '-sL', '--max-time', '120',
                                    '-o', str(dest), wb], capture_output=True)
                if r.returncode == 0 and magic_valid(dest):
                    ok += 1
                    break
                time.sleep(5 * (attempt + 1))
            else:
                fail += 1
                print(f'  FAIL {orig}')
                if dest.exists():
                    dest.unlink()
            time.sleep(0.7)
        print(f'download pass: {ok} fetched, {skip} already present, {fail} failed')

    # manifest: every wayback-recovered file currently on disk
    rows = []
    by_dest = {dest_for(o): (o, t) for o, t in latest.items()}
    for f in sorted(OUT.rglob('*')):
        if not f.is_file() or 'khipudb_sql' in f.parts:
            continue
        rel = f.relative_to(OUT)
        if f in by_dest:
            orig, ts = by_dest[f]
            src = 'wayback'
        elif f.name.startswith('KH0'):
            orig, ts, src = '', '', 'khipu_field_guide'   # user-downloaded KFG exports
        elif f.parent == OUT and f.name.startswith('UR'):
            # first six recovered individually before the bulk run (notebook 06 path);
            # byte-identical duplicates of the UR/ copies
            orig = ('http://khipukamayuq.fas.harvard.edu/DataTables/'
                    f'UR%20%3C1000%20data%20tables/{f.name}')
            ts, src = 'see UR/ row', 'wayback (duplicate of UR/ copy)'
        elif f.name == 'MANIFEST.csv':
            continue
        else:
            orig, ts, src = '', '', 'unknown'
        rows.append({'file': str(rel), 'source': src, 'original_url': orig,
                     'wayback_timestamp': ts, 'bytes': f.stat().st_size,
                     'sha256': sha256(f)})

    mpath = OUT / 'MANIFEST.csv'
    with mpath.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=['file', 'source', 'original_url',
                                          'wayback_timestamp', 'bytes', 'sha256'])
        w.writeheader()
        w.writerows(rows)
    print(f'wrote {mpath} ({len(rows)} rows)')


if __name__ == '__main__':
    main()
