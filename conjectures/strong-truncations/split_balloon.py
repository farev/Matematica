#!/usr/bin/env python3
"""Split multig -T lines into balloon-free (stdout) and balloon
(file given as argv[1]) streams, by the balloon definition: a doubled
edge whose endpoints share a third neighbour."""
import sys

out_b = open(sys.argv[1], "w")
n_free = n_ball = 0
for line in sys.stdin:
    t = line.split()
    if len(t) < 2:
        continue
    nv, ne = int(t[0]), int(t[1])
    vals = [int(x) for x in t[2:]]
    nb = [set() for _ in range(nv)]
    mult = {}
    for i in range(ne):
        a, b, m = vals[3 * i], vals[3 * i + 1], vals[3 * i + 2]
        mult[(a, b)] = m
        nb[a].add(b)
        nb[b].add(a)
    ball = any(m == 2 and (nb[a] & nb[b]) - {a, b}
               for (a, b), m in mult.items())
    if ball:
        out_b.write(line)
        n_ball += 1
    else:
        sys.stdout.write(line)
        n_free += 1
print("balloon-free %d, balloon %d" % (n_free, n_ball), file=sys.stderr)
