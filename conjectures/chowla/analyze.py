"""Statistical analysis of a census grid: scaling, bias, cross-scale coupling.

Usage: python3 analyze.py PREFIX_grid.csv [XMAXFIT]
Everything here is NUMERICAL (descriptive statistics of certified integers).
"""

import csv
import sys

import numpy as np

HMAX = 32


def load(path):
    with open(path) as f:
        r = csv.reader(f)
        header = next(r)
        raw = list(r)
    n_int = header.index("c255") + 1
    ints = np.array([[int(v) for v in row[:n_int]] for row in raw],
                    dtype=np.int64)
    flts = (np.array([[float(v) for v in row[n_int:]] for row in raw])
            if len(header) > n_int else None)
    return header, ints, flts


def main(path, xmaxfit=None):
    header, ints, flts = load(path)
    col = {n: j for j, n in enumerate(header)}
    x = ints[:, 0].astype(np.float64)
    S = np.stack([ints[:, col[f"S{h}"]] for h in range(1, HMAX + 1)], axis=1)

    # --- scaling: RMS over h of S_h(x)/sqrt(x), and exponent fit ---
    rms = np.sqrt((S.astype(np.float64) ** 2).mean(axis=1))
    ratio = rms / np.sqrt(x)
    sel = x >= x[-1] / 100 if xmaxfit is None else (x >= 1e7) & (x <= xmaxfit)
    A = np.vstack([np.log(x[sel]), np.ones(sel.sum())]).T
    alpha, logc = np.linalg.lstsq(A, np.log(rms[sel]), rcond=None)[0]
    print(f"exponent fit  RMS_h S_h ~ c x^alpha on x in "
          f"[{x[sel][0]:.1e},{x[sel][-1]:.1e}]:  alpha = {alpha:.4f}, "
          f"c = {np.exp(logc):.3f}")
    for xx in [x[-1] / 100, x[-1] / 10, x[-1]]:
        j = np.searchsorted(x, xx)
        j = min(j, len(x) - 1)
        print(f"  x = {x[j]:.2e}:  RMS_h S_h/sqrt(x) = {ratio[j]:.4f}")

    # --- sign bias of S_h across the grid, per h and pooled ---
    frac_neg = (S < 0).mean(axis=0)
    print(f"\nsign bias: fraction of grid with S_h(x) < 0, pooled over h: "
          f"{(S < 0).mean():.4f}")
    print("  h with strongest negative occupation:",
          {h + 1: round(float(frac_neg[h]), 3)
           for h in np.argsort(-frac_neg)[:5]})
    print("  h with least negative occupation:",
          {h + 1: round(float(frac_neg[h]), 3)
           for h in np.argsort(frac_neg)[:5]})
    print(f"  S_h(xmax) < 0 for {(S[-1] < 0).sum()}/32 shifts")

    # --- census extremes at xmax ---
    cen = ints[-1, col["c0"]: col["c0"] + 256].astype(np.float64)
    mu = x[-1] / 256
    sd = np.sqrt(x[-1] * (1 / 256) * (255 / 256))
    z = (cen - mu) / sd
    print(f"\ncensus at x={x[-1]:.1e}: max|z| = {np.abs(z).max():.2f} "
          f"(cell {np.abs(z).argmax()}), Gaussian-max expectation ~ "
          f"{np.sqrt(2 * np.log(512)):.2f}")

    # --- cross-scale increment correlation (Lemma 1 + random odd part) ---
    # corr( DS_{2h}[2y, 2y+2D),  DS_h[y, y+D) ) -> 1/sqrt(2) ?
    seg = x[0]
    n = len(x)
    print("\ncross-scale increment correlations (prediction 1/sqrt2 = 0.7071):")
    for D_units in [max(1, n // 200), max(1, n // 50)]:
        D = D_units  # in grid units
        pairs = []
        for h in [1, 2, 3, 4, 6, 8]:
            i_y = np.arange(D, n // 2 - D, D)      # y = x[i] at index i
            a = np.empty(0)
            b = np.empty(0)
            Sh = S[:, h - 1].astype(np.float64)
            S2h = S[:, 2 * h - 1].astype(np.float64)
            # y grid index i -> x = (i+1) seg ; 2y index = 2(i+1)-1
            i2 = 2 * (i_y + 1) - 1
            ok = i2 + 2 * D < n
            i_y, i2 = i_y[ok], i2[ok]
            dSh = Sh[i_y + D] - Sh[i_y]
            dS2h = S2h[i2 + 2 * D] - S2h[i2]
            c = np.corrcoef(dSh, dS2h)[0, 1]
            pairs.append((h, len(i_y), c))
        cs = [c for _, _, c in pairs]
        print(f"  block = {D * seg:.1e}: " +
              "  ".join(f"h{h}->h{2*h}: {c:+.3f}(n={m})"
                        for h, m, c in pairs) +
              f"   mean {np.mean(cs):+.4f}")

    # --- harmonic columns ---
    if flts is not None:
        hL = flts[:, 0]
        print(f"\nharmonic: sum lambda(n)/n at xmax = {hL[-1]:+.6f}")
        print("  ell_h(x) trajectories (h=1..8) at decades:")
        for xx in [1e6, 1e7, 1e8, 1e9, 1e10, 1e11, 1e12]:
            if xx <= x[-1]:
                j = min(np.searchsorted(x, xx), len(x) - 1)
                vals = "  ".join(f"{flts[j, h]:+.4f}" for h in range(1, 9))
                print(f"   x={xx:.0e}: {vals}")


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else None)
