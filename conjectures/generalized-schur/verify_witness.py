#!/usr/bin/env python3
"""Independent verifier for generalized-Schur lower-bound witnesses.

Reads a witness file:  line 1: n k t_1 .. t_k   line 2: colors of 1..n (0-based)
Checks, for each color j, that the class S_j = {x : c(x)=j} contains NO
solution of x_1 + ... + x_{t_j - 1} = x_{t_j} with all variables in S_j
(repeats allowed).

Algorithm (deliberately different from the CNF encoder's partition
enumeration): iterated-sumset bitsets. R_1 = S_j; R_{m+1} = { r + a <= n }.
R_{t_j-1} is the set of values representable as a sum of exactly t_j - 1
elements of S_j; the class is bad iff R_{t_j-1} intersects S_j. On failure a
concrete violating tuple is reconstructed by greedy backtracking and printed.
Exit 0 iff the witness is good.
"""
import sys


def bitset(vals):
    b = 0
    for v in vals:
        b |= 1 << v
    return b


def check(n, ts, colors):
    ok = True
    for j, t in enumerate(ts):
        S = [x for x in range(1, n + 1) if colors[x - 1] == j]
        Sb = bitset(S)
        mask = (1 << (n + 1)) - 1
        layers = [None, Sb]  # layers[m] = sums of exactly m elements, <= n
        for m in range(2, t):
            prev = layers[m - 1]
            cur = 0
            for a in S:
                cur |= (prev << a)
            cur &= mask
            layers.append(cur)
        bad = layers[t - 1] & Sb
        if bad:
            s = bad.bit_length() - 1  # one violating target
            # reconstruct: peel one summand at a time
            tup = []
            rem = s
            for m in range(t - 1, 1, -1):
                for a in S:
                    if rem - a >= 1 and (layers[m - 1] >> (rem - a)) & 1:
                        tup.append(a)
                        rem -= a
                        break
            tup.append(rem)
            assert sum(tup) == s and all(x in set(S) for x in tup + [s])
            print(f"BAD color {j} (t={t}): {'+'.join(map(str,sorted(tup)))} = {s}, all in class")
            ok = False
    return ok


def main():
    path = sys.argv[1]
    with open(path) as f:
        head = f.readline().split()
        n, k = int(head[0]), int(head[1])
        ts = [int(x) for x in head[2:2 + k]]
        colors = [int(c) for c in f.readline().split()]
    assert len(colors) == n, f"expected {n} colors, got {len(colors)}"
    assert all(0 <= c < k for c in colors)
    if check(n, ts, colors):
        print(f"WITNESS OK n={n} ts={ts}: no monochromatic solution in any class")
        sys.exit(0)
    sys.exit(1)


if __name__ == "__main__":
    main()
