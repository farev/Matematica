"""Standalone certificate verifier. No imports from the search code.

Reads a JSON certificate {"moduli": [...], "witness": [[...], ...]} and checks,
by direct enumeration of all 3^k - 1 signed nonempty subset sums in exact
integer arithmetic, that the witness is pm-zero-sum-free. Exit code 0 iff valid.

Usage: python3 verify_witness.py cert.json
       python3 verify_witness.py --inline "5 15" "0,1 0,2 0,4 1,0 2,0"
"""

import json
import sys
from itertools import product


def is_pm_zsf(moduli, elems):
    k = len(elems)
    for signs in product((-1, 0, 1), repeat=k):
        if all(s == 0 for s in signs):
            continue
        ok = False
        for j, m in enumerate(moduli):
            if sum(s * e[j] for s, e in zip(signs, elems)) % m != 0:
                ok = True
                break
        if not ok:
            return False, signs
    return True, None


if __name__ == "__main__":
    if sys.argv[1] == "--inline":
        moduli = [int(x) for x in sys.argv[2].split()]
        elems = [tuple(int(v) for v in e.split(",")) for e in sys.argv[3].split()]
    else:
        with open(sys.argv[1]) as f:
            cert = json.load(f)
        moduli = cert["moduli"]
        elems = [tuple(e) for e in cert["witness"]]
    ok, bad = is_pm_zsf(moduli, elems)
    if ok:
        print(f"VALID: {elems} is pm-zero-sum-free over {' x '.join('C%d' % m for m in moduli)} "
              f"(all {3**len(elems)-1} signed subset sums nonzero)")
        sys.exit(0)
    print(f"INVALID: signs {bad} give a zero sum")
    sys.exit(1)
