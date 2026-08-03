"""Pumping circular threshold words along a uniform morphism.

Implements, and independently re-checks, the two ingredients of Theorem C
(see NOTE.md):

  Lemma A.  If h is q-uniform and maps alpha^+-free words to alpha^+-free
            words, and w lies in S_2(n,m) -- every factor of w^omega of
            length <= m+2 has exponent <= alpha -- then h(w) lies in
            S_2(n,qm).

  Theorem M. A q-uniform h with (H1) distinct first letters, (H2) distinct
            last letters, (H3') relativised synchronization and (H4)
            h(v) alpha^+-free for every alpha^+-free v with |v| <= N0,
            maps alpha^+-free words to alpha^+-free words.

This file re-verifies (H1)-(H4) in Python (a cross-check on dejean_morph.c,
which shares no code with it), finds seeds by SAT, and then verifies the
pumped words h^j(w) directly against the definition.

Usage:
  python3 pump.py morphcheck N H0 [--alpha A/B]
  python3 pump.py seed N M [--alpha A/B] [--ext K]
  python3 pump.py chain N H0 W0 J [--alpha A/B]
"""
import argparse
import sys
from fractions import Fraction

import numpy as np

from circspec import RT, build, verify  # noqa: F401  (shared SAT encoder)
from pysat.solvers import Solver


# ---------------------------------------------------------------- basics

def qwin(alpha, p):
    """floor(alpha*p)+1-p : number of equalities in the shortest factor of
    period p and exponent > alpha."""
    ap = alpha * p
    return ap.numerator // ap.denominator + 1 - p


def afree(w, alpha):
    """Is the (linear) word w alpha^+-free?  Returns (ok, (i,p) or None)."""
    L = len(w)
    a = np.asarray(w, dtype=np.int32)
    for p in range(1, L):
        q = qwin(alpha, p)
        if p + q > L:
            break
        eq = a[:L - p] == a[p:]
        # longest run of True
        run = 0
        for i in range(len(eq)):
            if eq[i]:
                run += 1
                if run >= q:
                    return False, (i - q + 1, p)
            else:
                run = 0
    return True, None


def afree_fast(w, alpha):
    """Vectorised version of afree for long words."""
    L = len(w)
    a = np.asarray(w, dtype=np.int32)
    for p in range(1, L):
        q = qwin(alpha, p)
        if p + q > L:
            break
        eq = (a[:L - p] == a[p:])
        if q == 1:
            if eq.any():
                return False, (int(np.argmax(eq)), p)
            continue
        # run-length: a run of q consecutive Trues exists?
        acc = eq
        step = 1
        while step < q:
            k = min(step, q - step)
            acc = acc[:len(acc) - k] & acc[k:]   # never aliased: new array
            step += k
            if not acc.any():
                break
        if acc.any():
            return False, (int(np.argmax(acc)), p)
    return True, None


def circ_afree(w, alpha, ext=0):
    """Is the circular word w alpha^+-free, checking factors of w^omega of
    length <= m+ext?  Independent of the SAT encoder."""
    m = len(w)
    a = np.asarray(w, dtype=np.int32)
    for p in range(1, m):
        q = qwin(alpha, p)
        if p + q > m + ext:
            break
        eq = (a == np.roll(a, -p))          # eq[i] = w[i]==w[i+p mod m]
        if q == 1:
            if eq.any():
                return False, (int(np.argmax(eq)), p)
            continue
        acc = eq.copy()
        step = 1
        while step < q:
            k = min(step, q - step)
            acc &= np.roll(acc, -k)
            step += k
            if not acc.any():
                break
        if acc.any():
            return False, (int(np.argmax(acc)), p)
    return True, None


# ---------------------------------------------------- morphism conditions

def images(n, h0):
    q = len(h0)
    return [[(h0[i] + a) % n for i in range(q)] for a in range(n)]


def morphcheck(n, h0, alpha, verbose=True):
    q = len(h0)
    im = images(n, h0)
    rep = {}
    rep['H1'] = len({im[a][0] for a in range(n)}) == n
    rep['H2'] = len({im[a][q - 1] for a in range(n)}) == n
    # (H3') relativised synchronization, checked by brute force over a,b,c
    aa_free = alpha >= 2
    bad = None
    for a in range(n):
        for b in range(n):
            if a == b and not aa_free:
                continue
            ab = im[a] + im[b]
            for i in range(1, q):
                seg = ab[i:i + q]
                for c in range(n):
                    if seg == im[c]:
                        bad = (a, b, c, i)
    rep['H3'] = bad is None
    rep['H3_witness'] = bad
    # (H4): h(v) alpha^+-free for every alpha^+-free v with |v| <= N0
    def ceil_frac(f):
        return -((-f.numerator) // f.denominator)
    P0 = ceil_frac(Fraction(2 * q) / (alpha - 1))
    N0 = ceil_frac((alpha * P0 + 1) / q) + 1
    N0 = max(N0, 2 * n + 2)
    rep['N0'] = N0
    rep['P0'] = P0
    ok = True
    witness = None
    v = [0]
    img = list(im[0])

    okp, w = afree_fast(img, alpha)
    if not okp:
        ok, witness = False, ([0], w)

    def dfs(t):
        nonlocal ok, witness
        if not ok or t == N0:
            return
        for c in range(n):
            v.append(c)
            if afree_fast(v, alpha)[0]:
                base = len(img)
                img.extend(im[c])
                okq, wq = afree_fast(img, alpha)
                if not okq:
                    ok, witness = False, (list(v), wq)
                    del img[base:]
                    v.pop()
                    return
                dfs(t + 1)
                del img[base:]
                if not ok:
                    v.pop()
                    return
            v.pop()

    if ok:
        dfs(1)
    rep['H4'] = ok
    rep['H4_witness'] = witness
    rep['ALL'] = rep['H1'] and rep['H2'] and rep['H3'] and rep['H4']
    if verbose:
        for k in ('H1', 'H2', 'H3', 'H4', 'N0', 'P0', 'ALL'):
            print(f'  {k}: {rep[k]}')
        if rep['H3_witness']:
            print('  H3 witness:', rep['H3_witness'])
        if rep['H4_witness']:
            print('  H4 witness:', rep['H4_witness'])
    return rep


# ------------------------------------------------------------- seed search

def build_ext(n, m, alpha, ext):
    """SAT clauses for: every factor of w^omega of length <= m+ext has
    exponent <= alpha."""
    from pysat.formula import IDPool
    pool = IDPool()
    x = lambda i, c: pool.id(('x', i, c))
    e = lambda i, p: pool.id(('e', i, p))
    cls = []
    for i in range(m):
        cls.append([x(i, c) for c in range(n)])
        for c in range(n):
            for d in range(c + 1, n):
                cls.append([-x(i, c), -x(i, d)])
    need = set()
    p = 1
    while True:
        q = qwin(alpha, p)
        if p + q > m + ext:
            break
        if q == 1:
            for i in range(m):
                for c in range(n):
                    cls.append([-x(i, c), -x((i + p) % m, c)])
        else:
            need.add(p)
            for i in range(m):
                cls.append([-e((i + j) % m, p) for j in range(q)])
        p += 1
    for p in need:
        for i in range(m):
            j = (i + p) % m
            for c in range(n):
                cls.append([-x(i, c), -x(j, c), e(i, p)])
                cls.append([-e(i, p), -x(i, c), x(j, c)])
    cls.append([x(0, 0)])
    if m >= 2:
        cls.append([x(1, 1)])
    return cls, x


def seed(n, m, alpha, ext=2, solver='cadical153'):
    cls, x = build_ext(n, m, alpha, ext)
    with Solver(name=solver, bootstrap_with=cls) as s:
        if not s.solve():
            return None
        mod = set(l for l in s.get_model() if l > 0)
    w = []
    for i in range(m):
        for c in range(n):
            if x(i, c) in mod:
                w.append(c)
                break
    return w


def apply_morph(n, h0, w):
    im = images(n, h0)
    out = []
    for c in w:
        out.extend(im[c])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['morphcheck', 'seed', 'chain'])
    ap.add_argument('n', type=int)
    ap.add_argument('arg2')
    ap.add_argument('arg3', nargs='?')
    ap.add_argument('--alpha', default=None)
    ap.add_argument('--ext', type=int, default=2)
    a = ap.parse_args()
    n = a.n
    alpha = RT(n) if a.alpha is None else Fraction(a.alpha)

    if a.cmd == 'morphcheck':
        h0 = [int(ch) for ch in a.arg2]
        print(f'n={n} alpha={alpha} q={len(h0)} h0={a.arg2}')
        r = morphcheck(n, h0, alpha)
        sys.exit(0 if r['ALL'] else 1)

    if a.cmd == 'seed':
        m = int(a.arg2)
        w = seed(n, m, alpha, a.ext)
        if w is None:
            print('UNSAT')
            sys.exit(1)
        ok, bad = circ_afree(w, alpha, ext=a.ext)
        print('seed:', ''.join(map(str, w)))
        print('independent circular check (ext=%d):' % a.ext, ok, '' if ok else bad)
        sys.exit(0 if ok else 2)

    if a.cmd == 'chain':
        h0 = [int(ch) for ch in a.arg2]
        w0 = [int(ch) for ch in a.arg3]
        J = 3
        q = len(h0)
        print(f'n={n} alpha={alpha} q={q} |w0|={len(w0)}')
        w = w0
        for j in range(J + 1):
            ok2, bad2 = circ_afree(w, alpha, ext=2)
            ok0, bad0 = circ_afree(w, alpha, ext=0)
            print(f'  j={j} m={len(w):8d}  circular alpha^+-free: {ok0}   '
                  f'in S_2: {ok2}' + ('' if ok2 else f'  witness {bad2}'))
            if not ok0:
                print('  FAILED at j=%d' % j, bad0)
                sys.exit(2)
            if j < J:
                w = apply_morph(n, h0, w)
        sys.exit(0)


if __name__ == '__main__':
    main()
