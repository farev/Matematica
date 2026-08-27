#!/usr/bin/env python3
"""D_13-invariant witness hunt for a balanced 5-colouring of K_26.

Vertices = elements of the dihedral group D_13 (order 26). The 325 edges of
K_26 split into 19 Cayley classes: 6 rotation classes R_k = {{g, g r^k}}
(k = 1..6, 26 edges each) and 13 reflection classes M_i = {{g, g s r^i}}
(perfect matchings, 13 edges each). A D_13-invariant 5-colouring assigns
whole classes to colours. Lemma 1 forces every colour >= 55 edges; writing
a rotation classes and b reflection classes per colour, 26a + 13b >= 55
means 2a + b >= 5, and summing 2a+b over the five colours gives exactly
2*6 + 13 = 25 = 5*5 — so EVERY colour class has 2a + b = 5 exactly
(profiles (a,b) in {(2,1), (1,3), (0,5)}; 65 edges each).

Balanced <=> every colour class, as a graph, has independence number <= 5
(then no monochromatic K_6 automatically, since the classes partition the
edges). We filter each candidate group for alpha <= 5, then look for exact
covers of the 19 classes by 5 surviving groups.

Outcome either way is decisive for this ansatz: a hit refutes Erdős #617;
exhaustion proves no D_13-invariant witness exists. (The Z_26 ansatz is
already dead by arithmetic: its 12 full difference classes + one half
class cannot form five 2a+b=5 groups — see WRITEUP.)

Usage: python3 dihedral.py
"""
import itertools, sys

N = 26
# vertex numbering: rotation j -> j (0..12), reflection s r^j -> 13 + j
def vid(eps, j):
    return eps * 13 + (j % 13)

def rotation_class(k):
    """R_k: g ~ g r^k. For g = r^j: r^{j+k}; for g = s r^j: s r^{j+k}."""
    edges = set()
    for j in range(13):
        edges.add(tuple(sorted((vid(0, j), vid(0, j + k)))))
        edges.add(tuple(sorted((vid(1, j), vid(1, j + k)))))
    return frozenset(edges)

def reflection_class(i):
    """M_i: g ~ g (s r^i). For g = r^j: g*(s r^i) = r^j s r^i = s r^{i-j}.
    So r^j <-> s r^{i-j}."""
    edges = set()
    for j in range(13):
        edges.add(tuple(sorted((vid(0, j), vid(1, i - j)))))
    return frozenset(edges)

def alpha_le(edges, bound):
    """True iff the graph (on 26 vertices) has no independent set of size
    bound+1. Bitset DFS over complement cliques."""
    adj = [0] * N
    for u, v in edges:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    nonadj = [(~adj[v]) & ((1 << N) - 1) & ~(1 << v) for v in range(N)]
    target = bound + 1
    def grow(cand, size):
        if size == target:
            return True
        if size + bin(cand).count("1") < target:
            return False
        c = cand
        while c:
            v = (c & -c).bit_length() - 1
            c &= c - 1
            if grow(cand & nonadj[v] & ~((1 << (v + 1)) - 1), size + 1):
                return True
            cand &= ~(1 << v)
            if size + bin(cand).count("1") < target:
                return False
        return False
    return not grow((1 << N) - 1, 0)

def main():
    R = {k: rotation_class(k) for k in range(1, 7)}
    M = {i: reflection_class(i) for i in range(13)}
    # sanity: classes partition the 325 edges
    allE = set()
    for c in list(R.values()) + list(M.values()):
        assert not (allE & c)
        allE |= c
    assert len(allE) == 325
    for k, c in R.items():
        assert len(c) == 26, (k, len(c))
    for i, c in M.items():
        assert len(c) == 13

    # positive control for alpha_le: the best circulant from circulant.py
    # (221 edges, alpha <= 5) and a negative control (a single matching has
    # alpha = 13 > 5).
    S221 = [1, 2, 3, 4, 6, 7, 8, 9, 13]
    e221 = set()
    for x in range(26):
        for d in S221:
            e221.add(tuple(sorted((x, (x + d) % 26))))
    assert alpha_le(e221, 5), "control: 221-edge circulant should pass"
    assert not alpha_le(M[0], 5), "control: single matching must fail"
    print("[controls] alpha_le passes 221-circulant, rejects single matching")

    # enumerate candidate groups by profile, filter alpha <= 5
    good = {"21": [], "13": [], "05": []}
    for ks in itertools.combinations(range(1, 7), 2):
        for i in range(13):
            E = R[ks[0]] | R[ks[1]] | M[i]
            if alpha_le(E, 5):
                good["21"].append((ks, (i,)))
    for k in range(1, 7):
        for iss in itertools.combinations(range(13), 3):
            E = R[k] | M[iss[0]] | M[iss[1]] | M[iss[2]]
            if alpha_le(E, 5):
                good["13"].append(((k,), iss))
    for iss in itertools.combinations(range(13), 5):
        E = frozenset().union(*[M[i] for i in iss])
        if alpha_le(E, 5):
            good["05"].append(((), iss))
    print(f"surviving groups: (2rot+1refl): {len(good['21'])}/195, "
          f"(1rot+3refl): {len(good['13'])}/1716, "
          f"(5refl): {len(good['05'])}/1287")

    # exact cover: 5 groups, disjoint classes, covering all 19
    groups = good["21"] + good["13"] + good["05"]
    sols = []
    def cover(chosen, used_r, used_m, start):
        if len(chosen) == 5:
            if used_r == 63 - 1 and used_m == (1 << 13) - 1:  # bits 1..6
                sols.append(list(chosen))
            return
        for idx in range(start, len(groups)):
            ks, iss = groups[idx]
            rm = sum(1 << k for k in ks)
            mm = sum(1 << i for i in iss)
            if (used_r & rm) or (used_m & mm):
                continue
            chosen.append(groups[idx])
            cover(chosen, used_r | rm, used_m | mm, idx + 1)
            chosen.pop()
    cover([], 1, 0, 0)  # bit0 of used_r unused; rotations are bits 1..6
    print(f"exact covers found: {len(sols)}")
    for sol in sols[:5]:
        print("  WITNESS CANDIDATE:", sol)
    if not sols:
        print("no D_13-invariant balanced 5-colouring of K_26 exists (exhaustive)")

if __name__ == "__main__":
    main()
