#!/usr/bin/env python3
"""verify_row.py — independent re-verification of individual hard rows
(n, i) of the #699 sweep, sharing no code with sweep.c.

For a hard row (composite n, 2 <= i <= n - prevprime(n)) it recomputes:
  candidates  = primes p > i dividing n(n-1)...(n-i+1)
                (by direct trial-division factorization — no SPF sieve)
  uncovered   = { j in (i, n//2] : no candidate p has p | C(n,j) }
                (via Python big-int bitmasks built by an arithmetic
                 tiling formula — no C bitset code shared)
and reports the uncovered set, which must equal the sweep's result for
that row (empty for a clean row; exactly the exception j's otherwise).

Also re-derives the row's Sylvester–Schur guarantee (candidates nonempty).

Usage:
  python3 verify_row.py n i [n i ...]      verify specific rows
  python3 verify_row.py --sample K NMAX SEED   K deterministic pseudo-random
                                               hard rows with n <= NMAX
Exit 0 iff every row's uncovered set is empty OR is a known exception
listed in data/exceptions.csv (if present).
"""
import sys, os


def is_prime(m):
    if m < 2:
        return False
    if m < 4:
        return True
    if m % 2 == 0:
        return False
    d = 3
    while d * d <= m:
        if m % d == 0:
            return False
        d += 2
    return True


def prevprime(n):
    m = n - 1
    while not is_prime(m):
        m -= 1
    return m


def factor(m):
    fs = set()
    d = 2
    while d * d <= m:
        if m % d == 0:
            fs.add(d)
            while m % d == 0:
                m //= d
        d += 1 if d == 2 else 2
    if m > 1:
        fs.add(m)
    return fs


def Sp_mask(n, p, half):
    """bitmask over [0, half]: bit j set <=> p | C(n,j), via
    exists t: j mod p^t > n mod p^t.  One period is built directly and
    tiled by shift-or doubling (linear in half, unlike the division
    trick, which is quadratic for mid-size periods)."""
    S = 0
    pt = p
    while pt <= n:
        r = n % pt
        if r < pt - 1:
            block = ((1 << (pt - 1 - r)) - 1) << (r + 1)
            length = pt
            while length <= half:
                block |= block << length
                length *= 2
            S |= block
        pt *= p
    return S & ((1 << (half + 1)) - 1)


def check_row(n, i, verbose=True):
    assert not is_prime(n), f"n={n} is prime — not a hard row"
    q = prevprime(n)
    g = n - q
    assert 2 <= i <= g, f"(n={n}, i={i}) is not a hard row (gap {g})"
    half = n // 2
    cands = set()
    for r in range(i):
        cands |= {p for p in factor(n - r) if p > i}
    assert cands, f"Sylvester–Schur violated?! row ({n},{i}) — bug"
    U = 0
    for p in sorted(cands, reverse=True):
        if Sp_mask(n, p, half) >> i & 1:
            pass  # membership of i in S_p is automatic (p | some n-r, r < i)
        U |= Sp_mask(n, p, half)
    mask = ((1 << (half + 1)) - 1) & ~((1 << (i + 1)) - 1)
    miss = mask & ~U
    unc = []
    while miss:
        b = miss & -miss
        unc.append(b.bit_length() - 1)
        miss ^= b
    if verbose:
        print(f"row n={n} i={i}: gap={g} candidates={len(cands)} "
              f"uncovered={unc if unc else 'NONE'}")
    return unc


def known_exceptions():
    exc = set()
    if os.path.exists("data/exceptions.csv"):
        for line in open("data/exceptions.csv"):
            if line.startswith("n,"):
                continue
            parts = line.strip().split(",")
            if len(parts) >= 3:
                exc.add((int(parts[0]), int(parts[1]), int(parts[2])))
    return exc


def main():
    exc = known_exceptions()
    bad = 0
    if sys.argv[1] == "--sample":
        K, NMAX, seed = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
        state = seed
        rows = []
        while len(rows) < K:
            state = (state * 6364136223846793005 + 1442695040888963407) % 2**64
            n = 4 + state % (NMAX - 4)
            if is_prime(n):
                continue
            g = n - prevprime(n)
            if g < 2:
                continue
            state = (state * 6364136223846793005 + 1442695040888963407) % 2**64
            i = 2 + state % (g - 1)
            rows.append((n, i))
        print(f"sampling {K} hard rows, n <= {NMAX}, seed {seed} (LCG)")
    else:
        args = [int(x) for x in sys.argv[1:]]
        rows = list(zip(args[::2], args[1::2]))
    for n, i in rows:
        unc = check_row(n, i)
        for j in unc:
            if (n, i, j) not in exc:
                print(f"  UNEXPECTED uncovered j={j} at row ({n},{i}) — "
                      f"not in data/exceptions.csv")
                bad += 1
    print(f"verify_row: {len(rows)} rows checked, "
          f"{'ALL CONSISTENT' if not bad else f'{bad} INCONSISTENCIES'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
