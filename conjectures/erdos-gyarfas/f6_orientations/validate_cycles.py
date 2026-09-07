"""Validate the C cycle enumerator against an independent brute-force Python
enumerator (no pruning, dedupe by edge set) on Petersen, Heawood and random
cubic graphs, plus known literature counts."""
import random, subprocess, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))


def write_graph(adj, fn):
    with open(fn, "w") as f:
        f.write(f"{len(adj)}\n")
        for nb in adj:
            f.write(f"{len(nb)} " + " ".join(map(str, nb)) + "\n")


def run_c(adj, L, tag):
    gf = os.path.join(HERE, f"val_{tag}.graph")
    cf = os.path.join(HERE, f"val_{tag}.cycles")
    write_graph(adj, gf)
    res = subprocess.run([os.path.join(HERE, "cycles"), gf, str(L), "3", cf], capture_output=True, text=True, check=True)
    counts = {}
    for line in res.stdout.splitlines():
        _, l, c = line.replace(":", "").split()
        counts[int(l)] = int(c)
    cycles = set()
    with open(cf) as f:
        for line in f:
            parts = list(map(int, line.split()))
            ln, vs = parts[0], parts[1:]
            assert ln == len(vs)
            edges = frozenset(frozenset((vs[i], vs[(i + 1) % ln])) for i in range(ln))
            assert len(edges) == ln
            assert edges not in cycles, "duplicate cycle reported"
            cycles.add(edges)
    return counts, cycles


def brute(adj, L):
    """Every simple cycle of length <= L, as a frozenset of edges."""
    n = len(adj)
    found = set()
    for s in range(n):
        stack = [(s, [s])]
        while stack:
            x, path = stack.pop()
            for y in adj[x]:
                if y == s and len(path) >= 3:
                    edges = frozenset(frozenset((path[i], path[(i + 1) % len(path)])) for i in range(len(path)))
                    found.add(edges)
                elif y not in path and len(path) < L:
                    stack.append((y, path + [y]))
    counts = {}
    for c in found:
        counts[len(c)] = counts.get(len(c), 0) + 1
    return counts, found


def petersen():
    adj = [[] for _ in range(10)]
    def add(u, v):
        adj[u].append(v); adj[v].append(u)
    for i in range(5):
        add(i, (i + 1) % 5); add(i, i + 5); add(5 + i, 5 + (i + 2) % 5)
    return adj


def heawood():
    adj = [[] for _ in range(14)]
    def add(u, v):
        if v not in adj[u]:
            adj[u].append(v); adj[v].append(u)
    for i in range(14):
        add(i, (i + 1) % 14)
        add(i, (i + 5) % 14 if i % 2 == 0 else (i - 5) % 14)
    return adj


def random_cubic(n, rng):
    while True:
        pts = [v for v in range(n) for _ in range(3)]
        rng.shuffle(pts)
        adj = [[] for _ in range(n)]
        ok = True
        for i in range(0, len(pts), 2):
            u, v = pts[i], pts[i + 1]
            if u == v or v in adj[u]:
                ok = False; break
            adj[u].append(v); adj[v].append(u)
        if ok:
            return adj


def check(name, adj, L):
    cc, cs = run_c(adj, L, name)
    bc, bs = brute(adj, L)
    same = (cs == bs)
    print(f"{name}: C counts {dict(sorted(cc.items()))}")
    print(f"{name}: brute  {dict(sorted(bc.items()))}  identical cycle sets: {same}")
    assert same
    return cc


c = check("petersen", petersen(), 10)
assert c.get(5, 0) == 12 and c.get(6, 0) == 10 and c.get(7, 0) == 0 and c.get(8, 0) == 15 and c.get(9, 0) == 20 and c.get(10, 0) == 0, c
print("Petersen matches literature (12,10,0,15,20,0 for lengths 5..10)")
c = check("heawood", heawood(), 14)
assert c.get(6, 0) == 28 and all(c.get(l, 0) == 0 for l in range(3, 6)), c
print("Heawood: girth 6 and 28 six-cycles as expected")
rng = random.Random(12345)
for k in range(3):
    adj = random_cubic(24, rng)
    check(f"rand{k}", adj, 12)
print("ALL VALIDATIONS PASSED")
