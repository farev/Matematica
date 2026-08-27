#!/usr/bin/env python3
"""Append an at-least-m cardinality totalizer over the first C(N,2)
variables (the edge variables of a ramsey base CNF) to a CNF file —
typically BreakID's output over the base, so the symmetry-breaking
predicates see the clean formula and the counting constraint is added
afterwards (sound: the edge count is invariant under the vertex
symmetries the SBPs break, so a lex-leader of any >=m model still has
>= m edges).

Usage: python3 ramsey_card_append.py N m IN.cnf OUT.cnf
"""
import sys
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType

def main():
    N, m = int(sys.argv[1]), int(sys.argv[2])
    fin, fout = sys.argv[3], sys.argv[4]
    E = N * (N - 1) // 2
    with open(fin) as f:
        first = f.readline().split()
        assert first[:2] == ["p", "cnf"], first
        bvars, bclauses = int(first[2]), int(first[3])
    assert bvars >= E
    pool = IDPool(start_from=bvars + 1)
    card = CardEnc.atmost([-v for v in range(1, E + 1)], bound=E - m,
                          encoding=EncType.totalizer, vpool=pool)
    with open(fin) as f, open(fout, "w") as g:
        f.readline()
        g.write(f"p cnf {pool.top} {bclauses + len(card.clauses)}\n")
        for line in f:
            g.write(line)
        for cl in card.clauses:
            g.write(" ".join(map(str, cl)) + " 0\n")
    print(f"{fout}: {pool.top} vars, {bclauses + len(card.clauses)} clauses (>= {m} edges)")

if __name__ == "__main__":
    main()
