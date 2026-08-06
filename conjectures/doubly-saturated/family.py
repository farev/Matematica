from itertools import combinations
def circ(n,S):
    S=set(S)|{n-d for d in S}
    return [[(j-i)%n in S for j in range(n)] for i in range(n)]
def hascl(A,k,comp=False):
    n=len(A)
    E=(lambda u,v: not A[u][v]) if comp else (lambda u,v: A[u][v])
    return any(all(E(u,v) for u,v in combinations(c,2)) for c in combinations(range(n),k))
def dsat(A,s,t):
    n=len(A)
    if hascl(A,s) or hascl(A,t,comp=True): return "NOT (s,t)-good"
    for u,v in combinations(range(n),2):
        if A[u][v]:
            C=[w for w in range(n) if w not in (u,v) and not A[u][w] and not A[v][w]]
            if not any(all(not A[a][b] for a,b in combinations(c,2)) for c in combinations(C,t-2)): return f"edge {u}-{v} not critical"
        else:
            C=[w for w in range(n) if w not in (u,v) and A[u][w] and A[v][w]]
            if not any(all(A[a][b] for a,b in combinations(c,2)) for c in combinations(C,s-2)): return f"non-edge {u}-{v} unsaturated"
    return "DOUBLY SATURATED"
for t in (4,5,6,7):
    m=t-2; n=6*t-11; D=[m]+list(range(2*m+1,3*m+1))
    print(f"  (4,{t}): n={n} D={D} -> {dsat(circ(n,D),4,t)}")
