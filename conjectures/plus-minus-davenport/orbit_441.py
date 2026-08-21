#!/usr/bin/env python3
"""Aut-orbit of the found maximum dissociated 8-set in C9+C7+C7 (order 441).

Aut(C9 + C7^2) = Aut(C9) x GL(2,7), order 6 * 2016 = 12096; -id acts
trivially on plus-minus classes.  This gives the orbit size (a lower
bound on the number of maximum sets) and verifies every orbit member is
dissociated.  Full enumeration of all maximum sets (for a rigidity claim
like the one at order 147) is not run here — the complete depth-8 tree
walk is priced beyond this session; recorded as open in NOTE Q3.
"""

from itertools import product
from dissoc import Group, is_dissociated

G = Group([9, 7, 7])


def norm_class(g):
    return min(g, G.neg(g))


wit = [G.index(c) for c in
       [(0, 0, 1), (0, 1, 0), (0, 1, 2), (0, 1, 4), (0, 3, 1),
        (1, 0, 0), (2, 0, 0), (4, 0, 0)]]
assert is_dissociated(G, wit)
W = frozenset(norm_class(g) for g in wit)
assert len(W) == 8

mats = [(a, b, c, d) for a, b, c, d in product(range(7), repeat=4)
        if (a * d - b * c) % 7]
assert len(mats) == 2016
units9 = [1, 2, 4, 5, 7, 8]

orbit = set()
for (a, b, c, d) in mats:
    for u in units9:
        img = []
        for g in W:
            x, y, z = G.coords(g)
            img.append(norm_class(G.index(
                ((u * x) % 9, (a * y + b * z) % 7, (c * y + d * z) % 7))))
        orbit.add(frozenset(img))

ok = all(is_dissociated(G, sorted(s)) for s in orbit)
print(f"|Aut| = 12096 (effective 6048 on classes); orbit size = "
      f"{len(orbit)}; all dissociated: {ok}")
print("=> at least", len(orbit), "maximum dissociated 8-sets in C9+C7+C7")
