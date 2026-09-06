#!/usr/bin/env python3
"""Cube-and-conquer proof that F(3,4) <= 41.
A 42-point configuration in [3]^4 has three layers of exactly 14 points in every direction
(each layer is a 14-point configuration in [3]^3 and F(3,3) = 14).  Every 14-point configuration
of [3]^3 lies in one of the orbits under S_3 wr S_3 enumerated by enum_extremal.py; by applying a
symmetry of the first three coordinates we may assume layer x_4 = 0 is an orbit representative.
For each representative R: fix the 14 types (r,0) as selected and ask for 28 more among the
remaining 54 types with a valid colouring.  All cases UNSAT => F(3,4) <= 41.
Phase 1 (this script): enumerate the representatives; phase 2: solve every cube with CaDiCaL;
phase 3: re-solve every cube with Glucose 4 + DRUP and write cnf/drup pairs for rup_check.
usage: cube42.py reps.json  [--prove]"""
import sys, json, itertools, time
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType

repfile = sys.argv[1]; prove = '--prove' in sys.argv
reps = json.load(open(repfile))
j, k, n = 3, 4, 42
types = list(itertools.product(range(j), repeat=k)); T = len(types); tid = {t: i for i, t in enumerate(types)}

def build_base():
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
    top = nv
    card = CardEnc.atleast(lits=[s[t] for t in range(T)], bound=n, top_id=top, encoding=EncType.seqcounter)
    clauses += card.clauses; top = max(top, card.nv)
    # implied bounds: every line <= 2, plane <= 5, 3-cube <= 14 (F(3,1),F(3,2),F(3,3))
    for d, B in ((1, 2), (2, 5), (3, 14)):
        for free in itertools.combinations(range(k), d):
            fixed = [c for c in range(k) if c not in free]
            for vals in itertools.product(range(j), repeat=len(fixed)):
                lits = []
                for fv in itertools.product(range(j), repeat=d):
                    t = [0] * k
                    for c, v in zip(fixed, vals): t[c] = v
                    for c, v in zip(free, fv): t[c] = v
                    lits.append(s[tid[tuple(t)]])
                cd = CardEnc.atmost(lits=lits, bound=B, top_id=top, encoding=EncType.seqcounter)
                clauses += cd.clauses; top = max(top, cd.nv)
    return s, clauses, top

s, base, nv = build_base()
print(f"base: vars={nv} clauses={len(base)}; {len(reps)} cubes", flush=True)
results = []
for i, R in enumerate(reps):
    R = [tuple(r) for r in R]
    assumptions = []
    for t in range(T):
        tt = types[t]
        if tt[3] == 0:
            assumptions.append(s[t] if tt[:3] in R else -s[t])
    t0 = time.time()
    if not prove:
        with Solver(name='cadical153', bootstrap_with=base) as sol:
            r = sol.solve(assumptions=assumptions)
        print(f"cube {i}: {'SAT' if r else 'UNSAT'} {time.time()-t0:.1f}s", flush=True)
    else:
        cl = base + [[a] for a in assumptions]
        with open(f"cube42_{i}.cnf", "w") as f:
            f.write(f"p cnf {nv} {len(cl)}\n")
            for c in cl: f.write(' '.join(map(str, c)) + ' 0\n')
        with Solver(name='glucose4', bootstrap_with=cl, with_proof=True) as sol:
            r = sol.solve()
            if not r:
                with open(f"cube42_{i}.drup", "w") as f:
                    for l in sol.get_proof(): f.write(l + '\n')
        print(f"cube {i}: {'SAT' if r else 'UNSAT'} {time.time()-t0:.1f}s (glucose, proof written)", flush=True)
    results.append(r)
print("any SAT?", any(results), "| all UNSAT:", not any(results))
