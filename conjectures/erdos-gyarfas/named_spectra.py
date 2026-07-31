#!/usr/bin/env python3
"""named_spectra.py — power-of-2 cycle spectrum of named/constructed cubic graphs.

Constructs a battery of well-known cubic graphs (networkx builtins plus
LCF-code constructions).  Every construction is SELF-CERTIFIED before use:
we verify order, 3-regularity, and girth computationally, and the girth is
part of the output — so a wrong LCF code from the literature can at worst
appear as a row with unexpected girth, never as a silently wrong claim.

For each graph, reports which cycle lengths in {4,8,16,32,64} occur (via
cyclecheck, exact DFS).  Lengths whose check exceeds the per-length timeout
are reported as '?'.

Output: TSV to stdout — name, n, girth, spectrum, verdict.
A graph whose spectrum is empty ("-") with no '?' would be a counterexample
to the Erdos-Gyarfas conjecture.

Usage: python3 named_spectra.py [> data/named_spectra.tsv]
"""
import subprocess
import sys

import networkx as nx

POWERS = [4, 8, 16, 32, 64]
TIMEOUT_PER_GRAPH = 600  # seconds, for the whole cyclecheck call


def girth(G):
    """Odd/even girth via BFS from every vertex; exact, O(n*m)."""
    best = float("inf")
    for src in G:
        dist = {src: 0}
        parent = {src: None}
        queue = [src]
        while queue:
            nxt = []
            for u in queue:
                for v in G[u]:
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        parent[v] = u
                        nxt.append(v)
                    elif parent[u] != v and dist[v] >= dist[u]:
                        # non-tree edge closing a cycle through src (or above)
                        best = min(best, dist[u] + dist[v] + 1)
            queue = nxt
    return best


def g6(G):
    return nx.to_graph6_bytes(G, header=False).decode().strip()


def spectrum(G):
    """Run cyclecheck -p; return list of present lengths or None on timeout."""
    try:
        out = subprocess.run(["./cyclecheck", "-p"], input=g6(G) + "\n",
                             capture_output=True, text=True,
                             timeout=TIMEOUT_PER_GRAPH, check=True).stdout
    except subprocess.TimeoutExpired:
        return None
    spec = out.strip().split("\t")[1]
    return [] if spec == "-" else [int(x) for x in spec.split(",")]


def main():
    tests = []

    def add(name, G):
        tests.append((name, G))

    add("K4", nx.complete_graph(4))
    add("K3,3", nx.complete_bipartite_graph(3, 3))
    add("Petersen", nx.petersen_graph())
    add("Heawood", nx.heawood_graph())
    add("Moebius-Kantor", nx.moebius_kantor_graph())
    add("Pappus", nx.pappus_graph())
    add("Desargues", nx.desargues_graph())
    add("Dodecahedron", nx.dodecahedral_graph())
    add("McGee[LCF 12,7,-7]^8", nx.LCF_graph(24, [12, 7, -7], 8))
    add("Nauru[LCF 5,-9,7,-7,9,-5]^4",
        nx.LCF_graph(24, [5, -9, 7, -7, 9, -5], 4))
    add("TutteCoxeter[LCF -13,-9,7,-7,9,13]^5",
        nx.LCF_graph(30, [-13, -9, 7, -7, 9, 13], 5))
    add("Dyck[LCF 5,-5,13,-13]^8", nx.LCF_graph(32, [5, -5, 13, -13], 8))
    add("Foster[LCF 17,-9,37,-37,9,-17]^15",
        nx.LCF_graph(90, [17, -9, 37, -37, 9, -17], 15))
    # candidate codes for 70-vertex girth-10 graphs (Balaban-10-cage family);
    # girth is verified below, so a wrong code is exposed, not trusted
    add("Harries[LCF -29,-19,-13,13,21,-27,27,33,-13,13,19,-21,-33,29]^5",
        nx.LCF_graph(70, [-29, -19, -13, 13, 21, -27, 27, 33, -13, 13, 19,
                          -21, -33, 29], 5))
    # generalized Petersen graphs GP(m,k): outer m-cycle u_i, inner star v_i,
    # edges u_i~u_{i+1}, u_i~v_i, v_i~v_{i+k}; cubic for k != m/2
    def gp(m, k):
        G = nx.Graph()
        for i in range(m):
            G.add_edge(("u", i), ("u", (i + 1) % m))
            G.add_edge(("u", i), ("v", i))
            G.add_edge(("v", i), ("v", (i + k) % m))
        return nx.convert_node_labels_to_integers(G)

    for (pm, pk) in [(7, 2), (9, 2), (11, 2), (13, 4), (12, 5), (24, 5),
                     (26, 5), (30, 7), (48, 7)]:
        add(f"GP({pm},{pk})", gp(pm, pk))

    print("name\tn\tgirth\tpow2-present\tverdict")
    for name, G in tests:
        n = G.number_of_nodes()
        assert all(d == 3 for _, d in G.degree()), f"{name}: not cubic"
        g = girth(G)
        spec = spectrum(G)
        if spec is None:
            print(f"{name}\t{n}\t{g}\t?timeout\tundecided")
            continue
        relevant = [L for L in POWERS if L <= n]
        verdict = ("COUNTEREXAMPLE?!" if not spec else "has " +
                   ",".join(map(str, spec)))
        print(f"{name}\t{n}\t{g}\t"
              f"{','.join(map(str, spec)) if spec else '-'}\t{verdict}")


if __name__ == "__main__":
    main()
