"""Experiments probing WHY Gilbreath's conjecture should be true.

1. Growth of k*(x): the first all-{0,2} row, as a function of the sieve
   limit x.  (Determines how fast the triangle "cools".)

2. Defect dynamics: density of entries > 2 ("defects") per row, and the
   max entry per row.  Exponential decay of defects is the heart of
   Odlyzko's heuristic.

3. The primes-don't-matter test: shuffle the prime gaps (destroying all
   correlations between consecutive gaps but keeping the gap multiset)
   and check whether the triangle behaves identically.  Also an i.i.d.
   geometric-gap model.

4. Fragility test: adversarial small-gap sequences that violate the
   Gilbreath property, showing the conjecture is a genuinely
   statistical fact.
"""

import numpy as np

from verify import primes_up_to


def kstar_and_defects(row1, max_rows=100000, track=False):
    """row1: int array, first difference row (lead 1, even tail).
    Returns (k*, leads_ok, stats) where stats[k] = (defect_count, max_val)."""
    row = row1.astype(np.int16)
    stats = []
    k = 1
    while True:
        if row[0] != 1:
            return k, False, stats
        tail = row[1:]
        nbad = int(np.count_nonzero(tail > 2))
        if track:
            stats.append((k, nbad, int(tail.max()) if len(tail) else 0))
        if nbad == 0:
            return k, True, stats
        row = np.abs(np.diff(row))
        k += 1
        if k > max_rows:
            return -1, True, stats


def gaps_of_primes(limit):
    ps = primes_up_to(limit)
    return np.diff(ps)


if __name__ == "__main__":
    rng = np.random.default_rng(20260728)

    print("=== 1. growth of k*(x) ===")
    print(f"{'x':>12} {'n=pi(x)':>12} {'k*':>6}")
    for e in range(5, 10):
        x = 10**e
        g = gaps_of_primes(x)
        k, ok, _ = kstar_and_defects(g)
        assert ok
        print(f"{x:>12,} {len(g)+1:>12,} {k:>6}")

    print("\n=== 2. defect decay for primes < 10^8 ===")
    g = gaps_of_primes(10**8)
    k, ok, stats = kstar_and_defects(g, track=True)
    n = len(g)
    print(f"{'k':>4} {'defects':>10} {'density':>10} {'max':>5}")
    for kk, nbad, mx in stats:
        if kk in (1, 2, 3, 5, 10, 20, 40, 80, 120, 160) or nbad == 0:
            print(f"{kk:>4} {nbad:>10,} {nbad/n:>10.2e} {mx:>5}")
    # fit decay rate on the linear-in-log stretch k in [20, 140]
    ks = np.array([s[0] for s in stats if 20 <= s[0] <= 140 and s[1] > 0])
    ds = np.array([s[1] for s in stats if 20 <= s[0] <= 140 and s[1] > 0])
    slope = np.polyfit(ks, np.log(ds), 1)[0]
    print(f"fit: defects ~ exp({slope:+.4f} k)  => decay factor {np.exp(slope):.4f}/row")

    print("\n=== 3a. shuffled prime gaps (same multiset, no correlations) ===")
    for trial in range(3):
        gs = g.copy()
        tail = gs[1:]
        rng.shuffle(tail)
        gs[1:] = tail
        k, ok, _ = kstar_and_defects(gs)
        print(f"shuffle {trial}: gilbreath-like property holds = {ok}, k* = {k}")

    print("\n=== 3b. i.i.d. even gaps, geometric-ish, mean ~ log(10^8) ===")
    for trial in range(3):
        m = len(g)
        # even gaps 2,4,6,... with P(2j) ~ (1-q) q^(j-1), mean ~ 18
        q = 1 - 2 / np.log(10**8)
        iid = 2 * rng.geometric(1 - q, size=m)
        iid[0] = 1  # keep the 2,3 start
        k, ok, _ = kstar_and_defects(iid.astype(np.int64))
        print(f"iid {trial}: gilbreath-like property holds = {ok}, k* = {k}")

    print("\n=== 4. fragility: small-gap sequences that FAIL ===")
    for gaps in ([1, 4, 2, 2, 2, 2], [1, 2, 2, 6, 2, 2, 2, 2, 2]):
        seq = np.concatenate(([2], 2 + np.cumsum(gaps)))
        row = np.abs(np.diff(seq))
        print(f"seq {list(seq)}:")
        for i in range(1, 5):
            print(f"   d^{i}: {list(row)}" + ("   <-- lead != 1" if row[0] != 1 else ""))
            if len(row) <= 1:
                break
            row = np.abs(np.diff(row))
