#!/usr/bin/env python3
"""From-definition verifier for a type-formulation witness of F(j,k) >= n.
Input: text file, one line per pair "x y c" where x, y are types (either "012" or "(0, 1, 2)")
and c is the colour (a coordinate).  Checks, without any solver: (1) every listed colour is a
coordinate where the two types differ; (2) every pair of the vertex set appears exactly once;
(3) no monochromatic triangle.  Prints n, k, j (max value + 1) — the certificate of F(j,k) >= n.
usage: verify_witness.py witness.txt"""
import itertools
import re
import sys

col = {}; V = set()
for line in open(sys.argv[1]):
    line = line.strip()
    if not line: continue
    nums = re.findall(r'\d+', line)
    c = int(nums[-1]); digits = nums[:-1]
    if len(digits) == 2:               # compact "012 021 c"
        a = tuple(map(int, digits[0])); b = tuple(map(int, digits[1]))
    else:                              # "(0, 1, 2) (0, 2, 1) c"
        k = (len(digits)) // 2
        a = tuple(map(int, digits[:k])); b = tuple(map(int, digits[k:]))
    assert len(a) == len(b)
    if a > b: a, b = b, a
    assert (a, b) not in col, ("duplicate pair", a, b)
    assert a[c] != b[c], ("colour is not a differing coordinate", a, b, c)
    col[(a, b)] = c; V.add(a); V.add(b)
V = sorted(V); n = len(V); k = len(V[0]); j = max(max(v) for v in V) + 1
assert len(col) == n * (n - 1) // 2, ("missing pairs", len(col), n * (n - 1) // 2)
for a, b, d in itertools.combinations(V, 3):
    assert not (col[(a, b)] == col[(a, d)] == col[(b, d)]), ("monochromatic triangle", a, b, d)
print(f"VERIFIED: {n} distinct types in [{j}]^{k}, every pair coloured by a differing coordinate, "
      f"no monochromatic triangle ({n*(n-1)*(n-2)//6} triples checked): F({j},{k}) >= {n}")
