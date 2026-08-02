#!/usr/bin/env python3
"""Verify every graph fact that appears on the erdos-gyarfas page.

Sources checked against each other:
  - graph6 files committed by the cloud session (census, candidate, records)
  - the V/E/TRI/C16 arrays embedded in the session's note_artifact.html
Checks: regularity, connectivity, C4/C8 absence, exact C16 counts,
planarity, isomorphisms, triangle structure, and that the highlighted
C16 edge set really is a single 16-cycle of the drawn graph.

Run from this conjecture directory (reads data/*.g6). Committed output:
logs/verify_page_data_2026-07-31.log
"""
import sys
import networkx as nx

def g6_read(path):
    out = []
    for line in open(path):
        line = line.strip()
        if not line:
            continue
        data = [ord(c) - 63 for c in line]
        n = data[0]
        assert 0 <= n <= 62, "only short-form g6 handled"
        bits = []
        for v in data[1:]:
            for k in range(5, -1, -1):
                bits.append((v >> k) & 1)
        g = nx.Graph()
        g.add_nodes_from(range(n))
        idx = 0
        for j in range(1, n):
            for i in range(j):
                if bits[idx]:
                    g.add_edge(i, j)
                idx += 1
        out.append(g)
    return out

def count_cycles_exact(g, L):
    """Count cycles of length exactly L (each once). DFS with canonical
    start = min vertex on cycle; direction canonicalized by halving."""
    adj = {v: sorted(g.neighbors(v)) for v in g.nodes()}
    total = 0
    n = g.number_of_nodes()
    for s in range(n):
        # paths s -> ... -> s of length L using only vertices > s in between
        def dfs(u, depth, visited):
            nonlocal total
            if depth == L - 1:
                if g.has_edge(u, s):
                    total += 1
                return
            for w in adj[u]:
                if w <= s or w in visited:
                    continue
                visited.add(w)
                dfs(w, depth + 1, visited)
                visited.remove(w)
        dfs(s, 0, set())
    assert total % 2 == 0
    return total // 2

def spectrum_flags(g, lengths=(4, 8, 16)):
    return {L: count_cycles_exact(g, L) for L in lengths}

# ---- the arrays from note_artifact.html (the drawing) ----
E_draw = [[0,2],[0,9],[0,11],[1,7],[1,10],[1,19],[2,7],[2,14],[3,14],[3,15],[3,23],[4,5],[4,18],[4,21],[5,12],[5,21],[6,8],[6,12],[6,23],[7,10],[8,12],[8,19],[9,10],[9,11],[11,16],[13,17],[13,22],[13,23],[14,15],[15,22],[16,18],[16,20],[17,20],[17,22],[18,20],[19,21]]
TRI_draw = [[0,9],[0,11],[1,7],[1,10],[3,14],[3,15],[4,5],[4,21],[5,21],[6,8],[6,12],[7,10],[8,12],[9,11],[13,17],[13,22],[14,15],[16,18],[16,20],[17,22],[18,20]]
C16_draw = [[0,2],[0,9],[1,7],[1,19],[2,7],[4,18],[4,21],[5,12],[5,21],[6,8],[6,12],[8,19],[9,11],[11,16],[16,20],[18,20]]

gd = nx.Graph(); gd.add_edges_from(E_draw)
print("== drawn graph (from note_artifact.html arrays) ==")
print("n =", gd.number_of_nodes(), "m =", gd.number_of_edges())
degs = set(dict(gd.degree()).values())
print("degrees:", degs, "connected:", nx.is_connected(gd))
assert degs == {3} and gd.number_of_nodes() == 24 and nx.is_connected(gd)

sf = spectrum_flags(gd)
print("cycle counts C4/C8/C16:", sf)
assert sf[4] == 0 and sf[8] == 0, "drawn graph must be {4,8}-free"

# triangles of drawn graph
tris = [c for c in nx.enumerate_all_cliques(gd) if len(c) == 3]
tri_edges = set()
for a, b, c in tris:
    tri_edges |= {frozenset((a, b)), frozenset((b, c)), frozenset((a, c))}
print("triangles:", len(tris), "edges on triangles:", len(tri_edges))
assert tri_edges == {frozenset(e) for e in TRI_draw}, "TRI array mismatch"

# is C16_draw a single 16-cycle?
gc = nx.Graph(); gc.add_edges_from(C16_draw)
assert all(d == 2 for _, d in gc.degree()), "C16 edges: not all degree 2"
assert nx.is_connected(gc) and gc.number_of_nodes() == 16 and gc.number_of_edges() == 16
assert all(gd.has_edge(*e) for e in C16_draw), "C16 edge not in graph"
cyc_order = nx.cycle_basis(gc)[0]
print("C16 highlight is a single 16-cycle; order:", cyc_order)

print("planar:", nx.check_planarity(gd)[0])

# ---- census ----
print("\n== n=24 census file ==")
census = g6_read("data/c48free_cubic_n24.g6")
c16s = []
planars = []
for i, g in enumerate(census):
    assert set(dict(g.degree()).values()) == {3} and nx.is_connected(g)
    f = spectrum_flags(g)
    assert f[4] == 0 and f[8] == 0
    girth = min(len(c) for c in nx.minimum_cycle_basis(g))
    pl = nx.check_planarity(g)[0]
    ntri = sum(1 for c in nx.enumerate_all_cliques(g) if len(c) == 3)
    c16s.append(f[16]); planars.append(pl)
    print(f"graph {i}: girth={girth} triangles={ntri} C16={f[16]} planar={pl}")
print("C16 multiset:", sorted(c16s), " min:", min(c16s))
assert sorted(c16s) == sorted([330, 315, 207, 228])
assert sum(planars) == 1, "exactly one planar census graph"
planar_census = census[planars.index(True)]

print("\ndrawn graph iso to planar census graph:",
      nx.is_isomorphic(gd, planar_census))
assert nx.is_isomorphic(gd, planar_census)

cand = g6_read("data/markstrom_candidate_n24.g6")[0]
print("annealer candidate iso to planar census graph:",
      nx.is_isomorphic(cand, planar_census))
assert nx.is_isomorphic(cand, planar_census)

# ---- records ----
for path, n_exp, c16_exp in [("data/record_c48free_n56_c16_56.g6", 56, 56),
                             ("data/record_c48free_n58_c16_37.g6", 58, 37)]:
    print(f"\n== {path} ==")
    g = g6_read(path)[0]
    assert g.number_of_nodes() == n_exp
    assert set(dict(g.degree()).values()) == {3} and nx.is_connected(g)
    f = spectrum_flags(g)
    print("n =", n_exp, "cycle counts C4/C8/C16:", f)
    assert f[4] == 0 and f[8] == 0 and f[16] == c16_exp
    girth = min(len(c) for c in nx.minimum_cycle_basis(g))
    ntri = sum(1 for c in nx.enumerate_all_cliques(g) if len(c) == 3)
    print("girth:", girth, "triangles:", ntri)

print("\nALL CHECKS PASSED")
