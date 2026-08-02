"""Produce final NOTE tables and page-figure data from the capped main grid.

Usage: python3 finalize.py data/mainB_grid.csv
Writes: data/final_tables.txt (human-readable), data/page_data.js (figure data)
Everything printed is derived from certified integer columns (harmonic
columns are float64 with the documented rounding bound).
"""

import csv
import json
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
    flts = np.array([[float(v) for v in row[n_int:]] for row in raw])
    return header, ints, flts


def main(path):
    header, ints, flts = load(path)
    col = {n: j for j, n in enumerate(header)}
    x = ints[:, 0].astype(np.float64)
    xcap = int(x[-1])
    S = np.stack([ints[:, col[f"S{h}"]] for h in range(1, HMAX + 1)], axis=1
                 ).astype(np.float64)
    Lx = ints[:, col["Lx"]].astype(np.float64)
    hL = flts[:, 0]
    ell = flts[:, 1:]

    out = open("data/final_tables.txt", "w")
    def w(s=""):
        print(s); out.write(s + "\n")

    w(f"x_cap = {xcap:,} = {xcap:.3e}  ({len(x)} grid rows of {int(x[0]):,})")

    # decade table
    w("\nS_h at decades (h = 1..8), with S_h/sqrt(x):")
    decades = [10**9, 10**10, 10**11, 10**12]
    decades = [d for d in decades if d <= xcap] + ([xcap] if xcap not in
               [d for d in decades if d <= xcap] else [])
    hdr = "x          " + "".join(f"{'S'+str(h):>12}" for h in range(1, 9))
    w(hdr)
    for d in decades:
        j = np.searchsorted(x, d); j = min(j, len(x) - 1)
        w(f"{x[j]:<11.2e}" + "".join(f"{int(S[j, h-1]):>12,}" for h in range(1, 9)))
        w("  /sqrt(x): " + "".join(f"{S[j, h-1]/np.sqrt(x[j]):>12.3f}" for h in range(1, 9)))
    # normalized extremes at cap
    ratios = S[-1] / np.sqrt(x[-1])
    w(f"\nat x_cap: max_h |S_h|/sqrt(x) = {np.abs(ratios).max():.3f} "
      f"(h={int(np.abs(ratios).argmax())+1}), RMS_h = {np.sqrt((ratios**2).mean()):.3f}")
    w(f"|S_1(x_cap)|/x_cap = {abs(S[-1,0])/x[-1]:.3e}")
    w(f"L(x_cap) = {int(Lx[-1]):,},  L/sqrt(x) = {Lx[-1]/np.sqrt(x[-1]):.4f}")
    w(f"hL(x_cap) = {hL[-1]:+.4e}  (BFM: positive until 7.22e13)")

    # exponent fit on [1e8, xcap]
    rms = np.sqrt((S**2).mean(axis=1))
    sel = x >= 1e8
    A = np.vstack([np.log(x[sel]), np.ones(sel.sum())]).T
    alpha, logc = np.linalg.lstsq(A, np.log(rms[sel]), rcond=None)[0]
    w(f"\nexponent fit RMS_h S_h ~ c x^alpha on [1e8, {xcap:.1e}]: "
      f"alpha = {alpha:.4f}, c = {np.exp(logc):.3f}")

    # census extreme at cap
    cen = ints[-1, col["c0"]: col["c0"] + 256].astype(np.float64)
    mu = x[-1] / 256
    sd = np.sqrt(x[-1] * (1/256) * (255/256))
    z = (cen - mu) / sd
    w(f"census at cap: max|z| = {np.abs(z).max():.2f} at cell {int(np.abs(z).argmax())}")

    # cross-scale correlations, blocks of 20 grid units
    w("\ncross-scale increment correlation (predicted 1/sqrt2 = 0.7071):")
    n = len(x)
    D = 20
    allc = []
    for h in [1, 2, 3, 4, 6, 8]:
        Sh = S[:, h - 1]; S2h = S[:, 2*h - 1]
        i_y = np.arange(D, n // 2 - 2*D, D)
        i2 = 2 * (i_y + 1) - 1
        ok = i2 + 2*D < n
        i_y, i2 = i_y[ok], i2[ok]
        dSh = Sh[i_y + D] - Sh[i_y]
        dS2h = S2h[i2 + 2*D] - S2h[i2]
        c = np.corrcoef(dSh, dS2h)[0, 1]
        allc.append((h, len(i_y), c))
        w(f"  h={h}->{2*h}: corr = {c:+.4f}  (n = {len(i_y)} disjoint blocks)")
    cs = [c for _, _, c in allc]
    ns = [m for _, m, m2 in [(0, m, 0) for _, m, _ in allc]]
    pooled = float(np.mean(cs))
    se = float(np.std(cs, ddof=1) / np.sqrt(len(cs)))
    w(f"  pooled mean = {pooled:+.4f} +- {se:.4f} (se over 6 h-pairs)")

    # harmonic drift vs 1e9 baselines
    j9 = min(np.searchsorted(x, 1e9), len(x) - 1)
    drift = ell[-1] - ell[j9]
    w(f"\nharmonic drift ell_h(x_cap) - ell_h(1e9): max|.| = "
      f"{np.abs(drift).max():.2e} (model sigma 3.2e-5), "
      f"ell_1(x_cap) = {ell[-1,0]:+.6f}")

    # Pilatte gap
    m1 = abs(S[-1, 0]) / x[-1]
    need_c = -2 * np.log(m1) / np.log(np.log(x[-1]))
    w(f"\nparity-barrier gap: |S_1|/x = {m1:.2e} at x = {xcap:.1e}; "
      f"(log x)^(-c/2) would need c = {need_c:.1f}; "
      f"for c <= 0.06 the proven bound is >= {np.log(x[-1])**(-0.03):.3f}")

    out.close()

    # ---- page data: log-decimated series ----
    idx = np.unique(np.round(np.geomspace(1, len(x), 260)).astype(int) - 1)
    dat = {
        "x": [float(f"{v:.6g}") for v in x[idx]],
        "S": [[float(f"{S[i, h]:.6g}") for i in idx] for h in range(8)],
        "L": [float(f"{Lx[i]:.6g}") for i in idx],
        "ell1": [float(f"{ell[i,0]:.6g}") for i in idx],
        "rms": [float(f"{rms[i]:.6g}") for i in idx],
        "xcap": xcap,
    }
    with open("data/page_data.js", "w") as f:
        f.write("var CHOWLA = " + json.dumps(dat) + ";\n")
    print("wrote data/final_tables.txt, data/page_data.js")


if __name__ == "__main__":
    main(sys.argv[1])
