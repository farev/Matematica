#!/usr/bin/env python3
"""Engine A: exact computation of the plus-minus weighted Davenport constant.

For a finite abelian group G = Z_{n1} + ... + Z_{nr} (given by its cyclic
orders), computes

    dpm(G) = maximum length of a plus-minus zero-sum-free sequence over G,
    Dpm(G) = dpm(G) + 1   (the plus-minus weighted Davenport constant).

A sequence S = g_1 ... g_l over G is plus-minus zero-sum-free (pm-zsf) if no
nonempty subsequence T and signs eps_i in {+1,-1} give sum_{g_i in T} eps_i
g_i = 0.

Facts used (proved in NOTE.md, all elementary):

  F1. A pm-zsf sequence has pairwise distinct elements (g,g yields g-g=0),
      never contains 0, and never contains both g and -g (g+(-g)=0).  So a
      pm-zsf sequence is a SET containing at most one element of each class
      {g,-g}, and replacing an element by its inverse preserves pm-zsf-ness.
      Hence dpm is computed over sets of class representatives.

  F2. Let A(C) = { sum over C' subset C of eps_g g : eps in {-1,0,+1}^C }
      (all signed subset sums, empty sum 0 included).  For g not in C,
      C + g is pm-zsf  iff  C is pm-zsf and g not in A(C) and -g not in A(C).
      Moreover A(C+g) = A(C) | (A(C)+g) | (A(C)-g).

  F2 makes the exhaustive DFS below correct: the search tree over
  index-increasing sets of class representatives, pruned by F2, visits
  exactly the pm-zsf sets, each once.  Its maximum depth is dpm(G).

This engine favours transparency over speed: elements are integer-encoded
tuples, the signed-sum set A is a Python set of encoded elements.  All
arithmetic is exact (Python ints).  Cross-checked against the independent C
engine (dpm_fast.c) and the direct 3^L verifier (verify_witness.py).

Usage:
    python3 dpm.py 5 15            # d_pm and D_pm of Z_5 + Z_15, witnesses
    python3 dpm.py 5 15 --all     # also count all extremal pm-zsf sets
    python3 dpm.py 5 15 --json out.json
"""

import sys
import json
import time


class Group:
    """Finite abelian group as a product of cyclic groups, integer-encoded."""

    def __init__(self, orders):
        assert all(n >= 1 for n in orders)
        self.orders = tuple(orders)
        self.N = 1
        for n in orders:
            self.N *= n
        # mixed-radix encoding: idx = ((x1*n2)+x2)*n3+x3 ...
        self.radix = []
        m = self.N
        for n in orders:
            m //= n
            self.radix.append(m)

    def encode(self, tup):
        return sum(x % n * r for x, n, r in zip(tup, self.orders, self.radix))

    def decode(self, idx):
        out = []
        for n, r in zip(self.orders, self.radix):
            out.append((idx // r) % n)
        return tuple(out)

    def add(self, a, b):
        # a, b encoded
        s = 0
        for n, r in zip(self.orders, self.radix):
            s += ((a // r + b // r) % n) * r
        return s

    def neg(self, a):
        s = 0
        for n, r in zip(self.orders, self.radix):
            s += ((-(a // r)) % n) * r
        return s

    def classes(self):
        """Canonical representatives of the classes {g,-g}, g != 0."""
        reps = []
        seen = set()
        for g in range(1, self.N):
            if g in seen:
                continue
            h = self.neg(g)
            seen.add(g)
            seen.add(h)
            reps.append(min(g, h))
        return sorted(reps)


def search(group, collect_extremal=False, witness_cap=200):
    """Exhaustive DFS over pm-zsf sets.  Returns result dict."""
    reps = group.classes()
    M = len(reps)
    negs = {g: group.neg(g) for g in reps}
    add = group.add

    best = {"depth": 0, "witnesses": [[]], "count_at_best": 1}
    stats = {"nodes": 0}

    def dfs(start, chosen, A):
        depth = len(chosen)
        if depth > best["depth"]:
            best["depth"] = depth
            best["witnesses"] = [list(chosen)]
            best["count_at_best"] = 1
        elif depth == best["depth"] and depth > 0:
            best["count_at_best"] += 1
            if len(best["witnesses"]) < witness_cap:
                best["witnesses"].append(list(chosen))
        for j in range(start, M):
            g = reps[j]
            if g in A or negs[g] in A:
                continue
            stats["nodes"] += 1
            A2 = set(A)
            for s in A:
                A2.add(add(s, g))
                A2.add(add(s, negs[g]))
            chosen.append(g)
            dfs(j + 1, chosen, A2)
            chosen.pop()

    t0 = time.time()
    dfs(0, [], {0})
    t1 = time.time()

    # count_at_best counts every pm-zsf set of the final best depth reached
    # while it was the best; recount exactly if extremal census requested.
    n_extremal = None
    if collect_extremal:
        n_extremal = 0
        target = best["depth"]
        exact_witnesses = []

        def dfs2(start, chosen, A):
            nonlocal n_extremal
            if len(chosen) == target:
                n_extremal += 1
                if len(exact_witnesses) < witness_cap:
                    exact_witnesses.append(list(chosen))
                return
            for j in range(start, M):
                g = reps[j]
                if g in A or negs[g] in A:
                    continue
                A2 = set(A)
                for s in A:
                    A2.add(add(s, g))
                    A2.add(add(s, negs[g]))
                chosen.append(g)
                dfs2(j + 1, chosen, A2)
                chosen.pop()

        dfs2(0, [], {0})
        best["witnesses"] = exact_witnesses

    return {
        "orders": list(group.orders),
        "N": group.N,
        "n_classes": M,
        "dpm": best["depth"],
        "Dpm": best["depth"] + 1,
        "witnesses_encoded": best["witnesses"][:witness_cap],
        "witnesses": [
            [group.decode(g) for g in w] for w in best["witnesses"][:witness_cap]
        ],
        "n_extremal_sets": n_extremal,
        "nodes": stats["nodes"],
        "seconds": round(t1 - t0, 3),
        "engine": "A/python-setDFS",
    }


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    orders = [int(a) for a in args]
    if not orders:
        print(__doc__)
        sys.exit(1)
    collect = "--all" in flags
    g = Group(orders)
    res = search(g, collect_extremal=collect)
    out = None
    for f in flags:
        if f.startswith("--json"):
            pass
    if "--json" in " ".join(flags):
        i = sys.argv.index("--json")
        out = sys.argv[i + 1]
    label = " + ".join(f"Z_{n}" for n in orders)
    print(f"G = {label}  |G| = {res['N']}  classes = {res['n_classes']}")
    print(f"d_pm(G) = {res['dpm']}   D_pm(G) = {res['Dpm']}")
    print(f"nodes = {res['nodes']}  time = {res['seconds']}s")
    if res["n_extremal_sets"] is not None:
        print(f"extremal pm-zsf sets (as class-rep sets) = {res['n_extremal_sets']}")
    for w in res["witnesses"][:5]:
        print("  witness:", w)
    if out:
        with open(out, "w") as f:
            json.dump(res, f, indent=1, default=list)
        print("wrote", out)


if __name__ == "__main__":
    main()
