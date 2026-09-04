#!/usr/bin/env python3
"""Positive/negative controls for kobon_sat.py.

1. Count signotopes (no symmetry breaking, no cardinality) for n = 4..7 and compare with
   OEIS A006245: 8, 62, 908, 24698 (simple Euclidean pseudoline arrangements).
2. For n = 3..N, check SAT at the Bartholdi-Blanc-Loisel Theorem 1.4 value a^s_3(n) and
   UNSAT at a^s_3(n)+1; every SAT model is decoded and its triangle count recomputed by
   two independent routines (adjacency test on local sequences; face count of the sweep).
"""
import subprocess, sys, time, os
from pysat.solvers import Cadical195
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kobon_sat import Encoder, analyse

BBL = {3: 1, 4: 2, 5: 5, 6: 7, 7: 11, 8: 14, 9: 21, 10: 25, 11: 32, 12: 37, 13: 47, 14: 53, 15: 65, 16: 72}
A006245 = {4: 8, 5: 62, 6: 908, 7: 24698}
KISSAT = os.environ.get('KISSAT', 'kissat')


def count_signotopes(n):
    E = Encoder(n, None, symbreak=False)
    cnt = 0
    with Cadical195(bootstrap_with=E.clauses) as s:
        sigvars = list(E.sig.values())
        while s.solve():
            m = s.get_model()
            cnt += 1
            # block this sigma assignment (project on sigma variables)
            s.add_clause([-l for l in m if abs(l) in set(sigvars)])
    return cnt


def solve_kissat(path, timeout):
    t0 = time.time()
    try:
        p = subprocess.run([KISSAT, '-q', path], capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', None, time.time() - t0
    out = p.stdout
    if 's SATISFIABLE' in out:
        lits = []
        for line in out.splitlines():
            if line.startswith('v '):
                lits += [int(x) for x in line[2:].split()]
        return 'SAT', [l for l in lits if l != 0], time.time() - t0
    if 's UNSATISFIABLE' in out:
        return 'UNSAT', None, time.time() - t0
    return 'UNKNOWN', None, time.time() - t0


def run_case(n, t, timeout, full=False):
    E = Encoder(n, t, full=full, symbreak=True)
    path = f'/tmp/claude-0/-home-user-Matematica/21128dea-5602-504e-ae04-f9d7dc0e3405/scratchpad/kobon/ctrl_n{n}_t{t}{"_full" if full else ""}.cnf'
    E.write(path)
    res, model, dt = solve_kissat(path, timeout)
    info = ''
    if res == 'SAT':
        sigma = E.decode(model)
        seqs, swaps, tris, nfaces = analyse(n, sigma)
        info = f'adjacency-triangles={len(tris)} sweep-triangular-faces={nfaces}'
        assert len(tris) >= t and nfaces == len(tris), info
    return res, dt, info, E.nv, len(E.clauses)


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'all'
    if what in ('all', 'count'):
        for n, expect in A006245.items():
            t0 = time.time()
            c = count_signotopes(n)
            print(f'signotopes n={n}: {c} (A006245 {expect}) {"OK" if c == expect else "MISMATCH"} {time.time()-t0:.1f}s', flush=True)
    if what in ('all', 'tri'):
        nmax = int(sys.argv[2]) if len(sys.argv) > 2 else 12
        timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 600
        for n in range(3, nmax + 1):
            v = BBL[n]
            for t in (v, v + 1):
                res, dt, info, nv, nc = run_case(n, t, timeout)
                expect = 'SAT' if t == v else 'UNSAT'
                flag = 'OK' if res == expect else ('??' if res == 'TIMEOUT' else 'MISMATCH')
                print(f'n={n:2d} t={t:3d}: {res:8s} ({expect} expected) {flag} {dt:7.1f}s  vars={nv} clauses={nc} {info}', flush=True)
