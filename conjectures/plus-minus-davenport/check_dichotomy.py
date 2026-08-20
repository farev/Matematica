"""check_dichotomy.py — verify Conjecture D′ on every computed group.

D′: for every finite abelian G with invariant factors d1 | ... | dr,
dis(G) equals floor(log2 |G|) (counting bound) or L(G) = sum floor(log2 di)
(the Marchan-Ordaz-Schmid lower bound) — never strictly between, never
below L, never above the counting bound.

Reads data/census.csv (invariant factors known per row) and
data/families.csv (group given as its modulus list, which for the family
rows 3xM, 5xM, 7xM, pxp, cyclic is already the invariant-factor form since
the first modulus divides the second). Prints every violation; exit 0 iff
none.
"""
import csv
import sys


def fl2(n):
    return n.bit_length() - 1


def check(source, inv_factors, dis, order):
    L = sum(fl2(d) for d in inv_factors)
    ub = fl2(order)
    ok_range = L <= dis <= ub
    ok_dich = dis == L or dis == ub
    return L, ub, ok_range and ok_dich


def main():
    bad = total = 0
    with open("data/census.csv") as f:
        for r in csv.DictReader(f):
            inv = [int(x) for x in r["invariant_factors"].split("x")]
            L, ub, ok = check("census", inv, int(r["dis"]), int(r["order"]))
            total += 1
            if not ok:
                bad += 1
                print(f"VIOLATION census {r['invariant_factors']}: "
                      f"dis={r['dis']} L={L} ub={ub}")
    try:
        with open("data/families.csv") as f:
            for r in csv.DictReader(f):
                mods = [int(x) for x in r["group"].split("x")]
                for a, b in zip(mods, mods[1:]):
                    if b % a != 0:
                        print(f"note: {r['group']} not in invariant form; "
                              f"skipping D' row (L would be underestimated)")
                        break
                else:
                    L, ub, ok = check("families", mods, int(r["dis"]),
                                      int(r["order"]))
                    total += 1
                    if not ok:
                        bad += 1
                        print(f"VIOLATION families {r['group']}: "
                              f"dis={r['dis']} L={L} ub={ub}")
    except FileNotFoundError:
        pass
    print(f"checked {total} group values; D' violations: {bad}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
