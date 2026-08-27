#!/usr/bin/env python3
"""Emit the balanced r-colouring instance for K_N as native pseudo-Boolean
constraints (OPB format, for cutting-planes solvers such as RoundingSat).

Constraints (model <-> balanced colouring, exactly):
  per edge e:            sum_c x_{e,c} = 1
  per (r+1)-set S, c:    sum_{e in S} x_{e,c} >= 1
  per colour c (Lemma 1 Turan floor, implied): sum_e x_{e,c} >= LB

Usage: python3 opb_emit.py N r OUT.opb
"""
import itertools, sys

def turan_edges(n, s):
    q, rem = divmod(n, s)
    sizes = [q + 1] * rem + [q] * (s - rem)
    return (n * n - sum(a * a for a in sizes)) // 2

def main():
    N, r = int(sys.argv[1]), int(sys.argv[2])
    out = sys.argv[3]
    edges = list(itertools.combinations(range(N), 2))
    E = len(edges)
    eidx = {e: i for i, e in enumerate(edges)}
    var = lambda ei, c: ei * r + c + 1
    lb = E - turan_edges(N, r)
    ncons = E + len(list(itertools.combinations(range(N), r + 1))) * r + r
    with open(out, "w") as f:
        f.write(f"* #variable= {E*r} #constraint= {ncons}\n")
        for ei in range(E):
            f.write(" ".join(f"+1 x{var(ei,c)}" for c in range(r)) + " = 1 ;\n")
        for S in itertools.combinations(range(N), r + 1):
            inner = [eidx[e] for e in itertools.combinations(S, 2)]
            for c in range(r):
                f.write(" ".join(f"+1 x{var(ei,c)}" for ei in inner) + " >= 1 ;\n")
        for c in range(r):
            f.write(" ".join(f"+1 x{var(ei,c)}" for ei in range(E)) + f" >= {lb} ;\n")
    print(f"wrote {out}: {E*r} vars, {ncons} constraints, per-colour floor {lb}")

if __name__ == "__main__":
    main()
