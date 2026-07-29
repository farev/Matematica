"""Certified exact c_i: repairs the degenerate-triangulation defect of
ck_exact.py (which lost 1.7e-7 of measure at i=6).

Strategy per chamber cone:
  1. Two independent Delaunay triangulations (different generic rational
     projections of the cross-section).  All integrals exact.
  2. If they agree exactly (Z and I) and neither had a degenerate simplex,
     accept.  (Heuristic flag only - the final certificate is global.)
  3. Otherwise: exact "pulling" triangulation using the cone's known
     H-representation, with exact integer rank tests - no floating point.

Global certificate as before: sum of exponential-measure integrals over
all chambers must equal exactly 1 in Q.
"""

import itertools
import sys
import time
from fractions import Fraction

import numpy as np
from scipy.spatial import Delaunay

from ck_exact import det_bareiss, primitive, dd_rays

# two fixed generic projection matrices (rows), built deterministically
_rng = np.random.default_rng(1958)
_PROJ = [_rng.integers(-9, 10, size=(8, 9)).astype(float) for _ in range(2)]


def int_rank(vectors):
    """Exact rank of a list of integer vectors (fraction-free elimination)."""
    m = [list(map(Fraction, v)) for v in vectors]
    if not m:
        return 0
    rows, cols = len(m), len(m[0])
    r = 0
    for c in range(cols):
        piv = next((i for i in range(r, rows) if m[i][c] != 0), None)
        if piv is None:
            continue
        m[r], m[piv] = m[piv], m[r]
        for i in range(r + 1, rows):
            if m[i][c] != 0:
                f = m[i][c] / m[r][c]
                for j in range(c, cols):
                    m[i][j] -= f * m[r][j]
        r += 1
        if r == rows:
            break
    return r


def _integrals_from_simplices(rays, ell, simplices):
    s = [sum(r) for r in rays]
    lv = [sum(a * b for a, b in zip(ell, r)) for r in rays]
    Z = Fraction(0)
    I = Fraction(0)
    degen = False
    for simp in simplices:
        W = [rays[k] for k in simp]
        dt = abs(det_bareiss(W))
        if dt == 0:
            degen = True
            continue
        prod = Fraction(dt)
        for k in simp:
            prod /= s[k]
        Z += prod
        I += prod * sum(Fraction(lv[k], s[k]) for k in simp)
    return Z, I, degen


def _delaunay_simplices(rays, d, which):
    s = [sum(r) for r in rays]
    v = np.array([[ri / si for ri in r] for r, si in zip(rays, s)])
    P = _PROJ[which][: d - 1, : d]
    pts = v @ P.T
    tri = Delaunay(pts)
    return tri.simplices.tolist()


def exact_pulling(rays, cons, d):
    """Exact triangulation of cone spanned by `rays` with H-rep `cons`
    (list of integer normal vectors, cone = {x: c.x >= 0 for all c};
    must include the orthant facets).  Returns list of index d-tuples."""
    ray_idx = list(range(len(rays)))

    def zero_set(h, idxs):
        return [k for k in idxs if sum(a * b for a, b in zip(h, rays[k])) == 0]

    def tri(idxs, active, dim):
        # idxs: ray indices of this face-cone; dim: its linear dimension
        if len(idxs) == dim:
            return [list(idxs)]
        # facets of this face: constraints whose zero set within idxs has
        # rank dim-1 (and which do not contain the whole face)
        out = []
        r0 = idxs[0]
        seen = set()
        for h in cons:
            z = zero_set(h, idxs)
            key = tuple(z)
            if key in seen or len(z) == len(idxs) or r0 in z:
                continue
            seen.add(key)
            if len(z) >= dim - 1 and int_rank([rays[k] for k in z]) == dim - 1:
                for sub in tri(z, None, dim - 1):
                    out.append(sub + [r0])
        return out

    return tri(ray_idx, None, d)


def cone_integrals_certified(rays, ell, cons, d, stats):
    if len(rays) < d:
        return Fraction(0), Fraction(0)
    if len(rays) == d:
        Z, I, degen = _integrals_from_simplices(rays, ell, [list(range(d))])
        return Z, I
    try:
        s1 = _delaunay_simplices(rays, d, 0)
        Z1, I1, dg1 = _integrals_from_simplices(rays, ell, s1)
        s2 = _delaunay_simplices(rays, d, 1)
        Z2, I2, dg2 = _integrals_from_simplices(rays, ell, s2)
        if not dg1 and not dg2 and Z1 == Z2 and I1 == I2:
            return Z1, I1
    except Exception:
        pass
    stats["fallback"] += 1
    simp = exact_pulling(rays, cons, d)
    Z, I, degen = _integrals_from_simplices(rays, ell, simp)
    return Z, I


def compute_ci_certified(i, prefix=(), verbose=True):
    d = i + 1
    t0 = time.time()
    leaves = [0]
    stats = {"fallback": 0}
    Ztot, Itot = Fraction(0), Fraction(0)
    bases = [0] * (i + 2)
    for t in range(1, i + 1):
        bases[t + 1] = bases[t] + (i + 1 - t)
    orthant = [tuple(1 if k == j else 0 for k in range(d)) for j in range(d)]

    def dfs(level, funcs, cons):
        nonlocal Ztot, Itot
        if level > i:
            leaves[0] += 1
            rays = dd_rays(cons, d)
            Z, I = cone_integrals_certified(rays, funcs[0],
                                            orthant + cons, d, stats)
            Ztot += Z
            Itot += I
            return
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
                choose(j + 1, chosen_funcs + [f], chosen_cons + [f])

        choose(0, [], cons)

    base = [tuple(1 if k == j else 0 for k in range(d)) for j in range(d)]
    dfs(1, base, [])
    if verbose:
        print(f"i={i}: {leaves[0]} chambers, {stats['fallback']} exact "
              f"fallbacks, {time.time()-t0:.1f}s")
        print(f"  partition: {'PASS' if Ztot == 1 else 'FAIL ' + str(Ztot)}")
        print(f"  c_{i} = {Itot} = {float(Itot):.6f}")
    return Itot, Ztot, leaves[0], stats["fallback"]


if __name__ == "__main__":
    # self-test: force the exact pulling path on every chamber of i=3 and
    # compare with the Delaunay path
    print("== self-test: exact pulling vs Delaunay on all i=3 chambers ==")
    import ck_exact
    d = 4
    ok = True
    n_nonsimplicial = 0
    for pat in itertools.product((1, -1), repeat=6):
        # rebuild chamber constraints for this sign pattern
        funcs = [tuple(1 if k == j else 0 for k in range(d)) for j in range(d)]
        cons = []
        idx = 0
        fs = funcs
        for level in (1, 2, 3):
            diffs = [tuple(fs[j][k] - fs[j + 1][k] for k in range(d))
                     for j in range(len(fs) - 1)]
            nfs = []
            for j, df in enumerate(diffs):
                f = tuple(pat[idx] * v for v in df)
                idx += 1
                nfs.append(f)
                cons.append(f)
            fs = nfs
        rays = dd_rays(cons, d)
        orthant = [tuple(1 if k == j else 0 for k in range(d))
                   for j in range(d)]
        if len(rays) > d:
            n_nonsimplicial += 1
            simp = exact_pulling(rays, orthant + cons, d)
            Ze, Ie, _ = _integrals_from_simplices(rays, fs[0], simp)
            s1 = _delaunay_simplices(rays, d, 0)
            Zd, Id, _ = _integrals_from_simplices(rays, fs[0], s1)
            if Ze != Zd or Ie != Id:
                ok = False
                print("  MISMATCH at", pat)
    print(f"  {n_nonsimplicial} non-simplicial chambers, all "
          f"{'match' if ok else 'MISMATCH'}")

    for i in (2, 3, 4):
        ci, Z, ch, fb = compute_ci_certified(i)
        known = {2: Fraction(7, 9), 3: Fraction(227, 288),
                 4: Fraction(778959731701, 1447295850000)}
        if i in known:
            print(f"  vs known: {'MATCH' if ci == known[i] else 'MISMATCH'}")
