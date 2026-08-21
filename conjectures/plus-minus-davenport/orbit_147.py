#!/usr/bin/env python3
"""Rigidity of the dissociated 7-set in C7+C21.

The exhaustive count (verify_147) found exactly 2016 dissociated 7-sets
of plus-minus class representatives.  |Aut(C7+C21)| = |GL(2,7)| * |Aut(C3)|
= 2016 * 2 = 4032, and -id acts trivially on plus-minus classes, so IF the
action on witness sets is transitive, the orbit size is 4032/2 = 2016.

This script computes the Aut-orbit of one witness on the level of
plus-minus-class SETS and checks (a) orbit size, (b) that every element of
the orbit is dissociated, (c) whether orbit size == 2016 (=> uniqueness up
to Aut).

G = C7 + C21 written as C7 + C7 + C3 with coords (a, b; c),
Aut = GL(2,7) on (a,b)  x  {1,-1} on c.
"""

from itertools import product
from dissoc import Group, is_dissociated

G3 = Group([7, 7, 3])


def to3(g21):  # (x, y) in C7 x C21  ->  (x, y mod 7, y mod 3) via CRT
    x, y = g21
    return G3.index((x, y % 7, y % 3))


def norm_class(g):
    return min(g, G3.neg(g))


def orbit_of(witness_classes):
    """witness_classes: frozenset of class-rep indices in G3."""
    mats = []
    for a, b, c, d in product(range(7), repeat=4):
        if (a * d - b * c) % 7 != 0:
            mats.append((a, b, c, d))
    assert len(mats) == 2016, len(mats)

    seen = set()
    for (a, b, c, d) in mats:
        for e in (1, 2):  # Aut(C3) = {1, -1 = 2}
            img = []
            for g in witness_classes:
                x, y, z = G3.coords(g)
                nx = (a * x + b * y) % 7
                ny = (c * x + d * y) % 7
                nz = (e * z) % 3
                img.append(norm_class(G3.index((nx, ny, nz))))
            seen.add(frozenset(img))
    return seen


def main():
    # witness from dissoc (C7+C21 coords): map to C7+C7+C3
    wit21 = [(0, 1), (0, 2), (1, 1), (1, 5), (2, 1), (2, 10), (3, 19)]
    wit = frozenset(norm_class(to3(g)) for g in wit21)
    assert len(wit) == 7
    assert is_dissociated(G3, sorted(wit)), "witness not dissociated?!"

    orb = orbit_of(wit)
    print(f"Aut-orbit size of the witness (as class sets): {len(orb)}")
    ok = all(is_dissociated(G3, sorted(s)) for s in orb)
    print(f"all orbit members dissociated: {ok}")
    # independent witness from the desc run
    wit21b = [(3, 20), (3, 19), (3, 17), (3, 8), (2, 17), (2, 11), (1, 4)]
    witb = frozenset(norm_class(to3(g)) for g in wit21b)
    print(f"desc-run witness lies in the same orbit: {witb in orb}")
    print("=> " + ("UNIQUE up to Aut (orbit size == exhaustive count 2016)"
                   if len(orb) == 2016 else
                   f"NOT transitive: orbit {len(orb)} != 2016"))


if __name__ == "__main__":
    main()
