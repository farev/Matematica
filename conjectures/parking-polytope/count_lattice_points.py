#!/usr/bin/env python3
"""Exact count of lattice points of P_n = conv(PF_n), the convex hull of
parking functions of length n (OEIS A333331).

Method: Stanley's facet description of P_n (reported and used in
Amanbayeva-Wang, arXiv:2104.08454, Section 1):

    P_n = { x in R^n :  1 <= x_i <= n  for all i, and for every
            k-subset I of [n], 2 <= k <= n:
            sum_{i in I} x_i <= (n-k+1) + (n-k+2) + ... + n =: sigma(k) }.

For integer points the binding subset of size k is the k largest
coordinates, so c in Z^n is a lattice point iff 1 <= c_i and, sorting c
in weakly decreasing order, every prefix sum satisfies
prefix_k <= sigma(k) = k*n - k*(k-1)/2.

Counting: dynamic programming over the value v = n, n-1, ..., 1 and the
multiplicity m_v of v in the multiset of coordinates, carrying the state
(#coords so far, their sum).  Within a run of equal values the constraint
gap s(k) - sigma(k) is convex in k, so checking the run endpoints
suffices (proved in NOTE.md, Lemma 2).  The count of labeled vectors per
multiset is the multinomial, accumulated exactly via binomial factors.
All arithmetic is exact (Python big integers).

Usage:  python3 count_lattice_points.py [nmax]     (default 24)
Output: a(1)..a(nmax), one per line: "n a(n)".
Cost:   nmax=24 well under a second; nmax=60 a few seconds.
"""
import sys
from math import comb


def sigma(n: int, k: int) -> int:
    """Max possible sum of the k largest coordinates: (n-k+1)+...+n."""
    return k * n - k * (k - 1) // 2


def a(n: int) -> int:
    """Number of lattice points of conv(PF_n)."""
    # DP over values v = n down to 1; state (k, s) = (#coords used, sum),
    # reachable only with s <= sigma(n, k); value = number of labeled
    # vectors built so far (choosing which of the n positions carry which
    # values, via binomials).
    states = {(0, 0): 1}
    for v in range(n, 0, -1):
        new = {}
        for (k, s), cnt in states.items():
            # add m copies of value v (m = 0 allowed)
            for m in range(0, n - k + 1):
                k2, s2 = k + m, s + m * v
                # endpoint check suffices (convexity of s - sigma in run)
                if s2 > sigma(n, k2):
                    break  # larger m only worse: s2 grows by v each step,
                    # sigma grows by n-k2 <= previous increments; once
                    # violated at the endpoint it stays violated (see
                    # NOTE.md Lemma 2 for the monotone-break argument)
                w = cnt * comb(n - k, m)
                key = (k2, s2)
                new[key] = new.get(key, 0) + w
        states = new
    return sum(cnt for (k, s), cnt in states.items() if k == n)


if __name__ == "__main__":
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    for n in range(1, nmax + 1):
        print(n, a(n))
