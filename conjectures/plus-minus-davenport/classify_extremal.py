#!/usr/bin/env python3
"""classify_extremal.py — orbit classification of extremal ±free sets.

For G = Z_5 ⊕ Z_15 or Z_7 ⊕ Z_21 (generally Z_p ⊕ Z_{3p}, p ≠ 3 prime,
so G ≅ F_p² ⊕ Z_3 and Aut(G) = GL(2,p) × Aut(Z_3)), reads an --enum file of
extremal free sets and computes:

  - the number of Aut(G)-orbits on the sets (automorphisms act on sign
    classes; the global −1 acts trivially on classes, so the effective group
    is Aut(G)/{±1} of order |GL(2,p)|),
  - orbit sizes and representatives,
  - the distribution of the Aut-invariant t-profile: how many elements of
    the set have nonzero Z_3-component,
  - how many sets are "product type": every element in (C_p × {0}) ∪
    ({0} × C_{3p}) (subgroup-supported sets).

Usage: python3 classify_extremal.py --p 5 --file enum_5_15_size5.txt
"""
import sys
from itertools import product as iproduct


def main():
    a = sys.argv
    p = int(a[a.index("--p") + 1])
    path = a[a.index("--file") + 1]
    ds = (p, 3 * p)
    zero = (0, 0)

    def neg(v):
        return tuple((d - x) % d for x, d in zip(v, ds))

    # CRT split of second coordinate: b -> (b mod p, b mod 3); recombine
    def crt(bp, b3):
        for b in range(3 * p):
            if b % p == bp and b % 3 == b3:
                return b
        raise AssertionError

    crt_tab = {(bp, b3): crt(bp, b3) for bp in range(p) for b3 in range(3)}

    # all elements as (a, b); class reps
    elems = [(x, y) for x in range(p) for y in range(3 * p)]
    classes = sorted(v for v in elems if v != zero and v <= neg(v))
    cidx = {c: i for i, c in enumerate(classes)}

    def to_class(v):
        return min(v, neg(v))

    # GL(2,p) matrices
    mats = []
    for m in iproduct(range(p), repeat=4):
        if (m[0] * m[3] - m[1] * m[2]) % p != 0:
            mats.append(m)
    print(f"|GL(2,{p})| = {len(mats)}")

    # automorphism (M, s): (a, b) -> (u1', b') with u = (a, b mod p),
    # u' = M u, t' = s * (b mod 3); as permutation of class indices
    perms = []
    for M in mats:
        for s in (1, 2):
            perm = [0] * len(classes)
            ok = True
            for i, (x, y) in enumerate(classes):
                u = (x, y % p)
                t = y % 3
                u2 = ((M[0] * u[0] + M[1] * u[1]) % p,
                      (M[2] * u[0] + M[3] * u[1]) % p)
                t2 = (s * t) % 3
                img = (u2[0], crt_tab[(u2[1], t2)])
                perm[i] = cidx[to_class(img)]
            if ok:
                perms.append(tuple(perm))
    perms = sorted(set(perms))
    print(f"effective automorphism actions on classes: {len(perms)}")

    sets = []
    for line in open(path):
        if not line.startswith("ENUM"):
            continue
        toks = line.split()[1:]
        s = tuple(sorted(cidx[to_class(tuple(int(x) for x in t.strip('()').split(',')))]
                         for t in toks))
        sets.append(s)
    print(f"sets: {len(sets)}")

    # invariants
    tprofile = {}
    prodtype = 0
    for s in sets:
        nt = sum(1 for i in s if classes[i][1] % 3 != 0)
        tprofile[nt] = tprofile.get(nt, 0) + 1
        if all((classes[i][0] == 0) or (classes[i][1] == 0) for i in s):
            prodtype += 1
    print("t-profile (elements with nonzero Z_3 part -> #sets):",
          dict(sorted(tprofile.items())))
    print(f"product-type sets (supported on C_{p} x 0 union 0 x C_{3*p}):",
          prodtype)

    # orbits
    setset = set(sets)
    seen = set()
    orbits = []
    for s in sets:
        if s in seen:
            continue
        orb = set()
        stack = [s]
        while stack:
            cur = stack.pop()
            if cur in orb:
                continue
            orb.add(cur)
            for pm in perms:
                img = tuple(sorted(pm[i] for i in cur))
                if img not in orb:
                    stack.append(img)
        assert orb <= setset, "orbit leaves the extremal family — impossible"
        seen |= orb
        orbits.append((len(orb), s))
    orbits.sort(reverse=True)
    print(f"ORBITS: {len(orbits)}")
    for size, rep in orbits[:12]:
        rep_elems = [classes[i] for i in rep]
        nt = sum(1 for v in rep_elems if v[1] % 3 != 0)
        print(f"  orbit size {size:6d}  t-elems {nt}  rep {rep_elems}")
    if len(orbits) > 12:
        print(f"  ... and {len(orbits) - 12} more orbits")
    sizes = {}
    for size, _ in orbits:
        sizes[size] = sizes.get(size, 0) + 1
    print("orbit size histogram:", dict(sorted(sizes.items(), reverse=True)))


if __name__ == "__main__":
    main()
