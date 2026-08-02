#!/usr/bin/env python3
"""Sweep L(A) over 4-element integer alphabets A = {0,a,b,c}.

L(A) is the length of the longest additive-square-free word over A.  L is
invariant under the affine maps x -> alpha*x + beta (alpha != 0), because a
block of length k has sum alpha*S + k*beta, so equality of two equal-length
block sums is preserved.  We therefore normalise every alphabet to

    {0, a, b, c},  0 < a < b < c,  gcd(a, b, c) = 1,

and further quotient by the reflection A -> max(A) - A (the case alpha = -1),
which sends (a,b,c) -> (c-b, c-a, c).  We keep the lexicographically smaller
representative.

Each alphabet is handed to ./afsf, which does an exhaustive DFS with a node
budget.  If the tree closes inside the budget the value of L is EXACT; if the
budget or depth cap is hit we only get a lower bound.  Both are exact integer
computations -- there is no floating point anywhere in the pipeline.

Usage:  python3 sweep4.py MAXC [NODEBUDGET] [MAXDEPTH] [WORKERS] [OUT.csv]
"""
import subprocess
import sys
import os
from math import gcd
from concurrent.futures import ProcessPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
AFSF = os.path.join(HERE, "afsf")


def canonical(a, b, c):
    """Representative of {0,a,b,c} under reflection x -> c - x."""
    return min((a, b, c), (c - b, c - a, c))


def alphabets(maxc):
    seen = set()
    for c in range(1, maxc + 1):
        for b in range(1, c):
            for a in range(1, b):
                if gcd(gcd(a, b), c) != 1:
                    continue
                key = canonical(a, b, c)
                if key in seen:
                    continue
                seen.add(key)
                yield key


def degenerate(a, b, c):
    """True iff one letter is the sum of two others (Freedman's family):
    {0,x,y,x+y} up to relabelling, i.e. the relation vector (1,1,-1)."""
    return c == a + b


def run_one(job):
    a, b, c, budget, depth = job
    spec = f"0,{a},{b},{c}"
    out = subprocess.run([AFSF, "exhaust", spec, str(depth), str(budget)],
                         capture_output=True, text=True, timeout=100000).stdout
    L, exact, nodes, secs, word = None, None, None, None, ""
    for line in out.splitlines():
        if line.startswith("nodes="):
            parts = dict(p.split("=") for p in line.split())
            nodes, secs = int(parts["nodes"]), float(parts["secs"])
        elif line.startswith("RESULT"):
            exact = "exact" in line
            L = int(line.rsplit("=", 1)[1].lstrip(">="))
        elif line.startswith("word="):
            word = line[5:]
    return (a, b, c, L, exact, nodes, secs, word)


def main():
    maxc = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    budget = int(sys.argv[2]) if len(sys.argv) > 2 else 200_000_000
    depth = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    outfn = sys.argv[5] if len(sys.argv) > 5 else "data/sweep4.csv"

    jobs = [(a, b, c, budget, depth) for (a, b, c) in alphabets(maxc)]
    print(f"# {len(jobs)} normalised alphabets, maxc={maxc}, "
          f"budget={budget}, depth={depth}, workers={workers}", flush=True)

    os.makedirs(os.path.dirname(outfn) or ".", exist_ok=True)
    with open(outfn, "w") as f, ProcessPoolExecutor(max_workers=workers) as ex:
        f.write("a,b,c,L,exact,degenerate,nodes,secs,word\n")
        done = 0
        for (a, b, c, L, exact, nodes, secs, word) in ex.map(run_one, jobs):
            f.write(f"{a},{b},{c},{L},{int(bool(exact))},"
                    f"{int(degenerate(a,b,c))},{nodes},{secs:.3f},\"{word}\"\n")
            f.flush()
            done += 1
            if done % 25 == 0:
                print(f"# {done}/{len(jobs)}", flush=True)
            if L is not None and (L >= 100 or not exact):
                print(f"0,{a},{b},{c}  L{'=' if exact else '>='}{L} "
                      f"nodes={nodes} {secs:.1f}s", flush=True)
    print("# done", flush=True)


if __name__ == "__main__":
    main()
