"""Covariance-web analysis of the certified two-point grid (NUMERICAL).

Tests, on disjoint block increments of Delta = 20 grid units:
 (a) same-block cross-shift correlations corr(dS_h, dS_h'), model ~ 0
     (each is secretly a 4-point cancellation test);
 (b) the full cross-scale echo family corr(dS_2h(2y), dS_h(y)), model 1/sqrt2;
 (c) innovation orthogonality corr(dU_2h(2y), dS_h(y)), model ~ 0;
 (d) odd-core scaling RMS_h U_h(x)/sqrt(x/2) at decades.

Usage: python3 covariance_web.py data/mainB12_grid.csv
"""

import sys

import numpy as np

from certify import load


def main(path):
    header, rows = load(path)
    col = {n: j for j, n in enumerate(header)}
    x = rows[:, 0].astype(np.float64)
    n = len(rows)
    D = 20
    S = {h: rows[:, col[f"S{h}"]].astype(np.float64) for h in range(1, 33)}
    U = {h: rows[:, col[f"U{h}"]].astype(np.float64) for h in range(2, 33, 2)}

    # (a) same-block cross-shift matrix
    starts = np.arange(0, n - D, D)
    inc = {h: S[h][starts + D] - S[h][starts] for h in [1, 2, 3, 4, 6, 8]}
    hs = [1, 2, 3, 4, 6, 8]
    print(f"(a) same-block corr(dS_h, dS_h'), {len(starts)} blocks, D=20:")
    vals = []
    for i in range(len(hs)):
        for j in range(i + 1, len(hs)):
            c = np.corrcoef(inc[hs[i]], inc[hs[j]])[0, 1]
            vals.append(c)
            print(f"    ({hs[i]:>2},{hs[j]:>2}): {c:+.4f}", end="")
        print()
    print(f"    all 15 pairs: min {min(vals):+.4f}  max {max(vals):+.4f}  "
          f"pooled mean {np.mean(vals):+.5f}  (se per pair ~ {1/np.sqrt(len(starts)):.4f})")

    # (b) full echo family and (c) innovation orthogonality
    print("\n(b) echo corr(dS_2h(2y), dS_h(y)) and (c) corr(dU_2h(2y), dS_h(y)):")
    i_y = np.arange(D, n // 2 - 2 * D, D)
    i2 = 2 * (i_y + 1) - 1
    ok = i2 + 2 * D < n
    i_y, i2 = i_y[ok], i2[ok]
    echo, orth = [], []
    for h in range(1, 17):
        dSh = S[h][i_y + D] - S[h][i_y]
        dS2h = S[2 * h][i2 + 2 * D] - S[2 * h][i2]
        dU2h = U[2 * h][i2 + 2 * D] - U[2 * h][i2]
        e = np.corrcoef(dSh, dS2h)[0, 1]
        o = np.corrcoef(dSh, dU2h)[0, 1]
        echo.append(e); orth.append(o)
        print(f"    h={h:>2}: echo {e:+.4f}   innov-orth {o:+.4f}   (n={len(i_y)})")
    print(f"    echo pooled: {np.mean(echo):+.4f} +- {np.std(echo, ddof=1)/np.sqrt(len(echo)):.4f}"
          f"  (prediction 0.7071)")
    print(f"    orth pooled: {np.mean(orth):+.4f} +- {np.std(orth, ddof=1)/np.sqrt(len(orth)):.4f}"
          f"  (prediction 0)")

    # (d) odd-core scaling
    print("\n(d) odd-core RMS_h U_h(x)/sqrt(x/2) at decades:")
    for xx in [1e9, 1e10, 1e11, 1e12]:
        j = min(np.searchsorted(x, xx), n - 1)
        r = np.sqrt(np.mean([U[h][j] ** 2 for h in range(2, 33, 2)]) / (x[j] / 2))
        print(f"    x = {x[j]:.1e}:  {r:.3f}")


if __name__ == "__main__":
    main(sys.argv[1])
