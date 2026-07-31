"""Score P7 and P8a from a certified quad grid (NUMERICAL).

Usage: python3 quad_analysis.py data/quadA_grid.csv
"""

import sys

import numpy as np

from certify_quad import load
from quad_run import BASES, DOUBLES, qname


def main(path):
    header, rows = load(path)
    col = {n: j for j, n in enumerate(header)}
    x = rows[:, 0].astype(np.float64)
    n = len(rows)
    Q = {q: rows[:, col[qname(q)]].astype(np.float64) for q in BASES + DOUBLES}

    print("P7: size of the 12 quadruple correlations")
    for xx in [1e10, x[-1]]:
        j = min(np.searchsorted(x, xx), n - 1)
        vals = np.array([Q[q][j] / np.sqrt(x[j]) for q in BASES + DOUBLES])
        print(f"  x = {x[j]:.1e}:  RMS = {np.sqrt((vals**2).mean()):.3f}   "
              f"max|.| = {np.abs(vals).max():.3f}   "
              f"(registered: RMS in [0.55, 1.35], max < 3.5)")
    j = n - 1
    print("  values at x_max, base then double:")
    for base, dbl in zip(BASES, DOUBLES):
        print(f"    {qname(base):>6}: {Q[base][j]/np.sqrt(x[j]):+7.3f}   "
              f"{qname(dbl):>6}: {Q[dbl][j]/np.sqrt(x[j]):+7.3f}")

    print("\nP8a: quad descent echo, Δ = 20 grid units")
    D = 20
    i_y = np.arange(D, n // 2 - 2 * D, D)
    i2 = 2 * (i_y + 1) - 1
    ok = i2 + 2 * D < n
    i_y, i2 = i_y[ok], i2[ok]
    cs = []
    for base, dbl in zip(BASES, DOUBLES):
        dQb = Q[base][i_y + D] - Q[base][i_y]
        dQd = Q[dbl][i2 + 2 * D] - Q[dbl][i2]
        c = np.corrcoef(dQb, dQd)[0, 1]
        cs.append(c)
        print(f"  {qname(base)} -> {qname(dbl)}: {c:+.4f}  (n = {len(i_y)})")
    print(f"  pooled: {np.mean(cs):+.4f} +- {np.std(cs, ddof=1)/np.sqrt(len(cs)):.4f}"
          f"   (registered band [0.66, 0.75]; parameter-free value 0.7071)")


if __name__ == "__main__":
    main(sys.argv[1])
