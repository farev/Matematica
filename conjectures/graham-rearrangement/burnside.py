#!/usr/bin/env python3
"""Exact orbit counts for the dilation action of F_p^* on t-subsets of F_p^*.

Independent cross-check for verify_grc.c: the engine's per-(p,t) `reps` count
must equal orbits(p, t) exactly.  Pure integer arithmetic (Burnside/Cauchy-
Frobenius over the cyclic group F_p^* of order p-1: an element of
multiplicative order d fixes exactly C((p-1)/d, t/d) subsets when d | t, else
none).

Usage:  python3 burnside.py p tmin tmax
Output: one line per t:  p t C(p-1,t) orbits
"""
import sys
from math import comb


def euler_phi(m: int) -> int:
    r, x, f = m, m, 2
    while f * f <= x:
        if x % f == 0:
            while x % f == 0:
                x //= f
            r -= r // f
        f += 1
    if x > 1:
        r -= r // x
    return r


def orbits(p: int, t: int) -> int:
    n = p - 1
    total = 0
    for d in range(1, n + 1):
        if n % d == 0 and t % d == 0:
            total += euler_phi(d) * comb(n // d, t // d)
    assert total % n == 0, (p, t, total)
    return total // n


if __name__ == "__main__":
    p, tmin, tmax = map(int, sys.argv[1:4])
    for t in range(tmin, tmax + 1):
        print(f"p={p} t={t} subsets={comb(p - 1, t)} orbits={orbits(p, t)}")
