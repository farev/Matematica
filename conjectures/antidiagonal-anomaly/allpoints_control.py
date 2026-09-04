# Control: for B=(a,n-a) on the antidiagonal (1<=a<n/2), compute f_B(A) over ALL grid points A != B
# (A on the path from (0,0) to (n,n)), and record the argmax set; check the argmax lies in the ten points
# and that (1,0) wins iff the integer criterion holds.
from math import comb
import sys
N = int(sys.argv[1])
def f(n,a,b,c,d):
    # paths through A=(a,b) avoiding B=(c,d)
    tot = comb(a+b,a)*comb(2*n-a-b,n-a)
    if c>=a and d>=b:
        tot -= comb(a+b,a)*comb(c+d-a-b,c-a)*comb(2*n-c-d,n-c)
    elif a>=c and b>=d:
        tot -= comb(c+d,c)*comb(a+b-c-d,a-c)*comb(2*n-a-b,n-a)
    return tot
bad = 0
for n in range(9, N+1):
    rhs=(n-1)*comb(2*n-2,n-1)
    for a in range(1, (n-1)//2 + 1):
        c,d = a, n-a
        best=-1; arg=[]
        for x in range(n+1):
            for y in range(n+1):
                if (x,y) in [(0,0),(n,n),(c,d)]: continue
                v=f(n,x,y,c,d)
                if v>best: best=v; arg=[(x,y)]
                elif v==best: arg.append((x,y))
        crit = comb(n,a)**2*a*(n-2*a+1) > rhs
        ten = {(1,0),(0,1),(1,1),(2,1),(1,2),(n-1,n),(n,n-1),(n-1,n-1),(n-1,n-2),(n-2,n-1)}
        if not set(arg) <= ten: bad += 1; print("argmax outside ten points", n, a, arg)
        wins10 = (1,0) in arg and (1,1) not in arg
        if wins10 != crit: bad += 1; print("criterion mismatch", n, a, arg, crit)
print("checked n=9..%d, mismatches: %d" % (N, bad))
