#!/usr/bin/env python3
"""Certify the counterexample G18 (and any graph6 input) both ways:

  * UNSAT at 6 colors: plain definition-level CNF (no symmetry breaking),
    Glucose42 with DRUP proof logging; proof checked by the independent
    tools/satcert/rup_check; CNF + DRUP written to certs/.
  * chi'_s <= 7: a 7-coloring witness extracted and re-verified from the
    definition; written to certs/.

Usage: certify_ce.py <name> <graph6> [<rup_check-binary>]
Writes certs/<name>.cnf, certs/<name>.drup, certs/<name>_7col.txt
"""
import subprocess
import sys

from pysat.solvers import Glucose42


def parse_g6(s):
    n = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        v = ord(ch) - 63
        bits += [(v >> b) & 1 for b in range(5, -1, -1)]
    edges = []
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                edges.append((i, j))
            k += 1
    return n, edges


def conflicts(n, edges):
    nb = [set() for _ in range(n)]
    for a, b in edges:
        nb[a].add(b)
        nb[b].add(a)
    out = []
    m = len(edges)
    for i in range(m):
        a, b = edges[i]
        close = {a, b} | nb[a] | nb[b]
        for j in range(i + 1, m):
            c, d = edges[j]
            if c in close or d in close:
                out.append((i, j))
    return out, nb


def cnf_for(m, confl, K):
    def var(e, c):
        return e * K + c + 1
    cls = [[var(e, c) for c in range(K)] for e in range(m)]
    for (i, j) in confl:
        for c in range(K):
            cls.append([-var(i, c), -var(j, c)])
    return cls, m * K


def main():
    name, g6 = sys.argv[1], sys.argv[2]
    rup_bin = sys.argv[3] if len(sys.argv) > 3 else "../../tools/satcert/rup_check"
    n, edges = parse_g6(g6)
    m = len(edges)
    confl, nb = conflicts(n, edges)
    print("%s: n=%d m=%d conflict-pairs=%d" % (name, n, m, len(confl)))

    # --- 6 colors: expect UNSAT, log DRUP ---
    cls, nv = cnf_for(m, confl, 6)
    with open("certs/%s.cnf" % name, "w") as fh:
        fh.write("p cnf %d %d\n" % (nv, len(cls)))
        for c in cls:
            fh.write(" ".join(map(str, c)) + " 0\n")
    s = Glucose42(bootstrap_with=cls, with_proof=True)
    sat = s.solve()
    assert not sat, "expected UNSAT at 6 colors!"
    proof = s.get_proof()
    s.delete()
    with open("certs/%s.drup" % name, "w") as fh:
        for line in proof:
            fh.write(line + "\n")
    r = subprocess.run([rup_bin, "certs/%s.cnf" % name, "certs/%s.drup" % name],
                       capture_output=True, text=True)
    print("rup_check:", (r.stdout + r.stderr).strip(), "(exit %d)" % r.returncode)
    assert r.returncode == 0, "DRUP proof did not verify"

    # --- 7 colors: expect SAT, verify witness from definition ---
    cls7, _ = cnf_for(m, confl, 7)
    s = Glucose42(bootstrap_with=cls7)
    assert s.solve(), "expected SAT at 7 colors"
    model = set(l for l in s.get_model() if l > 0)
    s.delete()
    col = []
    for e in range(m):
        cs = [c for c in range(7) if e * 7 + c + 1 in model]
        col.append(cs[0])
    for i in range(m):
        for j in range(i + 1, m):
            if col[i] != col[j]:
                continue
            a, b = edges[i]
            c, d = edges[j]
            assert not ({a, b} & {c, d}), "witness: shared vertex"
            assert not (c in nb[a] or d in nb[a] or c in nb[b] or d in nb[b]), \
                "witness: not induced"
    with open("certs/%s_7col.txt" % name, "w") as fh:
        fh.write("graph6 %s\n" % g6)
        fh.write("edges (i<j lex): %s\n" % " ".join("%d-%d" % e for e in edges))
        fh.write("7-coloring (edge order as above): %s\n"
                 % " ".join(map(str, col)))
    print("7-coloring witness verified from the definition; "
          "chi'_s = 7 certified (UNSAT@6 + witness@7).")


if __name__ == "__main__":
    main()
