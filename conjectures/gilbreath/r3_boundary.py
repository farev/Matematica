"""X7 — the viability boundary: period P vs entry scale (the cooling race).

For the full-sequence period-P de Bruijn parity construction (conditioned
geometric entries, mean mu), the {0,2} phase at the lead survives iff the
parity rows die (depth P) before the value field cools to {0,1}
(depth T_cool ~ c log mu).  Measures bad-lead density at depths [4P, 32P]
across a (P, mu) grid; the phase boundary should follow mu ~ exp(c P).

This is the quantitative content of the 'noose': fixed-order insufficiency
at order K = log2 P costs entry scale exp(exp(K)); and no single sequence
with o(n)-bounded entries can keep growing-period structure hot at the lead.
"""

import numpy as np
from r3_common import de_bruijn, conditioned_geometric


def bad_density(P, mu, seed, span=32):
    theta = mu / (1 + mu)
    N = max(2048, span * P + 64)
    B = int(np.log2(P))
    y = de_bruijn(B)[np.arange(N) % P]
    r = np.random.default_rng(seed)
    g = r.geometric(1 - theta ** 2, size=N).astype(np.int64) - 1
    a = 2 * g + y
    x = a.copy()
    lo, hi = 4 * P, min(span * P, N - 2)
    bad = 0
    for s in range(1, hi + 1):
        x = np.abs(x[1:] - x[:-1])
        if s >= lo:
            bad += int(x[0] >= 2)
    return bad / (hi - lo + 1)


if __name__ == "__main__":
    grid_P = [8, 32, 64, 128, 256]
    grid_mu = [8, 64, 512, 4096, 32768, 262144]
    print("bad-lead density at depths [4P, 32P], 3 seeds "
          "(rows: P; cols: entry scale mu)")
    print("        " + "".join(f"mu=2^{int(np.log2(m)):>2}   " for m in grid_mu))
    for P in grid_P:
        cells = []
        for mu in grid_mu:
            d = [bad_density(P, mu, sd) for sd in (700, 701, 702)]
            cells.append(f"{np.mean(d):.3f}+-{np.std(d):.3f}")
        print(f"P={P:>4}  " + "  ".join(cells))
