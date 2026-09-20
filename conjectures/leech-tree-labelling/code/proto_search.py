import sys, time
sys.setrecursionlimit(10000)

def solve(n, k):
    N = n*(n-1)//2
    B = N - k
    nodes = 0
    dist = [[-1]*n for _ in range(n)]
    for v in range(n): dist[v][v] = 0
    members = {i:[i] for i in range(n)}
    cnt = [0]*(k+2)
    edges = []
    result = [None]

    def mex():
        for d in range(1, k+1):
            if cnt[d]==0: return d
        return k+1

    def rec(x, q_prev):
        nonlocal nodes
        nodes += 1
        m = mex()
        if m > k:
            result[0] = list(edges) + ['free']; return True
        if len(members) == 1:
            return False
        ids = sorted(members)
        singles = [i for i in ids if len(members[i])==1]
        nonsingles = [i for i in ids if len(members[i])>1]
        cand = nonsingles + singles[:2]
        for q in range(q_prev, m+1):
            for a in range(len(cand)):
                for b in range(a+1, len(cand)):
                    ci, cj = cand[a], cand[b]
                    Ci, Cj = members[ci], members[cj]
                    for u in Ci:
                        for v in Cj:
                            new = [dist[y][u] + q + dist[v][z] for y in Ci for z in Cj]
                            ex = 0; added = []
                            for d in new:
                                if d > k or cnt[d] > 0: ex += 1
                                else: cnt[d] = 1; added.append(d)
                            if x + ex <= B:
                                # merge
                                for y in Ci:
                                    for z in Cj:
                                        d = dist[y][u] + q + dist[v][z]
                                        dist[y][z] = d; dist[z][y] = d
                                members[ci] = Ci + Cj; del members[cj]
                                edges.append((u, v, q))
                                ok = rec(x+ex, q)
                                edges.pop()
                                members[ci] = Ci; members[cj] = Cj
                                for y in Ci:
                                    for z in Cj:
                                        dist[y][z] = -1; dist[z][y] = -1
                                if ok:
                                    for d in added: cnt[d] = 0
                                    return True
                            for d in added: cnt[d] = 0
        return False
    ok = rec(0, 1)
    return ok, nodes, result[0]

if __name__ == '__main__':
    for n in range(2, int(sys.argv[1])+1):
        N = n*(n-1)//2
        k = N
        t0 = time.time()
        # find largest k with a solution: descend from N
        while True:
            ok, nodes, wit = solve(n, k)
            if ok: break
            k -= 1
        print(f"n={n} a(n)={k} (excess {N-k}) nodes_at_k={nodes} time={time.time()-t0:.1f}s witness={wit}")
        sys.stdout.flush()
