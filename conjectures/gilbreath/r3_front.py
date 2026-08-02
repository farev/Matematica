"""X5 — the heat-front experiment: can a {0,2}-ocean invade a cooled {0,1}
strip leftward and re-derail the lead?

Setup: top parities are i.i.d. on columns [0, W) (the strip) and 2^B-periodic
de Bruijn on [W, N) (the ocean).  Values conditioned geometric.  The ocean's
cells are all even (nilpotency) and cool to {0,2}; the strip cools to {0,1}.
Bad leads at depths >> T_cool require value-2 cells to cross the strip.

Measured per depth s:
  ell(s)   = leftmost column with value >= 2 (the front position)
  lead(s)  = lead value
Reported: front trajectory summary, first bad-lead depth beyond 3*T_cool,
bad-lead density in depth bands, front arrival vs strip width scaling.
"""

import numpy as np
from r3_common import THETA, de_bruijn, conditioned_geometric

T_COOL_GUESS = 20


def run(W, N, B, seed):
    r = np.random.default_rng(seed)
    y = np.empty(N, dtype=np.uint8)
    y[:W] = r.integers(0, 2, W)
    y[W:] = de_bruijn(B)[np.arange(W, N) % (2 ** B)]
    a = conditioned_geometric(y, r)
    x = a.copy()
    depths = N - 1
    ell = np.full(depths, -1, dtype=np.int64)
    lead = np.empty(depths, dtype=np.int64)
    for s in range(depths):
        x = np.abs(x[1:] - x[:-1])
        lead[s] = x[0]
        hot = np.nonzero(x >= 2)[0]
        ell[s] = hot[0] if len(hot) else -1
    return ell, lead


def summarize(W, N, B, seeds):
    arrivals, densities, front_at = [], [], []
    for sd in seeds:
        ell, lead = run(W, N, B, sd)
        depths = np.arange(1, N)
        # bad leads beyond the strip's own cooling transient
        bad = depths[(lead >= 2) & (depths > 3 * T_COOL_GUESS)]
        arrivals.append(int(bad.min()) if len(bad) else -1)
        # density in the second half of the ocean's lifetime
        lo, hi = N // 2, N - W - 1
        seg = lead[lo:hi]
        densities.append(float(np.mean(seg >= 2)))
        # front position at a few checkpoints
        cps = [N // 8, N // 4, N // 2, 3 * N // 4]
        front_at.append([int(ell[c]) for c in cps])
    print(f"W={W:>5} N={N:>6} P=2^{B}: first bad lead beyond transient: "
          f"{sorted(arrivals)}")
    print(f"     bad-lead density in depths [{N//2}, {N-W-1}): "
          f"{np.mean(densities):.3f} +- {np.std(densities):.3f}")
    fa = np.array(front_at)
    print(f"     front ell(s) at s = N/8, N/4, N/2, 3N/4 "
          f"(median over seeds): {np.median(fa, axis=0).astype(int).tolist()}")
    return arrivals


if __name__ == "__main__":
    seeds = range(300, 308)
    # scaling in strip width W, ocean big enough to stay alive
    for W in (128, 256, 512, 1024):
        summarize(W, 16 * W, 5, seeds)
