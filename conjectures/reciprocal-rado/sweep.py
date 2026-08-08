#!/usr/bin/env python3
"""Production sweep for reciprocal Rado numbers f_r(k).

Per k: enumerate solutions ONCE at a cap (C enumerator, parallel by y
residue stripes), filter per n (solution sets are monotone in n), bracket
the boundary with Cadical (no proof), then certify the pair:
  SAT at f-1: witness verified by verify_witness.py (independent checker)
  UNSAT at f: Glucose 4.2.1 DRUP proof checked by tools/satcert/rup_check
Appends one row per value to data/results.csv, boundary artifacts in certs/.

Usage: sweep.py k r [ncap] [--start N]
"""
import sys, os, subprocess, time, hashlib, csv

HERE = os.path.dirname(os.path.abspath(__file__))
SATCERT = os.path.join(HERE, "..", "..", "tools", "satcert")
ENUM = os.path.join(HERE, "enum")
GLUCOSE = os.environ.get(
    "GLUCOSE_BIN",
    "/tmp/claude-0/-home-user-Matematica/eac8cfb3-85ae-5073-afc3-3fe178e7e078/"
    "scratchpad/build/glucose-4.2.1/simp/glucose_static")


def enum_parallel(k, ncap, stripes=4):
    """All solutions at cap, striped by y mod `stripes` via C enumerator."""
    # enum.c walks y in 1..n-1; stripe by filtering its output lines.
    # (One process per stripe would need C support; instead run one process
    # per y *block* using a patched range via env — simplest: single process
    # for k<=6, blocks for k>=7.)
    t0 = time.time()
    if k <= 6:
        out = subprocess.run([ENUM, str(k), str(ncap)], capture_output=True,
                             text=True, check=True).stdout
        sols = [tuple(map(int, ln.split())) for ln in out.splitlines()]
    else:
        procs, sols = [], []
        for s in range(stripes):
            procs.append(subprocess.Popen(
                [ENUM, str(k), str(ncap), f"--stripe={s}/{stripes}"],
                stdout=subprocess.PIPE, text=True))
        for p in procs:
            out, _ = p.communicate()
            if p.returncode != 0:
                raise RuntimeError("enum stripe failed")
            sols += [tuple(map(int, ln.split())) for ln in out.splitlines()]
    return sols, time.time() - t0


def supports(sols):
    seen = set()
    for t in sols:
        seen.add(frozenset(t))
    return seen


def clauses_for(supps, r, n):
    v = lambda x, c: (x - 1) * r + c + 1
    cls = [[v(x, c) for c in range(r)] for x in range(1, n + 1)]
    for S in supps:
        if max(S) <= n:
            for c in range(r):
                cls.append([-v(x, c) for x in S])
    return cls, n * r


def solve_fast(supps, r, n):
    from pysat.solvers import Cadical153
    cls, nv = clauses_for(supps, r, n)
    with Cadical153(bootstrap_with=cls) as s:
        if s.solve():
            model = set(l for l in s.get_model() if l > 0)
            col = []
            for x in range(1, n + 1):
                for c in range(r):
                    if (x - 1) * r + c + 1 in model:
                        col.append(c); break
                else:
                    raise RuntimeError("no color")
            return True, col
        return False, None


def write_cnf(cls, nv, path):
    with open(path, "w") as f:
        f.write(f"p cnf {nv} {len(cls)}\n")
        for c in cls:
            f.write(" ".join(map(str, c)) + " 0\n")
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def certify(supps, k, r, f, wit_col, tag):
    certdir = os.path.join(HERE, "certs")
    os.makedirs(certdir, exist_ok=True)
    # witness side
    wpath = os.path.join(certdir, f"{tag}_n{f-1}.witness")
    with open(wpath, "w") as fh:
        fh.write(f"{f-1} {r} {k}\n" + " ".join(map(str, wit_col)) + "\n")
    chk = subprocess.run([sys.executable, os.path.join(HERE, "verify_witness.py"),
                          wpath], capture_output=True, text=True)
    if "WITNESS OK" not in chk.stdout:
        raise RuntimeError(f"witness FAILED: {chk.stdout}{chk.stderr}")
    # unsat side: glucose_static streaming DRUP
    cls, nv = clauses_for(supps, r, f)
    cnff = os.path.join(certdir, f"{tag}_n{f}.cnf")
    prf = os.path.join(certdir, f"{tag}_n{f}.drup")
    sha = write_cnf(cls, nv, cnff)
    t0 = time.time()
    p = subprocess.run([GLUCOSE, "-certified", f"-certified-output={prf}", cnff],
                       capture_output=True, text=True)
    if "s UNSATISFIABLE" not in p.stdout:
        raise RuntimeError(f"glucose did not prove UNSAT at {f}")
    gsecs = time.time() - t0
    chk = subprocess.run([os.path.join(SATCERT, "rup_check"), cnff, prf],
                         capture_output=True, text=True)
    if chk.returncode != 0:
        raise RuntimeError(f"RUP FAILED: {chk.stdout}{chk.stderr}")
    os.remove(cnff)          # regenerable byte-identically; sha recorded
    return sha, wpath, prf, gsecs


def sweep(k, r, ncap=None, nstart=None):
    ncap = ncap or (3 * k * k + 8 * k + 80)
    sols, esecs = enum_parallel(k, ncap)
    supps = supports(sols)
    print(f"k={k} r={r}: enum@{ncap} nsol={len(sols)} nsupp={len(supps)} "
          f"{esecs:.1f}s", flush=True)
    # bracket
    n = nstart or 3 * k * k
    lo = hi = None
    wit = None
    step = 1
    t0 = time.time()
    while True:
        if n >= ncap:
            raise RuntimeError(f"cap {ncap} reached at n={n}: re-run with bigger cap")
        sat, col = solve_fast(supps, r, n)
        print(f"  n={n}: {'SAT' if sat else 'UNSAT'} "
              f"({time.time()-t0:.1f}s cum)", flush=True)
        if sat:
            lo, wit = n, col
            n += step
            step *= 2
        else:
            hi = n
            break
    if lo is None:
        # walked straight into UNSAT: step down to find SAT side
        n = hi - 1
        while True:
            sat, col = solve_fast(supps, r, n)
            print(f"  n={n}: {'SAT' if sat else 'UNSAT'}", flush=True)
            if sat:
                lo, wit = n, col
                break
            hi = n
            n -= 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        sat, col = solve_fast(supps, r, mid)
        print(f"  bisect n={mid}: {'SAT' if sat else 'UNSAT'}", flush=True)
        if sat:
            lo, wit = mid, col
        else:
            hi = mid
    f = hi
    assert lo == f - 1
    sha, wpath, prf, gsecs = certify(supps, k, r, f, wit, f"f{r}_{k}")
    nsol_at_f = sum(1 for t in sols if max(t) <= f)
    row = dict(k=k, r=r, f=f, nsol_at_f=nsol_at_f,
               nsupp_at_f=sum(1 for S in supps if max(S) <= f),
               enum_cap=ncap, enum_secs=round(esecs, 1),
               glucose_secs=round(gsecs, 1), cnf_sha=sha,
               witness=os.path.basename(wpath), proof=os.path.basename(prf))
    csvp = os.path.join(HERE, "data", "results.csv")
    os.makedirs(os.path.dirname(csvp), exist_ok=True)
    exists = os.path.exists(csvp)
    with open(csvp, "a", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(row))
        if not exists:
            w.writeheader()
        w.writerow(row)
    print(f"  ==> f_{r}({k}) = {f}   CERTIFIED (witness OK, DRUP VERIFIED)",
          flush=True)
    return f


if __name__ == "__main__":
    k, r = int(sys.argv[1]), int(sys.argv[2])
    ncap = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else None
    nstart = None
    for a in sys.argv:
        if a.startswith("--start="):
            nstart = int(a.split("=")[1])
    sweep(k, r, ncap, nstart)
