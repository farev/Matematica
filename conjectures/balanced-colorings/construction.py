#!/usr/bin/env python3
"""Balanced colourings from affine planes (Erdős #617).

A balanced r-colouring of K_N: an edge r-colouring such that every set of
r+1 vertices spans all r colours.

Lemma (pigeonhole). Let q be a prime power and AG(2,q) the affine plane of
order q: q^2 points, q+1 parallel classes of q lines each, every pair of
points on exactly one line. Colour edge {u,v} by the parallel class of the
line uv, then merge two parallel classes into one colour, giving q colours.
Any q+1 points meet some parallel class' q lines with a repeat (pigeonhole),
so for EVERY class d two of the points share a d-line and the edge between
them has class d. All q+1 classes appear on every (q+1)-subset, hence all q
merged colours do: the colouring is balanced. So T(q) >= q^2.

This script builds the colouring for q = 3, 4, 5 and verifies balancedness
FROM THE DEFINITION (every (q+1)-subset enumerated). Exact integer
arithmetic only. Emits data/K{q^2}_balanced_{q}col.txt with one line per
edge "u v colour" (vertices 0..q^2-1).

Controls:
  - r=2: the C_5 colouring of K_5 is balanced (known T(2) = 5); exhaustive
    check that K_6 has NO balanced 2-colouring (2^15 enumeration, matching
    R(3,3) = 6) -- ground truth for the SAT encoder.
  - negative: the all-one-colour colouring of K_25 must be REJECTED.
  - plane axioms checked: every pair of points on exactly one line.
"""
import itertools, sys

def gf_mul(a, b, q):
    if q in (2, 3, 5):
        return (a * b) % q
    if q == 4:  # GF(4) = GF(2)[x]/(x^2+x+1), elements 0,1,2=x,3=x+1
        MUL = [[0,0,0,0],[0,1,2,3],[0,2,3,1],[0,3,1,2]]
        return MUL[a][b]
    raise ValueError(q)

def gf_add(a, b, q):
    if q in (2, 3, 5):
        return (a + b) % q
    if q == 4:
        return a ^ b
    raise ValueError(q)

def affine_plane(q):
    """Return (points, classes): points = list of (x,y); classes = list of
    q+1 parallel classes, each a list of q lines, each line a set of point
    indices."""
    pts = [(x, y) for x in range(q) for y in range(q)]
    idx = {p: i for i, p in enumerate(pts)}
    classes = []
    # slope m in F_q: lines y = m*x + b
    for m in range(q):
        cls = []
        for b in range(q):
            line = {idx[(x, gf_add(gf_mul(m, x, q), b, q))] for x in range(q)}
            cls.append(line)
        classes.append(cls)
    # vertical lines x = c
    classes.append([{idx[(c, y)] for y in range(q)} for c in range(q)])
    # axiom check: every pair of points on exactly one line
    n = q * q
    for u in range(n):
        for v in range(u + 1, n):
            onct = sum(1 for cls in classes for L in cls if u in L and v in L)
            assert onct == 1, (u, v, onct)
    return pts, classes

def build_colouring(q, merge=(0, 1)):
    """Edge colouring of K_{q^2}: colour = parallel-class index, with class
    merge[1] relabelled to merge[0]; colours renumbered to 0..q-1."""
    n = q * q
    _, classes = affine_plane(q)
    # class of each edge
    edge_class = {}
    for ci, cls in enumerate(classes):
        for L in cls:
            for u, v in itertools.combinations(sorted(L), 2):
                edge_class[(u, v)] = ci
    assert len(edge_class) == n * (n - 1) // 2
    # merge classes merge[1] -> merge[0], renumber
    remap = {}
    nxt = 0
    for ci in range(q + 1):
        if ci == merge[1]:
            continue
        remap[ci] = nxt; nxt += 1
    remap[merge[1]] = remap[merge[0]]
    assert nxt == q
    return n, {e: remap[c] for e, c in edge_class.items()}

def is_balanced(n, r, colouring):
    """Definition-level check: every (r+1)-subset spans all r colours.
    Returns (ok, witness_bad_subset_or_None)."""
    for S in itertools.combinations(range(n), r + 1):
        seen = set()
        for u, v in itertools.combinations(S, 2):
            seen.add(colouring[(u, v)])
        if len(seen) != r:
            return False, S
    return True, None

def main():
    # --- r=2 controls -------------------------------------------------
    # C_5 colouring of K_5: colour 0 = cycle edges {i,i+1 mod 5}, colour 1 rest
    c5 = {}
    for u, v in itertools.combinations(range(5), 2):
        c5[(u, v)] = 0 if (v - u) % 5 in (1, 4) else 1
    ok, bad = is_balanced(5, 2, c5)
    assert ok, bad
    print("[control] K_5 with C_5 colouring: balanced 2-colouring OK (T(2)>=5)")
    # exhaustive: K_6 has no balanced 2-colouring (R(3,3)=6)
    edges6 = list(itertools.combinations(range(6), 2))
    found = False
    for mask in range(1 << 15):
        col = {e: (mask >> i) & 1 for i, e in enumerate(edges6)}
        ok, _ = is_balanced(6, 2, col)
        if ok:
            found = True; break
    assert not found
    print("[control] K_6: no balanced 2-colouring in all 2^15 colourings (matches R(3,3)=6)")

    # --- affine constructions q = 3, 4, 5 -----------------------------
    for q in (3, 4, 5):
        n, col = build_colouring(q)
        ncols = len(set(col.values()))
        assert ncols == q, ncols
        ok, bad = is_balanced(n, q, col)
        assert ok, (q, bad)
        nsub = len(list(itertools.combinations(range(n), q + 1))) if n <= 16 else None
        import math
        total = math.comb(n, q + 1)
        print(f"[proved+certified] K_{n}: balanced {q}-colouring from AG(2,{q}) "
              f"verified over all {total} ({q+1})-subsets -> T({q}) >= {n}")
        with open(f"data/K{n}_balanced_{q}col.txt", "w") as f:
            f.write(f"# balanced {q}-colouring of K_{n} from AG(2,{q}), merge classes 0,1\n")
            f.write(f"# verified from the definition over all {total} {q+1}-subsets\n")
            for (u, v), c in sorted(col.items()):
                f.write(f"{u} {v} {c}\n")

    # --- negative control ---------------------------------------------
    n = 25
    allzero = {e: 0 for e in itertools.combinations(range(n), 2)}
    ok, bad = is_balanced(n, 5, allzero)
    assert not ok
    print(f"[control] all-one-colour K_25 rejected (first bad 6-set: {bad})")
    print("ALL CHECKS PASSED")

if __name__ == "__main__":
    main()
