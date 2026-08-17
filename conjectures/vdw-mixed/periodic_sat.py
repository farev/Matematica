#!/usr/bin/env python3
"""Complete SAT search for exactly-periodic good partitions.

For period p, restrict x_i = b_{((i-1) mod p) + 1}. Every concrete AP clause
over [1,n] projects to a clause over the p block variables (duplicates
collapse; a clause containing both polarities of one variable is a tautology
and is dropped -- cannot happen within one AP clause since all literals share
sign, but stays for safety). An exactly-p-periodic coloring is a good
partition of [1,n] iff the block satisfies the projected CNF, so per (n, p)
this search is COMPLETE: UNSAT means no p-periodic witness at that n exists.

Every SAT block is expanded to [1,n] and re-verified by coloring_is_good
before being written.

Usage:
  python3 periodic_sat.py s t n pmin pmax        # scan periods
"""
import os
import sys

from pysat.solvers import Cadical195

from vdw_cnf import aps, coloring_is_good

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")


def projected_clauses(n, s, t, p):
    cls = set()
    for ap in aps(n, s):
        lits = frozenset(((q - 1) % p) + 1 for q in ap)
        cls.add(tuple(sorted(lits)))            # positive clause
    pos = list(cls)
    cls_t = set()
    for ap in aps(n, t):
        lits = frozenset(((q - 1) % p) + 1 for q in ap)
        cls_t.add(tuple(sorted(-v for v in lits)))
    return [list(c) for c in pos] + [list(c) for c in cls_t]


def scan(s, t, n, pmin, pmax, save=True, verbose=True):
    hits = []
    for p in range(pmin, pmax + 1):
        cls = projected_clauses(n, s, t, p)
        with Cadical195(bootstrap_with=cls) as S:
            if S.solve():
                model = S.get_model()
                block = [0] * (p + 1)
                for lit in model:
                    v = abs(lit)
                    if 1 <= v <= p:
                        block[v] = 1 if lit > 0 else 0
                col = [0] * (n + 1)
                for i in range(1, n + 1):
                    col[i] = block[((i - 1) % p) + 1]
                if not coloring_is_good(col, s, t):
                    raise RuntimeError(f"p={p}: expansion failed verification")
                hits.append(p)
                if verbose:
                    print(f"  p={p}: PERIODIC WITNESS exists", flush=True)
                if save:
                    os.makedirs(DATA, exist_ok=True)
                    path = os.path.join(
                        DATA, f"witness_{s}_{t}_n{n}_persat_p{p}.txt")
                    with open(path, "w") as f:
                        f.write(f"# good partition of [1,{n}] for ({s},{t}); "
                                f"exactly {p}-periodic (complete SAT per "
                                f"period), verified\n")
                        f.write("".join(str(col[i])
                                        for i in range(1, n + 1)) + "\n")
                    return hits, path
    return hits, None


if __name__ == "__main__":
    s, t, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    pmin, pmax = int(sys.argv[4]), int(sys.argv[5])
    hits, path = scan(s, t, n, pmin, pmax)
    if hits:
        print(f"periods with witnesses: {hits} -> {path}")
    else:
        print(f"NO exactly-periodic witness for ({s},{t}) n={n} "
              f"with p in [{pmin},{pmax}] (complete per-period result)")
