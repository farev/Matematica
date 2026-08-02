"""Certified 4-point correlation census for the Liouville function.

Records, on the cumulative grid x = seg, 2*seg, ...:

  Lx, Q_{0,a,b,c}(x) = sum_{n<=x} lambda(n)lambda(n+a)lambda(n+b)lambda(n+c)
  for six base quadruples and their doubles, the odd-restricted V columns
  for the doubles, and the 256-cell 8-window census.

Exactness: same argument as census_run.py (float64 BLAS dots of +-1
vectors; every intermediate an integer < 2^53, every IEEE add exact).

Certificates (certify_quad.py):
  C1Q  Q_{2a,2b,2c}(2y) = V_{2a,2b,2c}(2y) + Q_{a,b,c}(y)   [Lemma 1, 4 factors]
  C2Q  window-<=7 quadruples equal Walsh sums over the census
  C3   census sums to x
  XR   census columns identical to the certified mainB12 grid rows

Usage: python3 quad_run.py XMAX SEG WORKERS OUTPREFIX
"""

import json
import math
import sys
import time
from multiprocessing import Pool

import numpy as np

from liouville import lambda_block, primes_up_to

BASES = [(1, 2, 3), (1, 2, 4), (1, 3, 5), (2, 3, 4), (1, 2, 5), (1, 4, 5)]
DOUBLES = [(2 * a, 2 * b, 2 * c) for a, b, c in BASES]
QUADS = BASES + DOUBLES
EXTRA = 24

_PRIMES = None


def _init(primes):
    global _PRIMES
    _PRIMES = primes


def qname(t):
    return "Q" + "".join(str(v) for v in t)


def segment_stats(args):
    L, seg = args
    lam8 = lambda_block(L, L + seg + EXTRA, _PRIMES)
    lam = lam8.astype(np.float64)
    core = lam[:seg]
    out = np.zeros(2 + len(QUADS) + len(DOUBLES) + 256, dtype=np.int64)
    i = 0
    out[i] = seg; i += 1
    out[i] = int(round(core.sum())); i += 1
    for (a, b, c) in QUADS:
        t = core * lam[a:a + seg] * lam[b:b + seg]
        out[i] = int(round(np.dot(t, lam[c:c + seg]))); i += 1
    # odd-restricted V for the doubles: all four points stay in the odd
    # subsequence at half the offsets, so these are contiguous dots.
    start = 0 if L % 2 == 1 else 1
    odd_full = np.ascontiguousarray(lam[start::2])
    m = (seg - start + 1) // 2
    oc = odd_full[:m]
    for (a, b, c) in BASES:            # half-offsets of the doubles
        t = oc * odd_full[a:a + m] * odd_full[b:b + m]
        out[i] = int(round(np.dot(t, odd_full[c:c + m]))); i += 1
    bits = (lam8[:seg + 7] < 0).astype(np.int32)
    codes = np.zeros(seg, dtype=np.int32)
    for b in range(8):
        codes += bits[b:b + seg] << b
    out[i:i + 256] = np.bincount(codes, minlength=256); i += 256
    return out


def main():
    xmax = int(float(sys.argv[1]))
    seg = int(float(sys.argv[2]))
    workers = int(sys.argv[3])
    prefix = sys.argv[4]
    assert xmax % seg == 0
    nseg = xmax // seg
    primes = primes_up_to(math.isqrt(xmax + seg + EXTRA))
    meta = dict(xmax=xmax, seg=seg, workers=workers,
                quads=[list(q) for q in QUADS],
                numpy=np.__version__, python=sys.version.split()[0],
                started=time.strftime("%F %T"), machine="Apple M3 Pro 12c 36GB")
    with open(prefix + "_meta.json", "w") as f:
        json.dump(meta, f, indent=1)

    header = (["x", "Lx"] + [qname(q) for q in QUADS]
              + ["V" + qname(q)[1:] for q in DOUBLES]
              + [f"c{j}" for j in range(256)])
    cum = np.zeros(len(header), dtype=np.int64)
    t0 = time.time()
    tasks = [(k * seg + 1, seg) for k in range(nseg)]
    out = open(prefix + "_grid.csv", "w", buffering=1 << 16)
    out.write(",".join(header) + "\n")

    def handle(k, row):
        nonlocal cum
        cum += row
        out.write(str((k + 1) * seg) + "," + ",".join(map(str, cum[1:])) + "\n")
        if (k + 1) % 500 == 0 or k + 1 == nseg:
            el = time.time() - t0
            print(f"seg {k+1}/{nseg}  x={(k+1)*seg:.2e}  {el:.0f}s  "
                  f"eta {el/(k+1)*(nseg-k-1):.0f}s", flush=True)

    if workers == 1:
        _init(primes)
        for k, t in enumerate(tasks):
            handle(k, segment_stats(t))
    else:
        with Pool(workers, initializer=_init, initargs=(primes,)) as pool:
            for k, row in enumerate(pool.imap(segment_stats, tasks, chunksize=4)):
                handle(k, row)
    out.close()
    meta["finished"] = time.strftime("%F %T")
    meta["seconds"] = round(time.time() - t0, 1)
    with open(prefix + "_meta.json", "w") as f:
        json.dump(meta, f, indent=1)
    print("done", meta["seconds"], "s")


if __name__ == "__main__":
    main()
