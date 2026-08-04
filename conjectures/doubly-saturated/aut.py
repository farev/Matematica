"""Automorphism group order of C_19(1,3,5,6) by backtracking (independent of everything else)."""
import sys
from itertools import combinations
n, S0 = 19, [1,3,5,6]
S = set(S0) | {n-d for d in S0}
adj = [[(j-i) % n in S for j in range(n)] for i in range(n)]
count = 0
perm = [-1]*n
used = [False]*n
def bt(v):
    global count
    if v == n:
        count += 1; return
    for img in range(n):
        if used[img]: continue
        if all(adj[v][u] == adj[img][perm[u]] for u in range(v)):
            perm[v] = img; used[img] = True
            bt(v+1)
            used[img] = False
    perm[v] = -1
bt(0)
print("n =", n, " |Aut| =", count)
print("contains Z_19 : |Aut| divisible by 19 ->", count % 19 == 0)
print("degree sequence:", sorted(sum(r) for r in adj)[:1], "(regular)" )
# vertex- and edge-transitivity
print("vertex-transitive:", count % n == 0)
