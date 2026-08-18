#!/usr/bin/env python3
"""Top-down interval-pruned enumeration of A030979 terms below 3^L.
Reference implementation; exact integer arithmetic throughout.

State: the top d base-3 digits of n are fixed (digits 0/1 only), prefix
value A; completions satisfy A <= n <= A + (3^(L-d)-1)/2.

Prune (sound, conservative): with W = (3^(L-d)+1)/2 and e = min{e: b^e >= W}
for b in {5,7}: every completion n has floor(n/b^e) in {Q, Q+1}, Q = A//b^e,
and the base-b digits of n at positions >= e are the digits of floor(n/b^e).
If both Q and Q+1 have a digit above the cap (2 for b=5, 3 for b=7), no
completion is a term.  (The straddle refinement — only considering Q+1 when
the interval crosses a multiple of b^e — is deliberately omitted; it prunes
~20% more nodes but complicates the C engine.  Term lists are unaffected.)

Leaf: n = A; full digit check in bases 5,7 (base 3 by construction);
base-11 digits <= 5 recorded as the 1155 flag.

Output: term lines "n:flag11", then FINGERPRINT and HIST lines on stderr,
directly comparable with the C engine's."""
import sys

MODP = 1_000_000_007

def bad(x, b, c):
    while x:
        if x % b > c:
            return True
        x //= b
    return False

def search(L):
    P3 = [3 ** k for k in range(L + 1)]
    thr = []
    for d in range(L + 1):
        W = (P3[L - d] + 1) // 2
        row = []
        for bp in (5, 7):
            e = 0
            while bp ** e < W:
                e += 1
            row.append(bp ** e)
        thr.append(row)
    terms = []
    nodes = 0
    sys.setrecursionlimit(4 * L + 100)

    def rec(A, d):
        nonlocal nodes
        nodes += 1
        if d == L:
            if not bad(A, 5, 2) and not bad(A, 7, 3):
                terms.append((A, 0 if bad(A, 11, 5) else 1))
            return
        for (bp, cp, be) in ((5, 2, thr[d][0]), (7, 3, thr[d][1])):
            Q = A // be
            if bad(Q, bp, cp) and bad(Q + 1, bp, cp):
                return
        rec(A, d + 1)
        rec(A + P3[L - 1 - d], d + 1)

    rec(0, 0)
    return terms, nodes

def main():
    L = int(sys.argv[1])
    terms, nodes = search(L)
    cnt = len(terms)
    sum64 = xor64 = 0
    sump = 0
    hist = {}
    M = 1 << 64
    for n, f11 in terms:
        a64 = n % M
        sum64 = (sum64 + a64) % M
        xor64 ^= a64
        sump = (sump + n) % MODP
        ln = 0 if n == 0 else len(format_base3(n))
        hist[ln] = hist.get(ln, 0) + 1
        print(f"{n}:{f11}")
    print(f"FINGERPRINT L={L} nodes={nodes} terms={cnt} "
          f"sum64={sum64} xor64={xor64} summodp={sump}", file=sys.stderr)
    print("HIST " + " ".join(f"{k}:{v}" for k, v in sorted(hist.items())),
          file=sys.stderr)

def format_base3(n):
    s = ""
    while n:
        s = str(n % 3) + s
        n //= 3
    return s

if __name__ == "__main__":
    main()
