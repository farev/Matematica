#!/usr/bin/env python3
"""Exact branch-and-bound for the peaceable-queens decision problem,
working in the line-labeling formulation (NOTE.md Lemma 1):

  PQ(n, m) is satisfiable iff some labeling of the 6n-2 queen lines by
  {W, B} has at least m cells whose four lines are all W and at least m
  cells whose four lines are all B.

Search structure:
  stage 1: white row set S (all 2^n, color-swap-canonical: row 0 in S),
  stage 2: white column set T, pruned by the product bound,
  stage 3: DFS over diagonal labels (both families interleaved), pruned
           by the cell bound and the family-sum bound.

Pruning bounds (each proved in NOTE.md; all exact integer arithmetic):
  product bound (L3): m <= |S||T| and m <= (n-|S|)(n-|T|).
  cell bound (L4):    white <= #{cells in SxT with neither diagonal
                      labeled B}, black symmetric; prune if either < m.
  family-sum bound (L5): for each diagonal family, white + black <=
                      sum over diagonals of (W: alive white cells;
                      B: alive black cells; free: max of the two);
                      prune if < 2m.

Decision semantics: exhaustive over all labelings up to the color swap
(L6), so "UNSAT at m" proves a(n) <= m-1, and any SAT leaf yields a
witness placement, re-verified by the independent checker.

This is the reference implementation (pure Python, deliberately simple).
bnb.c is the fast port; both must agree on verdicts and node counts.
"""

import sys
import time


def solve(n, m, collect_witness=True, node_limit=None, verbose=False):
    """Returns (status, witness_or_None, nodes) with status in
    {"SAT", "UNSAT", "LIMIT"}."""
    N2 = 2 * n - 1
    FREE, W, B = 0, 1, 2

    # cell lists per diagonal, per grid, filled per (S, T)
    nodes = 0
    lo = (m + n - 1) // n      # min white rows
    hi = n - lo                # max white rows (black needs the rest)

    # diagonal label arrays and per-diagonal alive counts
    dplab = [FREE] * N2
    dmlab = [FREE] * N2

    for S in range(1 << n):
        if not (S & 1):
            continue  # color-swap canonical: row 0 is white
        rw = bin(S).count("1")
        if rw * n < m or (n - rw) * n < m:
            continue
        for T in range(1 << n):
            cw = bin(T).count("1")
            if rw * cw < m or (n - rw) * (n - cw) < m:
                continue
            nodes += 1
            if node_limit and nodes > node_limit:
                return "LIMIT", None, nodes

            # build per-diagonal cell counts for this (S, T)
            # white grid: r in S, c in T; black grid: r not in S, c not in T
            wcells_dp = [0] * N2
            wcells_dm = [0] * N2
            bcells_dp = [0] * N2
            bcells_dm = [0] * N2
            wcell_list = []
            bcell_list = []
            for r in range(n):
                rin = (S >> r) & 1
                for c in range(n):
                    cin = (T >> c) & 1
                    if rin and cin:
                        wcells_dp[r + c] += 1
                        wcells_dm[r - c + n - 1] += 1
                        wcell_list.append((r, c))
                    elif not rin and not cin:
                        bcells_dp[r + c] += 1
                        bcells_dm[r - c + n - 1] += 1
                        bcell_list.append((r, c))

            # DFS over diagonal labels.  alive white cell: neither diag B.
            # state: dplab/dmlab (reset after), alive flags per cell.
            for i in range(N2):
                dplab[i] = FREE
                dmlab[i] = FREE

            walive = [True] * len(wcell_list)
            balive = [True] * len(bcell_list)
            # index cells by diagonal for fast kill/revive
            wby_dp = [[] for _ in range(N2)]
            wby_dm = [[] for _ in range(N2)]
            bby_dp = [[] for _ in range(N2)]
            bby_dm = [[] for _ in range(N2)]
            for i, (r, c) in enumerate(wcell_list):
                wby_dp[r + c].append(i)
                wby_dm[r - c + n - 1].append(i)
            for i, (r, c) in enumerate(bcell_list):
                bby_dp[r + c].append(i)
                bby_dm[r - c + n - 1].append(i)

            wcount = [len(wcell_list)]
            bcount = [len(bcell_list)]
            leaf_wit = [None]

            def kill(fam_is_dp, idx, color_becomes):
                """Label diagonal; kill cells of the excluded color.
                Returns undo list."""
                undo = []
                if color_becomes == B:
                    lst = (wby_dp if fam_is_dp else wby_dm)[idx]
                    alive, cnt = walive, wcount
                else:
                    lst = (bby_dp if fam_is_dp else bby_dm)[idx]
                    alive, cnt = balive, bcount
                for i in lst:
                    if alive[i]:
                        alive[i] = False
                        cnt[0] -= 1
                        undo.append(i)
                return undo

            def revive(fam_is_dp, color_was, undo):
                if color_was == B:
                    alive, cnt = walive, wcount
                else:
                    alive, cnt = balive, bcount
                for i in undo:
                    alive[i] = True
                    cnt[0] += 1

            def family_sum_ok():
                # L5 for each family
                for lab, wby, bby, wc, bc in (
                        (dplab, wby_dp, bby_dp, walive, balive),
                        (dmlab, wby_dm, bby_dm, walive, balive)):
                    tot = 0
                    for i in range(N2):
                        aw = sum(1 for j in wby[i] if wc[j])
                        ab = sum(1 for j in bby[i] if bc[j])
                        if lab[i] == W:
                            tot += aw
                        elif lab[i] == B:
                            tot += ab
                        else:
                            tot += aw if aw >= ab else ab
                    if tot < 2 * m:
                        return False
                return True

            def dfs():
                nonlocal nodes
                nodes += 1
                if node_limit and nodes > node_limit:
                    return "LIMIT"
                if wcount[0] < m or bcount[0] < m:
                    return "UNSAT"
                if not family_sum_ok():
                    return "UNSAT"
                # choose an unlabeled diagonal with live cells of both
                # colors (a real conflict); prefer max min(live w, live b)
                best, bfam, bidx = -1, None, None
                for fam_is_dp, lab, wby, bby in (
                        (True, dplab, wby_dp, bby_dp),
                        (False, dmlab, wby_dm, bby_dm)):
                    for i in range(N2):
                        if lab[i] != FREE:
                            continue
                        aw = sum(1 for j in wby[i] if walive[j])
                        ab = sum(1 for j in bby[i] if balive[j])
                        if aw and ab:
                            score = aw if aw < ab else ab
                            if score > best:
                                best, bfam, bidx = score, fam_is_dp, i
                if best <= 0:
                    # no conflicts left: every free diagonal serves at
                    # most one color; counts are achievable.  Snapshot
                    # the live sets NOW — they are restored during
                    # unwinding (bug caught by the independent checker).
                    leaf_wit[0] = (list(walive), list(balive))
                    return "SAT"
                lab = dplab if bfam else dmlab
                for color in (W, B):
                    lab[bidx] = color
                    undo = kill(bfam, bidx, color)
                    r = dfs()
                    revive(bfam, color, undo)
                    lab[bidx] = FREE
                    if r != "UNSAT":
                        return r
                return "UNSAT"

            r = dfs()
            if r == "LIMIT":
                return "LIMIT", None, nodes
            if r == "SAT":
                witness = None
                if collect_witness:
                    wal, bal = leaf_wit[0]
                    witness = _extract(n, m, S, T, dplab, dmlab,
                                       wcell_list, bcell_list,
                                       wal, bal)
                return "SAT", witness, nodes
    return "UNSAT", None, nodes


def _extract(n, m, S, T, dplab, dmlab, wcl, bcl, wal, bal):
    """Build a grid from the SAT leaf: alive cells of each color.
    Free diagonals at the leaf serve only one color, so alive sets are
    simultaneously realizable."""
    grid = [["."] * n for _ in range(n)]
    for i, (r, c) in enumerate(wcl):
        if wal[i]:
            grid[r][c] = "W"
    for i, (r, c) in enumerate(bcl):
        if bal[i]:
            grid[r][c] = "B"
    return ["".join(row) for row in grid]


def main():
    n, m = int(sys.argv[1]), int(sys.argv[2])
    t0 = time.time()
    status, wit, nodes = solve(n, m)
    dt = time.time() - t0
    print(f"n={n} m={m}: {status} nodes={nodes} time={dt:.2f}s")
    if wit:
        for row in wit:
            print(row)


if __name__ == "__main__":
    main()
