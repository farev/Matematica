"""Independent re-derivation of every nonexistence leg of Masselot's
Theorems 1 and 2 (v1.0 census), plus his stated §5-§7 counts, plus an
independent decision of the cyclic C36 cell his Corollary imports from
Gordon's database.

All searches are complete: no orbit reduction is used anywhere in a
nonexistence path (orbit computations appear only to reproduce his
reported counts). Exact integer arithmetic throughout; NumPy is used
only for int-typed batch correlation filtering in the C6xC6 search.

Run from conjectures/signed-difference-sets/ (background-friendly):
    python3 masselot-review/check_targets.py
Writes masselot-review/out/targets_report.json and a text certificate
masselot-review/out/targets_certificate.txt.
"""

import json
import os
import sys
import time
from itertools import product

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import qrlib  # noqa: E402
from validate_pipeline import (  # noqa: E402
    profile_ok, refine_cyclic_double, cyclic_chain, idx2233)

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
REPORT = {}


def log(msg):
    print(msg, flush=True)


# ------------------------------------------------------------------ 32

def target_c32():
    """SDS(32,20,4,[32]): complete chain C8 -> C16 -> C32 from ALL C8
    system solutions (no orbit reduction), plus Masselot's Section 5
    counts for comparison."""
    log("=== (32,20,4) cyclic: chain C8 -> C16 -> C32 ===")
    k, lam, s = 20, 4, 12
    t0 = time.time()
    n_sum_norm, c8 = qrlib.enum_system([8], 4, k, lam, s)
    log(f"C8 system: {n_sum_norm} sum+norm candidates (Masselot: 9528), "
        f"{len(c8)} solutions (Masselot: 56)")
    orbits = qrlib.affine_orbits_cyclic(c8, 8)
    sizes = sorted(len(o) for o in orbits)
    log(f"affine orbits on C8: {len(orbits)} (Masselot: 5), "
        f"sizes {sizes} (Masselot: [8,8,8,16,16])")

    # rep-based C16 count, for comparison with 'twelve distinct C16
    # solutions across the normalized parents'
    add16, _, _ = qrlib.add_table([16])
    neg16 = qrlib.neg_table([16])
    peak16, off16 = k + lam, 2 * lam
    rep_c16_total = 0
    for orb in orbits:
        rep = list(orb[0])
        n_rep = 0
        for vec in refine_cyclic_double(rep, 8, 2):
            if profile_ok(vec, add16, neg16, peak16, off16):
                n_rep += 1
        rep_c16_total += n_rep
    log(f"C16 solutions summed over one representative per orbit: "
        f"{rep_c16_total} (Masselot: 12)")

    # the complete (unreduced) chain
    counts, final, dt = cyclic_chain(
        32, k, lam, s, [(8, 4, 4), (16, 2, 2), (32, 1, 1)])
    # composition check on C16 survivors: 2^b * 3^z refinements each
    log(f"complete chain stages (n, tried, survive): {counts}")
    log(f"FINAL C32 solutions: {len(final)}  "
        f"=> SDS(32,20,4,[32]) {'NONEXISTENT' if not final else 'EXISTS'} "
        f"[{time.time()-t0:.1f}s]")
    REPORT["c32_20_4"] = {
        "c8_sum_norm": n_sum_norm, "c8_solutions": len(c8),
        "orbits": sizes, "rep_c16_total": rep_c16_total,
        "chain_counts": counts, "final_solutions": len(final),
        "verdict": "NONEXISTENT" if not final else "EXISTS",
        "wall_s": round(time.time() - t0, 1),
    }
    return len(final) == 0


# --------------------------------------------------- 36: base systems

def base_systems_36():
    """The four marginal systems of (36,29,4) and Masselot's uniqueness
    claims for them."""
    log("=== (36,29,4) marginal systems ===")
    k, lam, s = 29, 4, 13
    out = {}
    t0 = time.time()

    nG, Gs = qrlib.enum_system([3], 12, k, lam, s)
    log(f"C3 system (m=12): {len(Gs)} solutions: {sorted(Gs)}")
    nH, Hs = qrlib.enum_system([2], 18, k, lam, s)
    log(f"C2 system (m=18): {len(Hs)} solutions: {sorted(Hs)}")
    nF, Fs = qrlib.enum_system([2, 2], 9, k, lam, s)
    forb = qrlib.translation_orbits(Fs, [2, 2])
    log(f"C2^2 system (m=9): {len(Fs)} solutions in {len(forb)} "
        f"translation orbit(s); rep {forb[0][0] if forb else None} "
        f"(Masselot: translates of (7,2,2,2))")
    nE, Es = qrlib.enum_system([3, 3], 4, k, lam, s)
    eorb = qrlib.translation_orbits(Es, [3, 3])
    log(f"C3^2 system (m=4): {nE} sum+norm candidates (Masselot: "
        f"106353), {len(Es)} solutions (Masselot: 9) in {len(eorb)} "
        f"translation orbit(s); rep {eorb[0][0] if eorb else None} "
        f"(Masselot: translates of (-3,2,...,2))")
    out.update({
        "c3": sorted(Gs), "c2": sorted(Hs),
        "c22_solutions": len(Fs), "c22_orbits": len(forb),
        "c33_sum_norm": nE, "c33_solutions": len(Es),
        "c33_orbits": len(eorb), "wall_s": round(time.time() - t0, 1),
    })
    REPORT["marginal_systems_36"] = out
    return Gs, Hs, Fs, Es


# ------------------------------------- 36: the two transparent cells

def target_c2x18(Gs, Fs):
    """SDS(36,29,4,[2,18]): complete enumeration of the order-12
    quotient system on C2^2 x C3 (kernel C3 of C2 x C2 x C9), iterating
    over ALL marginal pairs."""
    log("=== (36,29,4) in C2 x C18: [2,2,3] quotient system ===")
    k, lam = 29, 4
    peak, off = k + 2 * lam, 3 * lam  # m = 3
    t0 = time.time()
    add, _, _ = qrlib.add_table([2, 2, 3])
    neg = qrlib.neg_table([2, 2, 3])
    # cells b[(z,x)], z in C2^2 (4 slots), x in C3; index (a,b,x) =
    # 6a+3b+x in qrlib's [2,2,3] element order
    sols = []
    n_marg_norm_canonical = 0
    slices4 = {}
    for tval in set(t for T in Gs for t in T):
        slices4[tval] = [p for p in product(range(-3, 4), repeat=4)
                         if sum(p) == tval]
    for T in Gs:            # C3 marginal (all rotations, no normalization)
        for R in Fs:        # C2^2 marginal (all translates)
            for s0 in slices4[T[0]]:
                for s1 in slices4[T[1]]:
                    s2 = tuple(R[z] - s0[z] - s1[z] for z in range(4))
                    if any(abs(c) > 3 for c in s2) or sum(s2) != T[2]:
                        continue
                    vec = [0] * 12
                    for z in range(4):
                        a, b = z // 2, z % 2
                        vec[6 * a + 3 * b + 0] = s0[z]
                        vec[6 * a + 3 * b + 1] = s1[z]
                        vec[6 * a + 3 * b + 2] = s2[z]
                    if sum(c * c for c in vec) != peak:
                        continue
                    if T == (1, 6, 6) and R == (7, 2, 2, 2):
                        n_marg_norm_canonical += 1
                    if profile_ok(vec, add, neg, peak, off):
                        sols.append(vec)
    log(f"candidates with canonical marginals (1,6,6)/(7,2,2,2) passing "
        f"norm: {n_marg_norm_canonical} (Masselot: 144)")
    log(f"FULL [2,2,3] system solutions over all marginal pairs: "
        f"{len(sols)}  => SDS(36,29,4,[2,18]) "
        f"{'NONEXISTENT' if not sols else 'undecided'} "
        f"[{time.time()-t0:.1f}s]")
    REPORT["c2x18"] = {
        "canonical_candidates": n_marg_norm_canonical,
        "solutions": len(sols),
        "verdict": "NONEXISTENT" if not sols else "OPEN",
        "wall_s": round(time.time() - t0, 1),
    }
    return len(sols) == 0


def target_c3x12(Es, Hs):
    """SDS(36,29,4,[3,12]): complete enumeration of the order-18
    quotient system on C2 x C3^2 (kernel C2 of C3 x C3 x C4)."""
    log("=== (36,29,4) in C3 x C12: [2,3,3] quotient system ===")
    k, lam = 29, 4
    peak, off = k + lam, 2 * lam  # m = 2
    t0 = time.time()
    add, _, _ = qrlib.add_table([2, 3, 3])
    neg = qrlib.neg_table([2, 3, 3])
    pair_split = {tval: [p for p in product(range(-2, 3), repeat=2)
                         if sum(p) == tval] for tval in range(-4, 5)}
    sols = []
    n_marg_norm_canonical = 0
    canonical_T = (-3, 2, 2, 2, 2, 2, 2, 2, 2)
    for T in Es:
        for R in Hs:
            # DFS over the 9 C3^2 cells; each contributes (b0,b1) with
            # b0+b1 = T[w]; track partial C2 sums
            stack = [(0, (0, 0), [])]
            while stack:
                w, csums, chosen = stack.pop()
                if w == 9:
                    if csums == tuple(R):
                        vec = [0] * 18
                        for j, (b0, b1) in enumerate(chosen):
                            x, y = j // 3, j % 3
                            vec[0 * 9 + 3 * x + y] = b0
                            vec[1 * 9 + 3 * x + y] = b1
                        if sum(c * c for c in vec) == peak:
                            if T == canonical_T and R == (4, 9):
                                n_marg_norm_canonical += 1
                            if profile_ok(vec, add, neg, peak, off):
                                sols.append(vec)
                    continue
                rem = 9 - w - 1
                for (b0, b1) in pair_split[T[w]]:
                    c0, c1 = csums[0] + b0, csums[1] + b1
                    if abs(R[0] - c0) > 2 * rem or abs(R[1] - c1) > 2 * rem:
                        continue
                    stack.append((w + 1, (c0, c1), chosen + [(b0, b1)]))
    log(f"candidates with canonical marginals (-3,2^8)/(4,9) passing "
        f"norm: {n_marg_norm_canonical} (Masselot: 420)")
    log(f"FULL [2,3,3] system solutions over all marginal pairs: "
        f"{len(sols)}  => SDS(36,29,4,[3,12]) "
        f"{'NONEXISTENT' if not sols else 'undecided'} "
        f"[{time.time()-t0:.1f}s]")
    REPORT["c3x12"] = {
        "canonical_candidates": n_marg_norm_canonical,
        "solutions": len(sols),
        "verdict": "NONEXISTENT" if not sols else "OPEN",
        "wall_s": round(time.time() - t0, 1),
    }
    return len(sols) == 0


# --------------------------------------------------- 36: cyclic bonus

def target_c36(Gs, Hs):
    """Independent decision of SDS(36,29,4,[36]) (the Corollary's
    imported datum): complete C18 system (via C9 x C2 hierarchy), then
    ternary refinement to C36 if needed."""
    log("=== (36,29,4) in C36 (independent check of the imported "
        "cyclic nonexistence) ===")
    k, lam, s = 29, 4, 13
    t0 = time.time()
    _, C9s = qrlib.enum_system([9], 4, k, lam, s)
    log(f"C9 system (m=4): {len(C9s)} solutions")
    peak18, off18 = k + lam, 2 * lam
    add18, _, _ = qrlib.add_table([18])
    neg18 = qrlib.neg_table([18])
    pair_split = {tval: [p for p in product(range(-2, 3), repeat=2)
                         if sum(p) == tval] for tval in range(-4, 5)}
    c18 = []
    for T in C9s:
        for R in Hs:
            stack = [(0, (0, 0), [])]
            while stack:
                i, csums, chosen = stack.pop()
                if i == 9:
                    if csums == tuple(R):
                        vec = [0] * 18
                        for j, (b0, b1) in enumerate(chosen):
                            vec[j] = b0
                            vec[j + 9] = b1
                        if sum(c * c for c in vec) == peak18:
                            if profile_ok(vec, add18, neg18, peak18, off18):
                                c18.append(vec)
                    continue
                rem = 9 - i - 1
                for (b0, b1) in pair_split[T[i]]:
                    # cell i has parity i%2, cell i+9 parity (i+9)%2
                    p0, p1 = i % 2, (i + 9) % 2
                    nc = list(csums)
                    nc[p0] += b0
                    nc[p1] += b1
                    if abs(R[0] - nc[0]) > 2 * rem or \
                       abs(R[1] - nc[1]) > 2 * rem:
                        continue
                    stack.append((i + 1, tuple(nc), chosen + [(b0, b1)]))
    log(f"C18 system (m=2): {len(c18)} solutions")
    if not c18:
        log("C18 system EMPTY => SDS(36,29,4) nonexistent in EVERY "
            "order-36 abelian group with a C18 quotient (C36 and C2xC18)"
            f" [{time.time()-t0:.1f}s]")
        REPORT["c36"] = {"c18_solutions": 0,
                         "verdict": "NONEXISTENT (C18 quotient empty)",
                         "wall_s": round(time.time() - t0, 1)}
        return True
    add36, _, _ = qrlib.add_table([36])
    neg36 = qrlib.neg_table([36])
    final = []
    tried = 0
    for sol in c18:
        for vec in refine_cyclic_double(sol, 18, 1):
            tried += 1
            if profile_ok(vec, add36, neg36, k, lam):
                final.append(vec)
    log(f"ternary refinements to C36: {tried} tried, {len(final)} valid "
        f"=> SDS(36,29,4,[36]) "
        f"{'NONEXISTENT' if not final else 'EXISTS'} [{time.time()-t0:.1f}s]")
    REPORT["c36"] = {"c18_solutions": len(c18), "refinements": tried,
                     "final": len(final),
                     "verdict": "NONEXISTENT" if not final else "EXISTS",
                     "wall_s": round(time.time() - t0, 1)}
    return len(final) == 0


# ------------------------------------------------------- 36: C6 x C6

def target_c6x6(Es, Fs):
    """SDS(36,29,4,[6,6]): complete search over C2^2 x C3^2 via
    meet-in-the-middle on the marginal constraints and batched exact
    correlation filtering (int arithmetic; solver-free)."""
    log("=== (36,29,4) in C6 x C6: complete two-layer search ===")
    k, lam = 29, 4
    t0 = time.time()
    pats = {tval: [p for p in product((-1, 0, 1), repeat=4)
                   if sum(p) == tval] for tval in range(-4, 5)}

    # column index layout: position (a,b,x,y) -> 18a+9b+3x+y
    fib_cols = [[idx2233(z // 2, z % 2, j // 3, j % 3) for z in range(4)]
                for j in range(9)]

    # precompute the 35 shift permutations on [2,2,3,3]
    els = qrlib.elements([2, 2, 3, 3])
    idx = {e: i for i, e in enumerate(els)}
    shifts = []
    for d in els[1:]:
        perm = np.array(
            [idx[tuple((g[t] - d[t]) % n for t, n in
                       zip(range(4), (2, 2, 3, 3)))] for g in els],
            dtype=np.int64)
        shifts.append(perm)

    total_candidates = 0
    total_survivors = 0
    for Ti, T in enumerate(Es):
        for R in Fs:
            # halves: fibers 0..3 and 4..8
            def build(fibers):
                rows = [([0] * 36, (0, 0, 0, 0))]
                for j in fibers:
                    nxt = []
                    for vec, cs in rows:
                        for p in pats[T[j]]:
                            v2 = list(vec)
                            for z in range(4):
                                v2[fib_cols[j][z]] = p[z]
                            nxt.append(
                                (v2, tuple(c + q for c, q in zip(cs, p))))
                    rows = nxt
                return rows
            H1 = build(range(0, 4))
            H2 = build(range(4, 9))
            buckets = {}
            for vec, cs in H2:
                buckets.setdefault(cs, []).append(vec)
            pairs = []
            for vec, cs in H1:
                need = tuple(r - c for r, c in zip(R, cs))
                for v2 in buckets.get(need, ()):
                    pairs.append([a + b for a, b in zip(vec, v2)])
            total_candidates += len(pairs)
            if not pairs:
                continue
            X = np.array(pairs, dtype=np.int64)
            alive = np.ones(len(X), dtype=bool)
            for perm in shifts:
                if not alive.any():
                    break
                Y = X[alive]
                corr = np.einsum("ij,ij->i", Y, Y[:, perm])
                keep = corr == lam
                aidx = np.flatnonzero(alive)
                alive[aidx[~keep]] = False
            total_survivors += int(alive.sum())
    log(f"marginal-consistent candidates over all "
        f"{len(Es)}x{len(Fs)} marginal pairs: {total_candidates}; "
        f"surviving full correlation: {total_survivors}  "
        f"=> SDS(36,29,4,[6,6]) "
        f"{'NONEXISTENT' if not total_survivors else 'EXISTS'} "
        f"[{time.time()-t0:.1f}s]")
    REPORT["c6x6"] = {"candidates": total_candidates,
                      "survivors": total_survivors,
                      "verdict": ("NONEXISTENT" if not total_survivors
                                  else "EXISTS"),
                      "wall_s": round(time.time() - t0, 1)}
    return total_survivors == 0


def main():
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    ok32 = target_c32()
    Gs, Hs, Fs, Es = base_systems_36()
    ok_a = target_c2x18(Gs, Fs)
    ok_b = target_c3x12(Es, Hs)
    ok_c36 = target_c36(Gs, Hs)
    ok_66 = target_c6x6(Es, Fs)
    REPORT["all_nonexistence_confirmed"] = bool(
        ok32 and ok_a and ok_b and ok_c36 and ok_66)
    REPORT["total_wall_s"] = round(time.time() - t0, 1)
    with open(os.path.join(OUT, "targets_report.json"), "w") as f:
        json.dump(REPORT, f, indent=1)
    log(f"\nALL NONEXISTENCE LEGS CONFIRMED: "
        f"{REPORT['all_nonexistence_confirmed']} "
        f"[{REPORT['total_wall_s']}s total]")


if __name__ == "__main__":
    main()
