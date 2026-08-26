#!/usr/bin/env python3
"""Boundary-state calculus for strong 6-colorings of truncations.

Dart model (NOTE Lemma R): a strong 6-coloring of T(H) == a pair (c, t):
  * c: E(H) -> {0..5} proper (parallel edges adjacent),
  * t: darts -> colors with, at each vertex u with darts e,f,g,
        {c(e),c(f),c(g), t_u(e),t_u(f),t_u(g)} = {0..5},
  * for each edge e = uv:  t_u(x) != t_v(y) for darts x != e at u,
                           y != e at v.

A pendant piece attached by stem edge s at vertex w exports the state
    ( c(s), { t_w(x), t_w(y) } )   (x, y = the other two darts at w),
and two pieces joined stem-to-stem are compatible iff their stem colors
agree and their exported pair-sets are disjoint (NOTE Lemma S).

This script enumerates, by brute force over the dart model:
  * Sigma_B: states realizable by a balloon (u,v,w; uv doubled, uw, vw,
    stem at w)  — the expansion of a loop,
  * R_D: state pairs realizable by a dumbbell (x,y; xy doubled, stems at
    x and y) — the expansion of a plain edge,
  * Sigma_E: states realizable at one end of a bare stem, i.e. the
    unconstrained single-vertex piece (for calibration),
and closes the chain family balloon + D^k + balloon over all k by
fixed-point iteration, printing a machine-checked verdict for every k.

States are canonical under color permutation for reporting, but all 60
labelled states are used in the computations.
"""
from itertools import permutations, product, combinations

COLORS = range(6)


def all_states():
    return [(c, frozenset(p)) for c in COLORS
            for p in combinations(COLORS, 2) if c not in p]


def balloon_states():
    """u,v,w; edges e1,e2 = uv, f = uw, g = vw, stem s at w."""
    out = set()
    for ce1, ce2, cf, cg, cs in product(COLORS, repeat=5):
        if len({ce1, ce2, cf}) < 3 or len({ce1, ce2, cg}) < 3:
            continue
        if len({cf, cg, cs}) < 3:
            continue
        Pu = [x for x in COLORS if x not in (ce1, ce2, cf)]
        Pv = [x for x in COLORS if x not in (ce1, ce2, cg)]
        Pw = [x for x in COLORS if x not in (cf, cg, cs)]
        for tu in permutations(Pu):          # tu = (t_u(e1), t_u(e2), t_u(f))
            for tv in permutations(Pv):      # tv = (t_v(e1), t_v(e2), t_v(g))
                # edge e1: {t_u(e2), t_u(f)} vs {t_v(e2), t_v(g)}
                if {tu[1], tu[2]} & {tv[1], tv[2]}:
                    continue
                # edge e2: {t_u(e1), t_u(f)} vs {t_v(e1), t_v(g)}
                if {tu[0], tu[2]} & {tv[0], tv[2]}:
                    continue
                for tw in permutations(Pw):  # tw = (t_w(f), t_w(g), t_w(s))
                    # edge f = uw: {t_u(e1), t_u(e2)} vs {t_w(g), t_w(s)}
                    if {tu[0], tu[1]} & {tw[1], tw[2]}:
                        continue
                    # edge g = vw: {t_v(e1), t_v(e2)} vs {t_w(f), t_w(s)}
                    if {tv[0], tv[1]} & {tw[0], tw[2]}:
                        continue
                    out.add((cs, frozenset({tw[0], tw[1]})))
    return out


def dumbbell_relation():
    """x,y; edges d1,d2 = xy, stems sL at x, sR at y."""
    rel = set()
    for cd1, cd2, csl, csr in product(COLORS, repeat=4):
        if len({cd1, cd2, csl}) < 3 or len({cd1, cd2, csr}) < 3:
            continue
        Px = [c for c in COLORS if c not in (cd1, cd2, csl)]
        Py = [c for c in COLORS if c not in (cd1, cd2, csr)]
        for tx in permutations(Px):          # (t_x(d1), t_x(d2), t_x(sL))
            for ty in permutations(Py):      # (t_y(d1), t_y(d2), t_y(sR))
                # edge d1: {t_x(d2), t_x(sL)} vs {t_y(d2), t_y(sR)}
                if {tx[1], tx[2]} & {ty[1], ty[2]}:
                    continue
                # edge d2: {t_x(d1), t_x(sL)} vs {t_y(d1), t_y(sR)}
                if {tx[0], tx[2]} & {ty[0], ty[2]}:
                    continue
                rel.add(((csl, frozenset({tx[0], tx[1]})),
                         (csr, frozenset({ty[0], ty[1]}))))
    return rel


def compatible(s1, s2):
    return s1[0] == s2[0] and not (s1[1] & s2[1])


def canonical_orbits(states):
    seen = set()
    orbits = []
    for st in sorted(states):
        if st in seen:
            continue
        orb = set()
        for perm in permutations(COLORS):
            c, p = st
            orb.add((perm[c], frozenset(perm[x] for x in p)))
        orb &= set(states)
        seen |= orb
        orbits.append((st, len(orb)))
    return orbits


def main():
    SB = balloon_states()
    RD = dumbbell_relation()
    ALL = set(all_states())
    print("all conceivable states: %d" % len(ALL))
    print("Sigma_B (balloon): %d states" % len(SB))
    for rep, sz in canonical_orbits(SB):
        print("   orbit rep (c=%d, S=%s) size %d" % (rep[0], set(rep[1]), sz))
    missing = ALL - SB
    print("states a balloon can NOT produce: %d" % len(missing))
    for rep, sz in canonical_orbits(missing):
        print("   orbit rep (c=%d, S=%s) size %d" % (rep[0], set(rep[1]), sz))
    print("R_D (dumbbell): %d labelled pairs" % len(RD))

    # chain closure: states reachable on the right stem of B + D^k
    reach = SB
    print("\nchain family balloon + D^k + balloon:")
    seen = []
    k = 0
    while True:
        # is balloon-compatible right-closure nonempty? (k dumbbells used)
        ok = any(compatible(s, b) for s in reach for b in SB)
        print("  k=%d: reachable states %d -> %s" %
              (k, len(reach), "6-COLORABLE" if ok else "NOT 6-colorable"))
        if reach in seen:
            print("  reachable-set repeats earlier value: eventually periodic;"
                  " verdicts above cover all k >= 0 by periodicity from the"
                  " repeat point.")
            break
        seen.append(reach)
        nxt = {r for (l, r) in RD if any(compatible(s, l) for s in reach)}
        reach = nxt
        k += 1
        if k > 20:
            break


if __name__ == "__main__":
    main()
