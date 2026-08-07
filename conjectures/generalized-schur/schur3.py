#!/usr/bin/env python3
"""Exact k-color generalized (off-diagonal) Schur numbers, with certificates.

S(k; t_1,...,t_k) is the least m such that every k-coloring of {1..m} has,
for some color i, a monochromatic solution of

    x_1 + x_2 + ... + x_{t_i - 1} = x_{t_i}          (repeats allowed)

i.e. color class i must avoid solutions of the (t_i-1)-summand equation.
Diagonal case t_i = t for all i is the classical generalized Schur number;
t = 3 is Schur's x + y = z.

Encoding: v(x, j) = (x-1)*k + j + 1 true iff x has color j.
  - one at-least-one-color clause per x (no at-most-one needed: forbidding
    mono solutions per color separately is monotone in the true-set, so any
    satisfying assignment projects to a valid coloring)
  - per color j with parameter t: for every multiset {a_1 <= ... <= a_{t-1}}
    with s = sum a_i <= n, the clause OR_{y in set(a_1..a_{t-1}, s)} -v(y, j).
    Enumerating nondecreasing tuples (partitions with parts >= 1) visits each
    distinct clause once; a set() dedupes the (rare) collisions from
    different multisets with the same support set.

Solver: Glucose42 with DRUP proof for boundary runs (proof checked by the
independent C checker rup_check), Cadical153 allowed for exploration only.
Witnesses are verified by verify_witness.py (independent bitset algorithm).
"""
import sys, os, subprocess
from pysat.formula import CNF
from pysat.solvers import Glucose42, Cadical153


def clauses_for_color(t, n):
    """Distinct support-set clauses for x_1+...+x_{t-1}=x_t within {1..n}.

    Yields sorted tuples of the distinct integers involved. Enumerates
    nondecreasing (a_1,...,a_{t-1}) with sum <= n by recursion.
    """
    out = set()
    m = t - 1  # number of summands

    def rec(prefix, lo, remaining_slots, ssum):
        if remaining_slots == 0:
            support = tuple(sorted(set(prefix + (ssum,))))
            out.add(support)
            return
        a = lo
        while ssum + a * remaining_slots <= n:
            rec(prefix + (a,), a, remaining_slots - 1, ssum + a)
            a += 1

    rec(tuple(), 1, m, 0)
    return out


def encode(ts, n):
    """CNF for: exists coloring of {1..n} with no mono solution in any color."""
    k = len(ts)
    v = lambda x, j: (x - 1) * k + j + 1
    cnf = CNF()
    for x in range(1, n + 1):
        cnf.append([v(x, j) for j in range(k)])
    ncl = 0
    for j, t in enumerate(ts):
        for support in sorted(clauses_for_color(t, n)):
            cnf.append([-v(x, j) for x in support])
            ncl += 1
    return cnf, ncl


def decide(ts, n, workdir, tag, proof=True, solver="glucose"):
    """('SAT', coloring) or ('UNSAT', prooffile or None)."""
    k = len(ts)
    cnf, ncl = encode(ts, n)
    os.makedirs(workdir, exist_ok=True)
    if solver == "glucose":
        S = Glucose42(bootstrap_with=cnf, with_proof=proof)
    else:
        S = Cadical153(bootstrap_with=cnf)
        proof = False
    sat = S.solve()
    if sat:
        model = set(l for l in S.get_model() if l > 0)
        coloring = []
        for x in range(1, n + 1):
            for j in range(k):
                if (x - 1) * k + j + 1 in model:
                    coloring.append(j)
                    break
            else:
                raise RuntimeError(f"no color for {x}")
        S.delete()
        return "SAT", coloring
    if proof:
        prooffile = os.path.join(workdir, f"{tag}_n{n}.drup")
        with open(prooffile, "w") as f:
            for line in S.get_proof():
                f.write(line + "\n")
            f.write("0\n")  # empty clause terminator
        cnffile = os.path.join(workdir, f"{tag}_n{n}.cnf")
        cnf.to_file(cnffile)
        S.delete()
        return "UNSAT", (cnffile, prooffile)
    S.delete()
    return "UNSAT", None


def write_witness(path, ts, n, coloring):
    with open(path, "w") as f:
        f.write(f"{n} {len(ts)} {' '.join(map(str, ts))}\n")
        f.write(" ".join(str(c) for c in coloring) + "\n")


def rup_check(cnffile, prooffile):
    here = os.path.dirname(os.path.abspath(__file__))
    for cand in (os.path.join(here, "rup_check"),
                 os.path.join(here, "..", "..", "tools", "satcert", "rup_check"),
                 "/home/user/Matematica/tools/satcert/rup_check"):
        if os.path.exists(cand):
            r = subprocess.run([cand, cnffile, prooffile],
                               capture_output=True, text=True, timeout=36000)
            return r.returncode == 0 and "VERIFIED" in r.stdout, r.stdout.strip()
    return False, "rup_check binary not found"


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("ts", help="comma-separated t_1,..,t_k, e.g. 4,4,5")
    ap.add_argument("n", type=int)
    ap.add_argument("--workdir", default="work")
    ap.add_argument("--no-proof", action="store_true")
    ap.add_argument("--solver", default="glucose", choices=["glucose", "cadical"])
    a = ap.parse_args()
    ts = tuple(int(x) for x in a.ts.split(","))
    tag = "s" + "_".join(map(str, ts))
    res, aux = decide(ts, a.n, a.workdir, tag,
                      proof=not a.no_proof, solver=a.solver)
    if res == "SAT":
        wf = os.path.join(a.workdir, f"{tag}_n{a.n}.witness")
        write_witness(wf, ts, a.n, aux)
        print(f"SAT n={a.n} witness={wf}")
    else:
        if aux:
            ok, msg = rup_check(*aux)
            print(f"UNSAT n={a.n} proof={aux[1]} rup_check={'VERIFIED' if ok else 'FAILED: '+msg}")
            if not ok:
                sys.exit(2)
        else:
            print(f"UNSAT n={a.n} (no proof logged)")


if __name__ == "__main__":
    main()
