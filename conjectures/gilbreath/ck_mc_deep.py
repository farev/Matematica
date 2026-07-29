"""Deep Monte Carlo for c_i: extend to i = 4095 (binary digit sums to 12).

Merges with ck_montecarlo.csv (keeps whichever estimate has smaller SE).
"""

import time

import numpy as np

TIERS = [  # (depth n_max, total samples, batch)
    (1023, 1_000_000, 200_000),
    (2047, 450_000, 90_000),
    (4095, 150_000, 50_000),
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
    rng = np.random.default_rng(4095)
    t0 = time.time()
    est = {}
    old = np.loadtxt("ck_montecarlo.csv", delimiter=",", skiprows=1)
    for row in old:
        est[int(row[0])] = (row[1], row[2])
    for nmax, total, batch in TIERS:
        mean, se = run_tier(nmax, total, batch, rng)
        for i in range(nmax + 1):
            if i not in est or se[i] < est[i][1]:
                est[i] = (mean[i], se[i])
        print(f"tier n<={nmax} ({total:,} samples) done ({time.time()-t0:.0f}s)",
              flush=True)
    imax = max(est)
    out = np.array([[i, est[i][0], est[i][1]] for i in range(imax + 1)])
    np.savetxt("ck_mc_deep.csv", out, header="i,c_i,se", delimiter=",",
               comments="")
    for i in (511, 512, 1023, 1024, 2047, 2048, 4095):
        c, s = est[i]
        print(f"  c_{i} = {c:.6f} +- {s:.6f}   i*c_i = {i*c:.3f}")
    print(f"total {time.time()-t0:.0f}s")
