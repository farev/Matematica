"""Analysis of the c_i Monte Carlo data against exact anchors and models.

Models tested for the CHT conjecture c_i ~ 1/i (their Remark 1.5):
  (P)  pure power law        c_i ~ A / i^alpha
  (L)  Lucas two-term model  i*c_i ~ alpha + beta * 2^s(i) * log(i) / i,
       from the heuristic that a rare large initial value M at position m+1
       (m subset of i in binary, by Lucas) survives to the bottom entry as
       an exact Sierpinski pattern, contributing ~ 2^s(i) * E[M 1_{M big}].
"""

from fractions import Fraction

import numpy as np

EXACT = {
    0: Fraction(1), 1: Fraction(1), 2: Fraction(7, 9), 3: Fraction(227, 288),
    4: Fraction(778959731701, 1447295850000),
    5: Fraction(14008668886481596262550223816901,
                25320304994525128311856832700000),
}
try:
    with open("c6_exact.txt") as f:
        num, den = f.read().strip().split("/")
        EXACT[6] = Fraction(int(num), int(den))
except FileNotFoundError:
    pass

if __name__ == "__main__":
    data = np.loadtxt("ck_montecarlo.csv", delimiter=",", skiprows=1)
    i_arr, c, se = data[:, 0].astype(int), data[:, 1], data[:, 2]

    print("=== MC vs exact anchors ===")
    for k, v in sorted(EXACT.items()):
        fv = float(v)
        print(f"  c_{k}: exact {fv:.7f}   MC {c[k]:.7f} +- {se[k]:.7f}  "
              f"({(c[k]-fv)/se[k]:+.1f} sigma)")

    s = np.array([bin(k).count("1") for k in i_arr])
    logi = np.where(i_arr > 0, np.log(np.maximum(i_arr, 1)), 0)

    lo, hi = 16, 1023
    m = (i_arr >= lo) & (i_arr <= hi)

    print("\n=== (P) power-law fit on [16,1023] ===")
    A = np.polyfit(np.log(i_arr[m]), np.log(c[m]), 1)
    print(f"  c_i ~ {np.exp(A[1]):.3f} / i^{-A[0]:.4f}")

    print("\n=== i*c_i at dyadic scales (does it converge?) ===")
    for k in (16, 24, 32, 48, 64, 96, 128, 192, 256, 384, 512, 768, 1023):
        print(f"  i={k:>5}  i*c_i = {k*c[k]:.3f} +- {k*se[k]:.3f}   s(i)={bin(k).count('1')}")

    print("\n=== (L) regression: i*c_i = alpha + beta * 2^s(i)*log(i)/i ===")
    x = (2.0 ** s[m]) * logi[m] / i_arr[m]
    y = i_arr[m] * c[m]
    X = np.column_stack([np.ones_like(x), x])
    coef, res, *_ = np.linalg.lstsq(X, y, rcond=None)
    pred = X @ coef
    ss_res = ((y - pred) ** 2).sum()
    ss_tot = ((y - y.mean()) ** 2).sum()
    print(f"  alpha = {coef[0]:.4f}, beta = {coef[1]:.4f}, "
          f"R^2 = {1 - ss_res/ss_tot:.4f}")

    print("\n=== residual i*c_i grouped by s(i), i in [64,1023] ===")
    mm = (i_arr >= 64) & (i_arr <= 1023)
    for sv in sorted(set(s[mm])):
        g = mm & (s == sv)
        if g.sum() >= 3:
            vals = i_arr[g] * c[g]
            print(f"  s={sv}: mean i*c_i = {vals.mean():.3f} +- "
                  f"{vals.std()/np.sqrt(g.sum()):.3f}  (n={g.sum()})")

    print("\n=== powers of 2 and neighbors (Lucas dips) ===")
    for k in (64, 128, 256, 512):
        print(f"  i={k-1}: {(k-1)*c[k-1]:.3f}   i={k}: {k*c[k]:.3f}   "
              f"i={k+1}: {(k+1)*c[k+1]:.3f}")
