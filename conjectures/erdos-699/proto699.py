#!/usr/bin/env python3
"""Semantics prototype for Erdos #699 (Erdos-Szekeres):
for 1 <= i < j <= n/2, is there a prime p >= i with p | gcd(C(n,i), C(n,j))?
Strengthening: p > i outside a finite exceptional set of (n,i,j).

Brute force, exact integer arithmetic, Kummer/Lucas divisibility:
p | C(n,k)  iff  some base-p digit of k exceeds the corresponding digit of n.

Outputs:
  - any violation of the base conjecture (p >= i)   [expect none if ErSz right]
  - all exceptional triples for the strengthening (p > i fails, p = i saves)
  - per-n minimum witness count over pairs (margin statistic)
Also validates a second implementation path (big-int gcd + trial factoring)
against the Kummer path on a subgrid.
"""
import sys
from math import comb, gcd

def primes_up_to(N):
    sieve = bytearray([1]) * (N + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(N**0.5) + 1):
        if sieve[p]:
            sieve[p*p::p] = bytearray(len(sieve[p*p::p]))
    return [i for i in range(N + 1) if sieve[i]]

def divides_binom(p, n, k):
    """p | C(n,k) via Lucas: exists digit of k (base p) > digit of n."""
    while k:
        if k % p > n % p:
            return True
        k //= p
        n //= p
    return False

def run(NMAX, verbose=True):
    P = primes_up_to(NMAX)
    base_violations = []
    exceptional = []          # (n, i, j, witness_primes_eq_i)
    min_margin = {}           # n -> min over pairs of #witnesses (p >= i)
    for n in range(4, NMAX + 1):
        # divmask[k] = bitmask over prime-index of p | C(n,k)
        pr = [p for p in P if p <= n]
        divmask = [0] * (n // 2 + 1)
        for idx, p in enumerate(pr):
            bit = 1 << idx
            for k in range(1, n // 2 + 1):
                if divides_binom(p, n, k):
                    divmask[k] |= bit
        # geq_mask[i] = bitmask of primes >= i ; gt_mask[i] = primes > i
        mm = None
        for i in range(1, n // 2):
            geq = 0
            gt = 0
            for idx, p in enumerate(pr):
                if p >= i:
                    geq |= 1 << idx
                if p > i:
                    gt |= 1 << idx
            di = divmask[i]
            for j in range(i + 1, n // 2 + 1):
                common = di & divmask[j]
                w_geq = common & geq
                w_gt = common & gt
                cnt = bin(w_geq).count("1")
                mm = cnt if mm is None else min(mm, cnt)
                if w_geq == 0:
                    base_violations.append((n, i, j))
                elif w_gt == 0:
                    ws = [pr[idx] for idx in range(len(pr)) if w_geq >> idx & 1]
                    exceptional.append((n, i, j, ws))
        min_margin[n] = mm
    return base_violations, exceptional, min_margin, P

def crosscheck(NMAX, P):
    """Independent path: big-int gcd + trial factorization by primes <= n."""
    bad = 0
    for n in range(4, NMAX + 1):
        for i in range(1, n // 2):
            ci = comb(n, i)
            for j in range(i + 1, n // 2 + 1):
                g = gcd(ci, comb(n, j))
                ws = set()
                gg = g
                for p in P:
                    if p * p > gg and gg > 1:
                        break
                    while gg % p == 0:
                        ws.add(p)
                        gg //= p
                if gg > 1:
                    ws.add(gg)
                ws_geq = sorted(w for w in ws if w >= i)
                # Kummer path
                ws2 = sorted(p for p in P if p <= n and p >= i
                             and divides_binom(p, n, i) and divides_binom(p, n, j))
                if ws_geq != ws2:
                    bad += 1
                    print(f"MISMATCH n={n} i={i} j={j}: gcd-path {ws_geq} kummer-path {ws2}")
    return bad

if __name__ == "__main__":
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 300
    bv, exc, mm, P = run(NMAX)
    print(f"n <= {NMAX}")
    print(f"base (p >= i) violations: {len(bv)}")
    for t in bv[:20]:
        print("  VIOLATION", t)
    print(f"exceptional triples for p > i (saved only by p = i): {len(exc)}")
    for t in exc[:40]:
        print("  EXC", t)
    worst = sorted(mm.items(), key=lambda kv: (kv[1] if kv[1] is not None else 99, kv[0]))[:12]
    print("smallest per-n min-witness-count (n, min#witnesses):", worst)
    # independent cross-check on a small grid
    XC = min(NMAX, 120)
    bad = crosscheck(XC, P)
    print(f"cross-check vs big-int gcd path, n <= {XC}: {'OK' if bad == 0 else f'{bad} MISMATCHES'}")
