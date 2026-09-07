import sys
from itertools import permutations
def good(p):
    n=len(p); pre=[0]
    for x in p: pre.append(pre[-1]+x)
    for L in range(2,n):
        for i in range(0,n-L+1):
            if (pre[i+L]-pre[i])%L==0: return False
    return True
def count(n):
    # backtracking with incremental check
    n_=n; used=[False]*(n+1); a=[0]*n; pre=[0]*(n+1); cnt=0; ex=None
    sys.setrecursionlimit(10000)
    def rec(t):
        nonlocal cnt, ex
        if t==n:
            cnt+=1
            if ex is None: ex=list(a)
            return
        for v in range(1,n+1):
            if used[v]: continue
            pre[t+1]=pre[t]+v
            ok=True
            for L in range(2,t+2):
                if L==n: break
                if (pre[t+1]-pre[t+1-L])%L==0: ok=False; break
            if ok:
                used[v]=True; a[t]=v; rec(t+1); used[v]=False
    rec(0); return cnt, ex
for n in range(1,15):
    c,ex=count(n); print(n,c,ex); sys.stdout.flush()
