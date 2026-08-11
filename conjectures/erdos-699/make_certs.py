#!/usr/bin/env python3
"""make_certs.py — build per-triple certificates and data/exceptions.csv
from the merged sweep output (EXC lines), recomputing everything from
scratch in exact integer arithmetic.

A certificate for an exceptional triple (n, i, j) contains:
  1. the weak witness p = i: i prime, n mod i^2 < i  (=> i | C(n,i), Lemma 6),
     and the base-i carry giving i | C(n,j), with v_i of both;
  2. the complete candidate list P = { p prime : p > i, p | C(n,i) }
     (= primes > i dividing n(n-1)...(n-i+1), Lemma 5), and for each
     p in P the base-p digit table of j against n witnessing NO carry
     (so p does not divide C(n,j)) — hence no prime > i divides the gcd;
  3. the gcd's full prime factorization (valuations of both binomials at
     every common prime), and for n <= 3000 the bigint gcd itself.

Everything is independently checkable line by line with Criterion K /
Legendre.  Usage:  python3 make_certs.py merged_exc.txt
"""
import sys, math, os


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


def factor(m):
    fs = {}
    d = 2
    while d * d <= m:
        while m % d == 0:
            fs[d] = fs.get(d, 0) + 1
            m //= d
        d += 1 if d == 2 else 2
    if m > 1:
        fs[m] = fs.get(m, 0) + 1
    return fs


def digits(m, p):
    ds = []
    while m:
        ds.append(m % p)
        m //= p
    return ds or [0]


def vp_binom(n, k, p):
    s = lambda m: sum(digits(m, p))
    return (s(k) + s(n - k) - s(n)) // (p - 1)


def carries_table(n, j, p):
    """list of (t, j mod p^t, n mod p^t, carry?) for p^t <= n"""
    rows = []
    pt = p
    while pt <= n:
        rows.append((pt, j % pt, n % pt, j % pt > n % pt))
        pt *= p
    return rows


def cert(n, i, j, outdir):
    assert 1 <= i < j <= n // 2
    lines = []
    add = lines.append
    add(f"# Certificate: exceptional triple (n, i, j) = ({n}, {i}, {j})")
    add(f"# Claim: no prime p > {i} divides gcd(C({n},{i}), C({n},{j})),")
    add(f"#        while p = {i} divides both (weak version holds).")
    add(f"# Checkable with Kummer's criterion: p | C(n,k) iff exists t:")
    add(f"#        k mod p^t > n mod p^t.   Generated 2026-08-11.")
    add("")
    # 1. weak witness
    assert is_prime(i), "exception must have i prime (Lemma 6)"
    r2 = n % (i * i)
    assert r2 < i, "Lemma 6 criterion fails?!"
    add(f"[weak witness p = i = {i}]")
    add(f"i is prime; n mod i^2 = {r2} < {i}  =>  i | C(n,i)   (Lemma 6)")
    vni, vnj = vp_binom(n, i, i), vp_binom(n, j, i)
    assert vni >= 1 and vnj >= 1
    add(f"v_{i}(C(n,i)) = {vni}, v_{i}(C(n,j)) = {vnj}  (Legendre)")
    add("")
    # 2. candidates and their misses
    window = {}
    for r in range(i):
        window[n - r] = factor(n - r)
    P = sorted({p for fs in window.values() for p in fs if p > i})
    add(f"[candidate primes p > {i} dividing C(n,i)]  (Lemma 5: primes > i")
    add(f" dividing the window n..n-i+1 = {[n - r for r in range(i)]})")
    add(f"P = {P}")
    for p in P:
        v = vp_binom(n, i, p)
        assert v >= 1, f"candidate {p} does not divide C(n,i)?!"
        tab = carries_table(n, j, p)
        assert not any(c for _, _, _, c in tab), f"{p} divides C(n,j)?!"
        add(f"  p = {p}: v_p(C(n,i)) = {v}; base-p check of j = {j} vs n:")
        for pt, jm, nm, _ in tab:
            add(f"      t: p^t = {pt:<12}  j mod p^t = {jm:<12} <= "
                f"{nm:<12} = n mod p^t   (no carry)")
        add(f"    => p = {p} does NOT divide C(n,j); not in gcd.")
    add("")
    # 3. gcd factorization
    add("[gcd factorization]")
    com = []
    lim = max(P, default=i) if n > 3000 else n
    # all common primes are <= n; enumerate primes dividing C(n,i):
    # p <= i primes must be checked too
    smallp = [p for p in range(2, i + 1) if is_prime(p)]
    for p in smallp + P:
        a, b = vp_binom(n, i, p), vp_binom(n, j, p)
        if a >= 1 and b >= 1:
            com.append((p, min(a, b)))
            add(f"  common prime {p}: v_p(C(n,i)) = {a}, v_p(C(n,j)) = {b}"
                f" -> v_p(gcd) = {min(a, b)}")
    # primes in (i, n] not dividing C(n,i) cannot be in the gcd; P covers
    # the rest (Lemma 5).  For n <= 3000, verify with bigints:
    if n <= 3000:
        g = math.gcd(math.comb(n, i), math.comb(n, j))
        gg = 1
        for p, e in com:
            gg *= p**e
        assert g == gg, f"bigint gcd mismatch: {g} vs {gg}"
        add(f"  bigint check: gcd = {g} = "
            + "*".join(f"{p}^{e}" for p, e in com) + "   AGREES")
    else:
        add("  (n > 3000: bigint check skipped; Lemma 5 + tables above are")
        add("   the certificate that no other prime is common)")
    mx = max((p for p, _ in com), default=0)
    assert mx == i, f"largest common prime is {mx}, expected i = {i}"
    add(f"  largest common prime = {i} = i   (exception confirmed)")
    fn = os.path.join(outdir, f"EXC_{n}_{i}_{j}.txt")
    with open(fn, "w") as f:
        f.write("\n".join(lines) + "\n")
    return com


def main():
    src = sys.argv[1]
    triples = []
    for line in open(src):
        parts = line.split()
        if parts and parts[0] == "EXC":
            triples.append(tuple(map(int, parts[1:4])))
    triples = sorted(set(triples))
    os.makedirs("certs", exist_ok=True)
    rows = ["n,i,j,gcd_factorization,family"]
    for n, i, j in triples:
        com = cert(n, i, j, "certs")
        fac = "*".join(f"{p}^{e}" if e > 1 else str(p) for p, e in com)
        fam = ""
        if i == 2 and (n & (n - 1)) == 0:
            fam = f"2^{n.bit_length()-1}"
        elif i == 3:
            m = 0
            t = n - 1
            while t % 3 == 0:
                t //= 3
                m += 1
            if t == 1:
                fam = f"3^{m}+1"
        rows.append(f"{n},{i},{j},{fac},{fam}")
        print(f"certified ({n},{i},{j}): gcd = {fac}  {fam}")
    with open("data/exceptions.csv", "w") as f:
        f.write("\n".join(rows) + "\n")
    print(f"{len(triples)} certificates in certs/, table in data/exceptions.csv")


if __name__ == "__main__":
    main()
