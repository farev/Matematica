#!/usr/bin/env python3
"""verify_maximality.py — definition-level check of an extremal-set census.

Input: an --enum output of dpm (lines "ENUM (a,b) (c,d) ..."), the group, and
the census count claimed for that size. Verifies, directly from the
definition and independently of both engines' DFS logic:

  1. the file contains exactly the claimed number of distinct sets;
  2. every set is ±zero-sum-free (all 3^k − 1 signed subset sums nonzero);
  3. no set extends: for every sign-class representative c outside the set,
     some signed combination with coefficient ±1 on c and {−1,0,1} on the
     set sums to zero.

Together with agreement of two independent engines on the census counts
(which say these are ALL free sets of that size), 2+3 certify that k is the
maximum free length, i.e. D± = k + 1.

Usage:
  python3 verify_maximality.py --group 5 15 --size 5 --expect 85155 --file enum_5_15_size5.txt
"""
import sys
from itertools import product


def main():
    a = sys.argv
    gi, si, ei, fi = a.index("--group"), a.index("--size"), a.index("--expect"), a.index("--file")
    ds = tuple(int(x) for x in a[gi + 1:si])
    size = int(a[si + 1])
    expect = int(a[ei + 1])
    path = a[fi + 1]

    zero = tuple(0 for _ in ds)

    def neg(v):
        return tuple((d - x) % d for x, d in zip(v, ds))

    # sign-class representatives, independently derived
    def elements():
        cur = [zero]
        for i, d in enumerate(ds):
            cur = [t[:i] + (x,) + t[i + 1:] for t in cur for x in range(d)]
        return cur

    allel = elements()
    classes = [v for v in allel if v != zero and v <= neg(v)]

    sets = []
    for line in open(path):
        if not line.startswith("ENUM"):
            continue
        toks = line.split()[1:]
        s = tuple(tuple(int(x) for x in t.strip("()").split(",")) for t in toks)
        assert len(s) == size, f"bad line size: {line}"
        sets.append(s)
    uniq = set(frozenset(s) for s in sets)
    print(f"sets read: {len(sets)}, distinct: {len(uniq)}, expected: {expect}")
    ok_count = len(sets) == expect and len(uniq) == expect

    # precompute all 3^size coefficient vectors once
    coeff_all = [c for c in product((-1, 0, 1), repeat=size) if any(c)]

    bad_free = 0
    bad_max = 0
    for idx, s in enumerate(sets):
        # 2. freeness
        free = True
        for c in coeff_all:
            t = tuple(sum(ci * w[i] for ci, w in zip(c, s)) % d
                      for i, d in enumerate(ds))
            if t == zero:
                free = False
                break
        if not free:
            bad_free += 1
            if bad_free <= 3:
                print("NOT FREE:", s)
            continue
        # 3. non-extendability: reach set of s, then c extends iff
        #    0 ∉ R ∪ (R±c) ∪ {±c}  ⟺  (c ∈/ ...) — direct: c extends iff
        #    no coefficient vector with ±1 on c hits zero ⟺
        #    c ∉ R and −c ∉ R and (R+c) ∌ 0 and (R−c) ∌ 0
        #    ⟺ c ∉ R ∪ −R  (since 0 ∈ R+c ⟺ −c ∈ R). R is ±symmetric, so
        #    simply: c extends iff c ∉ R. Compute R once per set.
        R = set()
        for c in coeff_all:
            t = tuple(sum(ci * w[i] for ci, w in zip(c, s)) % d
                      for i, d in enumerate(ds))
            R.add(t)
        inset = set(s) | {neg(w) for w in s}
        for c in classes:
            if c in inset:
                continue
            if c not in R:
                bad_max += 1
                if bad_max <= 3:
                    print("EXTENDABLE:", s, "by", c)
                break
        if idx % 20000 == 0:
            print(f"  ...{idx} checked", flush=True)

    print(f"free: {len(sets) - bad_free}/{len(sets)}; "
          f"non-extendable: {len(sets) - bad_free - bad_max}/{len(sets) - bad_free}")
    verdict = ok_count and bad_free == 0 and bad_max == 0
    print("MAXIMALITY", "PASS" if verdict else "FAIL")
    sys.exit(0 if verdict else 1)


if __name__ == "__main__":
    main()
