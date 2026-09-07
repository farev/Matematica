"""Independent re-check of the small subgroup-invariant instances with a second
solver (glucose42) and the totalizer encoding instead of seqcounter."""
import sys, time
from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver
from orient import build, enumerate_cycles, off_labels, REQ

REPS = [(29, 28, 0, 3, 1), (29, 28, 0, 8, 1), (31, 30, 0, 7, 1), (31, 30, 0, 10, 1), (31, 30, 0, 11, 1), (31, 30, 0, 22, 1)]


def build_cnf_tot(cyc_lits, no, orbit_of):
    cnf = CNF(); top = 3 * no
    for o in range(no):
        v = [3 * o + 1, 3 * o + 2, 3 * o + 3]
        cnf.append(v); cnf.append([-v[0], -v[1]]); cnf.append([-v[0], -v[2]]); cnf.append([-v[1], -v[2]])
    for L, lits in cyc_lits:
        mapped = sorted(3 * orbit_of[x] + j + 1 for x, j in lits)
        used, distinct = set(), []
        for v in mapped:
            if v in used:
                top += 1; cnf.append([-top, v]); cnf.append([top, -v]); distinct.append(top)
            else:
                used.add(v); distinct.append(v)
        enc = CardEnc.atleast(lits=distinct, bound=REQ[L], top_id=top, encoding=EncType.totalizer)
        cnf.extend(enc.clauses); top = max(top, enc.nv)
    return cnf


for (p, ta, tb, ga, gb) in REPS:
    G, S, adj = build(p, ta, tb, ga, gb)
    n = G.n
    counts, cycles, _ = enumerate_cycles(adj, f"cc_p{p}_g{ga}")
    cyc_lits = [(len(c), off_labels(adj, c)) for c in cycles]
    r = next(r for r in range(2, p) if all(pow(r, (p - 1) // q, p) != 1 for q in range(2, p) if (p - 1) % q == 0 and all(q % m for m in range(2, q))))
    dlog = {pow(r, k, p): k for k in range(p - 1)}
    out = []
    for m in [d for d in range(1, p) if (p - 1) % d == 0]:   # m = number of orbits of Z_p x| H_{(p-1)/m}
        orbit_of = [dlog[int(G.a[x])] % m for x in range(n)]
        cnf = build_cnf_tot(cyc_lits, m, orbit_of)
        s = Solver(name="glucose42", bootstrap_with=cnf.clauses)
        t0 = time.time(); res = None
        while time.time() - t0 < 5:
            s.conf_budget(2000); res = s.solve_limited()
            if res is not None:
                break
        s.delete()
        out.append(f"{m}:{'UNSAT' if res is False else ('SAT' if res else 'TO')}")
    print(f"p={p} g=({ga},{gb}) glucose42/totalizer, Z_p x| H_d instances by #orbits -> " + " ".join(out))
