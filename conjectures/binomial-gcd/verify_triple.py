#!/usr/bin/env python3
"""Standalone verifier for claimed tight triples of Erdos #699.

A triple (n, i, j) is TIGHT iff
  (a) no prime p > i divides both C(n,i) and C(n,j), and
  (b) p = i is prime and divides both.
This verifier shares no code with the discovery engines. It needs the
complete factorization of n(n-1)...(n-i+1); each claimed factorization is
re-verified by multiplication and deterministic primality (sympy isprime,
BPSW + trial, exact for these sizes when combined with the multiplication
check and independent small-trial division).

Divisibility of C(n,k) by p is decided by Kummer's theorem: p | C(n,k) iff
adding k and (n-k) in base p produces a carry. Implemented here directly as
carry propagation (NOT digit domination, deliberately different from the
engines' Lucas formulation).
"""
import sys
from sympy import isprime


def kummer_carry(p, n, k):
    """Number of carries when adding k and n-k in base p (>=1 iff p | C(n,k))."""
    a, b = k, n - k
    assert 0 <= k <= n
    carries = 0
    carry = 0
    while a or b or carry:
        s = a % p + b % p + carry
        carry = 1 if s >= p else 0
        carries += carry
        a //= p
        b //= p
    return carries


def verify_tight(n, i, j, window_factorizations):
    """window_factorizations: dict t -> complete list of (prime, exponent)
    for n - t, 0 <= t < i. Returns (ok, transcript)."""
    T = []
    ok = True

    def chk(cond, msg):
        nonlocal ok
        T.append(("PASS" if cond else "FAIL") + ": " + msg)
        ok = ok and cond

    chk(1 <= i < j <= n // 2, f"range 1 <= {i} < {j} <= {n}//2")
    # verify factorizations
    admissible = []
    for t in range(i):
        m = n - t
        fl = window_factorizations[t]
        prod = 1
        for (q, e) in fl:
            prod *= q ** e
            chk(isprime(q), f"{q} (factor of n-{t}) is prime")
        chk(prod == m, f"product of claimed factorization of n-{t} equals {m}")
        for (q, e) in fl:
            if q > i:
                admissible.append(q)
    # Prop 1: primes p > i dividing C(n,i) are exactly `admissible`
    for q in admissible:
        chk(kummer_carry(q, n, i) >= 1, f"admissible {q} divides C(n,{i}) (Kummer)")
    # (a) each admissible prime must NOT divide C(n,j)
    for q in admissible:
        chk(kummer_carry(q, n, j) == 0, f"{q} does not divide C(n,{j})")
    # completeness of (a): any p > i dividing C(n,i) divides some n-t (Prop 1),
    # so the verified factorizations exhaust them. Record that reasoning:
    T.append(f"NOTE: by C(n,i)=n^(i)/i! and p>i, the admissible primes are "
             f"exactly the >i prime factors of the window — covered above.")
    # (b) p = i divides both
    chk(isprime(i), f"i = {i} is prime")
    chk(kummer_carry(i, n, i) >= 1, f"{i} divides C(n,{i})")
    chk(kummer_carry(i, n, j) >= 1, f"{i} divides C(n,{j})")
    return ok, T


def main():
    # The two deep family members discovered/extended this session, plus the
    # deepest previously known triple as a positive control.
    cases = [
        # (n, i, j, {t: [(q,e),...]})
        (1594324, 3, 797162,               # control: known (conglu 2026)
         {0: [(2, 2), (398581, 1)],
          1: [(3, 13)],
          2: [(2, 1), (797161, 1)]}),
        (2199023255552, 2, 285920731515,   # NEW: n = 2^41
         {0: [(2, 41)],
          1: [(13367, 1), (164511353, 1)]}),
    ]
    allok = True
    for (n, i, j, wf) in cases:
        ok, T = verify_tight(n, i, j, wf)
        print(f"\n=== triple (n={n}, i={i}, j={j}): "
              f"{'VERIFIED TIGHT' if ok else 'FAILED'} ===")
        for line in T:
            print("  " + line)
        allok = allok and ok
    # uniqueness of j for n = 2^41, i = 2: enumerate the dominated set of
    # 13367 independently and filter by 164511353-domination.
    n = 2 ** 41
    q1, q2 = 13367, 164511353
    ds = []
    m = n
    while m:
        ds.append(m % q1)
        m //= q1
    js = [0]
    pw = 1
    for d in ds:
        js = [j + a * pw for j in js for a in range(d + 1)]
        pw *= q1
    sols = [j for j in js if 2 < j <= n // 2
            and kummer_carry(q1, n, j) == 0 and kummer_carry(q2, n, j) == 0]
    print(f"\nuniqueness scan for n=2^41, i=2: dominated-set size base {q1} = "
          f"{len(js)}, solutions in (2, n/2] = {sols}")
    allok = allok and (sols == [285920731515])
    print("\nALL VERIFICATIONS PASS" if allok else "\nSOME VERIFICATION FAILED")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
