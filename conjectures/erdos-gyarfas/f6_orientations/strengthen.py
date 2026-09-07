"""Counting bounds (Lemma 5.2 style) per instance and strengthened CNFs.
Let n_t = number of vertices whose u-edge is the t-edge. Summing a(C) over the
14-cycles: n_t*c_t + (n-n_t)*c_g = sum_C a(C) <= 9*N14, so n_t <= (9*N14 - n*c_g)/(c_t-c_g).
If ord(g)=15, the 62 cosets of <g> are pure-g 15-cycles partitioning V, each
needing >= 3 t-choices, so n_t >= 3*n/15. Both bounds are added to the CNF
(sound strengthening); when the bound gives n_t = 0 we also add unit clauses
and turn the 14-cycle constraints into equalities (a(C)=9 forced)."""
import sys, os, json
from pysat.card import CardEnc, EncType
from pysat.formula import CNF
from orient import build, enumerate_cycles, off_labels, build_cnf, REQ, HERE

REPS = [(29, 28, 0, 3, 1), (29, 28, 0, 8, 1), (31, 30, 0, 7, 1), (31, 30, 0, 10, 1), (31, 30, 0, 11, 1), (31, 30, 0, 22, 1)]
summary = {}
for (p, ta, tb, ga, gb) in REPS:
    G, S, adj = build(p, ta, tb, ga, gb)
    n = G.n
    tag = f"p{p}_t{ta}_{tb}_g{ga}_{gb}"
    counts, cycles, _ = enumerate_cycles(adj, tag)
    cyc_lits = [(len(c), off_labels(adj, c)) for c in cycles]
    N14 = counts[14]
    # per-vertex per-label 14-cycle counts
    thru = [[0, 0, 0] for _ in range(n)]
    kt_hist = {}
    for L, lits in cyc_lits:
        if L != 14:
            continue
        kt = sum(1 for x, j in lits if j != 0) // 2   # vertices with t-edge on C come in pairs
        kt_hist[kt] = kt_hist.get(kt, 0) + 1
        for x, j in lits:
            for jj in range(3):
                if jj != j:
                    thru[x][jj] += 1
    c_t, c_g = thru[0][0], thru[0][1]
    assert all(v == [c_t, c_g, c_g] for v in thru)
    nt_max = (9 * N14 - n * c_g) // (c_t - c_g)
    ordg = G.order(S[1])
    nt_min = 3 * (n // ordg) if ordg == 15 else 0
    # 16-cycles made only of g-edges? (cosets of <g> when ord g = 16: not here) and
    # any 14-cycle with fewer than 3 t-edges cannot host 5 off-vertices when n_t = 0
    print(f"p={p} g=({ga},{gb}) ord(g)={ordg}: c_t={c_t} c_g={c_g} N14={N14}  n_t <= {nt_max};  n_t >= {nt_min}  "
          f"k_t histogram on 14-cycles {dict(sorted(kt_hist.items()))}  -> {'INFEASIBLE BY COUNTING' if nt_min > nt_max else 'feasible window'}")
    summary[tag] = {"c_t": c_t, "c_g": c_g, "N14": N14, "nt_max": nt_max, "nt_min": nt_min, "kt_hist": kt_hist}
    if nt_min > nt_max:
        continue
    cnf, ncons = build_cnf(cyc_lits, n, list(range(n)), n)
    top = cnf.nv
    tvars = [3 * x + 1 for x in range(n)]
    if nt_max == 0:
        for v in tvars:
            cnf.append([-v])
        # a(C) = 9 forced on every 14-cycle: at most 5 off as well
        for L, lits in cyc_lits:
            if L == 14:
                enc = CardEnc.atmost(lits=[3 * x + j + 1 for x, j in lits], bound=5, top_id=top, encoding=EncType.seqcounter)
                cnf.extend(enc.clauses); top = max(top, enc.nv)
    else:
        enc = CardEnc.atmost(lits=tvars, bound=nt_max, top_id=top, encoding=EncType.totalizer)
        cnf.extend(enc.clauses); top = max(top, enc.nv)
        if nt_min > 0:
            enc = CardEnc.atleast(lits=tvars, bound=nt_min, top_id=top, encoding=EncType.totalizer)
            cnf.extend(enc.clauses); top = max(top, enc.nv)
    cnf.nv = max(cnf.nv, top)
    fn = os.path.join(HERE, f"{tag}_strong.cnf")
    cnf.to_file(fn)
    print(f"   strengthened instance: {fn} vars={cnf.nv} clauses={len(cnf.clauses)}")
json.dump(summary, open(os.path.join(HERE, "counting_bounds.json"), "w"), indent=1)
