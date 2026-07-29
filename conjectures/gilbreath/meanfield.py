"""Testing the branching-process picture of Gilbreath defect decay.

Work in halved tail coordinates u = (entry)/2, so cooled entries are
u in {0,1} and a defect is u >= 2.  Facts proved in WRITEUP.md:

  * Descent: a defect at (k+1, j) forces a defect at (k, j) or (k, j+1).
  * Parity rigidity: u'_j = |u_j - u_{j+1}| == u_j + u_{j+1} (mod 2),
    so all parities are the XOR-Pascal (Sierpinski) image of row 1.

A defect u=2 at (k, j) has children at (k+1, j-1) and (k+1, j); child at
j survives iff u_{j+1} in {0} u {>=4}, i.e. essentially iff the right
neighbour is 0.  Naively P(neighbour = 0) ~ 1/2, giving mean offspring
~ 2 * 1/2 = 1: EXACTLY CRITICAL.  The observed exponential decay must
then come from correlations.  Here we measure everything.
"""

import numpy as np

from experiments import gaps_of_primes

if __name__ == "__main__":
    g = gaps_of_primes(10**8)
    u = (g[1:] // 2).astype(np.int16)  # halved tail of row 1
    n0 = len(u)

    print("row-by-row composition of the tail (halved coords):")
    print(f"{'k':>4} {'P(u=0)':>8} {'P(u=1)':>8} {'defects':>10} {'decay':>7} {'meas. offspring':>16}")
    prev_def = None
    for k in range(1, 176):
        nz = np.count_nonzero
        d = nz(u >= 2)
        p0 = nz(u == 0) / len(u)
        p1 = nz(u == 1) / len(u)
        decay = d / prev_def if prev_def else float("nan")
        # measured mean offspring of a defect: for each defect at j,
        # count surviving children in the next row directly
        if k in (2, 5, 10, 20, 40, 60, 80, 100, 120, 140, 160) or d == 0:
            nxt = np.abs(np.diff(u))
            dj = np.nonzero(u >= 2)[0]
            dj = dj[(dj >= 1) & (dj < len(u) - 1)]
            kids = (nxt[dj] >= 2).astype(int) + (nxt[dj - 1] >= 2).astype(int)
            off = kids.mean() if len(dj) else float("nan")
            print(f"{k:>4} {p0:>8.4f} {p1:>8.4f} {d:>10,} {decay:>7.4f} {off:>16.4f}")
        if d == 0:
            break
        prev_def = d
        u = np.abs(np.diff(u))

    print("\nparity-rigidity sanity check (lemma vs computation):")
    u1 = (g[1:] // 2).astype(np.int64)
    K, W = 24, 40  # compare row K parities on a window of width W
    u = u1.copy()
    for _ in range(K):
        u = np.abs(np.diff(u))
    from math import comb
    pred = [(sum(comb(K, i) * u1[j + i] for i in range(K + 1))) % 2 for j in range(W)]
    act = [int(x % 2) for x in u[:W]]
    print("  predicted:", pred)
    print("  actual   :", act)
    print("  match:", pred == act)
