"""Certified correlation & sign-pattern census for the Liouville function.

Computes, on a cumulative grid x = seg, 2*seg, 3*seg, ...

  L(x)        = sum_{n<=x} lambda(n)
  S_h(x)      = sum_{n<=x} lambda(n) lambda(n+h),        h = 1..32
  U_h(x)      = sum_{n<=x, n odd} lambda(n) lambda(n+h), h = 2,4,...,32
  T_*(x)      = triple correlations for {0,1,2}, {0,2,4}, {0,1,3}
  Q(x)        = quadruple correlation {0,1,2,3}
  c_0..c_255  = census of 8-long sign patterns (bit i = 1 iff lambda(n+i) = -1)

All quantities are exact integers (int64 accumulation, integer-only sieve).
The output CSV satisfies, by construction of the mathematics but NOT of the
code paths, the exact identities checked by certify.py:

  C1:  S_h(2y) = U_h(2y) + S_{h/2}(y)          (h even; 2-adic descent)
  C2:  S_h, T_*, Q  =  Walsh sums of the census (h <= 7)
  C3:  sum_eps census_eps(x) = x

Usage:
  python3 census_run.py XMAX SEG WORKERS OUTPREFIX [--coverage KMAX]

--coverage (single-process only) additionally tracks, for k <= KMAX, the
first occurrence n of every length-k sign pattern, writing
OUTPREFIX_coverage.csv (per-k: N_k = x by which all 2^k patterns occurred).
"""

import json
import math
import os
import sys
import time
from multiprocessing import Pool

import numpy as np

from liouville import lambda_block, primes_up_to

HMAX = 32
EXTRA = HMAX + 8  # sieve overhang past segment end
EVEN_H = list(range(2, HMAX + 1, 2))

_PRIMES = None


def _init(primes):
    global _PRIMES
    _PRIMES = primes


def segment_stats(args):
    """Exact integer statistics + float64 harmonic sums for n in [L, L+seg).

    All +-1 correlation sums are computed as float64 BLAS dot products.
    Every intermediate value is an integer of magnitude < 2^53, so each
    float64 addition is EXACT regardless of summation order: the integer
    outputs are certified, not approximate.  Only the harmonic (1/n-weighted)
    columns are genuinely floating point.
    """
    L, seg = args
    lam8 = lambda_block(L, L + seg + EXTRA, _PRIMES)
    lam = lam8.astype(np.float64)
    core = lam[:seg]
    ints = np.zeros(1 + 1 + HMAX + len(EVEN_H) + 4 + 256, dtype=np.int64)
    flts = np.zeros(1 + HMAX, dtype=np.float64)
    i = 0
    ints[i] = seg; i += 1
    ints[i] = int(round(core.sum())); i += 1
    for h in range(1, HMAX + 1):
        ints[i] = int(round(np.dot(core, lam[h:h + seg]))); i += 1
    # odd n, even shift h: n and n+h are consecutive-in-odd-subsequence
    # entries at distance h/2, so U_h is a contiguous dot product.
    start = 0 if L % 2 == 1 else 1
    odd_full = np.ascontiguousarray(lam[start::2])
    m = (seg - start + 1) // 2
    odd_core = odd_full[:m]
    for h in EVEN_H:
        ints[i] = int(round(np.dot(odd_core, odd_full[h // 2: h // 2 + m])))
        i += 1
    t01 = core * lam[1:1 + seg]
    ints[i] = int(round(np.dot(t01, lam[2:2 + seg]))); i += 1
    ints[i] = int(round(np.dot(core * lam[2:2 + seg], lam[4:4 + seg]))); i += 1
    ints[i] = int(round(np.dot(t01, lam[3:3 + seg]))); i += 1
    ints[i] = int(round(np.dot(t01, lam[2:2 + seg] * lam[3:3 + seg]))); i += 1
    del t01
    bits = (lam8[:seg + 7] < 0).astype(np.int32)
    codes = np.zeros(seg, dtype=np.int32)
    for b in range(8):
        codes += bits[b:b + seg] << b
    ints[i:i + 256] = np.bincount(codes, minlength=256); i += 256
    # harmonic columns (float64; total accumulated rounding error < 1e-8)
    w = core / np.arange(L, L + seg, dtype=np.float64)
    flts[0] = w.sum()
    for h in range(1, HMAX + 1):
        flts[h] = np.dot(w, lam[h:h + seg])
    return ints, flts


class Coverage:
    """First-occurrence tracking of length-k sign patterns, k <= kmax."""

    def __init__(self, kmax):
        self.kmax = kmax
        self.first = {k: np.full(1 << k, np.iinfo(np.int64).max, dtype=np.int64)
                      for k in range(1, kmax + 1)}
        self.done = {k: False for k in range(1, kmax + 1)}
        self.n_done = {}

    def update(self, L, seg, lam):
        if all(self.done.values()):
            return
        bits = (lam[:seg + self.kmax - 1] < 0).astype(np.int64)
        codes = np.zeros(seg, dtype=np.int64)
        for b in range(self.kmax):
            codes += bits[b:b + seg] << b
        for k in range(1, self.kmax + 1):
            if self.done[k]:
                continue
            ck = codes & ((1 << k) - 1)
            first = self.first[k]
            new = first[ck] == np.iinfo(np.int64).max
            if new.any():
                idx = np.nonzero(new)[0]
                uc, ui = np.unique(ck[idx], return_index=True)
                first[uc] = L + idx[ui]
            if (first != np.iinfo(np.int64).max).all():
                self.done[k] = True
                self.n_done[k] = int(first.max())


def main():
    xmax = int(float(sys.argv[1]))
    seg = int(float(sys.argv[2]))
    workers = int(sys.argv[3])
    prefix = sys.argv[4]
    kmax = 0
    if "--coverage" in sys.argv:
        kmax = int(sys.argv[sys.argv.index("--coverage") + 1])
        assert workers == 1, "coverage requires a single process"
    assert xmax % seg == 0
    nseg = xmax // seg

    primes = primes_up_to(math.isqrt(xmax + seg + EXTRA))
    meta = dict(xmax=xmax, seg=seg, workers=workers, kmax=kmax,
                numpy=np.__version__, python=sys.version.split()[0],
                started=time.strftime("%F %T"), machine="Apple M3 Pro 12c 36GB")
    with open(prefix + "_meta.json", "w") as f:
        json.dump(meta, f, indent=1)

    header = (["x", "Lx"] + [f"S{h}" for h in range(1, HMAX + 1)]
              + [f"U{h}" for h in EVEN_H]
              + ["T012", "T024", "T013", "Q0123"]
              + [f"c{j}" for j in range(256)]
              + ["hL"] + [f"h{h}" for h in range(1, HMAX + 1)])
    n_int = 2 + HMAX + len(EVEN_H) + 4 + 256   # incl. x slot
    cum_i = np.zeros(n_int, dtype=np.int64)     # slot 0 counts n's
    cum_f = np.zeros(1 + HMAX, dtype=np.float64)
    cov = Coverage(kmax) if kmax else None
    t0 = time.time()
    tasks = [(k * seg + 1, seg) for k in range(nseg)]

    out = open(prefix + "_grid.csv", "w", buffering=1 << 20)
    out.write(",".join(header) + "\n")

    def handle(k, row):
        nonlocal cum_i, cum_f
        ints, flts = row
        cum_i += ints
        cum_f += flts
        x = (k + 1) * seg
        out.write(str(x) + "," + ",".join(map(str, cum_i[1:]))
                  + "," + ",".join("%.17g" % v for v in cum_f) + "\n")
        if (k + 1) % 200 == 0 or k + 1 == nseg:
            el = time.time() - t0
            print(f"seg {k+1}/{nseg}  x={x:.2e}  {el:.0f}s  "
                  f"eta {el/(k+1)*(nseg-k-1):.0f}s", flush=True)

    if workers == 1:
        _init(primes)
        for k, (Ls, sg) in enumerate(tasks):
            if cov is not None:
                lam8 = lambda_block(Ls, Ls + sg + EXTRA, primes)
                cov.update(Ls, sg, lam8)
            handle(k, segment_stats((Ls, sg)))
    else:
        with Pool(workers, initializer=_init, initargs=(primes,)) as pool:
            for k, row in enumerate(pool.imap(segment_stats, tasks,
                                              chunksize=4)):
                handle(k, row)
    out.close()

    if cov is not None:
        with open(prefix + "_coverage.csv", "w") as f:
            f.write("k,N_k,complete,last_pattern_code\n")
            for k in range(1, kmax + 1):
                fk = cov.first[k]
                if cov.done[k]:
                    f.write(f"{k},{cov.n_done[k]},1,{int(fk.argmax())}\n")
                else:
                    miss = int((fk == np.iinfo(np.int64).max).sum())
                    f.write(f"{k},,0,missing={miss}\n")
        np.savez_compressed(prefix + "_firstocc.npz",
                            **{f"k{k}": cov.first[k]
                               for k in range(1, kmax + 1)})

    meta["finished"] = time.strftime("%F %T")
    meta["seconds"] = round(time.time() - t0, 1)
    with open(prefix + "_meta.json", "w") as f:
        json.dump(meta, f, indent=1)
    print("done", meta["seconds"], "s")


if __name__ == "__main__":
    main()
