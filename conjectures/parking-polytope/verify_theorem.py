#!/usr/bin/env python3
"""Verification of every new link in the Theorem A / Theorem B chain
(exact arithmetic throughout).

 1. S_n enumeration (multigraphs on [n], pair multiplicities <= 2, every
    component a tree or unicyclic, 2-cycles = doubled pairs allowed)
    vs a(n) from the facet DP.                     [dragon <-> multigraph]
 2. u(n) via component-count exponential formula: per-k component counts
    t_S(k) = trees + edge-doubled trees + unicyclic(>=3)  and
    t_U(k) = rooted trees (loop component) + unicyclic(>=3):
    check t_S(k) = t_U(k) exactly for k <= 12.      [dissymmetry identity]
 3. Ehrhart: #(m*Q_n cap Z^n) by dilate DP  vs
    sum over S_n of m^{s} * (m(m+1)/2)^{d}          [Theorem B, small n,m]
    vs the closed e.g.f. (1-T(mx))^{-1/2} exp((2-m)T/(2m) - T^2/(4m)).
 4. Exact convex-hull membership for n = 3, 4: the facet-description
    lattice points are EXACTLY the integer points expressible as convex
    combinations of parking functions (rational phase-1 simplex).
                                    [Stanley facet description, end-to-end]
"""
from fractions import Fraction
from itertools import product, combinations
from math import comb, factorial
import sys

sys.setrecursionlimit(10000)


def sigma(n, k):
    return k * n - k * (k - 1) // 2


def del_bound(n, k):
    """Edges of K_n meeting a k-set."""
    return comb(n, 2) - comb(n - k, 2)


# ---------- a(n) via facet DP (same algorithm as count_lattice_points) ----
def a_facet(n):
    states = {(0, 0): 1}
    for v in range(n, 0, -1):
        new = {}
        for (k, s), cnt in states.items():
            for m in range(0, n - k + 1):
                k2, s2 = k + m, s + m * v
                if s2 > sigma(n, k2):
                    break
                key = (k2, s2)
                new[key] = new.get(key, 0) + cnt * comb(n - k, m)
        states = new
    return sum(c for (k, s), c in states.items() if k == n)


# ---------- 1. S_n enumeration ----------
def components_ok(n, mult):
    """mult: dict edge->multiplicity. Every component tree or unicyclic?"""
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for (u, v), m in mult.items():
        if m:
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
    nv, ne = {}, {}
    touched = set()
    for x in range(n):
        touched.add(find(x))
    for r in touched:
        nv[r] = 0
        ne[r] = 0
    for x in range(n):
        nv[find(x)] += 1
    for (u, v), m in mult.items():
        if m:
            ne[find(u)] += m
    return all(ne[r] <= nv[r] for r in nv)


def S_count(n, with_stats=False):
    edges = list(combinations(range(n), 2))
    cnt = 0
    stats = []
    for ms in product((0, 1, 2), repeat=len(edges)):
        mult = dict(zip(edges, ms))
        if components_ok(n, mult):
            cnt += 1
            if with_stats:
                s = sum(1 for m in ms if m == 1)
                d = sum(1 for m in ms if m == 2)
                stats.append((s, d))
    return (cnt, stats) if with_stats else cnt


# ---------- 2. component-count identity ----------
def unicyclic_ge3(k):
    """Connected simple graphs on [k], exactly one cycle, length >= 3:
    number = sum_{j=3}^{k} C(k,j) * (j-1)!/2 * j * k^(k-j-1) ... use the
    standard cycle-of-rooted-trees count: (k-1 choose ...) -- compute via
    exact formula: sum over cycle length j of  k!/(j * 2 * (k-j)!) *
    (#forests of k-j vertices attached...) = j * k^{k-j-1} * ...
    Cleanest exact route: coefficient extraction from sum_{j>=3} T^j/(2j).
    """
    # exact via series in Fraction
    N = k
    T = [Fraction(0)] * (N + 1)
    for i in range(1, N + 1):
        T[i] = Fraction(i ** (i - 1), factorial(i))

    def mul(A, B):
        C = [Fraction(0)] * (N + 1)
        for i, ai in enumerate(A):
            if ai:
                for j in range(0, N + 1 - i):
                    if B[j]:
                        C[i + j] += ai * B[j]
        return C

    F = [Fraction(0)] * (N + 1)
    Tj = [Fraction(1)] + [Fraction(0)] * N
    for j in range(1, N + 1):
        Tj = mul(Tj, T)
        if j >= 3:
            for i in range(N + 1):
                F[i] += Tj[i] / (2 * j)
    v = F[k] * factorial(k)
    assert v.denominator == 1
    return v.numerator


def component_identity(kmax=12):
    ok = True
    for k in range(1, kmax + 1):
        trees = k ** (k - 2) if k >= 2 else 1
        edge_doubled = (k - 1) * (k ** (k - 2)) if k >= 2 else 0
        rooted = k ** (k - 1)
        c3 = unicyclic_ge3(k)
        tS = trees + edge_doubled + c3
        tU = rooted + c3
        if tS != tU:
            ok = False
        print(f"  k={k}: t_S={tS} t_U={tU} equal={tS == tU}")
    return ok


# ---------- 3. Ehrhart ----------
def ehrhart_dp(n, m):
    """#(m*Q_n cap Z^n): e >= 0 integer, sorted-desc prefix sums
    <= m * del_bound(n, k).  DP over values v = m(n-1) .. 0."""
    vmax = m * (n - 1)
    states = {(0, 0): 1}
    for v in range(vmax, -1, -1):
        new = {}
        for (k, s), cnt in states.items():
            for t in range(0, n - k + 1):
                k2, s2 = k + t, s + t * v
                if s2 > m * del_bound(n, k2):
                    break
                key = (k2, s2)
                new[key] = new.get(key, 0) + cnt * comb(n - k, t)
        states = new
    return sum(c for (k, s), c in states.items() if k == n)


def ehrhart_formula(n, m, stats):
    tot = 0
    for s, d in stats:
        tot += m ** s * (m * (m + 1) // 2) ** d
    return tot


def ehrhart_egf(nmax, m):
    """i(P_n, m) for n=1..nmax from exp( T(mx)/m - T/2 - T^2/(4m)
    - (1/2)log(1-T) ), T = T(mx)."""
    N = nmax
    T = [Fraction(0)] * (N + 1)
    for i in range(1, N + 1):
        T[i] = Fraction(i ** (i - 1) * m ** i, factorial(i))  # T(mx)

    def mul(A, B):
        C = [Fraction(0)] * (N + 1)
        for i, ai in enumerate(A):
            if ai:
                for j in range(0, N + 1 - i):
                    if B[j]:
                        C[i + j] += ai * B[j]
        return C

    F = [Fraction(0)] * (N + 1)
    # sum_{k>=1} T^k/(2k)  = -log(1-T)/2
    Tk = [Fraction(1)] + [Fraction(0)] * N
    for k in range(1, N + 1):
        Tk = mul(Tk, T)
        for i in range(N + 1):
            F[i] += Tk[i] / (2 * k)
        if k == 1:
            for i in range(N + 1):
                F[i] += Tk[i] * (Fraction(1, m) - Fraction(1, 2))
        if k == 2:
            for i in range(N + 1):
                F[i] -= Tk[i] / (4 * m)
    E = [Fraction(0)] * (N + 1)
    E[0] = Fraction(1)
    for mm in range(1, N + 1):
        s = Fraction(0)
        for j in range(1, mm + 1):
            s += j * F[j] * E[mm - j]
        E[mm] = s / mm
    out = []
    for i in range(1, N + 1):
        v = E[i] * factorial(i)
        assert v.denominator == 1, (i, v)
        out.append(v.numerator)
    return out


# ---------- 4. exact hull membership ----------
def parking_functions(n):
    out = []
    for c in product(range(1, n + 1), repeat=n):
        b = sorted(c)
        if all(b[i] <= i + 1 for i in range(n)):
            out.append(c)
    return out


def in_hull_exact(point, verts):
    """Phase-1 simplex with Fractions: is point a convex combination of
    verts?  Solve sum l_v * v = point, sum l_v = 1, l >= 0."""
    n = len(point)
    rows = n + 1
    cols = len(verts)
    # tableau for phase 1: minimize sum of artificials
    A = [[Fraction(verts[j][i]) for j in range(cols)] for i in range(n)]
    A.append([Fraction(1)] * cols)
    b = [Fraction(x) for x in point] + [Fraction(1)]
    # make b >= 0 (all entries already >= 0 here)
    # add artificial variables (identity)
    T = [A[i][:] + [Fraction(1) if k == i else Fraction(0)
                    for k in range(rows)] + [b[i]] for i in range(rows)]
    cost = [Fraction(0)] * cols + [Fraction(1)] * rows + [Fraction(0)]
    basis = list(range(cols, cols + rows))
    # reduced cost row = cost - sum of basic rows (since basic costs are 1)
    z = [Fraction(0)] * (cols + rows + 1)
    for i in range(rows):
        for j in range(cols + rows + 1):
            z[j] += T[i][j]
    # simplex iterations
    while True:
        piv = -1
        for j in range(cols + rows):
            if z[j] - cost[j] > 0:
                piv = j
                break
        if piv < 0:
            break
        ratio, prow = None, -1
        for i in range(rows):
            if T[i][piv] > 0:
                r = T[i][-1] / T[i][piv]
                if ratio is None or r < ratio:
                    ratio, prow = r, i
        if prow < 0:
            break  # unbounded (cannot happen here)
        pv = T[prow][piv]
        T[prow] = [x / pv for x in T[prow]]
        for i in range(rows):
            if i != prow and T[i][piv]:
                f = T[i][piv]
                T[i] = [x - f * y for x, y in zip(T[i], T[prow])]
        f = z[piv] - cost[piv]
        z = [x - f * y for x, y in zip(z, T[prow] + [Fraction(0)] * 0)]
        basis[prow] = piv
    objective = z[-1]  # remaining artificial mass
    return objective == 0


def hull_check(n):
    pf = parking_functions(n)
    facet_pts = set()
    for c in product(range(1, n + 1), repeat=n):
        srt = sorted(c, reverse=True)
        if all(sum(srt[:k]) <= sigma(n, k) for k in range(1, n + 1)):
            facet_pts.add(c)
    good = True
    n_in = 0
    for c in product(range(1, n + 1), repeat=n):
        inside = in_hull_exact(c, pf)
        claimed = c in facet_pts
        if inside != claimed:
            good = False
            print(f"    MISMATCH at {c}: hull={inside} facets={claimed}")
        if inside:
            n_in += 1
    return good, n_in, len(facet_pts)


if __name__ == "__main__":
    print("== 1. S_n (dragon multigraphs) vs a(n):")
    for n in range(1, 6):
        sc = S_count(n)
        af = a_facet(n)
        print(f"  n={n}: |S_n|={sc} a(n)={af} equal={sc == af}")
    print("== 2. per-component identity t_S(k) = t_U(k):")
    component_identity(12)
    print("== 3. Ehrhart: dilate DP vs S_n formula vs closed e.g.f.:")
    for n in range(1, 6):
        _, stats = S_count(n, with_stats=True)
        for m in range(1, 5):
            dp = ehrhart_dp(n, m)
            fo = ehrhart_formula(n, m, stats)
            eg = ehrhart_egf(n, m)[n - 1]
            print(f"  n={n} m={m}: dp={dp} formula={fo} egf={eg} "
                  f"equal={dp == fo == eg}")
    print("== 4. exact hull membership vs facet description:")
    for n in (3, 4):
        good, n_in, n_facet = hull_check(n)
        print(f"  n={n}: hull_count={n_in} facet_count={n_facet} "
              f"all_agree={good}")
