#!/usr/bin/env python3
"""Independent verification of term files ("n:flag11" lines, as emitted by
topdown.py and engine_td).  Pure Python bigints; shares no code with either
engine.  Per term n with flag f:
  1. digit conditions by string conversion: base-3 digits <= 1, base-5 <= 2,
     base-7 <= 3; base-11 digits <= 5 iff f = 1.
  2. Lucas route: C(2n,n) mod p != 0 iff the base-p digits of 2n dominate
     those of n digitwise, for p = 3,5,7 (must hold) and p = 11 (iff f).
     The digits of 2n are computed independently by bigint doubling, so this
     path does not reuse the "digits of n below p/2" criterion.
  3. n <= 10^5: literal gcd(math.comb(2n,n), 105) = 1 and 11-part vs flag.
Usage: validate_terms.py FILE [FILE...] [--sample K]
With --sample K, a deterministic pseudorandom subset of K terms per file is
checked (seeded by file name) in addition to the first and last 50.
Exits nonzero on any failure."""
import sys
import random
from math import comb, gcd

def digs(n, b):
    if n == 0:
        return [0]
    out = []
    while n:
        out.append(n % b)
        n //= b
    return out

def lucas_nonzero(n, p):
    dn, d2 = digs(n, p), digs(2 * n, p)
    dn += [0] * (len(d2) - len(dn))
    return all(a >= b for a, b in zip(d2, dn))

def check(n, f):
    if max(digs(n, 3)) > 1 or max(digs(n, 5)) > 2 or max(digs(n, 7)) > 3:
        return f"digit condition fails for {n}"
    if (max(digs(n, 11)) <= 5) != bool(f):
        return f"1155 flag wrong for {n}"
    if not all(lucas_nonzero(n, p) for p in (3, 5, 7)):
        return f"Lucas 3/5/7 fails for {n}"
    if lucas_nonzero(n, 11) != bool(f):
        return f"Lucas 11 vs flag fails for {n}"
    if n <= 10**5:
        c = comb(2 * n, n)
        if gcd(c, 105) != 1 or (gcd(c, 11) == 1) != bool(f):
            return f"literal comb fails for {n}"
    return None

def main():
    args = []
    skip = False
    for j, a in enumerate(sys.argv[1:]):
        if skip: skip = False; continue
        if a == "--sample": skip = True; continue
        if not a.startswith("--"): args.append(a)
    sample = 0
    if "--sample" in sys.argv:
        sample = int(sys.argv[sys.argv.index("--sample") + 1])
    bad = 0
    for fn in args:
        terms = []
        for line in open(fn):
            line = line.strip()
            if not line or ":" not in line:
                continue
            body = line.split()[-1]          # tolerate "MAX n:f" lines
            n, f = body.split(":")
            terms.append((int(n), int(f)))
        if not terms:
            print(f"{fn}: no terms")
            continue
        idx = set(range(min(50, len(terms)))) | set(
            range(max(0, len(terms) - 50), len(terms)))
        if sample:
            rng = random.Random(fn)
            idx |= {rng.randrange(len(terms)) for _ in range(sample)}
        errs = 0
        for i in sorted(idx):
            msg = check(*terms[i])
            if msg:
                print(f"{fn}: FAIL {msg}")
                errs += 1
        bad += errs
        print(f"{fn}: checked {len(idx)}/{len(terms)} terms, {errs} failures")
    sys.exit(1 if bad else 0)

if __name__ == "__main__":
    main()
