#!/usr/bin/env python3
"""Exhaustive branch-and-bound over sets of distinct primes 3 <= p1 < ... < pm
(or 2 <= p1 < ... in --parity all) satisfying

    1/p1 + ... + 1/pm + eps/(p1*...*pm) = 1,      eps in {-1, +1}.

eps = -1 : Giuga numbers with sum - prod = 1  (all known Giuga numbers).
eps = +1 : primary pseudoperfect numbers / all-prime improper-Znam solutions.

Every quantity in the critical path is an exact integer (gmpy2.mpz).
Maintained per node: the chosen prefix, P = prod(p_i), A = sum(P/p_i).
Then s = A/P is the exact reciprocal sum and the full equation for a
completed set is the integer identity  A + eps == P.

Window bounds are SUPERSETS of feasibility (padded floors/ceils); every
candidate inside a window is decided by exact per-candidate checks, so the
bounds only control cost, never soundness.  Primality uses gmpy2.is_prime
(trial division + Miller-Rabin): a "composite" verdict is a proof, so
pruning on it never discards a true prime; a false "prime" verdict can only
create a spurious candidate, which the final exact identity A + eps == P
and the independent verifier (verify_solution.py) screen.  Solutions found
are therefore verified; exhaustion is sound.

Derivation of the node algebra (proofs in NOTE.md):
  deficit D = P - A must satisfy D >= 1 at every internal node.
  t = 1 remaining prime:  p = (P + eps)/D exactly.
  t = 2 remaining (q < r): (D*q - P)*(D*r - P) = P*P + eps*D =: Nstar,
      with u = D*q - P >= 1, hence P/D < q <= (P + sqrt(Nstar))/D and
      r = (P*q + eps)/u.
  t >= 3: next prime p obeys 1/p < D/P + 1/(3P) and t/p > D/P - 1/(3P)
      (the eps-term of any completion lies in (0, 1/(3P))), giving
      3P/(3D+1) < p < 3Pt/(3D-1); for eps = +1 also p > P/D, for
      eps = -1 also p < tP/D + 1.

Exit codes: 0 run COMPLETE, 3 run INCOMPLETE (budget), 1 error.
"""
import argparse
import hashlib
import json
import multiprocessing as mp
import os
import sys
import time

import numpy as np
import gmpy2
from gmpy2 import mpz, isqrt, is_prime, next_prime

# ---------------------------------------------------------------- constants
WALK_CAP = 200_000           # below this window width: next_prime walk
SIEVE_CAP = 4_000_000_000    # below this width: rough segmented sieve
SIEVE_CHUNK = 200_000_000    # sieve segment size (memory bound)
SIEVE_BASE = 1_000_000       # base primes for the rough sieve
FACTOR_DIGITS_CAP = 46       # divisor route only when Nstar has <= this many digits
SIEVE_FAST_CAP = 1_500_000_000   # sieve first below this width (~100 s worst)
DIVISOR_TIME_CAP = 300       # seconds for factoring one Nstar (first try)
DIVISOR_TIME_CAP_LAST = 900  # last-resort factoring of huge-window nodes
DIVISOR_COUNT_CAP = 2_000_000    # refuse divisor enumeration beyond this
ONE = mpz(1)

_base_primes = None


def base_primes():
    """primes 3..SIEVE_BASE as int64 (rough-sieve base; module-level cache)"""
    global _base_primes
    if _base_primes is None:
        n = SIEVE_BASE
        mask = np.ones(n + 1, dtype=bool)
        mask[:2] = False
        for p in range(2, int(n ** 0.5) + 1):
            if mask[p]:
                mask[p * p::p] = False
        _base_primes = np.nonzero(mask)[0][1:].astype(np.int64)  # drop 2
    return _base_primes


def rough_chunks(lo, hi):
    """uint64 arrays of odd integers in [lo, hi] (requires hi < 2^64) with
    no prime factor <= SIEVE_BASE, plus any base primes inside the window.
    Superset of the primes in the window; every survivor is screened
    exactly downstream.  Segmented into SIEVE_CHUNK-wide slabs."""
    lo = max(int(lo), 3)
    hi = int(hi)
    if lo % 2 == 0:
        lo += 1
    seg_lo = lo
    bp = base_primes()
    while seg_lo <= hi:
        seg_hi = min(seg_lo + 2 * (SIEVE_CHUNK - 1), hi)
        count = (seg_hi - seg_lo) // 2 + 1     # odds seg_lo, ..., <= seg_hi
        mask = np.ones(count, dtype=bool)
        for p in bp:
            p = int(p)
            if p * p > seg_hi:
                break
            start = ((seg_lo + p - 1) // p) * p    # first multiple >= seg_lo
            if start % 2 == 0:
                start += p
            if start == p:                     # p itself in window: keep it
                start += 2 * p
            if start > seg_hi:
                continue
            mask[(start - seg_lo) // 2::p] = False
        yield np.uint64(seg_lo) + 2 * np.nonzero(mask)[0].astype(np.uint64)
        seg_lo = seg_hi + 2


# --------------------------------------------------------------- C kernel
_KLIB = None
KERNEL_CHUNK = 500_000_000
KERNEL_OUTCAP = 4096
# The kernel is exact whenever every intermediate fits its types:
#   Nstar = P^2 + eps*D < 2^128  (holds for P < 2^64),
#   u <= isqrt(Nstar) + D + 1 <= P + D + 2 < 2^64  (the U cap below),
#   q0 and q_hi as uint64.
KERNEL_U_CAP = 1 << 64
KERNEL_Q_CAP = 1 << 64


def kernel_lib():
    global _KLIB
    if _KLIB is None:
        import ctypes
        here = os.path.dirname(os.path.abspath(__file__))
        so = os.path.join(here, "kernel.so")
        src = os.path.join(here, "kernel.c")
        if (not os.path.exists(so)
                or os.path.getmtime(so) < os.path.getmtime(src)):
            import subprocess
            subprocess.run(["gcc", "-O2", "-shared", "-fPIC", "-o", so, src],
                           check=True)
        lib = ctypes.CDLL(so)
        for fn in ("t2_scan", "t2_scan2"):
            f = getattr(lib, fn)
            f.argtypes = [ctypes.c_uint64] * 7 + [
                ctypes.c_long, ctypes.POINTER(ctypes.c_long), ctypes.c_long]
            f.restype = ctypes.c_long
        _KLIB = lib
    return _KLIB


def _split64(x):
    return (int(x) >> 64) & ((1 << 64) - 1), int(x) & ((1 << 64) - 1)


FLINT_DIGITS_CAP = 52        # in-process flint factoring below this size


def factor_flint(n):
    """Full factorization via FLINT (C, fast qsieve). Verified here like
    factor_subprocess: wrong output can only become None, never wrong
    divisors. Returns {prime: exp} or None."""
    try:
        import flint
    except ImportError:
        return None
    try:
        res = flint.fmpz(n).factor()
    except Exception:                           # noqa: BLE001
        return None
    fac = {mpz(int(p)): int(e) for p, e in res}
    check = mpz(1)
    for p, e in fac.items():
        if not is_prime(p):
            return None
        check *= p ** e
    if check != n:
        return None
    return fac


def factor_subprocess(n, timeout):
    """Full factorization of n via sympy in a killable subprocess.
    Returns {prime: exponent} or None on timeout/failure.  The result is
    verified here (product check + primality of each factor), so a wrong
    or partial factorization can only become None, never wrong divisors."""
    import subprocess
    code = ("import sys,json\n"
            "n = int(sys.argv[1])\n"
            "try:\n"
            "    import flint\n"
            "    fac = {str(int(p)): int(e) for p, e in flint.fmpz(n).factor()}\n"
            "except Exception:\n"
            "    from sympy import factorint\n"
            "    fac = {str(k): v for k, v in factorint(n).items()}\n"
            "print(json.dumps(fac))")
    try:
        cp = subprocess.run([sys.executable, "-c", code, str(n)],
                            capture_output=True, timeout=timeout, text=True)
    except subprocess.TimeoutExpired:
        return None
    if cp.returncode != 0:
        return None
    try:
        fac = {mpz(k): int(v) for k, v in json.loads(cp.stdout).items()}
    except Exception:                           # noqa: BLE001
        return None
    check = mpz(1)
    for p, e in fac.items():
        if not is_prime(p):
            return None
        check *= p ** e
    if check != n:
        return None
    return fac


class Budget(Exception):
    pass


FIELDS = ("nodes", "t1", "t2", "t2_walked", "t2_sieved", "t2_kernel",
          "t2_width_sum", "t2_width_max", "divisor_nodes", "deepest")


class Stats:
    __slots__ = FIELDS + ("hard", "solutions", "bpsw_factors")

    def __init__(self):
        for f in FIELDS:
            setattr(self, f, 0)
        self.hard = []          # nodes that could not be exhausted
        self.solutions = []     # list of tuples of primes
        self.bpsw_factors = []  # divisor-route factors >= 2^64 (probable
        #                         primes only: divisor completeness at such
        #                         nodes rests on BPSW+MR; disclosed per run)

    def as_dict(self):
        d = {f: getattr(self, f) for f in FIELDS}
        d["hard"] = self.hard
        d["solutions"] = self.solutions
        d["bpsw_factors"] = self.bpsw_factors
        return d

    def merge_dict(self, d):
        for f in FIELDS:
            if f in ("t2_width_max", "deepest"):
                setattr(self, f, max(getattr(self, f), d[f]))
            else:
                setattr(self, f, getattr(self, f) + d[f])
        self.hard += d["hard"]
        self.solutions += [tuple(s) for s in d["solutions"]]
        self.bpsw_factors += d["bpsw_factors"]


def record_solution(stats, primes):
    """Final exact screen: the integer identity A + eps == P (recomputed
    from scratch here, independently of the incremental bookkeeping)."""
    P = mpz(1)
    for p in primes:
        P *= p
    A = sum(P // p for p in primes)
    return P, A


def close_t1(P, A, D, last, eps, parity_odd, prefix, stats):
    stats.t1 += 1
    num = P + eps
    if num % D:
        return
    p = num // D
    if p <= last:
        return
    if parity_odd and p % 2 == 0:
        return
    if not is_prime(p):
        return
    sol = prefix + (int(p),)
    Pf, Af = record_solution(stats, [mpz(x) for x in sol])
    if Af + eps == Pf:
        stats.solutions.append(sol)
    # else: spurious candidate from a pseudoprime; dropped, and the
    # discrepancy would be visible in verify_solution.py replays.


def close_t2(P, A, D, last, eps, parity_odd, prefix, stats):
    """Enumerate q in (P/D, (P+sqrt(Nstar))/D], r determined.

    Three tiers by window width: next_prime walk; rough segmented sieve
    with the exact divisibility test u | Pq+eps applied to every candidate
    (a composite q surviving the sieve is eliminated there or by the final
    is_prime); divisor enumeration of Nstar = (Dq-P)(Dr-P) after factoring.
    """
    stats.t2 += 1
    Nstar = P * P + eps * D
    if Nstar <= 0:
        return
    q_lo = max(mpz(last), P // D - 1)          # exclusive lower iteration edge
    q_hi = (P + isqrt(Nstar)) // D + 1         # padded inclusive upper edge
    if q_hi <= q_lo:
        return
    width = int(q_hi - q_lo)
    stats.t2_width_sum += width
    if width > stats.t2_width_max:
        stats.t2_width_max = width

    def try_q(q, check_q_prime):
        u = D * q - P
        if u <= 0:
            return
        num = P * q + eps
        if num % u:
            return
        if check_q_prime and not is_prime(q):
            return
        r = num // u
        if r <= q:
            return
        if parity_odd and r % 2 == 0:
            return
        if not is_prime(r):
            return
        sol = prefix + (int(q), int(r))
        Pf, Af = record_solution(stats, [mpz(x) for x in sol])
        if Af + eps == Pf:
            stats.solutions.append(sol)

    if width <= 20_000 or q_lo < 10:
        stats.t2_walked += 1
        q = next_prime(q_lo)
        while q <= q_hi:
            if not (parity_odd and q % 2 == 0):
                try_q(q, False)
            q = next_prime(q)
        return

    if q_hi < KERNEL_Q_CAP and P + 2 * D + 2 < KERNEL_U_CAP:
        # C kernel: scan every odd q, keep q with (Dq-P) | Nstar
        stats.t2_kernel += 1
        import ctypes
        lib = kernel_lib()
        scan = lib.t2_scan if os.environ.get("KERNEL_V1") else lib.t2_scan2
        out = (ctypes.c_long * KERNEL_OUTCAP)()
        n_hi, n_lo = _split64(Nstar)
        d_hi, d_lo = _split64(D)
        p_hi, p_lo = _split64(P)
        q = int(q_lo) + 1
        if q % 2 == 0:
            q += 1
        end = int(q_hi)
        while q <= end:
            cnt = min((end - q) // 2 + 1, KERNEL_CHUNK)
            got = scan(n_hi, n_lo, d_hi, d_lo, p_hi, p_lo,
                       q, cnt, out, KERNEL_OUTCAP)
            if got < 0:                      # out buffer overflow: rescan
                stats.hard.append({"prefix": [int(x) for x in prefix],
                                   "P": str(P), "D": str(D),
                                   "err": "kernel outcap overflow"})
                return
            for i in range(got):
                try_q(mpz(q + 2 * out[i]), True)
            q += 2 * cnt
        return

    def sieve_pass():
        # exact test per candidate: u | Pq+eps  <=>  u | Nstar
        # (valid because gcd(u, D) = gcd(P, D) = gcd(P, A) = 1: each prefix
        # prime p_i divides P but A = sum P/p_j = prod_{j != i} p_j (mod p_i)
        # is nonzero mod p_i).  Vectorized wheel: for a small prime p with
        # p ∤ Nstar and p ∤ D, the q with p | u form the single residue
        # class q ≡ P·D^{-1} (mod p); those u can never divide Nstar.
        # (p | D would need p | P for a kill — impossible, gcd(P, D) = 1.)
        stats.t2_sieved += 1
        excl = []
        for sp in (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47,
                   53, 59, 61):
            if Nstar % sp and D % sp:
                cls = (int(P) % sp) * pow(int(D) % sp, -1, sp) % sp
                excl.append((np.uint64(sp), np.uint64(cls)))
        for arr in rough_chunks(int(q_lo) + 1, int(q_hi)):
            for sp, cls in excl:
                arr = arr[arr % sp != cls]
            for qi in arr.tolist():
                q = mpz(qi)
                u = D * q - P
                if u > 0 and Nstar % u == 0:
                    try_q(q, True)

    def divisor_pass(cap=DIVISOR_TIME_CAP):
        stats.divisor_nodes += 1
        if Nstar.num_digits() <= FLINT_DIGITS_CAP:
            fac = factor_flint(int(Nstar))
        else:
            fac = factor_subprocess(int(Nstar), cap)
        if fac is None:
            return False
        ndiv = 1
        for ex in fac.values():
            ndiv *= ex + 1
        if ndiv > DIVISOR_COUNT_CAP:
            return False
        for pr in fac:
            if pr >> 64:
                stats.bpsw_factors.append(str(pr))
        divs = [mpz(1)]
        for pr, ex in fac.items():
            pr = mpz(pr)
            divs = [d * pr**k for d in divs for k in range(ex + 1)]
        for u in divs:
            if u * u > Nstar:
                continue
            if (u + P) % D:
                continue
            q = (u + P) // D
            if q <= last or q > q_hi:
                continue
            if parity_odd and q % 2 == 0:
                continue
            if not is_prime(q):
                continue
            try_q(q, False)
        return True

    # python tiers: with FLINT, factoring Nstar (<= ~52 digits here) costs
    # ~10-500 ms regardless of window width, so the divisor route leads;
    # the bounded sieve is the fallback when a factorization fails
    if Nstar.num_digits() <= FLINT_DIGITS_CAP and divisor_pass():
        return
    if width <= SIEVE_CAP and q_hi < (1 << 64):
        sieve_pass()
        return
    if divisor_pass(DIVISOR_TIME_CAP_LAST):
        return
    stats.hard.append({"prefix": [int(x) for x in prefix],
                       "P": str(P), "D": str(D), "width": width,
                       "err": "window beyond sieve cap; Nstar unfactored"})


def t3_window(P, D, t, last, eps):
    """superset window (lo_exclusive, hi_inclusive) for the next prime"""
    lo = (3 * P) // (3 * D + 1)                # p > 3P/(3D+1)
    if eps > 0:
        lo = max(lo, P // D)                   # p > P/D
    hi = (3 * P * t) // (3 * D - 1) + 1        # p < 3Pt/(3D-1), padded
    if eps < 0:
        hi = min(hi, (t * P) // D + 1)         # p < tP/D, padded
    return max(mpz(last), lo), hi


def iter_primes(lo, hi, parity_odd):
    """primes p with lo < p <= hi (probable primes: never misses a true
    prime; a rare pseudoprime yield is screened downstream)"""
    if hi <= lo:
        return
    if int(hi - lo) <= WALK_CAP or lo < 10:
        p = next_prime(lo)
        while p <= hi:
            if not (parity_odd and p % 2 == 0):
                yield p
            p = next_prime(p)
        return
    if int(hi - lo) > SIEVE_CAP or hi >= (1 << 64):
        raise WideWindow(int(hi - lo))
    for arr in rough_chunks(int(lo) + 1, int(hi)):
        for c in arr.tolist():
            cm = mpz(c)
            if is_prime(cm):
                yield cm


class WideWindow(Exception):
    pass


def recurse(P, A, last, t, eps, parity_odd, prefix, stats, budget):
    stats.nodes += 1
    if budget and stats.nodes > budget:
        raise Budget()
    if len(prefix) > stats.deepest:
        stats.deepest = len(prefix)
    D = P - A
    if D <= 0:
        return
    if t == 1:
        close_t1(P, A, D, last, eps, parity_odd, prefix, stats)
        return
    if t == 2:
        close_t2(P, A, D, last, eps, parity_odd, prefix, stats)
        return
    lo, hi = t3_window(P, D, t, last, eps)
    try:
        for p in iter_primes(lo, hi, parity_odd):
            recurse(P * p, A * p + P, p, t - 1, eps, parity_odd,
                    prefix + (int(p),), stats, budget)
    except WideWindow as w:
        stats.hard.append({"prefix": [int(x) for x in prefix], "t": t,
                           "P": str(P), "D": str(D),
                           "err": f"t3 window width {w.args[0]}"})


# ------------------------------------------------------------ parallel split
def frontier(m, eps, parity_odd, depth):
    """Enumerate all window-feasible prefixes of length `depth` (same bounds
    as recurse, no closures), for distribution to workers."""
    out = []

    def go(P, A, last, t, prefix):
        if len(prefix) == depth or t <= 2:
            out.append((str(P), str(A), str(last), t, prefix))
            return
        D = P - A
        if D <= 0:
            return
        lo, hi = t3_window(P, D, t, last, eps)
        try:
            for p in iter_primes(lo, hi, parity_odd):
                go(P * p, A * p + P, p, t - 1, prefix + (int(p),))
        except WideWindow:
            # unexpectedly wide window at shallow depth: hand the whole
            # node to a worker, which will re-derive and ledger it
            out.append((str(P), str(A), str(last), t, prefix))

    go(mpz(1), mpz(0), mpz(1), m, ())
    return out


def worker(job):
    Pstr, Astr, last, t, prefix, eps, parity_odd, budget = job
    stats = Stats()
    complete = True
    try:
        recurse(mpz(Pstr), mpz(Astr), mpz(last), t, eps, parity_odd,
                tuple(prefix), stats, budget)
    except Budget:
        complete = False
    d = stats.as_dict()
    d["complete"] = complete
    d["unit"] = list(prefix)
    return d


def run_m(m, eps, parity, jobs, budget, split_depth, resume=None):
    parity_odd = parity == "odd"
    t0 = time.time()
    stats = Stats()
    complete = True
    if jobs <= 1 or m <= min(split_depth + 2, 7):
        try:
            recurse(mpz(1), mpz(0), mpz(1), m, eps, parity_odd, (),
                    stats, budget)
        except Budget:
            complete = False
    else:
        units = frontier(m, eps, parity_odd, split_depth)
        # heaviest subtrees first: cost grows as the deficit shrinks
        units.sort(key=lambda u: (mpz(u[0]) - mpz(u[1])) / mpz(u[0])
                   if mpz(u[0]) > 0 else 1)
        done = {}
        if resume and os.path.exists(resume):
            with open(resume) as f:
                for line in f:
                    rec = json.loads(line)
                    if (rec.get("engine") == engine_sha()
                            and rec["m"] == m and rec["eps"] == eps
                            and rec["parity"] == parity):
                        done[tuple(rec["unit"])] = rec
        for key, rec in done.items():
            complete &= rec["complete"]
            stats.merge_dict(rec["stats"])
        jobs_list = [(P, A, last, t, prefix, eps, parity_odd, budget)
                     for (P, A, last, t, prefix) in units
                     if tuple(prefix) not in done]
        total = len(units)
        done_n = len(done)
        with mp.Pool(jobs) as pool:
            for d in pool.imap_unordered(worker, jobs_list, chunksize=1):
                c = d.pop("complete")
                unit = d.pop("unit")
                complete &= c
                stats.merge_dict(d)
                done_n += 1
                if resume:
                    with open(resume, "a") as f:
                        f.write(json.dumps(
                            {"engine": engine_sha(), "m": m, "eps": eps,
                             "parity": parity, "unit": unit,
                             "complete": c, "stats": d}) + "\n")
                if done_n % 200 == 0:
                    print(f"# progress {done_n}/{total} units, "
                          f"nodes={stats.nodes} t={time.time()-t0:.0f}s",
                          file=sys.stderr, flush=True)
    if stats.hard:
        complete = False
    return {
        "m": m, "eps": eps, "parity": parity,
        "complete": complete,
        "solutions": sorted({int_prod(s) for s in stats.solutions}),
        "solution_sets": sorted({tuple(sorted(s)) for s in stats.solutions}),
        "nodes": stats.nodes, "t1_closures": stats.t1,
        "t2_closures": stats.t2, "t2_walked": stats.t2_walked,
        "t2_sieved": stats.t2_sieved, "t2_kernel": stats.t2_kernel,
        "t2_width_sum": stats.t2_width_sum,
        "t2_width_max": stats.t2_width_max,
        "divisor_nodes": stats.divisor_nodes, "hard_nodes": stats.hard,
        "bpsw_factors": stats.bpsw_factors,
        "deepest": stats.deepest,
        "walltime_s": round(time.time() - t0, 3),
    }


def int_prod(s):
    P = 1
    for p in s:
        P *= p
    return P


def _sha16(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:16]


# captured at import so a mid-run edit of the sources cannot relabel a
# running job's record (recompile-mid-run defect class, 2026-08-13 log)
_ENGINE_SHA = _sha16(os.path.abspath(__file__))
_here = os.path.dirname(os.path.abspath(__file__))
_KERNEL_SHA = (_sha16(os.path.join(_here, "kernel.c"))
               if os.path.exists(os.path.join(_here, "kernel.c")) else "none")


def engine_sha():
    return _ENGINE_SHA + "+" + _KERNEL_SHA


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eps", type=int, choices=[-1, 1], required=True)
    ap.add_argument("--parity", choices=["odd", "all"], required=True)
    ap.add_argument("--m", type=int, required=True, help="exact factor count")
    ap.add_argument("--mmax", type=int, default=None,
                    help="run m..mmax inclusive")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--budget", type=int, default=0,
                    help="per-worker node budget, 0 = unlimited")
    ap.add_argument("--split-depth", type=int, default=3)
    ap.add_argument("--out", default=None, help="append JSONL here")
    ap.add_argument("--resume", default=None,
                    help="per-unit progress file: completed units are "
                         "recorded here and skipped on restart (same "
                         "engine hash required)")
    args = ap.parse_args()

    mmax = args.mmax or args.m
    ok = True
    for m in range(args.m, mmax + 1):
        rec = run_m(m, args.eps, args.parity, args.jobs, args.budget,
                    args.split_depth, resume=args.resume)
        rec["engine_sha"] = engine_sha()
        line = json.dumps(rec)
        print(line, flush=True)
        if args.out:
            with open(args.out, "a") as f:
                f.write(line + "\n")
        ok &= rec["complete"]
    sys.exit(0 if ok else 3)


if __name__ == "__main__":
    main()
