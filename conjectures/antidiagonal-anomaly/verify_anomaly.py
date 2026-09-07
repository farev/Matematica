#!/usr/bin/env python3
"""Exact verification of the antidiagonal-anomaly criterion of Gil-Liang-Odetola-Weiner
(arXiv:2609.01562, Proposition 7.2): for an obstruction B = (a, n-a), 2a < n, the boundary
point (1,0) carries more traffic than (1,1) iff R_n(a) = G(n,a)/D(n) > 1, where
    G(n,a) = (n-2a+1)/(n-a) * C(n,a) * C(n-2,a-1),   D(n) = C(2n-2,n-1)/n.
Lemma 1 of NOTE.md rewrites this as the integer inequality
    C(n,a)^2 * a * (n-2a+1)  >  (n-1) * C(2n-2, n-1).
This script decides, for every n in [N1, N2] and every 1 <= a <= n/2, whether the
inequality holds, using only integer arithmetic (running-product binomials), and writes a
certificate line per n:  n  a_max  A(n)  ratio_floor_1e9  A(n) = number of a with R_n(a) > 1.
The maximizing a and floor(1e9 * rho(n)) are exact integers (integer division).

Usage: python3 verify_anomaly.py N1 N2 [certificate.csv]
"""
import sys, time

def run(N1, N2, out=None):
    t0 = time.time()
    anomalous = []
    f = open(out, "w") if out else None
    if f: f.write("n,a_max,num_anomalous_a,floor_1e9_rho\n")
    worst = (0, 1, None, None)   # (num, den, n, a) of the largest ratio in range
    for n in range(N1, N2 + 1):
        cb = 1                               # C(2n-2, n-1) by running product
        for i in range(1, n):
            cb = cb * (n - 1 + i) // i
        rhs = (n - 1) * cb
        c = 1                                # C(n, a) by running product
        bestv, besta, cnt = 0, None, 0
        for a in range(1, n // 2 + 1):
            c = c * (n - a + 1) // a
            v = c * c * a * (n - 2 * a + 1)
            if v > bestv:
                bestv, besta = v, a
            if v > rhs:
                cnt += 1
        if cnt:
            anomalous.append(n)
        if bestv * worst[1] > worst[0] * rhs:
            worst = (bestv, rhs, n, besta)
        if f:
            f.write(f"{n},{besta},{cnt},{(10**9 * bestv) // rhs}\n")
    if f: f.close()
    return anomalous, worst, time.time() - t0

if __name__ == "__main__":
    N1, N2 = int(sys.argv[1]), int(sys.argv[2])
    out = sys.argv[3] if len(sys.argv) > 3 else None
    anomalous, worst, dt = run(N1, N2, out)
    def runs(xs):
        if not xs: return []
        res, s, p = [], xs[0], xs[0]
        for x in xs[1:]:
            if x == p + 1: p = x
            else: res.append((s, p)); s = p = x
        res.append((s, p)); return res
    print(f"range [{N1},{N2}]: anomalous n = {runs(anomalous)} (count {len(anomalous)})")
    print(f"largest rho(n) in range: {worst[0]/worst[1]:.12f} at n={worst[2]}, a={worst[3]}")
    print(f"elapsed {dt:.1f}s")
