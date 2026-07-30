"""Numerical verification of Theorem R2's plant mechanism (REDUCTION.md).

A lone value V planted at position m in a cooling Cramér background must
ride the always-open diagonal Pascal channel (C(t,t) = 1) and derail the
lead at depth m-1, arriving with V minus the background erosion given by
the mirrored CHT telescope. Reproduces: background cools at row ~14;
plant V = 3m at m = 6000 derails first at row 5999 with value ~14962.
"""

import numpy as np

rng = np.random.default_rng(1878)


def lead_trace(a, rows):
    x = a.astype(np.float64).copy()
    leads = []
    for _ in range(rows):
        x = np.abs(x[:-1] - x[1:])
        leads.append(x[0])
    return np.array(leads)


if __name__ == "__main__":
    n = 12000
    theta = 1 - 2 / np.log(1e8)
    base = rng.geometric(1 - theta, size=n).astype(np.float64) - 1

    lb = lead_trace(base, n - 1)
    settle = int(np.max(np.nonzero(lb > 1)[0])) if np.any(lb > 1) else -1
    print(f"background settles at row {settle}")

    m = 6000
    planted = base.copy()
    planted[m] = 3 * m
    lp = lead_trace(planted, n - 1)
    bad = np.nonzero(lp > 1)[0]
    late = bad[bad > settle + 10]
    print(f"plant V=3m at m={m}: first derailed depth {late.min()+1} "
          f"(prediction: light-cone arrival depth m={m}), arrival value "
          f"{lp[late.min()]:.0f}, {len(late)} derailed rows")
    assert late.min() + 1 == m
