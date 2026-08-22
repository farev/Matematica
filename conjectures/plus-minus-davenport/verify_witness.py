#!/usr/bin/env python3
"""verify_witness.py — independent checker for ±zero-sum-free witnesses.

Reads a group and a claimed ±zero-sum-free sequence and verifies, by brute
force over all 3^k − 1 sign patterns (coefficients in {−1, 0, +1}, not all
zero), that no nonempty signed subsequence sums to zero. This is the whole
definition, checked directly — no shared code or model with the engines.

Usage:
  python3 verify_witness.py --group 5 15 --witness "(1,0) (2,0) (0,1) (0,2) (0,4)"
  python3 verify_witness.py --selftest      # positive + negative controls

Exit status 0 iff the witness verifies (or the self-test passes).
"""
import sys
from itertools import product


def check(ds, witness):
    """Return (ok, reason)."""
    k = len(witness)
    zero = tuple(0 for _ in ds)
    for w in witness:
        if len(w) != len(ds) or any(not (0 <= x < d) for x, d in zip(w, ds)):
            return False, f"element {w} out of range for {ds}"
        if w == zero:
            return False, "witness contains 0 (0 alone is a zero subsum)"
    for coeffs in product((-1, 0, 1), repeat=k):
        if all(c == 0 for c in coeffs):
            continue
        s = tuple(sum(c * w[i] for c, w in zip(coeffs, witness)) % d
                  for i, d in enumerate(ds))
        if s == zero:
            return False, f"zero subsum with coefficients {coeffs}"
    return True, f"all {3 ** k - 1} signed subset sums nonzero"


def parse_witness(s):
    out = []
    for tok in s.replace("),", ") ").split():
        tok = tok.strip("()")
        out.append(tuple(int(x) for x in tok.split(",")))
    return out


def main():
    if "--selftest" in sys.argv:
        ok1, r1 = check((5, 15), [(1, 0), (2, 0), (0, 1), (0, 2), (0, 4)])
        # negative control A: contains a ± pair  (1,0), (4,0) = -(1,0)
        ok2, r2 = check((5, 15), [(1, 0), (4, 0), (0, 1)])
        # negative control B: repeated element
        ok3, r3 = check((5, 15), [(1, 1), (1, 1), (0, 2)])
        # negative control C: mixed relation (1,1)+(1,2)-(2,3) = 0
        ok4, r4 = check((5, 15), [(1, 1), (1, 2), (2, 3)])
        print("positive control:", "PASS" if ok1 else "FAIL", "-", r1)
        print("negative control A (± pair):", "PASS" if not ok2 else "FAIL", "-", r2)
        print("negative control B (repeat):", "PASS" if not ok3 else "FAIL", "-", r3)
        print("negative control C (relation):", "PASS" if not ok4 else "FAIL", "-", r4)
        good = ok1 and not ok2 and not ok3 and not ok4
        print("SELFTEST", "PASS" if good else "FAIL")
        sys.exit(0 if good else 1)

    gi = sys.argv.index("--group")
    wi = sys.argv.index("--witness")
    ds = tuple(int(x) for x in sys.argv[gi + 1:wi])
    witness = parse_witness(sys.argv[wi + 1])
    ok, reason = check(ds, witness)
    print(("VERIFIED ±zero-sum-free" if ok else "REJECTED"), "-", reason)
    print("group", ds, "length", len(witness), "witness", witness)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
