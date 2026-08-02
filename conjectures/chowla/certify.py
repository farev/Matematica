"""Certificate verification for census_run.py output.

Checks EXACT integer identities that independent code paths must satisfy:

  C1 (2-adic descent, Lemma 1):  for even h and every grid point 2y:
        S_h(2y) = U_h(2y) + S_{h/2}(y)
     S_h comes from a plain pair sum, U_h from an odd-indexed pair sum,
     S_{h/2}(y) from a different row entirely.

  C2 (Walsh duality, Lemma 2):  for h = 1..7 and the recorded triples and
     quadruple: the correlation recomputed as a signed sum over the
     256-cell census equals the directly summed correlation.

  C3 (census totality):  sum of census cells = x at every row.

Any single-bit error in sieve, aggregation, or boundary handling breaks
these.  Usage:  python3 certify.py PREFIX_grid.csv
"""

import sys

import numpy as np


def load(path):
    """Load the integer (certified) columns; float harmonic columns ignored."""
    import csv
    with open(path) as f:
        r = csv.reader(f)
        header = next(r)
        n_int = header.index("c255") + 1
        rows = np.array([[int(v) for v in row[:n_int]] for row in r],
                        dtype=np.int64)
    return header[:n_int], rows


def main(path):
    header, rows = load(path)
    col = {name: j for j, name in enumerate(header)}
    x = rows[:, col["x"]]
    seg = x[0]
    failures = 0

    # C3
    census = rows[:, col["c0"]: col["c0"] + 256]
    bad = np.nonzero(census.sum(axis=1) != x)[0]
    if bad.size:
        print(f"C3 FAIL at rows {bad[:5]}"); failures += 1
    else:
        print(f"C3 OK   census sums to x at all {len(x)} grid points")

    # C2: correlations from census via Walsh sums
    codes = np.arange(256)
    sgn = 1 - 2 * ((codes[:, None] >> np.arange(8)[None, :]) & 1)  # (256,8)
    for name, offs in ([(f"S{h}", (0, h)) for h in range(1, 8)]
                       + [("T012", (0, 1, 2)), ("T024", (0, 2, 4)),
                          ("T013", (0, 1, 3)), ("Q0123", (0, 1, 2, 3))]):
        w = np.prod([sgn[:, o] for o in offs], axis=0)
        rec = census @ w
        if not np.array_equal(rec, rows[:, col[name]]):
            print(f"C2 FAIL {name}"); failures += 1
    print(f"C2 OK   S1..S7, T012, T024, T013, Q0123 match census Walsh sums"
          f" at all grid points" if failures == 0 else "")

    # C1: 2-adic descent
    n1 = 0
    for h in range(2, 33, 2):
        S_h = rows[:, col[f"S{h}"]]
        U_h = rows[:, col[f"U{h}"]]
        S_half = rows[:, col[f"S{h//2}"]]
        for j in range(len(x)):          # row j: x = (j+1) seg
            if (j + 1) % 2 == 0:
                y_row = (j + 1) // 2 - 1
                if S_h[j] != U_h[j] + S_half[y_row]:
                    print(f"C1 FAIL h={h} x={x[j]}"); failures += 1
                n1 += 1
    if failures == 0:
        print(f"C1 OK   descent identity at {n1} (h, x) pairs")

    print("ALL CERTIFICATES PASS" if failures == 0
          else f"{failures} FAILURES")
    return failures


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
