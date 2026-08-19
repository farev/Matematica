#!/usr/bin/env python3
"""verify_witness.py — from-definition verifier for dissociated-set /
±zero-sum-free witnesses. Checks all 3^l - 1 signed subsets directly.
Shares no code with any search engine.

Usage:
  python3 verify_witness.py a b "(x1,y1)(x2,y2)..."     rank-2 witness
  python3 verify_witness.py a b c d "(x,y,z,w)(...)"    rank-4 witness
  python3 verify_witness.py --selftest
Exit 0 iff the witness is dissociated (positive verdict).
"""
import re
import sys
from itertools import product


def is_dissociated(mods, seq):
    l = len(seq)
    for signs in product((-1, 0, 1), repeat=l):
        if all(s == 0 for s in signs):
            continue
        v = [sum(s * g[k] for s, g in zip(signs, seq)) % m
             for k, m in enumerate(mods)]
        if all(x == 0 for x in v):
            return False, signs
    return True, None


def parse(mods, s):
    tuples = re.findall(r"\(([-0-9,\s]+)\)", s)
    seq = []
    for t in tuples:
        nums = [int(x) for x in t.split(",")]
        seq.append(tuple(nums[: len(mods)]))
    return seq


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        ok = True
        tests = [
            ((5, 15), "(0,1)(0,2)(0,4)(1,0)(2,0)", True),
            ((7, 21), "(0,1)(0,2)(1,1)(1,5)(2,1)(2,10)(3,19)", True),
            ((5, 15), "(0,1)(0,2)(0,3)", False),      # 1+2-3=0
            ((7, 21), "(1,1)(2,2)(3,3)", False),      # 1+2-3=0 both coords
            ((5, 15), "(0,5)(0,10)", False),          # 5+10 = 0 mod 15
            ((2, 2), "(0,1)(1,0)(1,1)", False),       # full sum = 0
        ]
        for mods, s, expect in tests:
            res, cert = is_dissociated(mods, parse(mods, s))
            good = res == expect
            ok = ok and good
            print(("PASS" if good else "FAIL"),
                  mods, s, "dissociated=%s" % res,
                  ("zero-sum signs=%s" % (cert,)) if cert else "")
        sys.exit(0 if ok else 1)
    args = [a for a in sys.argv[1:]]
    mods = tuple(int(a) for a in args if re.fullmatch(r"\d+", a))
    wit = [a for a in args if "(" in a][0]
    seq = parse(mods, wit)
    res, cert = is_dissociated(mods, seq)
    if res:
        print(f"OK: dissociated set of size {len(seq)} in {mods}")
        sys.exit(0)
    print(f"REJECTED: signed zero-sum {cert} in {mods} for {seq}")
    sys.exit(1)
