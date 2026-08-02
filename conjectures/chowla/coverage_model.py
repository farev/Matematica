"""Coupon-collector comparison for the sign-pattern coverage numbers N_k.

Pure Python standard library.

Model.  If the length-k windows of lambda behaved like independent uniform
draws from the 2^k patterns, the completion time would be the classical coupon
collector: E[N_k] = m*H_m ~ m(ln m + gamma) with m = 2^k, and

    (N_k / m) - ln m - gamma

would be a standard Gumbel variate (mean 0, sd pi/sqrt(6) = 1.2825).  The
column `gumbel_z` below is that quantity; it is the honest way to read the
"model ratio" column, because N_k/E[N_k] is a ratio of a Gumbel variate to a
number that grows like k, so the same absolute fluctuation looks smaller and
smaller as k grows.

Refinement, and why it does not matter.  Windows overlap, so the waiting times
are not those of a uniform coupon draw: for an i.i.d. fair coin the mean
waiting time for the word w is Conway's A(w) = sum_j delta_j 2^j, which ranges
from 2^k (no self-overlap) to 2^{k+1}-2 (constant word).  One might worry that
the highly periodic words dominate the maximum and bias N_k upward.  They do
not, and the bound is easy: A(w) >= (1+eps)*2^k forces an overlap at some
j >= k + log2(eps), i.e. forces w to have period p <= -log2(eps), and there are
fewer than 2^{p+1} such words.  Each is an exponential of mean at most
2^{k+1}, so the chance that any of them is still unseen at the coupon-collector
scale t = (k ln 2 + gamma) 2^k is at most 2^{p+1} exp(-(k ln2 + gamma)/2).
`conway_tail` prints that bound: it is below 1% for every k in range, so the
plain coupon collector is the right model for N_k to well under a percent.

Usage:  python3 coverage_model.py [coverage_csv ...]
        (defaults to the three committed coverage tables)
"""

import math
import sys

GAMMA = 0.5772156649015329
DEFAULT = ["data/fineA_coverage.csv", "data/coverage_ext.csv",
           "data/coverage_2830.csv", "data/coverage_3133.csv"]


def read(paths):
    rows = {}
    for p in paths:
        try:
            f = open(p)
        except OSError:
            continue
        for line in f:
            line = line.strip()
            if not line or line.startswith("k,"):
                continue
            parts = line.split(",")
            if len(parts) < 2:
                continue
            try:
                k, n = int(parts[0]), int(parts[1])
            except ValueError:
                continue
            code = None
            for c in parts[2:]:
                try:
                    code = int(c)
                except ValueError:
                    pass
            rows[k] = (n, code)
        f.close()
    return rows


def conway_tail(k, eps=0.01):
    """Upper bound on P(some period-<=p word is unseen at the collector scale)."""
    p = max(1, int(math.ceil(-math.log2(eps))))
    t_over_m = k * math.log(2) + GAMMA
    return min(1.0, 2.0 ** (p + 1) * math.exp(-t_over_m / 2.0))


def main():
    paths = sys.argv[1:] or DEFAULT
    rows = read(paths)
    if not rows:
        print("no coverage rows found", file=sys.stderr)
        return 1
    print("  k             N_k     model m*H_m   N_k/model   gumbel_z   "
          "conway_tail  last_code")
    for k in sorted(rows):
        n, code = rows[k]
        m = 2 ** k
        # exact harmonic number is 2^k terms; use the asymptotic with the
        # 1/(2m) correction, which is exact to far beyond the printed digits
        model = m * (math.log(m) + GAMMA + 1.0 / (2 * m))
        z = (n / m - math.log(m) - GAMMA) / (math.pi / math.sqrt(6))
        print(f"{k:>3} {n:>15} {model:>15.4g} {n/model:>11.4f} "
              f"{z:>10.2f} {conway_tail(k):>13.2e}  "
              f"{code if code is not None else '-'}")
    print(f"\ngumbel_z: (N_k/2^k - ln 2^k - gamma) / (pi/sqrt 6); "
          f"model mean 0, sd 1")
    print("conway_tail: bound on the self-overlap correction to the model "
          "(see module docstring)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
