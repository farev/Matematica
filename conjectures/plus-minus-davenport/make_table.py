#!/usr/bin/env python3
"""make_table.py — consolidate data/sweep/*.txt into data/table.csv.

Per cell: canonical invariant factors, order, rank, dim± (= maxlen = D±−1),
D±, floor, cap, verdict, node count, witness.

floor = max over cyclic decompositions of Σ⌊log₂ n_i⌋ (Lemmas 3+4). Computed
exactly: factor the moduli into prime powers, then maximize over partitions
of the prime-power multiset into pairwise-coprime cells (each cell = one
cyclic factor by CRT).
cap = ⌊log₂|G|⌋ (Lemma 2).
verdict: FORCED (floor=cap), FLOOR / CAP / MID for gap cells.

Exact integer arithmetic (integer log2 via bit_length).
"""
import os
import re
import sys
from functools import lru_cache

def ilog2(n):
    return n.bit_length() - 1

def factor(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f

def primary_parts(mods):
    """multiset of prime powers from the moduli list"""
    pp = []
    for m in mods:
        for p, e in factor(m).items():
            pp.append(p ** e)
    return sorted(pp)

def invariant_factors(mods):
    """canonical d_1 | d_2 | ... from the primary decomposition"""
    pp = primary_parts(mods)
    byp = {}
    for q in pp:
        p = factor(q).popitem()[0]
        byp.setdefault(p, []).append(q)
    r = max((len(v) for v in byp.values()), default=0)
    inv = []
    for i in range(r):
        d = 1
        for p, v in byp.items():
            vs = sorted(v, reverse=True)
            if i < len(vs):
                d *= vs[i]
        inv.append(d)
    return sorted(inv)

def best_floor(mods):
    pp = tuple(primary_parts(mods))

    @lru_cache(maxsize=None)
    def rec(rest):
        if not rest:
            return 0
        rest = list(rest)
        first = rest[0]
        others = rest[1:]
        best = -1
        # choose the coprime cell containing `first`
        from itertools import combinations
        p0 = set(factor(first))
        for k in range(0, len(others) + 1):
            for combo in combinations(range(len(others)), k):
                cell = [first] + [others[i] for i in combo]
                primes = []
                ok = True
                for q in cell:
                    for p in factor(q):
                        if p in primes:
                            ok = False
                            break
                    primes.extend(factor(q))
                    if not ok:
                        break
                if not ok:
                    continue
                prod = 1
                for q in cell:
                    prod *= q
                rem = tuple(x for i, x in enumerate(others) if i not in combo)
                sub = rec(rem)
                val = ilog2(prod) + sub
                if val > best:
                    best = val
        return best

    return rec(pp)

def parse_sweep(d):
    rows = []
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".txt"):
            continue
        txt = open(os.path.join(d, fn)).read().strip()
        if txt.startswith("TIMEOUT") or "PREFIX" in txt or not txt:
            mods = [int(x) for x in fn[:-4].split("_") if x.isdigit()]
            rows.append((mods, None, None, None, txt.split()[0]))
            continue
        m = re.match(
            r"(\d+) (\d+) (\d+) (\d+) (\d+) maxlen=(\d+) dpm=(\d+) nodes=(\d+) witness=(\S*)",
            txt)
        if not m:
            print(f"UNPARSED: {fn}: {txt[:80]}", file=sys.stderr)
            continue
        a, b, c, dd, n, ml, dpm, nodes = (int(m.group(i)) for i in range(1, 9))
        wit = m.group(9)
        mods = [x for x in (a, b, c, dd) if x > 1] or [1]
        rows.append((mods, ml, nodes, wit, None))
    return rows

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    rows = parse_sweep(os.path.join(base, "data", "sweep"))
    out = []
    for mods, ml, nodes, wit, err in rows:
        n = 1
        for x in mods:
            n *= x
        inv = invariant_factors(mods)
        fl = best_floor(mods)
        cap = ilog2(n)
        key = "x".join(map(str, inv))
        if err:
            out.append((n, key, len(inv), "", "", fl, cap, err, "", ""))
            continue
        if ml < fl or ml > cap:
            verdict = "VIOLATES-BOUNDS(BUG)"
        elif fl == cap:
            verdict = "FORCED"
        elif ml == fl:
            verdict = "FLOOR"
        elif ml == cap:
            verdict = "CAP"
        else:
            verdict = "MID"
        out.append((n, key, len(inv), ml, ml + 1, fl, cap, verdict, nodes, wit))
    # dedupe isomorphic presentations (same invariant factors), keep first
    seen = {}
    for row in sorted(out):
        k = row[1]
        if k in seen:
            if row[3] != "" and seen[k][3] != "" and row[3] != seen[k][3]:
                print(f"ISOMORPH MISMATCH {k}: {row} vs {seen[k]}", file=sys.stderr)
            continue
        seen[k] = row
    with open(os.path.join(base, "data", "table.csv"), "w") as f:
        f.write("order,group,rank,dim,dpm,floor,cap,verdict,nodes,witness\n")
        for row in sorted(seen.values()):
            f.write(",".join(map(str, row)) + "\n")
    n_gap = sum(1 for r in seen.values() if r[7] in ("FLOOR", "CAP", "MID"))
    print(f"{len(seen)} groups; {n_gap} gap cells; "
          f"{sum(1 for r in seen.values() if r[7] == 'FLOOR')} FLOOR, "
          f"{sum(1 for r in seen.values() if r[7] == 'CAP')} CAP, "
          f"{sum(1 for r in seen.values() if r[7] == 'MID')} MID, "
          f"{sum(1 for r in seen.values() if r[7] == 'FORCED')} FORCED, "
          f"{sum(1 for r in seen.values() if 'BUG' in str(r[7]))} bound violations")

if __name__ == "__main__":
    main()
