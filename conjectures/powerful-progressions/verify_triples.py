#!/usr/bin/env python3
"""Independent per-triple verifier for consecutive-powerful-number AP3s.

For each AP3 line in a census file, verifies with exact integer arithmetic,
sharing no code or method with the census program:
  (1) x, y, z are powerful  — via trial division to cbrt(n) and a perfect
      square cofactor test (different algorithm than the census's a^2 b^3
      generator);
  (2) y - x == z - y  (arithmetic progression);
  (3) consecutiveness: the only powerful numbers in [x, z] are x, y, z —
      by directly enumerating a^2 b^3 in the window for every squarefree
      b <= z^(1/3) (the enumeration is over a window of size 2d, so this
      is cheap regardless of how large z is).
Any failure exits nonzero. This verifies every LISTED triple absolutely;
completeness of the list is the census program's claim, cross-checked
separately by replication.
"""
import re, sys, math


def is_powerful(n):
    """Powerful test by trial division to cbrt(n), then cofactor must be
    1 or a perfect square (a prime p > cbrt(n) can only appear if p^2 = cofactor,
    since p^3 > n)."""
    if n <= 0:
        return False
    m = n
    p = 2
    while p * p * p <= m:
        if m % p == 0:
            e = 0
            while m % p == 0:
                e += 1
                m //= p
            if e < 2:
                return False
        p += 1 if p == 2 else 2
    if m == 1:
        return True
    r = math.isqrt(m)
    return r * r == m


_SQFREE = None  # sieved squarefree flags, built once


def _sqfree_table(limit):
    global _SQFREE
    if _SQFREE is None or len(_SQFREE) <= limit:
        t = bytearray([1]) * (limit + 1)
        p = 2
        while p * p <= limit:
            for q in range(p * p, limit + 1, p * p):
                t[q] = 0
            p += 1
        _SQFREE = t
    return _SQFREE


def powerful_in_window(lo, hi, cbrt_limit):
    """All powerful numbers in [lo, hi], by enumerating a^2 b^3 over
    squarefree b <= hi^(1/3) (sieved table shared across calls)."""
    t = _sqfree_table(cbrt_limit)
    out = set()
    b = 1
    while b * b * b <= hi:
        if t[b]:
            b3 = b * b * b
            a = math.isqrt((lo + b3 - 1) // b3)
            while a * a * b3 < lo:
                a += 1
            while a * a * b3 <= hi:
                out.add(a * a * b3)
                a += 1
        b += 1
    return sorted(out)


def main(path):
    triples = []
    with open(path) as fh:
        for line in fh:
            m = re.match(r"AP3 #(\d+): (\d+) (\d+) (\d+)", line)
            if m:
                triples.append((int(m.group(1)),) + tuple(map(int, m.group(2, 3, 4))))
    bad = 0
    zmax = max(t[3] for t in triples) if triples else 1
    cbrt = 1
    while cbrt ** 3 <= zmax:
        cbrt += 1
    for idx, x, y, z in triples:
        ok_pow = is_powerful(x) and is_powerful(y) and is_powerful(z)
        ok_ap = (y - x) == (z - y) and y > x
        win = powerful_in_window(x, z, cbrt)
        ok_consec = win == [x, y, z]
        if not (ok_pow and ok_ap and ok_consec):
            print(f"FAIL #{idx}: powerful={ok_pow} ap={ok_ap} consecutive={ok_consec}"
                  f" window={win[:6]}{'...' if len(win) > 6 else ''}")
            bad += 1
    print(f"{len(triples)} triples verified independently: "
          f"{len(triples) - bad} PASS, {bad} FAIL")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "census_1e17.txt")
