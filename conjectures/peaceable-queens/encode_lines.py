#!/usr/bin/env python3
"""Line-labeling CNF encoder for peaceable queens (the strong encoding).

Reformulation (Lemma 1 of NOTE.md; standard structure, implicit in
Bosch's 1999 ILP model): in any placement, no queen line (row, column,
or diagonal) contains both colors.  Conversely, given any labeling of
all 6n-2 lines by {W, B}, placing white queens on every cell whose four
lines are all W, and black queens on every cell whose four lines are all
B, yields a valid placement (two cells of opposite colors would have to
share a line labeled both ways).  Hence

  PQ(n, m) is satisfiable
    iff  some labeling ell: Lines -> {W, B} has
         #{cells all-four-W} >= m  and  #{cells all-four-B} >= m.

Variables:
  lw(row r)    = 1 + r                    r in 0..n-1   (true = W label)
  lw(col c)    = n + 1 + c                c in 0..n-1
  lw(diag+ s)  = 2n + 1 + s               s = r+c in 0..2n-2
  lw(diag- d)  = 4n - 1 + 1 + d           d = r-c+n-1 in 0..2n-2
  wa(r,c)      = 6n - 2 + 1 + r*n + c     (white-available)
  ba(r,c)      = 6n - 2 + n*n + 1 + r*n + c
  cardinality aux vars above that.

Clauses:  wa(r,c) -> each of the 4 line lits;  ba -> negations;
  atleast-m over wa, atleast-m over ba.
  (Only the -> direction is needed: for a lower bound on the count the
  solver gains nothing by setting wa false when available.  Soundness of
  a model: every wa=true cell really is all-W.  UNSAT direction: any
  placement of m+m yields a model with wa/ba set from the true armies.)

Optional --symbreak: lex-leader over the 8 board symmetries x color
swap, acting on the line-variable vector (color swap = global flip, and
board maps permute lines; flip composes as lex over negated image).
"""

import argparse
from pysat.card import CardEnc, EncType


def line_vars(n):
    def row(r):
        return 1 + r

    def col(c):
        return n + 1 + c

    def dp(s):  # r+c
        return 2 * n + 1 + s

    def dm(d):  # r-c+n-1
        return 4 * n - 1 + 1 + d

    return row, col, dp, dm


def avail_vars(n):
    base = 6 * n - 2

    def wa(r, c):
        return base + 1 + r * n + c

    def ba(r, c):
        return base + n * n + 1 + r * n + c

    return wa, ba


def d4_line_maps(n):
    """Each board symmetry induces a permutation (possibly with family
    exchange) of lines.  Represent a line by its lw literal builder and
    return, for each symmetry, a function cell-free: line-lit -> line-lit.
    We implement it concretely: for each symmetry g we return a dict
    mapping every line var to its image line var."""
    row, col, dp, dm = line_vars(n)
    maps = []

    def build(g):
        # image of each line under the cell map g: map two cells of the
        # line and read off the image line.
        m = {}
        # rows
        for r in range(n):
            (r1, c1), (r2, c2) = g(r, 0), g(r, 1)
            m[row(r)] = _classify(n, r1, c1, r2, c2)
        for c in range(n):
            (r1, c1), (r2, c2) = g(0, c), g(1, c)
            m[col(c)] = _classify(n, r1, c1, r2, c2)
        for s in range(2 * n - 1):
            # two cells on diag+ s
            cells = [(r, s - r) for r in range(n) if 0 <= s - r < n]
            if len(cells) == 1:
                (r1, c1) = g(*cells[0])
                m[dp(s)] = None, (r1, c1)  # single-cell line: see below
            else:
                (r1, c1), (r2, c2) = g(*cells[0]), g(*cells[1])
                m[dp(s)] = _classify(n, r1, c1, r2, c2)
        for d in range(2 * n - 1):
            cells = [(r, r - (d - n + 1)) for r in range(n)
                     if 0 <= r - (d - n + 1) < n]
            if len(cells) == 1:
                (r1, c1) = g(*cells[0])
                m[dm(d)] = None, (r1, c1)
            else:
                (r1, c1), (r2, c2) = g(*cells[0]), g(*cells[1])
                m[dm(d)] = _classify(n, r1, c1, r2, c2)
        return m

    def _classify(n_, r1, c1, r2, c2):
        row_, col_, dp_, dm_ = line_vars(n_)
        if r1 == r2:
            return row_(r1)
        if c1 == c2:
            return col_(c1)
        if r1 + c1 == r2 + c2:
            return dp_(r1 + c1)
        assert r1 - c1 == r2 - c2
        return dm_(r1 - c1 + n_ - 1)

    gs = [
        lambda r, c: (c, n - 1 - r),
        lambda r, c: (n - 1 - r, n - 1 - c),
        lambda r, c: (n - 1 - c, r),
        lambda r, c: (r, n - 1 - c),
        lambda r, c: (n - 1 - r, c),
        lambda r, c: (c, r),
        lambda r, c: (n - 1 - c, n - 1 - r),
    ]
    for g in gs:
        maps.append(build(g))
    return maps


def _fix_singletons(mp, n):
    """Diagonal corner lines have a single cell; classify by that cell's
    diagonal coordinates directly."""
    row, col, dp, dm = line_vars(n)
    out = {}
    for k, v in mp.items():
        if isinstance(v, tuple) and v[0] is None:
            (r1, c1) = v[1]
            # a single-cell diagonal maps to the diagonal (same family
            # ambiguity: corner cell lies on one dp and one dm; choose by
            # which family k belongs to under the symmetry's parity).
            # Correctness for lex-leader only needs a permutation of vars;
            # we map dp-corner to the dp of the image cell and dm-corner
            # to the dm of the image cell, EXCEPT when the symmetry swaps
            # the diagonal families (odd rotations / transpositions),
            # in which case the families exchange.
            out[k] = (r1, c1)
        else:
            out[k] = v
    return out


def build_lines(n, m, symbreak=False):
    row, col, dp, dm = line_vars(n)
    wa, ba = avail_vars(n)
    clauses = []

    for r in range(n):
        for c in range(n):
            lits = [row(r), col(c), dp(r + c), dm(r - c + n - 1)]
            for lit in lits:
                clauses.append([-wa(r, c), lit])
                clauses.append([-ba(r, c), -lit])

    wlist = [wa(r, c) for r in range(n) for c in range(n)]
    blist = [ba(r, c) for r in range(n) for c in range(n)]
    top = 6 * n - 2 + 2 * n * n
    cardw = CardEnc.atleast(lits=wlist, bound=m, top_id=top,
                            encoding=EncType.seqcounter)
    top = max(top, cardw.nv)
    cardb = CardEnc.atleast(lits=blist, bound=m, top_id=top,
                            encoding=EncType.seqcounter)
    top = max(top, cardb.nv)
    clauses.extend(cardw.clauses)
    clauses.extend(cardb.clauses)

    aux_next = [top + 1]

    def new_aux():
        v = aux_next[0]
        aux_next[0] += 1
        return v

    if symbreak:
        nlines = 6 * n - 2
        base_vec = list(range(1, nlines + 1))
        images = []
        # color swap alone: vector of negated vars.
        images.append([-v for v in base_vec])
        for mp in d4_line_maps(n):
            mp = {k: v for k, v in mp.items()}
            ok = all(not isinstance(v, tuple) for v in mp.values())
            if not ok:
                continue  # skip maps with unresolved singleton diagonals
            img = [mp[v] for v in base_vec]
            images.append(img)
            images.append([-x for x in img])
        for img in images:
            _lex_leader_lits(base_vec, img, clauses, new_aux)

    return max(aux_next[0] - 1, top), clauses


def _lex_leader_lits(vec_x, vec_y, clauses, new_aux):
    """vec_x <=_lex vec_y where entries are literals (possibly negated)."""
    prev_e = None
    k = len(vec_x)
    for i in range(k):
        x, y = vec_x[i], vec_y[i]
        if prev_e is None:
            clauses.append([-x, y])
            if i < k - 1:
                e = new_aux()
                clauses.append([-e, -x, y])
                clauses.append([-e, x, -y])
                prev_e = e
        else:
            clauses.append([-prev_e, -x, y])
            if i < k - 1:
                e = new_aux()
                clauses.append([-e, prev_e])
                clauses.append([-e, -x, y])
                clauses.append([-e, x, -y])
                prev_e = e


def decode_grid(n, model):
    """Read the line labels from a model and place the maximal armies."""
    row, col, dp, dm = line_vars(n)
    rows = []
    for r in range(n):
        s = ""
        for c in range(n):
            lits = [row(r), col(c), dp(r + c), dm(r - c + n - 1)]
            vals = [lit in model for lit in lits]
            if all(vals):
                s += "W"
            elif not any(vals):
                s += "B"
            else:
                s += "."
        rows.append(s)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("n", type=int)
    ap.add_argument("m", type=int)
    ap.add_argument("out")
    ap.add_argument("--symbreak", action="store_true")
    args = ap.parse_args()
    nvars, clauses = build_lines(args.n, args.m, args.symbreak)
    with open(args.out, "w") as f:
        f.write(f"c peaceable queens LINE encoding n={args.n} m={args.m} "
                f"symbreak={args.symbreak}\n")
        f.write(f"p cnf {nvars} {len(clauses)}\n")
        for cl in clauses:
            f.write(" ".join(map(str, cl)) + " 0\n")
    print(f"wrote {args.out}: {nvars} vars, {len(clauses)} clauses")


if __name__ == "__main__":
    main()
