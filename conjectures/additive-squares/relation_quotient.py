#!/usr/bin/env python3
"""The relation-quotient engine: turn one integer relation into a theorem.

BACKGROUND.  For an alphabet A = {0, a, b, c} of distinct integers, write a word
over A and pick a factor u v with |u| = |v|.  Let (p, q, r) be the vector of
count-differences of the letters a, b, c between u and v (the letter 0
contributes nothing to sums, and equal lengths make its count-difference
determined).  Then

        u v is an additive square   <=>   p*a + q*b + r*c = 0,

so additive-square-freeness of a word over A depends on A only through the
RELATION LATTICE

        Lambda(A) = { (p,q,r) in Z^3 : p*a + q*b + r*c = 0 },

a rank-2 sublattice of Z^3.

QUOTIENT LEMMA.  Let M be any sublattice of Lambda(A), let pi : Z^3 -> Z^3/M be
the quotient, and let A_M = {0, pi(e1), pi(e2), pi(e3)} regarded as a vector
alphabet.  Then

        L(A)  <=  L(A_M).

Proof.  Lift a word w over A to the word ŵ over {0,e1,e2,e3} letter by letter,
and push it to A_M.  If the pushed word had an additive square, its
count-difference vector d would satisfy pi(d) = 0, i.e. d in M, hence
d in Lambda(A), hence p*a+q*b+r*c = 0 and w itself would have an additive
square.  So w additive-square-free over A implies its image is
additive-square-free over A_M, and lengths are equal.  QED

Taking M = <v> for a single primitive relation vector v gives Z^3/<v> = Z^2, and
A_v is a four-letter alphabet of integer VECTORS -- the "universal alphabet for
the relation v".  Computing L(A_v) once therefore bounds L(A) simultaneously for
EVERY integer alphabet A satisfying that relation.  This is a theorem about an
infinite family obtained from a single finite computation.

Freedman's published bound is the special case v = (1,1,-1), i.e. c = a + b:
A_v = {(0,0),(1,0),(0,1),(1,1)} and L(A_v) = 60.

This script builds A_v for each primitive v, calls ./afsfv, and tabulates.

Usage:  python3 relation_quotient.py MAXNORM [NODEBUDGET] [MAXDEPTH] [WORKERS] [OUT.csv]
"""
import os
import subprocess
import sys
from itertools import product
from math import gcd
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
AFSFV = os.path.join(HERE, "afsfv")


# ---------------------------------------------------------------- lattice ---
def ext_gcd(a, b):
    if b == 0:
        return (abs(a), 1 if a >= 0 else -1, 0)
    g, x, y = ext_gcd(b, a % b)
    return (g, y, x - (a // b) * y)


def unimodular_sending_to_e1(v):
    """Return a 3x3 integer matrix U with det +-1 and U @ v == (g,0,0),
    where g = gcd(v).  For primitive v this is e1."""
    v = list(v)
    U = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

    def rowop(i, j, k):           # row_i += k * row_j   (unimodular)
        for t in range(3):
            U[i][t] += k * U[j][t]
        v[i] += k * v[j]

    def swap(i, j):
        U[i], U[j] = U[j], U[i]
        v[i], v[j] = v[j], v[i]

    def negate(i):
        U[i] = [-x for x in U[i]]
        v[i] = -v[i]

    # clear v[2] against v[1], then v[1] against v[0], by integer row ops
    for (hi, lo) in ((2, 1), (1, 0)):
        while v[hi] != 0:
            if v[lo] == 0:
                swap(hi, lo)
                continue
            rowop(hi, lo, -(v[hi] // v[lo]))
            if v[hi] != 0:
                swap(hi, lo)
    if v[0] < 0:
        negate(0)
    return U, v[0]


def det2(m, i, j):
    return m[0][i] * m[1][j] - m[0][j] * m[1][i]


def quotient_alphabet(v):
    """A_v: the images of e1,e2,e3 in Z^3/<v>, as three 2-vectors.

    Returns (letters, psi) where psi is the 2x3 matrix of the quotient map.
    Raises ValueError if v is not primitive or the four letters are not
    distinct (which happens exactly when v is proportional to some e_i or
    e_i - e_j, i.e. the alphabet degenerates to fewer than four letters)."""
    if gcd(gcd(abs(v[0]), abs(v[1])), abs(v[2])) != 1:
        raise ValueError("not primitive")
    U, g = unimodular_sending_to_e1(v)
    assert g == 1, g
    psi = [U[1], U[2]]                      # rows 2 and 3 of U
    # checks: psi kills v, and psi is onto Z^2 (2x2 minors coprime)
    for row in psi:
        assert sum(row[t] * v[t] for t in range(3)) == 0, (v, psi)
    minors = [det2(psi, 0, 1), det2(psi, 0, 2), det2(psi, 1, 2)]
    assert gcd(gcd(abs(minors[0]), abs(minors[1])), abs(minors[2])) == 1, (v, psi)
    letters = [(0, 0)] + [(psi[0][t], psi[1][t]) for t in range(3)]
    if len(set(letters)) != 4:
        raise ValueError("degenerate: fewer than four distinct letters")
    return letters, psi


def canon_v(v):
    """Canonical form of a relation up to sign and permutation of a,b,c."""
    best = None
    for s in (1, -1):
        w = tuple(s * x for x in v)
        for perm in [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]:
            cand = (w[perm[0]], w[perm[1]], w[perm[2]])
            if best is None or cand < best:
                best = cand
    return best


# ------------------------------------------------------------------ driver --
def run_one(job):
    v, budget, depth = job
    letters, psi = quotient_alphabet(v)
    spec = "|".join(f"{x},{y}" for (x, y) in letters)
    out = subprocess.run([AFSFV, "exhaust", "2", spec, str(depth), str(budget)],
                         capture_output=True, text=True, timeout=100000).stdout
    L = exact = nodes = secs = None
    word = ""
    for line in out.splitlines():
        if line.startswith("nodes="):
            d = dict(p.split("=") for p in line.split())
            nodes, secs = int(d["nodes"]), float(d["secs"])
        elif line.startswith("RESULT"):
            exact = "exact" in line
            L = int(line.rsplit("=", 1)[1].lstrip(">="))
        elif line.startswith("word="):
            word = line[5:]
    return (v, spec, L, exact, nodes, secs, word)


def main():
    maxnorm = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    budget = int(sys.argv[2]) if len(sys.argv) > 2 else 400_000_000
    depth = int(sys.argv[3]) if len(sys.argv) > 3 else 4000
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    outfn = sys.argv[5] if len(sys.argv) > 5 else "data/relations.csv"

    seen, vs = set(), []
    rng = range(-maxnorm, maxnorm + 1)
    for v in product(rng, rng, rng):
        if v == (0, 0, 0):
            continue
        if gcd(gcd(abs(v[0]), abs(v[1])), abs(v[2])) != 1:
            continue
        cv = canon_v(v)
        if cv in seen:
            continue
        try:
            quotient_alphabet(v)
        except ValueError:
            seen.add(cv)
            continue
        seen.add(cv)
        vs.append(cv)
    vs.sort(key=lambda v: (max(abs(x) for x in v), sum(abs(x) for x in v), v))

    print(f"# {len(vs)} primitive relation classes with sup-norm <= {maxnorm}",
          flush=True)
    os.makedirs(os.path.dirname(outfn) or ".", exist_ok=True)
    jobs = [(v, budget, depth) for v in vs]
    with open(outfn, "w") as f, ProcessPoolExecutor(max_workers=workers) as ex:
        f.write("p,q,r,alphabet,L,exact,nodes,secs,word\n")
        for (v, spec, L, exact, nodes, secs, word) in ex.map(run_one, jobs):
            f.write(f"{v[0]},{v[1]},{v[2]},\"{spec}\",{L},{int(bool(exact))},"
                    f"{nodes},{secs:.3f},\"{word}\"\n")
            f.flush()
            tag = "EXACT" if exact else "lower"
            print(f"v={str(v):16s} A_v={spec:28s} {tag} L{'=' if exact else '>='}{L}"
                  f"  nodes={nodes} {secs:.1f}s", flush=True)
    print("# done", flush=True)


if __name__ == "__main__":
    main()
