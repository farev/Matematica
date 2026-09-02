#!/usr/bin/env python3
"""Independent check of a witness assignment.  Usage:
   python3 verify_witness.py k witnessfile [--even q ...] [--fix q=v,...]
Reads R(q) for all primes q up to some bound B, computes R(n) = sum e*R(q) mod k for all
n <= B by a sieve (exact integer arithmetic), and reports the least n with R(n)=R(n+1)=0.
Checks: every prime <= B assigned, even-constraints, and agreement with --fix values.
"""
import sys
import numpy as np
k = int(sys.argv[1]); fn = sys.argv[2]; even = set(); fix = {}
a = sys.argv[3:]
while a:
    if a[0] == '--even': even.add(int(a[1])); a = a[2:]
    elif a[0] == '--fix': fix = {int(t.split('=')[0]): int(t.split('=')[1]) for t in a[1].split(',')}; a = a[2:]
    else: raise SystemExit("bad arg " + a[0])
R = {}
for line in open(fn):
    if line[0] == '#': continue
    q, v = line.split('='); R[int(q)] = int(v) % k
from sympy import nextprime
B = nextprime(max(R)) - 1          # every n <= B+1 factors over the assigned primes
sieve = np.ones(B + 2, dtype=bool); sieve[:2] = False
for i in range(2, int((B + 1) ** 0.5) + 1):
    if sieve[i]: sieve[i * i::i] = False
primes = np.nonzero(sieve)[0]
missing = [int(p) for p in primes if int(p) not in R]
assert not missing, f"unassigned primes: {missing[:10]}..."
for q in even: assert R[q] % 2 == 0, f"R({q}) must be even"
for q, v in fix.items(): assert R[q] == v % k, f"witness disagrees with fixed R({q})={v}"
Rn = np.zeros(B + 2, dtype=np.int64)
for p in primes:
    p = int(p); pw = p
    while pw <= B + 1:
        Rn[pw::pw] += R[p]; pw *= p
Rn %= k
zero = (Rn == 0); zero[0] = False
both = np.nonzero(zero[1:B + 1] & zero[2:B + 2])[0]
least = int(both[0]) + 1 if len(both) else None
print(f"k={k}: {len(primes)} primes assigned up to {B}; least n with R(n)=R(n+1)=0: {least}"
      + (f"  (i.e. all pairs n < {least} avoided; r(k,2,p) >= {least} for every p realising this vector)" if least else f"  (none up to {B})"))
