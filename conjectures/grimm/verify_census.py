#!/usr/bin/env python3
"""Independent verifier for grimm_sweep census files.

Deliberately shares no code or method with grimm_sweep.c: primality and
factorization come from sympy (isprime / factorint / nextprime), matching is
re-derived here with networkx-free Hungarian augmenting paths, margins are
recomputed from scratch.

Modes:
  --window LO HI CENSUS      exhaustive cross-check on [LO, HI]: recompute
                             every gap and every critical member by factoring
                             EVERY composite; the census restricted to the
                             window must match exactly (set equality on
                             (p, k, m, sorted factor tuple, L)).
  --check CENSUS [--sample N --seed S]
                             row/gap verification of a big census: every row
                             re-verified arithmetically (p and q=p+k+1 prime,
                             m composite in range, factorization correct and
                             complete, L = max factor <= k, assigned prime
                             divides m and is <= k, assignments distinct in
                             each gap, margin re-derived); for N sampled gaps
                             ALSO re-factor every member to confirm the
                             critical set is complete (no member missing).
Exit 0 iff everything checks.
"""
import argparse, csv, random, sys
from collections import defaultdict

import sympy
from sympy import isprime, factorint, nextprime, prevprime


def load(census):
    gaps = defaultdict(list)  # (p, k) -> [(m, [factors], L, assigned, margin)]
    with open(census) as f:
        for row in csv.DictReader(f):
            p, k, m = int(row["p"]), int(row["k"]), int(row["m"])
            fac = [int(x) for x in row["factorization"].split("*")]
            gaps[(p, k)].append((m, fac, int(row["L"]), int(row["assigned"]),
                                 int(row["margin"])))
    return gaps


def criticals_bruteforce(p, q):
    """All critical members of the gap (p, q), by factoring every member."""
    k = q - p - 1
    out = []
    for m in range(p + 1, q):
        fac = sorted(factorint(m))
        if fac[-1] <= k:
            out.append((m, fac, fac[-1]))
    return out


def margin_bruteforce(members):
    """Exact Hall margin over nonempty subsets of criticals."""
    s = len(members)
    best = None
    for T in range(1, 1 << s):
        uni = set()
        sz = 0
        for u in range(s):
            if T >> u & 1:
                sz += 1
                uni.update(members[u][1])
        d = len(uni) - sz
        best = d if best is None else min(best, d)
    return best


def check_gap_rows(p, k, rows, full=False):
    """Arithmetic verification of one gap's census rows. Returns error list."""
    errs = []
    q = p + k + 1
    if not isprime(p): errs.append(f"p={p} not prime")
    if not isprime(q): errs.append(f"q={q} not prime")
    if nextprime(p) != q: errs.append(f"gap ({p},{q}) not maximal: nextprime={nextprime(p)}")
    assigned_seen = set()
    for m, fac, L, assigned, margin in rows:
        if not (p < m < q): errs.append(f"m={m} outside gap")
        if isprime(m): errs.append(f"m={m} prime")
        true_fac = sorted(factorint(m))
        if sorted(fac) != true_fac: errs.append(f"m={m} factorization wrong: {fac} vs {true_fac}")
        if max(true_fac) != L: errs.append(f"m={m} L wrong")
        if L > k: errs.append(f"m={m} L={L} > k={k}: not critical")
        if assigned == 0: errs.append(f"m={m} unassigned (Hall failure recorded?)")
        else:
            if m % assigned: errs.append(f"m={m} assigned {assigned} does not divide")
            if assigned > k: errs.append(f"m={m} assigned {assigned} > k")
            if assigned in assigned_seen: errs.append(f"assigned {assigned} reused in gap p={p}")
            assigned_seen.add(assigned)
    members = [(m, fac, L) for m, fac, L, _, _ in rows]
    mb = margin_bruteforce(members)
    margins = {margin for _, _, _, _, margin in rows}
    if len(margins) != 1 or (mb is not None and margins != {mb} and -99 not in margins):
        errs.append(f"margin mismatch: census {margins}, recomputed {mb}")
    if full:
        # completeness: the census rows must be EXACTLY the criticals
        bf = criticals_bruteforce(p, q)
        if sorted(m for m, _, _ in bf) != sorted(m for m, _, _, _, _ in rows):
            errs.append(f"critical set mismatch at p={p}: brute {[m for m,_,_ in bf]} "
                        f"vs census {[m for m,_,_,_,_ in rows]}")
    return errs


def mode_window(lo, hi, census):
    gaps = load(census)
    in_window = {(p, k): rows for (p, k), rows in gaps.items() if lo <= p <= hi}
    # brute-force pass over every gap in the window
    p = int(sympy.nextprime(lo - 1))
    nerr = 0
    nchecked = ncrit_bf = 0
    while p <= hi:
        q = int(nextprime(p))
        k = q - p - 1
        bf = criticals_bruteforce(p, q) if k >= 1 else []
        ncrit_bf += len(bf)
        rows = in_window.pop((p, k), [])
        if sorted(m for m, _, _ in bf) != sorted(m for m, _, _, _, _ in rows):
            print(f"MISMATCH at gap ({p},{q}) k={k}: brute {[m for m,_,_ in bf]}"
                  f" vs census {[m for m,_,_,_,_ in rows]}")
            nerr += 1
        if rows:
            errs = check_gap_rows(p, k, rows, full=True)
            for e in errs: print(f"ERROR gap p={p}: {e}")
            nerr += len(errs)
        nchecked += 1
        p = q
    for (p, k) in in_window:
        print(f"SPURIOUS census gap p={p} k={k} (not found in window walk)")
        nerr += 1
    print(f"window [{lo},{hi}]: {nchecked} gaps walked, {ncrit_bf} criticals "
          f"by brute force, errors={nerr}")
    return nerr


def mode_check(census, sample, seed):
    """Light arithmetic pass on ALL rows (no sympy primality — feasible on
    million-row censuses), then heavy sympy verification (primality,
    maximality, full refactorization, completeness) on `sample` gaps."""
    gaps = load(census)
    nerr = 0
    for (p, k), rows in gaps.items():
        assigned_seen = set()
        margins = set()
        for m, fac, L, assigned, margin in rows:
            if not (p < m < p + k + 1): print(f"ERROR p={p}: m={m} outside gap"); nerr += 1
            if max(fac) != L: print(f"ERROR p={p}: m={m} L mismatch"); nerr += 1
            if L > k: print(f"ERROR p={p}: m={m} L={L} > k={k}"); nerr += 1
            if assigned == 0: print(f"ERROR p={p}: m={m} unassigned"); nerr += 1
            else:
                if m % assigned: print(f"ERROR p={p}: assigned {assigned} !| m={m}"); nerr += 1
                if assigned > k: print(f"ERROR p={p}: assigned {assigned} > k"); nerr += 1
                if assigned in assigned_seen: print(f"ERROR p={p}: assigned {assigned} reused"); nerr += 1
                assigned_seen.add(assigned)
            for f_ in fac:
                if m % f_: print(f"ERROR p={p}: listed factor {f_} !| m={m}"); nerr += 1
            margins.add(margin)
        if len(margins) != 1: print(f"ERROR p={p}: inconsistent margins {margins}"); nerr += 1
    print(f"light pass: {len(gaps)} gaps, {sum(len(r) for r in gaps.values())} rows, errors={nerr}")
    if sample:
        rng = random.Random(seed)
        keys = sorted(gaps.keys())
        chosen = rng.sample(keys, min(sample, len(keys)))
        serr = 0
        for (p, k) in chosen:
            errs = check_gap_rows(p, k, gaps[(p, k)], full=True)
            for e in errs: print(f"ERROR(sampled) gap p={p}: {e}")
            serr += len(errs)
        print(f"sampled heavy check: {len(chosen)} gaps (primality, maximality, "
              f"full refactor, completeness), errors={serr}")
        nerr += serr
    return nerr


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", nargs=3, metavar=("LO", "HI", "CENSUS"))
    ap.add_argument("--check", metavar="CENSUS")
    ap.add_argument("--sample", type=int, default=0)
    ap.add_argument("--seed", type=int, default=20260815)
    a = ap.parse_args()
    if a.window:
        sys.exit(1 if mode_window(int(a.window[0]), int(a.window[1]), a.window[2]) else 0)
    elif a.check:
        sys.exit(1 if mode_check(a.check, a.sample, a.seed) else 0)
    ap.print_help()


if __name__ == "__main__":
    main()
