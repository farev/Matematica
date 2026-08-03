"""Circular threshold words: existence spectrum by exact SAT search.

DEFINITIONS (self-contained; see NOTE.md for the correspondence to the
literature, which is secondary-sourced).

Sigma_n = {0,...,n-1}.  A *circular word* of length m is w in Sigma_n^m read
with indices mod m.  Its *factors* are the words w[i]w[i+1]...w[i+l-1]
(indices mod m) for 0 <= i < m and 1 <= l <= m; equivalently the factors of
w^omega of length at most m.  A nonempty word u has period p (1 <= p < |u|)
if u[j] = u[j+p] whenever both indices are legal; exp(u) = |u| / (least
period of u).  For a rational alpha > 1, w is *circular alpha^+-free* if
every factor of the circular word has exponent <= alpha.

For alpha = RT(n) (the repetition threshold: RT(3) = 7/4, RT(4) = 7/5,
RT(n) = n/(n-1) for n >= 5) we call such a w a *circular n-ary threshold
word*, and

    C(n) = { m >= 1 : a circular n-ary threshold word of length m exists }

is the *circular threshold spectrum*.

ENCODING.  A factor of exponent > alpha with least period p contains, as a
prefix, a factor of length L(p) = floor(alpha*p) + 1 with period p.  So w is
circular alpha^+-free iff for no p >= 1 with L(p) <= m and no i in Z_m does

    w[i+j] = w[i+j+p]   for all 0 <= j < q(p),   q(p) = L(p) - p

hold (indices mod m).  That is the clause set below.  Everything is exact
integer / rational arithmetic; the only floating point anywhere is absent.

Usage:
    python3 circspec.py spectrum N LO HI [--alpha A/B] [--out FILE] [--solver S]
    python3 circspec.py one N M [--alpha A/B]
"""
import argparse
import sys
from fractions import Fraction

from pysat.formula import IDPool
from pysat.solvers import Solver

SOLVERS = ('cadical153', 'glucose42', 'minisat22')


def RT(n):
    """Repetition threshold (Dejean; Thue for n=3, Pansiot for n=4)."""
    if n == 2:
        return Fraction(2)
    if n == 3:
        return Fraction(7, 4)
    if n == 4:
        return Fraction(7, 5)
    return Fraction(n, n - 1)


def forbidden_windows(m, alpha):
    """Yield (p, q) with q = L(p)-p >= 1 for every period p that fits."""
    out = []
    p = 1
    while True:
        L = (alpha * p).numerator // (alpha * p).denominator + 1
        if L > m:
            break
        out.append((p, L - p))
        p += 1
    return out


def build(n, m, alpha):
    pool = IDPool()
    x = lambda i, c: pool.id(('x', i, c))
    e = lambda i, p: pool.id(('e', i, p))
    cls = []
    for i in range(m):
        cls.append([x(i, c) for c in range(n)])
        for c in range(n):
            for d in range(c + 1, n):
                cls.append([-x(i, c), -x(i, d)])
    wins = forbidden_windows(m, alpha)
    need_eq = set()
    for p, q in wins:
        if q == 1:
            for i in range(m):
                for c in range(n):
                    cls.append([-x(i, c), -x((i + p) % m, c)])
        else:
            need_eq.add(p)
            for i in range(m):
                cls.append([-e((i + j) % m, p) for j in range(q)])
    for p in need_eq:
        for i in range(m):
            j = (i + p) % m
            for c in range(n):
                cls.append([-x(i, c), -x(j, c), e(i, p)])
                cls.append([-e(i, p), -x(i, c), x(j, c)])
    # Letter-relabelling symmetry break.  p=1 always has q=1 for alpha < 2,
    # so w[0] != w[1]; fixing w[0]=0, w[1]=1 loses no solutions up to
    # renaming letters.
    if m >= 1:
        cls.append([x(0, 0)])
    if m >= 2 and n >= 2:
        cls.append([x(1, 1)])
    return cls, x


def solve(n, m, alpha, solver='cadical153'):
    cls, x = build(n, m, alpha)
    with Solver(name=solver, bootstrap_with=cls) as s:
        ok = s.solve()
        if not ok:
            return False, None
        mod = set(l for l in s.get_model() if l > 0)
    w = []
    for i in range(m):
        for c in range(n):
            if x(i, c) in mod:
                w.append(c)
                break
    return True, w


def least_period(u):
    l = len(u)
    for p in range(1, l):
        if all(u[t] == u[t + p] for t in range(l - p)):
            return p
    return l


def verify(w, n, alpha):
    """Independent check, written straight from the definition.

    Returns (ok, witness).  O(m^3) -- deliberately naive, shares no code with
    the encoder.
    """
    m = len(w)
    if any(c < 0 or c >= n for c in w):
        return False, ('alphabet', None)
    for i in range(m):
        for l in range(2, m + 1):
            u = [w[(i + t) % m] for t in range(l)]
            p = least_period(u)
            if p < l and Fraction(l, p) > alpha:
                return False, (i, l, p)
    return True, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['spectrum', 'one'])
    ap.add_argument('n', type=int)
    ap.add_argument('lo', type=int)
    ap.add_argument('hi', type=int, nargs='?')
    ap.add_argument('--alpha', default=None, help='rational A/B; default RT(n)')
    ap.add_argument('--out', default=None)
    ap.add_argument('--solver', default='cadical153')
    ap.add_argument('--noverify', action='store_true')
    a = ap.parse_args()

    alpha = RT(a.n) if a.alpha is None else Fraction(a.alpha)
    if a.cmd == 'one':
        ok, w = solve(a.n, a.lo, alpha, a.solver)
        print('SAT' if ok else 'UNSAT')
        if ok:
            v, bad = verify(w, a.n, alpha)
            print('verified:', v, '' if v else bad)
            print(''.join(str(c) for c in w))
        return

    hi = a.hi
    rows = []
    # Write incrementally: a long sweep that is interrupted must still leave
    # its completed rows (and witnesses) on disk.
    fh = None
    if a.out:
        fh = open(a.out, 'w')
        fh.write('n,alpha,m,exists,witness\n')
    for m in range(a.lo, hi + 1):
        ok, w = solve(a.n, m, alpha, a.solver)
        if ok and not a.noverify:
            v, bad = verify(w, a.n, alpha)
            if not v:
                print(f'FATAL: witness at n={a.n} m={m} fails verify: {bad}',
                      file=sys.stderr)
                sys.exit(2)
        ws = ''.join(str(c) for c in w) if ok else ''
        rows.append((m, ok, ws))
        if fh:
            fh.write(f'{a.n},{alpha},{m},{1 if ok else 0},{ws}\n')
            fh.flush()
        print(f'n={a.n} alpha={alpha} m={m} {"SAT" if ok else "UNSAT"}',
              flush=True)
    if fh:
        fh.close()
    good = [m for m, ok, _ in rows if ok]
    bad = [m for m, ok, _ in rows if not ok]
    print(f'# n={a.n} alpha={alpha} range [{a.lo},{hi}]')
    print(f'# realizable  : {len(good)}')
    print(f'# exceptional : {bad}')


if __name__ == '__main__':
    main()
