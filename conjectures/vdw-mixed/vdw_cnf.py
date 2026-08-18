"""CNF encoder for mixed two-color van der Waerden numbers w(2; s, t).

Definitions (Landman-Robertson convention):
  w(2; s, t) = least n such that EVERY 2-coloring of [1, n] contains
  an s-term arithmetic progression monochromatic in color 0, or a
  t-term arithmetic progression monochromatic in color 1.

A "good partition" of [1, n] is a 2-coloring with no s-AP in color 0 and
no t-AP in color 1.  Good partitions of [1, n] exist iff n <= w(2;s,t) - 1.
Restriction of a good partition of [1,n] to [1,m], m < n, is good, so
SAT/UNSAT is monotone in n and boundary-only certification is sound:
  SAT witness at n = w-1  +  UNSAT proof at n = w   ==>   w(2;s,t) = w.

Encoding: variable x_i (DIMACS index i) for i in [1, n];
x_i = TRUE  means i has color 1 (the t side),
x_i = FALSE means i has color 0 (the s side).
For every s-AP  (a, a+d, ..., a+(s-1)d) in [1,n]:  clause  ( x_a | ... | x_{a+(s-1)d} )
For every t-AP  (a, a+d, ..., a+(t-1)d) in [1,n]:  clause  (~x_a | ... | ~x_{a+(t-1)d} )

AP count identity used as an encoder self-check:
  #{k-APs in [1,n] with d >= 1} = sum_{d=1}^{floor((n-1)/(k-1))} (n - (k-1)d).
"""

import sys


def aps(n: int, k: int):
    """All k-term APs (as tuples) in [1, n] with common difference >= 1."""
    out = []
    if k < 2:
        raise ValueError("k >= 2 required")
    dmax = (n - 1) // (k - 1)
    for d in range(1, dmax + 1):
        for a in range(1, n - (k - 1) * d + 1):
            out.append(tuple(a + i * d for i in range(k)))
    return out


def ap_count_formula(n: int, k: int) -> int:
    dmax = (n - 1) // (k - 1)
    return sum(n - (k - 1) * d for d in range(1, dmax + 1))


def vdw_clauses(n: int, s: int, t: int):
    """Clause list for 'a good partition of [1,n] for (s,t) exists'."""
    cls = []
    for ap in aps(n, s):
        cls.append([i for i in ap])          # not all color 0
    for ap in aps(n, t):
        cls.append([-i for i in ap])         # not all color 1
    return cls


def write_dimacs(path: str, n: int, clauses) -> None:
    with open(path, "w") as f:
        f.write(f"p cnf {n} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")


def coloring_is_good(coloring, s: int, t: int) -> bool:
    """Independent witness check: coloring is a 0/1 sequence indexed 1..n.

    Deliberately re-enumerates APs by nested loops over (a, d) and checks
    monochromaticity positionwise; shares no code path with vdw_clauses.
    """
    n = len(coloring) - 1  # coloring[0] unused
    for d in range(1, (n - 1) // (s - 1) + 1):
        for a in range(1, n - (s - 1) * d + 1):
            if all(coloring[a + i * d] == 0 for i in range(s)):
                return False
    for d in range(1, (n - 1) // (t - 1) + 1):
        for a in range(1, n - (t - 1) * d + 1):
            if all(coloring[a + i * d] == 1 for i in range(t)):
                return False
    return True


def brute_force_good_exists(n: int, s: int, t: int) -> bool:
    """Zero-cleverness decider for tiny n: try all 2^n colorings."""
    for mask in range(1 << n):
        col = [0] * (n + 1)
        for i in range(1, n + 1):
            col[i] = (mask >> (i - 1)) & 1
        if coloring_is_good(col, s, t):
            return True
    return False


def brute_force_w(s: int, t: int, nmax: int = 22):
    """w(2;s,t) by brute force if it is <= nmax, else None."""
    for n in range(1, nmax + 1):
        if not brute_force_good_exists(n, s, t):
            return n
    return None


if __name__ == "__main__":
    # Self-checks. 1) AP count formula vs enumeration.
    ok = True
    for n in (10, 37, 100):
        for k in (3, 4, 5, 8):
            a, b = len(aps(n, k)), ap_count_formula(n, k)
            if a != b:
                ok = False
                print(f"AP COUNT MISMATCH n={n} k={k}: enum {a} formula {b}")
    print("AP-count self-check:", "OK" if ok else "FAILED")

    # 2) Brute-force controls on tiny known values:
    #    w(2;3,3) = 9  (classical W(2,3))
    #    w(2;2,t) = 2t-1? no -- w(2;2,t): 2-APs are any pair, so color-0 class
    #    has at most 1 element; known w(2;2,t) = 2t - 1 ... we do NOT rely on
    #    this from memory: brute force IS the ground truth here, we print it.
    print("brute w(2;3,3) =", brute_force_w(3, 3), "(published: 9)")
    print("brute w(2;2,4) =", brute_force_w(2, 4), "(sanity, small)")
    print("brute w(2;3,4) =", brute_force_w(3, 4, nmax=19), "(published: 18)")
