#!/usr/bin/env python3
"""Independent cross-checks for the A333331 session (exact arithmetic only).

Four mutually independent computations, compared where their ranges overlap:

  A. brute(n):    lattice points of P_n by literal enumeration of {1..n}^n,
                  checking ALL 2^n - 1 subset inequalities (no sorting
                  shortcut, no DP) -- direct from Stanley's facet list.
  B. partial(n):  number of distinct in-degree vectors of partial
                  orientations of K_n (enumerating all 3^C(n,2) assignments
                  head-i/head-j/unoriented), then shifting by +1.
                  Tests the polymatroid reformulation (NOTE.md Lemma 1).
  C. loopgraphs(n): number of loop-graphs on [n] with n edges, every
                  component unicyclic (equivalently: choosable / #V=#E per
                  component).  The graph side of Wiseman's conjecture.
  D. egf(nmax):   exact series coefficients of Howroyd's conjectured
                  e.g.f. exp(-log(1-T)/2 + T/2 - T^2/4), T = tree fn.

Positive control: corrupting one inequality (sigma(k)-1) must change A.
"""
import sys
from fractions import Fraction
from itertools import product, combinations
from math import comb, factorial


def sigma(n, k):
    return k * n - k * (k - 1) // 2


# ---------- A. literal lattice-point enumeration ----------
def brute(n):
    idx = list(range(n))
    subsets = []
    for k in range(1, n + 1):
        for I in combinations(idx, k):
            subsets.append((I, sigma(n, k)))
    cnt = 0
    pts = set()
    for c in product(range(1, n + 1), repeat=n):
        ok = True
        for I, bound in subsets:
            s = 0
            for i in I:
                s += c[i]
            if s > bound:
                ok = False
                break
        if ok:
            cnt += 1
            pts.add(c)
    return cnt, pts


def brute_corrupted(n):
    """Positive control: tighten one bound by 1; count must differ."""
    idx = list(range(n))
    subsets = []
    for k in range(1, n + 1):
        for I in combinations(idx, k):
            b = sigma(n, k) - (1 if k == n else 0)
            subsets.append((I, b))
    cnt = 0
    for c in product(range(1, n + 1), repeat=n):
        if all(sum(c[i] for i in I) <= b for I, b in subsets):
            cnt += 1
    return cnt


# ---------- B. partial orientations of K_n ----------
def partial(n):
    edges = list(combinations(range(n), 2))
    vecs = set()
    for assign in product((0, 1, 2), repeat=len(edges)):
        deg = [0] * n
        for (u, v), a in zip(edges, assign):
            if a == 1:
                deg[u] += 1  # head u
            elif a == 2:
                deg[v] += 1  # head v
        vecs.add(tuple(deg))
    shifted = {tuple(d + 1 for d in v) for v in vecs}
    return len(shifted), shifted


# ---------- C. loop-graphs, n edges, all components unicyclic ----------
def loopgraphs(n):
    slots = [(i, i) for i in range(n)] + list(combinations(range(n), 2))
    cnt = 0
    for E in combinations(slots, n):
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for u, v in E:
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
        nv = {}
        ne = {}
        for x in range(n):
            nv[find(x)] = nv.get(find(x), 0) + 1
        for u, v in E:
            ne[find(u)] = ne.get(find(u), 0) + 1
        if all(nv[r] == ne.get(r, 0) for r in nv):
            cnt += 1
    return cnt


# ---------- D. Howroyd's conjectured e.g.f., exact ----------
def egf(nmax):
    # T(x) = sum_{k>=1} k^(k-1) x^k / k!
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

    # F = -log(1-T)/2 + T/2 - T^2/4 = sum_{k>=1} T^k/(2k) + T/2 - T^2/4
    F = [Fraction(0)] * (nmax + 1)
    Tk = [Fraction(1)] + [Fraction(0)] * nmax  # T^0
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
    # exp(F) via E' = F' E  (F[0]=0)
    E = [Fraction(0)] * (nmax + 1)
    E[0] = Fraction(1)
    for m in range(1, nmax + 1):
        s = Fraction(0)
        for j in range(1, m + 1):
            s += j * F[j] * E[m - j]
        E[m] = s / m
    out = []
    for m in range(1, nmax + 1):
        v = E[m] * factorial(m)
        assert v.denominator == 1, (m, v)
        out.append(v.numerator)
    return out


if __name__ == "__main__":
    nmax_small = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("== e.g.f. coefficients (Howroyd, conjectured), n=1..14:")
    for i, v in enumerate(egf(14), 1):
        print(" ", i, v)
    print("== brute lattice points vs partial-orientation vectors:")
    for n in range(1, nmax_small + 1):
        cb, pb = brute(n)
        cp, pp = partial(n)
        same_sets = pb == pp
        print(f"  n={n}: brute={cb} partial={cp} sets_equal={same_sets}")
    print("== positive control (corrupted bound must differ):")
    for n in (3, 4):
        cb, _ = brute(n)
        cc = brute_corrupted(n)
        print(f"  n={n}: honest={cb} corrupted={cc} differ={cb != cc}")
    print("== loop-graphs with unicyclic components (Wiseman objects):")
    for n in range(1, 8):
        print(f"  n={n}: u(n)={loopgraphs(n)}")
