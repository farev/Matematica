"""Hybrid search: canonical-language DFS x additive-consistency propagation.

For a witness of the additive ansatz W[q] = W[q//k] + W[q%k] (mod n),
W[0] = 0, we search the CANONICAL language tree (first occurrences named
0,1,2,...) while maintaining a partial injection nu: canonical letters ->
Z_n with the constraints nu(C[q]) = nu(C[q//k]) + nu(C[q%k]) for q >= k
and nu(C[0]) = 0.  At q >= k the equation usually pins the concrete value
v; the canonical branch must then use a letter compatible with v under nu
(assigned letter with nu = v, or a fresh letter, assigning nu := v).

Usage: python3 nu_search.py <n> <num> <den> <kmin> <kmax> <depth> [maxnodes]
"""

import sys
import time

from urt import UInc


def search_k(n, num, den, k, depth, maxnodes=5_000_000):
    inc = UInc(num, den, depth + 2)
    C = []          # canonical word
    nu = {}         # canonical letter -> Z_n value
    nuinv = {}      # value -> canonical letter
    nodes = 0
    survivors = []
    reached = 0

    def assign(c, v):
        """Try nu[c] = v; return token for undo or None if inconsistent."""
        if c in nu:
            return ("noop",) if nu[c] == v else None
        if v in nuinv:
            return None
        nu[c] = v
        nuinv[v] = c
        return ("did", c, v)

    def undo(tok):
        if tok[0] == "did":
            _, c, v = tok
            del nu[c]
            del nuinv[v]

    def rec(used):
        nonlocal nodes, reached
        q = len(C)
        reached = max(reached, q)
        if q == depth:
            survivors.append((tuple(C), dict(nu)))
            return True
        if nodes >= maxnodes:
            return True
        # candidate canonical letters
        cands = list(range(min(used + 1, n)))
        # additive constraint value (needs nu on the two source letters)
        vknown = None
        if q >= k:
            ci, cj = C[q // k], C[q % k]
            if ci in nu and cj in nu:
                vknown = (nu[ci] + nu[cj]) % n
        for c in cands:
            nodes += 1
            tok = ("noop",)
            if q == 0:
                tok = assign(c, 0)
                if tok is None:
                    continue
            elif vknown is not None:
                tok = assign(c, vknown)
                if tok is None:
                    continue
            if inc.push(c):
                C.append(c)
                stop = rec(used + 1 if c == used else used)
                C.pop()
                inc.pop()
                undo(tok)
                if stop:
                    return True
            else:
                inc.pop()
                undo(tok)
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
        note = ""
        if surv:
            C, nu = surv[0]
            B0 = tuple(nu[C[j]] for j in range(k))
            note = "  B0=" + ",".join(map(str, B0))
        print(f"k={k}: reach {reached}/{depth}, {nodes} nodes, "
              f"{len(surv)} survivors [{dt:.1f}s]{note}", flush=True)
        if surv:
            with open(f"data/nu_n{n}_k{k}.txt", "w") as f:
                for C, nu in surv:
                    B0 = tuple(nu[C[j]] for j in range(k))
                    f.write("B0=" + ",".join(map(str, B0)) + "\n")
                    f.write("C=" + ",".join(map(str, C)) + "\n")
