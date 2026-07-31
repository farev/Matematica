"""Extend first-occurrence pattern coverage to k = 25, 26, 27 (test of P5).

Per segment: boolean-bitset updates only (no sorting). When a k completes
within a segment, that one segment is re-scanned in fine chunks to locate
N_k exactly (the first x by which every pattern has occurred).

Usage: python3 coverage_ext.py XMAX SEG OUTCSV
"""

import math
import sys
import time

import numpy as np

from liouville import lambda_block, primes_up_to

KS = [25, 26, 27]  # overridden by --ks


def finish_point(ck, seen_before, L):
    """Exact N_k inside this segment: smallest index i such that marking
    ck[:i+1] onto seen_before leaves nothing missing."""
    lo, hi = 0, ck.size - 1        # invariant: complete at hi, not at lo-1
    missing0 = (~seen_before).sum()
    # binary search on prefix length
    while lo < hi:
        mid = (lo + hi) // 2
        s = seen_before[ck[:mid + 1]]
        newly = np.unique(ck[:mid + 1][~s]).size
        if newly == missing0:
            hi = mid
        else:
            lo = mid + 1
    last_code = None
    s = seen_before[ck[:lo + 1]]
    cand = ck[:lo + 1][~s]
    if cand.size:
        last_code = int(cand[-1])
    return L + lo, last_code


def main():
    global KS
    xmax = int(float(sys.argv[1]))
    seg = int(float(sys.argv[2]))
    out = sys.argv[3]
    if "--ks" in sys.argv:
        KS = [int(v) for v in sys.argv[sys.argv.index("--ks") + 1].split(",")]
    kmax = max(KS)
    primes = primes_up_to(math.isqrt(xmax + seg + kmax + 2))
    seen = {k: np.zeros(1 << k, dtype=bool) for k in KS}
    done = {}
    t0 = time.time()
    for L in range(1, xmax, seg):
        if len(done) == len(KS):
            break
        lam = lambda_block(L, L + seg + kmax, primes)
        bits = (lam[:seg + kmax - 1] < 0).astype(np.int64)
        codes = np.zeros(seg, dtype=np.int64)
        for b in range(kmax):
            codes += bits[b:b + seg] << b
        for k in KS:
            if k in done:
                continue
            ck = codes & ((1 << k) - 1)
            sk = seen[k]
            before = int(sk.sum())
            snapshot = None
            if (1 << k) - before < 4 * seg:      # completion plausible soon
                snapshot = sk.copy()
            sk[ck] = True
            after = int(sk.sum())
            if after == (1 << k):
                if snapshot is None:
                    snapshot = np.zeros(1 << k, dtype=bool)  # cannot happen
                N_k, last = finish_point(ck, snapshot, L)
                done[k] = (N_k, last)
                print(f"k={k}: N_k = {N_k}  last pattern code = {last}  "
                      f"({time.time()-t0:.0f}s)", flush=True)
        if (L - 1) % (10 * seg) == 0:
            print(f"  at x={L+seg-1:.2e} "
                  f"missing: " + " ".join(f"k{k}:{(1<<k)-int(seen[k].sum())}"
                                          for k in KS if k not in done),
                  flush=True)
    with open(out, "w") as f:
        f.write("k,N_k,last_pattern_code\n")
        for k in KS:
            if k in done:
                f.write(f"{k},{done[k][0]},{done[k][1]}\n")
            else:
                miss = (1 << k) - int(seen[k].sum())
                f.write(f"{k},incomplete_at_{xmax},{miss}_missing\n")
    print("done", round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main()
