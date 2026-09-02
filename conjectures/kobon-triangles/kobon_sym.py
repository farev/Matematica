#!/usr/bin/env python3
"""
Symmetries of the signotope model of Euclidean pseudoline arrangements.

A Euclidean (affine) simple pseudoline arrangement is a projective arrangement with a
marked line at infinity; a signotope additionally fixes a sweep direction, i.e. a cut of
the cyclic sequence of the 2n unbounded rays.  Moving the cut by one ray gives the
"shift": line n becomes line 1 with reversed direction, line i becomes line i+1.
On local sequences: s'_{1} = reverse(s_n), s'_{i+1} = s_i (labels renamed).  On signs:
    shift:  sigma'(i+1, j+1, k+1) =  sigma(i, j, k)      (k < n)
            sigma'(1,   i+1, j+1) = -sigma(i, j, n)      (i < j < n)
Reflection in a horizontal axis ("mirror") reverses the labels and flips every sign:
    mirror: sigma'(n+1-k, n+1-j, n+1-i) = -sigma(i, j, k).
shift^n is the global flip (rotation by 180 degrees), shift^(2n) = id; together with the
mirror they generate a dihedral group of order 4n acting on signotopes and preserving the
number of triangular faces.  validate() checks all of this exhaustively for small n.
"""
import itertools
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def shift_map(n):
    """dict: new triple -> (old triple, sign) for one shift."""
    m = {}
    for i, j, k in itertools.combinations(range(1, n + 1), 3):
        if k < n:
            m[(i + 1, j + 1, k + 1)] = ((i, j, k), +1)
        else:
            m[(1, i + 1, j + 1)] = ((i, j, n), -1)
    return m


def mirror_map(n):
    m = {}
    for t in itertools.combinations(range(1, n + 1), 3):
        m[tuple(sorted(n + 1 - x for x in t))] = (t, -1)
    return m


def compose(m1, m2):
    """apply m2 after m1:  new[t] = s2 * mid[t2],  mid[t2] = s1 * old[t1]  ->  new[t] = s1*s2*old[t1]."""
    out = {}
    for t, (t2, s2) in m2.items():
        t1, s1 = m1[t2]
        out[t] = (t1, s1 * s2)
    return out


def identity_map(n):
    return {t: (t, +1) for t in itertools.combinations(range(1, n + 1), 3)}


def group(n):
    """All 4n signed-permutation maps (as dicts new->(old,sign)), keyed by (a,b) = shift^a mirror^b."""
    S, M = shift_map(n), mirror_map(n)
    els = {}
    cur = identity_map(n)
    for a in range(2 * n):
        els[(a, 0)] = cur
        els[(a, 1)] = compose(cur, M)
        cur = compose(cur, S)
    return els


def apply(m, sigma):
    return {t: s * sigma[t1] for t, (t1, s) in m.items()}


def validate(n):
    from kobon_sat import Encoder, check_signotope, local_sequences, triangles, wiring_sweep
    from pysat.solvers import Cadical195
    E = Encoder(n, None, symbreak=False)
    sigs = []
    with Cadical195(bootstrap_with=E.clauses) as s:
        sv = set(E.sig.values())
        while s.solve():
            m = s.get_model()
            sigs.append(E.decode(m))
            s.add_clause([-l for l in m if abs(l) in sv])
    G = group(n)
    # distinctness of group elements
    keys = set()
    for g, m in G.items():
        keys.add(tuple(sorted((t, v) for t, v in m.items())))
    assert len(keys) == 4 * n, f'group has {len(keys)} distinct elements, expected {4*n}'
    # shift^n == flip
    flip = {t: (t, -1) for t in identity_map(n)}
    assert G[(n, 0)] == flip
    index = {tuple(sorted(s.items())): i for i, s in enumerate(sigs)}
    orbit_sizes = {}
    for s in sigs:
        seqs = local_sequences(n, s)
        wiring_sweep(n, seqs)
        nt = len(triangles(n, seqs))
        orb = set()
        for g, m in G.items():
            s2 = apply(m, s)
            assert check_signotope(n, s2), f'image under {g} is not a signotope'
            key = tuple(sorted(s2.items()))
            assert key in index, 'image not in the enumerated set'
            seqs2 = local_sequences(n, s2)
            wiring_sweep(n, seqs2)
            assert len(triangles(n, seqs2)) == nt, f'triangle count changed under {g}'
            orb.add(key)
        orbit_sizes[len(orb)] = orbit_sizes.get(len(orb), 0) + 1
    return len(sigs), orbit_sizes


if __name__ == '__main__':
    for n in (4, 5, 6, 7):
        cnt, orbs = validate(n)
        print(f'n={n}: {cnt} signotopes, all 4n={4*n} symmetries valid; orbit-size histogram {orbs}', flush=True)
