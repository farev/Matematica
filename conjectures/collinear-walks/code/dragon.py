import sys
N = int(sys.argv[1])
# t'_{2n} = t'_n + (n mod 2), t'_{2n+1} = t'_n + 1 - (n mod 2), mod 4
t = [0]*(N+2)
for n in range(1, N+2):
    m, e = divmod(n, 2)
    t[n] = (t[m] + ((m % 2) if e == 0 else 1 - (m % 2))) % 4
d = [(t[n+1]-t[n]) % 4 for n in range(N+1)]
assert all(x in (1,3) for x in d), set(d)
letters = [2*t[n] + (1 if d[n]==3 else 0) for n in range(N)]
open("dragon8.txt","w").write("".join(str(x) for x in letters))
open("dragon4.txt","w").write("".join(str(x) for x in t[:N]))
print("t' prefix:", t[:32])
print("delta prefix:", [1 if x==1 else -1 for x in d[:32]])
print("letters used:", sorted(set(letters)))
# valuation lemma check: nu_2(|Z_n - Z_m|^2) == nu_2(n-m) whenever t_m == t_n, for n < M
M = int(sys.argv[2])
Z = [0j]*(M+1)
for n in range(M):
    Z[n+1] = Z[n] + 1j**t[n]
def nu2(x):
    x = int(x); assert x != 0; v = 0
    while x % 2 == 0: x //= 2; v += 1
    return v
bad = 0; checked = 0
for m in range(M):
    for n in range(m+1, M):
        if t[m] == t[n]:
            w = Z[n]-Z[m]; nrm = int(round(w.real))**2 + int(round(w.imag))**2
            checked += 1
            if nrm == 0 or nu2(nrm) != nu2(n-m):
                bad += 1
                if bad < 5: print("LEMMA FAILS", m, n, w, nu2(n-m))
print("lemma checked pairs:", checked, "failures:", bad)
