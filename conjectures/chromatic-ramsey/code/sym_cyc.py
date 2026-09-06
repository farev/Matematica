#!/usr/bin/env python3
"""Colour E_k invariant under s (global 0<->1 swap) and rho (cyclic coordinate shift, rotating
colours). Print the colouring by orbits of pairs.  usage: sym_cyc.py k [extra: 'noswap'|'norho']"""
import sys, itertools, collections
from fixed_sat import solve

k = int(sys.argv[1]); flags = sys.argv[2:]
V = [v for v in itertools.product(range(3), repeat=k) if v.count(2) % 2 == 0]
ident = tuple(range(k)); ID = (0, 1, 2); SW = (1, 0, 2)
s = (ident, tuple(SW for _ in range(k)))
rho = (tuple((i + 1) % k for i in range(k)), tuple(ID for _ in range(k)))
syms = []
if 'noswap' not in flags: syms.append(s)
if 'norho' not in flags: syms.append(rho)
col = solve(V, k, syms=syms)
if col is None:
    print("no invariant colouring"); sys.exit()
def act(g, v):
    pi, sig = g; w = [None] * k
    for i in range(k): w[pi[i]] = sig[i][v[i]]
    return tuple(w)
# orbits of unordered pairs under <s, rho>
G = [s, rho]
seen = set(); orbits = []
for (x, y) in col:
    if (x, y) in seen: continue
    orb = set(); stack = [(x, y)]
    while stack:
        p = stack.pop()
        if p in orb: continue
        orb.add(p)
        for g in G:
            gx, gy = act(g, p[0]), act(g, p[1])
            if gx > gy: gx, gy = gy, gx
            stack.append((gx, gy))
    seen |= orb; orbits.append(sorted(orb))
print(f"k={k}: {len(col)} pairs, {len(orbits)} orbits under <s,rho>")
fmt = lambda v: ''.join(map(str, v))
for orb in orbits:
    x, y = orb[0]
    cs = sorted(set(col[p] for p in orb))
    print(f"  orbit size {len(orb):2d}: rep {fmt(x)}-{fmt(y)} colour {col[(x,y)]}  D={[c for c in range(k) if x[c]!=y[c]]}")
with open(f"col_sym_k{k}.txt", "w") as f:
    for (a, b), c in sorted(col.items()):
        f.write(f"{fmt(a)} {fmt(b)} {c}\n")
