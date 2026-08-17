#!/usr/bin/env python3
"""CNF encoder for the peaceable queens decision problem.

Decision problem PQ(n, m): do there exist >= m white and >= m black queens
on an n x n board such that no white queen and black queen share a row,
column, or diagonal?  (Pairwise line-exclusion model, no blocking — the
Bosch 1999 / Pratt ILP model behind OEIS A250000.  The a(1..13) ladder,
which this encoder reproduces exactly, is the operational check that this
is the right model.)

Variables (DIMACS numbering, deterministic):
  w(r,c) = 1 + r*n + c          for r,c in 0..n-1   (white queen at (r,c))
  b(r,c) = n*n + 1 + r*n + c                        (black queen at (r,c))
  auxiliary cardinality variables from 2*n*n + 1 upward.

Clauses:
  1. For every unordered pair of distinct cells p != q on a common row,
     column or diagonal:  (-w_p | -b_q) and (-b_p | -w_q).
  2. atleast-m over all w vars, atleast-m over all b vars
     (pysat CardEnc, sequential counter by default).

Optional symmetry breaking (--symbreak): lex-leader constraints for the
16-element group D4 x (color swap), sound for the decision problem
(any solution has a lex-minimal image under the group; constraints keep
at least that image).  Off by default; ladder controls run without it.

Usage: encode.py n m out.cnf [--symbreak] [--rowvars]
  --rowvars adds definitional row-occupancy variables RW_r, RB_r
  (RW_r <-> some white in row r) for cube-and-conquer splitting.
"""

import sys
import argparse
from pysat.card import CardEnc, EncType
from pysat.formula import IDPool


def cell_vars(n):
    def w(r, c):
        return 1 + r * n + c

    def b(r, c):
        return n * n + 1 + r * n + c

    return w, b


def aligned_pairs(n):
    """All unordered pairs of distinct cells sharing a queen line."""
    pairs = []
    cells = [(r, c) for r in range(n) for c in range(n)]
    for i, (r1, c1) in enumerate(cells):
        for r2, c2 in cells[i + 1:]:
            if r1 == r2 or c1 == c2 or r1 + c1 == r2 + c2 or r1 - c1 == r2 - c2:
                pairs.append(((r1, c1), (r2, c2)))
    return pairs


def d4_maps(n):
    """The 8 symmetries of the board as cell maps."""
    return [
        lambda r, c: (r, c),
        lambda r, c: (c, n - 1 - r),          # rot90
        lambda r, c: (n - 1 - r, n - 1 - c),  # rot180
        lambda r, c: (n - 1 - c, r),          # rot270
        lambda r, c: (r, n - 1 - c),          # mirror cols
        lambda r, c: (n - 1 - r, c),          # mirror rows
        lambda r, c: (c, r),                  # transpose
        lambda r, c: (n - 1 - c, n - 1 - r),  # anti-transpose
    ]


def lex_leader(vec_x, vec_y, pool, clauses):
    """Append CNF forcing vec_x <=_lex vec_y (x is the solution vector,
    y its image under a symmetry).  Standard chain encoding with
    equality-prefix variables."""
    k = len(vec_x)
    assert k == len(vec_y)
    # e_i: prefixes of length i are equal.  e_0 = true (implicit).
    prev_e = None
    for i in range(k):
        x, y = vec_x[i], vec_y[i]
        if prev_e is None:
            # x_0 <= y_0 :  (-x0 | y0)
            clauses.append([-x, y])
            if i < k - 1:
                e = pool.id(("lexeq", id(vec_y), i))
                # e -> (x0 <-> y0)
                clauses.append([-e, -x, y])
                clauses.append([-e, x, -y])
                prev_e = e
        else:
            # prev_e -> (x_i <= y_i)
            clauses.append([-prev_e, -x, y])
            if i < k - 1:
                e = pool.id(("lexeq", id(vec_y), i))
                # e -> prev_e, e -> (x_i <-> y_i)
                clauses.append([-e, prev_e])
                clauses.append([-e, -x, y])
                clauses.append([-e, x, -y])
                prev_e = e


def build(n, m, symbreak=False, rowvars=False):
    w, b = cell_vars(n)
    clauses = []

    # A cell hosts at most one piece: same-square white+black is excluded
    # (without this, one m-queens solution doubles as both armies).
    for r in range(n):
        for c in range(n):
            clauses.append([-w(r, c), -b(r, c)])

    for (r1, c1), (r2, c2) in aligned_pairs(n):
        clauses.append([-w(r1, c1), -b(r2, c2)])
        clauses.append([-b(r1, c1), -w(r2, c2)])

    wvars = [w(r, c) for r in range(n) for c in range(n)]
    bvars = [b(r, c) for r in range(n) for c in range(n)]

    top = 2 * n * n
    cardw = CardEnc.atleast(lits=wvars, bound=m, top_id=top,
                            encoding=EncType.seqcounter)
    top = max(top, cardw.nv)
    cardb = CardEnc.atleast(lits=bvars, bound=m, top_id=top,
                            encoding=EncType.seqcounter)
    top = max(top, cardb.nv)
    clauses.extend(cardw.clauses)
    clauses.extend(cardb.clauses)

    pool = IDPool(start_from=top + 1)

    if rowvars:
        # RW_r <-> OR_c w(r,c); RB_r likewise (full definitional closure so
        # cube literals in either polarity constrain the board).
        for r in range(n):
            rw = pool.id(("RW", r))
            rb = pool.id(("RB", r))
            row_w = [w(r, c) for c in range(n)]
            row_b = [b(r, c) for c in range(n)]
            clauses.append([-rw] + row_w)
            for v in row_w:
                clauses.append([rw, -v])
            clauses.append([-rb] + row_b)
            for v in row_b:
                clauses.append([rb, -v])

    if symbreak:
        base = [w(r, c) for r in range(n) for c in range(n)] + \
               [b(r, c) for r in range(n) for c in range(n)]
        images = []
        for gi, g in enumerate(d4_maps(n)):
            for swap in (False, True):
                if gi == 0 and not swap:
                    continue
                img_w, img_b = [], []
                for r in range(n):
                    for c in range(n):
                        rr, cc = g(r, c)
                        img_w.append(w(rr, cc))
                        img_b.append(b(rr, cc))
                if swap:
                    images.append(img_b + img_w)
                else:
                    images.append(img_w + img_b)
        for img in images:
            lex_leader(base, img, pool, clauses)

    nvars = max(pool.top, top)
    return nvars, clauses, pool


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("m", type=int)
    ap.add_argument("out")
    ap.add_argument("--symbreak", action="store_true")
    ap.add_argument("--rowvars", action="store_true")
    args = ap.parse_args()

    nvars, clauses, pool = build(args.n, args.m, args.symbreak, args.rowvars)
    with open(args.out, "w") as f:
        f.write(f"c peaceable queens n={args.n} m={args.m} "
                f"symbreak={args.symbreak} rowvars={args.rowvars}\n")
        f.write(f"c vars: w(r,c)=1+r*n+c, b(r,c)=n^2+1+r*n+c\n")
        f.write(f"p cnf {nvars} {len(clauses)}\n")
        for cl in clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")
    print(f"wrote {args.out}: {nvars} vars, {len(clauses)} clauses")


if __name__ == "__main__":
    main()
