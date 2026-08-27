#!/usr/bin/env python3
"""E*(N, s): maximum edges of a graph on N vertices with no K_s and no
independent set of size s (a Ramsey(s,s)-type graph), computed by SAT.

Motivation (NOTE.md §5): in a balanced r-colouring of K_N with N = r²+1 and
s = r+1, every colour class G_c has clique <= r and independence <= r
(a monochromatic K_{r+1} or an uncovered (r+1)-set both violate
balancedness), so its complement H_c is an (s,s)-Ramsey graph as well and
|H_c| <= E*(N, s). Summing |G_c| = C(N,2) over colours:

    C(N,2) >= r * (C(N,2) - E*(N, s))

so a balanced colouring can only exist if E*(N, s) >= (r-1)/r * C(N,2).
Threshold values: r=3: E*(10,4) >= 30; r=4: E*(17,5) >= 102;
r=5: E*(26,6) >= 260. If the computed E* is below threshold, that case of
Erdős #617 is PROVED by counting.

Encoding: edge variables x_e; for every s-subset S: >= 1 edge inside
(no I_s) and >= 1 non-edge inside (no K_s); "at least m edges" by totalizer.
Decide feasibility at a given m ("exists such a graph with >= m edges");
binary-search externally. Witness graphs are re-verified from the
definition (independent code path).

Usage:
  python3 ramsey_max.py N s m            decide >= m (SAT/UNSAT + witness)
  python3 ramsey_max.py N s m --dimacs F emit CNF only (for breakid+kissat)
  python3 ramsey_max.py verify N s FILE  re-check witness from definition
"""
import itertools, sys, time
from pysat.formula import CNF, IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

def build(N, s, m):
    edges = list(itertools.combinations(range(N), 2))
    eidx = {e: i + 1 for i, e in enumerate(edges)}  # var = edge index + 1
    E = len(edges)
    cnf = CNF()
    for S in itertools.combinations(range(N), s):
        inner = [eidx[e] for e in itertools.combinations(S, 2)]
        cnf.append(inner)                    # no independent s-set
        cnf.append([-v for v in inner])      # no s-clique
    pool = IDPool(start_from=E + 1)
    card = CardEnc.atmost([-v for v in range(1, E + 1)], bound=E - m,
                          encoding=EncType.totalizer, vpool=pool)
    cnf.extend(card.clauses)
    return cnf, edges, eidx

def verify(N, s, adj, m=None):
    """Definition-level check, independent of the encoding."""
    ecount = sum(adj[u][v] for u in range(N) for v in range(u + 1, N))
    for S in itertools.combinations(range(N), s):
        pairs = [(u, v) for u, v in itertools.combinations(S, 2)]
        ne = sum(adj[u][v] for u, v in pairs)
        assert ne >= 1, ("independent set", S)
        assert ne < len(pairs), ("clique", S)
    if m is not None:
        assert ecount >= m, (ecount, m)
    return ecount

def main():
    if sys.argv[1] == "verify":
        N, s = int(sys.argv[2]), int(sys.argv[3])
        adj = [[0] * N for _ in range(N)]
        with open(sys.argv[4]) as f:
            for line in f:
                if line.startswith("#"):
                    continue
                u, v = map(int, line.split())
                adj[u][v] = adj[v][u] = 1
        e = verify(N, s, adj)
        print(f"witness OK: {e} edges, no K_{s}, no I_{s} on {N} vertices")
        return

    N, s, m = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    cnf, edges, eidx = build(N, s, m)
    if "--dimacs" in sys.argv:
        f = sys.argv[sys.argv.index("--dimacs") + 1]
        cnf.to_file(f)
        print(f"wrote {f}: {cnf.nv} vars, {len(cnf.clauses)} clauses")
        return
    t0 = time.time()
    with Cadical195(bootstrap_with=cnf) as sv:
        res = sv.solve()
        model = sv.get_model() if res else None
    dt = time.time() - t0
    if res:
        pos = {v for v in model if v > 0}
        adj = [[0] * N for _ in range(N)]
        for e, v in eidx.items():
            if v in pos:
                adj[e[0]][e[1]] = adj[e[1]][e[0]] = 1
        ecount = verify(N, s, adj, m)
        out = f"data/ramsey_{N}_{s}_ge{m}.txt"
        with open(out, "w") as f:
            f.write(f"# graph on {N} vertices, no K_{s}, no I_{s}, "
                    f"{ecount} edges (>= {m}); definition-verified\n")
            for (u, v), var in eidx.items():
                if var in pos:
                    f.write(f"{u} {v}\n")
        print(f"SAT in {dt:.1f}s: E*({N},{s}) >= {ecount}; witness verified -> {out}")
    else:
        print(f"UNSAT in {dt:.1f}s: E*({N},{s}) < {m}")

if __name__ == "__main__":
    main()
