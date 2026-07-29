"""Exact rational computation of the CHT constants c_i.

c_i = E[ bottom of the Gilbreath triangle on a_1..a_{i+1} iid Exp(1) ].

Method.  Fixing the sign s of every intermediate difference delta^t_j
turns the bottom entry into a linear functional l(a) on the polyhedral cone

    C_sigma = { a >= 0,  s^t_j * delta^t_j(a) >= 0  for all t, j }.

The cones (one per feasible strict sign pattern sigma) tile R^{i+1}_{>=0}
up to measure zero.  Over a *simplicial* cone with integer rays w_1..w_d,

    int_C e^{-<1,a>} da           = |det W| * prod_k 1/s_k,
    int_C l(a) e^{-<1,a>} da      = |det W| * (prod_k 1/s_k) * sum_k l(w_k)/s_k,

with s_k = <1, w_k> > 0.  So: enumerate sign patterns depth-first with LP
pruning, get each cone's extreme rays by exact double description,
triangulate (Delaunay for combinatorics only; all arithmetic exact),
and sum.  Certificate: sum over all cones of the e^{-<1,a>} integrals
must equal exactly 1.

Validation: reproduces c_1 = 1, c_2 = 7/9, c_3 = 227/288 (CHT Section 1.3).
"""

import sys
import time
from fractions import Fraction
from math import gcd

import numpy as np
from scipy.optimize import linprog
from scipy.spatial import Delaunay


# ---------------------------------------------------------------- exact bits

def primitive(v):
    g = 0
    for x in v:
        g = gcd(g, abs(x))
    return tuple(x // g for x in v) if g else tuple(v)


def det_bareiss(mat):
    """Exact integer determinant (Bareiss), mat = list of rows of ints."""
    m = [list(r) for r in mat]
    n = len(m)
    sign, prev = 1, 1
    for k in range(n - 1):
        if m[k][k] == 0:
            for r in range(k + 1, n):
                if m[r][k] != 0:
                    m[k], m[r] = m[r], m[k]
                    sign = -sign
                    break
            else:
                return 0
        for r in range(k + 1, n):
            for c in range(k + 1, n):
                m[r][c] = (m[r][c] * m[k][k] - m[r][k] * m[k][c]) // prev
        prev = m[k][k]
    return sign * m[-1][-1]


def dd_rays(constraints, d):
    """Extreme rays of {x in R^d : x >= 0, B x >= 0}, exact integer DD.
    constraints: list of integer tuples (rows of B)."""
    all_cons = [tuple(1 if i == j else 0 for i in range(d)) for j in range(d)]
    all_cons += [tuple(c) for c in constraints]
    rays = [tuple(1 if i == j else 0 for i in range(d)) for j in range(d)]
    # zero-set bitmask of each ray w.r.t. all_cons (recomputed as we go)
    nc = len(all_cons)

    def zmask(r, upto):
        m = 0
        for ci in range(upto):
            if sum(a * b for a, b in zip(all_cons[ci], r)) == 0:
                m |= 1 << ci
        return m

    processed = d  # first d constraints (orthant) already satisfied by init
    for ci in range(d, nc):
        h = all_cons[ci]
        vals = [sum(a * b for a, b in zip(h, r)) for r in rays]
        P = [i for i, v in enumerate(vals) if v > 0]
        Z = [i for i, v in enumerate(vals) if v == 0]
        N = [i for i, v in enumerate(vals) if v < 0]
        if not N:
            processed = ci + 1
            continue
        masks = [zmask(r, ci) for r in rays]
        newrays = [rays[i] for i in P + Z]
        for ip in P:
            for im in N:
                common = masks[ip] & masks[im]
                # adjacency: no third ray's zero-set contains the common one
                adjacent = True
                for io in range(len(rays)):
                    if io != ip and io != im and (masks[io] & common) == common:
                        adjacent = False
                        break
                if adjacent:
                    w = tuple(vals[ip] * rays[im][k] - vals[im] * rays[ip][k]
                              for k in range(d))
                    newrays.append(primitive(w))
        rays = list(dict.fromkeys(newrays))
        processed = ci + 1
    return rays


def cone_integrals(rays, ell, d):
    """(Z, I): exact integrals of e^-<1,x> and ell(x) e^-<1,x> over the cone
    spanned by `rays` (assumed full-dim, subset of orthant)."""
    if len(rays) < d:
        return Fraction(0), Fraction(0)
    s = [sum(r) for r in rays]
    lv = [sum(a * b for a, b in zip(ell, r)) for r in rays]
    if len(rays) == d:
        simplices = [list(range(d))]
    else:
        # cross-section points projected to first d-1 coords, Delaunay for
        # combinatorics only
        pts = np.array([[ri / si for ri in r[: d - 1]] for r, si in
                        zip(rays, s)])
        try:
            tri = Delaunay(pts)
        except Exception:
            tri = Delaunay(pts, qhull_options="QJ")
        simplices = tri.simplices.tolist()
    Z = Fraction(0)
    I = Fraction(0)
    for simp in simplices:
        W = [rays[k] for k in simp]
        dt = abs(det_bareiss(W))
        if dt == 0:
            continue
        prod = Fraction(dt)
        for k in simp:
            prod /= s[k]
        Z += prod
        I += prod * sum(Fraction(lv[k], s[k]) for k in simp)
    return Z, I


# ------------------------------------------------------------- sign pattern DFS

def compute_ci(i, verbose=True, prefix=()):
    """prefix: forced signs (+1/-1) for the first len(prefix) sign slots in
    DFS order (level 1 slots j=1..i first, then level 2, ...).  Used to
    split the chamber enumeration across processes."""
    d = i + 1
    t0 = time.time()
    leaves = [0]
    Ztot = Fraction(0)
    Itot = Fraction(0)
    bases = [0] * (i + 2)
    for t in range(1, i + 1):
        bases[t + 1] = bases[t] + (i + 1 - t)

    def feasible(cons):
        """LP: does {x>=0, cons x >= 0} have full-dim interior?
        max t s.t. cons x >= t, x >= t, sum x = d. Full-dim iff t* > 0."""
        A_ub = []
        for c in cons:
            A_ub.append([-v for v in c] + [1.0])
        for j in range(d):
            row = [0.0] * d
            row[j] = -1.0
            A_ub.append(row + [1.0])
        res = linprog(c=[0.0] * d + [-1.0], A_ub=A_ub, b_ub=[0.0] * len(A_ub),
                      A_eq=[[1.0] * d + [0.0]], b_eq=[float(d)],
                      bounds=[(None, None)] * d + [(None, None)],
                      method="highs")
        return res.status == 0 and -res.fun > 1e-9

    def dfs(level, funcs, cons):
        nonlocal Ztot, Itot
        if level > i:
            leaves[0] += 1
            rays = dd_rays(cons, d)
            ell = funcs[0]  # bottom entry functional (already sign-fixed)
            Z, I = cone_integrals(rays, ell, d)
            Ztot += Z
            Itot += I
            return
        # differences at this level
        diffs = [tuple(funcs[j][k] - funcs[j + 1][k] for k in range(d))
                 for j in range(len(funcs) - 1)]

        def choose(j, chosen_funcs, chosen_cons):
            if j == len(diffs):
                dfs(level + 1, chosen_funcs, chosen_cons)
                return
            slot = bases[level] + j
            signs = (prefix[slot],) if slot < len(prefix) else (1, -1)
            for sgn in signs:
                f = tuple(sgn * v for v in diffs[j])
                nc = chosen_cons + [f]
                # Every sign pattern is feasible (provable by bottom-up
                # reconstruction), so the LP prune is optional; infeasible
                # or lower-dim patterns would contribute 0 anyway and the
                # exact partition check certifies the total.
                if SKIP_LP or feasible(nc):
                    choose(j + 1, chosen_funcs + [f], nc)

        choose(0, [], cons)

    base = [tuple(1 if k == j else 0 for k in range(d)) for j in range(d)]
    dfs(1, base, [])
    if verbose:
        print(f"i={i}: {leaves[0]} full-dimensional sign chambers, "
              f"{time.time()-t0:.1f}s")
        print(f"  partition check: sum Z = {Ztot}  "
              f"({'PASS' if Ztot == 1 else '*** FAIL ***'})")
        print(f"  c_{i} = {Itot} = {float(Itot):.6f}")
    return Itot, leaves[0], Ztot


SKIP_LP = "--nolp" in sys.argv

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    imax = int(args[0]) if args else 4
    known = {1: Fraction(1), 2: Fraction(7, 9), 3: Fraction(227, 288)}
    for i in range(1, imax + 1):
        ci, chambers, Z = compute_ci(i)
        if Z != 1:
            print("  PARTITION FAILURE - result not certified")
        if i in known:
            ok = ci == known[i]
            print(f"  vs known {known[i]}: {'MATCH' if ok else '*** MISMATCH ***'}")
        print()
