#!/usr/bin/env python3
"""Circulant search: k-colour K_n on Z_n by difference class so that every class is
triangle-free (symmetric sum-free difference set) and vertex j-colourable.
usage: circ_sat.py n k j [out.json]   — writes the full witness (classes + proper colourings)."""
import sys, time, json
from pysat.solvers import Solver

n, k, j = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
out = sys.argv[4] if len(sys.argv) > 4 else None
D = list(range(1, n // 2 + 1))          # difference classes {d, -d}
def dn(d): return min(d % n, (-d) % n)
nv = 0; C = {}
for d in D:
    for c in range(k):
        nv += 1; C[(d, c)] = nv
F = {}
for v in range(n):
    for c in range(k):
        for a in range(j):
            nv += 1; F[(v, c, a)] = nv
cl = []
for d in D:
    cl.append([C[(d, c)] for c in range(k)])
    for c in range(k):
        for c2 in range(c + 1, k): cl.append([-C[(d, c)], -C[(d, c2)]])
seen = set()
for d1 in D:
    for d2 in D:
        for d3 in (dn(d1 + d2), dn(d1 - d2)):
            if d3 == 0: continue
            key = tuple(sorted((d1, d2, d3)))
            if key in seen: continue
            seen.add(key)
            for c in range(k):
                cl.append(sorted(set([-C[(d1, c)], -C[(d2, c)], -C[(d3, c)]])))
for v in range(n):
    for c in range(k):
        cl.append([F[(v, c, a)] for a in range(j)])
for v in range(n):
    for w in range(v + 1, n):
        d = dn(w - v)
        for c in range(k):
            for a in range(j):
                cl.append([-C[(d, c)], -F[(v, c, a)], -F[(w, c, a)]])
cl.append([C[(1, 0)]])  # symmetry: difference 1 has colour 0
print(f"n={n} k={k} j={j} vars={nv} clauses={len(cl)}", flush=True)
t0 = time.time()
with Solver(name='cadical153', bootstrap_with=cl) as s:
    r = s.solve()
    print("result", "SAT" if r else "UNSAT", f"{time.time()-t0:.1f}s", flush=True)
    if r:
        m = set(l for l in s.get_model() if l > 0)
        classes = {c: [d for d in D if C[(d, c)] in m] for c in range(k)}
        colourings = {c: [next(a for a in range(j) if F[(v, c, a)] in m) for v in range(n)] for c in range(k)}
        print("difference classes:", classes)
        if out:
            json.dump({"n": n, "k": k, "j": j, "classes": classes, "colourings": colourings}, open(out, "w"))
            print("wrote", out)
