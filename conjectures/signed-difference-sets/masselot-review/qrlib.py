"""Quotient-system machinery for the independent re-verification of
Masselot's order-32/36 signed-difference-set decisions (v1.0 census).

Everything here is exact integer arithmetic (Python ints); no floats
anywhere. No code is shared with Masselot's repository, with Gordon's
sds_code.py, or with this repository's sds_search.c engine; the only
shared local code is sdslib.check_sds, used as the final referee on any
full-group vector this suite produces or consumes.

Background. Let A be an SDS(v,k,lam) in an abelian group H, so
A*A^(-1) = (k-lam) e + lam H in Z[H], and after a global sign flip
sum(A) = s with s^2 = k + lam(v-1). For K <= H with |K| = m and
Q = H/K, the projection B (cell sums over fibers) satisfies

    B*B^(-1) = (k-lam) e + lam*m * Q      in Z[Q],            (Q-system)

i.e. peak (shift-0) value  k + (m-1) lam  and value  m*lam  at every
nonzero shift, with every cell in [-m, m] and sum(B) = s.  We call the
set of ALL such B (no symmetry reduction of any kind) the complete
(Q, m) system for (v,k,lam).  Emptiness of any one system for a group H
possessing that quotient proves nonexistence of the SDS in H.
"""

from itertools import product


# ---------------------------------------------------------------- groups

def order(G):
    v = 1
    for n in G:
        v *= n
    return v


def elements(G):
    """All elements as tuples, lexicographic, last coordinate fastest --
    index i <-> mixed-radix digits of i (same convention as sdslib)."""
    return [tuple(e) for e in product(*[range(n) for n in G])]


def add_table(G):
    els = elements(G)
    v = len(els)
    idx = {e: i for i, e in enumerate(els)}
    return [
        [idx[tuple((a + b) % n for a, b, n in zip(x, y, G))] for y in els]
        for x in els
    ], els, idx


def neg_table(G):
    els = elements(G)
    idx = {e: i for i, e in enumerate(els)}
    return [idx[tuple((-a) % n for a, n in zip(x, G))] for x in els]


def full_correlation(vec, add, neg):
    """C(d) = sum_g vec[g] * vec[g - d] for every d (exact ints)."""
    v = len(vec)
    out = [0] * v
    support = [g for g in range(v) if vec[g]]
    for d in range(v):
        nd = neg[d]
        c = 0
        for g in support:
            c += vec[g] * vec[add[g][nd]]
        out[d] = c
    return out


def is_system_solution(vec, add, neg, peak, off):
    corr = full_correlation(vec, add, neg)
    if corr[0] != peak:
        return False
    return all(c == off for c in corr[1:])


# ------------------------------------------------- direct enumeration

def enum_system(G, m, k, lam, s):
    """Complete list of the (G, m) system for (v,k,lam): every vector
    over G with cells in [-m,m], sum s, and exact correlation profile
    (peak k+(m-1)lam, off-peak m*lam). DFS with sum/norm pruning, then
    exact full-correlation filter. Returns (n_sum_norm, solutions)."""
    v = order(G)
    peak = k + (m - 1) * lam
    off = m * lam
    add, _, _ = add_table(G)
    neg = neg_table(G)
    sols = []
    n_sum_norm = 0
    vec = [0] * v

    def rec(i, rsum, rnorm):
        nonlocal n_sum_norm
        if i == v:
            if rsum == 0 and rnorm == 0:
                n_sum_norm += 1
                if is_system_solution(vec, add, neg, peak, off):
                    sols.append(tuple(vec))
            return
        rem = v - i - 1
        for b in range(-m, m + 1):
            b2 = b * b
            if b2 > rnorm:
                continue
            nrs, nrn = rsum - b, rnorm - b2
            # remaining cells must be able to reach sum nrs and norm nrn
            if abs(nrs) > rem * m:
                continue
            if nrn > rem * m * m:
                continue
            # each remaining cell contributes >= (|cell|)^2 with
            # |cell| >= ceil(|nrs|/rem) on average -- cheap bound:
            # need nrn >= nrs^2/rem (Cauchy-Schwarz), integer-safe:
            if rem == 0:
                if nrs != 0 or nrn != 0:
                    continue
            elif nrs * nrs > nrn * rem:
                continue
            vec[i] = b
            rec(i + 1, nrs, nrn)
        vec[i] = 0

    peaknorm = peak  # sum of squares of cells equals the peak value
    rec(0, s, peaknorm)
    return n_sum_norm, sols


# ------------------------------------------------------------- orbits

def translation_orbits(sols, G):
    add, _, _ = add_table(G)
    v = order(G)
    solset = set(sols)
    seen, orbits = set(), []
    for x in sols:
        if x in seen:
            continue
        orb = set()
        for t in range(v):
            y = tuple(x[add[g][t]] for g in range(v))
            assert y in solset, "translation image escapes solution set"
            orb.add(y)
        seen |= orb
        orbits.append(sorted(orb))
    return orbits


def affine_orbits_cyclic(sols, n):
    """Orbits under x -> u*x + t on Z_n (u a unit)."""
    units = [u for u in range(1, n) if _gcd(u, n) == 1]
    solset = set(sols)
    seen, orbits = set(), []
    for x in sols:
        if x in seen:
            continue
        orb = set()
        for u in units:
            for t in range(n):
                y = tuple(x[(u * g + t) % n] for g in range(n))
                assert y in solset, "affine image escapes solution set"
                orb.add(y)
        seen |= orb
        orbits.append(sorted(orb))
    return orbits


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


# ----------------------------------------------- pair splittings cache

def splittings(total, bound, parts):
    """All tuples of `parts` integers in [-bound, bound] with the given
    sum (small cases only; memoised by caller if needed)."""
    if parts == 1:
        return [(total,)] if -bound <= total <= bound else []
    out = []
    for first in range(-bound, bound + 1):
        for rest in splittings(total - first, bound, parts - 1):
            out.append((first,) + rest)
    return out
