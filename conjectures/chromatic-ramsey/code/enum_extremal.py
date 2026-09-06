#!/usr/bin/env python3
"""Enumerate ALL vertex sets S of [j]^k of size n admitting a valid colouring (via SAT with
blocking clauses on the selection variables), canonicalise under the group S_j wr S_k
(value permutations per coordinate + coordinate permutations), and report the orbits.
usage: enum_extremal.py j k n [maxsols]"""
import sys, itertools, time
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType

j, k, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
maxsols = int(sys.argv[4]) if len(sys.argv) > 4 else 10**6
types = list(itertools.product(range(j), repeat=k)); T = len(types); tid = {t: i for i, t in enumerate(types)}
nv = 0; s = {}
for t in range(T): nv += 1; s[t] = nv
E = {}
for a in range(T):
    for b in range(a + 1, T):
        for c in range(k):
            if types[a][c] != types[b][c]: nv += 1; E[(a, b, c)] = nv
clauses = []
for a in range(T):
    for b in range(a + 1, T):
        clauses.append([-s[a], -s[b]] + [E[(a, b, c)] for c in range(k) if (a, b, c) in E])
for a in range(T):
    for b in range(a + 1, T):
        for c in range(k):
            if (a, b, c) not in E: continue
            for d in range(b + 1, T):
                if (a, d, c) in E and (b, d, c) in E:
                    clauses.append([-E[(a, b, c)], -E[(a, d, c)], -E[(b, d, c)]])
card = CardEnc.equals(lits=[s[t] for t in range(T)], bound=n, top_id=nv, encoding=EncType.seqcounter)
clauses += card.clauses; nv = max(nv, card.nv)
# group
perms = list(itertools.permutations(range(j)))
group = [(pi, sig) for pi in itertools.permutations(range(k)) for sig in itertools.product(perms, repeat=k)]
def act(g, v):
    pi, sig = g; w = [None] * k
    for i in range(k): w[pi[i]] = sig[i][v[i]]
    return tuple(w)
def canon(S):
    best = None
    for g in group:
        img = tuple(sorted(act(g, v) for v in S))
        if best is None or img < best: best = img
    return best
orbits = {}; count = 0; t0 = time.time()
with Solver(name='cadical153', bootstrap_with=clauses) as sol:
    while count < maxsols and sol.solve():
        m = set(l for l in sol.get_model() if l > 0)
        S = [types[t] for t in range(T) if s[t] in m]
        count += 1
        c = canon(S)
        orbits[c] = orbits.get(c, 0) + 1
        sol.add_clause([-s[tid[v]] for v in S])
print(f"F({j},{k}) sets of size {n}: {count} sets, {len(orbits)} orbits ({time.time()-t0:.0f}s)")
import json; json.dump([list(map(list,c)) for c in orbits], open(f"reps_{j}_{k}_{n}.json","w"))
for c, cnt in orbits.items():
    zeros2 = sorted(v.count(j - 1) % 2 for v in c)
    print(f"  orbit of size {cnt}: representative {list(c)[:6]}... ; even-#(j-1)-count pattern: {sum(zeros2)} odd-weight points")
