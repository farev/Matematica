"""Controls for the quotient-refinement suite, run BEFORE any new claim.

Cells with independently known answers (all decided in this repository
on 2026-08-09, independently of Masselot's census):

  A. SDS(20,11,2,[20]) -- complete unreduced enumeration here found
     exactly 40 labeled sets, closed under global sign flip, so exactly
     20 have coefficient sum +7. The cyclic chain C10 -> C20 must
     reproduce exactly those 20, each passing sdslib.check_sds.
     (Exact-count completeness control for the chain machinery.)

  B1. SDS(36,29,20,[6,6]) -- NONEXIST (exhaust, 69.9 s, certs/).
     The complete two-layer marginal search must return 0 solutions.
     (Exact-zero agreement control for the two-layer machinery.)

  B2. SDS(36,11,2,[6,6]) -- EXIST (verified witness in certs/).
     The witness's two projections must be members of my complete
     marginal-system enumerations (anti-false-negative check on
     enum_system), and the fiber search restricted to that single
     marginal pair must rediscover at least one valid SDS.
     (Plumbing control: patterns, column pruning, profile check,
     CRT coordinates, check_sds referee.)

  C. SDS(32,28,12,[32]) -- NONEXIST (exhaust). The cyclic chain
     C8 -> C16 -> C32 must terminate with zero solutions.

Exit nonzero on any deviation.
"""

import json
import os
import sys
import time
from itertools import product

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sdslib import check_sds  # noqa: E402
import qrlib  # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")


def log(msg):
    print(msg, flush=True)


def profile_ok(vec, add, neg, peak, off):
    """Early-exit exact correlation profile check."""
    v = len(vec)
    support = [g for g in range(v) if vec[g]]
    s0 = sum(vec[g] * vec[g] for g in support)
    if s0 != peak:
        return False
    for d in range(1, v):
        nd = neg[d]
        c = 0
        for g in support:
            c += vec[g] * vec[add[g][nd]]
        if c != off:
            return False
    return True


def refine_cyclic_double(sol, n_small, bound_small):
    """All splittings of a Z_n vector into a Z_{2n} vector:
    cell b_i = d_i + d_{i+n}, each d in [-bound_small, bound_small]."""
    n = n_small
    per_fiber = [qrlib.splittings(b, bound_small, 2) for b in sol]
    for combo in product(*per_fiber):
        vec = [0] * (2 * n)
        for i, (d0, d1) in enumerate(combo):
            vec[i] = d0
            vec[i + n] = d1
        yield vec


def cyclic_chain(v, k, lam, s, stages):
    """stages: (n, m, bound) smallest quotient upward, ending (v,1,1).
    No symmetry reduction at any stage. Returns (counts, solutions)."""
    n0, m0, _ = stages[0]
    t0 = time.time()
    n_sum_norm, sols = qrlib.enum_system([n0], m0, k, lam, s)
    counts = [(n0, n_sum_norm, len(sols))]
    log(f"    stage C{n0}: {n_sum_norm} sum+norm candidates, "
        f"{len(sols)} system solutions [{time.time()-t0:.1f}s]")
    current = [list(x) for x in sols]
    cur_n = n0
    for (n, m, bound) in stages[1:]:
        t1 = time.time()
        assert n == 2 * cur_n, "chain must double"
        peak = k + (m - 1) * lam
        off = m * lam
        add, _, _ = qrlib.add_table([n])
        neg = qrlib.neg_table([n])
        nxt = []
        tried = 0
        for sol in current:
            for vec in refine_cyclic_double(sol, cur_n, bound):
                tried += 1
                if profile_ok(vec, add, neg, peak, off):
                    nxt.append(vec)
        counts.append((n, tried, len(nxt)))
        log(f"    stage C{n}: {tried} refinements tried, "
            f"{len(nxt)} survive [{time.time()-t1:.1f}s]")
        current = nxt
        cur_n = n
    return counts, current, time.time() - t0


def control_A():
    """The engine's complete unreduced enumeration (with the forced
    |P|/|M| split, i.e. coefficient sum normalized to +7) found exactly
    40 labeled sets; require exact set equality with the chain's output."""
    log("[A] SDS(20,11,2,[20]) chain C10->C20 ...")
    v, k, lam, s = 20, 11, 2, 7
    cert = os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "certs", "audit_20_11_2_c20_full.txt")
    known = set()
    with open(cert) as f:
        for line in f:
            if not line.startswith("WITNESS "):
                continue
            pm = line.split("P=")[1]
            pstr, mstr = pm.split(" M=")
            P = [int(x) for x in pstr.split(",")]
            M = [int(x) for x in mstr.split(",")]
            vec = [0] * v
            for g in P:
                vec[g] = 1
            for g in M:
                vec[g] = -1
            known.add(tuple(vec))
    counts, final, dt = cyclic_chain(v, k, lam, s,
                                     [(10, 2, 2), (20, 1, 1)])
    ok_all = True
    for vec in final:
        P = [g for g in range(v) if vec[g] == 1]
        M = [g for g in range(v) if vec[g] == -1]
        ok, _ = check_sds(v, k, lam, [20], P, M)
        ok_all &= ok
    mine = {tuple(vec) for vec in final}
    verdict = (mine == known) and (len(known) == 40) and ok_all
    log(f"[A] chain found {len(mine)} labeled solutions; certificate "
        f"holds {len(known)}; exact set equality: {mine == known}; "
        f"all check_sds-valid: {ok_all} [{dt:.1f}s] "
        f"-> {'PASS' if verdict else 'FAIL'}")
    return verdict


# ---------------- two-layer machinery for C6 x C6 = C2^2 x C3^2 -------

def idx2233(a, b, x, y):
    return a * 18 + b * 9 + x * 3 + y


def crt_66_to_2233(P66, M66):
    """[6,6] coordinate sets -> coefficient vector over [2,2,3,3]."""
    vec = [0] * 36
    for (u, w), val in [(t, 1) for t in P66] + [(t, -1) for t in M66]:
        vec[idx2233(u % 2, w % 2, u % 3, w % 3)] = val
    return vec


def crt_2233_to_66(vec):
    P, M = [], []
    for i, val in enumerate(vec):
        if not val:
            continue
        y = i % 3
        x = (i // 3) % 3
        b = (i // 9) % 2
        a = i // 18
        u = (3 * a + 4 * x) % 6
        w = (3 * b + 4 * y) % 6
        (P if val == 1 else M).append((u, w))
    return P, M


def projections_2233(vec):
    """(T over C3^2, R over C2^2) cell-sum projections."""
    T = [0] * 9
    R = [0] * 4
    for i, val in enumerate(vec):
        if not val:
            continue
        y = i % 3
        x = (i // 3) % 3
        b = (i // 9) % 2
        a = i // 18
        T[x * 3 + y] += val
        R[a * 2 + b] += val
    return tuple(T), tuple(R)


def two_layer_pairs(k, lam, pairs, add, neg, stop_after=None):
    """Complete fiber DFS over the given (T, R) marginal pairs.
    Returns (nodes, solutions). Solutions satisfy the full [2,2,3,3]
    profile (peak k, off lam) and coefficient bounds {-1,0,1}."""
    peak, off = k, lam
    pats = {}
    for tval in range(-4, 5):
        pats[tval] = [p for p in product((-1, 0, 1), repeat=4)
                      if sum(p) == tval]
    sols = []
    nodes = 0
    done = False
    for (T, R) in pairs:
        if done:
            break
        colT = list(R)

        def rec(fi, cols, chosen):
            nonlocal nodes, done
            if done:
                return
            nodes += 1
            if fi == 9:
                if all(c == t for c, t in zip(cols, colT)):
                    vec = [0] * 36
                    for j, pat in enumerate(chosen):
                        for z in range(4):
                            vec[idx2233(z // 2, z % 2, j // 3, j % 3)] = pat[z]
                    if profile_ok(vec, add, neg, peak, off):
                        sols.append(vec)
                        if stop_after and len(sols) >= stop_after:
                            done = True
                return
            rem = 9 - fi - 1
            for pat in pats[T[fi]]:
                nc = [c + p for c, p in zip(cols, pat)]
                if any(abs(t - c) > rem for c, t in zip(nc, colT)):
                    continue
                chosen.append(pat)
                rec(fi + 1, nc, chosen)
                chosen.pop()

        rec(0, [0, 0, 0, 0], [])
    return nodes, sols


def control_B1():
    log("[B1] SDS(36,29,20,[6,6]) complete two-layer (expect 0) ...")
    t0 = time.time()
    k, lam, s = 29, 20, 27
    nTc, Tsols = qrlib.enum_system([3, 3], 4, k, lam, s)
    nRc, Rsols = qrlib.enum_system([2, 2], 9, k, lam, s)
    log(f"    T-system [3,3] m=4: {nTc} sum+norm, {len(Tsols)} solutions; "
        f"R-system [2,2] m=9: {nRc} sum+norm, {len(Rsols)} solutions")
    add, _, _ = qrlib.add_table([2, 2, 3, 3])
    neg = qrlib.neg_table([2, 2, 3, 3])
    pairs = [(T, R) for T in Tsols for R in Rsols]
    nodes, sols = two_layer_pairs(k, lam, pairs, add, neg)
    verdict = len(sols) == 0
    log(f"[B1] {len(pairs)} marginal pairs, {nodes} nodes, "
        f"{len(sols)} solutions (expected 0) [{time.time()-t0:.1f}s] "
        f"-> {'PASS' if verdict else 'FAIL'}")
    return verdict


def control_B2():
    log("[B2] SDS(36,11,2,[6,6]) witness-projection control ...")
    t0 = time.time()
    k, lam, s = 11, 2, 9
    # first witness from certs/SDS_36_11_2_6_6.txt
    P66 = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
           (1, 0), (2, 1), (3, 2), (4, 3), (5, 4)]
    M66 = [(0, 5)]
    ok, msg = check_sds(36, k, lam, [6, 6], P66, M66)
    if not ok:
        log(f"[B2] stored witness failed check_sds: {msg} -> FAIL")
        return False
    vec = crt_66_to_2233(P66, M66)
    T, R = projections_2233(vec)
    _, Tsols = qrlib.enum_system([3, 3], 4, k, lam, s)
    _, Rsols = qrlib.enum_system([2, 2], 9, k, lam, s)
    memb_T = T in set(Tsols)
    memb_R = R in set(Rsols)
    log(f"    witness projections: T={T} in T-system ({len(Tsols)} sols): "
        f"{memb_T}; R={R} in R-system ({len(Rsols)} sols): {memb_R}")
    add, _, _ = qrlib.add_table([2, 2, 3, 3])
    neg = qrlib.neg_table([2, 2, 3, 3])
    # witness-branch walk: the witness's own fiber patterns must form a
    # branch of the fiber DFS that no prune cuts (anti-false-negative)
    pats = {tval: [p for p in product((-1, 0, 1), repeat=4)
                   if sum(p) == tval] for tval in range(-4, 5)}
    prof = profile_ok(vec, add, neg, k, lam)
    branch_ok = True
    cols = [0, 0, 0, 0]
    for j in range(9):
        pat = tuple(vec[idx2233(z // 2, z % 2, j // 3, j % 3)]
                    for z in range(4))
        if pat not in pats[T[j]]:
            branch_ok = False
            break
        cols = [c + p for c, p in zip(cols, pat)]
        rem = 9 - j - 1
        if any(abs(t - c) > rem for c, t in zip(cols, R)):
            branch_ok = False
            break
    branch_ok &= all(c == t for c, t in zip(cols, R))
    verdict = memb_T and memb_R and prof and branch_ok
    log(f"[B2] witness passes [2,2,3,3] profile check: {prof}; witness "
        f"branch survives every DFS prune: {branch_ok} "
        f"[{time.time()-t0:.1f}s] -> {'PASS' if verdict else 'FAIL'}")
    return verdict


def control_C():
    log("[C] SDS(32,28,12,[32]) chain C8->C16->C32 (expect 0) ...")
    v, k, lam, s = 32, 28, 12, 20
    counts, final, dt = cyclic_chain(
        v, k, lam, s, [(8, 4, 4), (16, 2, 2), (32, 1, 1)])
    verdict = len(final) == 0
    log(f"[C] {len(final)} solutions (expected 0) [{dt:.1f}s] "
        f"-> {'PASS' if verdict else 'FAIL'}")
    return verdict


def main():
    os.makedirs(OUT, exist_ok=True)
    results = {}
    results["A"] = control_A()
    results["B1"] = control_B1()
    results["B2"] = control_B2()
    results["C"] = control_C()
    with open(os.path.join(OUT, "pipeline_controls.json"), "w") as f:
        json.dump(results, f, indent=1)
    log(f"controls: {results}")
    if not all(results.values()):
        sys.exit(1)
    log("all controls PASS")


if __name__ == "__main__":
    main()
