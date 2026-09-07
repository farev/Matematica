"""Independent re-encoding of the two tight instances (n_t = 0 forced, so each
vertex x has one Boolean y_x = 'u-edge of x is its g-edge' (else g^{-1}-edge)).
On a 14-cycle only the vertices whose t-edge lies on C can be off; exactly 5 of
them must choose their off-cycle g-edge (a(C) = 9 forced).  On a 16-cycle at
least one such vertex must.  Naive subset (clause-explosion) encoding, no
auxiliary variables, solved with glucose42 and cadical195."""
import sys, itertools, time
from pysat.solvers import Solver
from orient import build, enumerate_cycles, off_labels

for (p, ta, tb, ga, gb) in [(29, 28, 0, 8, 1), (31, 30, 0, 22, 1)]:
    G, S, adj = build(p, ta, tb, ga, gb)
    n = G.n
    counts, cycles, _ = enumerate_cycles(adj, f"tight_p{p}_g{ga}")
    clauses = []
    for cyc in cycles:
        L = len(cyc)
        lits = []
        for x, j in off_labels(adj, cyc):
            if j == 1:
                lits.append(x + 1)        # off iff y_x true (chooses g-edge, which is off C)
            elif j == 2:
                lits.append(-(x + 1))     # off iff chooses g^{-1}-edge
            # j == 0: off-edge is the t-edge, never chosen -> vertex always on
        if L == 14:
            m = len(lits)
            # at least 5 of m: every subset of size m-4 contains a true literal
            for sub in itertools.combinations(lits, m - 4):
                clauses.append(list(sub))
            # at most 5: every subset of size 6 contains a false literal
            for sub in itertools.combinations(lits, 6):
                clauses.append([-l for l in sub])
        elif L == 15:
            m = len(lits)
            for sub in itertools.combinations(lits, m - 2):
                clauses.append(list(sub))
        else:
            clauses.append(lits)
    print(f"p={p} g=({ga},{gb}): {n} variables, {len(clauses)} clauses (naive encoding)")
    for name in ["glucose42", "cadical195"]:
        t0 = time.time()
        with Solver(name=name, bootstrap_with=clauses) as s:
            r = s.solve()
        print(f"   {name}: {'SAT' if r else 'UNSAT'} in {time.time()-t0:.1f}s")
