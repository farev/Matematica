#!/usr/bin/env python3
import itertools
import sys
import time

from pysat.solvers import Solver

H, s = int(sys.argv[1]), int(sys.argv[2])
pts = list(itertools.product(range(H), repeat=s))
nv = 0; F = {}; G = {}
for p in pts:
    for d in range(s):
        for v in range(H):
            nv += 1; F[(p, d, v)] = nv
for p in pts:
    for d in range(s):
        for v in range(H):
            nv += 1; G[(p, d, v)] = nv
cl = []
for p in pts:
    for d in range(s):
        cl.append([F[(p, d, v)] for v in range(H)]); cl.append([G[(p, d, v)] for v in range(H)])
        for v in range(H):
            for w in range(v + 1, H):
                cl.append([-F[(p, d, v)], -F[(p, d, w)]]); cl.append([-G[(p, d, v)], -G[(p, d, w)]])
for x in pts:
    for y in pts:
        cl.append([F[(y, d, x[d])] for d in range(s)] + [G[(x, d, y[d])] for d in range(s)])
t0 = time.time()
with Solver(name='cadical153', bootstrap_with=cl) as S:
    r = S.solve()
    print(f"H={H} s={s}: {'SAT' if r else 'UNSAT'} ({time.time()-t0:.1f}s)")
    if r:
        m = set(l for l in S.get_model() if l > 0)
        f = {p: tuple(next(v for v in range(H) if F[(p, d, v)] in m) for d in range(s)) for p in pts}
        g = {p: tuple(next(v for v in range(H) if G[(p, d, v)] in m) for d in range(s)) for p in pts}
        # verify from definition
        assert all(any(x[d] == f[y][d] or y[d] == g[x][d] for d in range(s)) for x in pts for y in pts)
        print(" f =", f); print(" g =", g); print(" verified saturated")
