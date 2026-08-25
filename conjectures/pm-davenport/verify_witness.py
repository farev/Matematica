#!/usr/bin/env python3
"""Independent witness verifier: checks that a claimed set is dissociated
(equivalently plus-minus zero-sum-free) by direct enumeration of all
3^k - 1 nonzero coefficient vectors in {-1,0,+1}^k.

Shares no code with dpm.py / dpm_fast.c: arithmetic on tuples directly,
coefficient vectors from itertools.product.  Exact integers only.

Usage:
    python3 verify_witness.py "5,15" "(0,1) (0,2) (0,4) (1,0) (2,0)"
    python3 verify_witness.py --file witnesses.txt 5,15
      (file lines: one witness per line, elements as (a,b) tuples)

Exit 0 and print DISSOCIATED if every signed combination is nonzero;
exit 1 and print the offending combination otherwise.
"""

import sys
import re
from itertools import product


def parse_elems(s, r):
    tups = re.findall(r"\(([^)]*)\)", s)
    out = []
    for t in tups:
        parts = [int(x) for x in t.split(",")]
        assert len(parts) == r, f"element {t} has wrong rank"
        out.append(tuple(parts))
    return out


def check(orders, elems):
    """Return None if dissociated, else the offending coefficient vector."""
    k = len(elems)
    r = len(orders)
    # distinctness of plus-minus classes is implied by the definition below;
    # we do the full direct check regardless.
    for eps in product((-1, 0, 1), repeat=k):
        if all(e == 0 for e in eps):
            continue
        s = [0] * r
        for e, g in zip(eps, elems):
            if e:
                for i in range(r):
                    s[i] = (s[i] + e * g[i]) % orders[i]
        if all(x == 0 for x in s):
            return eps
    return None


def main():
    args = sys.argv[1:]
    if args and args[0] == "--file":
        fname, orders_s = args[1], args[2]
        orders = [int(x) for x in orders_s.split(",")]
        bad = 0
        n = 0
        with open(fname) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                elems = parse_elems(line, len(orders))
                if not elems:
                    continue
                n += 1
                eps = check(orders, elems)
                if eps is not None:
                    bad += 1
                    print(f"FAIL {line}  relation eps={eps}")
        print(f"checked {n} witnesses over Z_{'+Z_'.join(map(str,orders))}: "
              f"{n-bad} dissociated, {bad} FAILED")
        sys.exit(1 if bad else 0)
    else:
        orders = [int(x) for x in args[0].split(",")]
        elems = parse_elems(args[1], len(orders))
        eps = check(orders, elems)
        if eps is None:
            print(f"DISSOCIATED: {len(elems)} elements over "
                  f"Z_{'+Z_'.join(map(str,orders))}, all "
                  f"{3**len(elems)-1} signed combinations nonzero")
            sys.exit(0)
        print(f"NOT dissociated: eps={eps}")
        sys.exit(1)


if __name__ == "__main__":
    main()
