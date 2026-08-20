"""census.py — dis(G) and D_pm(G) for every abelian group of order <= LIMIT.

Enumerates abelian groups by elementary divisors (one partition per prime),
names them by invariant factors d1 | d2 | ..., and runs ./dis_search max on
each. Output: data/census.csv with columns
  order, invariant_factors, dis, Dpm, log2_upper, attains_upper, nodes, secs

Usage: python3 census.py [LIMIT] [MINORDER]   (defaults 100, 1)
Requires ./dis_search compiled in this directory.
"""
import subprocess
import sys
import time
from functools import reduce


def partitions(k):
    if k == 0:
        yield []
        return
    for first in range(k, 0, -1):
        for rest in partitions(k - first):
            if not rest or rest[0] <= first:
                yield [first] + rest


def factorize(n):
    f = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            f[d] = f.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def abelian_groups(n):
    """Yield each abelian group of order n as a list of prime-power moduli."""
    f = factorize(n)
    primes = sorted(f)

    def rec(i):
        if i == len(primes):
            yield []
            return
        p, e = primes[i], f[primes[i]]
        for part in partitions(e):
            for rest in rec(i + 1):
                yield [p ** a for a in part] + rest

    yield from rec(0)


def invariant_factors(moduli):
    """Multiset of prime powers -> invariant factor form d1 | d2 | ..."""
    f = {}
    for m in moduli:
        ff = factorize(m)
        (p, e), = ff.items()
        f.setdefault(p, []).append(e)
    for p in f:
        f[p].sort(reverse=True)
    r = max(len(v) for v in f.values())
    out = []
    for i in range(r):
        d = 1
        for p, exps in f.items():
            if i < len(exps):
                d *= p ** exps[i]
        out.append(d)
    return sorted(out)   # ascending d1 | d2 | ...


def main():
    limit = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    minorder = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    out = sys.stdout
    out.write("order,invariant_factors,dis,Dpm,log2_upper,attains_upper,nodes,secs\n")
    for n in range(max(2, minorder), limit + 1):
        for moduli in abelian_groups(n):
            args = ["./dis_search", "max"] + [str(m) for m in sorted(moduli)]
            t0 = time.time()
            res = subprocess.run(args, capture_output=True, text=True)
            dt = time.time() - t0
            line = res.stdout.strip().splitlines()[0]
            dis = int(line.split("dis=")[1].split()[0])
            nodes = int(line.split("nodes=")[1].split()[0])
            ub = n.bit_length() - 1          # floor(log2 n)
            inv = invariant_factors(moduli)
            out.write(f"{n},{'x'.join(map(str, inv))},{dis},{dis+1},{ub},"
                      f"{'yes' if dis == ub else 'NO'},{nodes},{dt:.2f}\n")
            out.flush()


if __name__ == "__main__":
    main()
