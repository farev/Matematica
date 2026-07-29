"""Gilbreath verification for primes < 10^10 via a segmented sieve.

Tests the empirical law k*(n) ~ 0.75 (ln n)^2 out of sample:
with n = pi(10^10) = 455,052,511 it predicts k* ~ 298.
"""

import time

import numpy as np

from verify import primes_up_to


def gaps_up_to_segmented(limit, seg=2 * 10**8):
    """int16 array of gaps of all primes <= limit (first gap is 3-2=1)."""
    base = primes_up_to(int(limit**0.5) + 1)
    base_odd = base[1:]  # odd base primes
    chunks = []
    last_prime = None
    t0 = time.time()
    for lo in range(3, limit + 1, seg):
        hi = min(lo + seg - 1, limit)
        # index i represents odd number lo_odd + 2i
        lo_odd = lo if lo % 2 == 1 else lo + 1
        m = (hi - lo_odd) // 2 + 1
        sieve = np.ones(m, dtype=bool)
        for p in base_odd:
            p = int(p)
            if p * p > hi:
                break
            start = max(p * p, ((lo_odd + p - 1) // p) * p)
            if start % 2 == 0:
                start += p
            if start > hi:
                continue
            sieve[(start - lo_odd) // 2 :: p] = False
        ps = lo_odd + 2 * np.nonzero(sieve)[0].astype(np.int64)
        if last_prime is None:
            ps = np.concatenate(([2], ps))
        else:
            ps = np.concatenate(([last_prime], ps))
        if len(ps) > 1:
            chunks.append(np.diff(ps).astype(np.int16))
            last_prime = int(ps[-1])
        if (lo - 3) % (seg * 5) == 0:
            print(f"  sieved to {hi:,} ({time.time()-t0:.0f}s)", flush=True)
    return np.concatenate(chunks)


if __name__ == "__main__":
    limit = 10**10
    t0 = time.time()
    row = gaps_up_to_segmented(limit)
    n = len(row) + 1
    print(f"pi({limit:,}) = {n:,}, sieve total {time.time()-t0:.0f}s", flush=True)
    assert row[0] == 1 and int(row.max()) < 32767

    t0 = time.time()
    k = 1
    while True:
        if row[0] != 1:
            print(f"*** ROW {k} STARTS WITH {int(row[0])}: CONJECTURE FALSE ***")
            break
        if not np.any(row[1:] > 2):
            print(f"row k* = {k}: tail all 0s and 2s")
            print(f"=> Gilbreath holds for the first {n-1:,} rows "
                  f"({time.time()-t0:.0f}s for {k} rows)")
            print(f"empirical law predicted k* ~ 0.75*(ln n)^2 = "
                  f"{0.75 * np.log(n) ** 2:.0f}")
            break
        row = np.abs(np.diff(row))
        k += 1
        if k % 50 == 0:
            print(f"  row {k}, defects {np.count_nonzero(row[1:] > 2):,}", flush=True)
