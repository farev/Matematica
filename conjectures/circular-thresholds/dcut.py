"""Longest alpha^+-free word over Sigma_n whose consecutive differences lie in
a set D of size <= 2.  Exhaustive DFS.  Feeds Theorem N' (see NOTE.md §8)."""
import sys, itertools
from pump import afree_fast, RT

def longest(n, alpha, D):
    best = [1]
    w = [0]
    def dfs():
        if len(w) > best[0]:
            best[0] = len(w)
        for d in D:
            w.append((w[-1] + d) % n)
            if afree_fast(w, alpha)[0]:
                dfs()
            w.pop()
    dfs()
    return best[0]

if __name__ == '__main__':
    print('n  alpha    max |h0| with |D|<=2   (argmax D)')
    for n in range(4, int(sys.argv[1]) + 1 if len(sys.argv) > 1 else 9):
        alpha = RT(n)
        bestlen, bestD = 0, None
        for D in itertools.chain(
                ((d,) for d in range(1, n)),
                itertools.combinations(range(1, n), 2)):
            L = longest(n, alpha, D)
            if L > bestlen:
                bestlen, bestD = L, D
        print(f'{n}  {str(alpha):6s}   {bestlen:3d}                  {bestD}')
