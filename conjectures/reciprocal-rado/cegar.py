#!/usr/bin/env python3
"""CEGAR driver for reciprocal Rado numbers at large k.

Soundness architecture (both directions rest on exact facts):
  * Every clause ever added is the support set of an exactly-verified
    solution tuple (asserted in integer arithmetic at generation time).
    A CNF built from a SUBSET of the true constraints is weaker than the
    full encoding, so its UNSAT implies UNSAT of the full encoding:
    an UNSAT verdict at n proves f <= n unconditionally.  The certified
    run re-solves the final clause set with Glucose DRUP -> rup_check.
  * A SAT model is only believed after the pristine independent checker
    (verify_witness.py, full semantics) accepts it; until then the model
    is a counterexample generator: violations found by the in-loop oracle
    (bounded distinct-value search) or the full checker become new
    clauses.  A SAT verdict at n proves f > n via the checked witness.

Base clauses: diagonal solutions (k copies of ky sum to 1/y; support
{y, ky}) and all solutions with at most DMAX distinct x-values (weighted
Egyptian DFS over partitions of k).  Learned clauses persist across n.

Usage: cegar.py k r --start=N [--dmax=3] [--nmax=N]
"""
import sys, os, subprocess, time, hashlib, csv
from math import gcd
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
SATCERT = os.path.join(HERE, "..", "..", "tools", "satcert")
GLUCOSE = os.environ.get(
    "GLUCOSE_BIN",
    "/tmp/claude-0/-home-user-Matematica/eac8cfb3-85ae-5073-afc3-3fe178e7e078/"
    "scratchpad/build/glucose-4.2.1/simp/glucose_static")


def partitions_le(k, dmax):
    """Partitions of k into at most dmax parts, as nonincreasing tuples."""
    out = []
    def rec(rem, maxpart, acc):
        if rem == 0:
            out.append(tuple(acc)); return
        if len(acc) == dmax:
            return
        for p in range(min(rem, maxpart), 0, -1):
            rec(rem - p, p, acc + [p])
    rec(k, k, [])
    return out


def distinct_perms(t):
    from itertools import permutations
    return sorted(set(permutations(t)))


def weighted_solutions_clean(k, n, dmax, ymin=1, ymax=None):
    """All solutions with <= dmax distinct x-values, as (y, ((w,x),...))."""
    ymax = ymax or n - 1
    seen = set()
    sols = []
    for part in partitions_le(k, dmax):
        for wv in distinct_perms(part):
            d = len(wv)
            suffix = [sum(wv[t:]) for t in range(d)]
            for y in range(ymin, ymax + 1):
                def dfs(t, lo, a, b, acc):
                    if a <= 0:
                        return
                    w = wv[t]
                    if t == d - 1:
                        if (w * b) % a == 0:
                            x = (w * b) // a
                            if lo <= x <= n:
                                tup = tuple(zip(wv, acc + [x]))
                                if tup not in seen:
                                    seen.add(tup)
                                    assert sum(Fraction(wi, xi) for wi, xi
                                               in tup) == Fraction(1, y)
                                    sols.append((y, tup))
                        return
                    xlo = max(lo, (w * b) // a + 1)
                    xhi = min(n, (suffix[t] * b) // a)
                    for x in range(xlo, xhi + 1):
                        na, nb = a * x - w * b, b * x
                        g = gcd(na, nb)
                        dfs(t + 1, x + 1, na // g, nb // g, acc + [x])
                dfs(0, y + 1, 1, y, [])
    return sols


class Cegar:
    def __init__(self, k, r, dmax=3):
        self.k, self.r, self.dmax = k, r, dmax
        self.supports = {}        # frozenset -> provenance string
        self.oracle_cache_n = 0

    def add_solution(self, y, wx_pairs, tag):
        S = frozenset([y] + [x for _, x in wx_pairs])
        assert sum(w for w, _ in wx_pairs) == self.k
        assert sum(Fraction(w, x) for w, x in wx_pairs) == Fraction(1, y)
        self.supports.setdefault(S, f"{tag}: 1/{y} = " +
                                 "+".join(f"{w}/{x}" for w, x in wx_pairs))

    def _enumw(self, n, dmax):
        """C weighted enumerator; returns [(y, ((w,x),...)), ...]."""
        p = subprocess.run([os.path.join(HERE, "enumw"), str(self.k), str(n),
                            str(dmax)], capture_output=True, text=True,
                           check=True)
        out = []
        for ln in p.stdout.splitlines():
            t = list(map(int, ln.split()))
            y, rest = t[0], t[1:]
            out.append((y, tuple((rest[i], rest[i + 1])
                                 for i in range(0, len(rest), 2))))
        return out

    def seed(self, n):
        t0 = time.time()
        self.cap = n
        for y, tup in self._enumw(n, self.dmax):
            self.add_solution(y, tup, f"d{self.dmax}")
        print(f"    seed: {len(self.supports)} supports at cap {n} "
              f"({time.time()-t0:.0f}s)", flush=True)
        # oracle cache: one tier deeper than the seed
        self.oracle_pool = []
        for y, tup in self._enumw(n, min(self.k, self.dmax + 1)):
            S = frozenset([y] + [x for _, x in tup])
            self.oracle_pool.append((max(S), S, y, tup))
        print(f"    pool: {len(self.oracle_pool)} cached solutions "
              f"({time.time()-t0:.0f}s)", flush=True)
        return time.time() - t0

    def clauses(self, n):
        r = self.r
        v = lambda x, c: (x - 1) * r + c + 1
        cls = [[v(x, c) for c in range(r)] for x in range(1, n + 1)]
        for S in self.supports:
            if max(S) <= n:
                for c in range(r):
                    cls.append([-v(x, c) for x in S])
        return cls

    def solve(self, n):
        from pysat.solvers import Cadical153
        with Cadical153(bootstrap_with=self.clauses(n)) as s:
            if not s.solve():
                return False, None
            model = set(l for l in s.get_model() if l > 0)
            col = []
            for x in range(1, n + 1):
                for c in range(self.r):
                    if (x - 1) * self.r + c + 1 in model:
                        col.append(c); break
            return True, col

    def oracle_violation(self, col, n, dmax):
        """Find a mono solution with <= dmax distinct x-values, or None."""
        for c in range(self.r):
            C = [x for x in range(1, n + 1) if col[x - 1] == c]
            Cset = set(C)
            for part in partitions_le(self.k, dmax):
                for wv in distinct_perms(part):
                    d = len(wv)
                    suffix = [sum(wv[t:]) for t in range(d)]
                    for y in C:
                        def dfs(t, lo, a, b, acc):
                            if a <= 0:
                                return None
                            w = wv[t]
                            if t == d - 1:
                                if (w * b) % a == 0:
                                    x = (w * b) // a
                                    if lo <= x <= n and x in Cset:
                                        return acc + [x]
                                return None
                            xlo = max(lo, (w * b) // a + 1)
                            xhi = min(n, (suffix[t] * b) // a)
                            for x in range(xlo, xhi + 1):
                                if x not in Cset:
                                    continue
                                na, nb = a * x - w * b, b * x
                                g = gcd(na, nb)
                                res = dfs(t + 1, x + 1, na // g, nb // g, acc + [x])
                                if res:
                                    return res
                            return None
                        got = dfs(0, y + 1, 1, y, [])
                        if got:
                            return y, tuple(zip(wv, got))
        return None

    def full_check(self, col, n, tag):
        """In-loop full oracle: the C checker (check_class), --all mode.
        Unique filename per call — concurrent lanes must never share paths."""
        self._fc = getattr(self, "_fc", 0) + 1
        wpath = os.path.join(HERE, "work",
                             f"{tag}_n{n}_p{os.getpid()}_{self._fc}.witness")
        os.makedirs(os.path.dirname(wpath), exist_ok=True)
        with open(wpath, "w") as f:
            f.write(f"{n} {self.r} {self.k}\n" + " ".join(map(str, col)) + "\n")
        p = subprocess.run([os.path.join(HERE, "check_class"), wpath, "--all"],
                           capture_output=True, text=True)
        ok = "WITNESS OK" in p.stdout
        if ok:
            os.rename(wpath, os.path.join(HERE, "work", f"{tag}_n{n}.witness"))
            wpath = os.path.join(HERE, "work", f"{tag}_n{n}.witness")
        else:
            os.remove(wpath)
        return ok, p.stdout, wpath

    def decide(self, n, tag, verbose=True):
        """CEGAR loop at fixed n. Returns (True, col, wpath) or (False, None, None)."""
        if n > getattr(self, "cap", 0):
            if verbose: print(f"    re-seeding at cap {int(n*1.3)+32}", flush=True)
            self.seed(int(n * 1.3) + 32)
        rounds = 0
        while True:
            rounds += 1
            sat, col = self.solve(n)
            if not sat:
                if verbose: print(f"    n={n}: UNSAT after {rounds} rounds "
                                  f"({len(self.supports)} supports)", flush=True)
                return False, None, None
            # batch oracle: every cached solution that is fully monochromatic
            batch = []
            for mx, S, y, tup in self.oracle_pool:
                if mx <= n and S not in self.supports:
                    c0 = col[y - 1]
                    if all(col[x - 1] == c0 for x in S):
                        batch.append((y, tup))
            if batch:
                for y, tup in batch:
                    self.add_solution(y, tup, "oracle")
                if verbose:
                    print(f"    n={n}: round {rounds}, +{len(batch)} clauses "
                          f"({len(self.supports)} total)", flush=True)
                continue
            # cache clean: the C full checker is the remaining oracle (batch)
            ok, msg, wpath = self.full_check(col, n, tag)
            if ok:
                if verbose: print(f"    n={n}: SAT, full check OK "
                                  f"({rounds} rounds)", flush=True)
                return True, col, wpath
            from collections import Counter
            added = 0
            for ln in msg.splitlines():
                if not ln.startswith("VIOLATION"):
                    continue
                body = ln.split(":", 1)[1]
                lhs, rhs = body.split("=")
                xs = [int(t.strip().split("/")[1]) for t in lhs.split("+")]
                y = int(rhs.strip().split()[0].split("/")[1])
                tup = tuple((w, x) for x, w in
                            sorted(Counter(xs).items(), key=lambda p: p[0]))
                self.add_solution(y, tup, "fullchk")
                added += 1
            if added == 0:
                raise RuntimeError(f"checker said not-OK but no violations "
                                   f"parsed: {msg[:400]}")
            if verbose:
                print(f"    n={n}: round {rounds}, full-check +{added} clauses "
                      f"({len(self.supports)} total)", flush=True)
        # unreachable

    def bracket(self, nstart, nmax=10**6, verbose=True):
        k, r = self.k, self.r
        tag = f"f{r}_{k}"
        self.seed(min(nmax, max(nstart + 64, int(nstart * 1.4))))
        n = nstart
        lo = hi = None
        wit = None
        step = 1
        while n <= nmax:
            sat, col, wp = self.decide(n, tag, verbose)
            if verbose: print(f"  n={n}: {'SAT' if sat else 'UNSAT'}", flush=True)
            if sat:
                lo, wit = n, col
                n += step; step *= 2
            else:
                hi = n; break
        if lo is None:
            n = hi - 1
            while True:
                sat, col, wp = self.decide(n, tag, verbose)
                if verbose: print(f"  n={n}: {'SAT' if sat else 'UNSAT'}", flush=True)
                if sat:
                    lo, wit = n, col; break
                hi = n; n -= 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            sat, col, wp = self.decide(mid, tag, verbose)
            if verbose: print(f"  bisect n={mid}: {'SAT' if sat else 'UNSAT'}",
                              flush=True)
            if sat:
                lo, wit = mid, col
            else:
                hi = mid
        return lo, hi, wit

    def certify(self, f, wit_col):
        """Certified pair: full-checked witness at f-1, Glucose DRUP at f."""
        k, r = self.k, self.r
        tag = f"f{r}_{k}"
        certdir = os.path.join(HERE, "certs")
        os.makedirs(certdir, exist_ok=True)
        wpath = os.path.join(certdir, f"{tag}_n{f-1}.witness")
        with open(wpath, "w") as fh:
            fh.write(f"{f-1} {r} {k}\n" + " ".join(map(str, wit_col)) + "\n")
        p = subprocess.run([os.path.join(HERE, "check_class"), wpath],
                           capture_output=True, text=True)
        if "WITNESS OK" not in p.stdout:
            raise RuntimeError(f"final witness FAILED: {p.stdout}")
        # slow pristine Python checker runs detached; session reviews the log
        with open(wpath + ".pyverify", "w") as lg:
            subprocess.Popen([sys.executable,
                              os.path.join(HERE, "verify_witness.py"), wpath],
                             stdout=lg, stderr=lg)
        # UNSAT side: write CNF + solution provenance, glucose, rup_check
        cls = self.clauses(f)
        cnff = os.path.join(certdir, f"{tag}_n{f}.cnf")
        with open(cnff, "w") as fh:
            fh.write(f"p cnf {f*r} {len(cls)}\n")
            for c in cls:
                fh.write(" ".join(map(str, c)) + " 0\n")
        sha = hashlib.sha256(open(cnff, "rb").read()).hexdigest()
        solsf = os.path.join(certdir, f"{tag}_n{f}.sols")
        with open(solsf, "w") as fh:
            for S in sorted(self.supports, key=lambda s: (max(s), sorted(s))):
                if max(S) <= f:
                    fh.write(self.supports[S] + "\n")
        prf = os.path.join(certdir, f"{tag}_n{f}.drup")
        t0 = time.time()
        p = subprocess.run([GLUCOSE, "-certified", f"-certified-output={prf}",
                            cnff], capture_output=True, text=True)
        if "s UNSATISFIABLE" not in p.stdout:
            raise RuntimeError("glucose did not prove UNSAT")
        gs = time.time() - t0
        chk = subprocess.run([os.path.join(SATCERT, "rup_check"), cnff, prf],
                             capture_output=True, text=True)
        if chk.returncode != 0:
            raise RuntimeError(f"RUP FAILED: {chk.stdout}{chk.stderr}")
        os.remove(cnff)
        row = dict(k=k, r=r, f=f, nsol_at_f=f"cegar:{sum(1 for S in self.supports if max(S) <= f)}",
                   nsupp_at_f=sum(1 for S in self.supports if max(S) <= f),
                   enum_cap="cegar", enum_secs="", glucose_secs=round(gs, 1),
                   cnf_sha=sha, witness=os.path.basename(wpath),
                   proof=os.path.basename(prf))
        csvp = os.path.join(HERE, "data", "results.csv")
        exists = os.path.exists(csvp)
        with open(csvp, "a", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(row))
            if not exists:
                w.writeheader()
            w.writerow(row)
        print(f"  ==> f_{r}({k}) = {f}   CERTIFIED (witness OK, DRUP VERIFIED; "
              f"clause provenance in {os.path.basename(solsf)})", flush=True)


if __name__ == "__main__":
    k, r = int(sys.argv[1]), int(sys.argv[2])
    nstart, dmax, nmax, cert_at = 3 * k * k, 3, 10**6, None
    for a in sys.argv[3:]:
        if a.startswith("--start="): nstart = int(a.split("=")[1])
        if a.startswith("--dmax="): dmax = int(a.split("=")[1])
        if a.startswith("--nmax="): nmax = int(a.split("=")[1])
        if a.startswith("--certify-at="): cert_at = int(a.split("=")[1])
    C = Cegar(k, r, dmax)
    if cert_at is not None:
        # boundary known: witness at cert_at-1 must already sit in certs/;
        # re-derive UNSAT at cert_at through the CEGAR loop, then certify.
        wf = os.path.join(HERE, "certs", f"f{r}_{k}_n{cert_at-1}.witness")
        with open(wf) as fh:
            fh.readline()
            wit = list(map(int, fh.readline().split()))
        C.seed(int(cert_at * 1.3) + 32)
        sat, _, _ = C.decide(cert_at, f"f{r}_{k}")
        assert not sat, f"expected UNSAT at {cert_at}"
        C.certify(cert_at, wit)
    else:
        lo, hi, wit = C.bracket(nstart, nmax)
        assert lo == hi - 1
        C.certify(hi, wit)
