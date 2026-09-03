#!/usr/bin/env python3
"""Bit Deletion game (OEIS A398916): reference Grundy computation and the closed form.

Game: position = positive integer n (binary). A move deletes one binary digit
of n; leading zeros are then stripped. The player who removes the last nonzero
digit (moves to 0) wins.  G(n) = Sprague-Grundy value, G(0) = 0.

Closed form (Theorem 1 of NOTE.md): write n = 1 0^{z_1} 1 0^{z_2} 1 ... 1 0^{z_{m+1}}
in binary (m = number of ones after the leading one, blocks may be empty), let
L = number of binary digits, and t = number of initial blocks that have odd
length (t = max{t : z_1,...,z_t all odd}).  Then

    G(n) = (L mod 2) + 2 * [t is odd].

Everything here is exact integer arithmetic.
"""
import sys, time
from collections import Counter


def grundy_table(N):
    """G(n) for 0 <= n < N straight from the definition (memoised bottom-up)."""
    G = bytearray(N)
    for n in range(1, N):
        s = 0  # bitmask of option values (values are small)
        L = n.bit_length()
        # delete bit at position i (from the top, i = 0 is the leading one)
        for i in range(L):
            hi = n >> (L - i)          # bits above position i
            lo = n & ((1 << (L - i - 1)) - 1)  # bits below position i
            m = (hi << (L - i - 1)) | lo
            s |= 1 << G[m]
        g = 0
        while s >> g & 1:
            g += 1
        G[n] = g
    return G


def closed_form(n):
    """G(n) by the block-parity rule."""
    if n == 0:
        return 0
    L = n.bit_length()
    bits = bin(n)[3:]          # everything after the leading 1
    blocks = bits.split('1')   # zero-blocks z_1..z_{m+1} (as strings)
    t = 0
    for b in blocks:
        if len(b) % 2 == 1:
            t += 1
        else:
            break
    return (L % 2) + 2 * (t % 2)


def h_value(u):
    """h(u) = [t(u) odd] for a binary string u (the digits after the leading 1)."""
    t = 0
    for b in u.split('1'):
        if len(b) % 2 == 1:
            t += 1
        else:
            break
    return t % 2


def formula_u(u):
    return ((len(u) + 1) % 2) + 2 * h_value(u)


def check_induction_step(maxlen):
    """For every string u of length <= maxlen, compute mex of the option values
    *as given by the closed form*, and compare with the closed form at u.
    This is an exhaustive check of the induction step of Theorem 1 for all
    u of length <= maxlen (the theorem proves it for every length)."""
    bad = 0
    total = 0
    for ell in range(0, maxlen + 1):
        for x in range(1 << ell):
            u = format(x, '0%db' % ell) if ell else ''
            opts = set()
            for i in range(ell):
                opts.add(formula_u(u[:i] + u[i + 1:]))
            # jump: delete the leading 1 of n = 1u
            if '1' in u:
                opts.add(formula_u(u[u.index('1') + 1:]))
            else:
                opts.add(0)
            g = 0
            while g in opts:
                g += 1
            total += 1
            if g != formula_u(u):
                bad += 1
                if bad < 5:
                    print("induction-step mismatch at u =", repr(u), g, formula_u(u))
    return total, bad


def check_lemmas(maxlen):
    """Exhaustively check the three deletion lemmas (E1'), (E2), (O1) of NOTE.md
    for all u of length <= maxlen."""
    bad = Counter()
    tot = Counter()
    for ell in range(1, maxlen + 1):
        for x in range(1 << ell):
            u = format(x, '0%db' % ell)
            if '1' not in u:
                continue
            z1 = u.index('1')
            b1 = z1 % 2
            v = u[z1 + 1:]
            hv = h_value(v)
            dels = [u[:i] + u[i + 1:] for i in range(ell)]
            hd = [h_value(d) for d in dels]
            if ell % 2 == 0 and (b1 == 1 or hv == 1):
                tot['E1'] += 1
                if 0 not in hd:
                    bad['E1'] += 1
            if ell % 2 == 0 and b1 == 1 and hv == 0:
                tot['E2'] += 1
                if 1 not in hd:
                    bad['E2'] += 1
            if ell % 2 == 1 and b1 == 1 and hv == 0:
                tot['O1'] += 1
                if 0 not in hd:
                    bad['O1'] += 1
    return dict(tot), dict(bad)


if __name__ == '__main__':
    K = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    t0 = time.time()
    N = 1 << K
    G = grundy_table(N)
    t1 = time.time()
    mism = [n for n in range(N) if G[n] != closed_form(n)]
    print("definition vs closed form for 0 <= n < 2^%d: %d mismatches (%.1fs DP, %.1fs check)"
          % (K, len(mism), t1 - t0, time.time() - t1))
    print("max G:", max(G), " G(4n)=G(n) violations:",
          sum(1 for n in range(1, N // 4) if G[4 * n] != G[n]))
    print("first 40 values:", list(G[:40]))
    print("OEIS A398916 data (first 34 terms) matches:",
          list(G[:34]) == [0,1,2,0,1,3,1,1,2,0,0,2,0,0,0,0,1,3,1,1,3,1,3,3,1,1,1,1,1,1,1,1,2,0])
    for L in range(1, K + 1):
        c = Counter(G[1 << (L - 1): 1 << L])
        hi = c.get(2, 0) + c.get(3, 0)
        print("  L=%2d bits: %s  high-valued count %d = 2^(L-3)? %s"
              % (L, dict(sorted(c.items())), hi, hi == (1 << (L - 3) if L >= 3 else None)))
    tot, bad = check_induction_step(min(K, 18))
    print("induction-step check over all u with |u| <= %d: %d strings, %d mismatches" % (min(K, 18), tot, bad))
    print("lemma check (E1',E2,O1) over |u| <= %d: cases %s, failures %s" % (min(K, 18), *check_lemmas(min(K, 18))))
