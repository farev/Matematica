#!/usr/bin/env python3
"""Search for the first configuration not covered by NOTE Theorem 3: n = 35 (m = 5), h = 3,
three pairwise disjoint hexagonal links with the periodic colouring 2,3,4,2,3,4 covering all
18 vertices of W, all 20 faces of G = T - V1 rainbow triangles or the three hexagons,
6 empty triangles partitioning W (every vertex on an empty face), 14 stellated (D) triangles.
Model: choose 20 of the 216 rainbow triples on the 18 vertices so that every hexagon edge lies in
exactly one chosen triple and every other bichromatic pair lies in 0 or 2; plus a packing of 6
chosen triples covering every vertex once.  Post-checks: vertex links are single paths (so the
complex is a surface with the three hexagons as boundary), connected (then it is the pair of
pants, hence planar).  For each solution build T (35 vertices) and compute disc(T) exactly.
"""
import sys, itertools
from pysat.formula import CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical153

# vertices: (hex, i), colour i % 3
V = [(hx, i) for hx in range(3) for i in range(6)]
vid = {v: k for k, v in enumerate(V)}
col = {v: v[1] % 3 for v in V}
hexedges = set()
for hx in range(3):
    for i in range(6):
        a, b = (hx, i), (hx, (i + 1) % 6)
        hexedges.add(frozenset((vid[a], vid[b])))
byc = [[vid[v] for v in V if col[v] == c] for c in range(3)]
triples = [(x, y, z) for x in byc[0] for y in byc[1] for z in byc[2]]
T = len(triples)
tv = {tr: k + 1 for k, tr in enumerate(triples)}       # triangle vars 1..216
pv = {tr: T + k + 1 for k, tr in enumerate(triples)}   # packing vars 217..432
top = 2 * T
cnf = CNF()
def pairs_of(tr): return [frozenset((tr[0], tr[1])), frozenset((tr[1], tr[2])), frozenset((tr[0], tr[2]))]
pair_tris = {}
for tr in triples:
    for e in pairs_of(tr): pair_tris.setdefault(e, []).append(tv[tr])
for e, lits in pair_tris.items():
    if e in hexedges:
        enc = CardEnc.equals(lits=lits, bound=1, top_id=top, encoding=EncType.seqcounter); top = enc.nv; cnf.extend(enc.clauses)
    else:
        enc = CardEnc.atmost(lits=lits, bound=2, top_id=top, encoding=EncType.seqcounter); top = enc.nv; cnf.extend(enc.clauses)
        # not exactly one: each chosen triangle on the pair forces another one
        for l in lits: cnf.append([-l] + [o for o in lits if o != l])
enc = CardEnc.equals(lits=[tv[tr] for tr in triples], bound=20, top_id=top, encoding=EncType.seqcounter); top = enc.nv; cnf.extend(enc.clauses)
# packing
for tr in triples: cnf.append([-pv[tr], tv[tr]])
for v in range(18):
    lits = [pv[tr] for tr in triples if v in tr]
    enc = CardEnc.equals(lits=lits, bound=1, top_id=top, encoding=EncType.seqcounter); top = enc.nv; cnf.extend(enc.clauses)

def links_ok(chosen):
    # each vertex: the chosen triangles containing it form a single path (edges = pairs of other vertices)
    for v in range(18):
        edges = [tuple(sorted(set(tr) - {v})) for tr in chosen if v in tr]
        deg = {}
        for a, b in edges: deg[a] = deg.get(a, 0) + 1; deg[b] = deg.get(b, 0) + 1
        ends = [x for x, d in deg.items() if d == 1]
        if any(d > 2 for d in deg.values()) or len(ends) != 2: return False
        # connectivity of the link graph
        adj = {}
        for a, b in edges: adj.setdefault(a, []).append(b); adj.setdefault(b, []).append(a)
        seen = {ends[0]}; st = [ends[0]]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y not in seen: seen.add(y); st.append(y)
        if len(seen) != len(deg): return False
    return True

def connected(chosen):
    adj = {v: set() for v in range(18)}
    for tr in chosen:
        for a, b in itertools.combinations(tr, 2): adj[a].add(b); adj[b].add(a)
    seen = {0}; st = [0]
    while st:
        x = st.pop()
        for y in adj[x]:
            if y not in seen: seen.add(y); st.append(y)
    return len(seen) == 18

def disc_of_T(chosen, empty):
    """T: vertices 0..17 (W), 18..20 (H: one per hexagon), then one per stellated triangle."""
    faces = []
    for hx in range(3):
        hv = 18 + hx
        for i in range(6): faces.append((hv, vid[(hx, i)], vid[(hx, (i + 1) % 6)]))
    nxt = 21
    for tr in chosen:
        if tr in empty: faces.append(tuple(tr))
        else:
            for a, b in ((tr[0], tr[1]), (tr[1], tr[2]), (tr[0], tr[2])): faces.append((nxt, a, b))
            nxt += 1
    n = nxt
    vf = [[] for _ in range(n)]
    for k, f in enumerate(faces):
        for v in f: vf[v].append(k)
    # order: BFS from 0
    adj = [set() for _ in range(n)]
    for f in faces:
        for a, b in itertools.combinations(f, 2): adj[a].add(b); adj[b].add(a)
    order = [0]; seen = {0}; qi = 0
    while qi < len(order):
        x = order[qi]; qi += 1
        for y in sorted(adj[x]):
            if y not in seen: seen.add(y); order.append(y)
    colr = [-1] * n
    sys.setrecursionlimit(10000)
    def ok(v, c):
        for k in vf[v]:
            f = faces[k]; o = [u for u in f if u != v]
            if colr[o[0]] == c and colr[o[1]] == c: return False
        return True
    def search(idx, r, b, target):
        if r > target or b > n - target: return False
        if idx == n: return r == target
        v = order[idx]
        for c in (0, 1):
            if c == 0 and r == target: continue
            if c == 1 and b == n - target: continue
            if not ok(v, c): continue
            colr[v] = c
            if search(idx + 1, r + (c == 0), b + (c == 1), target): return True
            colr[v] = -1
        return False
    for d in range(n % 2, n + 1, 2):
        for i in range(n): colr[i] = -1
        if search(0, 0, 0, (n - d) // 2): return d, n
    return -1, n

maxsol = int(sys.argv[1]) if len(sys.argv) > 1 else 50
found = 0; tried = 0
hist = {}
with Cadical153(bootstrap_with=cnf.clauses) as s:
    while s.solve():
        model = set(l for l in s.get_model() if l > 0)
        chosen = [tr for tr in triples if tv[tr] in model]
        empty = set(tr for tr in triples if pv[tr] in model)
        tried += 1
        if links_ok(chosen) and connected(chosen):
            found += 1
            d, n = disc_of_T(chosen, empty)
            hist[d] = hist.get(d, 0) + 1
            print(f"solution {found}: n={n} disc={d}  triangles={chosen}  empty={sorted(empty)}", flush=True)
            if found >= maxsol: break
        # block this exact triangle set (and packing) to move on
        s.add_clause([-tv[tr] for tr in chosen] + [-pv[tr] for tr in empty])
print(f"SAT models examined {tried}; valid pants triangulations {found}; disc histogram {hist}")
