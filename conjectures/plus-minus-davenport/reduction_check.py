#!/usr/bin/env python3
"""reduction_check.py — engine E5: decides dissociated-set existence in
G = Z_p x Z_{3p} = (F_p)^2 x Z_3 via the class-injectivity reduction
(NOTE.md, Lemma R), a mathematically different route from the DFS engines.

Reduction. Seek a dissociated set of size s in Z_p^2 x Z_3. Sign-normalize
so every element has Z_3-part 0 or 1; let S_1 = indices with part 1
(b = |S_1|), S_0 the rest (a = s - b). Then the set is dissociated iff the
tuple (h_1..h_s) in (F_p^2)^s has A -> sum_{i in A} h_i injective on each
class {A : |A cap S_1| = r (mod 3)}, r = 0,1,2.
[Proof in NOTE.md: signed zero-sums <-> subset-sum collisions within a
class, via P = A\\B, N = B\\A.]

For each split (a, b) this enumerates h-tuples directly (S_1 tuples sorted,
S_0 tuples sorted, h in F_p^2 arbitrary — repeats allowed across parts) and
checks the 2^s subset sums. Reports whether any split admits a solution.

Usage: python3 reduction_check.py p s [--count] [--maxsplits N]
Exact integer arithmetic only.
"""
import sys
from itertools import combinations, combinations_with_replacement


def check(p, s, count_solutions=False):
    n = p * p
    els = list(range(n))  # h encoded as x*p + y

    def hsum(idxs):
        x = y = 0
        for h in idxs:
            x += h // p
            y += h % p
        return (x % p) * p + (y % p)

    results = {}
    for b in range(0, s + 1):
        a = s - b
        found = 0
        example = None
        # S_1: b distinct elements of F_p^2 (distinct forced: class-1
        # singletons collide otherwise). S_0: a distinct elements
        # (class-0 singleton collisions force distinctness), disjointness
        # between S_0 and S_1 NOT forced (different classes) — but a
        # repeated h with one copy in each part is allowed; enumerate S_0
        # over all elements independently.
        for s1 in combinations(els, b):
            # early check: class-1 singletons pairwise distinct — by
            # construction; class-2 pairs of S_1 distinct sums — check on
            # the fly below.
            for s0 in combinations(els, a):
                tup = list(s0) + list(s1)
                # classes: |A cap S_1| mod 3; A over all subsets.
                # subset sums by DP over masks: sum[m] = sum[m - lowbit] + h
                seen = [set(), set(), set()]
                sums = [0] * (1 << s)
                cls = [0] * (1 << s)
                okall = True
                seen[0].add(0)
                for mask in range(1, 1 << s):
                    low = mask & (-mask)
                    i = low.bit_length() - 1
                    prev = mask ^ low
                    ps = sums[prev]
                    h = tup[i]
                    x = ps // p + h // p
                    y = ps % p + h % p
                    v = (x % p) * p + (y % p)
                    sums[mask] = v
                    c1 = cls[prev] + (1 if i >= a else 0)
                    cls[mask] = c1
                    v_cl = c1 % 3
                    if v in seen[v_cl]:
                        okall = False
                        break
                    seen[v_cl].add(v)
                if okall:
                    found += 1
                    if example is None:
                        example = (s0, s1)
                    if not count_solutions:
                        break
            if found and not count_solutions:
                break
        results[(a, b)] = (found, example)
        ex = ""
        if example:
            s0e = [(h // p, h % p) for h in example[0]]
            s1e = [(h // p, h % p) for h in example[1]]
            ex = f" example: S0={s0e} S1={s1e}"
        print(f"p={p} size={s} split(a={a},b={b}): "
              f"{'FEASIBLE' if found else 'infeasible'}"
              f"{' count=' + str(found) if count_solutions and found else ''}{ex}",
              flush=True)
    total = sum(1 for f, _ in results.values() if f)
    verdict = "EXISTS" if total else "DOES-NOT-EXIST"
    print(f"p={p}: dissociated set of size {s} in Z_{p} x Z_{3*p}: {verdict}")
    return total > 0


if __name__ == "__main__":
    p = int(sys.argv[1])
    s = int(sys.argv[2])
    check(p, s, count_solutions="--count" in sys.argv)
