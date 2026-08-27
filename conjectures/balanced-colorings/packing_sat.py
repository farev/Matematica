#!/usr/bin/env python3
"""Independent machine check of the Singleton-bound lemma (Erdős #617).

Lemma (NOTE.md §3): a balanced r-colouring of K_N in which every colour's
complement graph is r-partite exists  iff  there are r partitions of [N],
each into at most r parts, such that every pair of vertices is co-partitioned
in at most one of them  iff  there is an N-word code of length r over an
r-letter alphabet with pairwise Hamming distance >= r-1. Singleton forces
N <= r^2, so at N = r^2 + 1 no such colouring exists, for any r.

This script cross-checks the combinatorial core by SAT, independently of the
proof: variables y[v][c][p] = "vertex v is in part p of partition c",
exactly-one part per (v,c); for every pair u<v and every unordered pair of
partitions c<c', and all parts p, p': not both co-partitioned:
    ~(y[u][c][p] & y[v][c][p]) OR ~(y[u][c'][p'] & y[v][c'][p'])
encoded via auxiliary pair variables s[uv][c] = "u,v co-partitioned in c":
    y[u][c][p] & y[v][c][p] -> s[uv][c]        (definitional, one direction
                                                suffices for the AMO check)
    at-most-one over c of s[uv][c].

Usage: python3 packing_sat.py N r [--proof FILE]
Expected: SAT at N = r^2 (control, r prime power), UNSAT at N = r^2 + 1.
"""
import itertools, sys, time
from pysat.formula import CNF, IDPool
from pysat.solvers import Cadical195, Glucose42

def build(N, r):
    pool = IDPool()
    y = lambda v, c, p: pool.id(("y", v, c, p))
    s = lambda u, v, c: pool.id(("s", u, v, c))
    cnf = CNF()
    for v in range(N):
        for c in range(r):
            cnf.append([y(v, c, p) for p in range(r)])
            for p1 in range(r):
                for p2 in range(p1 + 1, r):
                    cnf.append([-y(v, c, p1), -y(v, c, p2)])
    for u, v in itertools.combinations(range(N), 2):
        for c in range(r):
            for p in range(r):
                cnf.append([-y(u, c, p), -y(v, c, p), s(u, v, c)])
        for c1 in range(r):
            for c2 in range(c1 + 1, r):
                cnf.append([-s(u, v, c1), -s(u, v, c2)])
    # symmetry breaking (sound): partition 0 of vertex v uses a part index
    # <= v (parts within a partition are interchangeable, applied to c=0 only
    # via first-occurrence ordering on vertices 0..r-1)
    for v in range(min(N, r)):
        for p in range(v + 1, r):
            cnf.append([-y(v, 0, p)])
    return cnf, pool

def main():
    N, r = int(sys.argv[1]), int(sys.argv[2])
    proof = sys.argv[sys.argv.index("--proof") + 1] if "--proof" in sys.argv else None
    cnf, pool = build(N, r)
    print(f"packing N={N} r={r}: {pool.top} vars, {len(cnf.clauses)} clauses")
    t0 = time.time()
    if proof:
        with Glucose42(bootstrap_with=cnf, with_proof=True) as sv:
            res = sv.solve()
            if not res:
                with open(proof, "w") as f:
                    for line in sv.get_proof():
                        f.write(line + "\n")
                    f.write("0\n")
    else:
        with Cadical195(bootstrap_with=cnf) as sv:
            res = sv.solve()
            model = sv.get_model() if res else None
    dt = time.time() - t0
    print(f"{'SAT' if res else 'UNSAT'} in {dt:.1f}s" + (f"; proof -> {proof}" if proof and not res else ""))
    if res and not proof:
        # extract and verify the packing from the definition
        pos = set(x for x in model if x > 0)
        part = {}
        for v in range(N):
            for c in range(r):
                ps = [p for p in range(r) if pool.id(("y", v, c, p)) in pos]
                assert len(ps) == 1
                part[(v, c)] = ps[0]
        for u, v in itertools.combinations(range(N), 2):
            agree = sum(1 for c in range(r) if part[(u, c)] == part[(v, c)])
            assert agree <= 1, (u, v, agree)
        print("packing verified from the definition (pairwise co-partition <= 1)")

if __name__ == "__main__":
    main()
