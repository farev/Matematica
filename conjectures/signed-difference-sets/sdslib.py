"""Independent signed-difference-set library (pure integer arithmetic).

Definition (Gordon, arXiv:2212.10630; convention pinned against his
sds_code.py `is_sds` and every witness in his database): a signed
difference set SDS(v,k,lam) in a finite abelian group G of order v is an
element A of the group ring Z[G] with coefficients in {-1,0,+1}, exactly
k nonzero coefficients, such that

    A * A^(-1)  =  k*e  +  lam*(G - e)        in Z[G],

i.e. the signed autocorrelation sum_g A(g) A(g-d) equals lam for every
d != 0 (at d = 0 it is k automatically).  Writing P = {g : A(g)=+1},
M = {g : A(g)=-1} and sigma = |P|-|M|, summing the defining equation
over G gives sigma^2 = k + lam*(v-1), so s = sqrt(k + lam*(v-1)) must be
a nonnegative integer with |P| = (k+s)/2, |M| = (k-s)/2 (after a global
sign flip making sigma >= 0; the flip preserves the SDS property).

Groups are given by their invariant-factor list [n1,...,nr] (e.g. [3,6]
is Z3 x Z6); elements are integers for cyclic groups or lists/tuples of
coordinates otherwise, exactly as stored in Gordon's sds.json.

This implementation shares no code with Gordon's Sage-based is_sds.
"""

import json
import math
import re

NAME_RE = re.compile(r"SDS\((\d+),(\d+),(-?\d+),\[([0-9, ]+)\]\)")


def parse_name(name):
    m = NAME_RE.fullmatch(name.replace(" ", ""))
    if not m:
        raise ValueError(f"bad SDS name: {name}")
    v, k, lam = int(m.group(1)), int(m.group(2)), int(m.group(3))
    G = [int(x) for x in m.group(4).split(",")]
    return v, k, lam, G


def s_of(v, k, lam):
    """Integer s with s^2 = k + lam*(v-1), or None."""
    t = k + lam * (v - 1)
    if t < 0:
        return None
    s = math.isqrt(t)
    return s if s * s == t else None


def elt_to_index(g, G):
    """Mixed-radix index of a group element (int or coordinate list)."""
    if len(G) == 1:
        if isinstance(g, (list, tuple)):
            g = g[0]
        return g % G[0]
    if not isinstance(g, (list, tuple)) or len(g) != len(G):
        raise ValueError(f"element {g} does not match group {G}")
    idx = 0
    for gi, ni in zip(g, G):
        idx = idx * ni + (gi % ni)
    return idx


def index_add_table(G):
    """v x v table of index(g+h) under mixed radix; small v only."""
    v = 1
    for n in G:
        v *= n
    coords = []
    for i in range(v):
        x, c = i, []
        for n in reversed(G):
            c.append(x % n)
            x //= n
        coords.append(tuple(reversed(c)))
    tab = [[0] * v for _ in range(v)]
    for i in range(v):
        for j in range(v):
            summed = tuple((a + b) % n for a, b, n in zip(coords[i], coords[j], G))
            idx = 0
            for gi, ni in zip(summed, G):
                idx = idx * ni + gi
            tab[i][j] = idx
    return tab


def neg_index(G):
    """index -> index of the negated element."""
    v = 1
    for n in G:
        v *= n
    out = [0] * v
    for i in range(v):
        x, c = i, []
        for n in reversed(G):
            c.append(x % n)
            x //= n
        c = list(reversed(c))
        negc = [(-a) % n for a, n in zip(c, G)]
        idx = 0
        for gi, ni in zip(negc, G):
            idx = idx * ni + gi
        out[i] = idx
    return out


def check_sds(v, k, lam, G, P, M, verbose=False):
    """Full independent verification. Returns (ok, message)."""
    order = 1
    for n in G:
        order *= n
    if order != v:
        return False, f"group order {order} != v={v}"
    A = [0] * v
    try:
        for g in P:
            i = elt_to_index(g, G)
            if A[i] != 0:
                return False, f"duplicate support element index {i}"
            A[i] = 1
        for g in M:
            i = elt_to_index(g, G)
            if A[i] != 0:
                return False, f"duplicate support element index {i}"
            A[i] = -1
    except ValueError as e:
        return False, str(e)
    if sum(1 for a in A if a) != k:
        return False, f"support size {sum(1 for a in A if a)} != k={k}"
    add = index_add_table(G)
    neg = neg_index(G)
    # C(d) = sum_g A(g) * A(g + (-d)) ... compute sum_g A(g)*A(add[g][neg_d])
    for d in range(1, v):
        c = 0
        nd = neg[d]
        for g in range(v):
            if A[g]:
                c += A[g] * A[add[g][nd]]
        if c != lam:
            return False, f"autocorrelation at d={d} is {c} != lam={lam}"
    s = s_of(v, k, lam)
    npos = sum(1 for a in A if a == 1)
    nneg = sum(1 for a in A if a == -1)
    if s is None or abs(npos - nneg) != s:
        return False, f"|P|-|M| = {npos-nneg} inconsistent with s={s}"
    if verbose:
        print(f"ok: |P|={npos} |M|={nneg} s={s}")
    return True, "ok"


def load_db(path="data/sds.json"):
    with open(path) as f:
        return json.load(f)


def cell_group(entry, G):
    """Group to use for arithmetic: G_rep overrides invariant factors."""
    return entry.get("G_rep", G)


def refinements(G):
    """Isomorphic coordinate systems: orderings of the prime-power
    decomposition of the invariant factors (for resolving witnesses
    stored in undeclared coordinates)."""
    from itertools import permutations

    pps = []
    for n in G:
        m = n
        p = 2
        while m > 1:
            if m % p == 0:
                q = 1
                while m % p == 0:
                    q *= p
                    m //= p
                pps.append(q)
            p += 1
    return sorted(set(permutations(pps)))
