# valuation defects nu2(|Z_n-Z_m|^2) - nu2(n-m) by boundary class d = t_n - t_m mod 4, dragon walk
from collections import Counter
M = 2048
t = [0]*(M+2)
for n in range(1, M+2):
    m, e = divmod(n, 2)
    t[n] = (t[m] + ((m % 2) if e == 0 else 1 - (m % 2))) % 4
Z = [0j]*(M+1)
for n in range(M): Z[n+1] = Z[n] + 1j**t[n]
def nu2(x):
    x = int(x)
    if x == 0: return 99
    v = 0
    while x % 2 == 0: x //= 2; v += 1
    return v
def nrm(w): return int(round(w.real))**2 + int(round(w.imag))**2
tab = {d: Counter() for d in range(4)}
tabW = {d: Counter() for d in range(4)}
for m in range(M):
    for n in range(m+1, M):
        d = (t[n]-t[m]) % 4
        e = nu2(n-m)
        tab[d][nu2(nrm(Z[n]-Z[m])) - e] += 1
        # 2W = 2Z + (1+i)u ; nu2(|2W_n-2W_m|^2) = nu2(|W..|^2)+2
        u_n = 1j**t[n]; u_m = 1j**t[m]
        W2 = 2*(Z[n]-Z[m]) + (1+1j)*(u_n-u_m)
        tabW[d][nu2(nrm(W2)) - 2 - e] += 1
for d in range(4):
    print("Z: class d=%d:" % d, sorted(tab[d].items()))
for d in range(4):
    print("W: class d=%d:" % d, sorted(tabW[d].items()))
