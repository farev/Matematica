"""Search for additive uniform morphisms whose fixed point is U-free.

Ansatz: phi(x) = x + B0 letterwise mod n (sigma-rotation, sigma = +1),
B0 in Sigma_n^k, B0[0] = 0.  Fixed point W = phi^omega(0) satisfies
W[q] = W[q // k] + W[q % k]  (mod n), i.e. W[q] = sum of B0 over the
base-k digits of q — a digit-sum word generalizing Thue-Morse.

DFS over B0's letters at positions < k; positions >= k are forced, so a
candidate dies as soon as its forced continuation violates U-freeness.
Survivors to depth D are near-certain witnesses, to be certified separately.

Usage: python3 blocksearch.py <n> <num> <den> <kmin> <kmax> <depth> [maxnodes]
"""

import sys
import time

from urt import UInc


def search_k(n, num, den, k, depth, maxnodes=20_000_000, first_only=False):
    inc = UInc(num, den, depth + 2)
    w = []
    nodes = 0
    survivors = []
    reached = 0

    def rec():
        nonlocal nodes, reached
        q = len(w)
        reached = max(reached, q)
        if q == depth:
            survivors.append(tuple(w[:k]))
            return first_only
        if nodes >= maxnodes:
            return True
        if q < k:
            cands = range(n) if q > 0 else (0,)
        else:
            cands = ((w[q // k] + w[q % k]) % n,)
        for c in cands:
            nodes += 1
            if inc.push(c):
                w.append(c)
                stop = rec()
                w.pop()
                inc.pop()
                if stop:
                    return True
            else:
                inc.pop()
        return False

    t0 = time.time()
    rec()
    dt = time.time() - t0
    return survivors, reached, nodes, dt


if __name__ == "__main__":
    n, num, den, kmin, kmax, depth = map(int, sys.argv[1:7])
    maxnodes = int(sys.argv[7]) if len(sys.argv) > 7 else 20_000_000
    for k in range(kmin, kmax + 1):
        surv, reached, nodes, dt = search_k(n, num, den, k, depth, maxnodes)
        print(f"k={k}: {len(surv)} survivors at depth {depth}, "
              f"max reach {reached}, {nodes} nodes [{dt:.1f}s]", flush=True)
        for b in surv[:5]:
            print("   B0 =", ",".join(map(str, b)))
        if surv:
            with open(f"data/blocks_n{n}_k{k}.txt", "w") as f:
                for b in surv:
                    f.write(",".join(map(str, b)) + "\n")
