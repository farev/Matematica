#!/usr/bin/env python3
"""families.py — exact level-2/3 strict-failure decisions for the structured
families n = 2^k and n = 3^m + 1 of Erdos #699, at exponents far beyond any
sweep. Exact integer arithmetic throughout; deterministic.

Method (reductions R2/R5 + NOTE.md): at level i, witness primes are
T_i = {p prime > i : n mod p < i}; p^e || n - r (r = n mod p < i <= p) forces
any strict-failure j into residues {0..r} mod p^e with upper base-p digits
dominated by those of (n - r)/p^e.  For these n the windows are:
  n = 2^k:    level 2: odd primes of 2^k - 1 (r=1)
              level 3: primes > 3 of (2^k - 1) [r=1] and (2^{k-1}-1)·2 [r=2]
  n = 3^m+1:  level 2: p = 3 with 3^m || n-1 kills everything (lemma)
              level 3: primes > 3 of 3^m + 1 [r=0] and 3^m - 1 [r=2]
Candidates: greedy CRT over the largest prime powers until modulus > n/2
(then <= 1 candidate per residue combo); each candidate gets the full
domination test against every prime in T_i.  A level decision is only
reported when the relevant factorizations are COMPLETE; otherwise UNDECIDED
with the uncracked composite listed.

Factoring: cyclotomic split (Phi_d(b)), trial division to 1e6, BPSW
(gmpy2.is_prime, 40 extra MR rounds), perfect powers, deterministic Brent
rho (fixed c schedule, iteration cap).  Primality is probable-prime grade;
headline claims get separate certification.

Usage: families.py pow2 KMAX | pow3 MMAX
Output CSV to stdout: family,exp,level,status,detail
  status in {NONE, FAIL, UNDECIDED};  FAIL detail = j:saved_by
Cross-checks (run in __main__): L3 condition vs general checker at pow3.
"""
import sys
from math import gcd, prod
import gmpy2

# ---------- factoring ----------

def small_primes(lim):
    s = bytearray([1]) * lim
    s[0:2] = b"\x00\x00"
    for p in range(2, int(lim ** 0.5) + 1):
        if s[p]:
            s[p * p::p] = bytearray(len(s[p * p::p]))
    return [i for i in range(lim) if s[i]]

SP = small_primes(1000000)

def brent_rho(n, cap=2_000_000):
    """deterministic Brent rho: c = 1,2,3,...; returns factor or None."""
    n = int(n)
    for c in range(1, 20):
        y, m, g_, r, q = 2, 128, 1, 1, 1
        x = ys = y
        count = 0
        while g_ == 1 and count < cap:
            x = y
            for _ in range(r):
                y = (y * y + c) % n
            k = 0
            while k < r and g_ == 1:
                ys = y
                for _ in range(min(m, r - k)):
                    y = (y * y + c) % n
                    q = q * abs(x - y) % n
                g_ = gcd(q, n)
                k += m
                count += m
            r *= 2
        if g_ == n:
            g_ = 1
            while g_ == 1:
                ys = (ys * ys + c) % n
                g_ = gcd(abs(x - ys), n)
        if 1 < g_ < n:
            return g_
    return None

def factor(n, out=None, hard=None):
    """full factorization dict; uncracked composites appended to hard[]"""
    if out is None:
        out = {}
    if hard is None:
        hard = []
    if n == 1:
        return out, hard
    for p in SP:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        if p * p > n:
            break
    if n == 1:
        return out, hard
    if gmpy2.is_prime(gmpy2.mpz(n), 40):
        out[n] = out.get(n, 0) + 1
        return out, hard
    for e in range(2, 64):
        r, exact = gmpy2.iroot(gmpy2.mpz(n), e)
        if exact:
            f2, h2 = factor(int(r))
            for p, a in f2.items():
                out[p] = out.get(p, 0) + a * e
            hard.extend(h2)
            return out, hard
    d = brent_rho(n)
    if d is None:
        hard.append(n)
        return out, hard
    factor(d, out, hard)
    factor(n // d, out, hard)
    return out, hard

def cyclo_factor(b, sign, e):
    """factor b^e - 1 (sign=-1) or b^e + 1 (sign=+1) via cyclotomic split"""
    from sympy import totient, divisors
    from sympy.polys.specialpolys import cyclotomic_poly
    N = b ** e + (1 if sign > 0 else -1)
    if sign < 0:
        parts = [int(cyclotomic_poly(d, b)) for d in divisors(e)]
    else:
        parts = [int(cyclotomic_poly(d, b)) for d in divisors(2 * e) if (2 * e) % d == 0 and e % d != 0]
    assert prod(parts) == N, (b, sign, e)
    out, hard = {}, []
    for piece in parts:
        factor(piece, out, hard)
    return out, hard

# ---------- level check ----------

def dominated(p, n, j):
    while j:
        if j % p > n % p:
            return False
        j //= p
        n //= p
    return True

def div_binom(p, n, k):
    return not dominated(p, n, k)

def crt_pair(r1, m1, r2, m2):
    g_, x = m1, gmpy2.invert(m1 % m2, m2)
    return (r1 + m1 * ((int(x) * ((r2 - r1) % m2)) % m2)) % (m1 * m2)

def check_level(n, i, T):
    """T: list of (p, pe, r) witness primes > i, complete.
    Returns list of strict-failure j (each with saved-by-i flag)."""
    half = n // 2
    if not T:
        raise RuntimeError("empty T — refuse to enumerate")
    T = sorted(T, key=lambda t: -t[1])
    # greedy moduli until product > half
    mods = []
    M = 1
    for (p, pe, r) in T:
        mods.append((p, pe, r))
        M *= pe
        if M > half:
            break
    combos = prod(r + 1 for (_, _, r) in mods)
    walk = half // M + 1
    if combos * walk > 200000:
        raise RuntimeError(f"cannot bound candidates: combos={combos} walk={walk}")
    fails = []
    def emit(j0):
        j = j0
        while j <= half:
            if j > i and all(dominated(p, n, j) for (p, pe, r) in T):
                ip = gmpy2.is_prime(gmpy2.mpz(i)) if i > 1 else False
                saved = bool(ip and div_binom(i, n, i) and div_binom(i, n, j))
                fails.append((j, saved))
            j += M
    def rec(idx, rem, mod):
        if idx == len(mods):
            emit(rem)
            return
        p, pe, r = mods[idx]
        for b in range(r + 1):
            if idx == 0:
                rec(idx + 1, b, pe)
            else:
                rec(idx + 1, crt_pair(rem, mod, b, pe), mod * pe)
    rec(0, 0, 1)
    return sorted(set(fails))

def tlist(facs, r, i):
    return [(p, p ** e, r) for p, e in facs.items() if p > i]

def run_pow2(K):
    rows = []
    for k in range(3, K + 1):
        n = 2 ** k
        f1, h1 = cyclo_factor(2, -1, k)          # 2^k - 1, r = 1
        f2, h2 = cyclo_factor(2, -1, k - 1)      # 2^{k-1} - 1 (n-2 = 2*this), r = 2
        # level 2
        if h1:
            rows.append(("pow2", k, 2, "UNDECIDED", f"hard:{h1}"))
        else:
            fails = check_level(n, 2, tlist(f1, 1, 2))
            rows.append(("pow2", k, 2, "FAIL" if fails else "NONE",
                         ";".join(f"{j}:{'EXC' if s else 'CEX'}" for j, s in fails)))
        # level 3
        if h1 or h2:
            rows.append(("pow2", k, 3, "UNDECIDED", f"hard:{h1+h2}"))
        else:
            T = tlist(f1, 1, 3) + tlist(f2, 2, 3)
            fails = check_level(n, 3, T)
            rows.append(("pow2", k, 3, "FAIL" if fails else "NONE",
                         ";".join(f"{j}:{'EXC' if s else 'CEX'}" for j, s in fails)))
    return rows

def l3_condition(m):
    """Lemma L3 direct evaluation for (3^m+1, 3, (3^m+1)/2): returns
    (verdict, detail) where verdict True = strict failure (EXC)."""
    fm, hm = cyclo_factor(3, -1, m)
    fp, hp = cyclo_factor(3, +1, m)
    if hm or hp:
        return None, f"hard:{hm+hp}"
    for facs, N in ((fm, 3 ** m - 1), (fp, 3 ** m + 1)):
        for p, e in facs.items():
            if p <= 3:
                continue
            c = N // p ** e
            if not dominated(p, c, c // 2):
                return False, f"witness p={p}"
    return True, "all conditions hold"

def run_pow3(M):
    rows = []
    for m in range(2, M + 1):
        n = 3 ** m + 1
        fp, hp = cyclo_factor(3, +1, m)          # n itself (odd part etc.), r = 0
        fm, hm = cyclo_factor(3, -1, m)          # n - 2, r = 2
        # level 2: p=3 with 3^m || n-1: T includes (3, 3^m, 1) — dominates all
        T2 = tlist(fp, 0, 2) + [(3, 3 ** m, 1)]
        fails2 = check_level(n, 2, T2)
        rows.append(("pow3", m, 2, "FAIL" if fails2 else "NONE",
                     ";".join(f"{j}:{'EXC' if s else 'CEX'}" for j, s in fails2)))
        # level 3
        if hp or hm:
            rows.append(("pow3", m, 3, "UNDECIDED", f"hard:{hp+hm}"))
        else:
            T3 = tlist(fp, 0, 3) + tlist(fm, 2, 3)
            fails3 = check_level(n, 3, T3)
            rows.append(("pow3", m, 3, "FAIL" if fails3 else "NONE",
                         ";".join(f"{j}:{'EXC' if s else 'CEX'}" for j, s in fails3)))
            # cross-check against Lemma L3 (j = n/2 membership)
            l3, det = l3_condition(m)
            has_half = any(j == n // 2 for j, _ in fails3)
            if l3 is not None and l3 != has_half:
                print(f"L3-MISMATCH m={m}: lemma={l3} ({det}) checker={has_half}",
                      file=sys.stderr)
                sys.exit(9)
    return rows

if __name__ == "__main__":
    fam, X = sys.argv[1], int(sys.argv[2])
    rows = run_pow2(X) if fam == "pow2" else run_pow3(X)
    print("family,exp,level,status,detail")
    for r in rows:
        print(",".join(str(x) for x in r))
