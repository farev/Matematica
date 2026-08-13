#!/usr/bin/env python3
"""dss_reference.py — independent reference implementation of the DSS search.

Same tree specification as dss_search.c (window P1, sum bound P2, second-moment
bound P3, incremental collision test P4, identical break/skip semantics), but
implemented differently: Python bigints as sum bitsets, plain recursion, no
prefix splitting. Node counts per depth must match the C engine exactly on any
(n, m) it can reach; disagreement means one of the two trees is wrong.

Usage: python3 dss_reference.py n m [--enum]
Emits the same RESULT line format as the C engine (minus tasks/threads).
"""
import sys
import time

FMIN = [0, 1, 2, 4, 7, 13, 24, 44, 84, 161]  # A276661(0..9); ladder-honest


def run(n, m, enum=False):
    target_sum = (1 << n) - 1
    target_sq = ((1 << (2 * n)) - 1) // 3
    nodes = [0] * (n + 1)
    solutions = []
    found = False

    def rec(depth, chosen, total, sqsum, sums):
        nonlocal found
        if found and not enum:
            return
        r = n - depth
        if r == 0:
            solutions.append(list(reversed(chosen)))
            if not enum:
                found = True
            return
        c = chosen[-1]
        for a in range(c - 1, FMIN[r] - 1, -1):
            msum = total + a + sum(a - j for j in range(1, r))
            msq = sqsum + a * a + sum((a - j) ** 2 for j in range(1, r))
            if msum < target_sum or msq < target_sq:
                break                      # P2/P3 monotone in a
            shifted = sums << a
            if sums & shifted:
                continue                   # P4 collision
            nodes[depth + 1] += 1
            rec(depth + 1, chosen + [a], total + a, sqsum + a * a,
                sums | shifted)
            if found and not enum:
                return

    t0 = time.time()
    nodes[1] = 1
    rec(1, [m], m, m * m, (1 << 0) | (1 << m))
    secs = time.time() - t0
    for s in solutions:
        print(f"SOLUTION n={n} m={m} set={','.join(map(str, s))}")
    status = "FOUND" if solutions else "NONE"
    print(f"RESULT n={n} m={m} status={status} solutions={len(solutions)} "
          f"nodes={sum(nodes)} depth_nodes={','.join(map(str, nodes[1:]))} "
          f"time={secs:.3f}")
    return status, nodes


if __name__ == "__main__":
    n, m = int(sys.argv[1]), int(sys.argv[2])
    run(n, m, enum="--enum" in sys.argv)
