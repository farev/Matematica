#!/usr/bin/env python3
"""Diamond piece transfer relation (graph side).

Piece: diamond a,b,c,d (edges ac, ad, bc, bd, cd; ab missing), stems
s1 = a-out1, s2 = b-out2.  Enumerates all colorings of the 7 piece
edges satisfying the internal strong-coloring conflicts and exports the
labelled boundary-state pairs ((c(s1), {c(ac), c(ad)}),
(c(s2), {c(bc), c(bd)})).

Also verifies the closed form: the relation is exactly
    { ((c, S1), (c, S2)) : |S1| = |S2| = 2, S1 cap S2 = empty,
                            c not in S1 cup S2 }
(color passes through unchanged, pairs disjoint) — 180 labelled pairs —
and that the *composition* of the relation with junction compatibility
on both sides is exactly { (c,Sx) ~ (c,Sy) : Sx != Sy }: strictly weaker
than the bare-edge junction rule Sx cap Sy = empty (disjoint 2-sets are
in particular distinct), so inserting a diamond into a bridge relaxes
the constraint — it can never destroy strong 6-colorability — but it is
not a universal joint: equal pairs on both sides remain forbidden.
(A first hand-derivation claimed the full relation; this check refuted
it — the case Sx = Sy leaves only one color for S2.)
"""
from itertools import combinations, product

a, b, c, d, o1, o2 = range(6)
E = [(a, c), (a, d), (b, c), (b, d), (c, d), (a, o1), (b, o2)]
nb = {v: set() for v in range(6)}
for x, y in E:
    nb[x].add(y)
    nb[y].add(x)


def conflict(e, f):
    (p, q), (r, s) = e, f
    return bool({p, q} & {r, s}) or r in nb[p] or s in nb[p] \
        or r in nb[q] or s in nb[q]


m = len(E)
confl = [(i, j) for i in range(m) for j in range(i + 1, m)
         if conflict(E[i], E[j])]
rel = set()
for cols in product(range(6), repeat=m):
    if any(cols[i] == cols[j] for i, j in confl):
        continue
    rel.add(((cols[5], frozenset({cols[0], cols[1]})),
             (cols[6], frozenset({cols[2], cols[3]}))))

closed = set()
for cc in range(6):
    rest = [x for x in range(6) if x != cc]
    for S1 in combinations(rest, 2):
        for S2 in combinations([x for x in rest if x not in S1], 2):
            closed.add(((cc, frozenset(S1)), (cc, frozenset(S2))))
assert rel == closed, "closed form mismatch"
print("diamond relation = color-preserving disjoint pairs: %d labelled "
      "pairs (verified)" % len(rel))

# composition check: which (c, Sx) ~ (c, Sy) pass through a diamond
ok = True
for cc in range(6):
    rest = [x for x in range(6) if x != cc]
    for Sx in combinations(rest, 2):
        for Sy in combinations(rest, 2):
            found = any(
                not (set(S1) & set(Sx)) and not (set(S2) & set(Sy))
                for (c1, S1), (c2, S2) in rel if c1 == cc
            )
            ok &= (found == (set(Sx) != set(Sy)))
print("composition through a diamond == { Sx != Sy } exactly:", ok)
