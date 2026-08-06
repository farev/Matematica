"""Clean-room check of double saturation, straight from the definition.

No bitmasks, no shared code with census.c / semireg.c / ds.c: every claim is
re-derived by explicit subset enumeration.  Four positive controls whose status
is forced, one negative control, then the 19-vertex graph.

    python3 verify.py
"""
from itertools import combinations


def circulant(n, S):
    S = set(S) | {n - d for d in S}
    return [[(j - i) % n in S for j in range(n)] for i in range(n)]


def has_clique(A, k):
    n = len(A)
    for c in combinations(range(n), k):
        if all(A[u][v] for u, v in combinations(c, 2)):
            return c
    return None


def has_indep(A, k):
    n = len(A)
    for c in combinations(range(n), k):
        if all(not A[u][v] for u, v in combinations(c, 2)):
            return c
    return None


def flip(A, u, v):
    B = [row[:] for row in A]
    B[u][v] = not B[u][v]
    B[v][u] = B[u][v]
    return B


def report(A, s, t, name):
    n = len(A)
    kc, ki = has_clique(A, s), has_indep(A, t)
    print(f"[{name}] n={n} edges={sum(map(sum, A)) // 2}  K{s}: {kc}   indep-{t}: {ki}")
    ok = kc is None and ki is None
    bad_add = bad_del = 0
    for u, v in combinations(range(n), 2):
        B = flip(A, u, v)
        if A[u][v]:                              # deletion must create an independent t-set
            if has_indep(B, t) is None:
                bad_del += 1
                print(f"   no indep-{t} after deleting {u}-{v}")
        else:                                    # addition must create a K_s
            if has_clique(B, s) is None:
                bad_add += 1
                print(f"   no K{s} after adding {u}-{v}")
    print(f"   additions failing: {bad_add}   deletions failing: {bad_del}")
    ok = ok and bad_add == 0 and bad_del == 0
    print(f"   ==> DOUBLY SATURATED ({s},{t}): {ok}")
    return ok


if __name__ == "__main__":
    # positive controls: status forced by uniqueness or by self-complementarity
    report(circulant(5, [1]), 3, 3, "C5 (3,3) control")
    report(circulant(13, [1, 5]), 3, 5, "C13(1,5) (3,5) control")
    report(circulant(13, [1, 3, 4]), 4, 4, "Paley(13) (4,4) control")
    report(circulant(17, [1, 2, 4, 8]), 4, 4, "Paley(17) (4,4) control")
    # negative control: the (3,4,8) Wagner graph is NOT doubly saturated
    report(circulant(8, [1, 4]), 3, 4, "Wagner V8 (3,4) negative control")
    # the 19-vertex graph (published; see NOTE.md section 4)
    report(circulant(19, [1, 3, 5, 6]), 4, 5, "C19(1,3,5,6)")
