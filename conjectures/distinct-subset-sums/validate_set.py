#!/usr/bin/env python3
"""validate_set.py — zero-cleverness validator for distinct-subset-sums claims.

Checks a claimed DSS set by brute enumeration of all 2^n subset sums
(exact Python integers, no shared code with either search engine).

Run with no arguments to execute the built-in control suite:
  positive controls (must PASS):
    - every known optimal set for n = 4..9 (values 7, 13, 24, 44, 84, 161),
      including J. P. Grossman's optimal 9-set;
    - the Conway-Guy 10-set with max 309 (the f(10) upper-bound witness).
  negative controls (must FAIL):
    - {1,2,3} (1+2=3), {2,3,4,7} (3+4=7), {1,2,4,8,15} (1+2+4+8=15).

Usage: python3 validate_set.py            # control suite
       python3 validate_set.py 3,5,6,7    # validate one set
"""
import sys
from itertools import combinations


def is_dss(s):
    s = sorted(s)
    n = len(s)
    if len(set(s)) != n or any(x < 1 for x in s):
        return False
    seen = set()
    for k in range(n + 1):
        for comb in combinations(s, k):
            t = sum(comb)
            if t in seen:
                return False
            seen.add(t)
    return len(seen) == 2 ** n


def conway_guy_set(n):
    """CG set with n elements: {u_n - u_{n-i}} for the u-sequence."""
    u = [0, 1]
    while len(u) < n + 1:
        # u_{k+1} = 2 u_k - u_{k-r}, r = round(sqrt(2k)); checked below
        # against the literature 10-set, so a slip here cannot pass silently
        k = len(u) - 1
        r = int((2 * k) ** 0.5 + 0.5)
        u.append(2 * u[k] - u[k - r])
    return sorted(u[n] - u[n - i] for i in range(1, n + 1))


POSITIVE = [
    ("f(4)=7 witness", [3, 5, 6, 7]),
    ("f(5)=13 witness", [6, 9, 11, 12, 13]),
    ("f(6)=24 witness", [11, 17, 20, 22, 23, 24]),
    ("f(7)=44 witness", [20, 31, 37, 40, 42, 43, 44]),
    ("f(8)=84 witness", [40, 60, 71, 77, 80, 82, 83, 84]),
    ("Grossman f(9)=161 witness", [77, 117, 137, 148, 154, 157, 159, 160, 161]),
    ("Conway-Guy 10-set max 309", [148, 225, 265, 285, 296, 302, 305, 307, 308, 309]),
]
NEGATIVE = [
    ("1+2=3", [1, 2, 3]),
    ("3+4=7", [2, 3, 4, 7]),
    ("1+2+4+8=15", [1, 2, 4, 8, 15]),
]


def controls():
    ok = True
    for name, s in POSITIVE:
        r = is_dss(s)
        print(f"{'PASS' if r else 'FAIL'} (expect PASS) {name}: {s}")
        ok &= r
    for name, s in NEGATIVE:
        r = is_dss(s)
        print(f"{'FAIL' if not r else 'PASS'} (expect FAIL) {name}: {s}")
        ok &= not r
    cg10 = conway_guy_set(10)
    match = cg10 == POSITIVE[-1][1]
    print(f"{'PASS' if match else 'FAIL'} CG recurrence reproduces the 10-set: {cg10}")
    ok &= match
    print("CONTROLS", "ALL OK" if ok else "BROKEN")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(controls())
    s = [int(x) for x in sys.argv[1].replace(" ", "").split(",")]
    r = is_dss(s)
    print(f"{'DSS' if r else 'NOT-DSS'} {sorted(s)} (n={len(s)}, max={max(s)})")
    sys.exit(0 if r else 1)
