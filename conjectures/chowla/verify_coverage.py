"""Independent verification of the sign-pattern coverage results.

Pure Python 3 standard library only -- no NumPy, no shared code with the
C sieve (`lambda_coverage.c`) or with `liouville.py`.  lambda(n) is obtained
by honest trial division, which is slow but leaves nothing to trust.

Two modes.

  python3 verify_coverage.py small [XMAX]
      Recompute N_k for every k with N_k <= XMAX from scratch (default
      200000, which covers k = 1..14) and print the table.  Compare against
      data/fineA_coverage.csv.

  python3 verify_coverage.py window K N CODE
      Check that the length-K window starting at N has pattern code CODE
      under the little-endian encoding
          code = sum_{b<K} [lambda(N+b) < 0] * 2^b
      This is the *exhibition* half of the certificate for N_K: it proves the
      pattern occurs there.  Minimality (that it occurs nowhere earlier) has
      no compact witness and rests on the exhaustive scan.

  python3 verify_coverage.py check FILE
      Run `window` on every row of a coverage CSV (k,N_k,last_pattern_code).
"""

import sys


def omega(n):
    """Number of prime factors of n with multiplicity, by trial division."""
    c = 0
    d = 2
    while d * d <= n:
        while n % d == 0:
            n //= d
            c += 1
        d += 1 if d == 2 else 2
    if n > 1:
        c += 1
    return c


def lam(n):
    return -1 if omega(n) & 1 else 1


def mode_small(xmax):
    bits = [0] * (xmax + 2)
    for n in range(1, xmax + 1):
        bits[n] = 1 if lam(n) < 0 else 0

    print("k,N_k,last_pattern_code")
    rows = []
    k = 1
    while True:
        if (1 << k) > 4 * xmax:
            break
        seen = bytearray(1 << k)
        remaining = 1 << k
        Nk = None
        code = 0
        for s in range(1, xmax - k + 2):
            if s == 1:
                code = 0
                for b in range(k):
                    code |= bits[s + b] << b
            else:
                code = (code >> 1) | (bits[s + k - 1] << (k - 1))
            if not seen[code]:
                seen[code] = 1
                remaining -= 1
                if remaining == 0:
                    Nk = s
                    break
        if Nk is None:
            break
        rows.append((k, Nk, code))
        print(f"{k},{Nk},{code}")
        k += 1
    return rows


def mode_window(k, n, code):
    got = 0
    for b in range(k):
        if lam(n + b) < 0:
            got |= 1 << b
    ok = got == code
    print(f"k={k} N_k={n} claimed_code={code} recomputed={got} "
          f"{'OK' if ok else 'MISMATCH'}")
    return ok


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    if sys.argv[1] == "small":
        xmax = int(float(sys.argv[2])) if len(sys.argv) > 2 else 200000
        mode_small(xmax)
        return 0
    if sys.argv[1] == "window":
        k, n, code = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        return 0 if mode_window(k, n, code) else 1
    if sys.argv[1] == "endgame":
        # lines: "k remaining start code" from lambda_coverage --endgame
        want = int(sys.argv[3]) if len(sys.argv) > 3 else 8
        rows = {}
        for line in open(sys.argv[2]):
            f = line.split()
            if len(f) != 4:
                continue
            rows.setdefault(int(f[0]), []).append(
                (int(f[1]), int(f[2]), int(f[3])))
        allok = True
        for k in sorted(rows):
            sel = sorted(rows[k])[:want]        # the last `want` to complete
            print(f"-- k={k}: verifying the {len(sel)} last-completing "
                  f"patterns by trial division")
            for rem, n, code in sel:
                allok &= mode_window(k, n, code)
        print("ALL OK" if allok else "FAILURES PRESENT")
        return 0 if allok else 1
    if sys.argv[1] == "check":
        allok = True
        with open(sys.argv[2]) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("k,"):
                    continue
                parts = line.split(",")
                k, n, code = int(parts[0]), int(parts[1]), int(parts[2])
                allok &= mode_window(k, n, code)
        print("ALL OK" if allok else "FAILURES PRESENT")
        return 0 if allok else 1
    print(__doc__)
    return 1


if __name__ == "__main__":
    sys.exit(main())
