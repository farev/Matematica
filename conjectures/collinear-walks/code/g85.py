# Kalviainen's g85 six-step walk: sigma(n) = sum_j (-1)^j b_j(n) mod 4, Cambie offsets, height 4n+sigma
import sys
N = int(sys.argv[1])
def sigma(n):
    s = 0; j = 0
    while n:
        if n & 1: s += (-1)**j
        n >>= 1; j += 1
    return s % 4
sig = [sigma(n) for n in range(N+2)]
c = {0: 0, 1: -1, 2: -1+1j, 3: -1j}
# step vectors v_{r,s} = (2 i^r + c_s - c_r, 4 + s - r)
vecs = {}
letters = []
for n in range(N):
    r, s = sig[n], sig[n+1]
    v = (2*(1j**r) + c[s] - c[r], 4 + s - r)
    key = (int(round(v[0].real)), int(round(v[0].imag)), v[1])
    if key not in vecs: vecs[key] = len(vecs)
    letters.append(vecs[key])
print("distinct step vectors:", len(vecs), sorted(vecs.items(), key=lambda kv: kv[1]))
trans = sorted(set((sig[n], sig[n+1]) for n in range(N)))
print("transitions:", trans)
open("g85_6.txt","w").write("".join(str(x) for x in letters))
# all-pairs valuation check (2): nu2(|w_n-w_m|^2) == nu2(h_n-h_m), for n < M
M = int(sys.argv[2])
z = [0j]*(M+1)
for n in range(M): z[n+1] = z[n] + 1j**sig[n]
def nu2(x):
    x = int(x); assert x != 0; v = 0
    while x % 2 == 0: x //= 2; v += 1
    return v
bad = 0; cnt = 0
for m in range(M):
    for n in range(m+1, M):
        w = 2*(z[n]-z[m]) + c[sig[n]] - c[sig[m]]
        nrm = int(round(w.real))**2 + int(round(w.imag))**2
        h = 4*(n-m) + sig[n] - sig[m]
        cnt += 1
        if nrm == 0 or nu2(nrm) != nu2(h): bad += 1
print("all-pairs identity (2) checked pairs:", cnt, "failures:", bad)
