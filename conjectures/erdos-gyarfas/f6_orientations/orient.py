"""Orientation analysis for Cay(AGL(1,p), {t, g, g^-1}) in Garcia's window calculus.
Usage: python3 orient.py p ta tb ga gb [--cnf-only]
Steps: build graph, enumerate 14/15/16-cycles (C enumerator), per-edge counts,
Lemma 5.2 check, group-invariant orientations, subgroup-invariant SAT instances,
and write the full DIMACS instance.
"""
import sys, os, time, json, subprocess, threading
import numpy as np
from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from pysat.solvers import Solver
from agl import AGL, girth_all_roots

HERE = os.path.dirname(os.path.abspath(__file__))
REQ = {14: 5, 15: 3, 16: 1}      # minimum number of OFF vertices per cycle length


def build(p, ta, tb, ga, gb):
    G = AGL(p)
    t, g = G.idx(ta, tb), G.idx(ga, gb)
    assert G.inv[t] == t and t != G.e and G.inv[g] != g and g != G.e
    S = [t, g, int(G.inv[g])]          # label 0 = t-edge, 1 = g-edge (x -> x*g), 2 = g^-1-edge
    adj = G.adjacency(S)
    return G, S, adj


def write_graph(adj, fn):
    with open(fn, "w") as f:
        f.write(f"{adj.shape[0]}\n")
        for nb in adj:
            f.write("3 " + " ".join(str(int(v)) for v in nb) + "\n")


def graph6(adj):
    n = adj.shape[0]
    bits = []
    for j in range(1, n):
        row = set(int(v) for v in adj[j])
        for i in range(j):
            bits.append(1 if i in row else 0)
    while len(bits) % 6:
        bits.append(0)
    s = chr(63 + n) if n <= 62 else chr(126) + "".join(chr(63 + ((n >> sh) & 63)) for sh in (12, 6, 0))
    return s + "".join(chr(63 + int("".join(map(str, bits[i:i + 6])), 2)) for i in range(0, len(bits), 6))


def enumerate_cycles(adj, tag):
    gf = os.path.join(HERE, f"{tag}.graph")
    cf = os.path.join(HERE, f"{tag}.cycles")
    write_graph(adj, gf)
    t0 = time.time()
    res = subprocess.run([os.path.join(HERE, "cycles"), gf, "16", "14", cf], capture_output=True, text=True, check=True)
    counts = {}
    for line in res.stdout.splitlines():
        _, l, c = line.replace(":", "").split()
        counts[int(l)] = int(c)
    cycles = []
    with open(cf) as f:
        for line in f:
            parts = list(map(int, line.split()))
            assert parts[0] == len(parts) - 1
            cycles.append(parts[1:])
    return counts, cycles, time.time() - t0


def off_labels(adj, cyc):
    """For each vertex on the cycle, the label (column of adj) of its edge NOT on the cycle."""
    L = len(cyc)
    out = []
    for i, x in enumerate(cyc):
        prev, nxt = cyc[i - 1], cyc[(i + 1) % L]
        offs = [j for j in range(3) if int(adj[x][j]) not in (prev, nxt)]
        assert len(offs) == 1, (x, cyc)
        out.append((x, offs[0]))
    return out


def check_orientation(adj, cycles, choice):
    """choice[x] = label of the u-edge at x. Returns number of violated cycles
    (a(C) = #vertices whose u-edge lies on C must be <= 3L-33), computed from the
    neighbour table, independently of the literal encoding."""
    bad = 0
    worst = {}
    for cyc in cycles:
        L = len(cyc)
        on = set()
        pos = {x: i for i, x in enumerate(cyc)}
        a = 0
        for i, x in enumerate(cyc):
            y = int(adj[x][choice[x]])
            if y == cyc[i - 1] or y == cyc[(i + 1) % L]:
                a += 1
        if a > 3 * L - 33:
            bad += 1
            worst[L] = max(worst.get(L, 0), a)
    return bad, worst


def build_cnf(cyc_lits, n_orbits, orbit_of, n):
    """Variables var(o,j) = 3o+j+1 for orbit o, label j. Exactly-one per orbit,
    at-least-REQ[L] of the off-literals per cycle (repeated literals aliased)."""
    cnf = CNF()
    top = 3 * n_orbits
    for o in range(n_orbits):
        v = [3 * o + 1, 3 * o + 2, 3 * o + 3]
        cnf.append(v)
        cnf.append([-v[0], -v[1]]); cnf.append([-v[0], -v[2]]); cnf.append([-v[1], -v[2]])
    seen = set()
    ncons = 0
    for L, lits in cyc_lits:
        mapped = tuple(sorted(3 * orbit_of[x] + j + 1 for x, j in lits))
        if mapped in seen:
            continue
        seen.add(mapped)
        ncons += 1
        # alias duplicates so every literal in the cardinality constraint is distinct
        used = set()
        distinct = []
        for v in mapped:
            if v in used:
                top += 1
                cnf.append([-top, v]); cnf.append([top, -v])
                distinct.append(top)
            else:
                used.add(v); distinct.append(v)
        enc = CardEnc.atleast(lits=distinct, bound=REQ[L], top_id=top, encoding=EncType.seqcounter)
        cnf.extend(enc.clauses)
        top = max(top, enc.nv)
    cnf.nv = max(cnf.nv, top)
    return cnf, ncons


def solve_with_limit(cnf, seconds, name="cadical195", chunk=2000):
    """Wall-clock-limited solve via a conflict-budget loop (pysat's interrupt()
    from a timer thread does not preempt the solver, so control must return
    to Python between chunks)."""
    s = Solver(name=name, bootstrap_with=cnf.clauses)
    t0 = time.time()
    r = None
    while time.time() - t0 < seconds:
        s.conf_budget(chunk)
        r = s.solve_limited()
        if r is not None:
            break
        chunk = min(chunk * 2, 50000)
    dt = time.time() - t0
    model = s.get_model() if r else None
    try:
        st = s.accum_stats()
    except Exception:
        st = None
    s.delete()
    return r, model, dt, st


def model_to_choice(model, orbit_of, n):
    tv = set(v for v in model if v > 0)
    choice = []
    for x in range(n):
        o = orbit_of[x]
        js = [j for j in range(3) if 3 * o + j + 1 in tv]
        assert len(js) == 1
        choice.append(js[0])
    return choice


def main():
    p, ta, tb, ga, gb = map(int, sys.argv[1:6])
    cnf_only = "--cnf-only" in sys.argv
    tag = f"p{p}_t{ta}_{tb}_g{ga}_{gb}"
    G, S, adj = build(p, ta, tb, ga, gb)
    n = G.n
    print(f"== p={p} t=({ta},{tb}) g=({ga},{gb}) ord(g)={G.order(S[1])} n={n}")
    with open(os.path.join(HERE, f"{tag}.edges"), "w") as f:
        for x in range(n):
            for y in adj[x]:
                if x < int(y):
                    f.write(f"{x} {int(y)}\n")
    with open(os.path.join(HERE, f"{tag}.g6"), "w") as f:
        f.write(graph6(adj) + "\n")
    counts, cycles, dt = enumerate_cycles(adj, tag)
    print(f"cycle counts (C enumerator, {dt:.1f}s): " + ", ".join(f"{l}:{counts[l]}" for l in range(3, 17)))
    assert all(counts[l] == 0 for l in range(3, 14)), "girth < 14!"
    assert counts[14] > 0
    N14, N15, N16 = counts[14], counts[15], counts[16]
    assert len(cycles) == N14 + N15 + N16
    cyc_lits = [(len(c), off_labels(adj, c)) for c in cycles]

    # per-vertex, per-label counts of 14-cycles through the edge with that label
    thru = np.zeros((n, 3), dtype=np.int64)   # 14-cycles through edge (x, x*S[j])
    for L, lits in cyc_lits:
        if L != 14:
            continue
        for x, j in lits:
            for jj in range(3):
                if jj != j:
                    thru[x, jj] += 1
    col_sets = [sorted(set(thru[:, j].tolist())) for j in range(3)]
    print(f"14-cycles through the t-edge / g-edge / g^-1-edge at a vertex (set of values over vertices): {col_sets}")
    c_t, c_g = col_sets[0][0], col_sets[1][0]
    assert n * c_t // 2 + n * c_g == 14 * N14
    cmin_sum = int(thru.min(axis=1).sum())
    print(f"Lemma 5.2 check: sum_v c_min(v) = {cmin_sum}  vs  9*N14 = {9*N14}  ->  {'OK (necessary condition holds)' if cmin_sum <= 9*N14 else 'FAILS: no orientation exists'}")

    # per-cycle label histograms (number of t-edges on the cycle)
    for lab, name in ((0, "t"), (1, "g/g^-1")):
        pass
    # group-invariant orientations
    for j, name in ((0, "u = t-edge everywhere"), (1, "u = g-edge everywhere"), (2, "u = g^-1-edge everywhere")):
        bad, worst = check_orientation(adj, cycles, [j] * n)
        print(f"invariant orientation [{name}]: violated cycles = {bad} (worst a(C) by length: {worst})")

    # subgroup-invariant instances
    r = next(r for r in range(2, p) if all(pow(r, (p - 1) // q, p) != 1 for q in range(2, p) if (p - 1) % q == 0 and all(q % m for m in range(2, q))))
    dlog = {pow(r, k, p): k for k in range(p - 1)}
    divisors = [d for d in range(1, p) if (p - 1) % d == 0]
    results = {}
    instances = []
    # translation-only: orbits = a-coordinate
    instances.append(("Z_p (translations only)", [x // p for x in range(n)]))
    for d in divisors:
        if d == 1:
            continue
        m = (p - 1) // d
        instances.append((f"Z_p x| H_{d} (index {m}, {m} orbits)", [dlog[int(G.a[x])] % m for x in range(n)]))
    for d in divisors:
        if d in (1,):
            continue
        H = [pow(r, k * ((p - 1) // d), p) for k in range(d)]
        orb = {}
        orbit_of = [0] * n
        for x in range(n):
            a, b = G.pair(x)
            key = min(G.idx((c * a) % p, (c * b) % p) for c in H)
            orbit_of[x] = orb.setdefault(key, len(orb))
        instances.append((f"H_{d} = <({H[1] if d>1 else 1},0)> (multiplicative, {len(orb)} orbits)", orbit_of))
    if not cnf_only:
        budget = float(os.environ.get("SUB_BUDGET", "30"))
        for name, orbit_of in sorted(instances, key=lambda t: max(t[1]) + 1):
            no = max(orbit_of) + 1
            if no == n or no > 200:
                continue
            cnf, ncons = build_cnf(cyc_lits, no, orbit_of, n)
            res, model, dt, st = solve_with_limit(cnf, budget)
            status = {True: "SAT", False: "UNSAT", None: f"TIMEOUT({budget}s)"}[res]
            extra = ""
            if res:
                choice = model_to_choice(model, orbit_of, n)
                bad, worst = check_orientation(adj, cycles, choice)
                extra = f"  independent re-verification: violated cycles = {bad}"
                if bad == 0:
                    with open(os.path.join(HERE, f"{tag}_orientation_{no}orbits.txt"), "w") as f:
                        for x in range(n):
                            f.write(f"{x} {int(adj[x][choice[x]])}\n")
            print(f"[{name}] orbits={no} vars={cnf.nv} clauses={len(cnf.clauses)} distinct cycle constraints={ncons}: {status} in {dt:.1f}s{extra}")
            results[name] = status
    # full instance
    cnf, ncons = build_cnf(cyc_lits, n, list(range(n)), n)
    fn = os.path.join(HERE, f"{tag}_full.cnf")
    cnf.to_file(fn)
    print(f"full instance written: {fn}  vars={cnf.nv} clauses={len(cnf.clauses)} cycle constraints={ncons}")
    json.dump({"p": p, "t": [ta, tb], "g": [ga, gb], "n": n, "N14": N14, "N15": N15, "N16": N16,
               "c_t": int(c_t), "c_g": int(c_g), "cmin_sum": cmin_sum, "sub_results": results},
              open(os.path.join(HERE, f"{tag}_summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
