#!/usr/bin/env python3
"""Structure analysis of the extremal dissociated sets of the two headline
groups, C_5+C_15 (= C_3+C_5^2) and C_7+C_21 (= C_3+C_7^2).

Computes, for G = C_3 + C_p^2 (p in {5,7}):
  * the full census of extremal dissociated class-rep sets (recomputed
    here, independently, by simple DFS over class reps — third/fourth
    computation of the census numbers),
  * the CRT profile (k0, k1) of each extremal set: k1 = number of elements
    with nonzero C_3-coordinate after sign-normalizing that coordinate
    to {0, 1},
  * the orbit census under Aut(G) = Aut(C_3) x Aut(C_p^2)
    = {+-1} x GL(2, p), acting on class-rep sets (global -1 acts
    trivially on classes, so the effective group is {+-1} x GL(2,p) / <-id>
    with the two -1's identified; we act by the full group and dedupe).

Exact integer arithmetic only.

Usage: python3 orbit_analysis.py p target_size   (e.g. 5 5, or 7 7)
"""

import sys
from itertools import product


def build(p):
    """G = Z_3 x Z_p x Z_p, elements as tuples (a, x, y)."""
    elems = [(a, x, y) for a in range(3) for x in range(p) for y in range(p)]
    return elems


def neg(g, p):
    return ((-g[0]) % 3, (-g[1]) % p, (-g[2]) % p)


def add(g, h, p):
    return ((g[0] + h[0]) % 3, (g[1] + h[1]) % p, (g[2] + h[2]) % p)


def classes(p):
    reps = []
    seen = set()
    for g in build(p):
        if g == (0, 0, 0) or g in seen:
            continue
        h = neg(g, p)
        seen.add(g)
        seen.add(h)
        reps.append(min(g, h))
    return sorted(reps)


def census(p, target):
    """All dissociated class-rep sets of size target, by DFS."""
    reps = classes(p)
    M = len(reps)
    out = []

    def dfs(start, chosen, A):
        if len(chosen) == target:
            out.append(tuple(chosen))
            return
        for j in range(start, M):
            g = reps[j]
            ng = neg(g, p)
            if g in A or ng in A:
                continue
            A2 = set(A)
            for s in A:
                A2.add(add(s, g, p))
                A2.add(add(s, ng, p))
            chosen.append(g)
            dfs(j + 1, chosen, A2)
            chosen.pop()

    dfs(0, [], {(0, 0, 0)})
    return reps, out


def gl2(p):
    mats = []
    for a, b, c, d in product(range(p), repeat=4):
        if (a * d - b * c) % p != 0:
            mats.append((a, b, c, d))
    return mats


def canonical(S, p, mats):
    """Canonical form of a class-rep set under {+-1} x GL(2,p)."""
    best = None
    for e in (1, 2):            # automorphism of Z_3: identity, inversion
        for (a, b, c, d) in mats:
            img = []
            for (t, x, y) in S:
                t2 = (e * t) % 3
                x2 = (a * x + b * y) % p
                y2 = (c * x + d * y) % p
                g = (t2, x2, y2)
                h = ((-t2) % 3, (-x2) % p, (-y2) % p)
                img.append(min(g, h))
            img = tuple(sorted(img))
            if best is None or img < best:
                best = img
    return best


def profile(S):
    """k1 = number of elements with nonzero Z_3 coordinate."""
    return sum(1 for (t, x, y) in S if t != 0)


def main():
    p = int(sys.argv[1])
    target = int(sys.argv[2])
    reps, ext = census(p, target)
    print(f"G = Z_3 + Z_{p}^2, |G| = {3*p*p}, classes = {len(reps)}")
    print(f"extremal dissociated {target}-sets: {len(ext)}")
    with open(f"certs/c3p{p}p{p}_extremal_{target}sets.txt", "w") as f:
        f.write(f"# all extremal dissociated {target}-sets of Z_3+Z_{p}+Z_{p}"
                f" as class-rep sets (a; x, y)\n")
        for S in ext:
            f.write(" ".join(f"({a},{x},{y})" for (a, x, y) in S) + "\n")

    profs = {}
    for S in ext:
        k1 = profile(S)
        profs[k1] = profs.get(k1, 0) + 1
    print("profile census (k1 = #elements with nonzero Z_3 part):")
    for k1 in sorted(profs):
        print(f"  k1 = {k1}: {profs[k1]} sets")

    mats = gl2(p)
    print(f"|GL(2,{p})| = {len(mats)}; acting with {{+-1}} x GL(2,{p}) "
          f"(order {2*len(mats)})")
    orbits = {}
    for S in ext:
        c = canonical(S, p, mats)
        orbits.setdefault(c, 0)
        orbits[c] += 1
    print(f"orbits: {len(orbits)}")
    for c, sz in sorted(orbits.items(), key=lambda kv: -kv[1]):
        print(f"  orbit size {sz}, representative {list(c)}")


if __name__ == "__main__":
    main()
