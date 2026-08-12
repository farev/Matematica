#!/usr/bin/env python3
"""Brute-force reference for Erdos problem #699 (Erdos-Szekeres 1978).

Statement (to be re-pinned from primary source): for all 1 <= i < j <= n/2
there is a prime p >= i with p | C(n,i) and p | C(n,j).
Strengthening: apart from finitely many (n,i,j), one can take p > i.

This script:
  1. checks the Kummer/Lucas divisibility test against direct big-int
     computation of C(n,k) mod p (positive control),
  2. sweeps all n <= N, all pairs 1 <= i < j <= floor(n/2),
  3. reports counterexamples (no p >= i) and the exceptional census
     (no p > i, i.e. only p = i works) exactly.

Exact integer arithmetic throughout. numpy used only for boolean masks.
"""
import sys
import numpy as np
from math import comb


def sieve(n):
    bs = np.ones(n + 1, dtype=bool)
    bs[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if bs[p]:
            bs[p * p:: p] = False
    return np.flatnonzero(bs)


def kummer_divides(p, n, k):
    """p | C(n,k) iff some base-p digit of k exceeds that of n (Lucas)."""
    while k:
        if k % p > n % p:
            return True
        k //= p
        n //= p
    return False


def control_kummer(nmax=120, primes=None):
    """Positive control: compare against direct big-int divisibility."""
    bad = 0
    for n in range(2, nmax + 1):
        for k in range(1, n // 2 + 1):
            c = comb(n, k)
            for p in primes[primes <= n]:
                if (c % int(p) == 0) != kummer_divides(int(p), n, k):
                    bad += 1
                    print(f"CONTROL FAIL n={n} k={k} p={p}")
    return bad


def divisibility_matrix(n, primes):
    """M[a, k] = True iff primes[a] | C(n,k), for k = 0..n//2."""
    nh = n // 2
    ks = np.arange(nh + 1, dtype=np.int64)
    ps = primes[primes <= n]
    M = np.zeros((len(ps), nh + 1), dtype=bool)
    for a, p in enumerate(ps):
        p = int(p)
        kk = ks.copy()
        nn = n
        cond = np.zeros(nh + 1, dtype=bool)
        while nn > 0:
            cond |= (kk % p) > (nn % p)
            kk //= p
            nn //= p
        M[a] = cond
    return ps, M


def sweep(N, primes, out):
    counterexamples = []
    exceptional = []   # (n, i, j) where no prime p > i divides both, but p = i does
    for n in range(4, N + 1):
        nh = n // 2
        ps, M = divisibility_matrix(n, primes)
        for i in range(1, nh):          # i < j <= nh so i <= nh-1
            row_i = M[:, i]
            adm_ge = row_i & (ps >= i)
            adm_gt = row_i & (ps > i)
            cov_ge = M[adm_ge].any(axis=0) if adm_ge.any() else np.zeros(nh + 1, bool)
            cov_gt = M[adm_gt].any(axis=0) if adm_gt.any() else np.zeros(nh + 1, bool)
            for j in range(i + 1, nh + 1):
                if not cov_ge[j]:
                    counterexamples.append((n, i, j))
                elif not cov_gt[j]:
                    exceptional.append((n, i, j))
        if n % 200 == 0:
            print(f"  n={n}: {len(counterexamples)} cex, "
                  f"{len(exceptional)} exceptional so far", flush=True)
    with open(out, "w") as f:
        f.write("# type,n,i,j  (brute-force reference, exact)\n")
        for t in counterexamples:
            f.write("CEX,%d,%d,%d\n" % t)
        for t in exceptional:
            f.write("EXC,%d,%d,%d\n" % t)
    return counterexamples, exceptional


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 800
    primes = sieve(max(N, 200))
    # cross-check the sieve against known pi(x) values
    import bisect
    for x, pix in [(100, 25), (1000, 168), (10000, 1229)]:
        if x <= len(primes) and primes[-1] >= x:
            got = int(np.searchsorted(primes, x, side="right"))
            assert got == pix, (x, got, pix)
    print("sieve control ok (pi(100)=25, pi(1000)=168, pi(10000)=1229 as applicable)")
    nbad = control_kummer(120, primes)
    print(f"kummer control: {nbad} mismatches on all (n,k,p) with n<=120")
    assert nbad == 0
    cex, exc = sweep(N, primes, "brute699_out.csv")
    print(f"\nN={N}: counterexamples={len(cex)}, exceptional triples={len(exc)}")
    for t in cex[:20]:
        print("  CEX", t)
    print("exceptional triples (all):")
    for t in exc:
        print("  EXC", t)
