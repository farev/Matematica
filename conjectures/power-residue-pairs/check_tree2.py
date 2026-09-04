#!/usr/bin/env python3
"""Streaming independent checker for a tree2 certificate (gzip).  Usage:
   python3 check_tree2.py k pairsfile cert.gz
Verifies:  (1) exhaustiveness -- leaves are in DFS order; at every internal node the
children's values cover the allowed values of the branching prime up to the node's
stabiliser in (Z/k)^* (unit symmetry R -> uR);  (2) every leaf is settled: its pair
(n, n+1) has n <= L and both members are k-th power residues under the leaf's
assignment (all their primes assigned);  (3) no unsettled leaves.  Exact arithmetic.
Then: every admissible R (R(q) even for q in the even-list) settles a pair n <= U :=
max leaf n, hence Lambda(k,2) <= U (for all primes p larger than every prime of S).
"""
import sys, gzip
from math import gcd
k = int(sys.argv[1]); L = None; even = set(); fixed = {}
pairs = {}
for line in open(sys.argv[2]):
    if line[0] == '#': continue
    n, fa, fb = line.split()
    fac = lambda s: [] if s == '1' else [(int(p), int(e) % k) for p, e in (t.split('^') for t in s.split(','))]
    pairs[int(n)] = ([(p, e) for p, e in fac(fa) if e], [(p, e) for p, e in fac(fb) if e])
units = [u for u in range(1, k) if gcd(u, k) == 1]
def allowed(q): return set(range(0, k, 2)) if q in even else set(range(k))
def stab(H, v): return [u for u in H if (u * v) % k == v]
def is_res(member, A): return all(q in A for q, e in member) and sum(e * A[q] for q, e in member) % k == 0
stack = []      # per level: [q, H_at_node, values_seen]
prev = None; nleaves = 0; U = -1; unsettled = 0; hist = {}
def close_level(lv):
    q, H, seen = lv
    cov = {(u * v) % k for v in seen for u in H}
    assert cov == allowed(q), ("children do not cover", q, sorted(seen), H, sorted(cov))
with gzip.open(sys.argv[3], 'rt') as f:
    for line in f:
        if line[0] == '#':
            if line.startswith('# k='):
                hdr = dict(t.split('=') for t in line[2:].split() if '=' in t); assert int(hdr['k']) == k; L = int(hdr['L'])
            elif line.startswith('# even:'): even = set(map(int, line.split(':')[1].split()))
            elif line.startswith('# fix:'): fixed = {int(a): int(b) for a, b in (t.split('=') for t in line.split(':')[1].split())}
            continue
        path, n = line.split('|'); n = int(n)
        dec = [(int(a), int(b)) for a, b in (t.split('=') for t in path.split())]
        nleaves += 1
        A = dict(fixed);
        for q, v in dec:
            assert q not in A and v in allowed(q), ("bad decision", dec); A[q] = v
        if n < 0: unsettled += 1
        else:
            assert n <= L and n in pairs, ("settling pair not in list / above L", n)
            m0, m1 = pairs[n]; assert is_res(m0, A) and is_res(m1, A), ("leaf not settled", dec, n)
            U = max(U, n); hist[n] = hist.get(n, 0) + 1
        # exhaustiveness bookkeeping (DFS order)
        if prev is None:
            H = units
            for q, v in fixed.items(): H = stab(H, v)
            for q, v in dec: stack.append([q, H, {v}]); H = stab(H, v)
        else:
            c = 0
            while c < len(prev) and c < len(dec) and prev[c] == dec[c]: c += 1
            assert c < len(prev) and c < len(dec), ("leaf path is prefix of another", prev, dec)
            while len(stack) > c + 1: close_level(stack.pop())
            assert stack[c][0] == dec[c][0], ("branching prime changed within node", prev, dec)
            stack[c][2].add(dec[c][1])
            H = stab(stack[c][1], dec[c][1])
            for q, v in dec[c + 1:]: stack.append([q, H, {v}]); H = stab(H, v)
        prev = dec
while stack: close_level(stack.pop())
print(f"k={k} L={L} even={sorted(even)} fixed={fixed}: {nleaves} leaves; tree exhaustive; unsettled={unsettled}; "
      f"all settled leaves verified; U = max settling n = {U}")
print("largest settling values:", sorted(hist.items(), reverse=True)[:8])
if unsettled: print("WARNING: unsettled leaves present -- no upper bound proved")
