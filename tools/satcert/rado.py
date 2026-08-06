#!/usr/bin/env python3
"""Exact k-color Rado numbers for linear equations, with certificates.

An equation is given as (coeffs, const): sum(coeffs[i]*x_i) + const = 0,
x_i in {1..n}. The k-color Rado number R_k(E) is the least n such that every
k-coloring of {1..n} contains a monochromatic solution (x_1,...,x_m) of E.
`nontrivial` controls which solutions count:
  - "all": every solution counts (Schur convention: x+y=z allows x=y)
  - "not_all_equal": solutions with all variables equal are ignored
  - "distinct": only solutions with pairwise distinct values count

Pipeline per n: CNF encode -> Glucose42.
  SAT   -> witness coloring (verified later by independent C checker)
  UNSAT -> DRUP proof, checked by rup_check (independent C RUP checker)

Variables: v(x, j) = (x-1)*k + j + 1, x in 1..n, j in 0..k-1.
No at-most-one-color clauses: any satisfying assignment projects to a valid
coloring (choose any true color per integer; mono solutions are forbidden in
every color separately, so the projection avoids them too).
"""
import sys, itertools, subprocess, os
from pysat.formula import CNF
from pysat.solvers import Glucose42, Cadical153, Minisat22


def solutions(coeffs, const, n, nontrivial):
    """Yield all solutions (x_1..x_m) in {1..n}^m of sum a_i x_i + c = 0."""
    m = len(coeffs)
    # brute force over first m-1 vars, solve for last: fine for m <= 4.
    am = coeffs[-1]
    for pre in itertools.product(range(1, n + 1), repeat=m - 1):
        s = sum(a * x for a, x in zip(coeffs, pre)) + const
        # am * xm = -s
        if am != 0 and (-s) % am == 0:
            xm = (-s) // am
            if 1 <= xm <= n:
                sol = pre + (xm,)
                if nontrivial == "not_all_equal" and len(set(sol)) == 1:
                    continue
                if nontrivial == "distinct" and len(set(sol)) != len(sol):
                    continue
                yield sol


def encode(coeffs, const, k, n, nontrivial):
    v = lambda x, j: (x - 1) * k + j + 1
    cnf = CNF()
    for x in range(1, n + 1):
        cnf.append([v(x, j) for j in range(k)])
    nsol = 0
    for sol in solutions(coeffs, const, n, nontrivial):
        nsol += 1
        xs = sorted(set(sol))
        for j in range(k):
            cnf.append([-v(x, j) for x in xs])
    return cnf, nsol


def decide(coeffs, const, k, n, nontrivial, workdir, tag, proof=True):
    """Return ('SAT', coloring) or ('UNSAT', prooffile). Coloring is list of
    color indices for 1..n."""
    cnf, nsol = encode(coeffs, const, k, n, nontrivial)
    with Glucose42(bootstrap_with=cnf, with_proof=proof) as s:
        sat = s.solve()
        if sat:
            model = set(l for l in s.get_model() if l > 0)
            col = []
            for x in range(1, n + 1):
                for j in range(k):
                    if (x - 1) * k + j + 1 in model:
                        col.append(j)
                        break
                else:
                    raise RuntimeError("integer with no color in model")
            return "SAT", col, nsol
        pf = s.get_proof() if proof else None
    if proof:
        cnff = os.path.join(workdir, f"{tag}.cnf")
        prf = os.path.join(workdir, f"{tag}.drup")
        cnf.to_file(cnff)
        with open(prf, "w") as f:
            f.write("\n".join(pf) + ("\n" if pf else ""))
        return "UNSAT", (cnff, prf), nsol
    return "UNSAT", None, nsol


def rado(coeffs, const, k, nontrivial, workdir, tag, nmax=20000, verbose=True):
    """Find R_k(E) by increasing n from the first SAT-relevant point."""
    n = 1
    last_witness = None
    while n <= nmax:
        res, payload, nsol = decide(coeffs, const, k, n, nontrivial, workdir,
                                    f"{tag}_n{n}", proof=True)
        if res == "SAT":
            last_witness = (n, payload)
            # jump: a good coloring of [1..n] restricts to [1..n'] for n'<n,
            # so R > n. Increment.
            n += 1
        else:
            cnff, prf = payload
            chk = subprocess.run(["./rup_check", cnff, prf],
                                 capture_output=True, text=True)
            ok = chk.returncode == 0
            if verbose:
                print(f"  n={n}: UNSAT ({nsol} solution tuples); "
                      f"RUP check: {'VERIFIED' if ok else 'FAILED'}")
            if not ok:
                raise RuntimeError(f"RUP check failed for {prf}: {chk.stderr}")
            return n, last_witness
    raise RuntimeError(f"no UNSAT up to nmax={nmax}")


def decide_fast(coeffs, const, k, n, nontrivial):
    """Cadical, no proof: for bracketing only. Returns True iff SAT."""
    cnf, _ = encode(coeffs, const, k, n, nontrivial)
    with Cadical153(bootstrap_with=cnf) as s:
        return s.solve()


def rado_fast(coeffs, const, k, nontrivial, workdir, tag, nstart=4,
              nmax=200000, verbose=True):
    """Exponential climb + bisection with a fast solver, then certify only
    the boundary: SAT witness at R-1, DRUP-checked UNSAT at R.
    Correctness rests solely on the boundary certificates plus monotonicity
    (a good coloring of [1..n] restricts to [1..n']), not on the bracketing
    solver."""
    lo, hi = None, None            # lo: known SAT, hi: known UNSAT
    n = nstart
    while n <= nmax:
        if decide_fast(coeffs, const, k, n, nontrivial):
            lo = n
            n *= 2
        else:
            hi = n
            break
        if verbose:
            print(f"  climb: n={lo} SAT")
    if hi is None:
        raise RuntimeError(f"no UNSAT up to nmax={nmax}")
    if verbose:
        print(f"  bracket: SAT at {lo}, UNSAT at {hi}")
    while hi - (lo or 0) > 1:
        mid = ((lo or 0) + hi) // 2
        if decide_fast(coeffs, const, k, mid, nontrivial):
            lo = mid
        else:
            hi = mid
        if verbose:
            print(f"  bisect: [{lo}, {hi}]")
    R = hi
    # certify boundary
    res, col, nsol = decide(coeffs, const, k, R - 1, nontrivial, workdir,
                            f"{tag}_wit", proof=False)
    if res != "SAT":
        raise RuntimeError("boundary mismatch: R-1 not SAT on certify pass")
    res2, payload, nsol2 = decide(coeffs, const, k, R, nontrivial, workdir,
                                  f"{tag}_n{R}", proof=True)
    if res2 != "UNSAT":
        raise RuntimeError("boundary mismatch: R not UNSAT on certify pass")
    cnff, prf = payload
    chk = subprocess.run(["./rup_check", cnff, prf], capture_output=True,
                         text=True)
    if chk.returncode != 0:
        raise RuntimeError(f"RUP check failed: {chk.stderr}")
    if verbose:
        print(f"  R = {R}; UNSAT at {R}: {nsol2} solution tuples, "
              f"proof RUP-VERIFIED; witness at {R-1} extracted")
    return R, col


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    wd = "work"
    os.makedirs(wd, exist_ok=True)
    # Calibration battery: classical values the pipeline must reproduce.
    # R_2(x+y=z) = 5, R_3(x+y=z) = 14  (Schur numbers 4, 13 + 1)
    # R_2(x+y=2z, not_all_equal) = 9   (= van der Waerden W(2;3))
    # R_3(x - y = z) = 14              (equivalent to Schur by y+z=x)
    tests = [
        ("schur2", [1, 1, -1], 0, 2, "all", 5),
        ("schur3", [1, 1, -1], 0, 3, "all", 14),
        ("ap2", [1, 1, -2], 0, 2, "not_all_equal", 9),
        ("diff3", [1, -1, -1], 0, 3, "all", 14),
    ]
    allok = True
    for tag, coeffs, const, k, nt, expect in tests:
        R, wit = rado(coeffs, const, k, nt, wd, tag, verbose=False)
        ok = R == expect
        allok &= ok
        print(f"{tag}: R = {R} (expected {expect}) {'OK' if ok else 'MISMATCH'}")
    print("CALIBRATION", "PASSED" if allok else "FAILED")
