#!/usr/bin/env python3
# memory-lean variant of fixed_sat.py for E_6 (365 vertices): clauses streamed into the solver
import itertools
import sys
import time

from pysat.solvers import Solver

k = int(sys.argv[1]); parity = int(sys.argv[2])
V = [v for v in itertools.product(range(3), repeat=k) if v.count(2) % 2 == parity]
n = len(V); E = {}; nv = 0
for a in range(n):
    for b in range(a + 1, n):
        for c in range(k):
            if V[a][c] != V[b][c]:
                nv += 1; E[(a, b, c)] = nv
print(f"n={n} k={k} vars={nv}", flush=True)
t0 = time.time(); ncl = 0
with Solver(name='cadical153') as sol:
    for a in range(n):
        for b in range(a + 1, n):
            sol.add_clause([E[(a, b, c)] for c in range(k) if (a, b, c) in E]); ncl += 1
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(k):
                x = E.get((a, b, c))
                if not x: continue
                for d in range(b + 1, n):
                    y = E.get((a, d, c)); z = E.get((b, d, c))
                    if y and z: sol.add_clause([-x, -y, -z]); ncl += 1
    print(f"clauses={ncl} built in {time.time()-t0:.0f}s", flush=True)
    r = sol.solve()
    print("result", "SAT" if r else "UNSAT", f"{time.time()-t0:.0f}s", flush=True)
    if r:
        m = set(l for l in sol.get_model() if l > 0)
        with open(f"col_even{parity}_k{k}.txt", "w") as f:
            for a in range(n):
                for b in range(a + 1, n):
                    c = next(c for c in range(k) if (a, b, c) in E and E[(a, b, c)] in m)
                    f.write(f"{''.join(map(str,V[a]))} {''.join(map(str,V[b]))} {c}\n")
        print("witness written", flush=True)
