#!/usr/bin/env python3
"""repunit_hunt.py — scan m for the L3 sufficient condition:
odd(3^m - 1) and odd(3^m + 1) both prime powers  ==>  (3^m+1, 3, (3^m+1)/2)
is a strict failure of the Erdos-Szekeres p > i strengthening (Erdos #699).

Fast filter: trial division by primes < 10^5 on both odd parts; survivors get
gmpy2.is_prime (BPSW + extra MR rounds) and perfect-power treatment.
Output: every m whose both sides survive as prime powers (candidates for new
exceptional triples), plus, for the record, each side's status.

Primality here is probable-prime grade (BPSW); any headline claim gets a
separate certified primality proof (Pocklington) before being labeled
CERTIFIED. Deterministic: no randomness.
"""
import sys
import gmpy2

def odd_part(x):
    v = 0
    while x % 2 == 0:
        x //= 2
        v += 1
    return x, v

def small_primes(lim):
    sieve = bytearray([1]) * lim
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(lim ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytearray(len(sieve[p * p::p]))
    return [i for i in range(lim) if sieve[i]]

SP = small_primes(100000)

def prime_power_status(x):
    """return ('one',), ('prime', x), ('pp', p, e), ('composite', witness) or
    ('pp-unknown-root',) — exact for the classes we act on."""
    if x == 1:
        return ("one",)
    # small-factor scan
    for p in SP:
        if x % p == 0:
            # x = p^e exactly?
            y = x
            e = 0
            while y % p == 0:
                y //= p
                e += 1
            if y == 1:
                return ("pp", p, e)
            return ("composite", p)  # p divides, cofactor > 1 not a power of p
    if gmpy2.is_prime(gmpy2.mpz(x), 40):
        return ("prime", x)
    # perfect power of a large prime?
    for e in range(2, 12):
        root, exact = gmpy2.iroot(gmpy2.mpz(x), e)
        if exact and gmpy2.is_prime(root, 40):
            return ("pp", int(root), e)
    return ("composite", None)  # composite, no small factor found

def main(M):
    hits = []
    for m in range(2, M + 1):
        a = 3 ** m - 1
        b = 3 ** m + 1
        oa, va = odd_part(a)
        ob, vb = odd_part(b)
        sa = prime_power_status(oa)
        sb = prime_power_status(ob)
        ok_a = sa[0] in ("one", "prime", "pp")
        ok_b = sb[0] in ("one", "prime", "pp")
        if ok_a and ok_b:
            hits.append(m)
            print(f"HIT m={m}: odd(3^m-1)={sa[0]}{'' if len(sa)<2 else ' '+str(sa[1])[:40]}"
                  f" v2={va}; odd(3^m+1)={sb[0]}{'' if len(sb)<2 else ' '+str(sb[1])[:40]} v2={vb}",
                  flush=True)
        elif m <= 20 or m % 100 == 0:
            print(f"  m={m}: -1 side {sa[0]}, +1 side {sb[0]}", flush=True)
    print("HITS:", hits)

if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 1400)
