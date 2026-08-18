#!/usr/bin/env python3
"""Counts table and heuristic comparison for the census ladder.

Reads HIST lines (per-base-3-length term counts) from run logs — full-mode
logs carry one HIST line; task-mode workers carry one each, which add — and
emits:
  * G(3^k) cumulative counts for every k up to the run's L,
  * local exponents theta(k1,k2) = ln(G2/G1) / ((k2-k1) ln 3) per band,
  * a least-squares global fit of ln G vs ln N over a stated range
    (NUMERICAL: it is a fit),
  * the independence-heuristic expectation of further 1155-terms, computed
    from the exact term list where given and from length bands beyond
    (NUMERICAL: it conditions on the heuristic).
Usage: analyze.py L LOG [LOG...] [--terms FILE] [--fit kmin kmax]
"""
import sys
from math import log

def read_hists(paths):
    hist = {}
    for p in paths:
        for line in open(p):
            if line.startswith("HIST"):
                for tok in line.split()[1:]:
                    k, v = tok.split(":")
                    hist[int(k)] = hist.get(int(k), 0) + int(v)
    return hist

def main():
    L = int(sys.argv[1])
    logs = []
    terms_file = None
    fit_lo, fit_hi = 50, None
    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--terms":
            terms_file = args[i + 1]
            i += 2
        elif args[i] == "--fit":
            fit_lo, fit_hi = int(args[i + 1]), int(args[i + 2])
            i += 3
        else:
            logs.append(args[i])
            i += 1
    if fit_hi is None:
        fit_hi = L
    hist = read_hists(logs)
    total = sum(hist.values())
    print(f"# ladder L={L}: {total} terms below 3^{L} (3^{L} ~ {L*log(3)/log(10):.1f} decimal digits)")
    print("# k  G(3^k)  log10(3^k)")
    G = 0
    cum = {}
    for k in range(L + 1):
        G += hist.get(k, 0)
        cum[k] = G
        if k % 10 == 0 or k == L or k == 148:
            print(f"{k} {G} {k*log(3)/log(10):.2f}")
    print("\n# local exponents theta = ln(G2/G1)/((k2-k1) ln 3) per 50-level band")
    for k1 in range(100, L, 50):
        k2 = min(k1 + 50, L)
        if cum[k1] and cum[k2] > cum[k1]:
            th = log(cum[k2] / cum[k1]) / ((k2 - k1) * log(3))
            print(f"band 3^{k1}..3^{k2}: theta_local = {th:.4f}")
    # global fit ln G = a + theta ln N over k in [fit_lo, fit_hi]
    pts = [(k * log(3), log(cum[k])) for k in range(fit_lo, fit_hi + 1)
           if cum[k] > 0]
    n = len(pts)
    sx = sum(x for x, _ in pts); sy = sum(y for _, y in pts)
    sxx = sum(x * x for x, _ in pts); sxy = sum(x * y for x, y in pts)
    theta = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    a = (sy - theta * sx) / n
    print(f"\n# NUMERICAL global fit over k in [{fit_lo},{fit_hi}]: "
          f"G(N) ~ {2.718281828**a:.3f} * N^{theta:.5f}   (heuristic: 0.02595)")
    # 1155 expectation, conditional on independence heuristic:
    # P(all base-11 digits of n <= 5) ~ (6/11)^{log_11 n} = n^{-0.25264}
    alpha = 1 - log(6) / log(11)
    exp_small = 0.0
    if terms_file:
        for line in open(terms_file):
            line = line.strip()
            if ":" not in line:
                continue
            v = int(line.split(":")[0])
            if v > 3160:
                exp_small += v ** (-alpha) if v < 10**300 else 0.0
        print(f"# NUMERICAL heuristic E[#1155-terms among exact terms in file, n>3160] = {exp_small:.4f}")
    exp_bands = 0.0
    kfile = 0
    if terms_file:
        # exact list assumed complete below 3^kfile: infer from file max
        vmax = max(int(l.split(":")[0]) for l in open(terms_file) if ":" in l)
        while 3 ** kfile <= vmax:
            kfile += 1
    for k in range(max(kfile, 9), L):
        band = cum[k + 1] - cum[k] if k + 1 <= L else 0
        if band:
            exp_bands += band * (3.0 ** (-(k) * alpha))
    print(f"# NUMERICAL heuristic E[#1155-terms in bands 3^{max(kfile,9)}..3^{L}] <= {exp_bands:.3e}")

if __name__ == "__main__":
    main()
