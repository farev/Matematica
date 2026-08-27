#!/usr/bin/env python3
"""Cardinality-strengthened CNF for balanced r-colourings of K_N (Erdős #617).

Same exact model as encoder.py (exactly-one colour per edge + coverage per
((r+1)-subset, colour)) PLUS the Turán floor of NOTE.md Lemma 1 encoded as
totalizer cardinality constraints:

    for every colour c:  #{e : colour(e) = c} >= C(N,2) - ex(N; K_{r+1})

ex(N; K_{r+1}) = e(T_r(N)) computed exactly. The bound is a PROVED
consequence of balancedness (Lemma 1), so adding it preserves the model set
exactly; it exists to hand the counting argument to the CDCL solver, which
cannot derive it by resolution at feasible cost.

Usage:
  python3 encoder2.py N r OUT.cnf                      standalone base+card
  python3 encoder2.py N r OUT.cnf --append-to B.cnf    B.cnf (e.g. BreakID
        output over the base encoding, whose first C(N,2)*r variables are the
        edge-colour vars) + card clauses with aux vars numbered above B's.
        Sound order: SBPs select isomorphism-class representatives and the
        Turan floor is isomorphism-invariant, so appending it after breaking
        preserves satisfiability exactly.
"""
import itertools, sys
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType

def turan_edges(n, s):
    """e(T_s(n)): complete s-partite, balanced parts."""
    q, rem = divmod(n, s)
    sizes = [q + 1] * rem + [q] * (s - rem)
    return (n * n - sum(a * a for a in sizes)) // 2

def comb2(n):
    return n * (n - 1) // 2

def card_clauses(N, r, start_var):
    E = comb2(N)
    var = lambda ei, c: ei * r + c + 1
    lb = E - turan_edges(N, r)
    print(f"K_{N} r={r}: Turan floor per colour = {lb} of {E} edges")
    pool = IDPool(start_from=start_var)
    out = []
    for c in range(r):
        lits = [var(ei, c) for ei in range(E)]
        # at-least-lb == at-most-(E-lb) on negated lits
        card = CardEnc.atmost([-l for l in lits], bound=E - lb,
                              encoding=EncType.totalizer, vpool=pool)
        out.extend(card.clauses)
    return out, pool.top

def main():
    N, r = int(sys.argv[1]), int(sys.argv[2])
    out = sys.argv[3]
    edges = list(itertools.combinations(range(N), 2))
    E = len(edges)
    eidx = {e: i for i, e in enumerate(edges)}
    var = lambda ei, c: ei * r + c + 1

    if "--append-to" in sys.argv:
        base = sys.argv[sys.argv.index("--append-to") + 1]
        header = None
        with open(base) as f:
            first = f.readline().split()
            assert first[:2] == ["p", "cnf"], first
            bvars, bclauses = int(first[2]), int(first[3])
        assert bvars >= E * r, (bvars, E * r)
        extra, top = card_clauses(N, r, bvars + 1)
        with open(base) as fin, open(out, "w") as fout:
            fin.readline()
            fout.write(f"p cnf {top} {bclauses + len(extra)}\n")
            for line in fin:
                fout.write(line)
            for cl in extra:
                fout.write(" ".join(map(str, cl)) + " 0\n")
        print(f"wrote {out}: {top} vars, {bclauses + len(extra)} clauses "
              f"(= {base} + {len(extra)} card clauses)")
        return

    cnf = CNF()
    for ei in range(E):
        cnf.append([var(ei, c) for c in range(r)])
        for c1 in range(r):
            for c2 in range(c1 + 1, r):
                cnf.append([-var(ei, c1), -var(ei, c2)])
    for S in itertools.combinations(range(N), r + 1):
        inner = [eidx[e] for e in itertools.combinations(S, 2)]
        for c in range(r):
            cnf.append([var(ei, c) for ei in inner])
    extra, top = card_clauses(N, r, E * r + 1)
    cnf.extend(extra)
    cnf.to_file(out)
    print(f"wrote {out}: {top} vars, {len(cnf.clauses)} clauses")

if __name__ == "__main__":
    main()
