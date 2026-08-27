#!/usr/bin/env python3
"""CNF encoder + solver driver for balanced r-colourings of K_N (Erdős #617).

Model <-> balanced colouring, exactly:
  vars x[e][c] (edge e gets colour c), e indexed in fixed lex order.
  exactly-one colour per edge (ALO + pairwise AMO);
  coverage: for every (r+1)-subset S and colour c, some edge inside S has c.

Optional colour-symmetry breaking (sound: colours are interchangeable in the
formula): value precedence along the fixed edge order — colour c+1 may first
appear only after colour c has appeared:
    x[j][c] -> OR_{i<j} x[i][c-1]   for c >= 1.

Usage:
  python3 encoder.py decide N r [--sym] [--dimacs FILE] [--proof FILE]
  python3 encoder.py check-witness N r FILE   (assume witness, must be SAT)

decide: solve with pysat Cadical195 (no proof) or Glucose42 (--proof DRUP).
SAT -> witness written to data/KN_balanced_rcol_sat.txt and re-verified from
the definition via construction.is_balanced (independent of the encoder).
"""
import itertools, sys, time
from pysat.formula import CNF
from pysat.solvers import Cadical195, Glucose42

from construction import is_balanced  # definition-level checker (independent)

def edge_list(N):
    return list(itertools.combinations(range(N), 2))

def build_cnf(N, r, sym=False):
    edges = edge_list(N)
    eidx = {e: i for i, e in enumerate(edges)}
    def var(ei, c):
        return ei * r + c + 1
    cnf = CNF()
    # exactly-one
    for ei in range(len(edges)):
        cnf.append([var(ei, c) for c in range(r)])
        for c1 in range(r):
            for c2 in range(c1 + 1, r):
                cnf.append([-var(ei, c1), -var(ei, c2)])
    # coverage
    for S in itertools.combinations(range(N), r + 1):
        inner = [eidx[e] for e in itertools.combinations(S, 2)]
        for c in range(r):
            cnf.append([var(ei, c) for ei in inner])
    # colour value-precedence symmetry breaking
    if sym:
        for c in range(1, r):
            for j in range(len(edges)):
                cnf.append([-var(j, c)] + [var(i, c - 1) for i in range(j)])
    return cnf, edges, var

def model_to_colouring(model, edges, r):
    pos = {v for v in model if v > 0}
    col = {}
    for ei, e in enumerate(edges):
        cs = [c for c in range(r) if ei * r + c + 1 in pos]
        assert len(cs) == 1, (e, cs)
        col[e] = cs[0]
    return col

def read_witness(fname):
    col = {}
    with open(fname) as f:
        for line in f:
            if line.startswith("#"):
                continue
            u, v, c = map(int, line.split())
            col[(u, v)] = c
    return col

def main():
    mode = sys.argv[1]
    N, r = int(sys.argv[2]), int(sys.argv[3])
    sym = "--sym" in sys.argv
    proof_file = None
    if "--proof" in sys.argv:
        proof_file = sys.argv[sys.argv.index("--proof") + 1]
    dimacs = None
    if "--dimacs" in sys.argv:
        dimacs = sys.argv[sys.argv.index("--dimacs") + 1]

    t0 = time.time()
    cnf, edges, var = build_cnf(N, r, sym=sym)
    nvars = len(edges) * r
    print(f"K_{N} r={r}: {nvars} vars, {len(cnf.clauses)} clauses "
          f"(built in {time.time()-t0:.1f}s, sym={sym})")
    if dimacs:
        cnf.to_file(dimacs)
        print(f"wrote {dimacs}")
        if mode == "dimacs-only":
            return

    if mode == "check-witness":
        col = read_witness(sys.argv[4])
        assumps = [var(ei, col[e]) for ei, e in enumerate(edges)]
        with Cadical195(bootstrap_with=cnf) as s:
            ok = s.solve(assumptions=assumps)
        print(f"witness assumption solve: {'SAT (consistent)' if ok else 'UNSAT (REJECTED)'}")
        return

    assert mode == "decide"
    t0 = time.time()
    if proof_file:
        with Glucose42(bootstrap_with=cnf, with_proof=True) as s:
            res = s.solve()
            dt = time.time() - t0
            if not res:
                with open(proof_file, "w") as f:
                    for line in s.get_proof():
                        f.write(line + "\n")
                    f.write("0\n")  # empty clause terminator for RUP checkers
                print(f"UNSAT in {dt:.1f}s; DRUP proof -> {proof_file}")
            else:
                model = s.get_model()
                print(f"SAT in {dt:.1f}s (proof mode)")
    else:
        with Cadical195(bootstrap_with=cnf) as s:
            res = s.solve()
            dt = time.time() - t0
            model = s.get_model() if res else None
        print(f"{'SAT' if res else 'UNSAT'} in {dt:.1f}s (cadical195)")

    if res:
        col = model_to_colouring(model, edges, r)
        ok, bad = is_balanced(N, r, col)
        assert ok, f"solver model FAILED definition check at {bad}"
        out = f"data/K{N}_balanced_{r}col_sat.txt"
        with open(out, "w") as f:
            f.write(f"# balanced {r}-colouring of K_{N} found by SAT; "
                    f"re-verified from the definition\n")
            for (u, v), c in sorted(col.items()):
                f.write(f"{u} {v} {c}\n")
        print(f"witness re-verified from the definition -> {out}")

if __name__ == "__main__":
    main()
