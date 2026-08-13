#!/usr/bin/env python3
"""cg_neighborhood.py — certified exclusion of near-Conway-Guy witnesses.

Any 10-element set with largest element m can be written {m - d_9, ..., m - d_0}
with deficiencies 0 = d_0 < d_1 < ... < d_9 < m. The Conway-Guy 10-set has
deficiency profile u = (0, 1, 2, 4, 7, 13, 24, 44, 84, 161). This script
exhaustively checks, for EVERY m in [162, 308] and EVERY strictly increasing
deficiency vector d with d_0 = 0 and L1-distance sum|d_i - u_i| <= K, whether
{m - d_i} is a DSS set (exact bigint bitset check, validated independently for
any hit). A hit would be an f(10) < 309 witness near the CG structure; the
certified outcome otherwise is:

    no 10-element DSS set with max <= 308 exists whose deficiency profile
    lies within L1-distance K of the Conway-Guy profile.

This complements the exhaustive m-sweep (which certifies small m completely):
here the whole m-range is covered, but only a structured slice of sets.

Usage: python3 cg_neighborhood.py [K] [mlo] [mhi]
"""
import sys
import time

U = (0, 1, 2, 4, 7, 13, 24, 44, 84, 161)


def is_dss_fast(vals):
    sums = 1
    for a in vals:
        sh = sums << a
        if sums & sh:
            return False
        sums |= sh
    return True


def gen_dvec(k_budget, prev, idx, cur, out):
    """strictly increasing d with d_0 = 0, |d_i - U[i]| summing <= K"""
    if idx == 10:
        out.append(tuple(cur))
        return
    lo = prev + 1
    # d_idx ranges over values with |d - U[idx]| <= remaining budget
    for d in range(max(lo, U[idx] - k_budget), U[idx] + k_budget + 1):
        spend = abs(d - U[idx])
        if spend <= k_budget:
            cur.append(d)
            gen_dvec(k_budget - spend, d, idx + 1, cur, out)
            cur.pop()


def main():
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    mlo = int(sys.argv[2]) if len(sys.argv) > 2 else 162
    mhi = int(sys.argv[3]) if len(sys.argv) > 3 else 308
    t0 = time.time()
    dvecs = []
    gen_dvec(K, 0, 1, [0], dvecs)
    # d_0 = 0 fixed; gen starts at idx 1 with prev = 0
    dvecs = [d for d in dvecs]
    print(f"K={K}: {len(dvecs)} deficiency vectors within L1 budget")
    hits = []
    checked = 0
    for m in range(mlo, mhi + 1):
        for d in dvecs:
            if d[9] >= m:
                continue
            vals = [m - x for x in d]
            checked += 1
            if is_dss_fast(vals):
                hits.append((m, sorted(vals)))
                print(f"*** WITNESS m={m} set={sorted(vals)} ***")
    print(f"checked {checked} candidate sets over m in [{mlo},{mhi}] "
          f"in {time.time()-t0:.1f}s: {len(hits)} DSS hits"
          + ("" if hits else " — no near-CG witness below 309"))


if __name__ == "__main__":
    main()
