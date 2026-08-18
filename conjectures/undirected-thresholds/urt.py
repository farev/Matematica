"""Toolkit for the undirected repetition threshold (URT) attack.

Session 2026-08-18.  Target: URT(n) = (n-1)/(n-2) for n >= 22 (Currie-Mol
conjecture, confirmed 4..21 by them; open beyond).

Definitions
-----------
* Sigma_n = {0..n-1}.  alpha = num/den, for URT(n) that is (n-1)/(n-2).
* An *undirected offender* in a word x is a factor u y u' with u nonempty,
  u' in {u, reverse(u)}, and |u y u'| / |u y| > alpha.  Writing l = |u| and
  g = |y| >= 0, the exponent condition is den*(2l+g) > num*(l+g).
  "U-alpha+-free" = no undirected offender.  (Ordinary offenders are the
  u'=u case; reversed offenders the u'=u^R case; a palindromic u makes them
  coincide.  Both scans together are exact.)
* A word is *in-class* if every (n-1) consecutive letters are pairwise
  distinct.  For alpha = (n-1)/(n-2), U-alpha+-freeness forces equal letters
  to sit at distance >= n-2+1 = n-1 - 1 + 1... precisely: distance d has
  exponent (d+1)/d > alpha iff d < n-2, so freeness forces d >= n-2 only.
  In-class (d >= n-1) is therefore a *strictly smaller* ansatz class: the
  search below is a sufficient search, and emptiness of the class would not
  disprove anything.
* Binary Pansiot code on in-class words, conventions identical to
  conjectures/circular-thresholds/pansiot.py (independently reimplemented
  here; cross-checked in tests_urt.py):
  state (a_1..a_{n-1} | b) in Sym(n); bit 0 emits a_1 (distance n-1
  recurrence), bit 1 emits the absent letter b; states compose on the right,
  g(w) = tau_{w_1} o ... o tau_{w_L} with (f o h)[i] = f[h[i]];
  decode(bits) = canonical window (0..n-2) + emitted letters.
* "U-code-free": decode(bits) is U-alpha+-free (includes the window).
* r = the window reversal permutation: r(i) = n-2-i on slots 0..n-2,
  r(n-1) = n-1.  Facts proved in NOTE.md: r tau_b r = tau_b^{-1};
  code(reverse(w)) = reverse(code(w)) for in-class w; a reversed
  letter-match of arm length L >= n-1 in decode(V) corresponds exactly to an
  anti-gid pair H_a = H_{a'} . r plus a mirrored bit-agreement run.
"""

from fractions import Fraction

import numpy as np


# ---------------------------------------------------------------- monodromy

def make_taus(n):
    tau0 = tuple(list(range(1, n - 1)) + [0, n - 1])
    tau1 = tuple(list(range(1, n)) + [0])
    return tau0, tau1


def comp(a, b):
    """(a o b)[i] = a[b[i]]."""
    return tuple(a[b[i]] for i in range(len(a)))


def pinv(a):
    out = [0] * len(a)
    for i, ai in enumerate(a):
        out[ai] = i
    return tuple(out)


def g_of(bits, n):
    tau0, tau1 = make_taus(n)
    acc = tuple(range(n))
    for c in bits:
        acc = comp(acc, tau1 if c else tau0)
    return acc


def prefix_H(bits, n):
    """[H_0=id, H_1, ..., H_L]."""
    tau0, tau1 = make_taus(n)
    acc = tuple(range(n))
    out = [acc]
    for c in bits:
        acc = comp(acc, tau1 if c else tau0)
        out.append(acc)
    return out


def rperm(n):
    return tuple(list(range(n - 2, -1, -1)) + [n - 1])


def cycle_type(p):
    n = len(p)
    seen = [False] * n
    t = []
    for i in range(n):
        if not seen[i]:
            c = 0
            j = i
            while not seen[j]:
                seen[j] = True
                j = p[j]
                c += 1
            t.append(c)
    return tuple(sorted(t))


# ------------------------------------------------------------ decode/encode

def decode(bits, n):
    st = list(range(n))
    out = list(st[: n - 1])
    for c in bits:
        if c == 0:
            x = st[0]
            st = st[1 : n - 1] + [st[0], st[n - 1]]
        else:
            x = st[n - 1]
            st = st[1 : n - 1] + [st[n - 1], st[0]]
        out.append(x)
    return out


def encode(word, n):
    bits = []
    for i in range(n - 1, len(word)):
        window = word[i - n + 1 : i]
        if len(set(window)) != n - 1:
            return None, False
        (miss,) = set(range(n)) - set(window)
        x = word[i]
        if x == word[i - n + 1]:
            bits.append(0)
        elif x == miss:
            bits.append(1)
        else:
            return None, False
    return bits, True


# ------------------------------------------------------- exact U-freeness

def ord_offender(x, num, den):
    """First ordinary offender found: (i, p, l) with x[i..i+l) = x[i+p..i+p+l),
    period p, arm l, den*(p+l) > num*p.  None if ordinary-free."""
    L = len(x)
    for p in range(1, L):
        qq = (num - den) * p // den + 1  # l >= qq  <=>  den*l > (num-den)*p
        run = 0
        for j in range(L - p):
            if x[j] == x[j + p]:
                run += 1
                if run >= qq:
                    return (j - run + 1, p, run)
            else:
                run = 0
    return None


def rev_offender(x, num, den):
    """First reversed offender: (a, l, s) with arms x[a..a+l) and
    x[s-a-l+1..s-a+1) disjoint-or-adjacent, x[a+t] == x[s-a-t], and
    den*G > num*(G-l) with span G = s-2a+1.  None if reversed-free."""
    L = len(x)
    for s in range(1, 2 * L - 2):
        run = 0
        top = None
        p0 = min((s - 1) // 2, L - 1)
        pend = max(0, s - L + 1)
        for p in range(p0, pend - 1, -1):
            if x[p] == x[s - p]:
                if run == 0:
                    top = p
                run += 1
                l = top - p + 1
                G = s - 2 * p + 1
                if den * G > num * (G - l):
                    return (p, l, s)
            else:
                run = 0
    return None


def u_offender(x, num, den):
    o = ord_offender(x, num, den)
    if o is not None:
        return ("ord",) + o
    o = rev_offender(x, num, den)
    if o is not None:
        return ("rev",) + o
    return None


def u_free(x, num, den):
    return u_offender(x, num, den) is None


def u_offender_naive(x, num, den):
    """Brute reference: try every (i, l, g) for both orientations."""
    L = len(x)
    for i in range(L):
        for l in range(1, (L - i) // 2 + 1):
            for g in range(0, L - i - 2 * l + 1):
                if den * (2 * l + g) <= num * (l + g):
                    continue  # exponent <= alpha; larger g only smaller
                j = i + l + g
                if x[i : i + l] == x[j : j + l]:
                    return ("ord", i, l, g)
                if x[i : i + l] == x[j : j + l][::-1]:
                    return ("rev", i, l, g)
    return None


# --------------------------------------------------- numpy batch U-checker

def _maxrun(eq):
    """Length of the longest run of True, and per-position run lengths."""
    if not len(eq):
        return 0, None
    c = np.cumsum(eq)
    m = np.maximum.accumulate(np.where(~eq, c, 0))
    runlen = np.where(eq, c - m, 0)
    return int(runlen.max()), runlen


def u_free_np(x, num, den, return_witness=False):
    """Vectorized exact U-freeness for long words (integer compares only)."""
    a = np.asarray(x, dtype=np.int64)
    L = len(a)
    for p in range(1, L):
        eq = a[p:] == a[:-p]
        qq = (num - den) * p // den + 1
        if qq > L - p:
            break  # longer periods need even longer runs than remain
        best, _ = _maxrun(eq)
        if best >= qq:
            if return_witness:
                return False, ("ord", p, best)
            return False
    for s in range(1, 2 * L - 2):
        p0 = min((s - 1) // 2, L - 1)
        pend = max(0, s - L + 1)
        if p0 < pend:
            continue
        ps = np.arange(p0, pend - 1, -1)
        eq = a[ps] == a[s - ps]
        _, runlen = _maxrun(eq)
        if runlen is None or not runlen.any():
            continue
        lv = runlen
        pv = ps
        Gv = s - 2 * pv + 1
        bad = den * Gv > num * (Gv - lv)
        bad &= lv > 0
        if bad.any():
            if return_witness:
                i = int(np.argmax(bad))
                return False, ("rev", int(pv[i]), int(lv[i]), s)
            return False
    if return_witness:
        return True, None
    return True


# -------------------------------------------- incremental U-freeness engine

class UInc:
    """Incremental U-alpha+-freeness for a growing word with push/pop.

    After each push, `ok` reports whether the current word is still U-free.
    Ordinary state: csuf[p] = length of the common-suffix run at period p.
    Reversed state: ar[s] = current run of mirror equalities at mirror sum s.
    All integer arithmetic.
    """

    def __init__(self, num, den, maxlen, strict=True):
        """strict=True: forbid exponents > num/den (the + version).
        strict=False: forbid exponents >= num/den as well."""
        self.num = num
        self.den = den
        self.strict = strict
        self.N = maxlen
        self.w = []
        self.csuf_stack = []
        self.ar_stack = []

    def push(self, letter):
        w = self.w
        q = len(w)
        w.append(letter)
        num, den = self.num, self.den
        aw = w
        # ordinary: periods p = 1..q ; csuf_new[p] = csuf_old[p]+1 if match
        old = self.csuf_stack[-1] if self.csuf_stack else np.zeros(0, dtype=np.int32)
        new = np.zeros(q + 1, dtype=np.int32)  # index p = 1..q
        if q >= 1:
            arr = np.asarray(w, dtype=np.int32)
            match = arr[q] == arr[q - np.arange(1, q + 1)]  # p = 1..q
            prev = np.zeros(q, dtype=np.int32)
            if len(old) > 1:
                prev[: len(old) - 1] = old[1:]
            runs = np.where(match, prev + 1, 0)
            new[1:] = runs
            # offender iff runs[p-1] >= qq(p)
            pvec = np.arange(1, q + 1)
            if self.strict:
                qqv = (num - den) * pvec // den + 1
            else:
                # forbid exponent >= num/den: l*den >= (num-den)*p
                qqv = -((-(num - den) * pvec) // den)  # ceil
            bad_ord = bool((runs >= qqv).any())
        else:
            bad_ord = False
        self.csuf_stack.append(new)
        # reversed: new pairs (s-q, q) for s = q..2q-1
        oldar = self.ar_stack[-1] if self.ar_stack else np.zeros(0, dtype=np.int32)
        ar = np.zeros(2 * q + 1, dtype=np.int32)  # index by s
        bad_rev = False
        if q >= 1:
            arr = np.asarray(w, dtype=np.int32)
            svec = np.arange(q, 2 * q)  # pairs (s-q, q), p = s-q in 0..q-1
            pvec2 = svec - q
            match2 = arr[pvec2] == arr[q]
            prevar = np.zeros(len(svec), dtype=np.int32)
            m = min(len(oldar), 2 * q)
            # oldar indexed by s (built at length q, s ranged 0..2q-2)
            take = svec[svec < len(oldar)]
            if len(take):
                prevar[: len(take)] = oldar[take]
            runs2 = np.where(match2, prevar + 1, 0)
            ar[svec] = runs2
            # run ends at pair (p, s-p) with p smallest; l = run length;
            # arm start a = p, span G = s - 2a + 1
            l2 = runs2
            Ga = svec - 2 * pvec2 + 1
            ok_pairs = l2 > 0
            if self.strict:
                cond = den * Ga > num * (Ga - l2)
            else:
                cond = den * Ga >= num * (Ga - l2)
            bad_rev = bool(cond[ok_pairs].any()) if ok_pairs.any() else False
        self.ar_stack.append(ar)
        return not (bad_ord or bad_rev)

    def pop(self):
        self.w.pop()
        self.csuf_stack.pop()
        self.ar_stack.pop()
