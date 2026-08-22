#!/usr/bin/env python3
"""dpm_indep.py — independent re-implementation of the ±zero-sum-free census.

Written separately from dpm.c as a cross-check: elements are tuples, group
arithmetic is componentwise modular arithmetic done inline, the reach set is
a Python set of tuples, and the recursion carries immutable state (no undo
stack). Reports the same census vector (number of ±free k-subsets of sign
classes) so the two engines can be compared entry by entry.

Usage: python3 dpm_indep.py d1 [d2 ...] [--maxdepth D]
"""
import sys


def main():
    args = [a for a in sys.argv[1:]]
    maxdepth = 64
    if "--maxdepth" in args:
        i = args.index("--maxdepth")
        maxdepth = int(args[i + 1])
        del args[i:i + 2]
    ds = tuple(int(a) for a in args)
    assert ds and all(d >= 2 for d in ds)

    def neg(v):
        return tuple((d - x) % d for x, d in zip(v, ds))

    def add(u, v):
        return tuple((x + y) % d for x, y, d in zip(u, v, ds))

    # all nonzero elements, lexicographic; sign-class representatives
    elems = []

    def gen(prefix):
        if len(prefix) == len(ds):
            elems.append(tuple(prefix))
            return
        for x in range(ds[len(prefix)]):
            gen(prefix + [x])

    gen([])
    zero = elems[0]
    assert zero == tuple(0 for _ in ds)
    nonzero = [v for v in elems if v != zero]
    classes = sorted(v for v in nonzero if v <= neg(v))

    count = {}
    best = {"len": 0, "wit": ()}

    def dfs(start, chosen, reach):
        k = len(chosen)
        if k > 0:
            count[k] = count.get(k, 0) + 1
            if k > best["len"]:
                best["len"] = k
                best["wit"] = tuple(chosen)
        if k >= maxdepth:
            return
        for i in range(start, len(classes)):
            c = classes[i]
            nc = neg(c)
            new = {c, nc}
            dead = False
            for s in reach:
                for t in (add(s, c), add(s, nc)):
                    if t == zero:
                        dead = True
                        break
                    new.add(t)
                if dead:
                    break
            if dead:
                continue
            dfs(i + 1, chosen + [c], reach | new)

    dfs(0, [], frozenset())

    print("GROUP", *ds)
    print("N", len(elems), "NONZERO", len(nonzero), "CLASSES", len(classes))
    for k in sorted(count):
        print("FREE", k, count[k])
    print("L", best["len"])
    print("DPM", best["len"] + 1)
    print("WITNESS", " ".join(str(w).replace(" ", "") for w in best["wit"]))


if __name__ == "__main__":
    main()
