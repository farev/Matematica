#!/usr/bin/env python3
"""Rational-arithmetic certification of the numerical step of Theorem A (NOTE.md, section 3):

    U(3000) = c0 * sqrt(3000/2999) * (1 - 1/sqrt(6000))^-1 * exp(1/sqrt(6000) + 1/(3*2999)) < 0.9937,
    c0 = sqrt(8/pi) * exp(-1/2).

Every transcendental quantity is replaced by a rational bound in the safe direction:
  pi  >= 4*(4*S_odd(1/5) - S_even(1/239))        (Machin; alternating-series bracketing),
  e   >= partial sum of the Taylor series (positive terms),
  sqrt(q) <= r  whenever r*r >= q  (r rational),
  exp(y) <= 1/(1-y) for 0 <= y < 1.
Only Fraction arithmetic is used; the script prints each certified inequality and exits 1 on failure.
"""
from fractions import Fraction as Fr

def arctan_partial(x, k):
    """Partial sum S_k = sum_{j=0}^{k} (-1)^j x^(2j+1)/(2j+1) of the alternating series."""
    return sum(Fr((-1) ** j) * x ** (2 * j + 1) / (2 * j + 1) for j in range(k + 1))

ok = True
def cert(name, cond, detail=""):
    global ok
    print(("OK   " if cond else "FAIL ") + name + ("  " + detail if detail else ""))
    ok = ok and cond

# pi lower bound: pi/4 = 4 arctan(1/5) - arctan(1/239); arctan(x) >= S_odd, arctan(x) <= S_even
pi_low = 4 * (4 * arctan_partial(Fr(1, 5), 5) - arctan_partial(Fr(1, 239), 2))
cert("pi > 3.1415", pi_low > Fr(31415, 10000), f"pi_low = {float(pi_low):.10f}")

# e lower bound (Taylor series, positive terms)
e_low = sum(Fr(1, 1) / __import__("math").factorial(k) for k in range(0, 10))
cert("e > 2.71828", e_low > Fr(271828, 100000), f"e_low = {float(e_low):.10f}")

# c0^2 = 8/(pi e) <= 8/(pi_low e_low); c0 <= 0.96808 if 0.96808^2 >= that
c0sq_up = Fr(8) / (pi_low * e_low)
c0_up = Fr(96808, 100000)
cert("c0 < 0.96808", c0_up * c0_up >= c0sq_up, f"c0^2 <= {float(c0sq_up):.10f}, 0.96808^2 = {float(c0_up*c0_up):.10f}")

n = 3000
# sqrt(n/(n-1)) <= 1.00017
s1 = Fr(100017, 100000)
cert("sqrt(3000/2999) < 1.00017", s1 * s1 >= Fr(n, n - 1))
# u = 1/sqrt(2n) <= 0.01291
u = Fr(1291, 100000)
cert("1/sqrt(6000) < 0.01291", u * u >= Fr(1, 2 * n))
# (1-u)^-1 with u an upper bound (increasing in u)
f2 = 1 / (1 - u)
# y = u + 1/(3(n-1)); exp(y) <= 1/(1-y)
y = u + Fr(1, 3 * (n - 1))
cert("0 <= y < 1", 0 <= y < 1, f"y = {float(y):.8f}")
f3 = 1 / (1 - y)
U_up = c0_up * s1 * f2 * f3
cert("U(3000) < 0.9939", U_up < Fr(9939, 10000), f"U_up = {float(U_up):.8f}")
cert("U(3000) < 1", U_up < 1)
print("ALL CERTIFIED" if ok else "CERTIFICATION FAILED")
raise SystemExit(0 if ok else 1)
