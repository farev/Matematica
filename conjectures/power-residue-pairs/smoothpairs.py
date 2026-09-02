#!/usr/bin/env python3
"""Enumerate all pairs (n, n+1) with both n and n+1 smooth over a given prime set,
n+1 <= L.  Output: sorted list of n, plus factorizations.

Usage:  python3 smoothpairs.py PMAX L [extra primes...]  -> writes pairs_P{PMAX}_L{L}.txt
Method: generate all S-smooth numbers <= L by DFS over primes (exact integer
arithmetic), sort, and scan adjacent differences equal to 1.  Nothing floating.
"""
import sys, time
from sympy import primerange, factorint

def smooth_numbers(primes, L):
    out = []
    ps = sorted(primes)
    def rec(i, cur):
        # cur is smooth; extend with primes ps[i:]
        out.append(cur)
        for j in range(i, len(ps)):
            p = ps[j]
            if cur * p > L:
                break  # ps sorted, larger primes also fail
            rec(j, cur * p)
    rec(0, 1)
    out.sort()
    return out

def consecutive_pairs(primes, L):
    sm = smooth_numbers(primes, L)
    pairs = []
    for a, b in zip(sm, sm[1:]):
        if b == a + 1:
            pairs.append(a)
    return pairs, len(sm)

def main():
    pmax = int(sys.argv[1]); L = int(sys.argv[2])
    extra = [int(x) for x in sys.argv[3:]]
    primes = sorted(set(list(primerange(2, pmax + 1)) + extra))
    t0 = time.time()
    pairs, nsm = consecutive_pairs(primes, L)
    t1 = time.time()
    fn = f"pairs_P{pmax}_L{L}" + ("_x" + "_".join(map(str, extra)) if extra else "") + ".txt"
    with open(fn, "w") as f:
        f.write(f"# primes<= {pmax} extra={extra} L={L} nsmooth={nsm} npairs={len(pairs)} time={t1-t0:.1f}s\n")
        f.write("# n  fact(n)  fact(n+1)   [fact = p^e,p^e,...]\n")
        for n in pairs:
            fa = ",".join(f"{p}^{e}" for p, e in sorted(factorint(n).items())) if n > 1 else "1"
            fb = ",".join(f"{p}^{e}" for p, e in sorted(factorint(n + 1).items()))
            f.write(f"{n} {fa} {fb}\n")
    print(f"primes<= {pmax} (+{extra}) L={L}: {nsm} smooth numbers, {len(pairs)} consecutive pairs, {t1-t0:.1f}s -> {fn}")

if __name__ == "__main__":
    main()
