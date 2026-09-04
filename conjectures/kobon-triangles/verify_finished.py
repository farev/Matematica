#!/usr/bin/env python3
"""Verify with drat-trim every cube whose solver run has finished (UNSAT line in a run_*.out
or a .done marker) and which has not been verified yet.  Appends to <cubedir>/verified.log.
usage: verify_finished.py <cubedir> [loop_seconds]
"""
import glob
import hashlib
import os
import re
import subprocess
import sys
import time

DRAT_TRIM = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'solvers', 'drat-trim', 'drat-trim')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def finished(cubedir):
    done = {}
    for f in glob.glob(os.path.join(cubedir, 'run_*.out')) + glob.glob(os.path.join(cubedir, '*.done')):
        for line in open(f):
            m = re.match(r'cube (\d+) (UNSAT|SAT|UNKNOWN) ([\d.]+)s', line)
            if m:
                done[int(m.group(1))] = (m.group(2), float(m.group(3)))
    return done


def verified(cubedir):
    v = {}
    p = os.path.join(cubedir, 'verified.log')
    if os.path.exists(p):
        for line in open(p):
            m = re.match(r'cube (\d+) (VERIFIED|FAILED)', line)
            if m:
                v[int(m.group(1))] = m.group(2)
    return v


def main():
    cubedir = sys.argv[1]
    loop = float(sys.argv[2]) if len(sys.argv) > 2 else 0
    while True:
        done, ver = finished(cubedir), verified(cubedir)
        todo = sorted(k for k, (st, _) in done.items() if st == 'UNSAT' and k not in ver)
        for k in todo:
            cnf = os.path.join(cubedir, f'cube_{k:04d}.cnf')
            drat = os.path.join(cubedir, f'cube_{k:04d}.drat')
            claim = os.path.join(cubedir, f'cube_{k:04d}.verifying')
            try:                                   # atomic claim so several verifiers can run
                fd = os.open(claim, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.close(fd)
            except FileExistsError:
                continue
            if not os.path.exists(drat):
                if os.path.exists(drat + '.gz'):
                    subprocess.run(['gunzip', '-k', '-f', drat + '.gz'])
                else:
                    os.remove(claim)
                    continue
            size, digest = os.path.getsize(drat), sha256(drat)
            t0 = time.time()
            p = subprocess.run([DRAT_TRIM, cnf, drat], capture_output=True, text=True)
            dt = time.time() - t0
            ok = 's VERIFIED' in p.stdout
            with open(os.path.join(cubedir, 'verified.log'), 'a') as f:
                f.write(f'cube {k} {"VERIFIED" if ok else "FAILED"} {dt:.1f}s solve={done[k][1]:.1f}s '
                        f'proof_bytes={size} sha256={digest}\n')
            if ok and os.environ.get('KEEP_PROOFS', '0') != '1':
                os.remove(drat)                    # disk: proofs are regenerable (deterministic solver)
                if os.path.exists(drat + '.gz'):
                    os.remove(drat + '.gz')
            if not ok:
                with open(os.path.join(cubedir, 'verify_failures.log'), 'a') as f:
                    f.write(f'=== cube {k} ===\n{p.stdout[-3000:]}\n')
        if not loop:
            break
        time.sleep(loop)


if __name__ == '__main__':
    main()
