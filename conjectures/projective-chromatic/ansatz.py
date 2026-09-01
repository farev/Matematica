"""Invariant-coloring ansatz for chi_2(8) under subgroups of GammaL(1,256).

Identify F_2^8 with F_256 via the primitive polynomial x^8+x^4+x^3+x^2+1
(0x11D); g = x (i.e. the integer 2) is verified primitive below. The maps
  mult_h : x -> h*x        (h in F_256^*)         and
  frob   : x -> x^2
send lines {x,y,x+y} to lines, so any subgroup G <= GammaL(1,256) acts on the
line set. A G-invariant proper 5-coloring = 5-coloring of the G-orbits such
that no line is monochromatic. Contraction rules per line {x,y,z} with orbit
cells (A,B,C):
  - all three in one cell A     -> ansatz DEAD unless cell A never gets used?
                                   (No: A must get *some* color -> mono line.
                                    So the whole G-ansatz is infeasible.)
  - exactly two cells (A,A,B)   -> edge constraint color(A) != color(B)
  - three distinct cells        -> not-all-equal triple
Solve the contracted instance with CDCL for k colors; if SAT, lift and verify
the full 255-point coloring from the definition (independent check).

Groups swept: G(d,e) = <mult by g^(255/d), frob^e-...>: for each d | 255
(subgroup H_d of order d) and each f | 8 (Frobenius power sigma^f generating
a subgroup of order 8/f), the group generated. d=1,f=8 is trivial (excluded:
that's the unrestricted problem). Orbits computed by closure; exact integers.
"""
import sys
from itertools import product
from lines import lines, check_coloring

POLY = 0x11D
N = 8
M = 255


def gf_mul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & 0x100:
            a ^= POLY
    return r


def build_tables():
    # verify g=2 is primitive: order 255
    exp = [0] * 256
    x = 1
    for i in range(255):
        exp[i] = x
        x = gf_mul(x, 2)
    assert x == 1, "g=2 not of order 255 for POLY 0x11D"
    assert len(set(exp[:255])) == 255
    log = [0] * 256
    for i in range(255):
        log[exp[i]] = i
    return exp, log


EXP, LOG = build_tables()
LINES = lines(N)


def orbits_of(gens):
    """gens: list of point->point maps on 1..255. Returns cell id per point."""
    cell = [-1] * (M + 1)
    nc = 0
    for p in range(1, M + 1):
        if cell[p] != -1:
            continue
        stack = [p]
        cell[p] = nc
        while stack:
            q = stack.pop()
            for gmap in gens:
                r = gmap[q]
                if cell[r] == -1:
                    cell[r] = nc
                    stack.append(r)
        nc += 1
    return cell, nc


def contract(cell, nc, k):
    """Build contracted CNF. Returns (cnf, nvars) or None if dead (a line
    lies inside one cell)."""
    var = lambda cellid, c: cellid * k + c + 1
    edges = set()
    naes = set()
    for (x, y, z) in LINES:
        a, b, c3 = cell[x], cell[y], cell[z]
        s = {a, b, c3}
        if len(s) == 1:
            return None, 0
        elif len(s) == 2:
            (u, v) = sorted(s)
            edges.add((u, v))
        else:
            naes.add(tuple(sorted(s)))
    cnf = []
    for cid in range(nc):
        cnf.append([var(cid, c) for c in range(k)])
        for c1 in range(k):
            for c2 in range(c1 + 1, k):
                cnf.append([-var(cid, c1), -var(cid, c2)])  # AMO: unions stay well-defined
    for (u, v) in edges:
        for c in range(k):
            cnf.append([-var(u, c), -var(v, c)])
    for (u, v, w) in naes:
        for c in range(k):
            cnf.append([-var(u, c), -var(v, c), -var(w, c)])
    return cnf, nc * k


def solve_group(d, f, k=5, verbose=True):
    """Subgroup: mult by g^(255//d) (order d) and frob^f (order 8/f if f|8; f=8 -> identity)."""
    gens = []
    if d > 1:
        h = EXP[255 // d]
        gens.append([0] + [gf_mul(h, p) for p in range(1, M + 1)])
    if f < 8:
        fmap = list(range(M + 1))
        for p in range(1, M + 1):
            q = p
            for _ in range(f):
                q = gf_mul(q, q)
            fmap[p] = q
        gens.append(fmap)
    if not gens:
        return "trivial", None
    cell, nc = orbits_of(gens)
    cnf, nv = contract(cell, nc, k)
    if cnf is None:
        if verbose:
            print(f"d={d} f={f}: DEAD (some orbit contains a full line), orbits={nc}")
        return "dead", None
    from pysat.solvers import Cadical195
    with Cadical195(bootstrap_with=cnf) as s:
        if s.solve():
            model = set(l for l in s.get_model() if l > 0)
            cellcolor = {}
            for cid in range(nc):
                for c in range(k):
                    if cid * k + c + 1 in model:
                        cellcolor[cid] = c
                        break
            color = [None] * (M + 1)
            for p in range(1, M + 1):
                color[p] = cellcolor[cell[p]]
            bad = check_coloring(N, color, k)
            assert not bad, f"lifted witness fails: {bad[:3]}"
            print(f"d={d} f={f}: *** SAT *** orbits={nc} — WITNESS FOUND AND VERIFIED")
            print("witness:", ",".join(str(color[p]) for p in range(1, M + 1)))
            return "sat", color
        else:
            if verbose:
                print(f"d={d} f={f}: UNSAT (orbits={nc}) — no G-invariant witness")
            return "unsat", None


if __name__ == "__main__":
    import signal

    k = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    tmo = int(sys.argv[2]) if len(sys.argv) > 2 else 120
    pairs = []
    for d in [255, 85, 51, 17, 15, 5, 3, 1]:
        for f in [1, 2, 4, 8]:
            if d == 1 and f == 8:
                continue
            pairs.append((d, f))

    class TO(Exception):
        pass

    def hdl(sig, frm):
        raise TO()

    signal.signal(signal.SIGALRM, hdl)
    results = {}
    for (d, f) in pairs:
        signal.alarm(tmo)
        try:
            res, _ = solve_group(d, f, k)
            results[(d, f)] = res
        except TO:
            print(f"d={d} f={f}: TIMEOUT after {tmo}s (inconclusive)")
            results[(d, f)] = "timeout"
        finally:
            signal.alarm(0)
    print("\nSummary:", results)
