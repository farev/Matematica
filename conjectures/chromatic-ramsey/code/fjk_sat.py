#!/usr/bin/env python3
"""SAT model for Sawin's F(j,k): largest n such that K_n has a k-edge-colouring with every
colour class triangle-free and vertex j-colourable.

Type formulation: vertices are distinct points of [j]^k; an edge between two types must get a
colour c in which their c-th coordinates differ; no monochromatic triangle.

usage: fjk_sat.py j k n [solver]
"""
import itertools
import sys
import time

from pysat.card import CardEnc, EncType
from pysat.solvers import Solver


def build(j, k, n, symbreak=True):
    types = list(itertools.product(range(j), repeat=k))
    T = len(types)
    tid = {t: i for i, t in enumerate(types)}
    nv = 0
    s = {}
    for t in range(T):
        nv += 1; s[t] = nv
    E = {}
    for a in range(T):
        for b in range(a + 1, T):
            for c in range(k):
                if types[a][c] != types[b][c]:
                    nv += 1; E[(a, b, c)] = nv
    clauses = []
    # selected pair needs a colour
    for a in range(T):
        for b in range(a + 1, T):
            cs = [E[(a, b, c)] for c in range(k) if (a, b, c) in E]
            clauses.append([-s[a], -s[b]] + cs)
    # no monochromatic triangle (only among selected... colour vars only matter if selected,
    # but forbidding regardless is sound: unselected pairs can take any/no colour)
    # To keep it simple, forbid triangles unconditionally (colour vars of unselected pairs are free
    # to be false).
    for a in range(T):
        for b in range(a + 1, T):
            for c in range(k):
                if (a, b, c) not in E: continue
                for d in range(b + 1, T):
                    if (a, d, c) in E and (b, d, c) in E:
                        clauses.append([-E[(a, b, c)], -E[(a, d, c)], -E[(b, d, c)]])
    # cardinality: at least n selected
    card = CardEnc.atleast(lits=[s[t] for t in range(T)], bound=n, top_id=nv, encoding=EncType.seqcounter)
    clauses += card.clauses
    nv = max(nv, card.nv)
    if symbreak:
        # the all-zero type is selected (translation symmetry S_j^k acts transitively on types)
        clauses.append([s[tid[tuple([0] * k)]]])
    return types, s, E, clauses, nv

def main():
    j, k, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    name = sys.argv[4] if len(sys.argv) > 4 else 'cadical153'
    types, s, E, clauses, nv = build(j, k, n)
    print(f"F({j},{k}) >= {n}?  types={len(types)} vars={nv} clauses={len(clauses)}", flush=True)
    t0 = time.time()
    with Solver(name=name, bootstrap_with=clauses) as sol:
        r = sol.solve()
        dt = time.time() - t0
        print(f"result={'SAT' if r else 'UNSAT'} time={dt:.1f}s", flush=True)
        if r:
            m = set(l for l in sol.get_model() if l > 0)
            sel = [t for t in range(len(types)) if s[t] in m]
            print("selected types:", [types[t] for t in sel])
            # verify: each selected pair has a colour with differing coordinate, no mono triangle
            col = {}
            for a in sel:
                for b in sel:
                    if a < b:
                        cs = [c for c in range(k) if (a, b, c) in E and E[(a, b, c)] in m]
                        assert cs, (a, b)
                        col[(a, b)] = cs[0]
            for a, b, d in itertools.combinations(sel, 3):
                assert not (col[(a, b)] == col[(a, d)] == col[(b, d)])
            print("witness verified: %d vertices" % len(sel))
            with open(f"witness_F{j}_{k}_n{n}.txt", "w") as f:
                for (a, b), c in sorted(col.items()):
                    f.write(f"{types[a]} {types[b]} {c}\n")

if __name__ == '__main__':
    main()
