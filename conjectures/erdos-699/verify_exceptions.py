#!/usr/bin/env python3
"""verify_exceptions.py — independent re-verification of exceptional triples
for Erdős Problem 699 / the Erdős–Szekeres strengthening.

For each claimed triple (n, i, j) with 1 <= i < j <= n//2 this recomputes,
from scratch and by a DIFFERENT method than the sweep engines (Legendre
digit-sum valuations, not the Kummer carry criterion, and no reduction
lemmas — ALL primes p <= n are enumerated):

    common(n,i,j)   = { p prime <= n : v_p(C(n,i)) >= 1 and v_p(C(n,j)) >= 1 }

and checks the exception claim:
    (a) no p in common with p > i          (strong version fails at (n,i,j))
    (b) i in common and i is prime         (weak version holds via p = i)
It also confirms gcd > 1 (classical) and reports the full common set.

For n <= XMAX (default 3000) it additionally verifies common(n,i,j) against
a third path: bigint gcd(math.comb(n,i), math.comb(n,j)) factored by trial
division.  Exact integer arithmetic throughout; no floating point.

Usage:  python3 verify_exceptions.py exceptions.txt
        (lines "n i j"; '#' comments ignored)
Exit 0 iff every triple verifies as claimed.

Self-test: --selftest runs positive AND negative controls (real exceptions
must PASS; fabricated non-exceptions must FAIL for the right reason).
"""
import sys, math


def primes_up_to(n):
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            sieve[p * p :: p] = b"\x00" * len(range(p * p, n + 1, p))
    return [i for i in range(n + 1) if sieve[i]]


def digitsum(m, p):
    s = 0
    while m:
        s += m % p
        m //= p
    return s


def vp_binom(n, k, p):
    """v_p(C(n,k)) by Legendre: (s_p(k) + s_p(n-k) - s_p(n)) / (p-1)."""
    num = digitsum(k, p) + digitsum(n - k, p) - digitsum(n, p)
    assert num % (p - 1) == 0
    return num // (p - 1)


def common_primes(n, i, j, primes):
    return [p for p in primes if p <= n
            and vp_binom(n, i, p) >= 1 and vp_binom(n, j, p) >= 1]


def verify_triple(n, i, j, primes, xmax=3000, verbose=True):
    ok = True
    msgs = []
    if not (1 <= i < j <= n // 2):
        return False, ["range violation: need 1 <= i < j <= n//2"]
    com = common_primes(n, i, j, primes)
    over = [p for p in com if p > i]
    at = [p for p in com if p == i]
    if over:
        ok = False
        msgs.append(f"NOT an exception: primes > i in gcd: {over[:10]}")
    if not at:
        ok = False
        msgs.append("weak witness p = i FAILS (i not in common set)"
                    + (" — WEAK COUNTEREXAMPLE!" if not over else ""))
    if at and not _is_prime_slow(i):
        ok = False
        msgs.append("i in common set but i is not prime (impossible)")
    if not com:
        msgs.append("gcd = 1 ?! (violates classical common-factor theorem)")
        ok = False
    if n <= xmax:
        g = math.gcd(math.comb(n, i), math.comb(n, j))
        com2 = []
        gg = g
        for p in primes:
            if p * p > gg and gg > 1:
                break
            while gg % p == 0:
                if p not in com2:
                    com2.append(p)
                while gg % p == 0:
                    gg //= p
        if gg > 1:
            com2.append(gg)
        if sorted(com2) != sorted(com):
            ok = False
            msgs.append(f"bigint path disagrees: {sorted(com2)} vs {sorted(com)}")
        else:
            msgs.append(f"bigint gcd path agrees (gcd has {len(str(g))} digits)")
    if verbose:
        status = "VERIFIED-EXC" if ok else "FAILED"
        print(f"{status} n={n} i={i} j={j} common={com}", *msgs, sep="\n    ")
    return ok, msgs


def _is_prime_slow(m):
    if m < 2:
        return False
    d = 2
    while d * d <= m:
        if m % d == 0:
            return False
        d += 1
    return True


def selftest():
    primes = primes_up_to(3000)
    good = [(10, 3, 5), (16, 2, 6), (28, 3, 14), (28, 5, 14), (244, 3, 122),
            (512, 2, 147), (2048, 2, 713), (2188, 3, 1094)]
    bad = [(30, 2, 3),    # strong holds here (common prime > 2 exists)
           (100, 3, 50),  # strong holds
           (244, 3, 121)] # neighbouring j, not an exception
    allok = True
    for t in good:
        ok, _ = verify_triple(*t, primes)
        if not ok:
            print(f"SELFTEST FAIL: real exception {t} rejected")
            allok = False
    for t in bad:
        ok, _ = verify_triple(*t, primes, verbose=False)
        if ok:
            print(f"SELFTEST FAIL: fabricated triple {t} accepted")
            allok = False
        else:
            print(f"negative control rejected as expected: {t}")
    print("SELFTEST", "PASS" if allok else "FAIL")
    return allok


def main():
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    fn = sys.argv[1]
    triples = []
    for line in open(fn):
        line = line.split("#")[0].strip()
        if not line:
            continue
        n, i, j = map(int, line.split()[:3])
        triples.append((n, i, j))
    if not triples:
        print("no triples to verify")
        sys.exit(0)
    nmax = max(t[0] for t in triples)
    primes = primes_up_to(nmax)
    bad = 0
    for t in triples:
        ok, _ = verify_triple(*t, primes)
        if not ok:
            bad += 1
    print(f"{len(triples) - bad}/{len(triples)} verified as exceptions")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
