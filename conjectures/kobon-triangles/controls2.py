#!/usr/bin/env python3
"""Controls for the v2 (segment-budget) encoding.
usage: controls2.py count            -> sigma-projection counts n=4..6 vs A006245 (no budget)
       controls2.py cases N@T,N@T,.. [timeout]  -> solve each with kissat, decode SAT models
Expected from Bartholdi-Blanc-Loisel Thm 1.4: a^s_3(n) = 1,2,5,7,11,14,21,25,32,37,47,53,65,72 (n=3..16).
"""
import os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kobon_sat2 import Encoder2
from kobon_sat import analyse
from controls import solve_kissat, A006245
from pysat.solvers import Cadical195

HERE = os.path.dirname(os.path.abspath(__file__))


def count(n):
    E = Encoder2(n, None, symbreak=False)
    sv = set(E.sig.values())
    c = 0
    with Cadical195(bootstrap_with=E.clauses) as s:
        while s.solve():
            m = s.get_model()
            c += 1
            s.add_clause([-l for l in m if abs(l) in sv])
    return c


def case(n, t, timeout, lexdepth=60, card='seqcounter'):
    E = Encoder2(n, t, symbreak=True, lexdepth=lexdepth, card=card)
    path = os.path.join(HERE, f'c2_n{n}_t{t}.cnf')
    E.write(path)
    res, model, dt = solve_kissat(path, timeout)
    info = ''
    if res == 'SAT':
        sigma = E.decode(model)
        seqs, swaps, tris, nfaces = analyse(n, sigma)
        info = f'adjacency-triangles={len(tris)} sweep-triangular-faces={nfaces}'
        assert len(tris) >= t and nfaces == len(tris), info
    return res, dt, info, E.nv, len(E.clauses), E.budget


if __name__ == '__main__':
    if sys.argv[1] == 'count':
        for n in (4, 5, 6):
            c = count(n)
            print(f'v2 sigma-projections n={n}: {c} (A006245 {A006245[n]}) {"OK" if c == A006245[n] else "MISMATCH"}', flush=True)
    else:
        timeout = float(sys.argv[3]) if len(sys.argv) > 3 else 1800
        for item in sys.argv[2].split(','):
            n, t = map(int, item.split('@'))
            res, dt, info, nv, nc, budget = case(n, t, timeout)
            print(f'v2 n={n:2d} t={t:3d} budget={budget}: {res:8s} {dt:8.1f}s vars={nv} clauses={nc} {info}', flush=True)
