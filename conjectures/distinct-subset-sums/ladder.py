#!/usr/bin/env python3
"""ladder.py — re-derive f(n) = A276661(n) for n = 2..9 from scratch.

For each n, sweeps m upward from f(n-1); the first m with a DSS n-set is
f(n). Bootstrap honesty: the level-n run's fmin prunes consult only
f(1..n-1), which this ladder has already re-derived by the time level n runs.

Checks performed per level:
  - value equals the OEIS A276661 term (generator-vs-OEIS cross-check);
  - every solution the engine reports is re-validated by validate_set.is_dss
    (independent brute enumeration);
  - for n <= LEVEL_XCHECK, the Python reference engine re-runs every m and
    its per-depth node counts must match the C engine exactly;
  - at m = f(n) an --enum rerun records ALL optimal sets.

Outputs: data/ladder_sweep.csv, data/optimal_sets.txt, stdout summary.
"""
import csv
import re
import subprocess
import sys
import time

from validate_set import is_dss
from dss_reference import run as ref_run

A276661 = {1: 1, 2: 2, 3: 4, 4: 7, 5: 13, 6: 24, 7: 44, 8: 84, 9: 161}
LEVEL_XCHECK = 7          # exhaustive C-vs-Python node-count comparison n <= 7
RESULT_RE = re.compile(
    r"RESULT n=(\d+) m=(\d+) status=(\w+) solutions=(\d+) nodes=(\d+) "
    r"depth_nodes=([\d,]+) tasks=(\d+) time=([\d.]+) threads=(\d+)")
SOL_RE = re.compile(r"SOLUTION n=\d+ m=\d+ set=([\d,]+)")


def run_c(n, m, enum=False):
    cmd = ["./dss_search", str(n), str(m)] + (["--enum"] if enum else [])
    out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    mres = RESULT_RE.search(out)
    assert mres, out
    sols = [[int(x) for x in s.split(",")] for s in SOL_RE.findall(out)]
    return mres, sols


def main():
    t0 = time.time()
    rows = []
    opt_lines = []
    for n in range(2, 10):
        start = A276661[n - 1]
        found_m = None
        for m in range(start, A276661[n] + 5):
            mres, sols = run_c(n, m)
            status, nodes, depth_nodes, tsec = (mres.group(3), int(mres.group(5)),
                                                mres.group(6), float(mres.group(8)))
            rows.append([n, m, status, mres.group(4), nodes, depth_nodes, tsec])
            if n <= LEVEL_XCHECK:
                rstatus, rnodes = ref_run(n, m)
                assert rstatus == status, f"status mismatch n={n} m={m}"
                # node counts are traversal-order-independent only on FULL
                # traversals; EXISTS runs that hit exit early and may differ
                if status == "NONE":
                    assert ",".join(map(str, rnodes[1:])) == depth_nodes, \
                        f"node-count mismatch n={n} m={m}: C={depth_nodes} py={rnodes[1:]}"
            for s in sols:
                assert is_dss(s), f"engine reported non-DSS set {s}"
                assert max(s) == m and len(s) == n
            if status == "FOUND":
                found_m = m
                break
        assert found_m == A276661[n], \
            f"LADDER BREAK: f({n}) = {found_m}, OEIS says {A276661[n]}"
        emres, esols = run_c(n, found_m, enum=True)
        for s in esols:
            assert is_dss(s) and max(s) == found_m and len(s) == n
        if n <= LEVEL_XCHECK:
            # enum runs are full traversals in both engines: counts and the
            # complete solution lists must agree exactly
            import io, contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rstatus, rnodes = ref_run(n, found_m, enum=True)
            rsols = sorted([int(x) for x in s.split(",")]
                           for s in SOL_RE.findall(buf.getvalue()))
            assert rstatus == "FOUND"
            assert ",".join(map(str, rnodes[1:])) == emres.group(6), \
                f"enum node mismatch n={n}: C={emres.group(6)} py={rnodes[1:]}"
            assert rsols == sorted(sorted(s) for s in esols), \
                f"enum solution-set mismatch n={n}"
        opt_lines.append(f"n={n} f(n)={found_m} optimal_sets={len(esols)}")
        for s in esols:
            opt_lines.append(f"  {s}")
        print(f"f({n}) = {found_m}  [matches A276661; {len(esols)} optimal set(s); "
              f"clears+hit nodes recorded]")

    with open("data/ladder_sweep.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "m", "status", "solutions", "nodes", "depth_nodes", "seconds"])
        w.writerows(rows)
    with open("data/optimal_sets.txt", "w") as fh:
        fh.write("\n".join(opt_lines) + "\n")
    print(f"ladder complete in {time.time() - t0:.1f}s; "
          f"C-vs-Python node counts matched exhaustively for n <= {LEVEL_XCHECK}")


if __name__ == "__main__":
    sys.exit(main())
