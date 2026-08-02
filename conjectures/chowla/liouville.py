"""Exact segmented sieve for the Liouville function.

lambda_block(L, R) returns an int8 array a with a[i] = lambda(L+i) for
L <= n < R.  Integer arithmetic only in the critical path: for each n we
track the product of its prime-power divisors with p <= sqrt(R); if that
product is < n, exactly one prime factor > sqrt(R) remains and contributes
1 to Omega(n).  No floating point anywhere.

Validated against brute-force trial division (test_liouville.py) and
against published values of L(x) = sum_{n<=x} lambda(n).
"""

import numpy as np


def primes_up_to(n: int) -> np.ndarray:
    """All primes <= n, by plain Eratosthenes (int64)."""
    if n < 2:
        return np.zeros(0, dtype=np.int64)
    sieve = np.ones(n + 1, dtype=bool)
    sieve[:2] = False
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p:: p] = False
    return np.nonzero(sieve)[0].astype(np.int64)


def _isqrt(n: int) -> int:
    import math
    return math.isqrt(n)


def lambda_block(L: int, R: int, primes: np.ndarray | None = None) -> np.ndarray:
    """lambda(n) for n in [L, R) as int8 (+1 / -1).  Requires L >= 1."""
    assert L >= 1
    size = R - L
    if primes is None:
        primes = primes_up_to(_isqrt(R - 1))
    # parity of the number of small prime-power divisors, and the product of
    # the small-prime part of n (exact, fits in int64 since n < 2^63)
    par = np.zeros(size, dtype=np.int8)
    acc = np.ones(size, dtype=np.int64)
    for p in primes:
        p = int(p)
        q = p
        while q < R:
            start = ((L + q - 1) // q) * q - L  # first index divisible by q
            if start < size:
                par[start::q] ^= 1
                acc[start::q] *= p
            q *= p
    n_vals = np.arange(L, R, dtype=np.int64)
    large = (acc < n_vals).astype(np.int8)  # one prime factor > sqrt(R-1) left
    lam = np.where((par ^ large) & 1, -1, 1).astype(np.int8)
    return lam


def lambda_brute(n: int) -> int:
    """Reference implementation: full trial division."""
    om = 0
    m = n
    d = 2
    while d * d <= m:
        while m % d == 0:
            om += 1
            m //= d
        d += 1
    if m > 1:
        om += 1
    return -1 if om & 1 else 1
