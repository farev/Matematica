#!/usr/bin/env python3
r"""Mechanical check of the palette-block induction step r -> r+1 (Theorem B):
base = a K'-colouring of a vertex set with every class triangle-free and properly r-labelled
(here the E_3 colouring, r = 3, K' = 3, labels = coordinates); palettes = t-subsets of [K] with
pairwise |P \ Q| >= s; each block carries a copy of the base on the colours outside P; cross
edges use saturated maps f, g: [r]^s -> [r]^s.  Output verified by verify_colouring.c.
usage: blockconstruct.py K t s base_colouring.txt out.bin"""
import itertools
import struct
import sys

K, t, s = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); basefile, out = sys.argv[4], sys.argv[5]
# base colouring: lines "x y c" with x,y strings over {0,1,2}; labels = coordinates
base = {}; V = set()
for l in open(basefile):
    a, b, c = l.split(); a = tuple(map(int, a)); b = tuple(map(int, b)); base[(a, b)] = int(c); V.add(a); V.add(b)
V = sorted(V); Kp = len(V[0]); r = 3
assert Kp == K - t, "base must use exactly K-t colours"
def basecol(a, b):
    return base[(a, b)] if (a, b) in base else base[(b, a)]
# saturated maps for H=r, s (from saturated.py, H=3 s=2); for s=1,r=2: f=id, g=neg
if (r, s) == (3, 2):
    f = {(0,0):(1,0),(0,1):(2,2),(0,2):(0,1),(1,0):(2,0),(1,1):(0,0),(1,2):(0,2),(2,0):(1,2),(2,1):(1,1),(2,2):(2,1)}
    g = {(0,0):(2,1),(0,1):(0,0),(0,2):(2,0),(1,0):(0,2),(1,1):(1,1),(1,2):(1,2),(2,0):(2,2),(2,1):(1,0),(2,2):(0,1)}
else:
    raise SystemExit("no gadget for these parameters")
pts = list(itertools.product(range(r), repeat=s))
assert all(any(x[d] == f[y][d] or y[d] == g[x][d] for d in range(s)) for x in pts for y in pts)
# palette family: greedy t-subsets with pairwise |P\Q| >= s
fam = []
for P in itertools.combinations(range(K), t):
    if all(len(set(P) - set(Q)) >= s for Q in fam): fam.append(P)
print(f"K={K} t={t} s={s}: {len(fam)} palettes {fam}", flush=True)
verts = [(P, v) for P in fam for v in V]
n = len(verts); idx = {w: i for i, w in enumerate(verts)}
# inside block P: base colour index c' in [K'] maps to the c'-th colour outside P
outside = {P: [c for c in range(K) if c not in P] for P in fam}
def label(P, v, c):  # proper r-labelling of class c inside block P (labels = coordinates), r if c in P
    return r if c in P else v[outside[P].index(c)]
col = bytearray(n * n)
for i, (P, u) in enumerate(verts):
    for jj in range(i + 1, n):
        Q, v = verts[jj]
        if P == Q:
            c = outside[P][basecol(u, v)]
        else:
            A = sorted(set(Q) - set(P))[:s]; B = sorted(set(P) - set(Q))[:s]
            x = tuple(label(P, u, a) for a in A); y = tuple(label(Q, v, b) for b in B)
            c = None
            for d in range(s):
                if x[d] == f[y][d]: c = A[d]; break
            if c is None:
                for d in range(s):
                    if y[d] == g[x][d]: c = B[d]; break
            assert c is not None
        col[i * n + jj] = col[jj * n + i] = c
lab = bytearray(n * K)
for i, (P, v) in enumerate(verts):
    for c in range(K): lab[i * K + c] = label(P, v, c)
with open(out, "wb") as fo:
    fo.write(struct.pack("<ii", n, K)); fo.write(col); fo.write(lab)
print(f"wrote {out}: n={n} vertices, K={K} colours, labels in 0..{r}", flush=True)
