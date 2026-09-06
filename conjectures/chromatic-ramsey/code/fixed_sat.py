#!/usr/bin/env python3
"""Colour a FIXED vertex set V subset of [3]^k: each pair gets a coordinate where it differs,
no monochromatic triangle. Optional symmetry constraints.
usage: fixed_sat.py k parity [k5_mode]
  parity 0: V = {x : #2's even}, parity 1: odd.
"""
import sys, time, itertools
from pysat.solvers import Solver

def solve(V, k, syms=(), name='cadical153', verbose=True):
    idx = {v: i for i, v in enumerate(V)}
    n = len(V)
    E = {}
    nv = 0
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(k):
                if V[a][c] != V[b][c]:
                    nv += 1; E[(a, b, c)] = nv
    def ev(a, b, c):
        if a > b: a, b = b, a
        return E.get((a, b, c))
    clauses = []
    for a in range(n):
        for b in range(a + 1, n):
            clauses.append([E[(a, b, c)] for c in range(k) if (a, b, c) in E])
    for a in range(n):
        for b in range(a + 1, n):
            for d in range(b + 1, n):
                for c in range(k):
                    x, y, z = ev(a, b, c), ev(a, d, c), ev(b, d, c)
                    if x and y and z:
                        clauses.append([-x, -y, -z])
    # symmetry: for g = (pi, sigmas): col(g x, g y) = pi(col(x,y))
    for (pi, sig) in syms:
        def g(v):
            w = [None] * k
            for i in range(k):
                w[pi[i]] = sig[i][v[i]]
            return tuple(w)
        for a in range(n):
            for b in range(a + 1, n):
                ga, gb = idx[g(V[a])], idx[g(V[b])]
                for c in range(k):
                    x = ev(a, b, c); y = ev(ga, gb, pi[c])
                    if x and y:
                        clauses.append([-x, y]); clauses.append([x, -y])
    if verbose:
        print(f"n={n} k={k} vars={nv} clauses={len(clauses)}", flush=True)
    t0 = time.time()
    with Solver(name=name, bootstrap_with=clauses) as sol:
        r = sol.solve()
        dt = time.time() - t0
        if verbose: print(f"result={'SAT' if r else 'UNSAT'} time={dt:.1f}s", flush=True)
        if not r: return None
        m = set(l for l in sol.get_model() if l > 0)
        col = {}
        for a in range(n):
            for b in range(a + 1, n):
                cs = [c for c in range(k) if (a, b, c) in E and E[(a, b, c)] in m]
                col[(V[a], V[b])] = cs[0]
        # verify
        for a, b, d in itertools.combinations(range(n), 3):
            assert not (col[(V[a], V[b])] == col[(V[a], V[d])] == col[(V[b], V[d])])
        return col

if __name__ == '__main__':
    k = int(sys.argv[1]); parity = int(sys.argv[2])
    V = [v for v in itertools.product(range(3), repeat=k) if v.count(2) % 2 == parity]
    col = solve(V, k)
    if col is not None:
        with open(f"col_even{parity}_k{k}.txt", "w") as f:
            for (a, b), c in sorted(col.items()):
                f.write(f"{''.join(map(str,a))} {''.join(map(str,b))} {c}\n")
        print("witness written, verified")
