#!/usr/bin/env python3
"""dpm_python.py — engine E2: independent Python implementation of the
exhaustive D± search, for cross-checking dpm_search.c node-for-node.

Same mathematical method (DFS over nondecreasing sequences of
sign-representatives with the signed-sum-set bitmask as state), implemented
independently: Python big-int bitmask, per-bit add loop, no code shared with
the C engine. (#nodes - 1) = number of ±zsf multisets; must equal E1's count
exactly on every cell.

Usage: python3 dpm_python.py a [b] [c] [d]
Output: same one-line format as dpm_search (module fields).
Exact integer arithmetic only.
"""
import sys


def search(mods):
    n = 1
    for m in mods:
        n *= m
    # element index: mixed radix over mods (most significant first)
    def unrank(i):
        co = []
        for m in reversed(mods):
            co.append(i % m)
            i //= m
        return tuple(reversed(co))
    def rank(co):
        i = 0
        for c, m in zip(co, mods):
            i = i * m + c
        return i
    els = [unrank(i) for i in range(n)]
    neg = [rank(tuple((-c) % m for c, m in zip(e, mods))) for e in els]
    add = [[rank(tuple((c1 + c2) % m for c1, c2, m in zip(els[i], els[j], mods)))
            for j in range(n)] for i in range(n)]
    reps = [i for i in range(1, n) if i <= neg[i]]

    best = [0]
    bestseq = [[]]
    nodes = [0]

    def dfs(T, seq, start):
        nodes[0] += 1
        if len(seq) > best[0]:
            best[0] = len(seq)
            bestseq[0] = list(seq)
        for k in range(start, len(reps)):
            g = reps[k]
            if (T >> g) & 1:
                continue
            Tp = T | (1 << g) | (1 << neg[g])
            t = T
            ag, ang = add[g], add[neg[g]]
            while t:
                lb = t & (-t)
                i = lb.bit_length() - 1
                Tp |= (1 << ag[i]) | (1 << ang[i])
                t ^= lb
            assert not (Tp & 1), "0 in signed-sum set after legal add"
            seq.append(g)
            dfs(Tp, seq, k)
            seq.pop()

    sys.setrecursionlimit(100000)
    dfs(0, [], 0)
    wit = "".join("(%s)" % ",".join(map(str, els[g])) for g in bestseq[0])
    mm = list(mods) + [1] * (4 - len(mods))
    print(f"{mm[0]} {mm[1]} {mm[2]} {mm[3]} {n} maxlen={best[0]} "
          f"dpm={best[0]+1} nodes={nodes[0]} witness={wit}")
    return best[0], nodes[0]


if __name__ == "__main__":
    mods = [int(x) for x in sys.argv[1:] if not x.startswith("-")]
    if not mods:
        print("usage: dpm_python.py a [b] [c] [d]", file=sys.stderr)
        sys.exit(1)
    search(mods)
