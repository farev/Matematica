#!/usr/bin/env python3
"""Which elements g of (Z_2)^k x S_k (value swaps 0<->1 per coordinate, coordinate permutations)
admit a g-invariant valid colouring of E_k?  Then try to grow invariant subgroups greedily.
usage: sym_search.py k"""
import itertools
import sys

from fixed_sat import solve

k = int(sys.argv[1])
V = [v for v in itertools.product(range(3), repeat=k) if v.count(2) % 2 == 0]
SW = {0: (0, 1, 2), 1: (1, 0, 2)}          # swap 0<->1 or not; 2 fixed
elems = []
for pi in itertools.permutations(range(k)):
    for bits in itertools.product((0, 1), repeat=k):
        elems.append((pi, tuple(SW[b] for b in bits)))
print("group elements:", len(elems))
ok = []
for g in elems:
    if g == (tuple(range(k)), tuple((0, 1, 2) for _ in range(k))): continue
    col = solve(V, k, syms=[g], verbose=False)
    if col is not None:
        ok.append(g); print("admissible:", g, flush=True)
print("admissible count:", len(ok))
# greedy: try pairs
pairs = []
for a, b in itertools.combinations(ok, 2):
    col = solve(V, k, syms=[a, b], verbose=False)
    if col is not None:
        pairs.append((a, b)); print("admissible pair:", a, b, flush=True)
print("admissible pairs:", len(pairs))
