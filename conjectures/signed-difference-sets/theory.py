#!/usr/bin/env python3
"""Character-theoretic nonexistence criteria for signed difference sets,
applied to every cell of Gordon's database.

Basis (proof in NOTE.md): for an SDS(v,k,lam) A in abelian G, every
nontrivial character chi of G satisfies |chi(A)|^2 = k - lam, and the
trivial character gives (|P|-|M|)^2 = k + lam(v-1).

T0 (admissibility): s^2 = k + lam(v-1) must be a perfect square with
   s == k (mod 2), 0 <= s <= k, and k <= v.
T1 (order-2 character): if |G| is even, chi of order 2 has chi(A) in Z,
   so k - lam must be a perfect square.
T2 (self-conjugacy, Turyn): if some m | exp(G), m > 2, and a prime
   p with p not dividing m, v_p(k-lam) odd, and -1 in <p> mod m, then
   |alpha|^2 = k - lam is unsolvable in Z[zeta_m]: every prime ideal of
   Z[zeta_m] above p is conjugation-fixed and unramified, so
   v_P(alpha * conj(alpha)) is even while v_P(k-lam) = v_p(k-lam) is odd.
   (p | m is excluded: ramified primes escape the argument — Gauss sums
   have |alpha|^2 = p.)

Cross-checks run by this script:
  - No Yes/All cell of the database may violate any criterion.
  - No exhaust EXIST decision from data/results.csv may violate any.
  - Criterion verdicts on exhausted cells must agree with NONEXIST.

Output: data/theory_closures.csv with one line per Open cell closed,
carrying the criterion and its parameters (m, p, valuation) — a
human-checkable certificate.
"""

import csv
import math
import os
import sys
from collections import Counter

import sdslib


def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def exponent(G):
    e = 1
    for n in G:
        e = e * n // math.gcd(e, n)
    return e


def divisors(n):
    ds = []
    i = 1
    while i * i <= n:
        if n % i == 0:
            ds.append(i)
            if i != n // i:
                ds.append(n // i)
        i += 1
    return sorted(ds)


def is_square(n):
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n


def self_conjugate(p, m):
    """True iff -1 is a power of p in (Z/m)*; requires gcd(p,m)=1."""
    t = p % m
    target = m - 1
    seen = set()
    while t not in seen:
        if t == target:
            return True
        seen.add(t)
        t = (t * p) % m
    return False


def test_cell(v, k, lam, G):
    """Returns (verdict, reason) where verdict is 'NO' or 'open'."""
    n = k - lam
    # T0
    t = k + lam * (v - 1)
    if t < 0 or not is_square(t):
        return "NO", "T0: k+lam(v-1) not a square"
    s = math.isqrt(t)
    if (k - s) % 2 or s > k:
        return "NO", f"T0: s={s} fails parity/size (s==k mod 2, s<=k)"
    if k > v:
        return "NO", "T0: k > v"
    if n < 0:
        return "NO", "T0: k < lam impossible (|C(d)| <= k)"
    # T1
    if v % 2 == 0 and not is_square(n):
        return "NO", f"T1: |G| even, k-lam={n} not a perfect square"
    # T2
    if n > 0:
        e = exponent(G)
        nf = factorize(n)
        for m in divisors(e):
            if m <= 2:
                continue
            for p, a in nf.items():
                if a % 2 == 1 and m % p != 0 and self_conjugate(p, m):
                    return "NO", (f"T2: m={m} | exp(G)={e}, p={p} "
                                  f"self-conjugate mod {m}, v_p(k-lam)={a} odd")
    return "open", ""


def main():
    db = sdslib.load_db()
    closures = []
    viol_yes = []
    counts = Counter()
    for name, entry in sorted(db.items()):
        v, k, lam, G = sdslib.parse_name(name)
        status = entry.get("status")
        verdict, reason = test_cell(v, k, lam, G)
        if status in ("Yes", "All") and verdict == "NO":
            viol_yes.append((name, reason))
        if status == "Open" and verdict == "NO":
            closures.append((name, v, k, lam, G, reason))
            counts[reason.split(":")[0]] += 1

    print(f"Open cells closed by criteria: {len(closures)} "
          f"(by test: {dict(counts)})")
    print(f"Yes/All cells violating a criterion (MUST be 0): {len(viol_yes)}")
    for x in viol_yes[:10]:
        print("  VIOLATION:", x)

    # cross-check against exhaust results
    agree = conflict = 0
    if os.path.exists("data/results.csv"):
        with open("data/results.csv") as f:
            for row in csv.DictReader(f):
                nm = row["name"]
                v, k, lam, G = sdslib.parse_name(nm)
                verdict, reason = test_cell(v, k, lam, G)
                if verdict == "NO" and row["decision"] == "EXIST":
                    conflict += 1
                    print(f"  CONFLICT: {nm} exhaust EXIST but {reason}")
                elif verdict == "NO" and row["decision"] == "NONEXIST":
                    agree += 1
    print(f"exhaust cross-check: {agree} criterion-closed cells agree with "
          f"NONEXIST, {conflict} conflicts (MUST be 0)")

    with open("data/theory_closures.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["name", "v", "k", "lam", "G", "criterion"])
        for (name, v, k, lam, G, reason) in closures:
            w.writerow([name, v, k, lam, str(G), reason])
    print("wrote data/theory_closures.csv")

    if viol_yes or conflict:
        sys.exit(1)


if __name__ == "__main__":
    main()
