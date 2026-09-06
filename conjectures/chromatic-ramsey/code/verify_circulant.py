#!/usr/bin/env python3
"""From-definition verifier for a circulant witness of F(j,k) >= n (no SAT, no sharing of code
with the search).  Input: JSON {n,k,j,classes:{c:[d,...]},colourings:{c:[a_v]}}.
Checks: (1) the classes partition {1..floor(n/2)}; (2) every pair {v,w} of Z_n gets the colour of
its difference class; (3) brute force over all triples: no monochromatic triangle; (4) for every
class c the map v -> a_v is a proper vertex j-colouring of the class's graph."""
import itertools
import json
import sys

w = json.load(open(sys.argv[1]))
n, k, j = w["n"], w["k"], w["j"]
classes = {int(c): set(v) for c, v in w["classes"].items()}
cols = {int(c): v for c, v in w["colourings"].items()}
D = set(range(1, n // 2 + 1))
assert set().union(*classes.values()) == D and sum(len(s) for s in classes.values()) == len(D), "not a partition"
def dn(d): return min(d % n, (-d) % n)
colour_of = {}
for d in D:
    for c, s in classes.items():
        if d in s: colour_of[d] = c
edge = {}
for v in range(n):
    for u in range(v + 1, n):
        edge[(v, u)] = colour_of[dn(u - v)]
mono = 0
for a, b, c in itertools.combinations(range(n), 3):
    if edge[(a, b)] == edge[(a, c)] == edge[(b, c)]: mono += 1
assert mono == 0, f"{mono} monochromatic triangles"
for c in range(k):
    assert len(cols[c]) == n and all(0 <= a < j for a in cols[c])
    for (v, u), cc in edge.items():
        if cc == c: assert cols[c][v] != cols[c][u], f"improper colouring in class {c}"
print(f"VERIFIED: K_{n} {k}-coloured by differences, every class triangle-free ({len(edge)} edges, "
      f"{n*(n-1)*(n-2)//6} triples checked) and properly {j}-coloured; hence F({j},{k}) >= {n}")
