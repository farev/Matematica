"""Calibration bench for the "microscope" program (see MICROSCOPE.md).

Measures, on the actual primes up to x, the maximal length of every
dangerous micro-pattern that a proof of Gilbreath via the CHT criterion
must exclude:

  L_cpap    longest run of EQUAL consecutive gaps
            (= longest AP of consecutive primes, minus 1;
               depth-1 zero-block of the CHT array)
  L_dconst  longest run with |gap difference| constant and nonzero
            (depth-1 constant blocks: the next lens up)
  L_par0/2  longest run of gaps all == 0 / all == 2 (mod 4)
            (constant gap parity: CHT scenario-1 fuel)
  L_2val    longest run of gaps taking at most 2 distinct values
            ({0,d}-block fuel at the top row: CHT scenario 2)

All are O(n) vectorized run-length scans on the gap array.
"""

import sys
import time

import numpy as np

from verify import primes_up_to


def run_lengths(condition):
    """Lengths of maximal True-runs in a boolean array."""
    c = np.asarray(condition, dtype=bool)
    if not c.any():
        return np.array([0])
    d = np.diff(c.astype(np.int8))
    starts = np.flatnonzero(d == 1) + 1
    ends = np.flatnonzero(d == -1) + 1
    if c[0]:
        starts = np.concatenate(([0], starts))
    if c[-1]:
        ends = np.concatenate((ends, [len(c)]))
    return ends - starts


def equal_value_runs(vals):
    """(max run of equal values, argmax start index in vals)."""
    eq = vals[1:] == vals[:-1]
    L = run_lengths(eq)
    return (int(L.max()) + 1) if len(L) else 1


def two_valued_max(vals):
    """Longest stretch of vals using at most 2 distinct values.
    Work on maximal constant segments; adjacent segments have different
    values, so a 2-valued stretch = consecutive segments alternating
    between two values, i.e. maximal chains where v[s+2] == v[s]."""
    cut = np.flatnonzero(vals[1:] != vals[:-1]) + 1
    starts = np.concatenate(([0], cut))
    seg_len = np.diff(np.concatenate((starts, [len(vals)])))
    v = vals[starts]
    if len(v) < 3:
        return len(vals)
    ok = v[2:] == v[:-2]           # segment s+2 continues the pair
    # chain of segments [s, s+m] valid if ok[s..s+m-2] all True
    best = 0
    csum = np.concatenate(([0], np.cumsum(seg_len)))
    # runs of True in ok give chains: chain covering segments s..s+r+1
    L = run_lengths(ok)
    d = np.diff(ok.astype(np.int8))
    st = np.flatnonzero(d == 1) + 1
    if len(ok) and ok[0]:
        st = np.concatenate(([0], st))
    for s, r in zip(st, L):
        best = max(best, int(csum[s + r + 2] - csum[s]))
    # also any two adjacent segments alone
    two = seg_len[:-1] + seg_len[1:]
    best = max(best, int(two.max()) if len(two) else int(seg_len.max()))
    return best


def bench(limit):
    t0 = time.time()
    g = np.diff(primes_up_to(limit))[1:]  # gaps of odd primes
    n = len(g)
    L_cpap = equal_value_runs(g)
    h = np.abs(np.diff(g.astype(np.int64)))
    # runs of equal nonzero |gap difference|
    eqh = (h[1:] == h[:-1]) & (h[1:] != 0)
    Lh = run_lengths(eqh)
    L_dconst = (int(Lh.max()) + 2) if len(Lh) else 2
    L_par0 = int(run_lengths(g % 4 == 0).max())
    L_par2 = int(run_lengths(g % 4 == 2).max())
    L_2val = two_valued_max(g)
    lg = np.log(limit)
    print(f"x=10^{np.log10(limit):.0f}  n_gaps={n:,}  ({time.time()-t0:.0f}s)")
    print(f"  L_cpap={L_cpap} (gaps)  -> CPAP of {L_cpap+1} primes"
          f"   [{L_cpap/lg:.2f} log x]")
    print(f"  L_dconst={L_dconst}   L_par0={L_par0}   L_par2={L_par2}"
          f"   L_2val={L_2val}   [{L_2val/lg:.2f} log x]")
    print(f"  danger threshold log^10 x = {lg**10:.2e}")
    return dict(x=limit, L_cpap=L_cpap, L_dconst=L_dconst, L_par0=L_par0,
                L_par2=L_par2, L_2val=L_2val)


if __name__ == "__main__":
    limit = float(sys.argv[1]) if len(sys.argv) > 1 else 1e9
    rows = []
    e = 6
    while 10**e <= limit:
        rows.append(bench(10**e))
        e += 1
    import csv
    with open("microscope_bench.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader()
        w.writerows(rows)
    print("saved microscope_bench.csv")
