#!/usr/bin/env python3
"""Emit the chain-family quotients C_k (two balloons joined through k
dumbbells) in multig -T format, k = 0..K (default 8).  T(C_k) is a
diamond-free claw-free cubic graph on 18 + 6k vertices; by the Balloon
Lemma none is strongly 6-edge-colorable.

Usage: make_family.py [K] | ./strong6
"""
import sys

K = int(sys.argv[1]) if len(sys.argv) > 1 else 8
for k in range(K + 1):
    n = 6 + 2 * k
    edges = {}

    def add(a, b, m=1):
        key = (min(a, b), max(a, b))
        edges[key] = edges.get(key, 0) + m

    add(0, 1, 2)          # left balloon: 0‖1 tied at 2
    add(0, 2)
    add(1, 2)
    prev = 2
    for i in range(k):    # dumbbells 3+2i ‖ 4+2i
        x, y = 3 + 2 * i, 4 + 2 * i
        add(x, y, 2)
        add(prev, x)
        prev = y
    add(n - 3, n - 2, 2)  # right balloon: (n-3)‖(n-2) tied at n-1
    add(n - 3, n - 1)
    add(n - 2, n - 1)
    add(prev, n - 1)
    lst = sorted(edges.items())
    print("%d %d  %s" % (n, len(lst),
                         " ".join("%d %d %d" % (a, b, m)
                                  for (a, b), m in lst)))
