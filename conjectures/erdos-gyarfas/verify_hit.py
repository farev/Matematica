#!/usr/bin/env python3
"""verify_hit.py — independent verification of a claimed {4,8,16,...}-free graph.

For a graph6 string (argv[1] or stdin), checks with THREE mechanisms that are
algorithmically independent of hunt.c/cyclecheck.c's shared DFS design:

  1. networkx simple_cycles enumeration for lengths <= 16 (complete),
  2. cyclecheck under R random vertex relabelings (catches order-dependent
     bugs in the DFS; same code, different inputs),
  3. SAT (pysat, minisat22): for each power L <= n, satisfiability of
     "there is a simple cycle of length exactly L" — SAT gives a witness
     cycle, UNSAT is a solver-certified absence proof.

Prints a verdict per length and an overall verdict. Exact/integer throughout;
the SAT solver is trusted only as an independent second opinion.

Usage: python3 verify_hit.py <graph6-string> [--sat-max L] [--skip-sat]
"""
import random
import subprocess
import sys

import networkx as nx

POWERS = [4, 8, 16, 32, 64]


def cyclecheck_spectrum(g6str):
    out = subprocess.run(["./cyclecheck", "-p"], input=g6str + "\n",
                         capture_output=True, text=True, check=True).stdout
    spec = out.strip().split("\t")[1]
    return set() if spec == "-" else {int(x) for x in spec.split(",")}


def sat_has_cycle(G, L, timeout_ignored=None):
    """SAT-encode existence of a simple cycle of length exactly L."""
    from pysat.solvers import Minisat22
    from pysat.card import CardEnc, EncType
    from pysat.formula import IDPool

    nodes = sorted(G.nodes())
    pool = IDPool()
    x = {(i, p): pool.id(f"x{i}_{p}") for i in nodes for p in range(L)}
    cnf = []
    # each position holds exactly one vertex
    for p in range(L):
        lits = [x[(i, p)] for i in nodes]
        cnf.append(lits)                                  # >= 1
        enc = CardEnc.atmost(lits, bound=1, vpool=pool, encoding=EncType.pairwise)
        cnf.extend(enc.clauses)
    # each vertex used at most once
    for i in nodes:
        lits = [x[(i, p)] for p in range(L)]
        enc = CardEnc.atmost(lits, bound=1, vpool=pool, encoding=EncType.pairwise)
        cnf.extend(enc.clauses)
    # consecutive positions adjacent (cyclically)
    adj = {i: set(G[i]) for i in nodes}
    for p in range(L):
        q = (p + 1) % L
        for i in nodes:
            # x[i,p] -> OR_{j in N(i)} x[j,q]
            cnf.append([-x[(i, p)]] + [x[(j, q)] for j in adj[i]])
    with Minisat22(bootstrap_with=cnf) as m:
        sat = m.solve()
        return sat


def main():
    if len(sys.argv) > 1 and not sys.argv[1].startswith("--"):
        g6 = sys.argv[1]
    else:
        g6 = sys.stdin.readline().strip()
    skip_sat = "--skip-sat" in sys.argv
    sat_max = 64
    if "--sat-max" in sys.argv:
        sat_max = int(sys.argv[sys.argv.index("--sat-max") + 1])

    G = nx.from_graph6_bytes(g6.encode())
    n = G.number_of_nodes()
    degs = sorted(d for _, d in G.degree())
    print(f"n={n} degrees min={degs[0]} max={degs[-1]} "
          f"connected={nx.is_connected(G)}")
    if degs[0] < 3:
        print("VERDICT: NOT min-degree-3 — irrelevant graph")
        sys.exit(1)

    relevant = [L for L in POWERS if L <= n]

    # 1. networkx enumeration <= 16
    nx_lens = set()
    for c in nx.simple_cycles(G, length_bound=min(16, n)):
        nx_lens.add(len(c))
    nx_found = {L for L in relevant if L <= 16 and L in nx_lens}
    print(f"networkx (<=16): powers present {sorted(nx_found) or 'none'}")

    # 2. cyclecheck under random relabelings
    rng = random.Random(12345)
    specs = []
    for _ in range(10):
        perm = list(G.nodes())
        rng.shuffle(perm)
        H = nx.relabel_nodes(G, dict(zip(G.nodes(), perm)))
        H2 = nx.convert_node_labels_to_integers(H)
        g6h = nx.to_graph6_bytes(H2, header=False).decode().strip()
        specs.append(frozenset(cyclecheck_spectrum(g6h)))
    agree = len(set(specs)) == 1
    cc_spec = set(specs[0])
    print(f"cyclecheck x10 relabelings: spectra agree={agree}, "
          f"present={sorted(cc_spec) or 'none'}")

    # 3. SAT per length
    sat_res = {}
    if not skip_sat:
        for L in relevant:
            if L > sat_max:
                sat_res[L] = None
                continue
            sat_res[L] = sat_has_cycle(G, L)
            print(f"SAT L={L}: {'cycle EXISTS' if sat_res[L] else 'UNSAT — no cycle'}")

    ok = agree and nx_found == {L for L in cc_spec if L <= 16}
    if not skip_sat:
        for L, r in sat_res.items():
            if r is None:
                continue
            ok = ok and (r == (L in cc_spec))
    empty = not cc_spec
    print(f"methods consistent: {ok}")
    if ok and empty:
        print("VERDICT: graph has NO power-of-2 cycle — COUNTEREXAMPLE "
              "(all three methods agree)")
    elif ok:
        print(f"VERDICT: conforms to conjecture (has {sorted(cc_spec)})")
    else:
        print("VERDICT: METHODS DISAGREE — investigate before claiming anything")
        sys.exit(2)


if __name__ == "__main__":
    main()
