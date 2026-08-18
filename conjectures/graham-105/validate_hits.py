#!/usr/bin/env python3
"""Independent verification of every reported hit (pure Python bigints,
no code shared with the C engine).  Per hit n with flag f11:
  1. digit conditions: base-3 digits <= 1, base-5 <= 2, base-7 <= 3;
     base-11 digits <= 5 iff f11.
  2. Lucas route: C(2n,n) mod p != 0 iff digitwise digits(2n) >= digits(n),
     checked for p = 3,5,7 (must be nonzero) and p = 11 (nonzero iff f11).
     Digits of 2n are computed independently by bigint doubling, so this
     does not reuse the "digits of n below p/2" criterion.
  3. n <= 10^5: literal gcd(math.comb(2n,n), .) computation.
Exits nonzero on any failure."""
import glob, sys
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

def main(pattern):
    hits = []
    for fn in glob.glob(pattern):
        for line in open(fn):
            parts = line.rstrip("\n").split(",")
            if len(parts) < 7 or parts[6] == "-":
                continue
            for tok in parts[6].split(" "):
                n, f11 = tok.split(":")
                hits.append((int(n), int(f11)))
    hits = sorted(set(hits))
    bad = 0
    for n, f11 in hits:
        d_ok = (max(digs(n, 3)) <= 1 and max(digs(n, 5)) <= 2
                and max(digs(n, 7)) <= 3)
        d11 = max(digs(n, 11)) <= 5
        l_ok = all(lucas_nonzero(n, p) for p in (3, 5, 7))
        l11 = lucas_nonzero(n, 11)
        if not (d_ok and l_ok and d11 == bool(f11) and l11 == bool(f11)):
            print(f"FAIL {n}: digits357={d_ok} lucas357={l_ok} "
                  f"d11={d11} l11={l11} flag={f11}")
            bad += 1
            continue
        if n <= 10**5:
            c = comb(2 * n, n)
            if gcd(c, 105) != 1 or (gcd(c, 11) == 1) != bool(f11):
                print(f"FAIL {n}: literal comb")
                bad += 1
    print(f"validated {len(hits)} distinct hits, {bad} failures")
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "data/grid45_w*.csv"))
