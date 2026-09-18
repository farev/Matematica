#!/usr/bin/env python3
"""Independent witness checker for Leech's covering tree problem (OEIS A007187).
Input: n k and a list of weighted edges "(u,v,w)" (as printed by the search engines,
weights >= 1000 mean 'free' edges whose weight is irrelevant and is set to 1000+i).
Checks: the edges form a spanning tree on n vertices with positive integer weights,
and every integer 1..k occurs as a path sum between two vertices.
Exit 0 and 'OK' iff the witness is valid.  No code shared with the search engines."""
import sys, re
from fractions import Fraction

def main():
    n, k = int(sys.argv[1]), int(sys.argv[2])
    text = ' '.join(sys.argv[3:]) if len(sys.argv) > 3 else sys.stdin.read()
    edges = [(int(a), int(b), int(w)) for a, b, w in re.findall(r'\((\d+),(\d+),(\d+)\)', text)]
    assert len(edges) == n - 1, f"expected {n-1} edges, got {len(edges)}"
    adj = {v: [] for v in range(n)}
    for a, b, w in edges:
        assert 0 <= a < n and 0 <= b < n and a != b and w >= 1, f"bad edge {(a,b,w)}"
        adj[a].append((b, w)); adj[b].append((a, w))
    # connectivity (n-1 edges + connected => tree)
    seen = {0}; stack = [0]
    while stack:
        v = stack.pop()
        for u, w in adj[v]:
            if u not in seen: seen.add(u); stack.append(u)
    assert len(seen) == n, "not connected"
    sums = {}
    for s in range(n):
        dist = {s: 0}; stack = [s]
        while stack:
            v = stack.pop()
            for u, w in adj[v]:
                if u not in dist: dist[u] = dist[v] + w; stack.append(u)
        for t in range(s + 1, n): sums[dist[t]] = sums.get(dist[t], 0) + 1
    missing = [v for v in range(1, k + 1) if v not in sums]
    N = n * (n - 1) // 2
    excess = N - sum(1 for v in sums if 1 <= v <= k)
    if missing:
        print(f"FAIL n={n} k={k} missing values {missing}"); sys.exit(1)
    print(f"OK n={n} k={k}: all of 1..{k} realized; {N} pairs, excess pairs = {excess}, max distance = {max(sums)}")

if __name__ == '__main__':
    main()
