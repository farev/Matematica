"""High-precision Monte Carlo for the CHT continuous-model sequence c_i.

c_i = E[bottom entry of the Gilbreath triangle on i+1 iid Exp(1) variables]
    = E[a_{(i,j)}] for the stationary array (CHT eq. (1.5)).

CHT computed c_0=1, c_1=1, c_2=7/9, c_3=227/288 exactly, simulated to
i = 20 with 10^6 samples, conjectured c_i ~ 1/i, and stated they cannot
prove even boundedness.  Here we push the simulation to i = 1023 with
tiered sample sizes, and test:
  (a) the 1/i conjecture (behavior of i * c_i),
  (b) fine structure vs. the binary digit sum s(i) (their Lucas remark).

Tiers overlap so the estimates cross-validate.
"""

import sys
import time

import numpy as np

TIERS = [  # (depth n_max, total samples, batch)
    (63, 40_000_000, 2_000_000),
    (255, 6_000_000, 500_000),
    (1023, 600_000, 150_000),
]


def run_tier(nmax, total, batch, rng):
    sums = np.zeros(nmax + 1)
    sumsq = np.zeros(nmax + 1)
    done = 0
    while done < total:
        b = min(batch, total - done)
        x = rng.exponential(size=(b, nmax + 1)).astype(np.float32)
        for i in range(nmax + 1):
            col = x[:, 0].astype(np.float64)
            sums[i] += col.sum()
            sumsq[i] += (col * col).sum()
            if i < nmax:
                x = np.abs(x[:, :-1] - x[:, 1:])
        done += b
    mean = sums / total
    se = np.sqrt(np.maximum(sumsq / total - mean**2, 0) / total)
    return mean, se


if __name__ == "__main__":
    rng = np.random.default_rng(288227)  # c_3 = 227/288
    t0 = time.time()
    est = {}
    for nmax, total, batch in TIERS:
        mean, se = run_tier(nmax, total, batch, rng)
        for i in range(nmax + 1):
            if i not in est or se[i] < est[i][1]:
                est[i] = (mean[i], se[i])
        print(f"tier n<={nmax} ({total:,} samples) done "
              f"({time.time()-t0:.0f}s)", flush=True)

    imax = max(est)
    c = np.array([est[i][0] for i in range(imax + 1)])
    e = np.array([est[i][1] for i in range(imax + 1)])
    np.savetxt("ck_montecarlo.csv",
               np.column_stack([np.arange(imax + 1), c, e]),
               header="i,c_i,se", delimiter=",", comments="")

    print("\nknown exact values check:")
    for i, v in [(0, 1.0), (1, 1.0), (2, 7 / 9), (3, 227 / 288)]:
        print(f"  c_{i}: MC {c[i]:.5f} +- {e[i]:.5f}   exact {v:.5f}   "
              f"dev {(c[i]-v)/e[i]:+.1f} sigma")

    print("\nselected values of i * c_i (the 1/i test):")
    for i in (4, 8, 16, 32, 64, 128, 256, 512, 1023):
        print(f"  i={i:>5}  c_i={c[i]:.5f}+-{e[i]:.5f}   i*c_i = {i*c[i]:.3f}")

    print("\ni*c_i grouped by binary digit sum s(i), for i in [64, 512]:")
    lo, hi = 64, 512
    s = np.array([bin(i).count('1') for i in range(imax + 1)])
    for sv in range(1, 10):
        mask = (np.arange(imax + 1) >= lo) & (np.arange(imax + 1) <= hi) & (s == sv)
        if mask.sum() > 0:
            vals = (np.arange(imax + 1) * c)[mask]
            print(f"  s(i)={sv}: mean i*c_i = {vals.mean():.3f} "
                  f"(n={mask.sum()}, sd {vals.std():.3f})")

    print("\npowers of two vs neighbors:")
    for i in (32, 64, 128, 256, 512):
        print(f"  c_{i-1}={c[i-1]:.5f}  c_{i}={c[i]:.5f}  c_{i+1}={c[i+1]:.5f}")
    print(f"\ntotal time {time.time()-t0:.0f}s")
