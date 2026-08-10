#!/usr/bin/env python3
"""verify_exceptions.py — self-contained, independent verifier for the
strict-failure (exceptional) triples of Erdős #699 found in this session.

For each claimed triple (n, i, j) with n = 2^k or n = 3^m + 1 this script
re-derives everything from first principles, sharing no code with the search
engines:

  1. re-factors the relevant windows (n, n-1, n-2 as needed) from the
     supplied factor lists, verifying each list exactly (product check +
     primality of every factor);
  2. recomputes the complete witness pool T_i = {p prime > i : n mod p < i}
     (T_i is contained in the primes of the window — proof: p | n - (n mod p));
  3. checks that j is p-dominated by n (Kummer: p does NOT divide C(n,j))
     for EVERY p in T_i — so no witness p > i exists;
  4. checks the saving witness p = i: i prime, i | C(n,i), i | C(n,j);
  5. re-enumerates ALL strict-failure j in (i, n/2] for that (n, i) by
     direct CRT over the verified prime powers (independent of the search
     engine's enumeration) and confirms the claimed j-list is complete.

Primality: Miller-Rabin with the 13 bases {2,...,41}, DETERMINISTIC for
x < 3 317 044 064 679 887 385 961 981 (Sorenson & Webster 2015); gmpy2
BPSW + 50 MR rounds above that bound, flagged per-claim in the output.
Every prime in every claimed triple is below the bound.

Exit 0 with "ALL VERIFIED" only if every claim checks. Output is the
certificate; commit it under certs/.
"""
import sys
from math import prod
import gmpy2

D64 = 1 << 64
SW_BOUND = 3317044064679887385961981  # Sorenson–Webster 2015: the 13 bases
SW_BASES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]  # deterministic below

def det_mr(n, a):
    """one Miller–Rabin round, exact"""
    if n % a == 0:
        return n == a
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    x = pow(a, d, n)
    if x in (1, n - 1):
        return True
    for _ in range(s - 1):
        x = x * x % n
        if x == n - 1:
            return True
    return False

def is_prime(x):
    """DETERMINISTIC for x < 3.317e24 (Sorenson–Webster); BPSW+50MR beyond."""
    if x < 2:
        return False
    if x < SW_BOUND:
        return all(det_mr(x, a) for a in SW_BASES)
    return bool(gmpy2.is_prime(gmpy2.mpz(x), 50))

def dominated(p, n, j):
    """True iff every base-p digit of j is <= the digit of n (p ∤ C(n,j))."""
    while j:
        if j % p > n % p:
            return False
        j //= p
        n //= p
    return True

def crt(r1, m1, r2, m2):
    x = int(gmpy2.invert(m1 % m2, m2))
    return (r1 + m1 * ((x * ((r2 - r1) % m2)) % m2)) % (m1 * m2)

# Claimed exceptional triples with the factorizations they depend on.
# Each window entry: (N_value_expr, [(p, e), ...]) — verified below.
# For n = 2^k, level 2: window = {n-1 = 2^k - 1}; T_2 = its odd primes.
# For n = 3^m+1, level 3: windows n = 3^m+1 and n-2 = 3^m-1; T_3 = primes>3.
CLAIMS = [
    # (label, n, i, j_list, windows) ; windows = list of (value, factors, r)
    ("2^4",   2**4,   2, [6],    [(2**4 - 1, [(3,1),(5,1)], 1)]),
    ("2^9",   2**9,   2, [147],  [(2**9 - 1, [(7,1),(73,1)], 1)]),
    ("2^11",  2**11,  2, [713],  [(2**11 - 1, [(23,1),(89,1)], 1)]),
    ("2^41",  2**41,  2, [285920731515],
        [(2**41 - 1, [(13367,1),(164511353,1)], 1)]),
    ("2^67",  2**67,  2, [23206563898901803639],
        [(2**67 - 1, [(193707721,1),(761838257287,1)], 1)]),
    ("2^101", 2**101, 2, [137177249633792241973877360183],
        [(2**101 - 1, [(7432339208719,1),(341117531003194129,1)], 1)]),
    ("2^137", 2**137, 2, [16141961986503368055107762054812561012816],
        [(2**137 - 1, [(32032215596496435569,1),(5439042183600204290159,1)], 1)]),
    ("3^2+1",  3**2 + 1,  3, [(3**2 + 1)//2],
        [(3**2 + 1,  [(2,1),(5,1)], 0),  (3**2 - 1,  [(2,3)], 2)]),
    ("3^3+1",  3**3 + 1,  3, [(3**3 + 1)//2],
        [(3**3 + 1,  [(2,2),(7,1)], 0),  (3**3 - 1,  [(2,1),(13,1)], 2)]),
    ("3^5+1",  3**5 + 1,  3, [(3**5 + 1)//2],
        [(3**5 + 1,  [(2,2),(61,1)], 0), (3**5 - 1,  [(2,1),(11,2)], 2)]),
    ("3^7+1",  3**7 + 1,  3, [(3**7 + 1)//2],
        [(3**7 + 1,  [(2,2),(547,1)], 0),(3**7 - 1,  [(2,1),(1093,1)], 2)]),
    ("3^13+1", 3**13 + 1, 3, [(3**13 + 1)//2],
        [(3**13 + 1, [(2,2),(398581,1)], 0),
         (3**13 - 1, [(2,1),(797161,1)], 2)]),
    # the lone i >= 4 exception, general window n=28: {28, 27, 26, 25, 24}
    ("28(i=5)", 28, 5, [14],
        [(28, [(2,2),(7,1)], 0), (27, [(3,3)], 1), (26, [(2,1),(13,1)], 2),
         (25, [(5,2)], 3), (24, [(2,3),(3,1)], 4)]),
]

def verify(label, n, i, j_list, windows):
    print(f"--- {label}: n={n}, i={i}, claimed strict-failure j = {j_list}")
    # 1. verify factorizations
    bpsw_flag = []
    for (val, facs, r) in windows:
        assert prod(p**e for p, e in facs) == val, f"{label}: product mismatch at r={r}"
        for p, e in facs:
            assert is_prime(p), f"{label}: {p} not prime"
            if p >= SW_BOUND:
                bpsw_flag.append(p)
        assert n - r == val or n == val + r, f"{label}: window offset wrong"
        assert n % val in (r % val,) or n - r == val, f"{label}: r mismatch"
    # 2. witness pool T_i: primes > i with n mod p < i.
    #    Every such p <= n divides n - (n mod p) with n mod p < i, so p is
    #    among the primes of the supplied windows PROVIDED the windows cover
    #    n-0 .. n-(i-1) completely — check coverage:
    covered = sorted(n - val for (val, facs, r) in windows)
    # for 2^k level 2 the window n (= 2^k, only prime 2 <= i) may be omitted:
    need = [r for r in range(i)]
    for r in need:
        if r not in covered:
            # allowed only if n - r has no prime factor > i beyond supplied:
            # for n = 2^k, r = 0: n's only prime is 2 <= i — safe.
            x = n - r
            while x % 2 == 0: x //= 2
            while x % 3 == 0 and i >= 3: x //= 3
            assert x == 1, f"{label}: window r={r} uncovered and n-r has odd part {x}"
    T = []
    for (val, facs, r) in windows:
        for p, e in facs:
            if p > i:
                assert n % p == r, f"{label}: residue check p={p}"
                T.append((p, e, r))
    print(f"    witness pool T_{i} = {[(p, f'^{e}', f'r={r}') for p,e,r in T]}"
          f"{'  [BPSW-grade: ' + str(bpsw_flag) + ']' if bpsw_flag else '  [all primality DETERMINISTIC (Sorenson–Webster < 3.317e24)]'}")
    # 3+4. each claimed j: no witness > i, saved by p = i
    half = n // 2
    for j in j_list:
        assert i < j <= half, f"{label}: j out of range"
        for (p, e, r) in T:
            assert dominated(p, n, j), f"{label}: p={p} divides C(n,{j}) — witness exists, NOT a failure!"
        assert is_prime(i), f"{label}: i={i} not prime — would be a COUNTEREXAMPLE"
        assert not dominated(i, n, i), f"{label}: i does not divide C(n,i)"
        assert not dominated(i, n, j), f"{label}: i does not divide C(n,j)"
        print(f"    j={j}: dominated for all {len(T)} witness primes; saved by p={i}  => EXC verified")
    # 5. completeness: re-enumerate all candidates via CRT over prime powers
    mods = sorted(((p**e, r) for (p, e, r) in T), reverse=True)
    M, R0 = 1, [(0, 1)]
    used = []
    for (pe, r) in mods:
        used.append((pe, r))
        M *= pe
        if M > half:
            break
    combos = [(0, 1)]
    for (pe, r) in used:
        combos = [(crt(c, m, b, pe), m * pe) for (c, m) in combos for b in range(r + 1)]
    found = set()
    for (c, m) in combos:
        j = c
        while j <= half:
            if j > i and all(dominated(p, n, j) for (p, e, r) in T):
                found.add(j)
            j += m
    assert found == set(j_list), f"{label}: completeness mismatch: {sorted(found)} vs {j_list}"
    print(f"    completeness: candidate re-enumeration finds exactly {sorted(found)}")
    return bpsw_flag

if __name__ == "__main__":
    flags = []
    for c in CLAIMS:
        flags += verify(*c)
    print()
    if flags:
        print(f"ALL VERIFIED (large-factor primality BPSW-grade for: {flags})")
    else:
        print("ALL VERIFIED — every primality DETERMINISTIC (Sorenson-Webster bound)")
