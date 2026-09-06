#!/usr/bin/env python3
"""SAT model for F(j,k) with implied subcube bounds added as explicit cardinality constraints:
every d-dimensional axis-parallel subcube contains at most B[d] selected types, where B[d] is a
known upper bound on F(j,d) (B[1]=2 always).  Writes DIMACS if requested.
usage: fjk_sat2.py j k n [--cnf file] [--nosolve]"""
import sys, time, itertools
from pysat.solvers import Solver
from pysat.card import CardEnc, EncType

KNOWN = {  # (j,d): upper bound on F(j,d)
    (3, 1): 2, (3, 2): 5, (3, 3): 14,
    (4, 1): 2, (4, 2): 5, (4, 3): 16,
    (5, 1): 2, (5, 2): 5, (5, 3): 16,
}

def build(j, k, n):
    types = list(itertools.product(range(j), repeat=k))
    T = len(types); tid = {t: i for i, t in enumerate(types)}
    nv = 0; s = {}
    for t in range(T):
        nv += 1; s[t] = nv
    E = {}
    for a in range(T):
        for b in range(a + 1, T):
            for c in range(k):
                if types[a][c] != types[b][c]:
                    nv += 1; E[(a, b, c)] = nv
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
    # subcube bounds
    nsub = 0
    for d in range(1, k):
        if (j, d) not in KNOWN: continue
        B = KNOWN[(j, d)]
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
                clauses += cd.clauses; top = max(top, cd.nv); nsub += 1
    clauses.append([s[tid[tuple([0] * k)]]])
    return types, s, E, clauses, top, nsub

def main():
    j, k, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    cnf = None; solve = True
    if '--cnf' in sys.argv: cnf = sys.argv[sys.argv.index('--cnf') + 1]
    if '--nosolve' in sys.argv: solve = False
    types, s, E, clauses, nv, nsub = build(j, k, n)
    print(f"F({j},{k}) >= {n}?  types={len(types)} vars={nv} clauses={len(clauses)} subcube-constraints={nsub}", flush=True)
    if cnf:
        with open(cnf, 'w') as f:
            f.write(f"p cnf {nv} {len(clauses)}\n")
            for c in clauses: f.write(' '.join(map(str, c)) + ' 0\n')
        print("wrote", cnf, flush=True)
    if not solve: return
    t0 = time.time()
    with Solver(name='cadical153', bootstrap_with=clauses) as sol:
        r = sol.solve()
        print(f"result={'SAT' if r else 'UNSAT'} time={time.time()-t0:.1f}s", flush=True)
        if r:
            m = set(l for l in sol.get_model() if l > 0)
            sel = [t for t in range(len(types)) if s[t] in m]
            col = {}
            for a in sel:
                for b in sel:
                    if a < b:
                        cs = [c for c in range(k) if (a, b, c) in E and E[(a, b, c)] in m]
                        assert cs; col[(a, b)] = cs[0]
            for a, b, d in itertools.combinations(sel, 3):
                assert not (col[(a, b)] == col[(a, d)] == col[(b, d)])
            print("witness verified: %d vertices" % len(sel))
            with open(f"witness2_F{j}_{k}_n{n}.txt", "w") as f:
                for (a, b), c in sorted(col.items()):
                    f.write(f"{''.join(map(str,types[a]))} {''.join(map(str,types[b]))} {c}\n")

if __name__ == '__main__':
    main()
