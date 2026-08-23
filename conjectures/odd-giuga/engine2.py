#!/usr/bin/env python3
"""Clean-room cross-check engine for search.py.

Independently derived and deliberately different:
  - stdlib Fraction arithmetic (no gmpy2), sympy primality/nextprime;
  - loose but obviously sound windows: with prefix sum s and product P,
    every future reciprocal sum lies within 1/P of 1 - s, because the
    final correction term eps/n satisfies |eps/n| <= 1/(3P) < 1/P;
  - two-primes-left handled by enumerating q and solving r as an exact
    Fraction (no divisor factorization, no C kernel);
  - every found set re-verified by summing Fractions from scratch.

Slower by design; run on ranges overlapping search.py.  Emits the same
JSONL shape (subset of fields).

usage: engine2.py EPS PARITY M [MMAX] [--out FILE]
"""
import json
import sys
import time
from fractions import Fraction

from sympy import isprime, nextprime


def run(eps, parity, m):
    parity_odd = parity == "odd"
    t0 = time.time()
    sols = []
    nodes = 0

    def verify(primes):
        n = 1
        for p in primes:
            n *= p
        return sum(Fraction(1, p) for p in primes) + Fraction(eps, n) == 1

    def rec(prefix, P, s, t):
        nonlocal nodes
        nodes += 1
        last = prefix[-1] if prefix else 1
        if t == 0:
            if s + Fraction(eps, P) == 1 and verify(prefix):
                sols.append(tuple(prefix))
            return
        rem = 1 - s
        # future sum = rem - eps/n with 0 < 1/n <= 1/(3P) and future sum
        # >= 1/(last new prime) > 1/n: so rem > 0 at every internal node
        if rem <= 0:
            return
        hi_gap = rem + Fraction(1, P)    # 1/p < rem + 1/n < hi_gap
        if t == 1:
            # 1/p + eps/(P p) = rem  =>  p = (1 + eps/P)/rem = (P+eps)/(P rem)
            if rem <= 0:
                return
            pf = Fraction(P + eps, 1) / (P * rem)
            if pf.denominator != 1:
                return
            p = pf.numerator
            if p <= last or (parity_odd and p % 2 == 0) or not isprime(p):
                return
            cand = prefix + [p]
            if verify(cand):
                sols.append(tuple(cand))
            return
        # window for the next prime p: 1/p < hi_gap and t/p > lo_gap
        p = nextprime(last)
        while True:
            fp = Fraction(1, p)
            if fp >= hi_gap:             # too small a prime: overshoot
                p = nextprime(p)
                continue
            # needed future sum >= rem - 1/n >= rem - 1/(P p); the t
            # distinct future reciprocals sum to < t/p: terminating cut
            if Fraction(t, p) + Fraction(1, P * p) <= rem:
                break
            if not (parity_odd and p % 2 == 0):
                if t == 2:
                    close2(prefix, P, s, p)
                else:
                    rec(prefix + [p], P * p, s + fp, t - 1)
            p = nextprime(p)

    def close2(prefix, P, s, q):
        nonlocal nodes
        nodes += 1
        # choose q, then 1/r + eps/(P q r) = rem2  =>  r = (Pq+eps)/(Pq rem2)
        rem2 = 1 - s - Fraction(1, q)
        if rem2 <= 0:
            return
        rf = Fraction(P * q + eps, 1) / (P * q * rem2)
        if rf.denominator != 1:
            return
        r = rf.numerator
        if r <= q or (parity_odd and r % 2 == 0) or not isprime(r):
            return
        cand = prefix + [q, r]
        if verify(cand):
            sols.append(tuple(cand))

    rec([], 1, Fraction(0), m)
    prods = []
    for s_ in sols:
        n = 1
        for p in s_:
            n *= p
        prods.append(n)
    return {
        "engine": "engine2", "m": m, "eps": eps, "parity": parity,
        "complete": True,
        "solutions": sorted(set(prods)),
        "solution_sets": sorted({tuple(sorted(s_)) for s_ in sols}),
        "nodes": nodes,
        "walltime_s": round(time.time() - t0, 3),
    }


def main():
    eps = int(sys.argv[1])
    parity = sys.argv[2]
    m0 = int(sys.argv[3])
    rest = sys.argv[4:]
    m1 = int(rest[0]) if rest and not rest[0].startswith("--") else m0
    out = None
    if "--out" in rest:
        out = rest[rest.index("--out") + 1]
    for m in range(m0, m1 + 1):
        rec = run(eps, parity, m)
        line = json.dumps(rec)
        print(line, flush=True)
        if out:
            with open(out, "a") as f:
                f.write(line + "\n")


if __name__ == "__main__":
    main()
