#!/usr/bin/env python3
"""Convert simple-graph graph6 lines (cubic) to multig -T lines (mult 1),
so strong6's default mode colors the truncation T(G).  Non-cubic input is
rejected."""
import sys

for line in sys.stdin:
    s = line.strip()
    if not s:
        continue
    n = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        v = ord(ch) - 63
        bits += [(v >> b) & 1 for b in range(5, -1, -1)]
    edges = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                edges.append((i, j))
            k += 1
    deg = [0] * n
    for a, b in edges:
        deg[a] += 1
        deg[b] += 1
    assert all(d == 3 for d in deg), "not cubic"
    print("%d %d  %s" % (n, len(edges),
                         " ".join("%d %d 1" % e for e in edges)))
