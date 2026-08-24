"""Implementation B: independent brute-force decision of "does a pm-zero-sum-free
set of size L exist over Z_m1 x ... x Z_mr?".

Deliberately shares NO code or method with dpm_core.py:
  * enumeration: itertools.combinations over sign-class representatives
    (dpm_core: DFS with incremental reachable sets);
  * test: every signed pattern in {-1,0,+1}^L (up to global sign, first
    nonzero fixed to +1) evaluated directly against each combination with
    numpy integer matrix products (dpm_core: set-based reachability).
All arithmetic is integer; numpy dtype int64; no floats.

Usage: python3 bruteforce_check.py m1 m2 ... -- L
Prints the number of pm-zsf L-subsets (0 means none exist).
"""

import sys
import numpy as np
from itertools import combinations, product


def run(moduli, L, chunk=200_000, count_all=True):
    r = len(moduli)
    N = 1
    for m in moduli:
        N *= m

    # elements as tuples, own indexing
    elems = list(product(*[range(m) for m in moduli]))
    assert len(elems) == N

    def neg(t):
        return tuple((-a) % m for a, m in zip(t, moduli))

    # sign-class representatives (lexicographic min of {g, -g}), 0 excluded
    reps = []
    seen = set()
    for t in elems:
        if t == tuple([0] * r) or t in seen:
            continue
        seen.add(t)
        seen.add(neg(t))
        reps.append(min(t, neg(t)))
    reps_arr = np.array(reps, dtype=np.int64)  # (nc, r)
    nc = len(reps)

    # signed patterns, first nonzero coefficient = +1 (global-sign quotient)
    pats = []
    for s in product((-1, 0, 1), repeat=L):
        nz = [x for x in s if x != 0]
        if not nz or nz[0] != 1:
            continue
        pats.append(s)
    P = np.array(pats, dtype=np.int64)  # (np_, L)
    np_ = len(P)
    assert np_ == (3 ** L - 1) // 2

    combos = np.array(list(combinations(range(nc), L)), dtype=np.int64)  # (M, L)
    M = len(combos)
    total_zsf = 0
    example = None
    for lo in range(0, M, chunk):
        C = combos[lo:lo + chunk]  # (c, L)
        # coords: (c, L, r)
        coords = reps_arr[C]
        # signed sums: (c, np_, r) = P (np_,L) . coords (c,L,r)
        S = np.einsum("pl,clr->cpr", P, coords)
        Z = np.ones((len(C), np_), dtype=bool)
        for j, m in enumerate(moduli):
            Z &= (S[:, :, j] % m) == 0
        has_zero = Z.any(axis=1)  # (c,)
        good = ~has_zero
        total_zsf += int(good.sum())
        if example is None and good.any():
            i = int(np.argmax(good))
            example = [tuple(int(x) for x in reps_arr[k]) for k in C[i]]
    return {"moduli": list(moduli), "L": L, "n_classes": nc,
            "n_combinations": M, "n_pm_zsf": total_zsf, "example": example}


if __name__ == "__main__":
    argv = sys.argv[1:]
    sep = argv.index("--")
    moduli = [int(a) for a in argv[:sep]]
    L = int(argv[sep + 1])
    out = run(moduli, L)
    print(out)
