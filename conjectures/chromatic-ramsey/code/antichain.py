#!/usr/bin/env python3
"""The antichain construction for F(3,K):
vertices = pairs (P, u) with P a t-subset of [K] and u in {+1,-1}^{[K]\P};
inside a block: colour = least coordinate c not in P with u_c != u'_c;
between blocks P != Q: a = min(Q\P), b = min(P\Q); colour a if u_a == v_b else b.
Emits the colouring as a dense matrix for the C verifier (verify_colouring.c) and checks
the 3-labelling lambda_c(P,u) = u_c if c not in P else 0 is proper.
usage: antichain.py K t out.bin"""
import sys, itertools, struct

K, t = int(sys.argv[1]), int(sys.argv[2]); out = sys.argv[3]
blocks = list(itertools.combinations(range(K), t))
verts = []
for P in blocks:
    free = [c for c in range(K) if c not in P]
    for signs in itertools.product((1, -1), repeat=len(free)):
        verts.append((P, dict(zip(free, signs))))
n = len(verts)
print(f"K={K} t={t}: {len(blocks)} blocks, n={n} vertices", flush=True)
col = bytearray(n * n)
for i in range(n):
    P, u = verts[i]
    for jj in range(i + 1, n):
        Q, v = verts[jj]
        if P == Q:
            c = next(cc for cc in range(K) if cc not in P and u[cc] != v[cc])
        else:
            a = min(set(Q) - set(P)); b = min(set(P) - set(Q))
            c = a if u[a] == v[b] else b
        col[i * n + jj] = col[jj * n + i] = c
# proper 3-labelling check (pure python, cheap): label_c(w) = u_c if c not in P else 0 -> encode 0,1,2
lab = bytearray(n * K)
for i, (P, u) in enumerate(verts):
    for c in range(K):
        lab[i * K + c] = 0 if c in P else (1 if u[c] == 1 else 2)
with open(out, "wb") as f:
    f.write(struct.pack("<ii", n, K)); f.write(col); f.write(lab)
print("wrote", out)
