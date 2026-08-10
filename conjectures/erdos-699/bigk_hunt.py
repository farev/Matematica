#!/usr/bin/env python3
"""bigk_hunt.py — decide level-2 strict failures at n = 2^k for large k using
candidate factorizations of 2^k - 1 recalled from memory of the Cunningham
tables. Every candidate factorization is VERIFIED in-script (exact product +
primality of every factor); a wrong or incomplete recollection makes that k
honestly UNDECIDED — recalled data can never contaminate a decision.
Primality: deterministic (<2^64) or BPSW+50MR (flagged) via gmpy2.
"""
import gmpy2
from math import prod

D64 = 1 << 64

def is_prime(x):
    return bool(gmpy2.is_prime(gmpy2.mpz(x), 50))

def dominated(p, n, j):
    while j:
        if j % p > n % p:
            return False
        j //= p
        n //= p
    return True

def crt(r1, m1, r2, m2):
    x = int(gmpy2.invert(m1 % m2, m2))
    return (r1 + m1 * ((x * ((r2 - r1) % m2)) % m2)) % (m1 * m2)

# candidate factor lists for 2^k - 1 (memory-grade until verified)
HINTS = {
    131: [263, 10350794431055162386718619237468234569],
    137: [32032215596496435569, 5439042183600204290159],
    139: [5625767248687, 1846812268885740906271243],
    149: [86656268566282183151, 8235109336690846723986161254029],
    167: [2349023, 62812169112966692268535520802983587091],
    197: [7487, 26828803997912886929710867041891989490486893845712448833],
    199: [164504919713, 4884164093883941177660049098586324302977543600799],
    241: [22000409, 160619474372352289412737508720216839225805656328990879953332340439],
}

def decide(k, facs):
    n = 1 << k
    N = n - 1
    if prod(facs) != N:
        return "UNVERIFIED (product mismatch)"
    exps = {}
    for p in facs:
        if not is_prime(p):
            return f"UNVERIFIED ({p} not prime)"
        exps[p] = exps.get(p, 0) + 1
    flags = [p for p in facs if p >= D64]
    half = n >> 1
    mods = sorted(((p ** e, 1) for p, e in exps.items()), reverse=True)
    combos = [(0, 1)]
    M = 1
    used = 0
    for (pe, r) in mods:
        combos = [(crt(c, m, b, pe), m * pe) for (c, m) in combos for b in (0, 1)]
        M *= pe
        used += 1
        if M > half:
            break
    fails = set()
    for (c, m) in combos:
        j = c
        while j <= half:
            if j > 2 and all(dominated(p, n, j) for p in exps):
                fails.add(j)
            j += m
    tag = f" [BPSW primality: {flags}]" if flags else " [primality deterministic]"
    if fails:
        return f"FAIL j={sorted(fails)}{tag}"
    return f"NONE{tag}"

if __name__ == "__main__":
    for k in sorted(HINTS):
        print(f"k={k}: {decide(k, HINTS[k])}", flush=True)
