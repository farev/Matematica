#!/usr/bin/env python3
"""Twisted tower: layers by last coordinate. Layer 0 = colE, layer 1 = g.colE, layer 2 = h.colO
for automorphisms g, h in (Z_2)^{k-1} x S_{k-1}.  Report which (g,h) admit a lift, for E_k and O_k.
usage: tower2.py k  (uses col_even0_k{k-1}.txt and col_even1_k{k-1}.txt as the base colourings)"""
import itertools
import sys

from tower import parse, solve_with_fixed, vertex_set

k = int(sys.argv[1]); d = k - 1
colE = parse(f"col_even0_k{d}.txt"); colO = parse(f"col_even1_k{d}.txt")
SW = {0: (0, 1, 2), 1: (1, 0, 2)}
elems = [(pi, tuple(SW[b] for b in bits)) for pi in itertools.permutations(range(d)) for bits in itertools.product((0, 1), repeat=d)]
def act(g, v):
    pi, sig = g; w = [None] * d
    for i in range(d): w[pi[i]] = sig[i][v[i]]
    return tuple(w)
def transport(col, g):
    pi, _ = g
    out = {}
    for (x, y), c in col.items():
        gx, gy = act(g, x), act(g, y)
        if gx > gy: gx, gy = gy, gx
        out[(gx, gy)] = pi[c]
    return out
limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
for parity, name in ((0, 'E'), (1, 'O')):
    V = vertex_set(k, parity)
    same = colE if parity == 0 else colO
    other = colO if parity == 0 else colE
    found = 0; tried = 0
    for g in elems:
        for h in elems:
            tried += 1
            if tried > limit: break
            fixed = {}
            for (x, y), c in same.items(): fixed[(x + (0,), y + (0,))] = c
            for (x, y), c in transport(same, g).items(): fixed[(x + (1,), y + (1,))] = c
            for (x, y), c in transport(other, h).items(): fixed[(x + (2,), y + (2,))] = c
            import contextlib
            import io
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                col = solve_with_fixed(V, k, fixed)
            if col is not None:
                found += 1
                print(f"{name}_{k}: lift exists with g={g} h={h}", flush=True)
                if found >= 5: break
        if found >= 5 or tried > limit: break
    print(f"{name}_{k}: found {found} lifts among {tried} (g,h) tried", flush=True)
