#!/usr/bin/env python3
"""Engine cross-validation: an independent pure-Python exhaustive search
(itertools combinations, no shared code with sds_search.c) run on small
cells; witness lists must match the C engine's EXACTLY (same reduction:
0 in P), and every witness must pass sdslib.check_sds.

Run from inside conjectures/signed-difference-sets/.
"""

import subprocess
import sys
from itertools import combinations

import sdslib


def py_exhaust(v, k, lam, G):
    """All SDS with 0 in P, as sorted (P_indices, M_indices) tuples."""
    s = sdslib.s_of(v, k, lam)
    assert s is not None and (k + s) % 2 == 0
    nP, nM = (k + s) // 2, (k - s) // 2
    add = sdslib.index_add_table(G)
    neg = sdslib.neg_index(G)
    out = []
    rest = list(range(1, v))
    for Pw in combinations(rest, nP - 1):
        P = (0,) + Pw
        inP = set(P)
        restM = [x for x in rest if x not in inP]
        for M in combinations(restM, nM):
            A = [0] * v
            for g in P:
                A[g] = 1
            for g in M:
                A[g] = -1
            ok = True
            for d in range(1, v):
                nd = neg[d]
                c = 0
                for g in P:
                    c += A[add[g][nd]]
                for g in M:
                    c -= A[add[g][nd]]
                if c != lam:
                    ok = False
                    break
            if ok:
                out.append((P, tuple(M)))
    return sorted(out)


def c_engine(v, k, lam, G):
    facs = ",".join(str(x) for x in G)
    r = subprocess.run(
        ["./sds_search", str(v), str(k), str(lam), facs, "--cap=1000000"],
        capture_output=True, text=True, check=True)
    wit = []
    for line in r.stdout.splitlines():
        if line.startswith("WITNESS"):
            p_part = line.split("P=")[1].split(" M=")[0]
            m_part = line.split("M=")[1]
            P = tuple(int(x) for x in p_part.split(",") if x != "")
            M = tuple(int(x) for x in m_part.split(",") if x != "")
            wit.append((tuple(sorted(P)), tuple(sorted(M))))
    result = [l for l in r.stdout.splitlines() if l.startswith("RESULT")][0]
    return sorted(wit), result


def coords_of(idx, G):
    c = []
    for n in reversed(G):
        c.append(idx % n)
        idx //= n
    return list(reversed(c)) if len(G) > 1 else c[0]


CELLS = [
    (5, 4, -1, [5]),
    (9, 8, 1, [3, 3]),
    (9, 8, -1, [3, 3]),
    (11, 6, 1, [11]),
    (10, 7, 2, [10]),
    (13, 12, -1, [13]),
    (18, 15, 2, [3, 6]),      # Open cell: decided by both implementations
    (20, 17, 8, [2, 10]),     # Open cell
]


def main():
    allok = True
    for (v, k, lam, G) in CELLS:
        pyw = py_exhaust(v, k, lam, G)
        cw, result = c_engine(v, k, lam, G)
        match = pyw == cw
        # independent verification of every witness
        ver = all(
            sdslib.check_sds(v, k, lam, G,
                             [coords_of(i, G) for i in P],
                             [coords_of(i, G) for i in M])[0]
            for (P, M) in cw)
        print(f"SDS({v},{k},{lam},{G}): python={len(pyw)} C={len(cw)} "
              f"match={match} witnesses_verify={ver}")
        print(f"    {result}")
        if not match or not ver:
            allok = False
    print("ENGINE CROSS-VALIDATION", "OK" if allok else "FAILED")
    sys.exit(0 if allok else 1)


if __name__ == "__main__":
    main()
