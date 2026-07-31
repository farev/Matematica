"""Shared machinery for the R3 session (REDUCTION.md Open Problem R3).

Conventions (match reduction_check.py):
  - top row a_0, a_1, ... nonnegative integers (normalized gaps);
    background model: geometric(1-theta) - 1, theta = 1 - 2/log(1e8).
  - iteration: row^{s+1}_i = |row^s_{i+1} - row^s_i|; lead of depth s is cell (s, 0).
  - a plant at index m influences the lead first at depth m.
  - erosion path of a plant at m: cells (s, m-1-s), s = 0..m-1 (all strictly
    left of the plant, so plant-independent).

Parity machinery:
  - parity of cell (s, n) = XOR_{t subset s} y_{n+t}   (Lucas; |x-y| = x+y mod 2)
  - with y'_u = y_{m-1-u} (prefix read right-to-left from the plant) and
    S[s, u] = C(s, u) mod 2, the path-cell parity at depth s is exactly
    z_s = (S y')_s.  S is involutive: S^2 = I over F_2.
"""

import numpy as np

THETA = 1 - 2 / np.log(1e8)


def sierpinski(m):
    """S[s, u] = C(s, u) mod 2 (1 iff u is a binary submask of s), m x m uint8."""
    idx = np.arange(m, dtype=np.uint64)
    return ((idx[None, :] & idx[:, None]) == idx[None, :]).astype(np.uint8)


def parity_triangle(y, rows):
    """XOR-Pascal evolution of a 0/1 array; returns list of rows (row 0 = y)."""
    t = [np.asarray(y, dtype=np.uint8)]
    for _ in range(rows):
        r = t[-1]
        t.append(r[:-1] ^ r[1:])
    return t


def value_rows(a, rows):
    """Absolute-difference evolution; returns list of rows (row 0 = a)."""
    t = [np.asarray(a, dtype=np.int64)]
    for _ in range(rows):
        r = t[-1]
        t.append(np.abs(r[1:] - r[:-1]))
    return t


def lead_trace(a, rows):
    """Leads of depths 1..rows without storing the triangle."""
    x = np.asarray(a, dtype=np.int64).copy()
    leads = np.empty(rows, dtype=np.int64)
    for s in range(rows):
        x = np.abs(x[1:] - x[:-1])
        leads[s] = x[0]
    return leads


def path_values(a, m):
    """Values of the erosion-path cells (s, m-1-s), s = 0..m-1."""
    x = np.asarray(a, dtype=np.int64).copy()
    out = np.empty(m, dtype=np.int64)
    out[0] = x[m - 1]
    for s in range(1, m):
        x = np.abs(x[1:] - x[:-1])
        out[s] = x[m - 1 - s]
    return out


def path_parity_direct(y, m):
    """Parities of path cells via the XOR iteration (ground truth)."""
    t = np.asarray(y, dtype=np.uint8).copy()
    out = np.empty(m, dtype=np.uint8)
    out[0] = t[m - 1]
    for s in range(1, m):
        t = t[:-1] ^ t[1:]
        out[s] = t[m - 1 - s]
    return out


def z_transform(y_prefix):
    """z = S . rev(y_prefix) over F_2, via the XOR-Pascal rows (O(m^2) bitwise)."""
    yr = np.asarray(y_prefix, dtype=np.uint8)[::-1]
    m = len(yr)
    S = sierpinski(m)
    return (S @ yr.astype(np.uint64) % 2).astype(np.uint8)


def conditioned_geometric(parities, rng, theta=THETA):
    """Sample a_i ~ (geometric(1-theta) - 1) conditioned on a_i mod 2 = parities[i].

    Exact: a = 2*(geometric(1-theta^2) - 1) + parity.
    """
    parities = np.asarray(parities, dtype=np.int64)
    g = rng.geometric(1 - theta ** 2, size=len(parities)).astype(np.int64) - 1
    return 2 * g + parities


def de_bruijn(order):
    """Binary de Bruijn sequence B(2, order) as a uint8 array of length 2^order
    (Lyndon-word concatenation)."""
    seq = []
    a = [0] * (order + 1)

    def db(t, p):
        if t > order:
            if order % p == 0:
                seq.extend(a[1:p + 1])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, 2):
                a[t] = j
                db(t + 1, t)

    db(1, 1)
    return np.array(seq, dtype=np.uint8)


def anchored_periodic(m, block):
    """Parity string y of length m, right-anchored periodic:
    y[m-1-u] = block[u mod len(block)]."""
    P = len(block)
    u = np.arange(m)
    y = np.empty(m, dtype=np.uint8)
    y[m - 1 - u] = block[u % P]
    return y


def window_counts(x, k):
    """Counts of all k-windows of an integer array, as a dict pattern -> count."""
    from collections import Counter
    x = np.asarray(x)
    n = len(x) - k + 1
    base = int(x.max()) + 1
    code = np.zeros(n, dtype=np.int64)
    for j in range(k):
        code = code * base + x[j:j + n]
    cnt = Counter(code.tolist())
    return cnt, base
