#!/usr/bin/env python3
"""Table for NOTE.md section 6: for 370 <= n <= 500 (default), the integer maximiser a_n of
R_n(a), the real maximiser x*(n) = (sqrt(2n+1)-1)/4 of phi_n, the rounding offset
delta_n = |(n/2 - a_n) - x*(n)|, floor(1e9 * rho(n)) (exact integer arithmetic) and the anomaly flag.
x* and delta are floating point and serve display only; a_n and rho are exact.
Usage: python3 transition_table.py [N1 N2] [out.csv]
"""
import sys
from math import sqrt
N1 = int(sys.argv[1]) if len(sys.argv) > 1 else 370
N2 = int(sys.argv[2]) if len(sys.argv) > 2 else 500
out = sys.argv[3] if len(sys.argv) > 3 else "transition_table.csv"
with open(out, "w") as f:
    f.write("n,a_n,x_star,delta_n,floor_1e9_rho,anomaly\n")
    for n in range(N1, N2 + 1):
        cb = 1
        for i in range(1, n):
            cb = cb * (n - 1 + i) // i
        rhs = (n - 1) * cb
        c, bestv, besta = 1, 0, None
        for a in range(1, n // 2 + 1):
            c = c * (n - a + 1) // a
            v = c * c * a * (n - 2 * a + 1)
            if v > bestv:
                bestv, besta = v, a
        xs = (sqrt(2 * n + 1) - 1) / 4
        delta = abs((n / 2 - besta) - xs)
        f.write(f"{n},{besta},{xs:.4f},{delta:.4f},{(10**9 * bestv) // rhs},{int(bestv > rhs)}\n")
print("wrote", out)
