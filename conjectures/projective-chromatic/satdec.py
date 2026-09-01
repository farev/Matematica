"""SAT decisions for chi_2(n): can F_2^n \ {0} be partitioned into k sum-free sets?

Encoding: var v(p,c) = point p gets color c (p in 1..2^n-1, c in 0..k-1).
 - ALO per point; (optional AMO not needed: any multi-colored solution
   restricts to a proper coloring by picking one color per point —
   monochromatic-line clauses only get easier; for witness extraction we
   just take the lowest set color and re-verify from the definition.)
 - For each line {x,y,z} and color c: (~v(x,c) | ~v(y,c) | ~v(z,c)).

Usage: satdec.py n k [--dimacs FILE]  -> prints SAT/UNSAT (+witness check)
"""
import sys
from lines import lines, check_coloring


def build_cnf(n, k):
    m = (1 << n) - 1
    var = lambda p, c: (p - 1) * k + c + 1
    cnf = []
    for p in range(1, m + 1):
        cnf.append([var(p, c) for c in range(k)])
    for (x, y, z) in lines(n):
        for c in range(k):
            cnf.append([-var(x, c), -var(y, c), -var(z, c)])
    return cnf, m * k


def main():
    n, k = int(sys.argv[1]), int(sys.argv[2])
    cnf, nv = build_cnf(n, k)
    if "--dimacs" in sys.argv:
        path = sys.argv[sys.argv.index("--dimacs") + 1]
        with open(path, "w") as f:
            f.write(f"p cnf {nv} {len(cnf)}\n")
            for cl in cnf:
                f.write(" ".join(map(str, cl)) + " 0\n")
        print(f"wrote {path}: {nv} vars {len(cnf)} clauses")
        return
    from pysat.solvers import Cadical195
    with Cadical195(bootstrap_with=cnf) as s:
        sat = s.solve()
        if sat:
            model = set(l for l in s.get_model() if l > 0)
            m = (1 << n) - 1
            color = [None] * (m + 1)
            for p in range(1, m + 1):
                for c in range(k):
                    if (p - 1) * k + c + 1 in model:
                        color[p] = c
                        break
            bad = check_coloring(n, color, k)
            assert not bad, f"WITNESS FAILS CHECK: {bad[:3]}"
            sizes = [sum(1 for p in range(1, m + 1) if color[p] == c) for c in range(k)]
            print(f"n={n} k={k}: SAT (witness verified from definition; class sizes {sizes})")
            print("witness:", ",".join(str(color[p]) for p in range(1, m + 1)))
        else:
            print(f"n={n} k={k}: UNSAT")


if __name__ == "__main__":
    main()
