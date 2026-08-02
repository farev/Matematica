"""X6 — nested-block construction, two scales: does the lead stay hot forever?

y is EXACTLY P2-periodic on [0, N): block g2 = [old prefix (P1-periodic,
length m1)][fresh de Bruijn tail].  Nilpotency is content-free: parity rows
>= P2 vanish identically, so the whole array below depth P2 is even and the
level-2 ({0,2}) structure covers every column INCLUDING the lead.  Prediction:
bad leads (= 2) at positive density for all depths >= ~P2 + level-2 cooling,
all the way to exhaustion -- in contrast to the layered construction
(r3_hierarchical.py), which sealed at the first generic band.

Also: k-window count deviations at truncations x = P2, 4 P2, 16 P2, N,
against sqrt(x) (weak budget) -- the stale head repeats coherently, the
predicted deviation is (x/P2) * (head bias), fixable by sparse repair
defects (theory; not implemented here).
"""

import numpy as np
from collections import Counter
from r3_common import THETA, de_bruijn, conditioned_geometric

M1 = 64          # old prefix length (itself P1=8-periodic)
P2 = 4096        # scale-2 period
N = 65536        # two-scale range (16 copies of g2)


def build():
    g1 = de_bruijn(3)                          # period 8
    old = g1[np.arange(M1) % 8]
    tail = de_bruijn(12)[:P2 - M1]             # fresh order-12 de Bruijn tail
    g2 = np.concatenate([old, tail])
    return g2[np.arange(N) % P2]


def lead_and_parity(a):
    x = np.asarray(a, dtype=np.int64).copy()
    lv = np.empty(len(a) - 1, dtype=np.int64)
    for s in range(len(a) - 1):
        x = np.abs(x[1:] - x[:-1])
        lv[s] = x[0]
    return lv


if __name__ == "__main__":
    y = build()
    print(f"nested 2-scale: N={N}, P2={P2}, stale head {M1} "
          f"({100*M1/P2:.1f}% of block)")

    dens_bands = [(P2 + 200, 2 * P2), (2 * P2, 4 * P2), (4 * P2, 8 * P2),
                  (8 * P2, 16 * P2 - 2)]
    for sd in (500, 501, 502):
        a = conditioned_geometric(y, np.random.default_rng(sd))
        lv = lead_and_parity(a)
        lvd = np.empty(N, dtype=np.int64)
        lvd[1:] = lv[:N - 1]
        lvd[0] = 0
        out = []
        for lo, hi in dens_bands:
            seg = lvd[lo:hi]
            out.append(f"[{lo},{hi}): {np.mean(seg >= 2):.3f}")
        deepest = int(np.max(np.nonzero(lvd >= 2)[0]))
        print(f"  seed {sd}: bad-lead density " + "  ".join(out)
              + f"  deepest bad {deepest}")

    # window statistics at truncations (single seed, k = 1..5)
    a = conditioned_geometric(y, np.random.default_rng(500))
    th = THETA
    for x in (P2, 4 * P2, 16 * P2):
        line = []
        for k in range(1, 6):
            n = x - k + 1
            code = np.zeros(n, dtype=np.int64)
            for j in range(k):
                code = code * 512 + a[j:j + n]
            cnt = Counter(code.tolist())
            dev = 0.0
            for pat, c in cnt.items():
                digs = []
                t = pat
                for _ in range(k):
                    digs.append(t % 512)
                    t //= 512
                p = np.prod([(1 - th) * th ** d for d in digs])
                dev = max(dev, abs(c - n * p))
            line.append(f"k={k}:{dev:7.1f}")
        print(f"  x={x:>6} sqrt(x)={np.sqrt(x):6.0f}  " + "  ".join(line))
