#!/usr/bin/env python3
"""Does any balanced 5-colouring of K_26 extend the affine/code family on
K_25? (Erdős #617, r = 5.)

The family (NOTE.md §2): drop one parallel class δ of AG(2,5); colour every
pair of points by the parallel class of its line, for the five kept classes
(colours 0..4); the 50 pairs whose line has direction δ are FREE — any
choice of colours for them keeps K_25 balanced, because the pigeonhole
argument uses only the five kept directions. This is the full
partition-structured family up to the choice of resolution (secondary:
AG(2,5) is the unique affine plane of order 5, so up to isomorphism the
choice is which class to drop — all equivalent under the plane's
collineations).

Question: choose colours for the 50 free pairs and for the 25 edges from a
new vertex v so that K_26 = K_25 + v is balanced. Only 6-sets containing v
are constrained (all-in-K_25 6-sets are balanced by the kept directions).

SAT instance: 75 five-valued variables (375 bools), C(25,5) = 53,130
6-sets x 5 colours coverage clauses. SAT => Erdős #617 is FALSE (witness
re-verified from the definition). UNSAT => the code family does not extend
(lemma; certified by DRUP on request).

Usage: python3 extend_code.py [--proof FILE] [--dimacs FILE]
"""
import itertools, sys, time
from pysat.formula import CNF
from pysat.solvers import Cadical195, Glucose42

from construction import affine_plane, is_balanced

Q = 5
N25 = 25
V = 25  # index of the new vertex in K_26

def build():
    pts, classes = affine_plane(Q)
    # kept directions 0..4 -> colours 0..4; dropped direction = class 5
    edge_colour = {}   # fixed colours for kept-direction pairs
    free_pairs = []    # dropped-direction pairs, variable
    for ci in range(Q + 1):
        for L in classes[ci]:
            for u, v in itertools.combinations(sorted(L), 2):
                if ci < Q:
                    edge_colour[(u, v)] = ci
                else:
                    free_pairs.append((u, v))
    assert len(edge_colour) == 250 and len(free_pairs) == 50
    fidx = {p: i for i, p in enumerate(free_pairs)}
    # variables: x[i][c] for i in 0..74 (0..49 free pairs, 50..74 v-edges)
    nvar_groups = 75
    var = lambda i, c: i * Q + c + 1
    vedge = lambda u: 50 + u  # variable group of edge (u, V), u in 0..24
    cnf = CNF()
    for i in range(nvar_groups):
        cnf.append([var(i, c) for c in range(Q)])
        for c1 in range(Q):
            for c2 in range(c1 + 1, Q):
                cnf.append([-var(i, c1), -var(i, c2)])
    # coverage for 6-sets {v} u T, T a 5-subset of K_25
    npairs_fixed = 0
    for T in itertools.combinations(range(N25), 5):
        fixed = set()
        groups = [vedge(u) for u in T]
        for a, b in itertools.combinations(T, 2):
            if (a, b) in edge_colour:
                fixed.add(edge_colour[(a, b)])
            else:
                groups.append(fidx[(a, b)])
        for c in range(Q):
            if c in fixed:
                continue
            cnf.append([var(g, c) for g in groups])
            npairs_fixed += 1
    return cnf, free_pairs, fidx, edge_colour, var, vedge

def main():
    proof = sys.argv[sys.argv.index("--proof") + 1] if "--proof" in sys.argv else None
    dim = sys.argv[sys.argv.index("--dimacs") + 1] if "--dimacs" in sys.argv else None
    t0 = time.time()
    cnf, free_pairs, fidx, edge_colour, var, vedge = build()
    print(f"extend-code: {cnf.nv} vars, {len(cnf.clauses)} clauses "
          f"({time.time()-t0:.1f}s build)")
    if dim:
        cnf.to_file(dim); print(f"wrote {dim}"); return
    t0 = time.time()
    if proof:
        with Glucose42(bootstrap_with=cnf, with_proof=True) as s:
            res = s.solve()
            if not res:
                with open(proof, "w") as f:
                    for line in s.get_proof():
                        f.write(line + "\n")
                    f.write("0\n")
    else:
        with Cadical195(bootstrap_with=cnf) as s:
            res = s.solve()
            model = s.get_model() if res else None
    dt = time.time() - t0
    print(f"{'SAT' if res else 'UNSAT'} in {dt:.1f}s")
    if res and not proof:
        pos = {x for x in model if x > 0}
        col = dict(edge_colour)
        for p, i in fidx.items():
            cs = [c for c in range(Q) if var(i, c) in pos]
            assert len(cs) == 1
            col[p] = cs[0]
        for u in range(N25):
            cs = [c for c in range(Q) if var(vedge(u), c) in pos]
            assert len(cs) == 1
            col[(u, V)] = cs[0]
        ok, bad = is_balanced(26, 5, col)
        assert ok, f"definition check failed at {bad}"
        out = "data/K26_balanced_5col_WITNESS.txt"
        with open(out, "w") as f:
            f.write("# BALANCED 5-COLOURING OF K_26 — Erdős #617 r=5 REFUTED\n")
            for (u, v), c in sorted(col.items()):
                f.write(f"{u} {v} {c}\n")
        print(f"!!! balanced 5-colouring of K_26 found and re-verified -> {out}")

if __name__ == "__main__":
    main()
