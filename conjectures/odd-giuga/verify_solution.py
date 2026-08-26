#!/usr/bin/env python3
"""Independent from-definition verifier for search.py solutions.

Deliberately shares no arithmetic with the engine: stdlib Fraction for the
unit-fraction identity, per-prime divisibility for the defining congruence,
sympy.isprime for primality, explicit distinctness/parity checks.

For eps = -1 (Giuga):   requires  p | (n/p - 1)  for every p | n
For eps = +1 (PPN/Znam): requires p | (n/p + 1)  for every p | n
and in both cases  sum(1/p) + eps/n == 1  exactly.

Usage: verify_solution.py results/foo.jsonl [...]
Exits 0 iff every solution in every record verifies and re-sorting the
solution products matches the record's `solutions` list.
"""
import json
import sys
from fractions import Fraction

from sympy import isprime


def check_set(primes, eps, parity):
    assert primes == sorted(primes), "not ascending"
    assert len(set(primes)) == len(primes), "repeated prime"
    n = 1
    for p in primes:
        assert isprime(p), f"{p} not prime"
        if parity == "odd":
            assert p % 2 == 1, f"{p} even in odd run"
        n *= p
    s = sum(Fraction(1, p) for p in primes) + Fraction(eps, n)
    assert s == 1, f"identity fails: {s}"
    for p in primes:
        assert (n // p + eps) % p == 0, f"divisibility fails at {p}"
    return n


def main():
    bad = 0
    total = 0
    for path in sys.argv[1:]:
        for line in open(path):
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            eps, parity = rec["eps"], rec["parity"]
            prods = []
            for s in rec["solution_sets"]:
                total += 1
                try:
                    prods.append(check_set(s, eps, parity))
                except AssertionError as e:
                    bad += 1
                    print(f"FAIL {path} m={rec['m']} {s}: {e}")
            if sorted(prods) != rec["solutions"]:
                bad += 1
                print(f"FAIL {path} m={rec['m']}: product list mismatch")
            tag = "COMPLETE" if rec["complete"] else "INCOMPLETE"
            print(f"ok {path} eps={eps:+d} parity={parity} m={rec['m']} "
                  f"{tag} solutions={len(prods)} nodes={rec['nodes']}")
    print(f"verified {total} solution sets, {bad} failures")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
