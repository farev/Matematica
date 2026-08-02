"""Certificates for the quad census: C1Q, C2Q, C3, and the cross-run
census identity against a certified reference grid.

Usage: python3 certify_quad.py QUAD_grid.csv [REF_grid.csv]
"""

import csv
import sys

import numpy as np

from quad_run import BASES, DOUBLES, qname


def load(path, n_int_stop=None):
    with open(path) as f:
        r = csv.reader(f)
        header = next(r)
        stop = header.index("c255") + 1
        rows = np.array([[int(v) for v in row[:stop]] for row in r],
                        dtype=np.int64)
    return header[:stop], rows


def main(path, ref=None):
    header, rows = load(path)
    col = {n: j for j, n in enumerate(header)}
    x = rows[:, 0]
    fails = 0

    census = rows[:, col["c0"]: col["c0"] + 256]
    if (census.sum(axis=1) != x).any():
        print("C3 FAIL"); fails += 1
    else:
        print(f"C3 OK   census sums to x at all {len(x)} rows")

    codes = np.arange(256)
    sgn = 1 - 2 * ((codes[:, None] >> np.arange(8)[None, :]) & 1)
    n_c2 = 0
    for q in BASES + DOUBLES:
        if max(q) <= 7:
            w = sgn[:, 0] * sgn[:, q[0]] * sgn[:, q[1]] * sgn[:, q[2]]
            if not np.array_equal(census @ w, rows[:, col[qname(q)]]):
                print(f"C2Q FAIL {qname(q)}"); fails += 1
            n_c2 += 1
    if fails == 0:
        print(f"C2Q OK  {n_c2} window-fitting quadruples match census Walsh sums")

    n_c1 = 0
    for base, dbl in zip(BASES, DOUBLES):
        Qd = rows[:, col[qname(dbl)]]
        Vd = rows[:, col["V" + qname(dbl)[1:]]]
        Qb = rows[:, col[qname(base)]]
        for j in range(1, len(x), 2):
            if Qd[j] != Vd[j] + Qb[(j + 1) // 2 - 1]:
                print(f"C1Q FAIL {qname(dbl)} x={x[j]}"); fails += 1
            n_c1 += 1
    if fails == 0:
        print(f"C1Q OK  quad descent at {n_c1} (pair, x) points")

    if ref:
        rh, rr = load(ref)
        rcol = {n: j for j, n in enumerate(rh)}
        m = min(len(rows), len(rr))
        a = rows[:m, col["c0"]: col["c0"] + 256]
        b = rr[:m, rcol["c0"]: rcol["c0"] + 256]
        la = rows[:m, col["Lx"]]; lb = rr[:m, rcol["Lx"]]
        if np.array_equal(a, b) and np.array_equal(la, lb):
            print(f"XR  OK  census + Lx identical to reference on {m} rows")
        else:
            print("XR  FAIL cross-run identity"); fails += 1

    print("ALL CERTIFICATES PASS" if fails == 0 else f"{fails} FAILURES")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
