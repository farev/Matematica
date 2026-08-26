#!/usr/bin/env python3
"""Independent decision of strong 6-edge-colorability (Engine B).

No code shared with strong6.c.  Builds T(H) from a multig -T line (or a
graph from graph6), derives the strong-edge-coloring constraint graph
straight from the definition (color classes must be induced matchings),
encodes proper K-coloring as CNF, and decides with a SAT solver (CaDiCaL
via python-sat).  For UNSAT verdicts it can emit a DRUP proof.

Usage:
  engine_b.py [-g6] [-k K] [--proof out.drup] < lines
Prints per line:  B <lineno> <n> <m> <SAT|UNSAT> [witness]
"""
import sys
from pysat.solvers import Cadical195, Glucose3


def parse_T(raw):
    t = raw.split()
    nv, ne = int(t[0]), int(t[1])
    vals = [int(x) for x in t[2:]]
    inst = []
    for i in range(ne):
        a, b, m = vals[3 * i], vals[3 * i + 1], vals[3 * i + 2]
        inst += [(a, b)] * m
    # truncation
    slot = [0] * nv
    edges = []
    for u in range(nv):
        edges += [(3 * u, 3 * u + 1), (3 * u, 3 * u + 2), (3 * u + 1, 3 * u + 2)]
    for (a, b) in inst:
        edges.append((3 * a + slot[a], 3 * b + slot[b]))
        slot[a] += 1
        slot[b] += 1
    assert slot == [3] * nv
    return 3 * nv, edges


def parse_g6(raw):
    s = raw.strip()
    n = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        v = ord(ch) - 63
        bits += [(v >> b) & 1 for b in range(5, -1, -1)]
    edges = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                edges.append((i, j))
            k += 1
    return n, edges


def strong_conflicts(n, edges):
    nb = [set() for _ in range(n)]
    for a, b in edges:
        nb[a].add(b)
        nb[b].add(a)
    m = len(edges)
    pairs = []
    for i in range(m):
        a, b = edges[i]
        close = {a, b} | nb[a] | nb[b]
        for j in range(i + 1, m):
            c, d = edges[j]
            if c in close or d in close:
                pairs.append((i, j))
    return pairs


def decide(n, edges, K, proof=None):
    m = len(edges)
    conflicts = strong_conflicts(n, edges)

    def var(e, c):
        return e * K + c + 1

    cnf = []
    for e in range(m):
        cnf.append([var(e, c) for c in range(K)])
    for (i, j) in conflicts:
        for c in range(K):
            cnf.append([-var(i, c), -var(j, c)])
    if proof:
        solver = Glucose3(bootstrap_with=cnf, with_proof=True)
    else:
        solver = Cadical195(bootstrap_with=cnf)
    sat = solver.solve()
    result = None
    if sat:
        model = set(l for l in solver.get_model() if l > 0)
        result = []
        for e in range(m):
            cs = [c for c in range(K) if var(e, c) in model]
            assert cs, "uncolored edge"
            result.append(cs[0])
        # re-check from definition
        nb = [set() for _ in range(n)]
        for a, b in edges:
            nb[a].add(b)
            nb[b].add(a)
        for i in range(m):
            for j in range(i + 1, m):
                if result[i] != result[j]:
                    continue
                a, b = edges[i]
                c, d = edges[j]
                assert not ({a, b} & {c, d}), "shares vertex"
                assert not ((c in nb[a]) or (d in nb[a]) or (c in nb[b])
                            or (d in nb[b])), "not induced"
    pf = solver.get_proof() if (proof and not sat) else None
    solver.delete()
    return sat, result, pf


def main():
    g6 = "-g6" in sys.argv
    K = 6
    if "-k" in sys.argv:
        K = int(sys.argv[sys.argv.index("-k") + 1])
    proof_out = None
    if "--proof" in sys.argv:
        proof_out = sys.argv[sys.argv.index("--proof") + 1]
    lineno = 0
    for raw in sys.stdin:
        raw = raw.strip()
        if not raw:
            continue
        lineno += 1
        n, edges = parse_g6(raw) if g6 else parse_T(raw)
        sat, witness, pf = decide(n, edges, K, proof=proof_out)
        if sat:
            print("B %d %d %d SAT %s" % (lineno, n, len(edges),
                                         " ".join(map(str, witness))))
        else:
            print("B %d %d %d UNSAT" % (lineno, n, len(edges)))
            if pf is not None:
                with open(proof_out, "w") as fh:
                    for cl in pf:
                        fh.write(cl + "\n" if isinstance(cl, str)
                                 else " ".join(map(str, cl)) + " 0\n")
                print("proof written: %s" % proof_out, file=sys.stderr)
    sys.stdout.flush()


if __name__ == "__main__":
    main()
