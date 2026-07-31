#!/usr/bin/env python3
"""crosscheck.py — independent validation of cyclecheck against networkx.

For a batch of graphs (random + named), compute the set of cycle lengths in
{4,8,16,32,64} present, using networkx.simple_cycles(length_bound=...), and
compare with cyclecheck -p output.  Exits nonzero on any mismatch.

Usage: python3 crosscheck.py [seed] [ngraphs]
"""
import random
import subprocess
import sys

import networkx as nx

POWERS = [4, 8, 16, 32, 64]


def spectrum_nx(G, maxlen):
    """Cycle lengths in POWERS (<= maxlen) present in G, by simple_cycles.

    maxlen is clipped to the largest power of 2 that is <= n, since larger
    cycles are irrelevant to the comparison.
    """
    n = G.number_of_nodes()
    bound = max((L for L in POWERS if L <= min(maxlen, n)), default=0)
    if bound == 0:
        return []
    lens = set()
    for c in nx.simple_cycles(G, length_bound=bound):
        lens.add(len(c))
    return sorted(L for L in POWERS if L in lens)


def spectrum_cc(graphs_g6):
    inp = "\n".join(graphs_g6) + "\n"
    out = subprocess.run(["./cyclecheck", "-p"], input=inp, capture_output=True,
                         text=True, check=True).stdout
    res = []
    for line in out.strip().split("\n"):
        g6, spec = line.split("\t")
        res.append([] if spec == "-" else [int(x) for x in spec.split(",")])
    return res


def g6(G):
    return nx.to_graph6_bytes(G, header=False).decode().strip()


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 20260730
    ngraphs = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    rng = random.Random(seed)

    tests = []  # (name, graph, maxlen for nx enumeration)

    tests.append(("petersen", nx.petersen_graph(), 10))
    tests.append(("heawood", nx.heawood_graph(), 14))
    tests.append(("K4", nx.complete_graph(4), 4))
    tests.append(("K5", nx.complete_graph(5), 5))
    tests.append(("C16", nx.cycle_graph(16), 16))
    tests.append(("C17", nx.cycle_graph(17), 17))
    tests.append(("K33", nx.complete_bipartite_graph(3, 3), 6))
    tests.append(("pappus", nx.LCF_graph(18, [5, 7, -7, 7, -7, -5], 3), 18))
    tests.append(("desargues", nx.desargues_graph(), 20))
    tests.append(("dodecahedral", nx.dodecahedral_graph(), 20))
    tests.append(("mcgee", nx.LCF_graph(24, [12, 7, -7], 8), 24))

    for i in range(ngraphs):
        # mix of random cubic (sparse, up to 22 vertices) and random gnp
        # (dense, kept small so full cycle enumeration stays cheap)
        if i % 2 == 0:
            n = rng.randrange(6, 23)
            if n % 2:
                n += 1
            G = nx.random_regular_graph(3, n, seed=rng.randrange(1 << 30))
        else:
            n = rng.randrange(6, 13)
            G = nx.gnp_random_graph(n, rng.uniform(0.15, 0.5),
                                    seed=rng.randrange(1 << 30))
        tests.append((f"rand{i}(n={G.number_of_nodes()})", G,
                      G.number_of_nodes()))

    names = [t[0] for t in tests]
    g6s = [g6(t[1]) for t in tests]
    got = spectrum_cc(g6s)
    bad = 0
    for (name, G, maxlen), spec_cc in zip(tests, got):
        spec_nx = spectrum_nx(G, maxlen)
        # cyclecheck only reports lengths <= n
        spec_nx = [L for L in spec_nx if L <= G.number_of_nodes()]
        mark = "ok" if spec_nx == spec_cc else "MISMATCH"
        if spec_nx != spec_cc:
            bad += 1
        print(f"{name:24s} nx={spec_nx} cc={spec_cc} {mark}")
    if bad:
        print(f"{bad} mismatches", file=sys.stderr)
        sys.exit(1)
    print(f"all {len(tests)} graphs agree")


if __name__ == "__main__":
    main()
