"""Implementation D: stratified verification that no pm-zero-sum-free 6-set
exists over G = C5 x C15, following the proof strata of NOTE.md Theorem 1.

Write G = C5 + C5 + C3 (CRT on the C15 factor), H = 5-torsion subgroup
(= C5 + C5), pi : G -> C3 the projection. A pm-zsf 6-set S splits as
t0 = |S ∩ H| elements of H and t1 = 6 - t0 elements outside; after per-element
sign normalization every outside element has pi = +1, and the outside
sigma-parts x_i in C5^2 are pairwise distinct. The constraints, per stratum
(T = S ∩ H must itself be pm-zsf in H, all values below must avoid
R(T) ∪ {0}):

  t1 = 2: x1 - x2
  t1 = 3: differences x_i - x_j and the triple sum x1+x2+x3
  t1 = 4: differences; all 4 triple sums; the 3 balanced sums x_i+x_j-x_k-x_l
  t1 = 5: differences; triple sums; balanced 2+2- sums; the five 4+1- sums
          x_i+x_j+x_k+x_l-x_m
  t1 = 6: as above plus the 3+3- sums and the full sum x1+...+x6
          (coefficient patterns eps in {-1,0,1}^t1 with sum(eps) = 0 mod 3)

This is a fourth implementation: no reachable-set DFS (impl A/C), no global
combination sweep (impl B). Exact integer arithmetic.

Run: python3 verify_strata.py  -> per-stratum counts; total must be 0.
"""

from itertools import combinations, product

M = 5


def h_add(a, b):
    return ((a[0] + b[0]) % M, (a[1] + b[1]) % M)


def h_neg(a):
    return ((-a[0]) % M, (-a[1]) % M)


H = [(a, b) for a in range(M) for b in range(M)]
H0 = tuple([0, 0])


def reach(T):
    R = set()
    for signs in product((-1, 0, 1), repeat=len(T)):
        if all(s == 0 for s in signs):
            continue
        R.add(tuple(sum(s * e[j] for s, e in zip(signs, T)) % M for j in range(2)))
    return R


def class_reps():
    reps, seen = [], set()
    for t in H:
        if t == (0, 0) or t in seen:
            continue
        seen.add(t)
        seen.add(h_neg(t))
        reps.append(min(t, h_neg(t)))
    return reps


REPS = class_reps()
assert len(REPS) == 12


def balanced_patterns(k):
    """Sign patterns eps in {-1,0,1}^k, eps != 0, sum(eps) % 3 == 0, first
    nonzero = +1 (global-sign quotient)."""
    out = []
    for s in product((-1, 0, 1), repeat=k):
        nz = [x for x in s if x != 0]
        if not nz or nz[0] != 1:
            continue
        if sum(s) % 3 != 0:
            continue
        out.append(s)
    return out


def stratum_count(t0, t1):
    """Number of pm-zsf 6-sets with |S ∩ H| = t0 (0 means: how many violating
    configurations exist; the theorem needs 0)."""
    pats = balanced_patterns(t1)
    total = 0
    # T ranges over pm-zsf t0-subsets of class reps of H
    tsets = []
    for T in combinations(REPS, t0):
        R = reach(T)
        if (0, 0) in R:
            continue
        tsets.append((T, R | {(0, 0)}))
    if t0 == 0:
        tsets = [((), {(0, 0)})]
    for T, Rf in tsets:
        # outside sigma-parts: distinct elements of C5^2 (all 25 allowed)
        for X in combinations(H, t1):
            ok = True
            for s in pats:
                v = tuple(sum(c * x[j] for c, x in zip(s, X)) % M for j in range(2))
                if v in Rf:
                    ok = False
                    break
            if ok:
                total += 1
    return len(tsets), total


if __name__ == "__main__":
    grand = 0
    for t0, t1 in ((4, 2), (3, 3), (2, 4), (1, 5), (0, 6)):
        nt, bad = stratum_count(t0, t1)
        grand += bad
        print(f"stratum (t0={t0}, t1={t1}): {nt} pm-zsf kernel sets; "
              f"admissible outside configurations: {bad}")
    print(f"\nTOTAL admissible 6-set configurations: {grand} "
          f"({'THEOREM CONFIRMED' if grand == 0 else 'CONTRADICTION!'})")
