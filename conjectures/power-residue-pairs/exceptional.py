# brute force: primes p = 1 (mod k) with NO pair of consecutive k-th power residues at all
import sys
from sympy import primerange
k = int(sys.argv[1]); B = int(sys.argv[2])
exc = []
for p in primerange(k+1, B):
    if (p-1) % k: continue
    # k-th power residues: x^k mod p for x=1..p-1 -> set bits
    res = bytearray(p)
    for x in range(1, p):
        res[pow(x, k, p)] = 1
    ok = any(res[n] and res[n+1] for n in range(1, p-1))
    if not ok: exc.append(p)
print(f"k={k}: exceptional primes (p=1 mod k, p<{B}):", exc)
