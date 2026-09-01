"""Invariant-coloring sweep for chi_2(8) under GL(8,2)-subgroups beyond
GammaL(1,256): block-diagonal Singer actions, twisted powers, swaps, and
small-order semisimple elements. Solver calls use conflict budgets so no
cell can hang.

Verdicts per group G:
  DEAD    — some G-orbit contains a full line (any G-invariant coloring has
            a monochromatic line; exact, certificate = the line + orbit).
  UNSAT   — contracted instance unsatisfiable (no G-invariant witness;
            certified by solver on an exact contraction).
  SAT     — witness found (lifted + verified from definition -> chi_2(8)=5).
  BUDGET  — inconclusive within conflict budget.
"""
import sys
from lines import lines, check_coloring
from ansatz import contract, orbits_of  # generic exact machinery
from pysat.solvers import Cadical195

M = 255
N = 8
K = 5


def gf_tables(poly, bits):
    """exp/log tables for GF(2^bits) with primitive poly (int form)."""
    size = 1 << bits
    exp = [0] * size
    x = 1
    for i in range(size - 1):
        exp[i] = x
        x <<= 1
        if x & size:
            x ^= poly
    assert x == 1, f"poly {poly:#x} not primitive for GF(2^{bits})"
    log = [0] * size
    for i in range(size - 1):
        log[exp[i]] = i
    return exp, log


GF16 = gf_tables(0b10011, 4)      # x^4+x+1
GF8 = gf_tables(0b1011, 3)        # x^3+x+1
GF32 = gf_tables(0b100101, 5)     # x^5+x^2+1
GF64 = gf_tables(0b1000011, 6)    # x^6+x+1


def mul(tabs, bits, a, b):
    exp, log = tabs
    if a == 0 or b == 0:
        return 0
    return exp[(log[a] + log[b]) % ((1 << bits) - 1)]


def pointmap(fn):
    """fn: F_2^8 -> F_2^8 bijection given as int->int; return map array."""
    arr = [0] * (M + 1)
    seen = set()
    for p in range(1, M + 1):
        q = fn(p)
        assert 1 <= q <= M, (p, q)
        arr[p] = q
        seen.add(q)
    assert len(seen) == M, "not a bijection"
    return arr


def split44(p):
    return p & 0xF, (p >> 4) & 0xF


def join44(a, b):
    return a | (b << 4)


def split53(p):
    return p & 0x1F, (p >> 5) & 0x7


def join53(a, b):
    return a | (b << 5)


def split62(p):
    return p & 0x3F, (p >> 6) & 0x3


def join62(a, b):
    return a | (b << 6)


def make_groups():
    g16 = 2  # generator of GF(16)*
    g8 = 2
    g32 = 2
    g64 = 2
    groups = {}

    def diag44(r1, r2):
        h1 = GF16[0][r1 % 15]
        h2 = GF16[0][r2 % 15]
        return pointmap(lambda p: join44(mul(GF16, 4, split44(p)[0], h1),
                                         mul(GF16, 4, split44(p)[1], h2)))

    swap44 = pointmap(lambda p: join44(split44(p)[1], split44(p)[0]))
    frob44 = pointmap(lambda p: join44(mul(GF16, 4, split44(p)[0], split44(p)[0]),
                                       mul(GF16, 4, split44(p)[1], split44(p)[1])))

    groups["4+4 diag Singer15"] = [diag44(1, 1)]
    groups["4+4 diag Singer15 + swap"] = [diag44(1, 1), swap44]
    groups["4+4 diag Singer15 + frob"] = [diag44(1, 1), frob44]
    groups["4+4 diag Singer15 + swap + frob"] = [diag44(1, 1), swap44, frob44]
    groups["4+4 twisted (g,g^2)"] = [diag44(1, 2)]
    groups["4+4 twisted (g,g^7)"] = [diag44(1, 7)]
    groups["4+4 twisted (g,g^14)"] = [diag44(1, 14)]
    groups["4+4 twisted (g,g^4)"] = [diag44(1, 4)]
    groups["4+4 indep Singers 15x15"] = [diag44(1, 0), diag44(0, 1)]
    groups["4+4 order5 diag (g^3,g^3)"] = [diag44(3, 3)]
    groups["4+4 order5 twisted (g^3,g^6)"] = [diag44(3, 6)]
    groups["4+4 order5 twisted (g^3,g^9)"] = [diag44(3, 9)]
    groups["4+4 order5 twisted (g^3,g^12)"] = [diag44(3, 12)]
    groups["4+4 order3 diag (g^5,g^5)"] = [diag44(5, 5)]
    groups["4+4 order3 twisted (g^5,g^10)"] = [diag44(5, 10)]

    def diag53(r1, r2):
        h1 = GF32[0][r1 % 31]
        h2 = GF8[0][r2 % 7]
        return pointmap(lambda p: join53(mul(GF32, 5, split53(p)[0], h1),
                                         mul(GF8, 3, split53(p)[1], h2)))

    groups["5+3 Singer31 x Singer7"] = [diag53(1, 1)]
    groups["5+3 Singer31 only"] = [diag53(1, 0)]
    groups["5+3 Singer7 only"] = [diag53(0, 1)]

    def diag62(r1):
        h1 = GF64[0][r1 % 63]
        return pointmap(lambda p: join62(mul(GF64, 6, split62(p)[0], h1), split62(p)[1]))

    groups["6+2 Singer63"] = [diag62(1)]
    groups["6+2 order21 (g^3)"] = [diag62(3)]
    groups["6+2 order9 (g^7)"] = [diag62(7)]
    groups["6+2 order7 (g^9)"] = [diag62(9)]
    frob62 = pointmap(lambda p: join62(mul(GF64, 6, split62(p)[0], split62(p)[0]),
                                       split62(p)[1]))
    groups["6+2 order9 + frob6"] = [diag62(7), frob62]
    groups["6+2 order7 + frob6"] = [diag62(9), frob62]
    return groups


def run(name, gens, budget=3 * 10**6):
    cell, nc = orbits_of(gens)
    cnf, nv = contract(cell, nc, K)
    if cnf is None:
        print(f"{name}: DEAD (orbit contains a line), cells={nc}", flush=True)
        return "dead"
    with Cadical195(bootstrap_with=cnf) as s:
        s.conf_budget(budget)
        r = s.solve_limited()
        if r is True:
            model = set(l for l in s.get_model() if l > 0)
            cellcolor = {}
            for cid in range(nc):
                for c in range(K):
                    if cid * K + c + 1 in model:
                        cellcolor[cid] = c
                        break
            color = [None] * (M + 1)
            for p in range(1, M + 1):
                color[p] = cellcolor[cell[p]]
            bad = check_coloring(N, color, K)
            assert not bad, f"lifted witness fails: {bad[:3]}"
            print(f"{name}: *** SAT *** cells={nc} — WITNESS FOUND AND VERIFIED", flush=True)
            print("witness:", ",".join(str(color[p]) for p in range(1, M + 1)))
            with open("witness_n8k5.txt", "w") as f:
                f.write(",".join(str(color[p]) for p in range(1, M + 1)) + "\n")
            return "sat"
        elif r is False:
            print(f"{name}: UNSAT, cells={nc} — no invariant witness", flush=True)
            return "unsat"
        else:
            print(f"{name}: BUDGET exhausted, cells={nc} — inconclusive", flush=True)
            return "budget"


if __name__ == "__main__":
    budget = int(sys.argv[1]) if len(sys.argv) > 1 else 3 * 10**6
    groups = make_groups()
    tally = {}
    for name, gens in groups.items():
        v = run(name, gens, budget)
        tally[v] = tally.get(v, 0) + 1
        if v == "sat":
            break
    print("\ntally:", tally)
