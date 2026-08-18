"""Zero-cleverness brute force: scan every n <= LIMIT, check base-b digit
conditions directly, and for small hits verify against the *definition*
gcd(C(2n,n), 105) = 1 via math.comb.  Ground truth for everything else."""
import sys
from math import comb, gcd

def digits_ok(n, b, dmax):
    while n:
        if n % b > dmax:
            return False
        n //= b
    return True

def main(limit):
    hits = []
    for n in range(limit + 1):
        if digits_ok(n, 3, 1) and digits_ok(n, 5, 2) and digits_ok(n, 7, 3):
            hits.append(n)
    for h in hits:
        if h <= 100_000:  # definition-level check, no Kummer shortcut
            assert gcd(comb(2 * h, h), 105) == 1, h
    # negative control: these must NOT be hits (2 has base-3 digit 2; 5 has base-5 digit... 5=12_3 bad anyway; use 121: 121 = 11111_3? no. Pick explicit)
    for bad in (2, 5, 11, 100, 755, 3159):
        ok = digits_ok(bad, 3, 1) and digits_ok(bad, 5, 2) and digits_ok(bad, 7, 3)
        assert not ok or bad in hits
    print(" ".join(map(str, hits)))
    print(f"count={len(hits)} limit={limit}", file=sys.stderr)

if __name__ == "__main__":
    main(int(float(sys.argv[1])))
