#!/usr/bin/env python3
"""Verify every cube's DRAT proof with drat-trim; write <cubedir>/verify.log and a summary.
usage: verify_cubes.py <cubedir> [k0 k1] [--delete-cnf]
For each cube k with cube_k.drat present: run drat-trim cnf drat, record VERIFIED / FAILED / missing.
"""
import os
import subprocess
import sys
import time
import hashlib

DRAT_TRIM = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solvers', 'drat-trim', 'drat-trim')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    cubedir = sys.argv[1]
    k0 = int(sys.argv[2]) if len(sys.argv) > 3 else 0
    k1 = int(sys.argv[3]) if len(sys.argv) > 3 else 10 ** 6
    idx = [l.split() for l in open(os.path.join(cubedir, 'index.txt')) if not l.startswith('#')]
    log = open(os.path.join(cubedir, f'verify_{k0:04d}.log'), 'a')
    nver = nfail = nmiss = 0
    for row in idx:
        k = int(row[0])
        if not (k0 <= k < k1):
            continue
        cnf = os.path.join(cubedir, f'cube_{k:04d}.cnf')
        drat = os.path.join(cubedir, f'cube_{k:04d}.drat')
        if not os.path.exists(drat):
            nmiss += 1
            log.write(f'cube {k} MISSING-PROOF\n')
            continue
        t0 = time.time()
        p = subprocess.run([DRAT_TRIM, cnf, drat, '-f'], capture_output=True, text=True)
        dt = time.time() - t0
        ok = 's VERIFIED' in p.stdout
        nver += ok
        nfail += (not ok)
        lemmas = ''
        for line in p.stdout.splitlines():
            if 'lemmas' in line or 'c verified' in line.lower():
                lemmas = line.strip()
        log.write(f'cube {k} {"VERIFIED" if ok else "FAILED"} {dt:.1f}s proof_sha256={sha256(drat)} '
                  f'proof_bytes={os.path.getsize(drat)} {lemmas}\n')
        log.flush()
        if not ok:
            print(f'cube {k} FAILED:\n{p.stdout[-2000:]}', flush=True)
    print(f'verified={nver} failed={nfail} missing={nmiss}')


if __name__ == '__main__':
    main()
