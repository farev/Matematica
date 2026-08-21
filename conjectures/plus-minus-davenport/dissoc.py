#!/usr/bin/env python3
"""Maximal dissociated sets in finite abelian groups  <=>  D_pm(G) - 1.

A sequence g_1,...,g_l over an additive finite abelian group G is
plus-minus zero-sum free (pm-zsf) if no nonempty I and signs a_i in {+1,-1}
give sum_{i in I} a_i g_i = 0.  Lemma E (NOTE.md): a sequence is pm-zsf iff
its 2^l subset sums are pairwise distinct as indexed subsets, i.e. iff it is
a *dissociated set* (in particular: no repeats, no 0, never both g and -g).
Hence

    D_pm(G) = lmax(G) + 1,   lmax(G) = max size of a dissociated subset.

Bounds:  sum_i floor(log2 n_i)  <=  lmax(+C_{n_i})  and  2^lmax <= |G|.

Groups are given by their list of cyclic factor sizes, e.g. [5, 15].
Elements are mixed-radix indices 0..|G|-1 (coordinate x_j has stride
prod of later factor sizes).  All arithmetic is exact integer arithmetic.
"""

import sys
from itertools import combinations, product
from math import prod


# ---------------------------------------------------------------- groups

class Group:
    def __init__(self, factors):
        self.factors = tuple(factors)
        self.n = prod(factors) if factors else 1
        # strides for mixed radix
        strides = []
        s = 1
        for f in reversed(factors):
            strides.append(s)
            s *= f
        self.strides = tuple(reversed(strides))

    def coords(self, x):
        return tuple((x // s) % f for f, s in zip(self.factors, self.strides))

    def index(self, cs):
        return sum((c % f) * s for c, f, s in zip(cs, self.factors, self.strides))

    def add(self, x, y):
        return self.index([a + b for a, b in
                           zip(self.coords(x), self.coords(y))])

    def neg(self, x):
        return self.index([-a for a in self.coords(x)])

    def add_table(self):
        """Flat list-of-lists addition table; also neg table."""
        n = self.n
        add = [[0] * n for _ in range(n)]
        for x in range(n):
            cx = self.coords(x)
            for y in range(x, n):
                cy = self.coords(y)
                z = self.index([a + b for a, b in zip(cx, cy)])
                add[x][y] = z
                add[y][x] = z
        negs = [self.neg(x) for x in range(n)]
        return add, negs

    def class_reps(self):
        """One representative per {g, -g} class, g != 0, ascending."""
        reps = []
        for g in range(1, self.n):
            if g <= self.neg(g):
                reps.append(g)
        return reps

    def __repr__(self):
        return "C" + "+C".join(str(f) for f in self.factors)


# ------------------------------------------------- definition-level check

def is_dissociated(G, elems):
    """All 2^l subset sums pairwise distinct (definition of dissociated)."""
    seen = set()
    for mask in range(1 << len(elems)):
        s = 0
        m = mask
        i = 0
        while m:
            if m & 1:
                s = G.add(s, elems[i])
            m >>= 1
            i += 1
        if s in seen:
            return False
        seen.add(s)
    return True


def is_pm_zsf_sequence(G, seq):
    """Direct definition: no nonempty sub-multiset with signs summing to 0.

    Independent of Lemma E -- iterates over all sign patterns in
    {-1, 0, +1}^l \\ {0}.  Used to validate the lemma computationally.
    """
    l = len(seq)
    for signs in product((-1, 0, 1), repeat=l):
        if all(s == 0 for s in signs):
            continue
        tot = 0
        for a, g in zip(signs, seq):
            if a == 1:
                tot = G.add(tot, g)
            elif a == -1:
                tot = G.add(tot, G.neg(g))
        if tot == 0:
            return False
    return True


def lmax_bruteforce(G, cap=None):
    """Max dissociated set size by raw combinations over class reps."""
    reps = G.class_reps()
    if cap is None:
        cap = G.n.bit_length() - 1  # floor(log2 n)
    best, best_set = 0, ()
    for k in range(1, cap + 1):
        found = False
        for c in combinations(reps, k):
            if is_dissociated(G, c):
                best, best_set = k, c
                found = True
                break
        if not found:
            break
    return best, best_set


def lmax_pm_sequence_bruteforce(G, cap=None):
    """Max pm-zsf SEQUENCE length by the raw definition, allowing repeats
    and all of G \\ handled naturally (0 allowed as candidate, will fail).
    Exponential; tiny groups only.  Validates Lemma E end to end."""
    if cap is None:
        cap = G.n.bit_length() - 1
    elems = list(range(G.n))
    best, best_seq = 0, ()
    for k in range(1, cap + 2):   # +1 above cap: lemma says none exists
        found = False
        # multisets: nondecreasing sequences
        for seq in combinations_with_replacement_fast(elems, k):
            if is_pm_zsf_sequence(G, seq):
                best, best_seq = k, seq
                found = True
                break
        if not found:
            break
    return best, best_seq


def combinations_with_replacement_fast(elems, k):
    from itertools import combinations_with_replacement
    return combinations_with_replacement(elems, k)


# ------------------------------------------------------------ DFS engine

def lmax_dfs(G, need=None, verbose=False):
    """Maximal dissociated set via DFS over class reps in ascending order.

    Incremental state: sums = set of subset sums so far (size 2^depth).
    Adding g is legal iff sums and {s+g} are disjoint.

    If `need` is given, stop as soon as a dissociated set of that size is
    found (returns (need, witness, nodes)); if the search completes without
    reaching `need`, the exhaustion proves lmax < need and the true max
    found is returned.  Node count = number of legal partial sets visited.
    """
    add, negs = G.add_table()
    reps = G.class_reps()
    cap = G.n.bit_length() - 1
    target = cap if need is None else need
    best = 0
    best_set = ()
    nodes = 0
    R = len(reps)
    stack_set = []

    def extend(start, sums):
        nonlocal best, best_set, nodes
        if best >= target:
            return True
        depth = len(stack_set)
        # not enough classes left to beat best
        if depth + (R - start) <= best:
            return False
        for idx in range(start, R):
            if best >= target:
                return True
            g = reps[idx]
            row = add[g]
            new = [row[s] for s in sums]
            # disjointness <=> dissociated after adding g
            ok = True
            for s in new:
                if s in sums:
                    ok = False
                    break
            if not ok:
                continue
            nodes += 1
            stack_set.append(g)
            if depth + 1 > best:
                best = depth + 1
                best_set = tuple(stack_set)
                if best >= target:
                    return True
            extend(idx + 1, sums | set(new))
            stack_set.pop()
        return False

    extend(0, {0})
    return best, best_set, nodes


# ------------------------------------------------------- group generation

def partitions(n):
    """All partitions of integer n as nonincreasing tuples."""
    if n == 0:
        yield ()
        return
    def gen(n, maxpart):
        if n == 0:
            yield ()
            return
        for first in range(min(n, maxpart), 0, -1):
            for rest in gen(n - first, first):
                yield (first,) + rest
    yield from gen(n, n)


def abelian_groups_of_order(n):
    """All abelian groups of order n, primary decomposition, as factor
    lists (prime-power cyclic factors, ascending)."""
    # factor n
    fac = {}
    m = n
    d = 2
    while d * d <= m:
        while m % d == 0:
            fac[d] = fac.get(d, 0) + 1
            m //= d
        d += 1
    if m > 1:
        fac[m] = fac.get(m, 0) + 1
    choices = []
    for p, e in sorted(fac.items()):
        opts = []
        for part in partitions(e):
            opts.append(tuple(p ** k for k in part))
        choices.append(opts)
    for combo in product(*choices):
        factors = []
        for tup in combo:
            factors.extend(tup)
        yield sorted(factors)


def invariant_factors(factors):
    """Canonical invariant-factor form d_1 | d_2 | ... of a factor list."""
    from collections import defaultdict
    prim = defaultdict(list)
    for f in factors:
        # split f into prime powers
        m = f
        d = 2
        while d * d <= m:
            e = 0
            while m % d == 0:
                e += 1
                m //= d
            if e:
                prim[d].append(d ** e)
            d += 1
        if m > 1:
            prim[m].append(m)
    for p in prim:
        prim[p].sort()
    out = []
    while any(prim.values()):
        d = 1
        for p in list(prim):
            if prim[p]:
                d *= prim[p].pop()
        out.append(d)
    return tuple(sorted(out))


# ----------------------------------------------------------------- tests

def run_controls():
    ok = True

    # Lemma E validation: pm-zsf sequences vs dissociated sets, tiny groups
    for factors in ([6], [8], [2, 4], [3, 3], [12], [2, 2, 3], [5], [10]):
        G = Group(factors)
        a, _ = lmax_bruteforce(G)
        b, _ = lmax_pm_sequence_bruteforce(G)
        status = "ok" if a == b else "MISMATCH"
        if a != b:
            ok = False
        print(f"lemma-E {G}: dissociated max {a}, pm-zsf sequence max {b} "
              f"[{status}]")

    # positive controls: proved formulas
    for n in range(2, 40):
        G = Group([n])
        a, _, _ = lmax_dfs(G)
        want = n.bit_length() - 1
        if a != want:
            ok = False
            print(f"CONTROL FAIL cyclic C{n}: got {a}, want {want}")
    print("control cyclic C2..C39: lmax = floor(log2 n)  [ok]")

    # C2^r attains its cap early (search stops at first witness); C3^r
    # requires FULL exhaustion above r, whose tree is ~all independent
    # sets -- Python-feasible only to r = 4 (r = 5 is for the C engine).
    for r in range(1, 7):
        G = Group([2] * r)
        a, _, _ = lmax_dfs(G)
        if a != r:
            ok = False
            print(f"CONTROL FAIL C2^{r}: got {a}, want {r}")
    for r in range(1, 5):
        G = Group([3] * r)
        a, _, _ = lmax_dfs(G)
        if a != r:
            ok = False
            print(f"CONTROL FAIL C3^{r}: got {a}, want {r}")
    print("control C2^r (r<=6), C3^r (r<=4): lmax = r  [ok]")

    # negative control: a planted non-dissociated set must be rejected
    G = Group([5, 15])
    bad = (G.index((1, 0)), G.index((2, 0)), G.index((3, 0)))  # 1+2=3
    if is_dissociated(G, bad):
        ok = False
        print("NEGATIVE CONTROL FAIL: planted relation accepted")
    else:
        print("negative control (planted 1+2=3 in C5+C15 rejected)  [ok]")

    # DFS agrees with raw brute force on assorted small groups
    for factors in ([9], [3, 9], [2, 2, 5], [25], [4, 4], [2, 16], [7, 7]):
        G = Group(factors)
        a, _, _ = lmax_dfs(G)
        b, _ = lmax_bruteforce(G)
        if a != b:
            ok = False
            print(f"CONTROL FAIL {G}: dfs {a} vs brute {b}")
    print("control dfs == bruteforce on 7 assorted groups  [ok]")

    print("ALL CONTROLS PASS" if ok else "CONTROL FAILURES -- DO NOT TRUST")
    return ok


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "controls":
        sys.exit(0 if run_controls() else 1)
    # ad hoc: dissoc.py f1 f2 ... [need=k]
    args = [a for a in sys.argv[1:] if not a.startswith("need=")]
    need = None
    for a in sys.argv[1:]:
        if a.startswith("need="):
            need = int(a.split("=")[1])
    G = Group([int(a) for a in args])
    cap = G.n.bit_length() - 1
    lower = sum(f.bit_length() - 1 for f in G.factors)
    print(f"{G}: order {G.n}, product lower bound {lower}, cap {cap}")
    best, bset, nodes = lmax_dfs(G, need=need)
    print(f"lmax = {best}  witness (coords) = "
          f"{[G.coords(g) for g in bset]}  nodes = {nodes}")
    print(f"=> D_pm({G}) = {best + 1}")
