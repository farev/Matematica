#!/usr/bin/env python3
"""Cross-checks for the two variants discussed in NOTE.md, straight from their
definitions (exact small-integer arithmetic, no seeds).

  (a) Misere play (Theorem 2): the player who removes the last nonzero digit
      LOSES.  Computes the misere outcome of every n < 2^K by the definition
      and compares with "misere P-position  <=>  normal Grundy value 1".
  (b) Base-b digit deletion (Remark 3): delete one base-b digit, discard
      leading zeros, last nonzero digit wins.  Computes the Grundy values by
      the definition for n < b^K and compares with the binary closed form
      applied to the zero/nonzero pattern of the base-b digits.

Usage: python3 variants.py [K_misere]      (default 20; ~1-2 min)
Run from inside conjectures/bit-deletion/ (imports grundy.py).
"""
import sys
from grundy import closed_form


def misere_check(K):
    N = 1 << K
    W = bytearray(N)      # W[n] = 1 iff the player to move at n wins (misere)
    W[0] = 1              # the previous player removed the last digit and lost
    for n in range(1, N):
        L = n.bit_length()
        win = 0
        for i in range(L):
            hi = n >> (L - i)
            lo = n & ((1 << (L - i - 1)) - 1)
            m = (hi << (L - i - 1)) | lo
            if not W[m]:
                win = 1
                break
        W[n] = win
    bad = sum(1 for n in range(1, N) if (W[n] == 0) != (closed_form(n) == 1))
    counts = []
    for k in range(0, (K - 1) // 2 + 1):
        lim = 1 << (2 * k + 1)
        if lim <= N:
            counts.append((lim, sum(1 for n in range(1, lim) if W[n] == 0), 4 ** k))
    return bad, counts


def digits(n, b):
    d = []
    while n:
        d.append(n % b)
        n //= b
    return d[::-1]


def value(d, b):
    n = 0
    for x in d:
        n = n * b + x
    return n


def base_check(b, K):
    N = b ** K
    G = bytearray(N)
    for n in range(1, N):
        d = digits(n, b)
        s = 0
        for i in range(len(d)):
            s |= 1 << G[value(d[:i] + d[i + 1:], b)]
        g = 0
        while s >> g & 1:
            g += 1
        G[n] = g
    bad = 0
    for n in range(N):
        pattern = int(''.join('0' if x == 0 else '1' for x in digits(n, b)) or '0', 2)
        if G[n] != closed_form(pattern):
            bad += 1
    return N, max(G), bad


if __name__ == '__main__':
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    bad, counts = misere_check(K)
    print("misere: n < 2^%d, disagreements with 'P <=> G = 1': %d" % (K, bad))
    for lim, c, expect in counts:
        print("   misere P-positions below %d: %d (expected 4^k = %d)" % (lim, c, expect))
    for b, KK in [(3, 13), (4, 10), (5, 9), (10, 6)]:
        N, mx, bad = base_check(b, KK)
        print("base %2d: n < %d, max Grundy value %d, mismatches vs binary zero-pattern formula: %d"
              % (b, N, mx, bad))
