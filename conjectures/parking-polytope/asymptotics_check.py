#!/usr/bin/env python3
"""Numerical check of the asymptotic law  a(n) ~ C * n^(n-1/4),
C = e^(1/4) * sqrt(2*pi) / (2^(1/4) * Gamma(1/4))  (Corollary in NOTE.md),
plus a regression test a(n) == egf-coefficients for n <= 40, and an
Ehrhart-reciprocity spot check (interior lattice points vs i(P_n, -1)).

Float use here is confined to the asymptotic RATIO display (the claim
checked is an asymptotic law; the terms themselves are exact).
"""
from fractions import Fraction
from math import comb, factorial, gamma, pi, e, sqrt, log, exp
import sys

sys.set_int_max_str_digits(100000)

from count_lattice_points import a as a_facet, sigma


def egf_terms(nmax):
    T = [Fraction(0)] * (nmax + 1)
    for k in range(1, nmax + 1):
        T[k] = Fraction(k ** (k - 1), factorial(k))

    def mul(A, B):
        C = [Fraction(0)] * (nmax + 1)
        for i, ai in enumerate(A):
            if ai:
                for j in range(0, nmax + 1 - i):
                    if B[j]:
                        C[i + j] += ai * B[j]
        return C

    F = [Fraction(0)] * (nmax + 1)
    Tk = [Fraction(1)] + [Fraction(0)] * nmax
    for k in range(1, nmax + 1):
        Tk = mul(Tk, T)
        for i in range(nmax + 1):
            F[i] += Tk[i] / (2 * k)
        if k == 1:
            for i in range(nmax + 1):
                F[i] += Tk[i] / 2
        if k == 2:
            for i in range(nmax + 1):
                F[i] -= Tk[i] / 4
    E = [Fraction(0)] * (nmax + 1)
    E[0] = Fraction(1)
    for m in range(1, nmax + 1):
        s = Fraction(0)
        for j in range(1, m + 1):
            s += j * F[j] * E[m - j]
        E[m] = s / m
    return [int(E[m] * factorial(m)) for m in range(1, nmax + 1)]


def interior_count(n):
    """Interior lattice points of P_n: all facet inequalities strict."""
    # c in Z^n with 1 < c_i < n... wait: 1 <= c_i is a facet, so interior
    # needs c_i > 1 i.e. c_i >= 2, c_i <= n-1... and strict subset sums.
    # Small n only: brute force.
    from itertools import product
    cnt = 0
    for c in product(range(2, n), repeat=n):
        srt = sorted(c, reverse=True)
        ok = all(sum(srt[:k]) < sigma(n, k) for k in range(1, n + 1))
        # also single-coordinate upper bound strict: c_i < n  (k=1 covers)
        if ok:
            cnt += 1
    return cnt


if __name__ == "__main__":
    NMAX = 40
    print(f"computing a(n), egf(n) for n <= {NMAX} ...")
    A = [a_facet(n) for n in range(1, NMAX + 1)]
    E = egf_terms(NMAX)
    print("regression a==egf through", NMAX, ":", A == E)
    with open("a_values.txt", "w") as f:
        for i, v in enumerate(A, 1):
            f.write(f"{i} {v}\n")
    C = e ** 0.25 * sqrt(2 * pi) / (2 ** 0.25 * gamma(0.25))
    print(f"asymptotic constant C = {C:.6f}")
    for n in (10, 20, 30, 40):
        # ratio a(n) / (C * n^(n-1/4)) via logs
        la = log(A[n - 1])
        lpred = log(C) + (n - 0.25) * log(n)
        print(f"  n={n}: a(n)/(C n^(n-1/4)) = {exp(la - lpred):.5f}")
    print("Ehrhart reciprocity spot check ((-1)^n i(P_n,-1) = #interior):")
    for n in (2, 3, 4, 5):
        # (-1)^n i(P_n,-1) = (-1)^n * sum_{M simple in S_n} (-1)^{s(M)}
        from itertools import combinations, product
        edges = list(combinations(range(n), 2))
        tot = 0
        for ms in product((0, 1), repeat=len(edges)):
            parent = list(range(n))

            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            for (u, v), m in zip(edges, ms):
                if m:
                    ru, rv = find(u), find(v)
                    if ru != rv:
                        parent[ru] = rv
            nv, ne = {}, {}
            for x in range(n):
                nv[find(x)] = nv.get(find(x), 0) + 1
            for (u, v), m in zip(edges, ms):
                if m:
                    ne[find(u)] = ne.get(find(u), 0) + 1
            if all(ne.get(r, 0) <= nv[r] for r in nv):
                tot += (-1) ** sum(ms)
        recip = (-1) ** n * tot
        inter = interior_count(n)
        print(f"  n={n}: (-1)^n i(-1)={recip} interior={inter} "
              f"equal={recip == inter}")
