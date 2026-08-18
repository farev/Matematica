"""Letter-space DFS for undirected-(num/den)+-free words over Sigma_n.

Canonical renaming (first occurrences are 0,1,2,...) kills the Sym(n)
symmetry: every free word has exactly one canonical representative, so
counts are counts of words up to letter renaming, and the tree is exhausted
iff the language (up to renaming) is exhausted.

Usage: python3 letterdfs.py <n> <num> <den> <maxdepth> [maxnodes]
Prints counts per length; says DIED at depth d if the tree is exhausted
below maxdepth, EXHAUSTED-CAP if maxnodes hit (inconclusive).
"""

import sys
import time

from urt import UInc


def run(n, num, den, maxdepth, maxnodes=50_000_000, verbose=True,
        collect_at=None):
    inc = UInc(num, den, maxdepth + 2)
    counts = [0] * (maxdepth + 1)
    nodes = 0
    capped = False
    deepest = []
    collected = []

    word = []

    def rec(used):
        nonlocal nodes, capped
        d = len(word)
        counts[d] += 1
        if collect_at is not None and d == collect_at:
            collected.append(tuple(word))
        if d == maxdepth:
            return
        if nodes >= maxnodes:
            capped = True
            return
        hi = used + 1 if used < n else n
        for c in range(hi):
            nodes += 1
            if inc.push(c):
                word.append(c)
                rec(used + 1 if c == used else used)
                word.pop()
            inc.pop()

    t0 = time.time()
    rec(0)
    dt = time.time() - t0
    died = None
    for d in range(maxdepth + 1):
        if counts[d] == 0:
            died = d
            break
    if verbose:
        step = max(1, maxdepth // 15)
        for d in range(0, maxdepth + 1, step):
            print(f"  len {d}: {counts[d]}")
        if died is not None and not capped:
            print(f"  DIED: no free words of length {died} "
                  f"(max length = {died - 1}), tree exhausted, "
                  f"{nodes} nodes [{dt:.1f}s]")
        elif capped:
            print(f"  CAP hit at {nodes} nodes (inconclusive) [{dt:.1f}s]")
        else:
            print(f"  alive at maxdepth {maxdepth}, {nodes} nodes [{dt:.1f}s]")
    return counts, died, capped, nodes, dt, collected


if __name__ == "__main__":
    n, num, den, maxdepth = map(int, sys.argv[1:5])
    maxnodes = int(sys.argv[5]) if len(sys.argv) > 5 else 50_000_000
    print(f"n={n} alpha={num}/{den} maxdepth={maxdepth}")
    run(n, num, den, maxdepth, maxnodes)
