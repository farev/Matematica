"""Fully general search for k-uniform-morphic self-similar U-free words.

We look for an infinite word W over Sigma_n with W = phi(W) for SOME
k-uniform morphism phi (unknown blocks), i.e. W[q] = B_{W[q//k]}[q % k],
with W[0] = first letter of B_{W[0]} (prolongable fixed point).

Structural constraint only: positions q, q' with the same class
(parent letter W[q//k], offset q%k) carry the same letter.  The DFS runs
in canonical space; the first position of each class is a free choice
(canonical letters + fresh), later positions are forced.  UInc prunes.

This subsumes every uniform-morphism ansatz (affine included) over Sigma_n
with block length k.  Exhaustion at depth D certifies: no U-free
prolongable fixed point of ANY k-uniform morphism exists whose prefix of
length D is U-free (i.e. the ansatz is dead at this k).

Usage: python3 selfsim_search.py <n> <num> <den> <kmin> <kmax> <depth> [maxnodes]
"""

import sys
import time

from urt import UInc


def search_k(n, num, den, k, depth, maxnodes=5_000_000, first_only=True):
    inc = UInc(num, den, depth + 2)
    W = []
    classpos = {}  # (parent_letter, offset) -> canonical letter chosen
    nodes = 0
    reached = 0
    survivors = []

    def rec(used):
        nonlocal nodes, reached
        q = len(W)
        reached = max(reached, q)
        if q == depth:
            survivors.append(list(W))
            return first_only
        if nodes >= maxnodes:
            return True
        if q == 0:
            key = (0, 0)  # B_{W[0]}[0] = W[0] = 0: bind the class now
            forced = 0
        else:
            key = (W[q // k], q % k)
            forced = classpos.get(key)
        cands = [forced] if forced is not None else list(range(min(used + 1, n)))
        for c in cands:
            nodes += 1
            if inc.push(c):
                W.append(c)
                newkey = key is not None and key not in classpos
                if newkey:
                    classpos[key] = c
                stop = rec(used + 1 if c == used else used)
                if newkey:
                    del classpos[key]
                W.pop()
                inc.pop()
                if stop:
                    return True
            else:
                inc.pop()
        return False

    t0 = time.time()
    rec(0)
    dt = time.time() - t0
    return survivors, reached, nodes, dt


if __name__ == "__main__":
    n, num, den, kmin, kmax, depth = map(int, sys.argv[1:7])
    maxnodes = int(sys.argv[7]) if len(sys.argv) > 7 else 5_000_000
    for k in range(kmin, kmax + 1):
        surv, reached, nodes, dt = search_k(n, num, den, k, depth, maxnodes)
        ex = "EXHAUSTED" if nodes < maxnodes else "CAPPED"
        print(f"k={k}: reach {reached}/{depth}, nodes {nodes}, "
              f"surv {len(surv)}, {ex} [{dt:.0f}s]", flush=True)
        if surv:
            with open(f"data/selfsim_n{n}_k{k}.txt", "w") as f:
                f.write(",".join(map(str, surv[0])) + "\n")
            print("  SURVIVOR — saved", flush=True)
