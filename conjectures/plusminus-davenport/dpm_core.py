"""Plus-minus weighted Davenport constants of finite abelian groups: core engine.

Implementation A (canonical). Exact integer arithmetic throughout; no floats
anywhere in any decision path.

Definitions (NOTE.md, Section 2):
  A sequence over G is a finite multiset. S is +-zero-sum-free (pm-zsf) if no
  nonempty subsequence T with signs eps_i in {+1,-1} has sum(eps_i t_i) = 0.
  d_pm(G) = maximum length of a pm-zsf sequence; D_pm(G) = d_pm(G) + 1.

Reductions used (proved in NOTE.md, Lemma R):
  * 0 never occurs in a pm-zsf sequence (weight +1 on it alone).
  * No element repeats (g, g with signs +1,-1 sums to 0), and g, -g never
    co-occur (signs +1,+1). Hence pm-zsf sequences are exactly SETS containing
    at most one element per sign class {g,-g}, and replacing an element by its
    negative preserves pm-zsf-ness. The search runs over subsets of class
    representatives.
  * Reachable-set recursion: with R(S) = { sum over nonempty T <= S with signs },
    R(S + g) = R(S) union (R(S)+g) union (R(S)-g) union {g,-g}; S+g pm-zsf
    iff 0 not in R(S+g). R is monotone under extension, so pruning a prefix
    whose R contains 0 is sound.

Search: depth-first over class representatives in increasing index order;
visits every pm-zsf subset exactly once; therefore "no pm-zsf set of size k
found" with exhaustive=True is a certificate that d_pm < k.
"""

from itertools import product
from math import gcd, prod
import json
import sys
import time


def floor_log2(n: int) -> int:
    assert n >= 1
    return n.bit_length() - 1


def invariant_factors(moduli):
    """Invariant-factor decomposition d_1 | d_2 | ... of prod Z_m."""
    # collect primary components
    primary = {}  # prime -> sorted list of exponents (descending)
    for m in moduli:
        mm = m
        d = 2
        while d * d <= mm:
            while mm % d == 0:
                e = 0
                while mm % d == 0:
                    mm //= d
                    e += 1
                primary.setdefault(d, []).append(e)
            d += 1
        if mm > 1:
            primary.setdefault(mm, []).append(1)
    for p in primary:
        primary[p].sort(reverse=True)
    r = max((len(v) for v in primary.values()), default=0)
    facs = []
    for i in range(r):
        f = 1
        for p, exps in primary.items():
            if i < len(exps):
                f *= p ** exps[i]
        facs.append(f)
    facs.sort()
    return facs  # ascending, each divides the next


class AbelianGroup:
    def __init__(self, moduli):
        self.moduli = tuple(int(m) for m in moduli)
        assert all(m >= 1 for m in self.moduli)
        self.N = prod(self.moduli)
        self.r = len(self.moduli)
        # mixed-radix indexing: index = sum a_i * radix_i
        self.radix = []
        acc = 1
        for m in reversed(self.moduli):
            self.radix.append(acc)
            acc *= m
        self.radix.reverse()
        # tables
        self.neg = [self.idx(tuple((-a) % m for a, m in zip(self.tup(e), self.moduli)))
                    for e in range(self.N)]
        self.ADD = [None] * self.N
        for g in range(self.N):
            tg = self.tup(g)
            row = [0] * self.N
            for h in range(self.N):
                th = self.tup(h)
                row[h] = self.idx(tuple((a + b) % m for a, b, m in zip(tg, th, self.moduli)))
            self.ADD[g] = row
        self.classes = [g for g in range(1, self.N) if g <= self.neg[g]]
        self.invfacs = invariant_factors(self.moduli)

    def tup(self, e):
        out = []
        for m, rad in zip(self.moduli, self.radix):
            out.append((e // rad) % m)
        return tuple(out)

    def idx(self, t):
        return sum(a * rad for a, rad in zip(t, self.radix))

    def name(self):
        return " x ".join(f"C{m}" for m in self.moduli)

    # ---- elementary bounds (proved in NOTE.md) ----
    def lower_d(self):
        """L5/L6: d_pm >= sum floor(log2 d_i) over invariant factors."""
        return sum(floor_log2(f) for f in self.invfacs)

    def upper_d(self):
        """L4 pigeonhole: d_pm <= floor(log2 |G|)."""
        return floor_log2(self.N)


def search_dpm(G: AbelianGroup, stop_size=None, collect_max=False, node_cap=None):
    """Exhaustive DFS over pm-zsf subsets of class representatives.

    The reachable set R is held as a numpy boolean indicator vector over G;
    all operations are boolean/index arithmetic (exact; no floats).
    ind_{R+g}[i] = ind_R[i-g], realized by the precomputed permutation
    SUB[g][i] = index(i - g).

    Returns dict with:
      dpm         largest pm-zsf set size found
      witness     one pm-zsf set of that size (element tuples)
      nodes       number of pm-zsf subsets visited (including empty set)
      exhaustive  True iff no cap terminated the search early
      maxsets     all pm-zsf sets of size dpm (only if collect_max)
    If stop_size is given, stops as soon as a pm-zsf set of that size is found
    (existence mode; exhaustive=False in that case unless tree exhausted).
    """
    import numpy as np

    neg = G.neg
    ADD = G.ADD
    classes = G.classes
    N = G.N
    # SUB[g][i] = i - g ; then (R+g) = R[SUB[g]]
    SUB = {}
    for g in set(classes) | {neg[c] for c in classes}:
        ng = neg[g]
        SUB[g] = np.array([ADD[i][ng] for i in range(N)], dtype=np.int64)
    state = {"nodes": 0, "best": 0, "wit": [], "capped": False, "stopped": False}
    maxsets = [] if collect_max else None

    def rec(start, chosen, R):
        state["nodes"] += 1
        if node_cap is not None and state["nodes"] > node_cap:
            state["capped"] = True
            return
        k = len(chosen)
        if k > state["best"]:
            state["best"] = k
            state["wit"] = list(chosen)
            if collect_max:
                maxsets.clear()
        if collect_max and k == state["best"] and k > 0:
            maxsets.append(list(chosen))
        if stop_size is not None and k >= stop_size:
            state["stopped"] = True
            return
        for i in range(start, len(classes)):
            g = classes[i]
            ng = neg[g]
            newR = R | R[SUB[g]] | R[SUB[ng]]
            newR[g] = True
            newR[ng] = True
            if newR[0]:
                continue
            rec(i + 1, chosen + [g], newR)
            if state["capped"] or state["stopped"]:
                return

    rec(0, [], np.zeros(N, dtype=bool))
    res = {
        "moduli": list(G.moduli),
        "invariant_factors": G.invfacs,
        "order": G.N,
        "dpm": state["best"],
        "witness": [G.tup(g) for g in state["wit"]],
        "nodes": state["nodes"],
        "exhaustive": (not state["capped"]) and (not state["stopped"]),
        "lower_d_bound": G.lower_d(),
        "upper_d_bound": G.upper_d(),
    }
    if collect_max:
        res["maxsets"] = [[G.tup(g) for g in s] for s in maxsets]
        res["n_maxsets"] = len(maxsets)
    return res


def verify_pm_zsf(moduli, elems):
    """Independent-style direct check that elems (list of tuples) is pm-zsf.

    Checks all 3^k - 1 signed nonempty subset sums directly. Used for witness
    verification inside reports; verify_witness.py repeats this standalone.
    """
    k = len(elems)
    moduli = tuple(moduli)
    for signs in product((-1, 0, 1), repeat=k):
        if all(s == 0 for s in signs):
            continue
        acc = tuple(sum(s * e[j] for s, e in zip(signs, elems)) % m
                    for j, m in enumerate(moduli))
        if all(a == 0 for a in acc):
            return False, signs
    return True, None


def report_group(moduli, stop_size=None, collect_max=False, node_cap=None, quiet=False):
    t0 = time.time()
    G = AbelianGroup(moduli)
    res = search_dpm(G, stop_size=stop_size, collect_max=collect_max, node_cap=node_cap)
    res["seconds"] = round(time.time() - t0, 3)
    res["Dpm"] = res["dpm"] + 1 if res["exhaustive"] else None
    if res["witness"]:
        ok, bad = verify_pm_zsf(G.moduli, res["witness"])
        assert ok, f"witness failed verification! signs={bad}"
        res["witness_verified"] = True
    if not quiet:
        print(json.dumps(res, default=str))
    return res


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    moduli = [int(a) for a in args]
    collect = "--all-max" in flags
    report_group(moduli, collect_max=collect)
