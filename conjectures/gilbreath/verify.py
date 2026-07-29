"""Large-scale verification of Gilbreath's conjecture.

Strategy (rigorous, see WRITEUP.md):

  Lemma (propagation). If a row of the difference triangle has the form
  (1, e_1, ..., e_m) with every e_i in {0, 2}, then the next row has the
  same form (with length m-1 >= 0 shrinking by one). Hence every deeper
  row inside the triangle also begins with 1.

  So: take the first n primes, iterate absolute differences, and find the
  first row k* whose tail is entirely {0, 2}.  Rows 1..k* are checked
  directly to begin with 1; rows k*+1 .. n-1 begin with 1 by the lemma.
  That verifies Gilbreath's conjecture for the first n-1 rows.

Along the way we record the "cooling front" f(k): the length of the
maximal prefix of row k (after the leading 1) that consists only of
0s and 2s.  The conjecture is equivalent to f(k) >= 1 for all k, and
the verification succeeds at the first k with f(k) = (row length - 1).
"""

import sys
import time

import numpy as np


def primes_up_to(n: int) -> np.ndarray:
    """Odds-only sieve; returns all primes <= n."""
    if n < 3:
        return np.array([2][: max(0, n - 1)], dtype=np.int64)
    half = (n - 1) // 2  # index i represents odd number 2i+1, i >= 1
    sieve = np.ones(half + 1, dtype=bool)
    sieve[0] = False  # 1 is not prime
    for i in range(1, (int(n**0.5) - 1) // 2 + 1):
        if sieve[i]:
            p = 2 * i + 1
            start = (p * p - 1) // 2
            sieve[start::p] = False
    odds = 2 * np.nonzero(sieve)[0].astype(np.int64) + 1
    return np.concatenate(([2], odds))


def verify(limit: int, front_log=None):
    t0 = time.time()
    ps = primes_up_to(limit)
    n = len(ps)
    print(f"primes <= {limit:,}: n = {n:,}  (sieve {time.time()-t0:.1f}s)")

    # Row 1 of the triangle. Entries after the first are even and bounded
    # by the largest prime gap below `limit` (282 for 10^9), so int16 is safe.
    row = np.abs(np.diff(ps)).astype(np.int16)
    del ps

    t0 = time.time()
    k = 1
    leads = []
    while True:
        lead = int(row[0])
        leads.append(lead)
        if lead != 1:
            print(f"*** ROW {k} DOES NOT START WITH 1 (starts with {lead}) ***")
            print("*** GILBREATH'S CONJECTURE IS FALSE ***")
            return
        tail = row[1:]
        # cooling front: first tail position holding a value > 2
        # (tail entries are always even, so <=2 means in {0,2})
        bad = np.nonzero(tail > 2)[0]
        f_k = int(bad[0]) if len(bad) else len(tail)
        if front_log is not None:
            front_log.append((k, f_k, len(tail)))
        if len(bad) == 0:
            print(f"row k* = {k}: tail of length {len(tail):,} is all 0s and 2s")
            print(f"=> by the propagation lemma, rows 1..{n-1:,} all begin with 1")
            print(f"=> Gilbreath's conjecture holds for the first {n-1:,} rows")
            print(f"   ({time.time()-t0:.1f}s for {k} difference rows)")
            assert all(l == 1 for l in leads)
            return k
        row = np.abs(np.diff(row))
        k += 1


if __name__ == "__main__":
    limit = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**8
    front = []
    verify(limit, front)
    # report the growth of the cooling front
    print("\ncooling front f(k) (prefix of tail that is all 0/2):")
    checkpoints = [1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
    for k, f_k, tlen in front:
        if k in checkpoints or f_k == tlen:
            print(f"  k={k:>4}  f(k)={f_k:>12,}   (row tail length {tlen:,})")
