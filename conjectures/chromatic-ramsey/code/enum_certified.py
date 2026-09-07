#!/usr/bin/env python3
"""Certified census of the n-point colourable vertex sets of [j]^k.
Same model as enum_extremal.py, but solved incrementally by Glucose 4 with DRUP logging; when the
final call returns UNSAT, the DRUP proof refutes (base CNF + all blocking clauses), i.e. certifies
that the listed sets are ALL the colourable n-sets.  Writes <prefix>.cnf (base + blocking
clauses), <prefix>.drup, <prefix>_sets.json.  Check with:  rup_check <prefix>.cnf <prefix>.drup
usage: enum_certified.py j k n prefix"""
import itertools
import json
import sys
import time

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

j, k, n, prefix = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
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
sets = []; blocking = []; t0 = time.time()
with Solver(name='glucose4', bootstrap_with=clauses, with_proof=True) as sol:
    while sol.solve():
        m = set(l for l in sol.get_model() if l > 0)
        S = [t for t in range(T) if s[t] in m]
        sets.append([types[t] for t in S])
        bl = [-s[t] for t in S]; blocking.append(bl); sol.add_clause(bl)
        if len(sets) % 5000 == 0: print(f"  {len(sets)} sets, {time.time()-t0:.0f}s", flush=True)
    proof = sol.get_proof()
print(f"census complete: {len(sets)} colourable {n}-sets of [{j}]^{k}; final UNSAT proof {len(proof)} lines; {time.time()-t0:.0f}s", flush=True)
allcl = clauses + blocking
with open(prefix + ".cnf", "w") as f:
    f.write(f"p cnf {nv} {len(allcl)}\n")
    for c in allcl: f.write(' '.join(map(str, c)) + ' 0\n')
with open(prefix + ".drup", "w") as f:
    f.writelines(l + '\n' for l in proof)
json.dump(sets, open(prefix + "_sets.json", "w"))
print("wrote", prefix + ".cnf", prefix + ".drup", prefix + "_sets.json")
