#!/usr/bin/env python3
"""Filter graph6 lines: keep connected cubic claw-free graphs (diamonds allowed).

Definition-level (no structure lemma): for each vertex u with neighbours
{a,b,c}, let inner = #edges among {a,b,c}.  claw at u <=> inner == 0;
diamond through u <=> inner == 2 (for cubic graphs).  Prints surviving
graph6 lines; -v prints "kept/total" to stderr at the end.
"""
import sys


def parse_g6(s):
    n = ord(s[0]) - 63
    bits = []
    for ch in s[1:]:
        v = ord(ch) - 63
        bits += [(v >> b) & 1 for b in range(5, -1, -1)]
    nb = [set() for _ in range(n)]
    k = 0
    for j in range(1, n):
        for i in range(j):
            if bits[k]:
                nb[i].add(j)
                nb[j].add(i)
            k += 1
    return n, nb


def ok(n, nb):
    for u in range(n):
        if len(nb[u]) != 3:
            return False
        a, b, c = nb[u]
        inner = (b in nb[a]) + (c in nb[a]) + (c in nb[b])
        if inner == 0:
            return False
    return True


total = kept = 0
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    total += 1
    n, nb = parse_g6(line)
    if ok(n, nb):
        kept += 1
        print(line)
print("dfcf_filter: kept %d of %d" % (kept, total), file=sys.stderr)
