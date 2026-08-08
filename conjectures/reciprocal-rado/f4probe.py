#!/usr/bin/env python3
"""Bracket probes for f_4(2): stream CNF from enum2 output, solve with the
CaDiCaL binary (no proof; bracketing only). Usage: f4probe.py n1 n2 ...
Writes work/f42_n{n}.{cnf,out}; prints one line per n. Model kept on SAT.
"""
import sys, os, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))
CADICAL = os.environ.get(
    "CADICAL_BIN",
    "/tmp/claude-0/-home-user-Matematica/eac8cfb3-85ae-5073-afc3-3fe178e7e078/"
    "scratchpad/build/cadical-rel-3.0.0/build/cadical")
R = 4

def probe(n):
    t0 = time.time()
    out = subprocess.run([os.path.join(HERE, "enum2"), str(n)],
                         capture_output=True, text=True, check=True).stdout
    cnff = os.path.join(HERE, "work", f"f42_n{n}.cnf")
    v = lambda x, c: (x - 1) * R + c + 1
    ncl = 0
    with open(cnff, "w") as f:
        f.write(f"p cnf {n * R} 0\n")            # patched below
        for x in range(1, n + 1):
            f.write(" ".join(str(v(x, c)) for c in range(R)) + " 0\n"); ncl += 1
        seen = set()
        for ln in out.splitlines():
            z, x, y = map(int, ln.split())
            S = frozenset((z, x, y))
            if S in seen: continue
            seen.add(S)
            for c in range(R):
                f.write(" ".join(str(-v(u, c)) for u in sorted(S)) + " 0\n"); ncl += 1
    # patch header with true clause count
    data = open(cnff).read().split("\n", 1)
    with open(cnff, "w") as f:
        f.write(f"p cnf {n * R} {ncl}\n" + data[1])
    enum_secs = time.time() - t0
    t0 = time.time()
    outf = os.path.join(HERE, "work", f"f42_n{n}.out")
    with open(outf, "w") as f:
        p = subprocess.run([CADICAL, "-q", cnff], stdout=f, text=True)
    res = open(outf).read()
    sat = "s SATISFIABLE" in res
    print(f"n={n}: {'SAT' if sat else 'UNSAT' if 's UNSATISFIABLE' in res else '??'}"
          f"  ({ncl} clauses, enum {enum_secs:.0f}s, solve {time.time()-t0:.0f}s)",
          flush=True)
    if not sat:
        os.remove(cnff)
    return sat

if __name__ == "__main__":
    for n in map(int, sys.argv[1:]):
        if not probe(n):
            break
