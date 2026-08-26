#!/usr/bin/env python3
"""Cross-check: is every chi'_s = 7 quotient in the census bridged?
Reads census records, rebuilds H as a multigraph, finds bridges
(multi-edges are never bridges), tabulates verdict x bridged."""
import sys
from collections import Counter

def parse_H(raw):
    t = raw.split(); nv, ne = int(t[0]), int(t[1])
    v = [int(x) for x in t[2:]]
    edges = []          # expanded edge instances
    for i in range(ne):
        a, b, m = v[3*i], v[3*i+1], v[3*i+2]
        edges += [(a, b)] * m
    return nv, edges

def bridges(nv, edges):
    adj = [[] for _ in range(nv)]
    for i, (a, b) in enumerate(edges):
        adj[a].append((b, i)); adj[b].append((a, i))
    disc = [-1]*nv; low = [0]*nv; out = []; t = [0]
    for s in range(nv):
        if disc[s] != -1: continue
        st = [(s, -1, iter(adj[s]))]; disc[s] = low[s] = t[0]; t[0] += 1
        while st:
            u, pe, it = st[-1]
            adv = False
            for w, ei in it:
                if ei == pe: continue
                if disc[w] == -1:
                    disc[w] = low[w] = t[0]; t[0] += 1
                    st.append((w, ei, iter(adj[w]))); adv = True; break
                low[u] = min(low[u], disc[w])
            if not adv:
                st.pop()
                if st:
                    p = st[-1][0]
                    low[p] = min(low[p], low[u])
                    if low[u] > disc[p]: out.append(pe)
    return out

tab = Counter(); bad = []; per = {}
for fn in sys.argv[1:]:
    for line in open(fn):
        if not line.startswith("R "): continue
        head, _, raw = line.partition(" | ")
        verdict = head.split()[4]; raw = raw.strip()
        if not raw or not raw[0].isdigit(): continue
        nv, edges = parse_H(raw)
        br = len(bridges(nv, edges)) > 0
        v = "7" if verdict.startswith("NOT") else "6"
        tab[(v, br)] += 1
        per.setdefault(nv, Counter())[(v, br)] += 1
        if v == "7" and not br: bad.append((fn, line.rstrip()[:120]))
print("verdict  bridged   count")
for (v, br), n in sorted(tab.items()):
    print("   %s      %-5s     %d" % (v, br, n))
print()
print("order   total   6/bridgeless   6/bridged   7/bridged   7/bridgeless")
for nv in sorted(per):
    c = per[nv]; t = sum(c.values())
    print("%5d %7d %14d %11d %11d %14d" % (
        nv, t, c[("6", False)], c[("6", True)], c[("7", True)], c[("7", False)]))
if bad:
    print("\nBRIDGELESS chi'_s=7 QUOTIENTS FOUND:")
    for fn, l in bad[:20]: print(" ", fn, l)
    print(" (%d total)" % len(bad))
else:
    print("\nno bridgeless quotient has chi'_s = 7 in these files")
