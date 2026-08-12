#!/usr/bin/env python3
"""Family census for Erdos #699 exceptional triples at structured n.

For n in the families {2^k} and {3^m + 1} (far beyond any full sweep),
decide for every danger level i (i <= g(n) = n - prevprime(n)) whether an
exceptional triple (n, i, j) or counterexample exists, exactly:

  - admissible primes p > i are exactly the primes p > i dividing
    n(n-1)...(n-i+1)  [L1: C(n,i) = n^(i)/i!, p does not divide i!]
  - a triple needs no prime in (n-i, n]  [L2], so i <= g(n)
  - j must avoid p | C(n,j) for ALL admissible p (Kummer digit test),
    j enumerated by CRT over the two strongest congruence constraints
    (p | C(n,j) is implied by j mod p > n mod p; the complement is a
    union of intervals mod p)
  - survivors classified via p = i (prime, n mod i^2 < i, Kummer on j).

Every n-t (t < g) must factor COMPLETELY into primes for a negative claim
("no exceptional triple at (n,i)"); if a cofactor resists factoring, the
level is reported UNKNOWN (a hidden prime could only cover MORE j, so
'exception exists' claims stay valid under partial factorization, while
'no exception' claims require completeness -- we require completeness for
both to keep it simple, except where noted).

Exact integer arithmetic only.
"""
import sys
from sympy import isprime, factorint, prevprime

CANDMAX = 100_000_000


def kummer_divides(p, n, k):
    while k:
        if k % p > n % p:
            return True
        k //= p
        n //= p
    return False


def factor_or_none(x, limit=2**22):
    """Complete prime factorization or None if a cofactor resists."""
    try:
        f = factorint(x, limit=limit)
    except Exception:
        return None
    out = {}
    for q, e in f.items():
        if isprime(q):
            out[q] = e
        else:
            # try harder on the cofactor with rho/p-1 via full factorint
            try:
                f2 = factorint(q)
            except Exception:
                return None
            if all(isprime(r) for r in f2):
                for r, e2 in f2.items():
                    out[r] = out.get(r, 0) + e2 * e
            else:
                return None
    return out


def digits(n, p):
    d = []
    while n:
        d.append(n % p)
        n //= p
    return d


def dom_size(n, p):
    """|{j in [0,n]: p does not divide C(n,j)}| = prod(digit+1) (Lucas)."""
    s = 1
    for d in digits(n, p):
        s *= d + 1
        if s > CANDMAX:
            return s
    return s


def dom_enumerate(n, p, hi):
    """Yield all j in [0, hi] with p not dividing C(n,j) (digit-dominated),
    streaming (no materialization), pruning branches that exceed hi."""
    ds = digits(n, p)
    L = len(ds)
    pws = [p ** l for l in range(L)]

    def rec(pos, acc):
        if pos < 0:
            yield acc
            return
        for a in range(ds[pos] + 1):
            v = acc + a * pws[pos]
            if v > hi:
                break
            if pos == 0:
                yield v
            else:
                yield from rec(pos - 1, v)

    yield from rec(L - 1, 0)


def check_level(n, i, admissible, verbose=False):
    """admissible: list of (p, t) with t = n mod p < i, p > i, COMPLETE.
    Enumerate the dominated set of the admissible prime with the smallest
    dominated set (these are the only j any prime could fail on), then
    exact-test survivors against all other admissible primes and p = i.
    Returns (exceptional_list, counterexample_list)."""
    nh = n // 2
    exc, cex = [], []
    if not admissible:
        raise RuntimeError(f"empty admissible set at n={n} i={i} (Sylvester–Schur violated?)")
    A = sorted(set(admissible))
    sizes = [(dom_size(n, p), p) for (p, t) in A]
    best_size, best_p = min(sizes)
    if best_size > CANDMAX:
        raise RuntimeError(f"dominated-set blowup at n={n} i={i}: min size {best_size}")
    for j in dom_enumerate(n, best_p, nh):
        if not (i < j <= nh):
            continue
        if any(kummer_divides(p, n, j) for (p, t) in A):
            continue
        # no p > i covers j; try p = i
        if isprime(i) and n % (i * i) < i and kummer_divides(i, n, j):
            exc.append((n, i, j))
        else:
            cex.append((n, i, j))
    return exc, cex


def danger_levels(n):
    """g(n) = n - prevprime(n); 0 if n prime."""
    if isprime(n):
        return 0
    return n - prevprime(n)


def family_entry(n, tag, imax_cap=None):
    """Full exceptional/counterexample decision for all i <= g(n)."""
    g = danger_levels(n)
    nh = n // 2
    imax = min(g, nh - 1 if nh >= 2 else 0)
    if imax_cap:
        imax = min(imax, imax_cap)
    results = []
    # factor window n, n-1, ..., n-imax+1
    fac = {}
    for t in range(imax):
        f = factor_or_none(n - t)
        fac[t] = f
        if f is None:
            print(f"  {tag} n={n}: t={t} ({n-t}) FACTORING FAILED -> UNKNOWN above i={t}")
            imax = t  # levels i <= t are still complete (they use t' < i <= t)
            break
    for i in range(1, imax + 1):
        adm = []
        for t in range(i):
            for q in fac[t]:
                if q > i:
                    adm.append((q, t))
        try:
            exc, cex = check_level(n, i, adm)
        except RuntimeError as e:
            results.append(("UNK", n, i, 0))
            print(f"  {tag} UNKNOWN at i={i}: {e}")
            continue
        for e in exc:
            results.append(("EXC",) + e)
            print(f"  {tag} EXC n={e[0]} i={e[1]} j={e[2]}")
        for c in cex:
            results.append(("CEX",) + c)
            print(f"  {tag} CEX n={c[0]} i={c[1]} j={c[2]} <-- COUNTEREXAMPLE")
    return g, imax, results


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "both"
    out = []
    if which in ("2k", "both"):
        print("=== family n = 2^k ===")
        for k in range(4, 65):
            n = 2 ** k
            g, imax, res = family_entry(n, f"2^{k}")
            status = "complete" if imax == min(g, n // 2 - 1) else f"partial<=i={imax}"
            print(f"2^{k}: g={g} swept_i<={imax} [{status}] " +
                  (f"hits={len(res)}" if res else "clean"))
            out.append((f"2^{k}", n, g, imax, status, res))
    if which in ("3m", "both"):
        print("=== family n = 3^m + 1 ===")
        for m in range(2, 41):
            n = 3 ** m + 1
            g, imax, res = family_entry(n, f"3^{m}+1")
            status = "complete" if imax == min(g, n // 2 - 1) else f"partial<=i={imax}"
            print(f"3^{m}+1: g={g} swept_i<={imax} [{status}] " +
                  (f"hits={len(res)}" if res else "clean"))
            out.append((f"3^{m}+1", n, g, imax, status, res))
    with open("family_census.csv", "w") as f:
        f.write("# family,n,g,imax_swept,status,hits\n")
        for tag, n, g, imax, status, res in out:
            f.write(f"{tag},{n},{g},{imax},{status},\"{res}\"\n")


if __name__ == "__main__":
    main()
