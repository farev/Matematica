"""X1 + X2 — the exact corridor experiment (R3-ATTACK brief, experiment 1).

Corridor = right-anchored 2^B-periodic parity prefix (the FULL solution space
of the corridor system, by Lemma R3.2), values sampled as conditioned
geometric.  The brief hoped: path cells at depth >= T_cool are 0, erosion
O(T_cool), a plant V ~ 3 T_cool derails the lead at depth m.

The nilpotency corollary predicts instead: parity rows >= P vanish
identically on the cone, so genuine cooling to {0,1} would force the array
to be eventually 0 (i.e. rows eventually constant) over the window --
impossible for random magnitudes.  The array must therefore cool one 2-adic
level up, to {0,2}: parity-0 path cells carry value 2 at positive density,
erosion stays Theta(position), and the brief's plant dies.

Also measures: bad leads (value >= 2) produced by the corridor prefix ALONE
(no plant), including the alternating case P = 2.
"""

import numpy as np
from r3_common import (THETA, anchored_periodic, de_bruijn, path_values,
                       conditioned_geometric, lead_trace, value_rows,
                       z_transform)

rng = np.random.default_rng(1878)
MEAN = THETA / (1 - THETA)


def corridor_run(m, B, seed, n_extra=64):
    """Build one corridor at scale m with period 2^B; return diagnostics."""
    r = np.random.default_rng(seed)
    P = 2 ** B
    y = anchored_periodic(m, de_bruijn(B))
    # extend parities arbitrarily (i.i.d.) right of the corridor window
    y_full = np.concatenate([y, r.integers(0, 2, m + n_extra - m + 1 + 64)
                             .astype(np.uint8)])[:m + 1 + n_extra]
    a = conditioned_geometric(y_full, r)
    return y, a, P


def erosion_profile(a, m):
    pv = path_values(a, m)
    return pv, np.cumsum(pv)


def analyze_scale(m, B, seeds):
    P = 2 ** B
    print(f"\n=== corridor m={m}, P=2^{B}={P} (de Bruijn block) ===")
    ero_tot, ero_shallow, twos, bad_dens, arr = [], [], [], [], []
    for sd in seeds:
        y, a, P = corridor_run(m, B, sd)
        pv, cum = erosion_profile(a, m)
        ero_tot.append(cum[-1])
        ero_shallow.append(cum[min(2 * P, m - 1)])
        deep = pv[2 * P:]
        twos.append(np.mean(deep == 2))
        # value support on the deep path: confirm {0,2}-cooling
        arr.append(sorted(set(deep.tolist()))[:6])
        # corridor alone: bad leads at depths in [2P, m]
        lt = lead_trace(a, m)
        bad = np.nonzero(lt[2 * P:m] >= 2)[0]
        bad_dens.append(len(bad) / (m - 2 * P))
    print(f"  deep path-value support (first seeds): {arr[:3]}")
    print(f"  P(path value = 2) beyond depth 2P: "
          f"{np.mean(twos):.3f} +- {np.std(twos):.3f}")
    print(f"  erosion: shallow (<=2P rows) {np.mean(ero_shallow):.0f}, "
          f"TOTAL over m rows {np.mean(ero_tot):.0f} +- {np.std(ero_tot):.0f} "
          f"(= {np.mean(ero_tot)/m:.2f} per row; brief hoped O(T_cool)~1e2)")
    print(f"  corridor ALONE, no plant: bad-lead density on depths [2P, m]: "
          f"{np.mean(bad_dens):.3f} +- {np.std(bad_dens):.3f}")
    return float(np.mean(ero_tot)), float(np.mean(ero_shallow))


def plant_test(m, B, V, seed, label):
    y, a, P = corridor_run(m, B, seed)
    base_bad = set(np.nonzero(lead_trace(a, m + 40) >= 2)[0].tolist())
    ap = a.copy()
    ap[m] = V
    lt = lead_trace(ap, m + 40)
    new_bad = [d for d in np.nonzero(lt >= 2)[0].tolist() if d not in base_bad]
    arrive = lt[m - 1]  # leads[s] = lead of depth s+1; depth m -> index m-1
    print(f"  plant V={V:>6} ({label}): lead at depth m = {arrive}; "
          f"new bad depths near m: "
          f"{[d+1 for d in new_bad if d+1 >= m-2][:4] or 'NONE'}")
    return arrive


if __name__ == "__main__":
    seeds = range(100, 120)

    # X1: the alternating case P = 2 (order-1 de Bruijn block)
    analyze_scale(2048, 1, seeds)

    # X2: the brief's corridor, m ~ 1000, P = 32
    ero_tot, ero_sh = analyze_scale(1024, 5, seeds)

    print("\n  plant tests at m=1024, P=32 (corridor background, seed 100):")
    plant_test(1024, 5, int(3 * ero_sh), 100, "brief: 3x shallow erosion")
    plant_test(1024, 5, int(ero_tot) + 10, 100, "measured erosion + 10")
    plant_test(1024, 5, 3 * 1024, 100, "control 3m")

    # control: unconditioned background, same measurement
    print("\n=== control: i.i.d. background (no corridor), m=1024 ===")
    tot = []
    for sd in seeds:
        r = np.random.default_rng(sd)
        a = (r.geometric(1 - THETA, size=1024 + 65) - 1).astype(np.int64)
        pv, cum = erosion_profile(a, 1024)
        tot.append(cum[-1])
    print(f"  erosion over m rows: {np.mean(tot):.0f} +- {np.std(tot):.0f} "
          f"(= {np.mean(tot)/1024:.2f} per row)")
