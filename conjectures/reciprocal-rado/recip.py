#!/usr/bin/env python3
"""Reciprocal Rado numbers f_r(k), with certificates.

f_r(k) = least n such that every r-coloring of {1..n} has a monochromatic
solution of 1/x_1 + ... + 1/x_k = 1/x_{k+1}, the x_i not necessarily
distinct (Gaiser, Discrete Math 2024; Gaiser-Ramezanpour arXiv:2607.04373).

Solutions: since all terms are positive, 1/x_i < 1/y for every i, so every
x_i > y strictly. Canonical form: (y; x_1 <= ... <= x_k), all in [1, n].
Enumeration: exact-rational DFS with the standard Egyptian-fraction bounds
(at depth with j terms left and remainder a/b: x > b/a, x <= j*b/a).

Encoding (variables v(x,c) = (x-1)*r + c + 1, x in 1..n, c in 0..r-1):
  - at-least-one-color clause per integer;
  - for each solution's SUPPORT SET S = {y, x_1, ..., x_k} (deduplicated
    across solutions) and each color c: clause OR_{v in S} -v(v,c).
No at-most-one-color clauses: any satisfying assignment projects to a valid
coloring (mono solutions are forbidden in every color separately).

Pipeline per n: Cadical (no proof) for bracketing only; the claimed value
rests solely on the certified boundary pair:
  SAT at f-1  -> witness coloring, checked by verify_witness.py (independent
                 restricted-to-class enumeration, largest-first order)
  UNSAT at f  -> DRUP proof from Glucose 4.2.1, checked by tools/satcert/
                 rup_check (independent C RUP checker); big instances use
                 the standalone glucose_static binary (streams proof to disk).
"""
import sys, os, math, hashlib, subprocess, time
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
SATCERT = os.path.join(HERE, "..", "..", "tools", "satcert")
GLUCOSE_BIN = os.environ.get("GLUCOSE_BIN", "")  # standalone, optional


def solutions(k, n):
    """Yield every canonical solution (y, xs) with xs nondecreasing, k terms."""
    out = []
    def dfs(j, lo, a, b, prefix):
        # need sum of j unit fractions, each denom in [lo, n], equal to a/b
        if j == 1:
            if a > 0 and b % a == 0:
                x = b // a
                if lo <= x <= n:
                    out.append(prefix + (x,))
            return
        # x must satisfy 1/x < a/b (strict: j-1 positive terms remain)
        # and j/x >= a/b  =>  x <= j*b/a
        xlo = max(lo, b // a + 1)
        xhi = min(n, (j * b) // a)
        for x in range(xlo, xhi + 1):
            na, nb = a * x - b, b * x
            g = gcd(na, nb)
            dfs(j - 1, x, na // g, nb // g, prefix + (x,))
    res = []
    for y in range(1, n):
        out = []
        dfs(k, y + 1, 1, y, ())
        for xs in out:
            res.append((y, xs))
    return res


def support_sets(k, n):
    """Deduplicated support sets of all solutions; returns (sets, nsol)."""
    sols = solutions(k, n)
    seen = set()
    for y, xs in sols:
        seen.add(frozenset((y,) + xs))
    return [sorted(s) for s in seen], len(sols)


def encode(k, r, n):
    """Return (clauses, nvars, nsol, nsupp)."""
    v = lambda x, c: (x - 1) * r + c + 1
    cls = []
    for x in range(1, n + 1):
        cls.append([v(x, c) for c in range(r)])
    supps, nsol = support_sets(k, n)
    for S in supps:
        for c in range(r):
            cls.append([-v(x, c) for x in S])
    return cls, n * r, nsol, len(supps)


def write_cnf(cls, nvars, path):
    with open(path, "w") as f:
        f.write(f"p cnf {nvars} {len(cls)}\n")
        for c in cls:
            f.write(" ".join(map(str, c)) + " 0\n")
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    return h


def decide_fast(k, r, n):
    """Cadical, no proof: bracketing only."""
    from pysat.solvers import Cadical153
    cls, nv, _, _ = encode(k, r, n)
    with Cadical153(bootstrap_with=cls) as s:
        if s.solve():
            return True, extract(s.get_model(), r, n)
        return False, None


def extract(model, r, n):
    pos = set(l for l in model if l > 0)
    col = []
    for x in range(1, n + 1):
        for c in range(r):
            if (x - 1) * r + c + 1 in pos:
                col.append(c)
                break
        else:
            raise RuntimeError(f"integer {x} has no color in model")
    return col


def certify_unsat(k, r, n, workdir, tag, use_binary=False):
    """Glucose DRUP at n, checked by rup_check. Returns (cnf_sha, prooflines, secs)."""
    os.makedirs(workdir, exist_ok=True)
    cls, nv, nsol, nsupp = encode(k, r, n)
    cnff = os.path.join(workdir, f"{tag}.cnf")
    prf = os.path.join(workdir, f"{tag}.drup")
    sha = write_cnf(cls, nv, cnff)
    t0 = time.time()
    if use_binary:
        if not GLUCOSE_BIN:
            raise RuntimeError("GLUCOSE_BIN not set")
        p = subprocess.run([GLUCOSE_BIN, "-certified",
                            f"-certified-output={prf}", cnff],
                           capture_output=True, text=True)
        if "s UNSATISFIABLE" not in p.stdout:
            raise RuntimeError(f"expected UNSAT at n={n}: {p.stdout[-300:]}")
    else:
        from pysat.solvers import Glucose42
        with Glucose42(bootstrap_with=cls, with_proof=True) as s:
            if s.solve():
                raise RuntimeError(f"expected UNSAT at n={n}, got SAT")
            proof = s.get_proof()
        with open(prf, "w") as f:
            f.write("\n".join(proof) + ("\n" if proof else ""))
    secs = time.time() - t0
    chk = subprocess.run([os.path.join(SATCERT, "rup_check"), cnff, prf],
                         capture_output=True, text=True)
    if chk.returncode != 0:
        raise RuntimeError(f"RUP check FAILED for {prf}: {chk.stdout} {chk.stderr}")
    return sha, prf, secs, nsol, nsupp


def write_witness(col, k, r, n, path):
    with open(path, "w") as f:
        f.write(f"{n} {r} {k}\n")
        f.write(" ".join(map(str, col)) + "\n")


def find_f(k, r, workdir, tag, nstart=None, nmax=100000, verbose=True):
    """Exponential climb + bisection (Cadical), then certified boundary pair."""
    os.makedirs(workdir, exist_ok=True)
    lo, hi, wit = None, None, None       # lo: SAT, hi: UNSAT
    n = nstart or max(2, k)
    while n <= nmax:
        sat, col = decide_fast(k, r, n)
        if sat:
            lo, wit = n, col
            if verbose: print(f"  climb n={n}: SAT", flush=True)
            n *= 2
        else:
            hi = n
            if verbose: print(f"  climb n={n}: UNSAT", flush=True)
            break
    if hi is None:
        raise RuntimeError(f"no UNSAT up to {nmax}")
    while hi - (lo or 0) > 1:
        mid = ((lo or 0) + hi) // 2
        sat, col = decide_fast(k, r, mid)
        if sat:
            lo, wit = mid, col
        else:
            hi = mid
        if verbose: print(f"  bisect n={mid}: {'SAT' if sat else 'UNSAT'}", flush=True)
    # certified boundary pair
    wpath = os.path.join(workdir, f"{tag}_n{lo}.witness")
    write_witness(wit, k, r, lo, wpath)
    chk = subprocess.run([sys.executable, os.path.join(HERE, "verify_witness.py"),
                          wpath], capture_output=True, text=True)
    if "WITNESS OK" not in chk.stdout:
        raise RuntimeError(f"witness verification FAILED: {chk.stdout} {chk.stderr}")
    sha, prf, secs, nsol, nsupp = certify_unsat(k, r, hi, workdir, f"{tag}_n{hi}")
    return dict(k=k, r=r, f=hi, sat_at=lo, witness=wpath, cnf_sha=sha,
                proof=prf, unsat_secs=round(secs, 2), nsol=nsol, nsupp=nsupp)


if __name__ == "__main__":
    # CLI: recip.py k r n        -> decide one instance (fast, no proof)
    #      recip.py k r n --cert -> certified UNSAT at n
    #      recip.py k r --find   -> full certified boundary search
    k, r = int(sys.argv[1]), int(sys.argv[2])
    wd = os.path.join(HERE, "work")
    if "--find" in sys.argv:
        res = find_f(k, r, wd, f"f{r}_{k}")
        print(res)
    elif "--cert" in sys.argv:
        n = int(sys.argv[3])
        print(certify_unsat(k, r, n, wd, f"f{r}_{k}_n{n}",
                            use_binary="--binary" in sys.argv))
    else:
        n = int(sys.argv[3])
        sat, col = decide_fast(k, r, n)
        print("SAT" if sat else "UNSAT")
