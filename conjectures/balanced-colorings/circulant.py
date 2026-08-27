#!/usr/bin/env python3
"""Circulant lower bounds for E*(N, s) = max edges, no K_s, no I_s.

Sweeps all connection sets S subseteq {1..N//2} for circulants on Z_N,
computes clique and independence numbers exactly (bitset branch-and-bound),
and reports the max edge count among graphs with omega < s and alpha < s.

Usage: python3 circulant.py N s
"""
import sys
from functools import lru_cache

def max_clique_ge(adj_masks, n, k):
    """True iff the graph has a clique of size >= k. Simple BB on bitsets."""
    best = 0
    def expand(cand, size):
        nonlocal best
        if size + bin(cand).count("1") < k:
            return False
        if size >= k:
            return True
        c = cand
        while c:
            v = (c & -c).bit_length() - 1
            c &= c - 1
            if expand(cand & adj_masks[v] & ~((1 << (v + 1)) - 1), size + 1):
                return True
            cand &= ~(1 << v)
            if size + bin(cand).count("1") < k:
                return False
        return False
    return expand((1 << n) - 1, 0)

def main():
    N, s = int(sys.argv[1]), int(sys.argv[2])
    half = N // 2
    diffs = list(range(1, half + 1))
    best = (-1, None)
    results = []
    for mask in range(1 << len(diffs)):
        S = {diffs[i] for i in range(len(diffs)) if (mask >> i) & 1}
        # edge count: each difference class d contributes N edges, except the
        # half class d = N/2 (even N), which contributes N/2
        e = sum(N // 2 if 2 * d == N else N for d in S)
        if e <= best[0]:
            continue
        adj = [0] * N
        for x in range(N):
            for d in S:
                adj[x] |= 1 << ((x + d) % N)
                adj[x] |= 1 << ((x - d) % N)
        # clique check on G, independence = clique on complement
        if max_clique_ge(adj, N, s):
            continue
        cadj = [(~adj[x]) & ((1 << N) - 1) & ~(1 << x) for x in range(N)]
        if max_clique_ge(cadj, N, s):
            continue
        best = (e, sorted(S))
        results.append(best)
        print(f"E*({N},{s}) >= {e}  circulant S = {sorted(S)}")
    if best[0] < 0:
        print(f"no circulant on Z_{N} avoids K_{s} and I_{s}")
    else:
        print(f"best circulant: {best[0]} edges, S = {best[1]}")

if __name__ == "__main__":
    main()
