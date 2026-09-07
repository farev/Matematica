"""Enumerate connection sets {t, g, g^-1} of AGL(1,p), t an involution, g of
order >= 3, and compute girth of Cay(G,S) by BFS from the identity (valid for
vertex-transitive graphs; girth-14 hits are re-verified from every root).
Usage: python3 scan.py p
"""
import sys, time, csv
import numpy as np
from agl import AGL, bfs_girth_and_connected, connected, girth_all_roots

p = int(sys.argv[1])
t0 = time.time()
G = AGL(p)
n = G.n
invs = G.involutions()
assert len(invs) == p, (len(invs), p)
gens = [x for x in range(n) if x != G.e and G.inv[x] != x and x < G.inv[x]]
print(f"p={p} |G|={n} involutions={len(invs)} candidate g (mod inversion)={len(gens)} pairs={len(invs)*len(gens)}")

rows = []
hist = {}
g14 = []
for t in invs:
    for g in gens:
        S = [t, g, int(G.inv[g])]
        adj = G.adjacency(S)
        if not connected(adj, G.e):
            gir = 0  # disconnected: S does not generate
        else:
            gir, _ = bfs_girth_and_connected(adj, G.e)
        hist[gir] = hist.get(gir, 0) + 1
        rows.append((t, g, gir))
        if gir == 14:
            g14.append((t, g))
print("girth histogram (0 = not generating):", dict(sorted(hist.items())))
print(f"girth-14 pairs: {len(g14)}   scan time {time.time()-t0:.1f}s")

# full-root verification of girth for the girth-14 hits (no transitivity assumption)

# conjugacy classes of the pairs (t, {g, g^-1}) under conjugation by G
def conj(h, x):
    return int(G.mul[G.mul[h, x], G.inv[h]])

classes = {}
for (t, g) in g14:
    best = None
    for h in range(n):
        tt = conj(h, t)
        gg = conj(h, g)
        gi = int(G.inv[gg])
        key = (tt, min(gg, gi))
        if best is None or key < best:
            best = key
    classes.setdefault(best, []).append((t, g))
print(f"conjugacy classes among girth-14 pairs: {len(classes)}")
# all-root girth re-check for one representative per class (no transitivity assumption)
for key in sorted(classes):
    adj = G.adjacency([key[0], key[1], int(G.inv[key[1]])])
    print(f"  all-root girth of class rep {G.pair(key[0])},{G.pair(key[1])}: {girth_all_roots(adj)}")
with open(f"girth14_p{p}.csv", "w") as f:
    w = csv.writer(f)
    w.writerow(["class_rep_t_a", "class_rep_t_b", "class_rep_g_a", "class_rep_g_b", "class_size",
                "rep_g_order"])
    for key, members in sorted(classes.items()):
        ta, tb = G.pair(key[0])
        ga, gb = G.pair(key[1])
        w.writerow([ta, tb, ga, gb, len(members), G.order(key[1])])
        print(f"  class rep t=({ta},{tb}) g=({ga},{gb}) ord(g)={G.order(key[1])} size={len(members)}")
with open(f"scan_p{p}_all.csv", "w") as f:
    w = csv.writer(f)
    w.writerow(["t_a", "t_b", "g_a", "g_b", "girth"])
    for (t, g, gir) in rows:
        w.writerow([*G.pair(t), *G.pair(g), gir])
print(f"total {time.time()-t0:.1f}s")
