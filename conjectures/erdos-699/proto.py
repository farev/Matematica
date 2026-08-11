#!/usr/bin/env python3
"""proto.py — exact full-pair reference for Erdős Problem 699 (prototype).

Statement (pinned from google-deepmind/formal-conjectures
FormalConjectures/ErdosProblems/699.lean, fetched 2026-08-11):

  WEAK  (#699):  for all 1 <= i < j <= n//2, exists prime p >= i
                 with p | gcd(C(n,i), C(n,j)).
  STRONG (ErSz): same with p > i; conjecturally finitely many
                 exceptional triples (n,i,j).

Method: exact integer arithmetic only. For each n and each prime p <= n,
build the bitmask S_p = { k in [0, n//2] : p | C(n,k) } via the Kummer
carry criterion   p | C(n,k)  <=>  exists t >= 1 : (k mod p^t) > (n mod p^t).
Then for each i, union the S_p over admissible primes and check coverage
of (i, n//2].  No floating point anywhere.

This is the FULL-PAIR version (no big-prime reduction): it is the reference
that the reduced/production implementation is validated against.

Usage: python3 proto.py N [--census] [--xcheck N2]
  N        : verify all n <= N (full pairs)
  --census : print all strong-exceptional triples found
  --xcheck : additionally cross-check all n <= N2 against direct bigint
             gcd factoring (independent path: math.comb + trial division)
"""
import sys, math
from array import array


def primes_up_to(n):
    if n < 2:
        return []
    sieve = bytearray([1]) * (n + 1)
    sieve[0:2] = b"\x00\x00"
    for p in range(2, int(n**0.5) + 1):
        if sieve[p]:
            sieve[p * p :: p] = b"\x00" * len(range(p * p, n + 1, p))
    return [i for i in range(n + 1) if sieve[i]]


def build_Sp(n, p, half):
    """Bitmask (Python int) of k in [0, half] with p | C(n,k), via
    exists t: k mod p^t > n mod p^t.  Bit k set <=> p | C(n,k)."""
    S = 0
    pt = p
    while pt <= n:
        r = n % pt
        # residues r+1 .. pt-1 set, in one period of length pt
        if r < pt - 1:
            period = (((1 << (pt - 1 - r)) - 1) << (r + 1))
            nblocks = half // pt + 1
            tile = (1 << (pt * nblocks)) - 1
            tile //= (1 << pt) - 1  # 000..1000..1000..1 pattern
            S |= period * tile
        pt *= p
    return S & ((1 << (half + 1)) - 1)


def check_n(n, primes, want_census):
    """Return (weak_violations, strong_exceptions) for this n.
    weak_violations: list of (i, j) with NO prime p >= i dividing gcd.
    strong_exceptions: list of (i, j) where weak holds but no p > i."""
    half = n // 2
    if half < 2:
        return [], []
    pren = [p for p in primes if p <= n]
    Sp = {p: build_Sp(n, p, half) for p in pren}
    full = ((1 << (half + 1)) - 1) & ~3  # bits 2..half  (j >= 2 candidates)
    weak_bad, strong_exc = [], []
    for i in range(1, half):  # i < j <= half so i <= half-1
        mask_j = full & ~((1 << (i + 1)) - 1)  # bits i+1 .. half
        if mask_j == 0:
            continue
        U_ge = 0
        U_gt = 0
        for p in pren:
            if p < i:
                continue
            if (Sp[p] >> i) & 1:
                U_ge |= Sp[p]
                if p > i:
                    U_gt |= Sp[p]
                if U_gt & mask_j == mask_j:
                    break
        miss_weak = mask_j & ~U_ge
        miss_strong = mask_j & ~U_gt
        if miss_weak:
            for j in bits(miss_weak):
                weak_bad.append((i, j))
        if miss_strong and want_census:
            for j in bits(miss_strong & ~miss_weak):
                strong_exc.append((i, j))
    return weak_bad, strong_exc


def bits(x):
    while x:
        b = x & -x
        yield b.bit_length() - 1
        x ^= b


# ---------- independent cross-check path (bigint gcd + trial division) ----
def xcheck_n(n, primes):
    """Direct: compute gcds with math.comb, factor by trial division.
    Returns same structure as check_n (weak violations, strong exceptions)."""
    half = n // 2
    C = [math.comb(n, k) for k in range(half + 1)]
    pren = [p for p in primes if p <= n]
    weak_bad, strong_exc = [], []
    for i in range(1, half):
        for j in range(i + 1, half + 1):
            g = math.gcd(C[i], C[j])
            ok_ge = ok_gt = False
            for p in pren:
                if g % p == 0:
                    if p >= i:
                        ok_ge = True
                    if p > i:
                        ok_gt = True
                        break
            if not ok_ge:
                weak_bad.append((i, j))
            elif not ok_gt:
                strong_exc.append((i, j))
    return weak_bad, strong_exc


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 1000
    census = "--census" in sys.argv
    x2 = 0
    for a, v in zip(sys.argv, sys.argv[1:]):
        if a == "--xcheck":
            x2 = int(v)
    primes = primes_up_to(N)
    all_weak, all_exc = [], []
    for n in range(4, N + 1):
        wb, se = check_n(n, primes, True)
        for i, j in wb:
            all_weak.append((n, i, j))
        for i, j in se:
            all_exc.append((n, i, j))
    print(f"n <= {N}: weak violations: {len(all_weak)}")
    for t in all_weak:
        print("  WEAK-COUNTEREXAMPLE?", t)
    print(f"n <= {N}: strong exceptional triples: {len(all_exc)}")
    if census:
        for t in all_exc:
            print("  EXC", t)
    if x2:
        mism = 0
        for n in range(4, x2 + 1):
            a = check_n(n, primes, True)
            b = xcheck_n(n, primes)
            if a != b:
                mism += 1
                print(f"MISMATCH at n={n}: fast={a} slow={b}")
        print(f"xcheck n <= {x2}: {mism} mismatches")


if __name__ == "__main__":
    main()
