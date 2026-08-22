#!/usr/bin/env python3
"""case_audit.py — decomposition audit of L(C_5 ⊕ C_15) = 5, independent of
both search engines.

Works in G = F_5² ⊕ Z_3 (≅ C_5 ⊕ C_15). Any ±free set can be sign-normalized
so every element has t-part in {0, 1} (sign flips preserve freeness). Write
S = S₀ ⊔ S₁ by t-part. Then (Reduction Lemma, NOTE.md):

  S is ±free  ⟺  (i) S₀ = {(u,0)} with the u's a ±free subset of V = F_5²,
               (ii) for every nonempty "balanced" signed subset of S₁
                    (#plus ≡ #minus mod 3) with V-part w:
                    w ∉ {0} ∪ Reach(S₀).

This script certifies, by direct enumeration over V-configurations (never
touching the engines' DFS or reach code):

  A. L(F_5²) = 4: no ±free 5-subset of the 12 sign classes of F_5²;
  B. saturation: every ±free 4-subset of F_5² has Reach = V ∖ {0}
     (this alone kills case |S₀| = 4 — the hand proof of NOTE Lemma 5);
  C. cases (|S₀|, |S₁|) = (4,2), (3,3), (2,4), (1,5), (0,6) are all empty:
     no configuration passes (i)+(ii). Hence no ±free 6-set exists in G and
     D±(C_5 ⊕ C_15) = 6, given the (engine-independent) Reduction Lemma.

Also prints near-miss statistics per case (minimum number of violated
constraints over all configurations) to guide the hand proof.
"""
import sys
from itertools import combinations, product

p = 5
V = [(a, b) for a in range(p) for b in range(p)]
ZERO = (0, 0)
NONZERO = [v for v in V if v != ZERO]


def neg(v):
    return ((p - v[0]) % p, (p - v[1]) % p)


def add(u, v):
    return ((u[0] + v[0]) % p, (u[1] + v[1]) % p)


CLASSES = sorted(v for v in NONZERO if v <= neg(v))  # 12 classes


def reach(S):
    """All nonzero-coefficient signed sums of the set S (tuples in V)."""
    R = set()
    for coeffs in product((-1, 0, 1), repeat=len(S)):
        if not any(coeffs):
            continue
        w = (sum(c * v[0] for c, v in zip(coeffs, S)) % p,
             sum(c * v[1] for c, v in zip(coeffs, S)) % p)
        R.add(w)
    return R


def free(S):
    return ZERO not in reach(S)


def balanced_patterns(k):
    """Nonzero coefficient vectors in {−1,0,1}^k with #+ ≡ #− (mod 3)."""
    out = []
    for coeffs in product((-1, 0, 1), repeat=k):
        if not any(coeffs):
            continue
        plus = sum(1 for c in coeffs if c == 1)
        minus = sum(1 for c in coeffs if c == -1)
        if (plus - minus) % 3 == 0:
            out.append(coeffs)
    return out


def main():
    # A. L(F_5^2) = 4
    free4 = [S for S in combinations(CLASSES, 4) if free(S)]
    free5 = [S for S in combinations(CLASSES, 5) if free(S)]
    print(f"A: free 4-class-subsets of F_5^2: {len(free4)}; "
          f"free 5-subsets: {len(free5)} (must be 0)")
    assert len(free5) == 0

    # B. saturation of maximal free sets
    unsat = [S for S in free4 if len(reach(S)) != p * p - 1]
    print(f"B: free 4-sets with Reach != V\\0: {len(unsat)} (must be 0)")
    assert not unsat

    freesets = {0: [()],
                1: [S for S in combinations(CLASSES, 1)],
                2: [S for S in combinations(CLASSES, 2) if free(S)],
                3: [S for S in combinations(CLASSES, 3) if free(S)],
                4: free4}

    # C. the five cases
    grand_ok = True
    for s0 in (4, 3, 2, 1, 0):
        s1 = 6 - s0
        pats = balanced_patterns(s1)
        found = 0
        best_viol = None
        for S0 in freesets[s0]:
            B = set(NONZERO) - reach(S0) if s0 else set(NONZERO)
            # quick necessary condition: pairwise differences must be in B,
            # so if |B| is tiny the double loop below short-circuits fast.
            for S1 in combinations(V, s1):
                viol = 0
                ok = True
                for c in pats:
                    w = (sum(ci * v[0] for ci, v in zip(c, S1)) % p,
                         sum(ci * v[1] for ci, v in zip(c, S1)) % p)
                    if w not in B:
                        viol += 1
                        ok = False
                        if best_viol is not None and viol >= best_viol:
                            break
                if ok:
                    found += 1
                    print(f"   COUNTEREXAMPLE case ({s0},{s1}):", S0, S1)
                if best_viol is None or viol < best_viol:
                    best_viol = viol
        status = "EMPTY" if found == 0 else f"FOUND {found}"
        print(f"C: case (|S0|,|S1|)=({s0},{s1}): {status}; "
              f"min violated constraints over all configs: {best_viol}")
        grand_ok &= (found == 0)

    print("CASE AUDIT", "PASS — no ±free 6-set in F_5^2 ⊕ Z_3"
          if grand_ok else "FAIL")
    sys.exit(0 if grand_ok else 1)


if __name__ == "__main__":
    main()
