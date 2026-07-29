"""Empirical audit of the Chase-Hunter-Tao (arXiv 2607.08712) deterministic
criterion, on the actual primes.

CHT Theorem 1.6 (instantiated, their Section 1.4): Gilbreath's conjecture for
row N-1 follows from
  (i)   entries of the normalized-gap array are << log^10 N,
  (ii)  the array contains no all-zero block of length ~ log^10 N,
  (iii) the array contains no {0,d}-valued block (d >= 2) of depth i and
        length >> 8^M * i, with M >= 10 log log N.

Their array: top row a_{0,j} = (p_{j+2}-p_{j+1})/2 - 1 (normalized gaps),
then iterated absolute differences.  We measure, for every row:
  * the longest run of zeros,
  * the longest {0,d}-valued run for each d >= 2 (a run in which every
    non-zero entry equals d),
and report the worst offenders against (ii) and (iii).
"""

import sys
import time

import numpy as np

from verify import primes_up_to


def longest_zero_run(nz, n):
    """nz = sorted positions of non-zero entries in a row of length n."""
    if len(nz) == 0:
        return n
    gaps = np.diff(nz) - 1
    best = int(gaps.max()) if len(gaps) else 0
    return max(best, int(nz[0]), int(n - 1 - nz[-1]))


def best_0d_runs(row):
    """For each d >= 2, the longest run of entries all in {0, d}.
    Returns dict d -> length, plus the overall winner (d, length, position).
    A {0,d}-run is a maximal window whose non-zero entries all equal d,
    bounded by non-zero entries != d (or the row ends)."""
    n = len(row)
    nz = np.flatnonzero(row)
    if len(nz) == 0:
        return {}, (0, n, 0), n and 0
    vals = row[nz]
    # boundaries of maximal constant-value segments of the non-zero entries
    cut = np.flatnonzero(vals[1:] != vals[:-1]) + 1
    starts = np.concatenate(([0], cut))          # segment start (index in nz)
    ends = np.concatenate((cut, [len(nz)]))      # segment end (exclusive)
    seg_val = vals[starts]
    # window spanned by segment s: from just after the previous non-zero
    # with a different value, to just before the next one
    left = np.where(starts == 0, 0, nz[starts - 1] + 1)
    right = np.where(ends == len(nz), n, nz[np.minimum(ends, len(nz) - 1)])
    right = np.where(ends == len(nz), n, right)
    lengths = right - left
    best = {}
    win = (0, 0, 0)
    for v, ln, lf in zip(seg_val, lengths, left):
        v, ln = int(v), int(ln)
        if v >= 2:
            if ln > best.get(v, 0):
                best[v] = ln
            if ln > win[1]:
                win = (v, ln, int(lf))
    return best, win, longest_zero_run(nz, n)


if __name__ == "__main__":
    limit = int(float(sys.argv[1])) if len(sys.argv) > 1 else 10**8
    t0 = time.time()
    ps = primes_up_to(limit)
    N = len(ps) - 2
    # CHT normalized gaps: a_j = (p_{j+2} - p_{j+1})/2 - 1
    row = ((np.diff(ps)[1:]) // 2 - 1).astype(np.int16)
    del ps
    print(f"N = {N:,} normalized gaps (primes <= {limit:,})")
    logN = np.log(N)
    print(f"log^10 N = {logN**10:.3e}   (CHT zero-block danger length)")
    M = 10 * np.log(np.log(N))
    print(f"M = 10 loglog N = {M:.1f}, 8^M = {8**M:.3e} (CHT {{0,d}}-block factor)\n")

    worst_zero = (0, -1)          # (length, depth)
    worst_0d = (0, -1, 0, 0)      # (length, depth, d, position)
    ratio_worst = (0.0, -1, 0, 0)  # (length/max(depth,1), depth, d, length)
    depth = 0
    while True:
        best, win, zrun = best_0d_runs(row)
        if zrun > worst_zero[0]:
            worst_zero = (zrun, depth)
        if win[1] > worst_0d[0]:
            worst_0d = (win[1], depth, win[0], win[2])
        r = win[1] / max(depth, 1)
        if r > ratio_worst[0]:
            ratio_worst = (r, depth, win[0], win[1])
        if depth in (0, 1, 2, 5, 10, 20, 40, 80, 160) :
            print(f"depth {depth:>3}: longest zero-run {zrun:>4},  "
                  f"longest {{0,d}}-run {win[1]:>6} (d={win[0]}) at j={win[2]}")
        if not np.any(row[1:] > 1) or depth > 400:
            break
        row = np.abs(np.diff(row))
        depth += 1
    print(f"\nscanned depths 0..{depth}  ({time.time()-t0:.0f}s)")
    print(f"WORST zero-run       : length {worst_zero[0]:,} at depth {worst_zero[1]}")
    print(f"  vs CHT danger length log^10 N = {logN**10:.3e}  "
          f"-> margin 10^{np.log10(logN**10 / max(worst_zero[0],1)):.1f}")
    print(f"WORST {{0,d}}-run      : length {worst_0d[0]:,} (d={worst_0d[2]}) "
          f"at depth {worst_0d[1]}, j={worst_0d[3]}")
    print(f"WORST length/depth   : {ratio_worst[0]:.1f} "
          f"(d={ratio_worst[2]}, length {ratio_worst[3]} at depth {ratio_worst[1]})")
    print(f"  vs CHT danger ratio 8^M = {8**M:.3e}  "
          f"-> margin 10^{np.log10(8**M / max(ratio_worst[0],1)):.1f}")
