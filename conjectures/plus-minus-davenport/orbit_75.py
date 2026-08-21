#!/usr/bin/env python3
"""Structure of maximum dissociated sets (5-sets) in C5+C15.

Enumerates ALL dissociated 5-sets over plus-minus class reps (C(37,5)
subsets, brute force), then decomposes them into orbits of
Aut(C5+C15) = GL(2,5) x Aut(C3), acting on class sets.
Also records, per orbit, the invariant k = number of elements with
nonzero C3-component, and whether the 5-set extends (it never does --
that is the deficiency theorem -- but recompute the extension count as a
cross-check: total extensions tried must be 0 successes).
"""

from itertools import combinations, product
from dissoc import Group, is_dissociated

G = Group([5, 5, 3])


def to553(g15):
    x, y = g15
    return G.index((x, y % 5, y % 3))


def norm_class(g):
    return min(g, G.neg(g))


def all_dissociated_5sets():
    reps = G.class_reps()
    out = []
    for c in combinations(reps, 5):
        if is_dissociated(G, c):
            out.append(frozenset(c))
    return out


def aut_images(s):
    mats = []
    for a, b, c, d in product(range(5), repeat=4):
        if (a * d - b * c) % 5 != 0:
            mats.append((a, b, c, d))
    assert len(mats) == 480
    for m in mats:
        a, b, c, d = m
        for e in (1, 2):
            img = []
            for g in s:
                x, y, z = G.coords(g)
                img.append(norm_class(G.index(
                    ((a * x + b * y) % 5, (c * x + d * y) % 5, (e * z) % 3))))
            yield frozenset(img)


def main():
    sets5 = all_dissociated_5sets()
    print(f"dissociated 5-sets in C5+C15: {len(sets5)}")

    # extension cross-check: none extends to 6 (deficiency)
    reps = G.class_reps()
    ext = 0
    for s in sets5:
        for r in reps:
            if r not in s and is_dissociated(G, sorted(s) + [r]):
                ext += 1
    print(f"extensions to dissociated 6-sets: {ext} (must be 0)")

    # orbit decomposition
    pool = set(sets5)
    orbits = []
    while pool:
        s = next(iter(pool))
        orb = set(aut_images(s))
        orbits.append(orb)
        pool -= orb
    print(f"Aut-orbits of maximum dissociated sets: {len(orbits)}")
    for i, orb in enumerate(sorted(orbits, key=len)):
        rep = sorted(next(iter(orb)))
        k = sum(1 for g in rep if G.coords(g)[2] != 0)
        # order profile of elements
        prof = sorted(order_of(g) for g in rep)
        print(f"  orbit {i}: size {len(orb)}, k(C3-support)={k}, "
              f"element orders {prof}, rep {[G.coords(g) for g in rep]}")


def order_of(g):
    o = 1
    x = g
    while x != 0:
        x = G.add(x, g)
        o += 1
    return o


if __name__ == "__main__":
    main()
