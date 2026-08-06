"""Pansiot-code toolkit for circular threshold words (session 2026-08-06).

Conventions (fixed by validation against the repository's own data; see
data/pansiot_validation.log):

* Sigma_n = {0..n-1}, alpha = RT(n): 7/4 at n=3, 7/5 at n=4, n/(n-1) at n>=5.
* A word is *valid* if every n-1 consecutive letters are pairwise distinct.
  Every alpha+-free word is valid (q(p)=1 for p <= n-2).
* State before emitting a letter: the tuple (a_1..a_{n-1} | b) of the last
  n-1 letters (oldest first) plus the missing letter -- an element of Sym(n).
* Steps: bit 0 emits a_1 (recurrence at distance n-1), new state
  (a_2..a_{n-1}, a_1 | b) = old . tau0;  bit 1 emits b (the fresh letter),
  new state (a_2..a_{n-1}, b | a_1) = old . tau1, where
      tau0 = (1..n-1 -> 2..n-1,1; n -> n)   [(n-1)-cycle on window slots]
      tau1 = the n-cycle (1 2 ... n).
  States compose on the right: g(w) = tau_{w_1} o ... o tau_{w_L},
  (a o b)[i] = a[b[i]].
* decode(bits) = canonical initial window (0..n-2) followed by the emitted
  letters; the equal-letter pattern of the result is intrinsic to the bits
  (Lemma S: letter at bit t equals s0[H_t[pos(c_t)]] with H_t the prefix
  monodromy and pos(0)=0, pos(1)=n-1), so freeness of a decode is a property
  of the bit word alone: "code-free".
* code_free includes the initial window in the check; this is exactly the
  in-context requirement (the artificial window plays the role of the n-1
  letters that precede any occurrence).
"""
from itertools import permutations
from fractions import Fraction


def alpha_of(n):
    if n == 3:
        return (7, 4)
    return (7, 5) if n == 4 else (n, n - 1)


def make_taus(n):
    tau0 = tuple(list(range(1, n - 1)) + [0, n - 1])
    tau1 = tuple(list(range(1, n)) + [0])
    return tau0, tau1


def comp(a, b):
    return tuple(a[b[i]] for i in range(len(a)))


def g_of(bits, tau0, tau1):
    n = len(tau0)
    acc = tuple(range(n))
    for c in bits:
        acc = comp(acc, tau1 if c else tau0)
    return acc


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
    """word over Sigma_n with all (n-1)-windows rainbow -> (bits, True),
    starting from the word's own first n-1 letters."""
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


def is_afree(x, num, den):
    """No factor of exponent > num/den.  Run-based; exact integers."""
    L = len(x)
    for p in range(1, L):
        qq = (num * p) // den + 1 - p
        run = 0
        for j in range(L - p):
            if x[j] == x[j + p]:
                run += 1
                if run >= qq:
                    return False
            else:
                run = 0
    return True


def code_free(bits, n, num, den):
    return is_afree(decode(bits, n), num, den)


def valid_blocks(n, num, den, k):
    """All code-free bit words of length exactly k."""
    res = []

    def rec(bits):
        if len(bits) == k:
            res.append(tuple(bits))
            return
        for b in (0, 1):
            bits.append(b)
            if code_free(bits, n, num, den):
                rec(bits)
            bits.pop()

    rec([])
    return res


def all_codefree_upto(n, num, den, N):
    out = []

    def rec(w):
        if w:
            out.append(tuple(w))
        if len(w) == N:
            return
        for b in (0, 1):
            w.append(b)
            if code_free(w, n, num, den):
                rec(w)
            w.pop()

    rec([])
    return out


def circular_afree(w, num, den):
    """Circular alpha+-freeness from Definition 1 (NOTE.md section 1):
    no p >= 1 with L(p) = floor(alpha p)+1 <= m and a cyclic run of
    q(p) = L(p)-p matches at distance p."""
    m = len(w)
    for p in range(1, m):
        Lp = (num * p) // den + 1
        if Lp > m:
            break
        qq = Lp - p
        for i in range(m):
            if all(w[(i + j) % m] == w[(i + j + p) % m] for j in range(qq)):
                return False, (p, i)
    return True, None


def decode_cycle(bits_cycle, n):
    """Decode a monodromy-id cyclic codeword to a circular word (canonical
    start state; asserts closure)."""
    st = list(range(n))
    out = []
    for c in bits_cycle:
        if c == 0:
            x = st[0]
            st = st[1 : n - 1] + [st[0], st[n - 1]]
        else:
            x = st[n - 1]
            st = st[1 : n - 1] + [st[n - 1], st[0]]
        out.append(x)
    assert st == list(range(n)), "monodromy is not id; cycle does not close"
    return out
